from typing import List, Dict, NoReturn, TypeAlias
from dataclasses import dataclass

Registers: TypeAlias = Dict[str, int]
Labels: TypeAlias = Dict[str, int]
Memory: TypeAlias = List[int]


def halt() -> NoReturn:
    raise Exception("Halt")


class Insn:
    def execute(
        self, memory: List[int], registers: Dict[str, int], labels: Dict[str, int]
    ) -> None:
        raise NotImplementedError(f"execute not implemented for {self.__class__}")

    def disasm(self, long: bool = False) -> str:
        raise NotImplementedError(f"disasm not implemented for {self.__class__}")


@dataclass
class Label(Insn):
    label: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        pass

    def disasm(self, long: bool = False) -> str:
        op: str = "Label" if long else "lab"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.label.__repr__() }  {cmt}"


@dataclass
class Noop(Insn):
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        pass

    def disasm(self, long: bool = False) -> str:
        op: str = "Noop" if long else "noop"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op}  {cmt}"


@dataclass
class Jump(Insn):
    label: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers["PC"] = labels[self.label]

    def disasm(self, long: bool = False) -> str:
        op: str = "Jump" if long else "j"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.label.__repr__() }  {cmt}"


@dataclass
class JumpIfZero(Insn):
    v: str
    label: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        if registers[self.v] == 0:
            registers["PC"] = labels[self.label]

    def disasm(self, long: bool = False) -> str:
        op: str = "JumpIfZero" if long else "jz"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.v }, {self.label.__repr__() }  {cmt}"


@dataclass
class JumpIfNotZero(Insn):
    v: str
    label: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        if registers[self.v] != 0:
            registers["PC"] = labels[self.label]

    def disasm(self, long: bool = False) -> str:
        op: str = "JumpIfNotZero" if long else "jnz"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.v }, {self.label.__repr__() }  {cmt}"


@dataclass
class JumpIndirect(Insn):
    v: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers["PC"] = registers[self.v]

    def disasm(self, long: bool = False) -> str:
        op: str = "JumpIndirect" if long else "ji"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.v }  {cmt}"


@dataclass
class Immediate(Insn):
    dst: str
    value: int
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = self.value

    def disasm(self, long: bool = False) -> str:
        op: str = "Immediate" if long else "imm"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.value.__repr__() }  {cmt}"


@dataclass
class LoadLabel(Insn):
    dst: str
    label: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = labels[self.label]

    def disasm(self, long: bool = False) -> str:
        op: str = "LoadLabel" if long else "llabel"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.label.__repr__() }  {cmt}"


@dataclass
class Move(Insn):
    dst: str
    x: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = registers[self.x]

    def disasm(self, long: bool = False) -> str:
        op: str = "Move" if long else "move"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.x }  {cmt}"


@dataclass
class Add(Insn):
    dst: str
    x: str
    y: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = registers[self.x] + registers[self.y]

    def disasm(self, long: bool = False) -> str:
        op: str = "Add" if long else "add"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.x }, {self.y }  {cmt}"


@dataclass
class AddImmediate(Insn):
    dst: str
    x: str
    value: int
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = registers[self.x] + self.value

    def disasm(self, long: bool = False) -> str:
        op: str = "AddImmediate" if long else "addi"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.x }, {self.value.__repr__() }  {cmt}"


@dataclass
class Sub(Insn):
    dst: str
    x: str
    y: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = registers[self.x] - registers[self.y]

    def disasm(self, long: bool = False) -> str:
        op: str = "Sub" if long else "sub"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.x }, {self.y }  {cmt}"


@dataclass
class Mul(Insn):
    dst: str
    x: str
    y: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = registers[self.x] * registers[self.y]

    def disasm(self, long: bool = False) -> str:
        op: str = "Mul" if long else "mul"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.x }, {self.y }  {cmt}"


@dataclass
class Div(Insn):
    dst: str
    x: str
    y: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = registers[self.x] // registers[self.y]

    def disasm(self, long: bool = False) -> str:
        op: str = "Div" if long else "div"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.x }, {self.y }  {cmt}"


@dataclass
class Negate(Insn):
    dst: str
    v: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = -registers[self.v]

    def disasm(self, long: bool = False) -> str:
        op: str = "Negate" if long else "neg"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.v }  {cmt}"


@dataclass
class LessThan(Insn):
    dst: str
    x: str
    y: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = int(registers[self.x] < registers[self.y])

    def disasm(self, long: bool = False) -> str:
        op: str = "LessThan" if long else "lt"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.x }, {self.y }  {cmt}"


@dataclass
class GreaterThan(Insn):
    dst: str
    x: str
    y: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = int(registers[self.x] > registers[self.y])

    def disasm(self, long: bool = False) -> str:
        op: str = "GreaterThan" if long else "gt"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.x }, {self.y }  {cmt}"


@dataclass
class LessThanEqual(Insn):
    dst: str
    x: str
    y: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = int(registers[self.x] <= registers[self.y])

    def disasm(self, long: bool = False) -> str:
        op: str = "LessThanEqual" if long else "leq"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.x }, {self.y }  {cmt}"


@dataclass
class GreaterThanEqual(Insn):
    dst: str
    x: str
    y: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = int(registers[self.x] >= registers[self.y])

    def disasm(self, long: bool = False) -> str:
        op: str = "GreaterThanEqual" if long else "geq"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.x }, {self.y }  {cmt}"


@dataclass
class Equal(Insn):
    dst: str
    x: str
    y: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = int(registers[self.x] == registers[self.y])

    def disasm(self, long: bool = False) -> str:
        op: str = "Equal" if long else "eq"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.x }, {self.y }  {cmt}"


@dataclass
class NotEqual(Insn):
    dst: str
    x: str
    y: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = int(registers[self.x] != registers[self.y])

    def disasm(self, long: bool = False) -> str:
        op: str = "NotEqual" if long else "neq"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.x }, {self.y }  {cmt}"


@dataclass
class Not(Insn):
    dst: str
    v: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = 1 - registers[self.v]

    def disasm(self, long: bool = False) -> str:
        op: str = "Not" if long else "not"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.v }  {cmt}"


@dataclass
class Load(Insn):
    dst: str
    address: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers[self.dst] = memory[registers[self.address]]

    def disasm(self, long: bool = False) -> str:
        op: str = "Load" if long else "ld"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.dst}, {self.address }  {cmt}"


@dataclass
class Store(Insn):
    address: str
    v: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        memory[registers[self.address]] = registers[self.v]

    def disasm(self, long: bool = False) -> str:
        op: str = "Store" if long else "st"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.address }, {self.v }  {cmt}"


@dataclass
class Print(Insn):
    v: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        print(registers[self.v])

    def disasm(self, long: bool = False) -> str:
        op: str = "Print" if long else "print"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.v }  {cmt}"


@dataclass
class CallIndirect(Insn):
    v: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers["RA"] = registers["PC"]
        registers["PC"] = registers[self.v]

    def disasm(self, long: bool = False) -> str:
        op: str = "CallIndirect" if long else "calli"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.v }  {cmt}"


@dataclass
class Call(Insn):
    label: str
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        registers["RA"] = registers["PC"]
        registers["PC"] = labels[self.label]

    def disasm(self, long: bool = False) -> str:
        op: str = "Call" if long else "call"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op} {self.label.__repr__() }  {cmt}"


@dataclass
class Halt(Insn):
    comment: str = ""

    def execute(self, memory: Memory, registers: Registers, labels: Labels) -> None:
        halt()

    def disasm(self, long: bool = False) -> str:
        op: str = "Halt" if long else "halt"
        cmt: str = "" if not self.comment else f" <<{self.comment}>>"
        return f"{op}  {cmt}"


reserved = [
    "Label",
    "lab",
    "Noop",
    "noop",
    "Jump",
    "j",
    "JumpIfZero",
    "jz",
    "JumpIfNotZero",
    "jnz",
    "JumpIndirect",
    "ji",
    "Immediate",
    "imm",
    "LoadLabel",
    "llabel",
    "Move",
    "move",
    "Add",
    "add",
    "AddImmediate",
    "addi",
    "Sub",
    "sub",
    "Mul",
    "mul",
    "Div",
    "div",
    "Negate",
    "neg",
    "LessThan",
    "lt",
    "GreaterThan",
    "gt",
    "LessThanEqual",
    "leq",
    "GreaterThanEqual",
    "geq",
    "Equal",
    "eq",
    "NotEqual",
    "neq",
    "Not",
    "not",
    "Load",
    "ld",
    "Store",
    "st",
    "Print",
    "print",
    "CallIndirect",
    "calli",
    "Call",
    "call",
    "Halt",
    "halt",
]
