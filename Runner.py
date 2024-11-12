import os
import re
import time
import shutil
import subprocess
import threading
from functools import wraps

class Runner :
    def __init__(self, path: str, mars:str, the_dir: str, isFlow: bool) :
        self._path = path
        self._dir = the_dir
        self._mars = mars
        self._is_flow = isFlow
        
    def __find_endless(self, path) :
        contents = []
        with open(path, "r", encoding="utf-8") as file :
            contents = file.readlines()
        if "beq" in contents[-1] :
            if contents[-2].rstrip(":\n") in contents[-1] :
                contents = contents[-2:]
                with open(path, "w", encoding="utf-8") as file :
                    file.write(contents)
                return True, contents[-1]
            
        return False, None
    
    def __translate(self, mips: str) :
        code = mips.strip().replace("$", "").replace(",", "")
        code = code.split(" ")
        if code[0] == "beq" :
            # print(code)
            # print(f"000100{int(code[1]):05b}{int(code[2]):05b}1111111111111100")
            num = hex(int(f"100{int(code[1]):05b}{int(code[2]):05b}1111111111111100" ,2))
            return f"{int(num, base=16):08x}"
        
    def _is_pcpass(self, out) :
        pc = re.findall("@([\da-f]+):", out)[0]
        pc = int(pc, 16)
        if pc > int("6fff", 16) or pc < int("3000", 16) :
            return True
        else :
            return False
        
    def dump_hex(self, src, hex_dst) :
        os.makedirs(hex_dst, exist_ok=True)
        for code in src :
            flag, test = self.__find_endless(code)
            hex_txt = os.path.join(hex_dst, f"{os.path.basename(code).replace('.asm', '.txt')}")
            mips = [
                "java",
                "-jar",
                self._mars,
                "mc",
                "CompactLargeText",
                "ig",
                "dump",
                ".text",
                "HexText",
                hex_txt,
                code,
                # ">",
                # os.path.join(self._dir ,"info.txt")
            ]
            if self._is_flow :
                mips.insert(3, "db")
            mips = " ".join(mips)

            print()
            print(f"{os.path.basename(code)} :Mars is dumping data...")
            # os.system(mips)
            safe_execute(mips, os.path.join(self._dir, "info.txt"))
            
            print(f"{os.path.basename(code)} :Data already dumped!")
            if flag :
                with open(hex_txt, "a", encoding="utf-8") as file :
                    file.write(self.__translate(test) + "\n")
                    file.write("3c02d04c\n")

    def _run_asm(self, src, out_log) :
        os.makedirs(out_log, exist_ok=True)
        for code in src :
            log_txt = os.path.join(out_log, f"{os.path.basename(code).replace('.asm', '.txt')}")
            ext = [
                "java",
                "-jar",
                self._mars,
                "mc",
                "CompactLargeText",
                "coL1",
                "ig",
                code,
                # ">",
                # log_txt
            ]
            if self._is_flow :
                ext.insert(3, "db")
            print()
            print(f"{os.path.basename(code)} :Mars executing asm...")
            # os.system(ext)
            safe_execute(ext, log_txt)
            contents = ""
            with open(log_txt, "r", encoding="utf-8") as file :
                contents = file.readlines()
            contents = [content for content in contents if "@" in content]
            # print(contents)
            with open(log_txt, "w", encoding="utf-8") as file :
                file.writelines(contents)
            print(f"{os.path.basename(code)} :Executed!")


    def run_mars(self, src, hex_dst, out_log) :
        self.dump_hex(src, hex_dst)    
        self._run_asm(src, out_log)

class LogisimRunner(Runner) :
    def __init__(self, path, mars, the_dir, isFlow) -> None: 
        super(LogisimRunner, self).__init__(path, mars, the_dir, isFlow)
        

    def __read_data(self, path) :
        name = os.path.basename(path).replace(".txt", "")
        print()
        print(f"{name} :Loading datas.....")
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
        # print(contents)
        contents = "".join(contents)
        # print(contents)
        # print(data)
        front = re.findall(r'<comp lib="4" loc="\(\d+,\d+\)" name="ROM">.*?<a name="contents">.*?\n', contents, re.DOTALL)[0]
        end = re.findall(r'<comp lib="4" loc="\(\d+,\d+\)" name="ROM">.*?<a name="contents">.*?\n.*?(</a>.*?</comp>)', contents, re.DOTALL)[0]
        # print(re.findall(r'<comp lib="4" loc="\(\d+,\d+\)" name="ROM">.*?<a name="contents">.*?\n(.*?)</comp>', contents, re.DOTALL))
        rom = re.sub(r'<comp lib="4" loc="\(\d+,\d+\)" name="ROM">.*?<a name="contents">.*?\n(.*?)</comp>',front + data + end, contents, flags = re.DOTALL)
        rom = re.sub(r'<main name=".*?"/>',   '<main name="main"/>', rom)
        rom = re.sub(r'<circuit name="main">', '<circuit name="test">', rom)
        rom = re.sub(r'<a name="circuit" val="main"/>', '<a name="circuit" val="test"/>', rom)
        # print(rom)
        with open(os.path.join(self._dir, "circ", cpu_name, f"{mips_name}-{cpu_name}.circ"), "w", encoding="utf-8") as loaded_file :
            loaded_file.write(rom)
        print(f"{cpu_name}: {mips_name}'s datas is already loaded!")


    def load_logisim(self, mips_test, *args) :
        """
            mips_test: 传入的ROM数据\n
            args: 批量导入不同的.circ文件中
        """
        for mips in mips_test :
            data, mips_name = self.__read_data(mips)
            # print(args)
            for cpu in args :
                # print(cpu)
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
            # print(log)
            log = log.split("\t")
            instr = int("".join(log[0].split(" ")), 2)
            pc = int("".join(log[1].split(" ")), 2)
            reg_we = int("".join(log[2].split(" ")), 2)
            reg = int("".join(log[3].split(" ")), 2)
            reg_data = int("".join(log[4].split(" ")), 2)
            mem_we = int("".join(log[5].split(" ")), 2)
            mem = int("".join(log[6].split(" ")), 2)
            mem_data = int("".join(log[7].split(" ")), 2)
            # print(instr)
            # print(pc)
            # print(reg_we)
            # print(reg)
            # print(reg_data)
            # print(mem_we)
            # print(mem_data)
            if reg_we and reg != 0 :
                spj_str = f"@{pc:08x}: ${reg:2d} <= {reg_data:08x}\n"
                # print(spj_str)
                spj.append(spj_str)
            elif mem_we :
                spj_str = f"@{pc:08x}: *{mem:08x} <= {mem_data:08x}\n"
                # print(spj_str)
                spj.append(spj_str)
        with open(log_txt, "w", encoding="utf-8") as file :
            file.writelines(spj)
            file.write("\n")

    def run_logisim(self, *args) :
        content = ""
        with open(os.path.join("util","test_main.txt"), "r", encoding="utf-8") as main_file :
            content = "".join(main_file.readlines())
        # print(content)

        for cpu in args :
            cpu_files, more = find_files(cpu, ".circ")

            out_log = os.path.join(self._dir, "log", os.path.basename(cpu))
            # os.system(f"mkdir -p {out_log}")
            os.makedirs(out_log, exist_ok=True)
            for cpu_file in cpu_files :
                self.__add_main(cpu_file, content)
                print()
                print(f"{os.path.basename(cpu_file)}: Running logisim......")
                logs, log_txt = self.__get_raw_logs(cpu_file, out_log)

                print(f"{os.path.basename(cpu_file)}: Output the spj......")
                self.__trans_to_spj(logs, log_txt)
                
                print(f"{os.path.basename(cpu_file)}: Logisim is already!")

class XilinxRunner(Runner) :
    def __init__(self, path, mars, cpu_path, the_dir, isFlow) :
        super(XilinxRunner, self).__init__(path, mars, the_dir, isFlow)
        self.__cpu_path = cpu_path
        self.__cpu_in_dir = os.path.basename(cpu_path)
        self.__cpus = None
        self.__funct_path = os.path.join(self._path, "bin", "nt64")
        self.__fuse_path = os.path.join(self.__funct_path, "fuse.exe")

    def fuse(self):
        more, cpus = find_dirs(self.__cpu_path)
        cpus = [cpu for cpu in cpus if os.path.isdir(os.path.join(self.__cpu_path, cpu))]
        self.__cpus = cpus
        for cpu in cpus:
            print()
            print(f"{cpu}: Start creating .prj and .tcl......")
            safe_makedirs(os.path.join(self._dir, self.__cpu_in_dir, cpu, "source"))
            ori_cpu_files, more = find_files(os.path.join(self.__cpu_path, cpu), ".v")
            cpu_files = []
            flag = False

            for file in ori_cpu_files:
                name = os.path.basename(file)
                safe_copy(file, os.path.join(self._dir, self.__cpu_in_dir, cpu, "source", name))
                
            safe_copy(os.path.join("util","mips_tb.v"), os.path.join(self._dir, self.__cpu_in_dir, cpu, "source", "mips_tb.v"))
            ori_cpu_files.append(os.path.join(self.__cpu_in_dir, "mips_tb.v"))
            wrong = self.__fuse_ext(cpu, ori_cpu_files)
            if not wrong:
                return False
            
        return True

    def __fuse_ext(self, cpu, ori_cpu_files):
        prj_path = os.path.join(self._dir, self.__cpu_in_dir, cpu, "mips.prj")
        tcl_path = os.path.join(self._dir, self.__cpu_in_dir, cpu, "mips.tcl")
        with open(prj_path, "w", encoding="utf-8") as prj:
            for file in ori_cpu_files:
                name = os.path.basename(file)
                prj.write('verilog work \"' + os.path.join("source", name) + "\"\n")

        with open(tcl_path, "w", encoding="utf-8") as tcl:
            tcl.write("run 200us;\nexit")
        print(f"{cpu}: .prj and .tcl prepared!!!")
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
        print(f"{cpu}: Starting fusing......")
        safe_execute(fuse, os.path.join(self._dir, self.__cpu_in_dir, cpu, "fuse_info.txt"), cwd=os.path.join(self._dir, self.__cpu_in_dir, cpu))
        path = os.path.join(self._dir, self.__cpu_in_dir, cpu, "mips.exe")
        if not os.path.exists(path):
            print("There is something wrong when fusing")
            errors = []
            with open(os.path.join(self._dir, self.__cpu_in_dir, cpu, "fuse.log"), "r", encoding="utf-8") as fse:
                errors = fse.readlines()
            errors = [error for error in errors if "ERROR" in error]
            for error in errors:
                print(error.strip())
            return False

        safe_remove(os.path.join(self._dir, self.__cpu_in_dir, cpu, "fuse_info.txt"))
        safe_remove(os.path.join(self._dir, self.__cpu_in_dir, cpu, "fuse.log"))
        safe_remove(os.path.join(self._dir, self.__cpu_in_dir, cpu, "fuse.xmsgs"))
        safe_remove(os.path.join(self._dir, self.__cpu_in_dir, cpu, "fuseRelaunch.cmd"))
        print(f"{cpu}: fuse end!!!")
        return True
    def __isim_ext(self, cpu):
        ext = [
            "mips.exe",
            "-nolog",
            "-tclbatch",
            "mips.tcl",
        ]
        ext = " ".join(ext)
        # print(ext)
        # os.system(ext)
        safe_execute(ext, os.path.join(self._dir, self.__cpu_in_dir, cpu, "output.txt"), cwd=os.path.join(self._dir, self.__cpu_in_dir, cpu), delay=0.5)
        # time.sleep(0.5)
        # xrunner.safe_rmtree(os.path.join(test_dir,"isim"))
        # safe_remove(os.path.join(self._dir, self.__cpu_path, cpu, "isim.wdb"))
        # safe_remove(os.path.join(self._dir, self.__cpu_path, cpu, "isim.log"))

    def run_isim(self):
        all_test = os.path.join(self._dir, "hex")
        tests, names = find_files(all_test)

        for cpu in self.__cpus :
            print()
            print(f"{cpu}: Start logging output......")
            safe_makedirs(os.path.join(self._dir, "log", cpu))
            for test in tests :
                print(f"{cpu}: Executing {os.path.basename(test)}......")
                name = os.path.basename(test).replace(".txt", "")
                safe_copy(test, os.path.join(self._dir, self.__cpu_in_dir, cpu, "code.txt"))
                self.__isim_ext(cpu)
                contents = []
                with open(os.path.join(self._dir, self.__cpu_in_dir, cpu, "output.txt"), "r", encoding="utf-8") as file :
                    contents = file.readlines()
                contents = [content for content in contents if "@" in content and "$ 0" not in content]
                contents = ["@" + content.split("@")[1] for content in contents]
                filted = []
                for content in contents :
                    if self._is_pcpass(content) :
                        break
                    filted.append(content)

                with open(os.path.join(self._dir, self.__cpu_in_dir, cpu, "output.txt"), "w", encoding="utf-8") as file :
                    file.writelines(filted)
                safe_copy(os.path.join(self._dir, self.__cpu_in_dir, cpu, "output.txt"), os.path.join(self._dir, "log", cpu, f"{name}-{cpu}-out.txt"))
                print(f"{cpu}: {os.path.basename(test)} is executed!!!")
            safe_rmtree(os.path.join(self._dir, self.__cpu_in_dir, cpu))
        safe_rmtree(os.path.join(self._dir, self.__cpu_in_dir))
        
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
            if file.endswith(key) :
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
            if _dir.endswith(key) :
                results.append(os.path.join(root, _dir))
                names.append(_dir)
    return results, names

def safe_execute(cmd, file, cwd=".", retries=5, delay=0.1) :
    for _ in range(retries) :
        try :
            with open(file, "w", encoding="utf-8") as stdout :
                subprocess.run(cmd, stdout=stdout, stderr=subprocess.STDOUT, cwd=cwd)
            return 
        except (FileNotFoundError, PermissionError) :
            time.sleep(delay)
    try:
        # print(f"cd {cwd} && " + cmd)
        cmd += f" > {os.path.basename(file)}"
        os.system(f"cd {cwd} && " + cmd)
    except :
        print("Error: can't execute the code correctly!!!")

def safe_rmtree(path, retries=5, delay=0.1):
    for _ in range(retries):
        try:
            shutil.rmtree(path)
            return  # 成功删除后返回
        except (FileNotFoundError, PermissionError):
            time.sleep(delay)  # 等待一段时间后重试
    print(f"Failed to delete {path} after {retries} attempts.")

def safe_remove(path, retries=5, delay=0.1):
    for _ in range(retries):
        try:
            os.remove(path)
            return  # 成功删除后返回
        except (FileNotFoundError, PermissionError):
            time.sleep(delay)  # 等待一段时间后重试
    print(f"Failed to delete {path} after {retries} attempts.")

def safe_copy(src, dst, retries=5, delay=0.1) :
    for _ in range(retries) :
        try: 
            shutil.copy(src, dst)
            return
        except (FileNotFoundError, PermissionError):
            time.sleep(delay)
    print(f"Failed to copy {src} to {dst} after {retries} attempts.")
    

def safe_makedirs(path, exist_ok=True, retries=5, delay=0.1) :
    for _ in range(retries) :
        try :
            os.makedirs(path, exist_ok=exist_ok)
            return
        except (PermissionError, OSError) :
            time.sleep(delay)
    print(f"Failed to makedirs {path} after {retries} attempts.")

class TimeoutException(Exception):
    pass

def timeout(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = [TimeoutException(f"Function {func.__name__} timed out after {seconds} seconds")]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    result[0] = e
            
            thread = threading.Thread(target=target)
            thread.start()
            thread.join(seconds)

            if thread.is_alive():
                return result[0]  # 返回超时异常或超时信息
            else:
                return result[0]
        return wrapper
    return decorator


if __name__ == "__main__" :
    runner = Runner("abc", "test_dr")
    # num = runner.translate("beq $31, $15, jumplabel")
    # print()

    print(runner.is_pcpass("@00005004: $29 <= 0d89e43c"))