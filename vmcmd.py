import argparse
from typing import List

from .vm_parser import Parser
from .scanner import Scanner

# from vm_insns
from .vm_utils import dump_insns
from .vm import *


def get_args():
    ap = argparse.ArgumentParser(description="Run VM files")
    ap.add_argument(
        "args", nargs="*", type=int, help="Arguments to pass to VM"
    )
    ap.add_argument("--file", type=str, required=True, help="The file to run")
    ap.add_argument("--verbose", action="store_true", help="verbose output")
    return ap.parse_args()


def main():
    args = get_args()
    fname = args.file
    with open(fname) as f:
        input = f.read()
    lexer = Scanner(input, reserved=reserved)
    psr = Parser(lexer)
    insns: List[Insn] = psr.parse()

    if args.verbose:
        dump_insns(insns)

    params = list(reversed(args.args)) + [0]  # w/ space for return value
    exe = Execution(
        insns,
        params + [0] * 100000,
        {"SP": len(params)},
    )
    exe.verbose = args.verbose
    exe.run()


if __name__ == "__main__":
    main()
