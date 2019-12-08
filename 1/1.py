import sys

def calc_fuel(mass, fuel_mass):
    return _calc_fuel(mass, fuel_mass, 0)

def calc_fuel(mass, part_2):
    fuel = mass // 3 - 2
    if fuel > 0 and part_2:
        extra_fuel = calc_fuel(fuel, part_2)
        return fuel + extra_fuel
    else:
        return 0 if fuel < 0 else fuel

in_str = sys.stdin.read()
fuels = [calc_fuel(int(line), part_2=True) for line in in_str.split('\n')[1:] if line]

print(sum(fuels))
