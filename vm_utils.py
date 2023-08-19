from typing import List, Dict
from collections import defaultdict

from . import vm, vm_insns


def invoke_vm(
    insns: List[vm_insns.Insn], params: List[str], verbose: bool
) -> None:
    if verbose:
        dump_insns(insns)
    args: List[int] = []
    for arg in reversed(params):
        if arg.isnumeric():
            args.append(int(arg))
        else:
            raise Exception(f"Invalid argument: {arg}")

    memory: List[int] = args + [0] * 100000
    regs: Dict[str, int] = defaultdict(
        int,
        {
            "PC": 0,
            "FP": 0,
            "SP": len(args) + 1,
        },
    )
    exe = vm.Execution(insns, memory, regs)
    exe.verbose = verbose
    exe.run()
    assert exe.regs["SP"] == len(args) + 1


def dump_insns(insns: List[vm_insns.Insn]) -> None:
    print("Instructions:")
    insn: vm_insns.Insn
    for i, insn in enumerate(insns):
        indent: str = (
            ""
            if isinstance(insn, vm_insns.Label)
            or isinstance(insn, vm_insns.Noop)
            else "        "
        )
        dis = insn.disasm(long=False)
        print(f"[{i:5}] {indent}{dis}")
