import json
import os
import os.path
from pathlib import Path
import re
import shutil
import sys

import numpy as np
from Runner import LogisimRunner, XilinxRunner, Runner
import Runner
from DataMaker import DataMaker
from Config import Config
import time
from typing import Tuple
from DataMaker import DataMaker

def _random_test_task(params: Tuple[int, bool, bool, str, int, int, bool]):
    times, exc, with_mars, out_path, random_set, unit_set, flow = params
    datamaker = DataMaker(random_set, unit_set, flow)
    datamaker.random_test(times, exc, with_mars, out_path)

class Machine :
    def __init__(self, pool=None) :
        self.__test_dir = "2024-11-27-23-43-04-withOthers-excTest"
        self.__config = Config()
        self.__cpu_dir = ""
        self.__asm_dir = "exc"            
        self.__runner = None
        self.__test_times = 0
        self.__pool = pool

    
    def create_test(self) :
        self.__create_testdir()
        self.__gen_data()
        self.__create_runner()


    def __gift(self):
        input("Please enter your password: ")
        self.__exit()

    def start_test(self) :
        flag = True
        self.__get_std_mars()
        if self.__config.type == "logisim" :
            self.__run_logisim()
        elif self.__config.type == "verilog" :
            flag = self.__run_xilinx()
        if flag:
            self.__judge()
        else:
            raise Exception

    def __create_runner(self) :
        if self.__config.type == "logisim" :
            self.__runner = LogisimRunner(self.__config.logisim_path, self.__config.mars_path, self.__test_dir, self.__config.flow, self.__config.exc, self.__pool)
            self.__cpu_dir = self.__config.cir_dir
        elif self.__config.type == "verilog" :
            self.__runner = XilinxRunner(self.__config.xilinx_path, self.__config.mars_path, self.__config.verilog_dir, self.__test_dir, self.__config.flow, self.__config.exc, self.__config.tb, self.__asm_dir, self.__pool)
            self.__cpu_dir = self.__config.verilog_dir    

    def __create_testdir(self) :
        local_time = time.localtime()
        formatted_time = time.strftime("%Y-%m-%d-%H-%M-%S", local_time)
        self.__test_dir = f"{formatted_time}-{self.__config.src}-{self.__config.mtd}"
        # os.system(f"mkdir -p {test_dir}")
        Runner.safe_makedirs(self.__test_dir, exist_ok=True)

    def __set_testcode(self, start):
        dirs, useless = Runner.find_dirs(self.__config.self_dir)
        for _dir in dirs:
            asm, useless = Runner.find_files(_dir, ".asm")
            if len(asm) == 1:
                Runner.safe_copy(asm[0], os.path.join(self.__test_dir, self.__asm_dir, f"self_{start}.asm"))
            elif len(asm) == 2:
                handler = asm[0] if "handler" in os.path.basename(asm[0]) else asm[1]
                code = asm[1] if "handler" in os.path.basename(asm[0]) else asm[1]
                contents = []
                with open(handler, "r", encoding="utf-8") as handler_file:
                    contents = handler_file.readlines()
                
                mips = []
                with open(code, "r", encoding="utf-8") as file:
                    mips = file.readlines()
                mips = [code for code in mips if code.strip() != ""]
                mips = [code for code in mips if code.strip()[-1] != ":"]
                mips = [code for code in mips if code.strip()[0] != "#"]
                nops = ["nop\n" for _ in range(1120 - len(mips))]
                mips.extend(nops)
                mips.extend(contents)
                with open(os.path.join(self.__test_dir, self.__asm_dir, f"self_{start}.asm"), "w", encoding="utf-8") as file:
                    file.writelines(mips)
            tb, useless = Runner.find_files(_dir, ".v")
            if tb != []:
                tb = tb[0]
                Runner.safe_makedirs(os.path.join(self.__test_dir, "tbs"))
                Runner.safe_copy(tb, os.path.join(self.__test_dir, "tbs", f"self_{start}_tb.v"))
            start += 1

    def __gen_data(self) :
        times = 0

        if self.__config.type == "logisim" :
            times = 880
        elif self.__config.type == "verilog" :
            times = 3600

        datamaker = DataMaker(self.__config.random_set, self.__config.unit_set, self.__config.flow)
        if self.__config.mtd == "lazyTest" :
            self.__asm_dir = "lazy"
            Runner.safe_makedirs(os.path.join(self.__test_dir, self.__asm_dir))
            datamaker.unit_test(times, self.__config.exc, self.__config.type, os.path.join(self.__test_dir, self.__asm_dir))
            if self.__config.exc:
                datamaker.exc_test(1000, self.__config.src == "withMars", os.path.join(self.__test_dir, self.__asm_dir))
                if self.__config.src != "withMars":
                    Runner.safe_makedirs(os.path.join(self.__test_dir, "tbs"))
                    datamaker.int_test(800, False, True, os.path.join(self.__test_dir, self.__asm_dir), os.path.join(self.__test_dir, "tbs"))
            tasks = []
            for i in range(50):
                out_path = os.path.join(self.__test_dir, self.__asm_dir, f"lazy_{i}.asm")
                tasks.append((times, self.__config.exc, self.__config.src == "withMars", out_path, self.__config.random_set, self.__config.unit_set, self.__config.flow))
            if self.__pool is not None:
                list(self.__pool.map(_random_test_task, tasks))
            else:
                for params in tasks:
                    _random_test_task(params)
        elif self.__config.mtd == "randomTest" :
            self.__asm_dir = "random"
            Runner.safe_makedirs(os.path.join(self.__test_dir, self.__asm_dir))
            x = self.__config.test_times
            tasks = []
            for i in range(x):
                out_path = os.path.join(self.__test_dir, self.__asm_dir, f"random_{i}.asm")
                tasks.append((times, self.__config.exc, self.__config.src == "withMars", out_path, self.__config.random_set, self.__config.unit_set, self.__config.flow))
            if self.__pool is not None:
                list(self.__pool.map(_random_test_task, tasks))
            else:
                for params in tasks:
                    _random_test_task(params)

        elif self.__config.mtd == "unitTest" :
            self.__asm_dir = "unit"
            Runner.safe_makedirs(os.path.join(self.__test_dir, self.__asm_dir))
            datamaker.unit_test(times, self.__config.exc, self.__config.type, os.path.join(self.__test_dir, self.__asm_dir))

        elif self.__config.mtd == "excTest" :
            self.__asm_dir = "exc"
            Runner.safe_makedirs(os.path.join(self.__test_dir, self.__asm_dir))
            datamaker.exc_test(1000, self.__config.src == "withMars", os.path.join(self.__test_dir, self.__asm_dir))

        elif self.__config.mtd == "intTest" :
            self.__asm_dir = "int"
            Runner.safe_makedirs(os.path.join(self.__test_dir, self.__asm_dir))
            Runner.safe_makedirs(os.path.join(self.__test_dir, "tbs"))
            datamaker.int_test(800, False, False, os.path.join(self.__test_dir, self.__asm_dir), os.path.join(self.__test_dir, "tbs"))

        elif self.__config.mtd == "selfTest" :
            self.__asm_dir = "self"
            Runner.safe_makedirs(os.path.join(self.__test_dir, self.__asm_dir))
            x = self.__config.test_times
            ind = 0
            self_paths, self_files = Runner.find_files(self.__config.self_dir, "asm")
            self_paths = [path for path in self_paths if path.split(os.sep)[-2] == self.__config.self_dir]
            for file in self_paths:
                Runner.safe_copy(file, os.path.join(self.__test_dir, self.__asm_dir, f"self_{ind}.asm"))
                ind += 1
            
            self_paths, self_files = Runner.find_files(self.__config.self_dir, "txt")
            self_paths = [path for path in self_paths if path.split(os.sep)[-2] == self.__config.self_dir]
            for file in self_paths:
                disam = [
                    os.path.join("util", "disasm.exe"),
                    "-i",
                    file,
                    "-o",
                    os.path.join(self.__test_dir, self.__asm_dir, f"self_{ind}.asm")
                ]
                Runner.safe_execute(disam, "test.txt")
                ind += 1
            Runner.safe_remove("test.txt")
            self.__set_testcode(ind)

            if x > ind :
                temp = x - ind
                if self.__config.self_util != "":
                    for i in range(temp) :
                        if self.__config.self_util.endswith(".exe") :
                            command = [
                                self.__config.self_util
                            ]
                            command = " ".join(command)
                            Runner.safe_execute(command, os.path.join(self.__test_dir, "self", f"self_{ind + i}.asm"))
                        elif self.__config.self_util.endswith(".jar") :
                            command = [
                                "java",
                                "-jar",
                                self.__config.self_util
                            ]
                            command = " ".join(command)
                            Runner.safe_execute(command, os.path.join(self.__test_dir, "self", f"self_{ind + i}.asm"))
                        elif self.__config.self_util.endswith(".py") :
                            command = [
                                "python",
                                self.__config.self_util
                            ]
                            command = " ".join(command)
                            Runner.safe_execute(command, os.path.join(self.__test_dir, "self", f"self_{ind + i}.asm"))
                        else:
                            Runner.print_colored("ERROR: Please check your self-util")
                            raise Exception
                else:
                    for i in range(temp):
                        datamaker.random_test(times, os.path.join(self.__test_dir, self.__asm_dir, f"self_{ind + i}.asm"))

        files, useless = Runner.find_files(os.path.join(self.__test_dir, self.__asm_dir))
        self.__test_times = len(files)

    def __get_std_mars(self) :
        # if src_slt == "withMars" :
        src = []
        src,more = Runner.find_files(os.path.join(self.__test_dir, self.__asm_dir))

        hex_dst = os.path.join(self.__test_dir, "hex")
        out_log = os.path.join(self.__test_dir, "stdout")
        if self.__config.src == "withMars" :
            self.__runner.run_mars(src, hex_dst, out_log)
        else :
            self.__runner.dump_hex(src, hex_dst)
        Runner.safe_remove(os.path.join(self.__test_dir, "info.txt"))
        Runner.safe_rmtree(os.path.join(self.__test_dir, "info"))

    def __run_logisim(self) :
        self.__load_all_circ()
        self.__run_all_circ()

    def __run_xilinx(self):
        flag = self.__runner.fuse()
        if not flag:
            return False
        self.__runner.run_isim()
        return True

    def __load_all_circ(self) :
        circ_file = Runner.find_files(self.__cpu_dir, ".circ")
        to_load = []
        # os.system(f"mkdir -p {test_dir}/circ")
        Runner.safe_makedirs(os.path.join(self.__test_dir, "circ"), exist_ok=True)
        lens = len(circ_file[0])
        for i in range(lens) :
            path = circ_file[0][i]
            name = circ_file[1][i]
            # os.system(f"cp {path} {test_dir}/circ/{name}")
            Runner.safe_copy(path, os.path.join(self.__test_dir, "circ", name))
            to_load.append(os.path.join(self.__test_dir, "circ", name))

        mips_test, more = Runner.find_files(os.path.join(self.__test_dir, "hex"))
        # Runner.print_colored(to_load)
        self.__runner.load_logisim(mips_test, *to_load) 

        for i in range(lens) :
            name = circ_file[1][i]
            # os.system(f"rm {test_dir}/circ/{name}")
            os.remove(os.path.join(self.__test_dir, "circ", name))

    def __run_all_circ(self) :
        circ_file, more = Runner.find_dirs(os.path.join(self.__test_dir, "circ"))
        # Runner.print_colored(circ_file)
        self.__runner.run_logisim(*circ_file)
        Runner.safe_rmtree(os.path.join(self.__test_dir, "circ"))

    def __delete(self, flag, wrong, circ_files, wrong_files) :
        if flag :
            # os.system(f"rm -rf {test_dir}")
            Runner.safe_rmtree(self.__test_dir, 10, 0.2)
            Runner.print_colored()
            Runner.print_colored("-------------------------", 32)
            Runner.print_colored("|                       |", 32)
            Runner.print_colored("|       ACCEPTED        |", 32)               
            Runner.print_colored("|                       |", 32)
            Runner.print_colored("-------------------------", 32)
            Runner.print_colored()
        else :
            Runner.print_colored()
            Runner.print_colored("--------------------------", 31)
            Runner.print_colored("|                        |", 31)
            Runner.print_colored("|      WRONG ANSWER      |", 31)
            Runner.print_colored("|                        |", 31)
            Runner.print_colored("--------------------------", 31)
            Runner.print_colored("Testcode: ", end="")
            ind = 0
            for i in sorted([wr.replace(".txt", "") for wr in wrong_files]):
                if ind == len(wrong_files) - 1:
                    Runner.print_colored(i)
                else:
                    Runner.print_colored(i, end=", ")
                ind += 1
            Runner.print_colored()
            for circ in circ_files :
                if circ not in wrong :
                    # os.system(f"rm -rf {test_dir}/circ/{circ}")
                    # os.system(f"rm -rf {test_dir}/log/{circ}")
                    # os.system(f"rm -rf {test_dir}/dif/{circ}")
                    if self.__config.src == "withMars" :
                        Runner.safe_rmtree(os.path.join(self.__test_dir, "log", circ))
                    Runner.safe_rmtree(os.path.join(self.__test_dir, "dif", circ))

            useless, stdouts = Runner.find_files(os.path.join(self.__test_dir, self.__asm_dir))
            for stdout in stdouts:
                if self.__config.src == "withOthers" and stdout.replace(".asm", ".txt") not in wrong_files:
                    Runner.safe_rmtree(os.path.join(self.__test_dir, "dif", stdout.replace(".asm", "")))
                if stdout.replace(".asm", ".txt") not in wrong_files :
                    for circ in circ_files :
                        Runner.safe_remove(os.path.join(self.__test_dir, "log", circ, f"{stdout.replace('.asm', '')}-{circ}-out.txt"))
                    Runner.safe_remove(os.path.join(self.__test_dir, self.__asm_dir, stdout))
                    Runner.safe_remove(os.path.join(self.__test_dir, "hex", stdout.replace(".asm", ".txt")))
                    if os.path.exists(os.path.join(self.__test_dir, "stdout")):
                        Runner.safe_remove(os.path.join(self.__test_dir, "stdout", stdout.replace(".asm", ".txt")))
            # Runner.safe_rmtree(os.path.join(self.__test_dir, self.__cpu_dir))

    def __compare_mars(self, file, stdouts) :
        def get_index(table, index) -> int:
            ind = 0
            for k in range(len(table)):
                if table[k] == 1:
                    ind += 1
                    if ind == index:
                        return k
            return -1
        flag = True
        name = file.split('-')[1]
        mips_test = file.split('-')[0]
        outputs = []
        with open(os.path.join(self.__test_dir, "log", name, file), "r", encoding="utf-8") as out :
            outputs = out.readlines()
        lens  = len(stdouts)
        i = 0 
        len1 = len(stdouts)
        len2 = len(outputs)
        lens = min(len1, len2)
        asm_source = []
        hex_source = []
        ori_source = []
        try:
            with open(os.path.join(self.__test_dir, self.__asm_dir, f"{mips_test}.asm"), "r", encoding="utf-8") as _asm:
                ori_source = _asm.readlines()
        except UnicodeDecodeError :
            with open(os.path.join(self.__test_dir, self.__asm_dir, f"{mips_test}.asm"), "r", encoding="GB2312") as _asm:
                ori_source = _asm.readlines()

        asm_source = [asm for asm in ori_source if asm.strip() != ""]
        asm_source = [src for src in asm_source if src.strip()[-1] != ":"]
        asm_source = [asm for asm in asm_source if asm.strip()[0] != "#"]
        table = [1 if asm.strip()!="" and asm.strip()[-1]!=":" and asm.strip()[0]!="#" else 0 for asm in ori_source]

        with open(os.path.join(self.__test_dir, "hex", f"{mips_test}.txt"), "r", encoding="utf-8") as _hex:
            hex_source = _hex.readlines()
        for i in range(lens) :
            if stdouts[i] != outputs[i] :
                flag = False
            
                pc = stdouts[i].split(" ")[0].strip("@:")
                pc = int(pc, 16) - int("3000", 16)
                dist = pc >> 2
                with open(os.path.join(self.__test_dir, "dif", name, f"{mips_test}-std-dif.log"), "w", encoding="utf-8") as dif :
                    dif.write(f"First error in line {i + 1}\n")
                    dif.write(f"------the first different Mips code \"{hex_source[dist].strip()}\"-----\n")
                    ind = get_index(table, dist+1)
                    dif.write(f"Mips Code: \"{asm_source[dist].strip()}\" in line {ind+1}\n")
                    dif.write(f"Mars: \"{stdouts[i].strip()}\"\n")
                    dif.write(f"{name}: \"{outputs[i].strip()}\"\n")
                    dif.write(f"---------------------------------------\n")
                    if i >= 1 :
                        pc = stdouts[i-1].split(" ")[0].strip("@:")
                        pc = int(pc, 16) - int("3000", 16)
                        dist = pc >> 2
                        ind = get_index(table, dist+1)
                        dif.write(f"the most recent same Mips code is: \"{asm_source[dist].strip()}\" in line {ind+1}\n")
                        dif.write(f"the most recent same Mips code output is: \"{outputs[i - 1].strip()}\"\n\n")
                break
        if len1 != len2 :
            with open(os.path.join(self.__test_dir, "dif", name, f"{mips_test}-std-dif.log"), "a", encoding="utf-8") as dif :
                dif.write(f"Error: lines don't equal!!!!,Please see\n\"out.txt\"\n\"stdout.txt\"")
            flag = False
            
        return flag, name

    def __compare_others(self, outputs, files) :
        def get_index(table, index) -> int:
            ind = 0
            for k in range(len(table)):
                if table[k] == 1:
                    ind += 1
                    if ind == index:
                        return k
            return -1
        flag = True
        wrong = []
        more, circ_files = Runner.find_dirs(os.path.join(self.__test_dir, "log"))
        person = len(outputs)
        test = len(files)
        # Runner.print_colored(test)
        # Runner.print_colored(files)
        # Runner.print_colored(person)
        # Runner.print_colored(len(outputs))
        # Runner.print_colored(len(outputs[0]))
        for t in range(test) :
            for x in range(person) :
                for j in range(x + 1, person) :
                    len1 = len(outputs[x][t])
                    len2 = len(outputs[j][t])
                    lens = min(len1, len2)

                    asm_source = []
                    ori_source = []
                    hex_source = []
                    try:
                        with open(os.path.join(self.__test_dir, self.__asm_dir, f"{files[t]}.asm"), "r", encoding="utf-8") as _asm:
                            ori_source = _asm.readlines()
                    except UnicodeDecodeError :
                        with open(os.path.join(self.__test_dir, self.__asm_dir, f"{files[t]}.asm"), "r", encoding="GB2312") as _asm:
                            ori_source = _asm.readlines()
                    
                    asm_source = [asm for asm in ori_source if asm.strip() != ""]
                    asm_source = [src for src in asm_source if src.strip()[-1] != ":"]
                    asm_source = [asm for asm in asm_source if asm.strip()[0] != "#"]
                    table = [1 if asm.strip()!="" and asm.strip()[-1]!=":" and asm.strip()[0]!="#" else 0 for asm in ori_source]

                    with open(os.path.join(self.__test_dir, "hex", f"{files[t]}.txt"), "r", encoding="utf-8") as _hex:
                        hex_source = _hex.readlines()
                    for i in range(lens) :
                        if outputs[x][t][i] != outputs[j][t][i] :
                            flag = False
                            x_pc = outputs[x][t][i].split(" ")[0].strip("@:")
                            x_pc = int(x_pc, 16) - int("3000", 16)
                            x_dist = x_pc >> 2
                            j_pc = outputs[j][t][i].split(" ")[0].strip("@:")
                            j_pc = int(j_pc, 16) - int("3000", 16)
                            j_dist = j_pc >> 2
                            # os.path.join(self.__test_dir, "dif", files[t], f"{circ_files[x]}-{circ_files[j]}-dif.txt")
                            with open(os.path.join(self.__test_dir, "dif", files[t], f"{circ_files[x]}-{circ_files[j]}-dif.log"), "w", encoding="utf-8") as dif :
                                dif.write(f"First dif in line {i + 1}\n")
                                dif.write(f"------the first different Mips code-----\n")
                                ind = get_index(table, x_dist+1)
                                dif.write(f"{circ_files[x]} execute: \"{asm_source[x_dist].strip()}\" in line {ind+1}\n")
                                dif.write(f"{circ_files[x]}: \"{outputs[x][t][i].strip()}\"\n")
                                ind = get_index(table, j_dist+1)
                                dif.write(f"{circ_files[j]} execute: \"{asm_source[j_dist].strip()}\" in line {ind+1}\n")
                                dif.write(f"{circ_files[j]}: \"{outputs[j][t][i].strip()}\"\n")
                                dif.write(f"---------------------------------------\n")
                                if i >= 1 :
                                    pc = outputs[x][t][i-1].split(" ")[0].strip("@:")
                                    pc = int(pc, 16) - int("3000", 16)
                                    dist = pc >> 2
                                    ind = get_index(table, dist+1)
                                    dif.write(f"the most recent same Mipc code is: \"{asm_source[dist].strip()}\" in line {ind+1}\n")
                                    dif.write(f"the most recent same Mips code output is: \"{outputs[x][t][i - 1].strip()}\"\n\n")

                            if files[t] not in wrong :
                                wrong.append(files[t])
                            break
                    if len1 != len2 :
                        with open(os.path.join(self.__test_dir, "dif", files[t], f"{circ_files[x]}-{circ_files[j]}-dif.log"), "a", encoding="utf-8") as dif :
                            dif.write(f"Error: lines don't equal!!!!,Please see\n\"{circ_files[x]}-out.txt\"\n\"{circ_files[j]}-out.txt\"")
                        flag = False
                        if files[t] not in wrong :
                            wrong.append(files[t])
        return flag, wrong

    def __remake(self, wrong_files) :
        for wrong_file in wrong_files:
            new_dir = os.path.join(self.__test_dir, wrong_file)
            Runner.safe_makedirs(new_dir)
            Runner.safe_copy(os.path.join(self.__test_dir, self.__asm_dir, f"{wrong_file}.asm"), os.path.join(new_dir, "code.asm"))
            Runner.safe_copy(os.path.join(self.__test_dir, "hex", f"{wrong_file}.txt"), os.path.join(new_dir, "code.txt"))
            if os.path.exists(os.path.join(self.__test_dir, "tbs", f"{wrong_file}_tb.v")):
                Runner.safe_copy(os.path.join(self.__test_dir, "tbs", f"{wrong_file}_tb.v"), os.path.join(new_dir, "mips_tb.v"))

            if self.__config.src == "withMars":
                cpu_files, useless = Runner.find_files(os.path.join(self.__test_dir, "dif"), wrong_file)
                for cpu_file in cpu_files:
                    cpu_name = cpu_file.split(os.sep)[-2]
                    Runner.safe_makedirs(os.path.join(new_dir, cpu_name))
                    Runner.safe_copy(cpu_file, os.path.join(new_dir, cpu_name, "dif.log"))
                    Runner.safe_copy(os.path.join(self.__test_dir, "stdout", f"{wrong_file}.txt"), os.path.join(new_dir, cpu_name, "stdout.txt"))
                    Runner.safe_copy(os.path.join(self.__test_dir, "log", cpu_name, f"{wrong_file}-{cpu_name}-out.txt"), os.path.join(new_dir, cpu_name, "out.txt"))

            else:
                cpu_difs, usless = Runner.find_files(os.path.join(self.__test_dir, "dif", wrong_file))
                for cpu_dif in cpu_difs:
                    cpu_dif_name = os.path.basename(cpu_dif)
                    dir_name = cpu_dif_name.replace("-dif.log", "")
                    cpu1 = dir_name.split('-')[0]
                    cpu2 = dir_name.split('-')[1]
                    Runner.safe_makedirs(os.path.join(new_dir, dir_name))
                    Runner.safe_copy(cpu_dif, os.path.join(new_dir, dir_name, "dif.log"))
                    Runner.safe_copy(os.path.join(self.__test_dir, "log", cpu1, f"{wrong_file}-{cpu1}-out.txt"), os.path.join(new_dir, dir_name, f"{cpu1}-out.txt"))
                    Runner.safe_copy(os.path.join(self.__test_dir, "log", cpu2, f"{wrong_file}-{cpu2}-out.txt"), os.path.join(new_dir, dir_name, f"{cpu2}-out.txt"))

        Runner.safe_rmtree(os.path.join(self.__test_dir, "hex"))
        Runner.safe_rmtree(os.path.join(self.__test_dir, "stdout"))
        Runner.safe_rmtree(os.path.join(self.__test_dir, "log"))
        Runner.safe_rmtree(os.path.join(self.__test_dir, "tbs"))
        Runner.safe_rmtree(os.path.join(self.__test_dir, "dif"))
        Runner.safe_rmtree(os.path.join(self.__test_dir, self.__asm_dir))

    def __judge(self) :
        flag = True
        wrong = []
        # os.system(f"mkdir -p {test_dir}/dif")
        Runner.safe_makedirs(os.path.join(self.__test_dir, "dif"), exist_ok=True)
        more, circ_files = Runner.find_dirs(os.path.join(self.__test_dir, "log"))

        if self.__config.src == "withMars" :
            for circ in circ_files :
                Runner.safe_makedirs(os.path.join(self.__test_dir, "dif", circ), exist_ok=True)
            stdouts_files, more = Runner.find_files(os.path.join(self.__test_dir, "stdout"))
            expected_hex, _ = Runner.find_files(os.path.join(self.__test_dir, "hex"))
            expected_names = set([os.path.basename(x) for x in expected_hex])
            got_names = set([os.path.basename(x) for x in stdouts_files])
            missing = sorted(list(expected_names - got_names))
            wrong_files = []
            for miss in missing:
                flag = False
                if miss not in wrong_files:
                    wrong_files.append(miss)
            for stdout_file in stdouts_files :
                stdouts = []
                with open(stdout_file, "r", encoding="utf-8") as std_file :
                    stdouts = std_file.readlines()
                if stdouts == []:
                    flag = False
                    if os.path.basename(stdout_file) not in wrong_files:
                        wrong_files.append(os.path.basename(stdout_file))
                    continue

                for root, dirs, files in os.walk(os.path.join(self.__test_dir, "log")) :
                    for file in files :
                        if os.path.basename(stdout_file).replace(".txt", "") == file.split("-")[0] :
                            the_flag, name = self.__compare_mars(file, stdouts)
                            if not the_flag and name not in wrong :
                                wrong.append(name)
                            if not the_flag and os.path.basename(stdout_file) not in wrong_files :
                                wrong_files.append(os.path.basename(stdout_file))
                            flag = flag and the_flag
        else :
            outputs = []
            files = []
            more, files = Runner.find_files(os.path.join(self.__test_dir, "hex"))
            files = [file.replace(".txt", "") for file in files]

            for circ in circ_files :
                lens = len(files)
                output = []
                for i in range(lens) :
                    # os.system(f"mkdir -p {test_dir}/dif/{files[i]}")
                    Runner.safe_makedirs(os.path.join(self.__test_dir, "dif", files[i]), exist_ok=True)
                    with open(os.path.join(self.__test_dir, "log", circ, f"{files[i]}-{circ}-out.txt"), "r", encoding="utf-8") as out :
                        output.append(out.readlines())
                    # Runner.print_colored(files)
                outputs.append(output)
            # Runner.print_colored(circ_files)
            flag, wrong = self.__compare_others(outputs, files)
            wrong_files = [wr + ".txt" for wr in wrong ]
        self.__delete(flag, wrong, circ_files, wrong_files)
        wrong_files = [wr.replace(".txt", "") for wr in wrong_files]
        self.__remake(wrong_files)    


if __name__ == "__main__":
    test = Machine()
    test.create_test()
    test.start_test()
