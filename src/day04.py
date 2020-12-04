import re

def read_passports(lines):
    passport = {}
    for entry in [entry for line in lines for entry in line.split(' ')]:
        if len(entry) == 0:
            yield passport
            passport = {}
        else:
            [field, value] = entry.split(':')
            passport[field] = value
    yield passport

def has_all_fields(passport):
    for field in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']:
        if field not in passport:
            return False
    return True

def solve_part_1(passports):
    return sum(1 for p in passports if has_all_fields(p))

def solve_part_2(passports):
    def valid_byr(byr):
        return int(byr) >= 1920 and int(byr) <= 2002

    def valid_iyr(iyr):
        return int(iyr) >= 2010 and int(iyr) <= 2020

    def valid_eyr(eyr):
        return int(eyr) >= 2020 and int(eyr) <= 2030
    
    def valid_hgt(hgt):
        if not re.match("[0-9]+(cm|in)", hgt):
            return False
        value = int(hgt[:-2])
        if hgt.endswith("cm"):
            return value >= 150 and value <= 193
        else:
            return value >= 59 and value <= 76

    def valid_hcl(hcl):
        return re.match("^#[0-9a-f]{6}$", hcl)

    def valid_ecl(ecl):
        return ecl in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

    def valid_pid(pid):
        return re.match("^[0-9]{9}$", pid)
        
    def valid(p):
        if not has_all_fields(p):
            return False
        if not valid_byr(p['byr']):
            return False
        if not valid_iyr(p['iyr']):
            return False
        if not valid_eyr(p['eyr']):
            return False
        if not valid_hgt(p['hgt']):
            return False
        if not valid_hcl(p['hcl']):
            return False
        if not valid_ecl(p['ecl']):
            return False
        if not valid_pid(p['pid']):
            return False
        return True
    
    return sum(1 for p in passports if valid(p))

if __name__ == "__main__":
    with open("day04_input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        passports = list(read_passports(lines))
        print(solve_part_1(passports))
        print(solve_part_2(passports))