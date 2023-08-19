RDGEN = python3 ~/personal/rdgen/main.py

GENERATED = \
	vm.ebnf \
	vm.json \
	vm_insns.py \
	vm_parser.py

VM = \
	vm.py \
	vm_insns.py \
	vm_parser.py \
	vm_scanner.py \
	vmcmd.py

all: $(GENERATED)

vm.json: vm.yaml
	yq -p yaml -o json vm.yaml > vm.json

vm.ebnf: mk_interp.py vm.json
	python3 mk_interp.py --spec vm.json --ebnf vm.ebnf

vm_parser.py: mk_interp.py vm.ebnf
	$(RDGEN) create --decorate --input vm.ebnf --output vm_parser.py
	black -q vm_parser.py

vm_insns.py: mk_interp.py vm.json
	python3 mk_interp.py --spec vm.json --insns vm_insns.py
	black -q vm_insns.py

clean:
	rm -f $(GENERATED) 
