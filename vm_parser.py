from .vm import *
from .scanner import Token, Scanner

from typing import NoReturn, Set


class ParseErrorException(Exception):
    msg: str
    token: Token
    expected: Set[str]

    def __init__(self, msg: str, current: Token, expected: Set[str]):
        self.msg = msg
        self.current = current
        self.expected = expected

    def __str__(self):
        return f"Parse error {self.msg} at {self.current}:  Expected {self.expected}"


class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner: Scanner = scanner

    def error(self, msg: str, expected: Set[str]) -> NoReturn:
        current: Token = self.scanner.peek()
        raise ParseErrorException(msg, current, expected)

    def match(self, kind: str) -> Token:
        if self.current() == kind:
            return self.scanner.consume()
        else:
            self.error("", {kind})

    def current(self) -> str:
        return self.scanner.peek().kind

    def parse(self):
        v = self._start()
        self.match("EOF")
        return v

    def _start(self) -> List[Insn]:
        # start -> { operation }
        _start_: List[Insn]
        _start_ = []
        while self.current() in {
            "Add",
            "AddImmediate",
            "Call",
            "CallIndirect",
            "Div",
            "Equal",
            "GreaterThan",
            "GreaterThanEqual",
            "Halt",
            "Immediate",
            "Jump",
            "JumpIfNotZero",
            "JumpIfZero",
            "JumpIndirect",
            "Label",
            "LessThan",
            "LessThanEqual",
            "Load",
            "LoadLabel",
            "Move",
            "Mul",
            "Negate",
            "Noop",
            "Not",
            "NotEqual",
            "Print",
            "Store",
            "Sub",
            "add",
            "addi",
            "call",
            "calli",
            "div",
            "eq",
            "geq",
            "gt",
            "halt",
            "imm",
            "j",
            "ji",
            "jnz",
            "jz",
            "lab",
            "ld",
            "leq",
            "llabel",
            "lt",
            "move",
            "mul",
            "neg",
            "neq",
            "noop",
            "not",
            "print",
            "st",
            "sub",
        }:
            _start__element_ = self._operation()
            _start_.append(_start__element_)
        return _start_

    def _operation(self) -> Insn:
        # operation -> ("Label" | "lab") string'label [ "," ] comment'cmt =«Label(label, cmt)» | ("Noop" | "noop") comment'cmt =«Noop(cmt)» | ("Jump" | "j") string'label [ "," ] comment'cmt =«Jump(label, cmt)» | ("JumpIfZero" | "jz") reg'v [ "," ] string'label [ "," ] comment'cmt =«JumpIfZero(v, label, cmt)» | ("JumpIfNotZero" | "jnz") reg'v [ "," ] string'label [ "," ] comment'cmt =«JumpIfNotZero(v, label, cmt)» | ("JumpIndirect" | "ji") reg'v [ "," ] comment'cmt =«JumpIndirect(v, cmt)» | ("Immediate" | "imm") reg'dst [ "," ] integer'value [ "," ] comment'cmt =«Immediate(dst, value, cmt)» | ("LoadLabel" | "llabel") reg'dst [ "," ] string'label [ "," ] comment'cmt =«LoadLabel(dst, label, cmt)» | ("Move" | "move") reg'dst [ "," ] reg'x [ "," ] comment'cmt =«Move(dst, x, cmt)» | ("Add" | "add") reg'dst [ "," ] reg'x [ "," ] reg'y [ "," ] comment'cmt =«Add(dst, x, y, cmt)» | ("AddImmediate" | "addi") reg'dst [ "," ] reg'x [ "," ] integer'value [ "," ] comment'cmt =«AddImmediate(dst, x, value, cmt)» | ("Sub" | "sub") reg'dst [ "," ] reg'x [ "," ] reg'y [ "," ] comment'cmt =«Sub(dst, x, y, cmt)» | ("Mul" | "mul") reg'dst [ "," ] reg'x [ "," ] reg'y [ "," ] comment'cmt =«Mul(dst, x, y, cmt)» | ("Div" | "div") reg'dst [ "," ] reg'x [ "," ] reg'y [ "," ] comment'cmt =«Div(dst, x, y, cmt)» | ("Negate" | "neg") reg'dst [ "," ] reg'v [ "," ] comment'cmt =«Negate(dst, v, cmt)» | ("LessThan" | "lt") reg'dst [ "," ] reg'x [ "," ] reg'y [ "," ] comment'cmt =«LessThan(dst, x, y, cmt)» | ("GreaterThan" | "gt") reg'dst [ "," ] reg'x [ "," ] reg'y [ "," ] comment'cmt =«GreaterThan(dst, x, y, cmt)» | ("LessThanEqual" | "leq") reg'dst [ "," ] reg'x [ "," ] reg'y [ "," ] comment'cmt =«LessThanEqual(dst, x, y, cmt)» | ("GreaterThanEqual" | "geq") reg'dst [ "," ] reg'x [ "," ] reg'y [ "," ] comment'cmt =«GreaterThanEqual(dst, x, y, cmt)» | ("Equal" | "eq") reg'dst [ "," ] reg'x [ "," ] reg'y [ "," ] comment'cmt =«Equal(dst, x, y, cmt)» | ("NotEqual" | "neq") reg'dst [ "," ] reg'x [ "," ] reg'y [ "," ] comment'cmt =«NotEqual(dst, x, y, cmt)» | ("Not" | "not") reg'dst [ "," ] reg'v [ "," ] comment'cmt =«Not(dst, v, cmt)» | ("Load" | "ld") reg'dst [ "," ] reg'address [ "," ] comment'cmt =«Load(dst, address, cmt)» | ("Store" | "st") reg'address [ "," ] reg'v [ "," ] comment'cmt =«Store(address, v, cmt)» | ("Print" | "print") reg'v [ "," ] comment'cmt =«Print(v, cmt)» | ("CallIndirect" | "calli") reg'v [ "," ] comment'cmt =«CallIndirect(v, cmt)» | ("Call" | "call") string'label [ "," ] comment'cmt =«Call(label, cmt)» | ("Halt" | "halt") comment'cmt =«Halt(cmt)»
        _operation_: Insn
        if self.current() in {"Label", "lab"}:
            if self.current() in {"Label"}:
                self.match("Label")
            elif self.current() in {"lab"}:
                self.match("lab")
            else:
                self.error("syntax error", {'"Label"', '"lab"'})
            label = self._string()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Label(label, cmt)
        elif self.current() in {"Noop", "noop"}:
            if self.current() in {"Noop"}:
                self.match("Noop")
            elif self.current() in {"noop"}:
                self.match("noop")
            else:
                self.error("syntax error", {'"noop"', '"Noop"'})
            cmt = self._comment()
            _operation_ = Noop(cmt)
        elif self.current() in {"Jump", "j"}:
            if self.current() in {"Jump"}:
                self.match("Jump")
            elif self.current() in {"j"}:
                self.match("j")
            else:
                self.error("syntax error", {'"j"', '"Jump"'})
            label = self._string()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Jump(label, cmt)
        elif self.current() in {"JumpIfZero", "jz"}:
            if self.current() in {"JumpIfZero"}:
                self.match("JumpIfZero")
            elif self.current() in {"jz"}:
                self.match("jz")
            else:
                self.error("syntax error", {'"JumpIfZero"', '"jz"'})
            v = self._reg()
            if self.current() in {","}:
                self.match(",")
            label = self._string()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = JumpIfZero(v, label, cmt)
        elif self.current() in {"JumpIfNotZero", "jnz"}:
            if self.current() in {"JumpIfNotZero"}:
                self.match("JumpIfNotZero")
            elif self.current() in {"jnz"}:
                self.match("jnz")
            else:
                self.error("syntax error", {'"JumpIfNotZero"', '"jnz"'})
            v = self._reg()
            if self.current() in {","}:
                self.match(",")
            label = self._string()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = JumpIfNotZero(v, label, cmt)
        elif self.current() in {"JumpIndirect", "ji"}:
            if self.current() in {"JumpIndirect"}:
                self.match("JumpIndirect")
            elif self.current() in {"ji"}:
                self.match("ji")
            else:
                self.error("syntax error", {'"ji"', '"JumpIndirect"'})
            v = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = JumpIndirect(v, cmt)
        elif self.current() in {"Immediate", "imm"}:
            if self.current() in {"Immediate"}:
                self.match("Immediate")
            elif self.current() in {"imm"}:
                self.match("imm")
            else:
                self.error("syntax error", {'"imm"', '"Immediate"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            value = self._integer()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Immediate(dst, value, cmt)
        elif self.current() in {"LoadLabel", "llabel"}:
            if self.current() in {"LoadLabel"}:
                self.match("LoadLabel")
            elif self.current() in {"llabel"}:
                self.match("llabel")
            else:
                self.error("syntax error", {'"llabel"', '"LoadLabel"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            label = self._string()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = LoadLabel(dst, label, cmt)
        elif self.current() in {"Move", "move"}:
            if self.current() in {"Move"}:
                self.match("Move")
            elif self.current() in {"move"}:
                self.match("move")
            else:
                self.error("syntax error", {'"Move"', '"move"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            x = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Move(dst, x, cmt)
        elif self.current() in {"Add", "add"}:
            if self.current() in {"Add"}:
                self.match("Add")
            elif self.current() in {"add"}:
                self.match("add")
            else:
                self.error("syntax error", {'"add"', '"Add"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            x = self._reg()
            if self.current() in {","}:
                self.match(",")
            y = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Add(dst, x, y, cmt)
        elif self.current() in {"AddImmediate", "addi"}:
            if self.current() in {"AddImmediate"}:
                self.match("AddImmediate")
            elif self.current() in {"addi"}:
                self.match("addi")
            else:
                self.error("syntax error", {'"AddImmediate"', '"addi"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            x = self._reg()
            if self.current() in {","}:
                self.match(",")
            value = self._integer()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = AddImmediate(dst, x, value, cmt)
        elif self.current() in {"Sub", "sub"}:
            if self.current() in {"Sub"}:
                self.match("Sub")
            elif self.current() in {"sub"}:
                self.match("sub")
            else:
                self.error("syntax error", {'"Sub"', '"sub"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            x = self._reg()
            if self.current() in {","}:
                self.match(",")
            y = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Sub(dst, x, y, cmt)
        elif self.current() in {"Mul", "mul"}:
            if self.current() in {"Mul"}:
                self.match("Mul")
            elif self.current() in {"mul"}:
                self.match("mul")
            else:
                self.error("syntax error", {'"mul"', '"Mul"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            x = self._reg()
            if self.current() in {","}:
                self.match(",")
            y = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Mul(dst, x, y, cmt)
        elif self.current() in {"Div", "div"}:
            if self.current() in {"Div"}:
                self.match("Div")
            elif self.current() in {"div"}:
                self.match("div")
            else:
                self.error("syntax error", {'"div"', '"Div"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            x = self._reg()
            if self.current() in {","}:
                self.match(",")
            y = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Div(dst, x, y, cmt)
        elif self.current() in {"Negate", "neg"}:
            if self.current() in {"Negate"}:
                self.match("Negate")
            elif self.current() in {"neg"}:
                self.match("neg")
            else:
                self.error("syntax error", {'"Negate"', '"neg"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            v = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Negate(dst, v, cmt)
        elif self.current() in {"LessThan", "lt"}:
            if self.current() in {"LessThan"}:
                self.match("LessThan")
            elif self.current() in {"lt"}:
                self.match("lt")
            else:
                self.error("syntax error", {'"LessThan"', '"lt"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            x = self._reg()
            if self.current() in {","}:
                self.match(",")
            y = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = LessThan(dst, x, y, cmt)
        elif self.current() in {"GreaterThan", "gt"}:
            if self.current() in {"GreaterThan"}:
                self.match("GreaterThan")
            elif self.current() in {"gt"}:
                self.match("gt")
            else:
                self.error("syntax error", {'"gt"', '"GreaterThan"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            x = self._reg()
            if self.current() in {","}:
                self.match(",")
            y = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = GreaterThan(dst, x, y, cmt)
        elif self.current() in {"LessThanEqual", "leq"}:
            if self.current() in {"LessThanEqual"}:
                self.match("LessThanEqual")
            elif self.current() in {"leq"}:
                self.match("leq")
            else:
                self.error("syntax error", {'"LessThanEqual"', '"leq"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            x = self._reg()
            if self.current() in {","}:
                self.match(",")
            y = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = LessThanEqual(dst, x, y, cmt)
        elif self.current() in {"GreaterThanEqual", "geq"}:
            if self.current() in {"GreaterThanEqual"}:
                self.match("GreaterThanEqual")
            elif self.current() in {"geq"}:
                self.match("geq")
            else:
                self.error("syntax error", {'"geq"', '"GreaterThanEqual"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            x = self._reg()
            if self.current() in {","}:
                self.match(",")
            y = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = GreaterThanEqual(dst, x, y, cmt)
        elif self.current() in {"Equal", "eq"}:
            if self.current() in {"Equal"}:
                self.match("Equal")
            elif self.current() in {"eq"}:
                self.match("eq")
            else:
                self.error("syntax error", {'"Equal"', '"eq"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            x = self._reg()
            if self.current() in {","}:
                self.match(",")
            y = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Equal(dst, x, y, cmt)
        elif self.current() in {"NotEqual", "neq"}:
            if self.current() in {"NotEqual"}:
                self.match("NotEqual")
            elif self.current() in {"neq"}:
                self.match("neq")
            else:
                self.error("syntax error", {'"neq"', '"NotEqual"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            x = self._reg()
            if self.current() in {","}:
                self.match(",")
            y = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = NotEqual(dst, x, y, cmt)
        elif self.current() in {"Not", "not"}:
            if self.current() in {"Not"}:
                self.match("Not")
            elif self.current() in {"not"}:
                self.match("not")
            else:
                self.error("syntax error", {'"Not"', '"not"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            v = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Not(dst, v, cmt)
        elif self.current() in {"Load", "ld"}:
            if self.current() in {"Load"}:
                self.match("Load")
            elif self.current() in {"ld"}:
                self.match("ld")
            else:
                self.error("syntax error", {'"Load"', '"ld"'})
            dst = self._reg()
            if self.current() in {","}:
                self.match(",")
            address = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Load(dst, address, cmt)
        elif self.current() in {"Store", "st"}:
            if self.current() in {"Store"}:
                self.match("Store")
            elif self.current() in {"st"}:
                self.match("st")
            else:
                self.error("syntax error", {'"st"', '"Store"'})
            address = self._reg()
            if self.current() in {","}:
                self.match(",")
            v = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Store(address, v, cmt)
        elif self.current() in {"Print", "print"}:
            if self.current() in {"Print"}:
                self.match("Print")
            elif self.current() in {"print"}:
                self.match("print")
            else:
                self.error("syntax error", {'"print"', '"Print"'})
            v = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Print(v, cmt)
        elif self.current() in {"CallIndirect", "calli"}:
            if self.current() in {"CallIndirect"}:
                self.match("CallIndirect")
            elif self.current() in {"calli"}:
                self.match("calli")
            else:
                self.error("syntax error", {'"CallIndirect"', '"calli"'})
            v = self._reg()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = CallIndirect(v, cmt)
        elif self.current() in {"Call", "call"}:
            if self.current() in {"Call"}:
                self.match("Call")
            elif self.current() in {"call"}:
                self.match("call")
            else:
                self.error("syntax error", {'"call"', '"Call"'})
            label = self._string()
            if self.current() in {","}:
                self.match(",")
            cmt = self._comment()
            _operation_ = Call(label, cmt)
        elif self.current() in {"Halt", "halt"}:
            if self.current() in {"Halt"}:
                self.match("Halt")
            elif self.current() in {"halt"}:
                self.match("halt")
            else:
                self.error("syntax error", {'"Halt"', '"halt"'})
            cmt = self._comment()
            _operation_ = Halt(cmt)
        else:
            self.error(
                "syntax error",
                {
                    '"LessThan"',
                    '"imm"',
                    '"Move"',
                    '"Not"',
                    '"Jump"',
                    '"GreaterThan"',
                    '"sub"',
                    '"Halt"',
                    '"ld"',
                    '"LoadLabel"',
                    '"JumpIndirect"',
                    '"leq"',
                    '"eq"',
                    '"Print"',
                    '"jz"',
                    '"Immediate"',
                    '"Equal"',
                    '"move"',
                    '"Label"',
                    '"JumpIfZero"',
                    '"Call"',
                    '"noop"',
                    '"geq"',
                    '"neq"',
                    '"Div"',
                    '"Negate"',
                    '"neg"',
                    '"call"',
                    '"CallIndirect"',
                    '"JumpIfNotZero"',
                    '"mul"',
                    '"jnz"',
                    '"Mul"',
                    '"LessThanEqual"',
                    '"GreaterThanEqual"',
                    '"NotEqual"',
                    '"print"',
                    '"st"',
                    '"div"',
                    '"add"',
                    '"lab"',
                    '"Noop"',
                    '"Load"',
                    '"not"',
                    '"gt"',
                    '"lt"',
                    '"j"',
                    '"AddImmediate"',
                    '"Store"',
                    '"Sub"',
                    '"llabel"',
                    '"halt"',
                    '"addi"',
                    '"Add"',
                    '"ji"',
                    '"calli"',
                },
            )
        return _operation_

    def _string(self) -> str:
        # string -> STR'tok =«tok.value»
        _string_: str
        tok = self.match("STR")
        _string_ = tok.value
        return _string_

    def _reg(self) -> str:
        # reg -> ID'tok =«tok.value»
        _reg_: str
        tok = self.match("ID")
        _reg_ = tok.value
        return _reg_

    def _integer(self) -> int:
        # integer -> INT'tok =«int(tok.value)»
        _integer_: int
        tok = self.match("INT")
        _integer_ = int(tok.value)
        return _integer_

    def _comment(self) -> str:
        # comment -> (string | =«""»)
        _comment_: str
        if self.current() in {"STR"}:
            _comment_ = self._string()
        elif self.current() in {
            "Add",
            "AddImmediate",
            "Call",
            "CallIndirect",
            "Div",
            "Equal",
            "GreaterThan",
            "GreaterThanEqual",
            "Halt",
            "Immediate",
            "Jump",
            "JumpIfNotZero",
            "JumpIfZero",
            "JumpIndirect",
            "Label",
            "LessThan",
            "LessThanEqual",
            "Load",
            "LoadLabel",
            "Move",
            "Mul",
            "Negate",
            "Noop",
            "Not",
            "NotEqual",
            "Print",
            "Store",
            "Sub",
            "add",
            "addi",
            "call",
            "calli",
            "div",
            "eq",
            "geq",
            "gt",
            "halt",
            "imm",
            "j",
            "ji",
            "jnz",
            "jz",
            "lab",
            "ld",
            "leq",
            "llabel",
            "lt",
            "move",
            "mul",
            "neg",
            "neq",
            "noop",
            "not",
            "print",
            "st",
            "sub",
            "EOF",
        }:
            _comment_ = ""
        else:
            self.error(
                "syntax error",
                {
                    '"LessThan"',
                    '"imm"',
                    '"Not"',
                    '"Move"',
                    '"Jump"',
                    '"GreaterThan"',
                    '"sub"',
                    '"Halt"',
                    "EOF",
                    '"ld"',
                    '"LoadLabel"',
                    '"eq"',
                    '"leq"',
                    '"JumpIndirect"',
                    '"Print"',
                    '"jz"',
                    '"Immediate"',
                    '"Equal"',
                    '"move"',
                    '"Label"',
                    '"JumpIfZero"',
                    '"Call"',
                    '"noop"',
                    '"geq"',
                    '"neq"',
                    '"Div"',
                    '"Negate"',
                    '"neg"',
                    '"call"',
                    '"CallIndirect"',
                    '"JumpIfNotZero"',
                    '"mul"',
                    '"jnz"',
                    '"Mul"',
                    '"LessThanEqual"',
                    '"GreaterThanEqual"',
                    '"NotEqual"',
                    '"print"',
                    '"st"',
                    "STR",
                    '"div"',
                    '"add"',
                    '"lab"',
                    '"Noop"',
                    '"Load"',
                    '"not"',
                    '"gt"',
                    '"lt"',
                    '"j"',
                    '"AddImmediate"',
                    '"Store"',
                    '"Sub"',
                    '"llabel"',
                    '"halt"',
                    '"addi"',
                    '"Add"',
                    '"ji"',
                    '"calli"',
                },
            )
        return _comment_
