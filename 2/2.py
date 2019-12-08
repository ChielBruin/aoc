import sys

def run_machine(mem):
    idx = 0
    while not mem[idx] == 99:
        opc = mem[idx]
        if opc is 1:    # add
            v1 = mem[mem[idx+1]]
            v2 = mem[mem[idx+2]]
            mem[mem[idx+3]] = v1 + v2

            idx += 4 # Move to next
        elif opc is 2:  # mul
            v1 = mem[mem[idx+1]]
            v2 = mem[mem[idx+2]]
            mem[mem[idx+3]] = v1 * v2

            idx += 4 # Move to next
        else:
            raise Exception('Illegal operand %d' % opc)
    return mem

in_str = sys.stdin.read()
opcs = [int(opc) for opc in in_str.split('\n')[1].split(',')]

# Part 1:
# opcs[1] = 12
# opcs[2] = 2
# print(run_machine(opcs)[0])

# Part 2:
exp = 19690720
for i in range(100):
    for j in range(100):
        mem = opcs.copy()
        mem[1] = i
        mem[2] = j
        try:
            out = run_machine(mem)[0]
        except:
            #Corrupt state for i and j
            out = -1
        if exp == out:
            print(100 * i + j)
            exit(0)
        else:
            continue
