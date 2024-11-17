import os
import numpy as np

class DataMaker:
    def __init__(self, the_class, the_unit):
        # self.__class = {
        #     "cal_r": ['add', 'sub'],
        #     "cal_i": ['ori'],
        #     "lui": ['lui'],
        #     "store": ['sw'],
        #     "load": ['lw'],
        #     "branch": ['beq'],
        #     "j_l": ['jal'],
        #     "j_r": ['jr'],
        #     "nop": ['nop']
        # }
        self.__class = the_class

        self.__unit = the_unit
        self.__log = []

        # self.__nojump = ["cal_r", "cal_i", "lui", "store", "load", "j_l", "j_r", "nop", "md", "mt", "mf"]
        self.__all_regs = [i for i in range(32)]
        self.__get_regs()
        self.__init_pymars()
        

    def __init_pymars(self):
        self.__pc = 0
        self.__mips = []
        self.__unused = []
        self.__count = 0
        self.__grf = [0 for _ in range(32)] 
        self.__dm = [0 for _ in range(3072)]
        self.__hi = 0
        self.__lo = 0

    def __get_pc(self) :
        return int("3000", 16) + self.__pc * 4

    def __get_regs(self) :
        regs = list(range(1, 31))
        # test_regs
        self.__test_regs = np.random.choice(regs, 3, replace=False)

        for test_reg in self.__test_regs :
            regs.remove(test_reg)
        self.__test_regs = np.concatenate(([0] , self.__test_regs, [31]))
        # print(self.__test_regs)


        # jump_regs
        self.__jump_regs = np.random.choice(regs, 8, replace=False)
        # print(self.__jump_regs)

        for jump_reg in self.__jump_regs :
            regs.remove(jump_reg)

        self.__unused = regs


    def __create_jarea(self) :
        self.__mips.append(f"Jarea:\n")
        self.__mips.append(self.beq(0, 0, "JareaEnd"))
        initial = []
        for reg in self.__jump_regs :
            self.__mips.append(f"JBackFor{reg}_0:\n")
            pc = self.__get_pc()
            self.__mips.append(self.add(0, 31, reg))
            self.__mips.append(self.jr(reg))
            self.__mips.append(self.ori(0, 0, pc))
            self.__mips.append(f"JBackFor{reg}_1:\n")
            pc = self.__get_pc()
            initial.append(pc)
            self.__mips.append(self.jr(31))
            self.__mips.append(self.ori(0, reg, pc))

        pc = self.__get_pc()
        initial.append(pc)
        self.__mips.append("JBackFor31_0:\n")
        self.__mips.append(self.jr(31))
        self.__mips.append("JareaEnd:\n")
        # print(mips)
        return initial

    def __create_test(self, jump_initial) :
        times = 4
        the_tests = np.random.choice(list(self.__class.keys()), times)
        # print(the_tests)

        rd = self.__test_regs[np.random.choice([1, 2, 3])]
        self.__mips.append(f"Test{self.__count}Begin:\n")
        registers = []
        jump_regs = list(self.__jump_regs)[:]
        for the_test in the_tests:
            register = []
            other = np.random.choice(self.__test_regs)
            rs = np.random.choice([other, rd])
            rt = np.random.choice(self.__test_regs)
            rd = np.random.choice(self.__test_regs)
            reg = 0
            imm = np.random.randint(0, 200)
            # imm = imm >> 2
            # imm = imm << 2
            offset = f"Test{self.__count}End"
            j_flag = False
            md_flag = False

            if the_test == "branch":
                self.__mips.append(self.ori(0, rs, imm))
                self.__mips.append(self.ori(0, rt, imm))
                # print(f"${rs} <= {imm}")
                # print(f"${rt} <= {imm}")
                j_flag = True
            elif the_test == "j_l":
                reg = np.random.choice(jump_regs)
                reg = np.random.choice([reg, 31])
                if reg != 31:
                    jump_regs.remove(reg)
                offset = f"JBackFor{reg}_0"
                j_flag = True
            elif the_test == "j_r":
                rs = np.random.choice(jump_regs)
                j_flag = True
            elif the_test == "md":        
                x = np.random.randint(0, 2)
                if x == 1:
                    self.__mips.append(self.mthi(rs))
                else:
                    self.__mips.append(self.mtlo(rs))

            register = [rs, rt, rd, imm, offset, reg, j_flag, md_flag]
            registers.append(register)

        the_ind = 0
        jump_flag = False
        store_flag = False
        not_jump = True
        muldiv_flag = False
        for the_test in the_tests:
            rs = registers[the_ind][0]
            rt = registers[the_ind][1]
            rd = registers[the_ind][2]
            imm = registers[the_ind][3]
            offset = registers[the_ind][4]
            reg = registers[the_ind][5]
            j_flag = registers[the_ind][6]
            md_flag = registers[the_ind][7]
            jump_flag = jump_flag or j_flag
            muldiv_flag = muldiv_flag or md_flag
            the_ind += 1

            code, useless, store_now, not_jump = self.method(the_test, rs=rs, rt=rt, rd=rd, imm=imm, offset=offset, flag=not_jump)
            store_flag = store_flag or store_now
            if code != None:
                self.__mips.append(code)

            if j_flag:
                if offset != f"JBackFor31_0":
                    pc = self.__get_pc() + 4
                    self.__mips.append(self.ori(0, 31, pc))
                else :
                    self.__mips.append(self.nop())
        pc = self.__get_pc()
        self.__mips.append(self.ori(0, 31, pc))
        self.__mips.append(f"Test{self.__count}End:\n")

        for ind in range(times) :
            reg = registers[ind][5]
            if reg != 0 and reg != 31:
                self.__mips.append(self.ori(0, reg, np.random.choice([jump_initial[-1], jump_initial[list(self.__jump_regs).index(reg)]])))
            ind += 1

        if muldiv_flag:
            x = np.random.randint(0, 2)
            if x == 1:
                self.__mips.append(self.mfhi(np.random.choice(self.__test_regs)))
            else:
                self.__mips.append(self.mflo(np.random.choice(self.__test_regs)))


        for test_reg in self.__test_regs:
            if test_reg != 0:
                if self.__grf[test_reg] > 100 or self.__grf[test_reg] < -100:
                # num = np.random.randint(0, 200) >> 2
                # num = num << 2
                    num = np.random.randint(0, 50)
                    self.__mips.append(self.ori(0, test_reg, num))
        
        if store_flag:
            for i in range(50):
                if self.__dm[i] > int("6fff", 16) or self.__dm[i] < -int("6fff", 16):
                    self.__mips.append(self.sw(0, np.random.choice(self.__test_regs), 4*i))
        
        self.__count += 1


    def __init_regs(self, jump_initial) :
        for test_reg in self.__test_regs:
            # num = np.random.randint(0, 200) >> 2
            # num = num << 2
            num = np.random.randint(0, 50)
            self.__mips.append(self.ori(0, test_reg, num))

        lens = len(self.__jump_regs)
        for i in range(lens):
            self.__mips.append(self.ori(0, self.__jump_regs[i], np.random.choice([jump_initial[i], jump_initial[-1]])))

    def __init_dm(self):
        the_new = np.concatenate((self.__test_regs, self.__jump_regs), axis=0)
        for _ in range(20):
            off = np.random.randint(0, 50)
            off = off >> 2
            off = off << 2
            self.__mips.append(self.sw(0, np.random.choice(the_new), off))

    def random_test(self, max_time, path="test.asm") :
        self.__init_pymars()
        jump_initial = self.__create_jarea()
        self.__init_regs(jump_initial)
        self.__init_dm()
        while len(self.__mips) <= max_time:
            self.__create_test(jump_initial)

        with open(path, "w", encoding="utf-8") as file:
            file.writelines(self.__mips)

        self.__init_pymars()
        # with open("log.txt", "w", encoding="utf-8") as file:
        #     file.writelines(self.__log)

    def method(self, mtd_class, rs=0, rt=0, rd=0, imm=0, offset="End", flag=True) :
        mtd_name = np.random.choice(self.__class[mtd_class])
        mtd = getattr(self, mtd_name, None)
        store_flag = False
        the_jump = False
        if  mtd_class == "lui":
            imm = 0
        elif mtd_class == "store" or mtd_class == "load":
            off = np.random.randint(0, 200)
            off = off >> 2
            off = off << 2
            imm = off - self.__grf[rs]
            if mtd_name == "lh" or mtd_name == "sh":
                imm += np.random.randint(0, 2) * 2
            if mtd_name == "lb" or mtd_name == "sb":
                imm += np.random.randint(0, 4)

            while True:
                if imm <= 32767 and imm >= -32768:
                    break
                
                if self.__grf[rs] > (32500 + 3072 * 4) or self.__grf[rs] < -32500:
                    for test_reg in self.__test_regs:
                        if test_reg != 0:
                            if self.__grf[test_reg] > 200 or self.__grf[test_reg] < -200:
                            # num = np.random.randint(0, 200) >> 2
                            # num = num << 2
                                num = np.random.randint(0, 200)
                                self.__mips.append(self.ori(0, test_reg, num))
                    return [None, rd, False, flag]
                
                lef = 0
                rig = 12000
                while lef < rig :
                    off = (lef + rig) >> 1
                    off = off >> 2
                    off = off << 2
                    imm = off - self.__grf[rs]
                    if imm > 32767 :
                        rig = off - 1
                    elif imm < -32768:
                        lef = off + 1
                    else:
                        break
            
            if mtd_class == "store":
                if self.__grf[rt] > int("6fff", 16) or self.__grf[rt] < -int("6fff", 16):
                    store_flag = True
        elif mtd_class == "branch":
            if mtd_name == "beq":
                the_jump = self.__grf[rs] == self.__grf[rt]
    
            if mtd_name == "bne":
                the_jump = self.__grf[rs] != self.__grf[rt]
                if the_jump:
                    num = np.random.randint(0, 10)
                    if num < 3:
                        mtd = getattr(self, "beq", None)
                        the_jump = False
        elif mtd_class == "md":
            if mtd_name == "div" or mtd_name == "divu":
                if self.__grf[rt] == 0:
                    choices = []
                    for test_reg in self.__test_regs:
                        if self.__grf[test_reg] != 0 :
                            choices.append(test_reg)
                    if choices != []:
                        rt = np.random.choice(choices)
                    else:
                        return [None, rs, False, flag]

        flag = (not the_jump) and flag
        the_return = []

        if mtd_class == "cal_r":
            the_return = [mtd(rs, rt, rd, flag), rd]
        elif mtd_class == "cal_i":
            the_return = [mtd(rs, rt, imm, flag), rt]
        elif mtd_class == "lui":
            the_return = [mtd(rt, imm, flag), rt]
        elif mtd_class == "load":
            the_return = [mtd(rs, rt, imm, flag), rt]
        elif mtd_class == "store":
            the_return = [mtd(rs, rt, imm, flag), rt]
        elif mtd_class == "branch":
            the_return = [mtd(rs, rt, offset), rt]
        elif mtd_class == "j_l":
            the_return = [mtd(offset, flag), 31]
        elif mtd_class == "j_r":
            the_return = [mtd(rs), rs]
        elif mtd_class == "md":
            the_return = [mtd(rs, rt, flag), rs]
        elif mtd_class == "mf":
            the_return = [mtd(rd, flag), rd]
        elif mtd_class == "mt":
            the_return = [mtd(rs, flag), rs]
        else: 
            the_return = [mtd(), 0]

        the_return.append(store_flag)
        the_return.append(flag)
        return the_return
    

    def set_test(self, times) :
        the_test = []
        for one in self.__unit["set_test"]:
            the_test.extend(self.__class[one][:])

        len0 = len(self.__mips)
        while (len(self.__mips) - len0) < (times // 10) :
            hi = np.random.randint(0, 65535)
            lo = np.random.randint(0, 65535)
            reg = np.random.choice(self.__all_regs)
            self.__mips.append(self.lui(reg, hi))
            self.__mips.append(self.ori(reg, reg, lo))
        
        while len(self.__mips) < times :
            rs = np.random.choice(self.__all_regs)
            rt = np.random.choice(self.__all_regs)
            offset = np.random.randint(-32768, 32767)
            mtd_name = np.random.choice(the_test)
            mtd = getattr(self, mtd_name, None)
            if mtd_name in self.__class['lui']:
                self.__mips.append(mtd(rt, offset))
            elif mtd_name in self.__class["mt"] or mtd_name in self.__class["mf"]:
                if len(self.__mips) > ((times * 2) // 3) :
                    self.__mips.append(mtd(rs))
            else:
                self.__mips.append(mtd(rs, rt, offset))

        return self.__mips

    def __set(self, rs, imm) :
        num = imm & 0xffffffff
        hi = (num >> 16) & 0x0000ffff
        lo = num & 0x0000ffff
        if hi != 0:
            self.__mips.append(self.lui(rs, hi))
            self.__mips.append(self.ori(rs, rs, lo))
        else:
            self.__mips.append(self.ori(0, rs, lo))

    def __set_zero(self, rs) :
        low = np.random.randint(5)
        low = -low
        high = np.random.randint(1, 5)
        num = np.random.randint(low, high)

        self.__set(rs, num)

    def __set_inf_32bits(self, rs) :
        pos_num = np.random.randint(2147483647 - 5, 2147483647)
        neg_num = np.random.randint(-2147483648, -2147483648 + 5)
        num = np.random.choice([pos_num, neg_num])

        self.__set(rs, num)

    def __set_inf_16bits(self, rs) :
        pos_num = np.random.randint(32767 - 5, 32767)
        neg_num = np.random.randint(-32768, -32768 + 5)
        num = np.random.choice([pos_num, neg_num])

        self.__set(rs, num)

    def __set_random_16bits(self, rs) :
        self.__mips.append(self.ori(0, rs, np.random.randint(-32768, 32767)))

    def __set_random_32bits(self, rs) :
        low = np.random.randint(-2147483648, -1)
        high = np.random.randint(2147483647)
        num = np.random.randint(low, high)

        self.__set(rs, num)

    def arth_test(self, times) :
        the_test = []
        for one in self.__unit["arth_test"]:
            the_test.extend(self.__class[one][:])
        
        set_mtds = ["__set_zero", "__set_inf_32bits", "__set_inf_16bits", "__set_random_32bits", "__set_random_16bits"]
        len0 = len(self.__mips)
        while (len(self.__mips) - len0) < times :
            rs = np.random.choice(self.__all_regs)
            rt = np.random.choice(self.__all_regs)
            rd = np.random.choice(self.__all_regs)
            set_mtd = np.random.choice(set_mtds)
            mtd = getattr(self, "_DataMaker" + set_mtd, None)
            mtd(rs)
            if rs != rt :
                set_mtd = np.random.choice(set_mtds)
                mtd = getattr(self, "_DataMaker" + set_mtd, None)
                mtd(rt)
            mtd_name = np.random.choice(the_test)
            mtd = getattr(self, mtd_name, None)
            if mtd_name in self.__class["md"]:
                if len(self.__mips) > (times // 2):
                    flag = True
                    if "div" in mtd_name and self.__grf[rt] == 0:
                        flag = False
                    if flag :
                        # print(f"${rt}: {self.__grf[rt]}")
                        self.__mips.append(mtd(rs, rt))
                        self.__mips.append(self.mfhi(np.random.choice(self.__all_regs)))
                        self.__mips.append(self.mflo(np.random.choice(self.__all_regs)))
            else:
                self.__mips.append(mtd(rs, rt, rd))

        return self.__mips


    def mem_test(self, times) :
        the_test = []
        for one in self.__unit["mem_test"]:
            the_test.extend(self.__class[one][:])
        
        set_mtds = ["__set_zero", "__set_inf_32bits", "__set_inf_16bits", "__set_random_32bits", "__set_random_16bits"]
        
        while len(self.__mips) < times :
            set_mtd = np.random.choice(set_mtds)
            mtd = getattr(self, "_DataMaker" + set_mtd, None)
            rt = np.random.choice(self.__all_regs)
            
            mtd(rt)

            for _ in range(5):
                base = np.random.choice(self.__all_regs)
                flag = True if base != 0 else False
                off = np.random.randint(0, 400)
                imm = np.random.randint(0, 400)
                if flag:
                        imm = np.random.randint(-32768, 32768)
                mtd_name = np.random.choice(the_test)
                mtd = getattr(self, mtd_name, None)
                    
                if "h" in mtd_name:
                    off >>= 1
                    off <<= 1
                    if not flag:
                        imm >>= 1
                        imm <<= 1
                elif "w" in mtd_name:
                    off >>= 2
                    off <<= 2
                    if not flag:
                        imm >>= 2
                        imm <<= 2
                
                self.__set(base, off - imm)
                self.__mips.append(mtd(base, rt, imm))

        return self.__mips        

    def branch_test(self, times) :
        the_test = []
        for one in self.__unit["branch_test"]:
            the_test.extend(self.__class[one][:])

        i = 0
        len0 = len(self.__mips)
        while (len(self.__mips) -len0) < times :
            is_br = np.random.randint(2)
            choice = np.random.choice([1, 2])

            mtd_name = np.random.choice(the_test)
            mtd = getattr(self, mtd_name, None)
            rs = np.random.choice(self.__all_regs)
            rt = np.random.choice(self.__all_regs)
            label = f"Branch_{i}"
            if is_br == 0 and rs != rt:
                if mtd_name == "beq": 
                    num1 = np.random.randint(0, 32767)
                    num2 = np.random.randint(32768, 65535)
                elif mtd_name == "bne":
                    num1 = np.random.randint(0, 65535)
                    num2 = num1
                self.__mips.append(self.ori(0, rs, num1))
                self.__mips.append(self.ori(0, rt, num2))
                self.__mips.append(mtd(rs, rt, label))
                self.arth_test(1)
                self.__mips.append(label + ":\n")
            else :
                if choice == 1 :
                    if rs != rt:
                        if mtd_name == "beq":
                            num1 = np.random.randint(0, 65535)
                            num2 = num1
                        elif mtd_name == "bne":
                            num1 = np.random.randint(0, 32767)
                            num2 = np.random.randint(32768, 65535)
                    self.__mips.append(self.ori(0, rs, num1))
                    self.__mips.append(self.ori(0, rt, num2))
                    self.__mips.append(mtd(rs, rt, label))
                    self.__mips.append(self.nop())
                    self.__mips.append(self.ori(0, rs, np.random.randint(0, 65535)))
                    self.__mips.append(label + ":\n")
                    
                elif choice == 2 and rs != rt :
                    rd = 1
                    while True :
                        rd = np.random.randint(1, 32)
                        if rd != rs and rd != rt:
                            break
                    if rs != 0 or rt != 0:
                        i += 1
                        continue
                    num = np.random.randint(10, 65535)
                    num1 = np.random.randint(1, num // 4)
                    self.__mips.append(self.ori(0, rs, num))
                    if mtd_name == "beq":
                        self.__mips.append(self.ori(0, rt, num - num1))
                    elif mtd_name == "bne":
                        self.__mips.append(self.ori(0, rt, num - 3* num1))
                    self.__mips.append(self.ori(0, rd, num1))
                    self.__mips.append(label + ":\n")
                    self.__mips.append(self.add(rt, rd, rt))
                    self.__mips.append(mtd(rs, rt, label))
                    self.__mips.append(self.nop())
            i += 1
        return self.__mips

    def jump_test(self, times) :
        index = 0
        index_b = 0
        len0 = len(self.__mips)
        while (len(self.__mips) -len0) < (times // 2) :
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
                label = f"Jump_{i + index}"
                jlabel = f"Jump_{int(pos[i] + index)}"
                self.__mips.append(label + ":\n")
                self.__mips.append(self.jal(jlabel))
                self.__mips.append(self.nop())
            label = f"Jump_{x + index}"
            self.__mips.append(label + ":\n")
            self.__mips.append(self.nop())
            index += x + 1
            
        while len(self.__mips) < times :
            rs = np.random.randint(1, 31)
            jlabel = f"Jump_{index_b + index}"
            blabel = f"BranchforJ_{index_b}"
            self.__mips.append(self.beq(0, 0, blabel))
            self.__mips.append(jlabel + ":\n")
            self.__mips.append(self.add(31, 0, rs))
            self.__mips.append(self.jr(rs))
            self.__mips.append(self.nop())
            self.__mips.append(blabel + ":\n")
            self.__mips.append(self.jal(jlabel))
            self.__mips.append(self.nop())
            index_b += 1
        
        return self.__mips

    def unit_test(self, times, test_dir="."):
        self.set_test(times)
        with open(os.path.join(test_dir, "set_test.asm"), "w", encoding="utf-8") as file:
            file.writelines(self.__mips)
        self.__mips = []

        self.arth_test(times)
        with open(os.path.join(test_dir, "arth_test.asm"), "w", encoding="utf-8") as file:
            file.writelines(self.__mips)
        self.__mips = []

        self.mem_test(times)
        with open(os.path.join(test_dir, "mem_test.asm"), "w", encoding="utf-8") as file:
            file.writelines(self.__mips)
        self.__mips = []
    
        self.branch_test(times)
        with open(os.path.join(test_dir, "branch_test.asm"), "w", encoding="utf-8") as file:
            file.writelines(self.__mips)
        self.__mips = []

        self.jump_test(times)
        with open(os.path.join(test_dir, "jump_test.asm"), "w", encoding="utf-8") as file:
            file.writelines(self.__mips)
        self.__mips = []


    def __ignore_overflow(self, number) -> int:
        number = number & 0xffffffff
        if number > 0x7fffffff :
            number -= 0x100000000
        return int(number)
    
    def __unsigned(self, number) -> int:
        number = number & 0xffffffff
        if number < 0 :
            number += 0x100000000
        return int(number)

    def lui(self, rt, offset, flag=True) -> str :
        self.__pc += 1
        offset = offset & 0xffff
        if flag and int(rt) != 0:
            self.__grf[rt] = self.__ignore_overflow(offset << 16)
            # self.__log.append(f"lui ${rt}, {offset:#x} : {rt} <= {(self.__ignore_overflow(offset << 16) & 0xfffffff):#x}\n")
        return f"lui ${rt}, {offset:#x}\n"

    def ori(self, rs, rt, offset, flag=True) -> str :
        self.__pc += 1
        offset = offset & 0xffff
        if flag and int(rt) != 0:
            self.__grf[rt] = self.__ignore_overflow(self.__unsigned(self.__grf[rs]) | offset)
            # self.__log.append(f"ori ${rt}, ${rs}, {offset:#x} : {rt} <= {(self.__ignore_overflow(self.__unsigned(self.__grf[rs]) | offset) & 0xfffffff):#x}\n")

        return f"ori ${rt}, ${rs}, {offset:#x}\n"    

    def addi(self, rs, rt, offset, flag=True) -> str :
        self.__pc += 1
        if flag and int(rt) != 0:
            self.__grf[rt] = self.__ignore_overflow(self.__grf[rs] + offset)
            # self.__log.append(f"addi ${rt}, ${rs}, {offset} : {rt} <= {(self.__ignore_overflow(self.__grf[rs] + offset) & 0xfffffff):#x}\n")

        return f"addi ${rt}, ${rs}, {offset}\n"
    
    def andi(self, rs, rt, offset, flag=True) -> str :
        self.__pc += 1
        offset = offset & 0xffff
        if flag and int(rt) != 0:
            self.__grf[rt] = self.__ignore_overflow(self.__unsigned(self.__grf[rs]) & offset)
            # self.__log.append(f"andi ${rt}, ${rs}, {offset:#x} : {rt} <= {(self.__ignore_overflow(self.__unsigned(self.__grf[rs]) & offset) & 0xfffffff):#x}\n")

        return f"andi ${rt}, ${rs}, {offset:#x}\n"

    def add(self, rs, rt, rd, flag=True) -> str :
        self.__pc += 1
        if flag and int(rd) != 0:
            self.__grf[rd] = self.__ignore_overflow(self.__grf[rs] + self.__grf[rt])
            # self.__log.append(f"add ${rd}, ${rs}, ${rt} : {rd} <= {(self.__ignore_overflow(self.__grf[rs] + self.__grf[rt]) & 0xfffffff):#x}\n")

        return f"add ${rd}, ${rs}, ${rt}\n"

    def sub(self, rs, rt, rd, flag=True) -> str :
        self.__pc += 1
        if flag and int(rd) != 0:
            self.__grf[rd] = self.__ignore_overflow(self.__grf[rs] - self.__grf[rt])
            # self.__log.append(f"sub ${rd}, ${rs}, ${rt} : {rd} <= {(self.__ignore_overflow(self.__grf[rs] - self.__grf[rt]) & 0xfffffff):#x}\n")

        return f"sub ${rd}, ${rs}, ${rt}\n"

    def andr(self, rs, rt, rd, flag=True) -> str :
        self.__pc += 1
        if flag and int(rd) != 0:
            self.__grf[rd] = self.__ignore_overflow(self.__grf[rs] & self.__grf[rt])
            # self.__log.append(f"and ${rd}, ${rs}, ${rt} : {rd} <= {(self.__ignore_overflow(self.__grf[rs] & self.__grf[rt]) & 0xfffffff):#x}\n")
        return f"and ${rd}, ${rs}, ${rt}\n"

    def orr(self, rs, rt, rd, flag=True) -> str :
        self.__pc += 1
        if flag and int(rd) != 0 :
            self.__grf[rd] = self.__ignore_overflow(self.__grf[rs] | self.__grf[rt])
            # self.__log.append(f"or ${rd}, ${rs}, ${rt} : {rd} <= {(self.__ignore_overflow(self.__grf[rs] | self.__grf[rt]) & 0xfffffff):#x}\n")

        return f"or ${rd}, ${rs}, ${rt}\n"
    
    def slt(self, rs, rt, rd, flag=True) -> str :
        self.__pc += 1
        if flag and int(rd) != 0 :
            self.__grf[rd] = 1 if self.__grf[rs] < self.__grf[rt] else 0
            # self.__log.append(f"slt ${rd}, ${rs}, ${rt}: {rd} <= {1 if self.__grf[rs] < self.__grf[rt] else 0}\n")
        return f"slt ${rd}, ${rs}, ${rt}\n"
    
    def sltu(self, rs, rt, rd, flag=True) -> str :
        self.__pc += 1
        if flag and int(rd) != 0:
            self.__grf[rd] = 1 if self.__unsigned(self.__grf[rs]) < self.__unsigned(self.__grf[rt]) else 0
            # self.__log.append(f"sltu ${rd}, ${rs}, ${rt}: {rd} <= {1 if self.__unsigned(self.__grf[rs]) < self.__unsigned(self.__grf[rt]) else 0}\n")
            
        return f"sltu ${rd}, ${rs}, ${rt}\n"

    def lw(self, base, rt, offset, flag=True) -> str :
        self.__pc += 1
        off = (int(self.__grf[int(base)]) + int(offset)) >> 2
        if flag and int(rt) != 0:
            self.__grf[rt] = self.__ignore_overflow(self.__dm[off])
            # self.__log.append(f"lw ${rt}, {int(offset)}(${base}): {rt} <= {(self.__ignore_overflow(self.__dm[off]) & 0xffffffff):#x}\n")
        return f"lw ${rt}, {int(offset)}(${base})\n"

    def lh(self, base, rt, offset, flag=True) -> str :
        self.__pc += 1
        off = (int(self.__grf[base]) + int(offset)) >> 2
        adder = (int(self.__grf[base]) + int(offset)) & 0x3
        mask = (0xffff << (adder * 8))
        if flag and int(rt) != 0:
            num = ((self.__dm[off] & mask) >> (adder * 8)) & 0xffff
            if num & 0x8000 != 0 :
                num = num - 0x10000
            self.__grf[rt] = self.__ignore_overflow(num)
            # self.__log.append(f"lh ${rt}, {int(offset)}(${base}): {rt} <= {(self.__ignore_overflow(num) & 0xffffffff):#x}\n")
        return f"lh ${rt}, {int(offset)}(${base})\n"
    
    def lb(self, base, rt, offset, flag=True) -> str :
        self.__pc += 1
        off = (int(self.__grf[base]) + int(offset)) >> 2
        adder = (int(self.__grf[base]) + int(offset)) & 0x3
        mask = (0xff << (adder * 8))
        if flag and int(rt) != 0:
            num = ((self.__dm[off] & mask) >> (adder * 8)) & 0xff
            if num & 0x80 != 0 :
                num = num - 0x100
            self.__grf[rt] = self.__ignore_overflow(num)
            # self.__log.append(f"lb ${rt}, {int(offset)}(${base}): {rt} <= {(self.__ignore_overflow(num) & 0xffffffff):#x}\n")
        return f"lb ${rt}, {int(offset)}(${base})\n"

    def sw(self, base, rt, offset, flag=True) -> str :
        self.__pc += 1
        off = (int(self.__grf[int(base)]) + int(offset)) >> 2
        if flag:
            self.__dm[off] = self.__ignore_overflow(self.__grf[rt])
            # self.__log.append(f"sw ${rt}, {int(offset)}(${base}): {off} <= {(self.__ignore_overflow(self.__grf[rt]) & 0xffffffff):#x}\n")
            
        return f"sw ${rt}, {int(offset)}(${base})\n"

    def sh(self, base, rt, offset, flag=True) -> str :
        self.__pc += 1
        off = (int(self.__grf[base]) + int(offset)) >> 2
        adder = (int(self.__grf[base]) + int(offset)) & 0x3
        mask = (0xffffffff - (0xffff << (adder * 8)))
        if flag:
            toset = self.__grf[rt]
            if toset < 0:
                toset += 0x100000000
            toset = (toset & 0xffff) << (adder * 8)
            self.__dm[off] = self.__ignore_overflow((self.__dm[off] & mask) | toset )
            # self.__log.append(f"sh ${rt}, {int(offset)}(${base}): {off} <= {(self.__ignore_overflow((self.__dm[off] & mask) | toset ) & 0xffffffff):#x}\n")

        return f"sh ${rt}, {int(offset)}(${base})\n"

    def sb(self, base, rt, offset, flag=True) -> str :
        self.__pc += 1
        off = (int(self.__grf[base]) + int(offset)) >> 2
        adder = (int(self.__grf[base]) + int(offset)) & 0x3
        mask = (0xffffffff - (0xff << (adder * 8)))
        if flag:
            toset = self.__grf[rt]
            if toset < 0:
                toset += 0x100000000
            toset = (toset & 0xff) << (adder * 8)
            self.__dm[off] = self.__ignore_overflow((self.__dm[off] & mask) | toset)
            # self.__log.append(f"sb ${rt}, {int(offset)}(${base}): {off} <= {(self.__ignore_overflow((self.__dm[off] & mask) | toset ) & 0xffffffff):#x}\n")
        return f"sb ${rt}, {int(offset)}(${base})\n"
    
    def mult(self, rs, rt, flag=True) -> str :
        self.__pc += 1
        num = self.__grf[rs] * self.__grf[rt]
        if flag:    
            self.__hi = self.__ignore_overflow((num & 0xffffffff00000000) >> 32 ) & 0xffffffff
            self.__lo = self.__ignore_overflow(num & 0xffffffff)
            # self.__log.append(f"mult ${rs}, ${rt}: hi <= {(self.__ignore_overflow((num & 0xffffffff00000000) >> 32 ) & 0xffffffff):#x}, lo <= {self.__ignore_overflow(num & 0xffffffff):#x}\n")
        return f"mult ${rs}, ${rt}\n"

    def multu(self, rs, rt, flag=True) -> str :
        self.__pc += 1
        num = self.__unsigned(self.__grf[rs]) * self.__unsigned(self.__grf[rt])
        if flag :
            self.__hi = self.__ignore_overflow((num & 0xffffffff00000000) >> 32) & 0xffffffff
            self.__lo = self.__ignore_overflow(num & 0xffffffff)
            # self.__log.append(f"multu ${rs}, ${rt}: hi <= {(self.__ignore_overflow((num & 0xffffffff00000000) >> 32 ) & 0xffffffff):#x}, lo <= {self.__ignore_overflow(num & 0xffffffff):#x}\n")
        return f"multu ${rs}, ${rt}\n"
    
    def div(self, rs, rt, flag=True) -> str :
        self.__pc += 1
        a = self.__grf[rs]
        b = self.__grf[rt]
        quotient = int(a / b) 
        # MARS 中的余数（与被除数符号一致）
        remainder = a - quotient * b  # 根据 a == (a // b) * b + (a % b)
        # 如果余数符号不匹配被除数，则调整余数和商
        if remainder != 0 and (remainder < 0) != (a < 0):
            remainder -= b
            quotient += 1

        if flag:
            self.__hi = self.__ignore_overflow(remainder & 0xffffffff)
            self.__lo = self.__ignore_overflow(quotient & 0xffffffff)
            # self.__log.append(f"div ${rs}, ${rt}: hi <= {(self.__ignore_overflow(remainder & 0xffffffff)):#x}, lo <= {self.__ignore_overflow(quotient & 0xffffffff):#x}\n")
        return f"div ${rs}, ${rt}\n"

    def divu(self, rs, rt, flag=True) -> str :
        self.__pc += 1
        a = self.__grf[rs]
        b = self.__grf[rt]
        if a < 0:
            a += 0x100000000
            a &= 0xffffffff
        if b < 0:
            b += 0x100000000
            b &= 0xffffffff

        if flag:
            self.__hi = self.__ignore_overflow((a % b) & 0xffffffff)
            self.__lo = self.__ignore_overflow((a // b) & 0xffffffff)
            # self.__log.append(f"divu ${rs}, ${rt}: hi <= {(self.__ignore_overflow((a % b) & 0xffffffff)):#x}, lo <= {self.__ignore_overflow((a // b) & 0xffffffff):#x}\n")
        return f"divu ${rs}, ${rt}\n"

    def mfhi(self, rd, flag=True) -> str :
        self.__pc += 1
        if flag and int(rd) != 0:
            self.__grf[rd] = self.__ignore_overflow(self.__hi)
            # self.__log.append(f"mfhi ${rd}: {rd} <= {self.__ignore_overflow(self.__hi):#x}\n")
        return f"mfhi ${rd}\n"
    
    def mflo(self, rd, flag=True) -> str :
        self.__pc += 1
        if flag and int(rd) != 0:
            self.__grf[rd] = self.__ignore_overflow(self.__lo)
            # self.__log.append(f"mflo ${rd}: {rd} <= {self.__ignore_overflow(self.__lo):#x}\n")
        return f"mflo ${rd}\n"
    
    def mthi(self, rs, flag=True) -> str :
        self.__pc += 1
        if flag:
            self.__hi = self.__ignore_overflow(self.__grf[rs])
            # self.__log.append(f"mfhi ${rs}: hi <= {self.__ignore_overflow(self.__grf[rs]):#x}\n")
        return f"mthi ${rs}\n"
    
    def mtlo(self, rs, flag=True) -> str :
        self.__pc += 1
        if flag:
            self.__lo = self.__ignore_overflow(self.__grf[rs])
            # self.__log.append(f"mfhi ${rs}: lo <= {self.__ignore_overflow(self.__grf[rs]):#x}\n")
        return f"mtlo ${rs}\n"

    def beq(self, rs, rt, offset) -> str :
        self.__pc += 1
        return f"beq ${rs}, ${rt}, {offset}\n"

    def bne(self, rs, rt, offset) -> str :
        self.__pc += 1
        return f"bne ${rs}, ${rt}, {offset}\n"

    def nop(self) -> str :
        self.__pc += 1
        return "nop\n"

    def jal(self, offset, flag=True) -> str :
        self.__pc += 1
        if flag:
            self.__grf[31] = self.__ignore_overflow(self.__get_pc() + 4)
            # self.__log.append(f"jal {offset}: 31 <= {self.__ignore_overflow(self.__get_pc() + 4):#x}\n")
        return f"jal {offset}\n"

    def jr(self, rs) -> str :
        self.__pc += 1
        return f"jr ${rs}\n"


if __name__ == "__main__" :
    datamaker = DataMaker()
    # datamaker.get_regs()
    # lui = datamaker.method("lui")(1, 32223)
    # print(lui)
    # datamaker.random_test(3600)
    datamaker.unit_test(4000)
    # print(int("7fffffff", 16))
    # print(-int("80000000", 16))
    # print(datamaker.ignore_overflow(-2147483649))
    # print(datamaker.unsigned(-1))
    # print(datamaker.unsigned(2147483647))
    # print(datamaker.unsigned(-2147483648))
    # res = 0xf234f678
    # off = 0x1234567f
    # num = -1
    # adder = off & 0x3
    # mask = (0xffffffff - (0xff << (adder * 8)))
    # toset = num
    # if toset < 0:
    #     toset += 0x100000000
    # toset = (toset & 0xff) << (adder * 8)
    # res = (res & mask) | toset
    # print(f"{res:#x}")