from typing import List, Dict, Optional
import pprint
import textwrap

from .vm_insns import *


class Execution:
    def __init__(
        self,
        insns: List[Insn],
        memory: List[int],
        regs: Dict[str, int],
    ):
        self.insns: List[Insn] = insns
        self.memory: List[int] = memory
        self.regs: Dict[str, int] = regs
        if "FP" not in self.regs:
            self.regs["FP"] = 0
        if "SP" not in self.regs:
            self.regs["SP"] = 0
        if "PC" not in self.regs:
            self.regs["PC"] = 0
        self.labels: dict[str, int] = {}
        for i, insn in enumerate(self.insns):
            if isinstance(insn, Label):
                label = insn.label
                if label in self.labels:
                    raise Exception(f"Duplicate label: {label}")
                self.labels[label] = i

        for insn in self.insns:
            if hasattr(insn, "label"):
                lab: str = getattr(insn, "label")
                if lab not in self.labels:
                    raise Exception(f"Undefined label: {lab}")

        self.verbose = False

    def __repr__(self) -> str:
        return f"Execution({self.insns}, {self.regs})"

    def dump_state(self) -> None:
        insn = self.insns[self.regs["PC"]]
        frame: list[int] = []
        caller: list[int] = []
        if self.regs["FP"] == 0:
            frame = self.memory[self.regs["FP"] : self.regs["SP"]]
            frame = frame[:20]
        else:
            start = self.memory[self.regs["FP"] + 1]
            caller = self.memory[start : self.regs["FP"]]
            frame = self.memory[self.regs["FP"] : self.regs["SP"]]
            frame = frame[:20]
        print(f"      regs  =")
        s = pprint.pformat(dict(self.regs), sort_dicts=False)
        print(textwrap.indent(s, " " * 14))
        print(f"      frame = {frame}")
        print(f"      caller= {caller}")
        print(f"[{self.regs['PC']:4}] {insn}")

    def step(self) -> Optional["Execution"]:
        insn = self.insns[self.regs["PC"]]
        self.regs["PC"] += 1
        try:
            insn.execute(self.memory, self.regs, self.labels)
        except Exception as e:
            if f"{e}" == "Halt":
                return None
            raise
        return self

    def run(self) -> None:
        if self.verbose:
            print("Begin Execution")
            self.dump_state()
        o: Optional[Execution] = self
        while o is not None:
            o = self.step()
            if self.verbose:
                self.dump_state()
        if self.verbose:
            print("End Execution")
