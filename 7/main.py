import sys
from itertools import permutations


class Component (object):
    def __init__ (self, setting, mem, id):
        self.setting = setting
        self._setting = setting
        self.mem = mem
        self.idx = 0
        self.id = id

    def load_param(self, mem, idx, modes, amount=1):
        for i in range(amount):
            if len(modes) <= i or modes[i] == 0:
                # Position mode
                yield mem[mem[idx+i+1]]
            else:
                # Immediate mode
                yield mem[idx+i+1]

    def store_param(self, mem, idx, offset, val, modes=None):
        mode_idx = offset -1
        if modes and len(modes) > mode_idx and modes[mode_idx] == 1:
            print(mode_idx, modes)
            raise Exception('Invalid write mode')
        mem[mem[idx+offset]] = val

    def run_machine(self, input):
        idx = self.idx
        while True:
            opc = int(str(self.mem[idx])[-2:])
            modes = [int(c) for c in reversed(str(self.mem[idx])[:-2])]

            if opc == 1:    # add
                v1, v2 = self.load_param(self.mem, idx, modes, amount=2)
                self.store_param(self.mem, idx, 3, v1 + v2, modes=modes)
                idx += 4 # Move to next

            elif opc == 2:  # mul
                v1, v2 = self.load_param(self.mem, idx, modes, amount=2)
                self.store_param(self.mem, idx, 3, v1 * v2, modes=modes)
                idx += 4

            elif opc == 3:  # Input
                if not self.setting is None:
                    self.store_param(self.mem, idx, 1, self.setting, modes=modes)
                    self.setting = None
                elif input == None:
                    raise Exception('Invalid state, expected input')
                else:
                    self.store_param(self.mem, idx, 1, input, modes=modes)
                    input = None
                idx += 2

            elif opc == 4: # Output
                v = list(self.load_param(self.mem, idx, modes))[0]
                idx += 2
                self.idx = idx
                return v

            elif opc == 5: # Jump if true
                c, trgt = self.load_param(self.mem, idx, modes, amount=2)
                if not c == 0:
                    idx = trgt
                else:
                    idx += 3

            elif opc == 6: # Jump if false
                c, trgt = self.load_param(self.mem, idx, modes, amount=2)
                if c == 0:
                    idx = trgt
                else:
                    idx += 3

            elif opc == 7:  # less than
                v1, v2 = self.load_param(self.mem, idx, modes, amount=2)
                if v1 < v2:
                    self.store_param(self.mem, idx, 3, 1, modes=modes)
                else:
                    self.store_param(self.mem, idx, 3, 0, modes=modes)
                idx += 4

            elif opc == 8:  # Equal
                v1, v2 = self.load_param(self.mem, idx, modes, amount=2)
                if v1 == v2:
                    self.store_param(self.mem, idx, 3, 1, modes=modes)
                else:
                    self.store_param(self.mem, idx, 3, 0, modes=modes)
                idx += 4

            elif opc == 99:
                return None
            else:
                raise Exception('Illegal operand %d' % opc)

class Amplifier (object):
    def __init__(self, settings, opcs):
        self.children = [Component(setting, opcs.copy(), idx) for idx, setting in enumerate(settings)]

    def run(self, init_val):
        val = init_val
        for component in self.children:
            n_val = component.run_machine(val)
            if n_val is None:
                raise Exception('Done')
            else:
                val = n_val
        return val

class FeedbackAmplifier (Amplifier):
    def run(self, init_val):
        res = init_val
        while True:
            try:
                res = super(FeedbackAmplifier, self).run(res)
            except Exception as ex:
                if ex.args[0] == 'Done':
                    return res
                else:
                    raise ex

def find_max_output(mk_amp, inputs):
    max = (0, None)
    for input in permutations(inputs):
        amp = mk_amp(input)
        out = amp.run(0)
        if out > max[0]:
            max = (out, input)
    return max

in_str = sys.stdin.read().split('\n')[1:]
opcs   = [int(opc)   for opc   in in_str[0].split(',')]

# Part 1:
print('Part 1:')
inputs = [0, 1, 2, 3, 4]
max, config = find_max_output(lambda i: Amplifier(i, opcs.copy()), inputs)
print('%d with %s as settings' % (max, list(config)))

# Part 2:
print()
print('Part 2:')
inputs = [5,6,7,8,9]
max, config = find_max_output(lambda i: FeedbackAmplifier(i, opcs.copy()), inputs)
print('%d with %s as settings' % (max, list(config)))
