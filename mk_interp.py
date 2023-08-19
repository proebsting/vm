from argparse import Namespace, ArgumentParser
import json
from typing import List, Dict, TextIO, Optional, NamedTuple, Any


class Operand(NamedTuple):
    name: str
    type: str


class Stack(NamedTuple):
    before: List[str]
    after: List[str]


class Operation(NamedTuple):
    cls: str
    short: str
    operands: List[Operand]
    stack: Stack
    memory: Optional[Stack]
    side_effects: Optional[str]


def get_args() -> Namespace:
    ap = ArgumentParser(description="Create parser and scanner components")
    ap.add_argument("--spec", required=True, help="The file to read")
    ap.add_argument("--ebnf", help="The ebnf file to write")
    ap.add_argument("--insns", help="The insns file to write")
    return ap.parse_args()


epilogue = """
%% string.return = "str"
string : STR'tok =<< tok.value >> .

%% reg.return = "str"
reg : ID'tok =<< tok.value>> .

%% integer.return = "int"
integer : INT'tok =<< int(tok.value) >> .

%% comment.return = "str"
comment : ( string | =<<"">> ) .
"""

prologue = """
<< from .vm import * >>
<< from .scanner import Token, Scanner >>

%% start.return = "List[Insn]"
start : {operation} .
%% operation.return = "Insn"
operation :
"""

type_to_nonterminal = {
    "int": "integer",
    "str": "string",
}


def gen_ebnf(args: Namespace, spec: List[Operation]):
    if not args.ebnf:
        return
    with open(args.ebnf, "w") as f:
        f.write(prologue)
        leading = "  "
        for operation in spec:
            opstring = (
                f'("{operation.cls}" | "{operation.short}")'
                if operation.short
                else f'"{operation.cls}"'
            )
            reg = regs(operation)
            imms = [f"reg'{x}" for x in reg]
            for operand in operation.operands:
                imms.append(
                    f"{type_to_nonterminal[operand.type]}'{operand.name} "
                )
            imms += ["comment'cmt"]
            arg = (
                reg
                + [operand.name for operand in operation.operands]
                + ["cmt"]
            )
            arguments = ", ".join(arg)
            argstring = ' [","] '.join(imms)
            f.write(
                f"    {leading}{opstring} {argstring} =<< {operation.cls}({arguments}) >>\n"
            )
            leading = "| "
        f.write("    .\n")
        f.write(epilogue)


def gen_reserved(f: TextIO, spec: List[Operation]):
    f.write("reserved = [\n")
    for operation in spec:
        f.write(f'    "{operation.cls}",\n')
        f.write(f'    "{operation.short}",\n')
    f.write("]\n")


def regs(operation: Operation) -> List[str]:
    regs: List[str] = []
    regs += ["dst"] if operation.stack.after else []
    regs += operation.stack.before
    return regs


prol = """
class Insn:
    def execute(
        self, memory: List[int], registers: Dict[str, int], labels: Dict[str, int]
    ) -> None:
        raise NotImplementedError(f"execute not implemented for {self.__class__}")

    def disasm(self, long: bool = False) -> str:
        raise NotImplementedError(f"disasm not implemented for {self.__class__}")
"""


def gen_classes(f: TextIO, spec: List[Operation]):
    f.write(prol)
    for operation in spec:
        gen_class(f, operation)


def gen_class(f: TextIO, operation: Operation):
    f.write("@dataclass\n")
    f.write(f"class {operation.cls}(Insn):\n")
    gen_class_fields(f, operation)
    gen_class_execute_method(f, operation)
    gen_class_disasm_method(f, operation)


def gen_class_disasm_method(f: TextIO, operation: Operation):
    s = "{op}"
    comma = ""
    if operation.stack.after:
        s += " {self.dst}"
        comma = ","
    for reg in operation.stack.before:
        s += f"{comma} {{self.{reg} }}"
        comma = ","
    for operand in operation.operands:
        s += f"{comma} {{self.{operand.name}.__repr__() }}"
        comma = ","
    cmt = f"            cmt:str = '' if not self.comment else f' <<{{self.comment}}>>'\n"
    s += "  {cmt}"
    ret = f"            return f'{s}'\n"
    f.write(f"    def disasm(self, long:bool=False)->str:\n")
    f.write(
        f"            op:str = '{operation.cls}' if long else '{operation.short}'\n"
    )
    f.write(cmt)
    f.write(ret)


def gen_class_execute_method(f: TextIO, operation: Operation):
    def embellish(s: str) -> str:
        for reg in ["PC", "RA"]:
            s = s.replace(f"{reg}", f"registers['{reg}']")
        for reg in operation.stack.before:
            s = s.replace(f"{reg}", f"registers[self.{reg}]")
        for x in operation.operands:
            if x.name == "label":
                s = s.replace("label", "labels[self.label]")
            else:
                s = s.replace(f"{x.name}", f"self.{x.name}")
        return s

    f.write(
        f"    def execute(self, memory:Memory, registers:Registers, labels:Labels) -> None:\n"
    )
    if not (operation.stack.after or operation.side_effects):
        f.write("        pass\n")
    if operation.stack.after:
        assert len(operation.stack.after) == 1
        e = embellish(operation.stack.after[0])
        f.write(f"        registers[self.dst] = {e}\n")
    if operation.side_effects:
        for se in operation.side_effects:
            e = embellish(se)
            f.write(f"        {e}\n")
    f.write("\n")


def gen_class_fields(f: TextIO, operation: Operation):
    if operation.stack.after:
        assert len(operation.stack.after) == 1, operation.stack.after
        f.write("    dst:str\n")
    for reg in operation.stack.before:
        f.write(f"    {reg}: str\n")
    for operand in operation.operands:
        f.write(f"    {operand.name}:{operand.type}\n")
    f.write("    comment: str = ''\n")


def gen_insns(args: Namespace, spec: List[Operation]):
    if not args.insns:
        return
    prologue = """
from typing import List, Dict, NoReturn, TypeAlias
from dataclasses import dataclass

Registers:TypeAlias = Dict[str, int]
Labels:TypeAlias = Dict[str, int]
Memory:TypeAlias = List[int]

@dataclass
class VM_Error(Exception):
    msg:str

def halt() -> NoReturn:
    raise VM_Error("Halt")
"""
    with open(args.insns, "w") as f:
        f.write(prologue)
        gen_classes(f, spec)
        # gen_disasm(f, spec)
        gen_reserved(f, spec)


def convert_spec(js: List[Dict[str, Any]]) -> List[Operation]:
    operations: List[Operation] = []
    operation: Dict[str, Any]
    for operation in js:
        operands: List[Operand] = (
            [
                Operand(name=op["name"], type=op["type"])
                for op in operation["operands"]
            ]
            if "operands" in operation
            else []
        )
        stack = Stack(
            before=operation["stack"]["before"],
            after=operation["stack"]["after"],
        )
        memory = (
            Stack(
                before=operation["memory"]["before"],
                after=operation["memory"]["after"],
            )
            if "memory" in operation
            else None
        )
        side_effect = (
            operation["side_effect"] if "side_effect" in operation else None
        )
        operations.append(
            Operation(
                cls=operation["class"],
                short=operation["short"],
                operands=operands,
                stack=stack,
                memory=memory,
                side_effects=side_effect,
            )
        )
    return operations


def main():
    args = get_args()
    # read args.spec as json file
    with open(args.spec) as f:
        spec: List[Operation] = convert_spec(json.load(f))

    gen_ebnf(args, spec)
    gen_insns(args, spec)


if __name__ == "__main__":
    main()
