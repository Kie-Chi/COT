import numpy as np

class DataMaker:
    def __init__(self):
        self.__class = {
            "cal_r": ['add', 'sub'],
            "cal_i": ['ori'],
            "lui": ['lui'],
            "store": ['sw'],
            "load": ['lw'],
            "branch": ['beq'],
            "j_l": ['jal'],
            "j_r": ['jr'],
            "nop": ['nop']
        }
        self.__nojump = ["cal_r", "cal_i", "lui", "store", "load", "j_l", "j_r", "nop"]
        self.__get_regs()
        self.__pc = 0
        self.__mips = []
        self.__unused = []
        self.__count = 0
        self.__grf = [0 for _ in range(32)] 
        self.__dm = [0 for _ in range(3072)]

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
            rs = rd
            rt = np.random.choice(self.__test_regs)
            rd = np.random.choice(self.__test_regs)
            reg = 0
            imm = np.random.randint(0, 200)
            # imm = imm >> 2
            # imm = imm << 2
            offset = f"Test{self.__count}End"

            j_flag = False

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
            register = [rs, rt, rd, imm, offset, reg, j_flag]
            registers.append(register)

        the_ind = 0
        jump_flag = False
        store_flag = False
        not_jump = True
        for the_test in the_tests:
            rs = registers[the_ind][0]
            rt = registers[the_ind][1]
            rd = registers[the_ind][2]
            imm = registers[the_ind][3]
            offset = registers[the_ind][4]
            reg = registers[the_ind][5]
            j_flag = registers[the_ind][6]
            jump_flag = jump_flag or j_flag
            the_ind += 1

            code, useless, store_now, not_jump = self.method(the_test, rs=rs, rt=rt, rd=rd, imm=imm, offset=offset, flag=not_jump)
            store_flag = store_flag or store_now
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
        for test_reg in self.__test_regs:
            if test_reg != 0:
                if self.__grf[test_reg] > 200 or self.__grf[test_reg] < -200:
                # num = np.random.randint(0, 200) >> 2
                # num = num << 2
                    num = np.random.randint(0, 200)
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
            num = np.random.randint(0, 200)
            self.__mips.append(self.ori(0, test_reg, num))

        lens = len(self.__jump_regs)
        for i in range(lens):
            self.__mips.append(self.ori(0, self.__jump_regs[i], np.random.choice([jump_initial[i], jump_initial[-1]])))

    def __init_dm(self):
        the_new = np.concatenate((self.__test_regs, self.__jump_regs), axis=0)
        for _ in range(20):
            off = np.random.randint(0, 200)
            off = off >> 2
            off = off << 2
            self.__mips.append(self.sw(0, np.random.choice(the_new), off))

    def random_test(self, max_time) :
        jump_initial = self.__create_jarea()
        self.__init_regs(jump_initial)
        self.__init_dm()
        while len(self.__mips) <= max_time:
            self.__create_test(jump_initial)

        with open("test.asm", "w", encoding="utf-8") as file:
            file.writelines(self.__mips)
        return self.__mips

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
            while True:
                if imm < 32767 and imm > -32768:
                    break
                
                if self.__grf[rs] > (32700 + 3072 * 4) or self.__grf[rs] < -32700:
                    for test_reg in self.__test_regs:
                        if test_reg != 0:
                            if self.__grf[test_reg] > 200 or self.__grf[test_reg] < -200:
                            # num = np.random.randint(0, 200) >> 2
                            # num = num << 2
                                num = np.random.randint(0, 200)
                                self.__mips.append(self.ori(0, test_reg, num))
                    return 
                
                off = np.random.randint(0, 10000)
                off = off >> 2
                off = off << 2
                imm = off - self.__grf[rs]
            if mtd_class == "store":
                if self.__grf[rt] > int("6fff", 16) or self.__grf[rt] < -int("6fff", 16):
                    store_flag = True
        elif mtd_class == "branch":
            the_jump = self.__grf[rs] == self.__grf[rt]
        
        flag = not the_jump and flag
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
        else: 
            the_return = [mtd(), 0]

        the_return.append(store_flag)
        the_return.append(flag)
        return the_return

    def lui(self, rt, offset, flag=True) -> str :
        self.__pc += 1
        if flag:
            self.__grf[rt] = (offset << 16) if int(rt) != 0 else 0
        return f"lui ${rt}, {offset:#x}\n"

    def ori(self, rs, rt, offset, flag=True) -> str :
        self.__pc += 1
        if flag:
            self.__grf[rt] = (self.__grf[rs] | offset) if int(rt) != 0 else 0
        return f"ori ${rt}, ${rs}, {offset:#x}\n"    

    def add(self, rs, rt, rd, flag=True) -> str :
        self.__pc += 1
        if flag:
            self.__grf[rd] = (self.__grf[rs] + self.__grf[rt]) if int(rd) != 0 else 0
        return f"add ${rd}, ${rs}, ${rt}\n"

    def sub(self, rs, rt, rd, flag=True) -> str :
        self.__pc += 1
        if flag:
            self.__grf[rd] = (self.__grf[rs] - self.__grf[rt]) if int(rd) != 0 else 0
        return f"sub ${rd}, ${rs}, ${rt}\n"

    def lw(self, base, rt, offset, flag=True) -> str :
        self.__pc += 1
        off = (int(self.__grf[int(base)]) + int(offset)) >> 2
        if flag:
            self.__grf[rt] = self.__dm[off] if rt != 0 else 0
        return f"lw ${rt}, {int(offset)}(${base})\n"

    def sw(self, base, rt, offset, flag=True) -> str :
        self.__pc += 1
        off = (int(self.__grf[int(base)]) + int(offset)) >> 2
        if flag:
            self.__dm[off] = self.__grf[rt]
        return f"sw ${rt}, {int(offset)}(${base})\n"

    def beq(self, rs, rt, offset) -> str :
        self.__pc += 1
        return f"beq ${rs}, ${rt}, {offset}\n"

    def nop(self) -> str :
        self.__pc += 1
        return "nop\n"

    def jal(self, offset, flag=True) -> str :
        self.__pc += 1
        if flag:
            self.__grf[31] = self.__get_pc() + 4
        return f"jal {offset}\n"

    def jr(self, rs) -> str :
        self.__pc += 1
        return f"jr ${rs}\n"


if __name__ == "__main__" :
    datamaker = DataMaker()
    # datamaker.get_regs()
    # lui = datamaker.method("lui")(1, 32223)
    # print(lui)
    datamaker.random_test(3600)