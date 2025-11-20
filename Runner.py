import os
import re
import sys
import time
import shutil
import subprocess
import threading
from functools import wraps

class Runner :
    def __init__(self, path: str, mars:str, the_dir: str, isFlow: bool, Except: bool) :
        self._path = path
        self._dir = the_dir
        self._mars = mars
        self._is_flow = isFlow
        self._is_except = Except
        
    def dump_hex(self, src, hex_dst) :
        os.makedirs(hex_dst, exist_ok=True)
        print_colored()
        print_colored("Mars: ", 34, end="")
        print_colored("Start dumping datas...")
        for code in src :
            # flag, test = self.__find_endless(code)
            hex_txt = os.path.join(hex_dst, f"{os.path.basename(code).replace('.asm', '.txt')}")
            mips = [
                "java",
                "-jar",
                os.path.join("..", self._mars),
                "mc",
                "LargeText",
                "a",
                "dump",
                ".text",
                "HexText",
                hex_txt.replace(self._dir+os.sep, ""),
                code.replace(self._dir+os.sep, ""),
                # ">",
                # os.path.join(self._dir ,"info.txt")
            ]
            # mips = [
            #     "java",
            #     "-jar",
            #     self._mars,
            #     "mc",
            #     "CompactLargeText",
            #     "a",
            #     "dump",
            #     ".text",
            #     "HexText",
            #     hex_txt,
            #     code,
            #     # ">",
            #     # os.path.join(self._dir ,"info.txt")
            # ]
            mips = " ".join(mips)

            # print_colored()
            print_colored(f"{os.path.basename(code)}: ", 35, end="")
            print_colored("Mars is dumping data...", 37)
            # os.system(mips)
            safe_execute(mips, os.path.join(self._dir, "info.txt"), cwd=self._dir)
            contents = safe_read(os.path.join(self._dir, "info.txt"))
            contents = [content for content in contents if "Error" in content]
            if contents != []:
                for content in contents:
                    print_colored(content)
                raise Exception
            contents = safe_read(hex_txt)
            lens = len(contents)
            extra = ["00000000\n" for _ in range(4094 - lens)]
            extra.append("1000ffff\n")
            extra.append("00000000\n")
            contents.extend(extra)
            safe_write(hex_txt, contents)
        print_colored("Mars: ", 34, end="")
        print_colored("All dumped!!!")

    def _run_asm(self, src, out_log) :
        os.makedirs(out_log, exist_ok=True)
        print_colored()
        print_colored("Mars: ", 34, end="")
        print_colored("Start executing asm...")
        for code in src :
            log_txt = os.path.join(out_log, f"{os.path.basename(code).replace('.asm', '.txt')}")
            # ext = [
            #     "java",
            #     "-jar",
            #     self._mars,
            #     "mc",
            #     "CompactLargeText",
            #     "ig",
            #     "coL1",
            #     code,
            #     # ">",
            #     # log_txt
            # ]
            ext = [
                "java",
                "-jar",
                self._mars,
                "mc",
                "LargeText",
                "40000",
                "lg",
                code,
                # ">",
                # log_txt
            ]
            if self._is_flow :
                ext.insert(3, "db")
            if self._is_except :
                ext.insert(3, "ex")
            print_colored(f"{os.path.basename(code)}: ", 35, end="")
            print_colored("Mars executing asm...", 37)
            # os.system(ext)
            safe_execute(ext, log_txt)
            contents = ""
            with open(log_txt, "r", encoding="utf-8") as file :
                contents = file.readlines()
            flag = False
            if "Program terminated when maximum step limit 40000 reached.\n" in contents:
                if len(contents) > 20000:
                    flag = True
            
            if not flag:
                contents = [content for content in contents if "@" in content]
                contents = [content for content in contents if "$ 0" not in content]
                with open(log_txt, "w", encoding="utf-8") as file :
                    file.writelines(contents)
            else:
                safe_remove(code)
                safe_remove(log_txt)
                safe_remove(log_txt.replace("stdout", "hex"))
            # print_colored(contents)
            # print_colored(f"{os.path.basename(code)} :Executed!")
        print_colored("Mars: ", 34, end="")
        print_colored("All executed!!!")


    def run_mars(self, src, hex_dst, out_log) :
        self.dump_hex(src, hex_dst)    
        self._run_asm(src, out_log)

class LogisimRunner(Runner) :
    def __init__(self, path, mars, the_dir, isFlow, Except) -> None: 
        super(LogisimRunner, self).__init__(path, mars, the_dir, isFlow, Except)
        

    def __read_data(self, path) :
        name = os.path.basename(path).replace(".txt", "")
        data = []
        with open(path, "r", encoding="utf-8") as data_file :
            contents = [content.strip() for content in data_file.readlines()]
        i = 0
        while i < len(contents) :
                content = contents[i: i + 8]
                data_str = " ".join(content)
                data_str += '\n'
                data.append(data_str)
                i += 8
        data = "".join(data)
        return data, name

    def __sub_rom(self, path, data, mips_name) :
        cpu_name = os.path.basename(path).replace(".circ", "")
        # os.system(f"mkdir -p {test_dir}/circ/{cpu_name}")
        os.makedirs(os.path.join(self._dir, "circ", cpu_name), exist_ok=True)
        with open(path, "r", encoding="utf-8") as cpu_file :
            contents = cpu_file.readlines()
        # print_colored(contents)
        contents = "".join(contents)
        # print_colored(contents)
        # print_colored(data)
        front = re.findall(r'<comp lib="4" loc="\(\d+,\d+\)" name="ROM">.*?<a name="contents">.*?\n', contents, re.DOTALL)[0]
        end = re.findall(r'<comp lib="4" loc="\(\d+,\d+\)" name="ROM">.*?<a name="contents">.*?\n.*?(</a>.*?</comp>)', contents, re.DOTALL)[0]
        # print_colored(re.findall(r'<comp lib="4" loc="\(\d+,\d+\)" name="ROM">.*?<a name="contents">.*?\n(.*?)</comp>', contents, re.DOTALL))
        rom = re.sub(r'<comp lib="4" loc="\(\d+,\d+\)" name="ROM">.*?<a name="contents">.*?\n(.*?)</comp>',front + data + end, contents, flags = re.DOTALL)
        rom = re.sub(r'<main name=".*?"/>',   '<main name="main"/>', rom)
        rom = re.sub(r'<circuit name="main">', '<circuit name="test">', rom)
        rom = re.sub(r'<a name="circuit" val="main"/>', '<a name="circuit" val="test"/>', rom)
        # print_colored(rom)
        with open(os.path.join(self._dir, "circ", cpu_name, f"{mips_name}-{cpu_name}.circ"), "w", encoding="utf-8") as loaded_file :
            loaded_file.write(rom)


    def load_logisim(self, mips_test, *args) :
        """
            mips_test: 传入的ROM数据\n
            args: 批量导入不同的.circ文件中
        """
        for mips in mips_test :
            data, mips_name = self.__read_data(mips)
            # print_colored(args)
            for cpu in args :
                # print_colored(cpu)
                self.__sub_rom(cpu, data, mips_name)
                
    
    def __add_main(self, path, main) :
        origin = []
        with open(path, "r", encoding="utf-8") as load_file :
            origin = load_file.read()
        change = re.sub(r'</project>', main + "\n</project>", origin)

        with open(path, "w", encoding="utf-8") as change_file :
            change_file.write(change)
    
    def __get_raw_logs(self, path, out_log) :
        log_txt = os.path.join(out_log, f"{os.path.basename(path).replace('.circ', '-out.txt')}")
    
        logisim = [
            "java",
            "-jar",
            self._path,
            path,
            "-tty",
            "table",
            "speed",
            "1GHz"
            # ">",
            # log_txt
        ]
        logisim = " ".join(logisim)
    
        # os.system(logisim)
        safe_execute(logisim, log_txt)
    
        logs = ""
        with open(log_txt, "r", encoding="utf-8") as log :
            logs = log.readlines()
        return logs, log_txt
    
    def __trans_to_spj(self, logs, log_txt) :
        spj = []
        for log in logs :
            log = log.strip()
            # print_colored(log)
            log = log.split("\t")
            instr = int("".join(log[0].split(" ")), 2)
            pc = int("".join(log[1].split(" ")), 2)
            reg_we = int("".join(log[2].split(" ")), 2)
            reg = int("".join(log[3].split(" ")), 2)
            reg_data = int("".join(log[4].split(" ")), 2)
            mem_we = int("".join(log[5].split(" ")), 2)
            mem = int("".join(log[6].split(" ")), 2)
            mem_data = int("".join(log[7].split(" ")), 2)
            # print_colored(instr)
            # print_colored(pc)
            # print_colored(reg_we)
            # print_colored(reg)
            # print_colored(reg_data)
            # print_colored(mem_we)
            # print_colored(mem_data)
            if reg_we and reg != 0 :
                spj_str = f"@{pc:08x}: ${reg:2d} <= {reg_data:08x}\n"
                # print_colored(spj_str)
                spj.append(spj_str)
            elif mem_we :
                spj_str = f"@{pc:08x}: *{mem:08x} <= {mem_data:08x}\n"
                # print_colored(spj_str)
                spj.append(spj_str)
        with open(log_txt, "w", encoding="utf-8") as file :
            file.writelines(spj)
            
    def run_logisim(self, *args) :
        content = ""
        with open(os.path.join("util","test_main.txt"), "r", encoding="utf-8") as main_file :
            content = "".join(main_file.readlines())
        # print_colored(content)

        for cpu in args :
            cpu_files, more = find_files(cpu, ".circ")

            out_log = os.path.join(self._dir, "log", os.path.basename(cpu))
            # os.system(f"mkdir -p {out_log}")
            os.makedirs(out_log, exist_ok=True)
            print_colored()
            print_colored(f"{os.path.basename(cpu)}: ", 34, end="")
            print_colored("Running logisim...")
            for cpu_file in cpu_files :
                self.__add_main(cpu_file, content)    
                print_colored(f"{os.path.basename(cpu_file).replace('.circ', '').split('-')[-1]}: ", 35, end="")
                print_colored(f"Executing {os.path.basename(cpu_file).replace('.circ', '').split('-')[0]}...", 37)
                logs, log_txt = self.__get_raw_logs(cpu_file, out_log)
                self.__trans_to_spj(logs, log_txt)
            print_colored(f"{os.path.basename(cpu)}: ", 34, end="")
            print_colored("All Executed!!!")
class XilinxRunner(Runner) :
    def __init__(self, path, mars, cpu_path, the_dir, isFlow, Except, tb, asm_dir) :
        super(XilinxRunner, self).__init__(path, mars, the_dir, isFlow, Except)
        self.__tb = tb
        self.__cpu_path = cpu_path
        self.__cpu_in_dir = os.path.basename(cpu_path)
        self.__cpus = None
        if os.path.exists(os.path.join(self._path, "bin", "nt64")):
            self.__funct_path = os.path.join(self._path, "bin", "nt64")
            self.__fuse_path = os.path.join(self.__funct_path, "fuse.exe")
        else:
            self.__funct_path = os.path.join(self._path, "bin", "lin64")
            self.__fuse_path = os.path.join(self.__funct_path, "fuse")
        self._asm_dir = asm_dir

    def fuse(self):
        mips_cpus = find_file_with_depth(self.__cpu_path, "mips.v", 4)
        cpus = []
        cpus_path = []
        for mips in mips_cpus:
            if os.path.dirname(mips) not in cpus:
                cpus.append(self.__cpu_in_dir + os.path.dirname(mips).replace(self.__cpu_path, "").replace(os.sep, "@"))
                cpus_path.append(os.path.dirname(mips))
        print_colored()
        print_colored("ISE: ", 34, end="")
        print_colored("Start fusing...")
        ind = -1
        self.__cpus = cpus
        for cpu in cpus:
            ind += 1
            print_colored(f"{cpu}: ", 35, end="")
            print_colored("Start creating .prj and .tcl...", 37)
            safe_makedirs(os.path.join(self._dir, self.__cpu_in_dir, cpu, "source"))
            ori_cpu_files = []
            for root, dirs, files in os.walk(cpus_path[ind]):
                for file in files:
                    if file.endswith(".v"):
                        ori_cpu_files.append(os.path.join(root, file))
                del dirs[:]

            has_tb = False
            for file in ori_cpu_files:
                name = os.path.basename(file)
                if name == "mips_tb.v":
                    has_tb = True
                safe_copy(file, os.path.join(self._dir, self.__cpu_in_dir, cpu, "source", name))
                
            if self.__tb != 0:
                safe_copy(os.path.join("util",f"mips_tb_{self.__tb}.v"), os.path.join(self._dir, self.__cpu_in_dir, cpu, "source", "mips_tb.v"))

            if not has_tb:
                ori_cpu_files.append(os.path.join(self.__cpu_in_dir, "mips_tb.v"))
            print_colored(f"{cpu}: ", 35, end="")
            print_colored("Start fusing...", 37)
            wrong = self.__fuse_ext(cpu, ori_cpu_files)
            if not wrong:
                return False
        print_colored("ISE: ", 34, end="")
        print_colored("All Executed!!!")
        return True

    def __fuse_ext(self, cpu, ori_cpu_files):
        prj_path = os.path.join(self._dir, self.__cpu_in_dir, cpu, "mips.prj")
        tcl_path = os.path.join(self._dir, self.__cpu_in_dir, cpu, "mips.tcl")
        with open(prj_path, "w", encoding="utf-8") as prj:
            for file in ori_cpu_files:
                name = os.path.basename(file)
                prj.write('verilog work \"' + os.path.join("source", name) + "\"\n")

        with open(tcl_path, "w", encoding="utf-8") as tcl:
            tcl.write("run 300us;\nexit")

        useless, names = find_files(os.path.join(self._dir, self._asm_dir))
        flag = False
        if not os.path.exists(os.path.join(self._dir, "tbs")):
            flag = True
        else:
            for name in names:
                if not os.path.exists(os.path.join(self._dir, "tbs", name.replace(".asm", "_tb.v"))):
                    flag = True
                    break

        if flag :
            self.__re_fuse(cpu)
            # print_colored(f"{cpu}: Fuse end!!!")
        return True
    
    def __re_fuse(self, cpu):
        fuse = [
            self.__fuse_path,
            "-nodebug",
            "-prj",
            "mips.prj",
            "-o",
            "mips.exe",
            "mips_tb"
        ]
        fuse = " ".join(fuse)
        safe_execute(fuse, os.path.join(self._dir, self.__cpu_in_dir, cpu, "fuse_info.txt"), cwd=os.path.join(self._dir, self.__cpu_in_dir, cpu))
        path = os.path.join(self._dir, self.__cpu_in_dir, cpu, "mips.exe")
        if not os.path.exists(path):
            print_colored("ERROR: There is something wrong when fusing", 31)
            errors = []
            with open(os.path.join(self._dir, self.__cpu_in_dir, cpu, "fuse.log"), "r", encoding="utf-8") as fse:
                errors = fse.readlines()
            errors = [error for error in errors if "ERROR" in error]
            for error in errors:
                print_colored(error.strip(), 31)
            return False

        safe_remove(os.path.join(self._dir, self.__cpu_in_dir, cpu, "fuse_info.txt"))
        safe_remove(os.path.join(self._dir, self.__cpu_in_dir, cpu, "fuse.log"))
        safe_remove(os.path.join(self._dir, self.__cpu_in_dir, cpu, "fuse.xmsgs"))
        safe_remove(os.path.join(self._dir, self.__cpu_in_dir, cpu, "fuseRelaunch.cmd"))

    def __isim_ext(self, cpu):
        if os.name != str("nt"):
            test = os.path.join(".", "mips.exe")
        else:
            test = "mips.exe"
        ext = [
            test,
            "-nolog",
            "-tclbatch",
            "mips.tcl",
        ]
        ext = " ".join(ext)
        # print_colored(ext)
        # os.system(ext)
        if os.name == str("nt"):
            os.environ["LD_LIBRARY_PATH"] = os.path.join(self._path, "lib", "nt64")
            os.environ["XILINX"] = self._path
        else:
            os.environ["LD_LIBRARY_PATH"] = os.path.join(self._path, "lib", "lin64")
            os.environ["XILINX"] = self._path

        safe_execute(ext, os.path.join(self._dir, self.__cpu_in_dir, cpu, "output.txt"), cwd=os.path.join(self._dir, self.__cpu_in_dir, cpu), retries=10, delay=0.1)
        # time.sleep(0.5)
        # xrunner.safe_rmtree(os.path.join(test_dir,"isim"))
        # safe_remove(os.path.join(self._dir, self.__cpu_path, cpu, "isim.wdb"))
        # safe_remove(os.path.join(self._dir, self.__cpu_path, cpu, "isim.log"))

    def __sort_no_tb(self, file):
        name = os.path.basename(file)
        name = name.replace(".txt", "")
        return os.path.exists(os.path.join(self._dir, "tbs", f"{name}_tb.v"))

    def run_isim(self):
        all_test = os.path.join(self._dir, "hex")
        tests, names = find_files(all_test)
        print_colored()
        print_colored("ISim: ", 34, end="")
        print_colored("Start stimulating...")
        for cpu in self.__cpus :
            safe_makedirs(os.path.join(self._dir, "log", cpu))
            tests.sort(key=self.__sort_no_tb)
            ind = 0
            for test in tests :
                print_colored(f"{cpu}: ", 35, end="")
                print_colored(f"Executing {os.path.basename(test).replace('.txt', '')}...", 37)
                name = os.path.basename(test).replace(".txt", "")
                safe_copy(test, os.path.join(self._dir, self.__cpu_in_dir, cpu, "code.txt"))
                if os.path.exists(os.path.join(self._dir, "tbs", f"{name}_tb.v")):
                    safe_copy(os.path.join(self._dir, "tbs", f"{name}_tb.v"), os.path.join(self._dir, self.__cpu_in_dir, cpu, "source", "mips_tb.v"))
                    self.__re_fuse(cpu)
                self.__isim_ext(cpu)
                contents = []
                with open(os.path.join(self._dir, self.__cpu_in_dir, cpu, "output.txt"), "r", encoding="utf-8") as file :
                    contents = file.readlines()
                if contents == []:
                    ind += 1
                    print_colored("WARNING: No output got", 33)
                contents = [content for content in contents if "@" in content and "$ 0" not in content]
                if self._is_flow == True :
                    contents = [(int(content.split("@")[0].strip()), 1 if "*" in content.split("@")[1] else 0, "@" + content.split("@")[1]) for content in contents]
                else :
                    contents = [(0, 0, "@" + content.split("@")[1]) for content in contents]
                filted = contents
                # for content in contents :
                #     if self._is_pcpass(content[2]) :
                #         break
                #     filted.append(content)
                if self._is_flow == True:
                    filted.sort(key=lambda x : (x[0], x[1]))
                filted = [fil[2] for fil in filted]

                with open(os.path.join(self._dir, self.__cpu_in_dir, cpu, "output.txt"), "w", encoding="utf-8") as file :
                    file.writelines(filted)
                safe_copy(os.path.join(self._dir, self.__cpu_in_dir, cpu, "output.txt"), os.path.join(self._dir, "log", cpu, f"{name}-{cpu}-out.txt"))
                # print_colored(f"{cpu}: {os.path.basename(test)} is executed!!!")
            if ind == len(test):
                print_colored("ERROR: Something wrong with ISim, Please restart the machine or your PC")
                raise Exception
            safe_rmtree(os.path.join(self._dir, self.__cpu_in_dir, cpu), 20, 0.)
        print_colored("ISim: ", 34, end="")
        print_colored("All executed!!!")
        safe_rmtree(os.path.join(self._dir, self.__cpu_in_dir), 20, 0.3)
        
def find_files(path, key="") :
    """
        tuple[list, list]\n
        第一个返回参数：完整路径\n
        第二个返回参数：文件名
    """
    results = []
    names = []
    for root, dirs, files in os.walk(path) :
        for file in files :
            if file.endswith(key) or file.startswith(key):
                results.append(os.path.join(root, file)) 
                names.append(file)
    return results, names

def find_dirs(path, key="") :
    """
        tuple[list, list]\n
        第一个返回参数：完整路径\n
        第二个返回参数：目录名
    """
    results = []
    names = []
    for root, dirs, files in os.walk(path) :
        for _dir in dirs :
            if _dir.endswith(key) or _dir.startswith(key):
                results.append(os.path.join(root, _dir))
                names.append(_dir)
    return results, names

def find_option_with_depth(root_dir, option, max_depth=2):
    result = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 计算当前目录的深度
        depth = dirpath[len(root_dir):].count(os.sep)
        if depth > max_depth:
            del dirnames[:]  # 不递归更深的目录
            continue
        if "$RECYCLE.BIN" in dirpath :
            del dirnames[:]
            del filenames[:]
        if "bin" in dirnames :
            del dirnames[:]
            del filenames[:]

        files = [file for file in filenames if option in file]
        for file in files :
            result.append(os.path.join(dirpath, file))
    return result

def find_file_with_depth(root_dir, target_file, max_depth=2):
    result = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 计算当前目录的深度
        depth = dirpath[len(root_dir):].count(os.sep)
        if depth > max_depth:
            del dirnames[:]  # 不递归更深的目录
            continue
        if "$RECYCLE.BIN" in dirpath :
            del dirnames[:]
            del filenames[:]
        if "bin" in dirnames :
            del dirnames[:]
            del filenames[:]
        if target_file in filenames:
            result.append(os.path.join(dirpath, target_file))
    return result

def find_directory_with_depth(root_dir, target_dir, max_depth=3):
    result = []
    for root, dirs, files in os.walk(root_dir):
        depth = root[len(root_dir):].count(os.sep)
        if depth > max_depth:
            del dirs[:]  # 停止更深层的遍历
            continue
        flag = False
        if target_dir in dirs:
            flag = True
            result.append(os.path.join(root, target_dir))
        if flag :
            del dirs[:]
    return result

def find_path_with_depth(root_dir, target_path, max_depth=3):
    result = []
    for root, dirs, files in os.walk(root_dir):
        depth = root[len(root_dir):].count(os.sep)
        if depth > max_depth:
            del dirs[:]  # 停止更深的搜索
            continue

        sub_dirs = target_path.split(os.sep)
        current_dir = root
        found = True
        for sub_dir in sub_dirs:
            current_dir = os.path.join(current_dir, sub_dir)
            if not os.path.exists(current_dir):
                found = False
                break

        if found:
            result.append(current_dir)
    return result

def safe_execute(cmd, file, cwd=".", retries=5, delay=0.1) :
    for _ in range(retries) :
        try :
            with open(file, "w", encoding="utf-8") as stdout :
                subprocess.run(cmd, stdout=stdout, stderr=subprocess.STDOUT, cwd=cwd)
            return
        except (FileNotFoundError, PermissionError) :
            time.sleep(delay)
    try:
        cmd = f"{cmd} > {os.path.basename(file)}"
        # print(f"cd {cwd} && {cmd}")
        os.system(f"cd {cwd} && {cmd}")
    except :
        print_colored("ERROR: can't execute the code correctly!!!", 31)
        raise Exception
    
def safe_rmtree(path, retries=5, delay=0.1):
    if os.path.exists(path):
        for _ in range(retries):
            try:
                shutil.rmtree(path)
                return  # 成功删除后返回
            except (FileNotFoundError, PermissionError):
                time.sleep(delay)  # 等待一段时间后重试
        print_colored(f"Failed to delete {path} after {retries} attempts.", 33)

def safe_remove(path, retries=5, delay=0.1):
    if os.path.exists(path):
        for _ in range(retries):
            try:
                os.remove(path)
                return  # 成功删除后返回
            except (FileNotFoundError, PermissionError):
                time.sleep(delay)  # 等待一段时间后重试
        print_colored(f"Failed to delete {path} after {retries} attempts.", 33)

def safe_copy(src, dst, retries=5, delay=0.1) :
    for _ in range(retries) :
        try: 
            shutil.copy(src, dst)
            return
        except (FileNotFoundError, PermissionError):
            time.sleep(delay)
    print_colored(f"Failed to copy {src} to {dst} after {retries} attempts.", 33)
    
def safe_read(src, retries=5, delay=0.1) :
    contents = []
    for _ in range(retries) :
        try :
            with open(src, "r", encoding="utf-8") as file :
                contents = file.readlines()
            return contents
        except (FileNotFoundError, PermissionError):
            time.sleep(delay)

def safe_write(src, contents, retries=5, delay=0.1) :
    for _ in range(retries) :
        try :
            with open(src, "w", encoding="utf-8") as file :
                file.writelines(contents)
            return
        except (FileNotFoundError, PermissionError):
            time.sleep(delay)
def safe_makedirs(path, exist_ok=True, retries=5, delay=0.1) :
    for _ in range(retries) :
        try :
            os.makedirs(path, exist_ok=exist_ok)
            return
        except (PermissionError, OSError) :
            time.sleep(delay)
    print_colored(f"Failed to makedirs {path} after {retries} attempts.", 33)

def print_colored(text="", fg_color=97, bg_color=None, style=None, end="\n", flush=False):
    # 格式化颜色和样式
    color_code = str(fg_color)
    if bg_color:
        color_code += f";{bg_color}"
    if style:
        color_code += f";{style}"
    # 打印带颜色的文本
    print(f"\033[{color_code}m{text}\033[0m", end=end, flush=flush)

def color_str(text="", fg_color=97, bg_color=None, style=None):
    color_code = str(fg_color)
    if bg_color:
        color_code += f";{bg_color}"
    if style:
        color_code += f";{style}"
    # 打印带颜色的文本
    return f"\033[0m\033[{color_code}m{text}\033[0m\033[97m"

if __name__ == "__main__" :
    # runner = Runner("abc", "test_dr")
    # num = runner.translate("beq $31, $15, jumplabel")
    # print_colored()

    # print_colored(runner.is_pcpass("@00005004: $29 <= 0d89e43c"))
    print_colored("test")
