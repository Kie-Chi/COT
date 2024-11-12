import json
import os
from pathlib import Path
import shutil
from Runner import LogisimRunner, XilinxRunner, Runner
import Runner
from Generator import *
from FlowDataMaker import DataMaker
import time

class Machine :
    def __init__(self) :
        self.__test_dir = "2024-11-07-16-45-53-withMars-selfTest"
        self.__type = None
        self.__flow = True
        
        self.__cpu_dir = None
        self.__cir_dir = None
        self.__verilog_dir = None
        self.__asm_dir = ""

        self.__branch_time = 0
        self.__jump_time = 0
        self.__test_times = 0
        
        self.__xilinx_path = None
        self.__logisim_path = None
        self.__mars_path = None

        self.__read_config()
        
        self.__src = ""
        self.__mtd = ""
        self.__runner = None

    def __read_config(self) :

        config = []
        for root, dirs, files in os.walk("configs") :
            for file in files :
                if file.endswith(".json") :
                    config.append(os.path.join(root, file))
        file_config = {}
        if config :
            with open(config[0], "r", encoding="utf-8") as file :
                file_config:dict = json.load(file)
                self.__type = file_config["type"]
                self.__xilinx_path = file_config["xilinx_path"]
                self.__logisim_path = file_config["logisim_path"]
                self.__mars_path = file_config["mars_path"]
                self.__cir_dir = file_config["circ_dir"]
                self.__verilog_dir = file_config["verilog_dir"]
                self.__test_times = file_config["test_times"]
            
    
    def __create_runner(self) :
        if self.__type == "logisim" :
            self.__runner = LogisimRunner(self.__logisim_path, self.__mars_path, self.__test_dir)
            self.__cpu_dir = self.__cir_dir
        elif self.__type == "verilog" :
            self.__runner = XilinxRunner(self.__xilinx_path, self.__mars_path, self.__verilog_dir, self.__test_dir, self.__flow)
            self.__cpu_dir = self.__verilog_dir
    def create_test(self) :
        print("Welcome to co_test_builder")
        print("Several options about source as follow")
        print("1: with Mars")
        print("2: with others")
        src_slt = int(input("the source you want is:"))
        print("Several options about method as follow")
        print("1: unit test")
        print("2: random test")
        print("3: self test")
        mtd_slt = int(input("the method you want is:"))
        
        if src_slt == 1 :
            self.__src = "withMars"
        else :
            self.__src = "withOthers"
        
        if mtd_slt == 1 :
            self.__mtd = "unitTest"
        elif mtd_slt == 2 :
            self.__mtd = "randomTest"
        else :
            self.__mtd = "selfTest"
        self.__create_testdir()
        self.__create_runner()
        self.__gen_data()

    def start_test(self) :
        flag = True
        self.__get_std_mars()
        if self.__type == "logisim" :
            self.__run_logisim()
        elif self.__type == "verilog" :
            flag = self.__run_xilinx()
        if flag:
            self.__judge()

    def __create_testdir(self) :
        current_timestamp = time.time()
        local_time = time.localtime()
        formatted_time = time.strftime("%Y-%m-%d-%H-%M-%S", local_time)
        self.__test_dir = f"{formatted_time}-{self.__src}-{self.__mtd}"
        # os.system(f"mkdir -p {test_dir}")
        Runner.safe_makedirs(self.__test_dir, exist_ok=True)

    def __gen_data(self) :
        data = []
        level = 0
        times = 0
        if self.__type == "logisim" :
            level = 1
        elif self.__type == "verilog" :
            level = 2

        if self.__type == "logisim" :
            times = 880
        elif self.__type == "verilog" :
            times = 3600


        if self.__mtd == "unitTest" :
            unit_test(self.__test_dir, times, self.__branch_time, self.__jump_time, level=level)
            self.__asm_dir = "unit"
        else :
            self.__asm_dir = "random"
            # os.system(f"mkdir -p {test_dir}/random")
            # Runner.safe_makedirs(f"{test_dir}/random", exist_ok=True)
            Runner.safe_makedirs(os.path.join(self.__test_dir, "random"), exist_ok=True)
            x = np.random.randint(self.__test_times - 3, self.__test_times)
            if self.__mtd == "randomTest" :
                if self.__flow == True :
                    for i in range(x) :
                        with open(os.path.join(self.__test_dir, "random", f"random_{i}.asm"), "w", encoding="utf-8") as file :
                            file.writelines(DataMaker().random_test(4000))
                else :
                    for i in range(x) :
                        with open(os.path.join(self.__test_dir, "random", f"random_{i}.asm"), "w", encoding="utf-8") as file :
                            file.writelines(random_test(list(range(32)), times, self.__branch_time, self.__jump_time, level=level))
            else :
                for i in range(x) :
                    command = [
                        "echo",
                        os.path.join(self.__test_dir, "random", f"random_{i}.asm"),
                        "|",
                        "util\\testcode.exe"
                    ]
                    command = " ".join(command)
                    Runner.safe_execute(command, "test.txt")
                    Runner.safe_remove("test.txt")

    def __get_std_mars(self) :
        # if src_slt == "withMars" :
        src = []
        if self.__mtd == "unitTest" :
            src,more = Runner.find_files(os.path.join(self.__test_dir, "unit"))
        else :
            src,more = Runner.find_files(os.path.join(self.__test_dir, "random"))

        hex_dst = os.path.join(self.__test_dir, "hex")
        out_log = os.path.join(self.__test_dir, "stdout")
        if self.__src == "withMars" :
            self.__runner.run_mars(src, hex_dst, out_log)
        else :
            self.__runner.dump_hex(src, hex_dst)
        Runner.safe_remove(os.path.join(self.__test_dir, "info.txt"))

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
        # print(to_load)
        self.__runner.load_logisim(mips_test, *to_load) 

        for i in range(lens) :
            name = circ_file[1][i]
            # os.system(f"rm {test_dir}/circ/{name}")
            os.remove(os.path.join(self.__test_dir, "circ", name))

    def __run_all_circ(self) :
        more, circ_file = Runner.find_dirs(os.path.join(self.__test_dir, "circ"))
        # print(circ_file)
        self.__runner.run_logisim(*circ_file)
        Runner.safe_rmtree(self.__test_dir, "circ")

    def __delete(self, flag, wrong, circ_files) :
        if flag :
            # os.system(f"rm -rf {test_dir}")
            Runner.safe_rmtree(self.__test_dir)
            print()
            print("-------------------------")
            print()
            print("All Right!!!!")               
            print()
            print("-------------------------")
            print()
        else :
            print()
            print("--------------------------")
            print()
            print("Something is wrong about",*(sorted(wrong)))
            print()
            print("--------------------------")
            print()
            for circ in circ_files :
                if circ not in wrong :
                    # os.system(f"rm -rf {test_dir}/circ/{circ}")
                    # os.system(f"rm -rf {test_dir}/log/{circ}")
                    # os.system(f"rm -rf {test_dir}/dif/{circ}")
                    if self.__src == "withMars" :
                        Runner.safe_rmtree(os.path.join(self.__test_dir, "log", circ))
                    Runner.safe_rmtree(os.path.join(self.__test_dir, "dif", circ))
            # Runner.safe_rmtree(os.path.join(self.__test_dir, self.__cpu_dir))

    def __compare_mars(self, file, stdouts) :
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
        with open(os.path.join(self.__test_dir, self.__asm_dir, f"{mips_test}.asm"), "r", encoding="utf-8") as _asm:
            ori_source = _asm.readlines()
        asm_source = [src for src in ori_source if ":\n" not in src]

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
                    dif.write(f"Mips Code : \"{asm_source[dist].strip()}\" in line {ori_source.index(asm_source[dist]) + 1}\n")
                    dif.write(f"Mars: \"{stdouts[i].strip()}\"\n")
                    dif.write(f"{name}: \"{outputs[i].strip()}\"\n")
                    dif.write(f"---------------------------------------\n")
                    if i >= 1 :
                        pc = stdouts[i-1].split(" ")[0].strip("@:")
                        pc = int(pc, 16) - int("3000", 16)
                        dist = pc >> 2
                        dif.write(f"the most recent same Mips code is \"{asm_source[dist].strip()}\" in line {ori_source.index(asm_source[dist]) + 1}\n")
                        dif.write(f"the most recent same Mips code output is: \"{outputs[i - 1].strip()}\"\n\n")
                break
        if len1 != len2 :
            with open(os.path.join(self.__test_dir, "dif", name, f"{mips_test}-std-dif.log"), "a", encoding="utf-8") as dif :
                dif.write(f"lines don't equal!!!!,please see\n\"{os.path.join('log', name, f'{mips_test}.txt')}\"\n\"{os.path.join('stdout', f'{mips_test}.txt')}\"")
            flag = False
            
        return flag, name

    def __compare_others(self, outputs, files) :
        flag = True
        wrong = []
        more, circ_files = Runner.find_dirs(os.path.join(self.__test_dir, "log"))
        person = len(outputs)
        test = len(files)
        # print(test)
        # print(files)
        # print(person)
        # print(len(outputs))
        # print(len(outputs[0]))
        for t in range(test) :
            for x in range(person) :
                for j in range(x + 1, person) :
                    len1 = len(outputs[x][t])
                    len2 = len(outputs[j][t])
                    lens = min(len1, len2)

                    asm_source = []
                    ori_source = []
                    hex_source = []
                    with open(os.path.join(self.__test_dir, self.__asm_dir, f"{files[t]}.asm"), "r", encoding="utf-8") as _asm:
                        ori_source = _asm.readlines()
                    asm_source = [src for src in ori_source if ":\n" not in src]

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
                                dif.write(f"{circ_files[x]} execute \"{asm_source[x_dist].strip()}\" in line {ori_source.index(asm_source[x_dist]) + 1}\n")
                                dif.write(f"{circ_files[x]}: \"{outputs[x][t][i].strip()}\"\n")
                                dif.write(f"{circ_files[j]} execute \"{asm_source[j_dist].strip()}\" in line {ori_source.index(asm_source[j_dist]) + 1}\n")
                                dif.write(f"{circ_files[j]}: \"{outputs[j][t][i].strip()}\"\n")
                                dif.write(f"---------------------------------------\n")
                                if i >= 1 :
                                    pc = outputs[x][t][i-1].split(" ")[0].strip("@:")
                                    pc = int(pc, 16) - int("3000", 16)
                                    dist = pc >> 2
                                    dif.write(f"the most recent same Mipc code is: \"{asm_source[dist].strip()}\" in line {ori_source.index(asm_source[dist]) + 1}\n")
                                    dif.write(f"the most recent same Mips code output is: \"{outputs[x][t][i - 1].strip()}\"\n\n")

                            if files[t] not in wrong :
                                wrong.append(files[t])
                            break
                    if len1 != len2 :
                        with open(os.path.join(self.__test_dir, "dif", files[t], f"{circ_files[x]}-{circ_files[j]}-dif.log"), "a", encoding="utf-8") as dif :
                            dif.write(f"lines don't equal!!!!,please see\n\"{os.path.join('log', circ_files[x], f'{files[t]}.txt')}\"\n\"{os.path.join('log', circ_files[j], f'{files[t]}.txt')}\"")
                        flag = False
                        if files[t] not in wrong :
                            wrong.append(files[t])
        return flag, wrong

    def __judge(self) :
        flag = True
        wrong = []
        # os.system(f"mkdir -p {test_dir}/dif")
        Runner.safe_makedirs(os.path.join(self.__test_dir, "dif"), exist_ok=True)
        more, circ_files = Runner.find_dirs(os.path.join(self.__test_dir, "log"))

        if self.__src == "withMars" :
            for circ in circ_files :
                # os.system(f"mkdir -p {test_dir}/dif/{circ}")
                Runner.safe_makedirs(os.path.join(self.__test_dir, "dif", circ), exist_ok=True)
            stdouts_files, more = Runner.find_files(os.path.join(self.__test_dir, "stdout"))
            for stdout_file in stdouts_files :
                stdouts = []
                with open(stdout_file, "r", encoding="utf-8") as std_file :
                    stdouts = std_file.readlines()

                for root, dirs, files in os.walk(os.path.join(self.__test_dir, "log")) :
                    for file in files :
                        if os.path.basename(stdout_file).replace(".txt", "") == file.split("-")[0] :
                            the_flag, name = self.__compare_mars(file, stdouts)
                            if not the_flag and name not in wrong :
                                wrong.append(name)
                            flag = flag and the_flag
            self.__delete(flag, wrong, circ_files)
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
                    # print(files)
                outputs.append(output)
            # print(circ_files)
            flag, wrong = self.__compare_others(outputs, files)
            self.__delete(flag, wrong, files)
            


if __name__ == "__main__":
    test = Machine()
    test.create_test()
    test.start_test()
