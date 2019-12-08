import sys

def load_param(mem, idx, modes, amount=1):
    for i in range(amount):
        if len(modes) <= i or modes[i] is 0:
            # Position mode
            yield mem[mem[idx+i+1]]
        else:
            # Immediate mode
            yield mem[idx+i+1]

def store_param(mem, idx, offset, val, modes=None):
    mode_idx = offset -1
    if modes and len(modes) > mode_idx and modes[mode_idx] is 1:
        print(mode_idx, modes)
        raise Exception('Invalid write mode')
    mem[mem[idx+offset]] = val

def run_machine(mem, inputs):
    idx = 0
    while True:
        opc = int(str(mem[idx])[-2:])
        modes = [int(c) for c in reversed(str(mem[idx])[:-2])]

        if opc is 1:    # add
            v1, v2 = load_param(mem, idx, modes, amount=2)
            store_param(mem, idx, 3, v1 + v2, modes=modes)
            idx += 4 # Move to next

        elif opc is 2:  # mul
            v1, v2 = load_param(mem, idx, modes, amount=2)
            store_param(mem, idx, 3, v1 * v2, modes=modes)
            idx += 4

        elif opc is 3:  # Input
            input = inputs[0]
            inputs = inputs[1:]
            store_param(mem, idx, 1, input, modes=modes)
            idx += 2

        elif opc is 4: # Output
            v = list(load_param(mem, idx, modes))[0]
            print(v)
            idx += 2

        elif opc is 5: # Jump if true
            c, trgt = load_param(mem, idx, modes, amount=2)
            if not c == 0:
                idx = trgt
            else:
                idx += 3

        elif opc is 6: # Jump if false
            c, trgt = load_param(mem, idx, modes, amount=2)
            if c == 0:
                idx = trgt
            else:
                idx += 3

        elif opc is 7:  # less than
            v1, v2 = load_param(mem, idx, modes, amount=2)
            if v1 < v2:
                store_param(mem, idx, 3, 1, modes=modes)
            else:
                store_param(mem, idx, 3, 0, modes=modes)
            idx += 4

        elif opc is 8:  # Equal
            v1, v2 = load_param(mem, idx, modes, amount=2)
            if v1 == v2:
                store_param(mem, idx, 3, 1, modes=modes)
            else:
                store_param(mem, idx, 3, 0, modes=modes)
            idx += 4

        elif opc is 99:
            break
        else:
            raise Exception('Illegal operand %d' % opc)
    return mem

in_str = sys.stdin.read().split('\n')[1:]
inputs = [int(input) for input in in_str[0].split(',') if input]
opcs   = [int(opc)   for opc   in in_str[1].split(',')]

mem = run_machine(opcs, inputs)
if len(mem) < 20:
    print('mem:')
    print(mem)
