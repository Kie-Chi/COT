import os
import numpy as np

class Generator: 
    def __init__(self) :
        self.__class = {
            "cal_r": ['add', 'sub'],
            "cal_i": ['ori'],
            "lui": ['lui'],
            "store": ['sw'],
            "load": ['lw'],
            "branch": ['beq'],
            "j_l": ['jal'],
            "j_r": ['jr'] 
        }


    def __get_test_regs(self) :
        regs = list(range(32))
        self.__test_regs = np.random.choice(regs)
    
    



def init_grf(times=3) :
    """
        此函数测试指令lui与ori
    """
    lines = []
    for z in range(times) :
        for i in range(32) :
            hi = np.random.randint(0, 65535)
            lo = np.random.randint(0, 65535)
            lui_line = lui(i, hi)
            ori_line = ori(i, i, lo)
            lines.append(lui_line)
            lines.append(ori_line)
    return lines
    # with open("init_grf.asm", "w", encoding="utf-8") as file :
    #     file.writelines(lines)

def choice_one(rs) :
    low = np.random.randint(5)
    low = -low
    high = np.random.randint(1, 5)
    num = np.random.randint(low, high)

    hi = (num >> 16) & 0x0000ffff
    lo = num & 0x0000ffff

    mips = []
    mips.append(lui(rs, hi))
    mips.append(ori(rs, rs, lo))
    return mips

def choice_two(rs) :
    pos_num = np.random.randint(2147483647 - 5, 2147483647)
    neg_num = np.random.randint(-2147483648, -2147483648 + 5)
    num = np.random.choice([pos_num, neg_num])
    # print(num)
    # print(f"{num:#b}")
    # print(f"{num:#x}")
    hi = (num >> 16) & 0x0000ffff
    lo = num & 0x0000ffff
    # print(f"{hi:#x}")
    # print(f"{lo:#x}")
    mips = []
    mips.append(lui(rs, hi))
    mips.append(ori(rs, rs, lo))
    return mips

def choice_three(rs) :
    low = np.random.randint(-2147483648, -1)
    high = np.random.randint(2147483647)
    # print(low)
    # print(high)
    num = np.random.randint(low, high)
    # print(num)
    hi = (num >> 16) & 0x0000ffff
    lo = num & 0x0000ffff
    mips = []
    mips.append(lui(rs, hi))
    mips.append(ori(rs, rs, lo))
    return mips

def arth_test(times) :
    """
        此函数测试指令add与sub
    """
    lines = []
    has_used = np.zeros(32, dtype=bool)
    # print(has_used)
    
    choice = [1, 2, 3]# 1: 0附近 2: 21474868附近 3: random
    # print(np.random.choice(choice))
    
    for i in range(times) :
        registers = np.random.randint(0, 32, 4)
        choices = np.random.randint(1, 4, 2)
        # print(registers)
        # print(choices)
        for j in range(2) :
            if choices[j] == 1 :
                lines.extend(choice_one(registers[j]))
            elif choices[j] == 2 :
                lines.extend(choice_two(registers[j]))
            else :
                lines.extend(choice_three(registers[j]))
        lines.append(add(registers[0], registers[1], registers[2]))
        lines.append(sub(registers[0], registers[1], registers[3]))

    # with open("arth_test.asm", "w", encoding="utf-8") as file :
    #     file.writelines(lines)
    return lines

def init_base(base, rt) :
    mips = []
    while True :
        num = np.random.randint(-3072, 3072)
        offset = np.random.randint(-3072 + 10, 3072 - 10) 
        if base == 0 :
            if offset >= 0 and offset < 3072 :
                num <<= 2
                offset <<= 2
                hi = (num >> 16) & 0x0000ffff
                lo = num & 0x0000ffff
                mips.append(lui(base, hi))
                mips.append(ori(base, base, lo))
                choice = np.random.randint(0, 2)
                if choice == 0 :
                    mips.append(lw(base, rt, offset))
                else :
                    mips.append(sw(base, rt, offset))
                return mips
        else :    
            if num + offset >= 0 and num + offset < 3072 :
                num <<= 2
                offset <<= 2
                hi = (num >> 16) & 0x0000ffff
                lo = num & 0x0000ffff
                mips.append(lui(base, hi))
                mips.append(ori(base, base, lo))
                choice = np.random.randint(0, 2)
                if choice == 0 :
                    mips.append(lw(base, rt, offset))
                else :
                    mips.append(sw(base, rt, offset))
                return mips

def store_test(times) :
    """
        此函数测试指令lw与sw
    """
    lines = []

    for i in range(times) :
        register = np.random.randint(0, 32, 2)
        base = register[0]
        rt = register[1]
        # print(offset)
        lines.extend(init_base(base, rt))
    
    # with open("store_test.asm", "w", encoding="utf-8") as file :
    #     file.writelines(lines)

    return lines

def branch_test(branch_time ,times, forbidden=True) :
    
    mips = []
    flag = False
    least = (times * 19) // 20 # 最少出现死循环的时间
    for i in range(times) :
        choice = np.random.choice([1, 2])
        if i > least and not forbidden :
            choice = np.random.choice([1, 2, 3], p=[0.45, 0.45, 0.1])
        
        is_beq = np.random.randint(2)
        # print(is_beq)
        # print(choice)
        register = np.random.randint(0, 32, 2)
        rs = register[0]
        rt = register[1]
        label = f"Branch{branch_time}_{i}"
        if is_beq == 0 and rs != rt:
            while True :
                num1 = np.random.randint(0, 65535)
                num2 = np.random.randint(0, 65535)
                offset = np.random.randint(0, 65535)
                if num1 != num2 :
                    mips.append(ori(0, rs, num1))
                    mips.append(ori(0, rt, num2))
                    mips.append(beq(rs, rt, label))
                    mips.append(ori(0, rs, offset))
                    mips.append(label + ":\n")
                    break
        else :
            if choice == 1 :
                mips.append(beq(rs, rt, label))
                mips.extend(arth_test(1))
                mips.append(label + ":\n")
                
            elif choice == 2 and rs != rt :
                rd = 0
                while True :
                    rd = np.random.randint(0, 32)
                    if rd != rs and rd != rt and rd != 0:
                        break
                num = np.random.randint(10, 65535)
                num1 = np.random.randint(1, num - 2)
                mips.append(ori(0, rs, num))
                mips.append(ori(0, rt, num - num1))
                mips.append(ori(0, rd, num1))
                mips.append(label + ":\n")
                mips.append(add(rt, rd, rt))
                mips.append(beq(rs, rt, label))
            else :
                if choice == 3 :
                    num = np.random.randint(65535)
                    mips.append(ori(0, rs, num))
                    mips.append(ori(0, rt, num))
                    mips.append
                    mips.append(label + ":\n")
                    mips.append(beq(rs, rt, label))
                    flag = True
                    break
    # with open("jump_test.asm", "w", encoding="utf-8") as file :
    #     file.writelines(mips)
    return mips, flag

def jump_test(jump_time, times, isjal=1, isjr=0, forbidden=True) :
    mips = []
    flag = False
    origin = times
    index = 0
    index_b = 0
    while times > 0:
        choice = np.random.randint(0, 2)
        if (choice == 0 or isjal == 1) and isjr == 0:
            x = np.random.randint(5, 7)
            label = np.random.choice(x-1, x-3, replace=False) + 1
            label = np.concatenate(([0], label, [x]), axis=0)
            the_all = list(range(x))

            for i in range(x):
                if i in label:
                    the_all.remove(i)

            relay = np.random.choice(the_all, 2, replace=False)
            pos = np.zeros(x)
            for i in range(x - 2) :
                pos[label[i]] = label[i + 1]
            pos[relay[0]] = relay[1]
            pos[relay[1]] = relay[0]
            # print(pos)
            
            for i in range(x) :
                label = f"Jump{jump_time}_{i + index}"
                jlabel = f"Jump{jump_time}_{int(pos[i] + index)}"
                mips.append(label + ":\n")
                mips.append(jal(jlabel))
            label = f"Jump{jump_time}_{x + index}"
            mips.append(label + ":\n")
            mips.append(nop())
            index += x + 1
            times -= 2 * x + 3
        else :
            rs = np.random.randint(1, 31)
            jlabel = f"Jump{jump_time}_{index_b}"
            blabel = f"BranchforJ{jump_time}_{index_b}"
            mips.append(beq(0, 0, blabel))
            mips.append(jlabel + ":\n")
            mips.append(add(31, 0, rs))
            mips.append(jr(rs))
            mips.append(blabel + ":\n")
            mips.append(jal(jlabel))
            index_b += 1
            times -= 6
        
    # with open("test/jump_test.asm", "w", encoding="utf-8") as file :
    #     file.writelines(mips)
    return mips

def for_loop(times) :
    pass

def unit_test(test_dir, times, branch_time, jump_time=0, level=1, forbidden=True) :
    unit_dir = os.path.join(test_dir,"unit")
    # os.system(f"mkdir {unit_dir}")
    os.makedirs(unit_dir, exist_ok=True)
    with open(os.path.join(unit_dir, "set_test.asm"), "w", encoding="utf-8") as file :
        loop = times // 70 + 1
        file.writelines(init_grf(loop))
    
    with open(os.path.join(unit_dir, "arth_test.asm"), "w", encoding="utf-8") as file :
        loop = times // 6 + 1
        file.writelines(arth_test(loop))

    with open(os.path.join(unit_dir, "store_test.asm"), "w", encoding="utf-8") as file :
        loop = times // 6 + 1
        file.writelines(store_test(loop))
    
    with open(os.path.join(unit_dir, "branch_test.asm"), "w", encoding="utf-8") as file :
        loop = times // 8 + 1
        code, flag = branch_test(branch_time, loop, forbidden)
        file.writelines(code)
    
    if level > 1 :
        with open(os.path.join(unit_dir, "jump_test.asm"), "w", encoding="utf-8") as file :
            loop = (times * 9) // 10
            file.writelines(jump_test(jump_time, loop // 2, isjal=1))
            jump_time += 1
            file.writelines(jump_test(jump_time, loop // 2, isjr= 1))

def random_test(registers ,times, branch_time, jump_time, level=1, forbidden=True) :
    mips = []
    i = 0
    least = (times * 9) // 10
    while i < times :
        
        choice = np.random.randint(0, 8)
        if level > 1 :
            choice = np.random.randint(0, 9)
        rs = np.random.choice(registers)
        rt = np.random.choice(registers)
        rd = np.random.choice(registers)
        offset = np.random.randint(0, 65535)
        if choice == 0 :
            mips.append(lui(rt, offset))
            i += 1
        elif choice == 1 :
            mips.append(ori(rs, rt, offset))
            i += 1
        elif choice == 2 :
            mips.append(add(rs, rt, rd))
            i += 1
        elif choice == 3 :
            mips.append(sub(rs, rt, rd))
            i += 1
        elif choice == 4 :
            mips.extend(store_test(1))
            i += 6
        elif choice == 5 :
            mips.extend(store_test(5)) 
            i += 6
        elif choice == 6 :
            the_forbidden = True
            if i > least and not forbidden :
                the_forbidden = False
            code, flag = branch_test(branch_time, 1, the_forbidden)
            mips.extend(code)
            if flag :
                break
            branch_time += 1
            i += 12
        elif choice == 7 :
            mips.append(nop())
            i += 1
        elif choice == 8 :
            mips.extend(jump_test(jump_time, 1, isjal=0, isjr=0))
            jump_time += 1
            i += 10

    with open("test/new.asm", "w", encoding="utf-8") as file :
        file.writelines(mips)
    return mips


def lui(rt, offset) -> str :
    return f"lui ${rt}, {offset:#x}\n"

def ori(rs, rt, offset) -> str :
    return f"ori ${rt}, ${rs}, {offset:#x}\n"    

def add(rs, rt, rd) -> str :
    return f"add ${rd}, ${rs}, ${rt}\n"

def sub(rs, rt, rd) -> str :
    return f"sub ${rd}, ${rs}, ${rt}\n"

def lw(base, rt, offset) -> str :
    return f"lw ${rt}, {offset}(${base})\n"

def sw(base, rt, offset) -> str :
    return f"sw ${rt}, {offset}(${base})\n"

def beq(rs, rt, offset) -> str :
    return f"beq ${rs}, ${rt}, {offset}\n"

def nop() -> str :
    return "nop\n"

def jal(offset) -> str :
    return f"jal {offset}\n"

def jr(rs) -> str :
    return f"jr ${rs}\n"


if __name__ == "__main__" :
    os.makedirs("test", exist_ok=True)
    branch_time = 0
    jump_time = 0
    num = np.random.randint(0, 32)
    offset = np.random.randint(0, 65535)
    # print(offset)
    # print(hex(offset))  
    # init_grf()
    # arth_test(100)
    # choice_one(1)
    # store_test(10)
    # jump_test(branch_time, 10)
    unit_test("test", 3600, branch_time, level=2, forbidden=True)
    random_test(list(range(32)), 3600, branch_time, jump_time, level=2)
    # jump_test(0, 500)
    