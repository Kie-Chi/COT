import os
import re
import sys
import time
import shutil
import subprocess
import threading
from functools import wraps
from typing import Optional, Iterable, Tuple

REGEX_REG = r'@\s*(?P<pc>[0-9a-f]+)\s*:\s*\$\s*(?P<reg>[0-9a-f]+)\s*<=\s*(?P<val>[0-9a-f]+)'
REGEX_ADDR = r'@\s*(?P<pc>[0-9a-f]+)\s*:\s*\*\s*(?P<addr>[0-9a-f]+)\s*<=\s*(?P<val>[0-9a-f]+)'
REGEX_REG_FLOW = r'\s*(?P<ts>\d+)\s*' + REGEX_REG
REGEX_ADDR_FLOW = r'\s*(?P<ts>\d+)\s*' + REGEX_ADDR

def _dump_hex_task(params: Tuple[str, str, str, str, str]):
    code, hex_txt, mars, the_dir, java_path = params
    mips = [
        java_path,
        "-jar",
        os.path.join("..", mars),
        "mc",
        "LargeText",
        "a",
        "dump",
        ".text",
        "HexText",
        hex_txt.replace(the_dir+os.sep, ""),
        code.replace(the_dir+os.sep, ""),
    ]
    info_dir = os.path.join(the_dir, "info")
    os.makedirs(info_dir, exist_ok=True)
    info_file = os.path.join(info_dir, f"{os.path.basename(code)}.info.txt")
    print_colored(f"{os.path.basename(code)}: ", 35, end="")
    print_colored("Mars is dumping data...", 37)
    safe_execute(mips, info_file, cwd=the_dir)
    contents = safe_read(info_file)
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

def _run_asm_task(params: Tuple[str, str, str, bool, bool, str]):
    code, log_txt, mars, is_flow, is_except, java_path = params
    ext = [
        java_path,
        "-jar",
        mars,
        "mc",
        "LargeText",
        "40000",
        "lg",
        code,
    ]
    if is_flow:
        ext.insert(3, "db")
    if is_except:
        ext.insert(3, "ex")
    print_colored(f"{os.path.basename(code)}: ", 35, end="")
    print_colored("Mars executing asm...", 37)
    safe_execute(ext, log_txt)
    contents = ""
    with open(log_txt, "r", encoding="utf-8") as file:
        contents = file.readlines()
    flag = False
    if "Program terminated when maximum step limit 40000 reached.\n" in contents:
        if len(contents) > 20000:
            flag = True
    if not flag:
        reg_pat = re.compile(REGEX_REG_FLOW if is_flow else REGEX_REG, re.IGNORECASE)
        addr_pat = re.compile(REGEX_ADDR_FLOW if is_flow else REGEX_ADDR, re.IGNORECASE)
        filtered = []
        for content in contents:
            m = reg_pat.search(content)
            if m:
                reg_str = m.group('reg')
                try:
                    reg_num = int(reg_str)
                except Exception:
                    try:
                        reg_num = int(reg_str, 16)
                    except Exception:
                        reg_num = 1
                if reg_num != 0:
                    filtered.append(content)
                continue
            m = addr_pat.search(content)
            if m:
                filtered.append(content)
        with open(log_txt, "w", encoding="utf-8") as file:
            file.writelines(filtered)
    else:
        safe_remove(code)
        safe_remove(log_txt)
        safe_remove(log_txt.replace("stdout", "hex"))

def _fuse_task(params: Tuple[str, str, str, str, int, str, str, str]):
    cpu, cpu_src_path, the_dir, cpu_in_dir, tb, xilinx_path, fuse_path, asm_dir = params
    target_root = os.path.join(the_dir, cpu_in_dir, cpu)
    safe_makedirs(os.path.join(target_root, "source"))
    ori_cpu_files = []
    for root, dirs, files in os.walk(cpu_src_path):
        for file in files:
            if file.endswith(".v"):
                ori_cpu_files.append(os.path.join(root, file))
        del dirs[:]
    has_tb = False
    for file in ori_cpu_files:
        name = os.path.basename(file)
        if name == "mips_tb.v":
            has_tb = True
        safe_copy(file, os.path.join(target_root, "source", name))
    if tb != 0:
        safe_copy(os.path.join("util", f"mips_tb_{tb}.v"), os.path.join(target_root, "source", "mips_tb.v"))
    prj_path = os.path.join(target_root, "mips.prj")
    tcl_path = os.path.join(target_root, "mips.tcl")
    with open(prj_path, "w", encoding="utf-8") as prj:
        for file in ori_cpu_files:
            name = os.path.basename(file)
            prj.write('verilog work "' + os.path.join("source", name) + "\"\n")
        if not has_tb:
            prj.write('verilog work "' + os.path.join("source", "mips_tb.v") + "\"\n")
    with open(tcl_path, "w", encoding="utf-8") as tcl:
        tcl.write("run 300us;\nexit")
    useless, names = find_files(os.path.join(the_dir, asm_dir))
    flag = False
    if not os.path.exists(os.path.join(the_dir, "tbs")):
        flag = True
    else:
        for name in names:
            if not os.path.exists(os.path.join(the_dir, "tbs", name.replace(".asm", "_tb.v"))):
                flag = True
                break
    if flag:
        fuse = [
            fuse_path,
            "-nodebug",
            "-prj",
            "mips.prj",
            "-o",
            "mips.exe",
            "mips_tb",
            "-mt",
            "off",
        ]
        fuse = " ".join(fuse)
        if os.name == str("nt"):
            os.environ["LD_LIBRARY_PATH"] = os.path.join(xilinx_path, "lib", "nt64")
            os.environ["XILINX"] = xilinx_path
        else:
            os.environ["LD_LIBRARY_PATH"] = os.path.join(xilinx_path, "lib", "lin64")
            os.environ["XILINX"] = xilinx_path
        safe_execute(fuse, os.path.join(target_root, "fuse_info.txt"), cwd=target_root)
        path = os.path.join(target_root, "mips.exe")
        if not os.path.exists(path):
            print_colored("ERROR: There is something wrong when fusing", 31)
            errors = []
            with open(os.path.join(target_root, "fuse.log"), "r", encoding="utf-8") as fse:
                errors = fse.readlines()
            errors = [error for error in errors if "ERROR" in error]
            for error in errors:
                print_colored(error.strip(), 31)
            return False
        safe_remove(os.path.join(target_root, "fuse_info.txt"))
        safe_remove(os.path.join(target_root, "fuse.log"))
        safe_remove(os.path.join(target_root, "fuse.xmsgs"))
        safe_remove(os.path.join(target_root, "fuseRelaunch.cmd"))
    return True

def _isim_task(params: Tuple[str, str, str, str, str, bool, str, Iterable[str]]):
    cpu, base_cpu, the_dir, cpu_in_dir, xilinx_path, fuse_path, is_flow, asm_dir, tests = params
    safe_makedirs(os.path.join(the_dir, "log", base_cpu))
    def sort_key(file):
        name = os.path.basename(file).replace(".txt", "")
        return os.path.exists(os.path.join(the_dir, "tbs", f"{name}_tb.v"))
    tests = sorted(list(tests), key=sort_key)
    ind = 0
    for test in tests:
        print_colored(f"{cpu}: ", 35, end="")
        print_colored(f"Executing {os.path.basename(test).replace('.txt', '')}...", 37)
        name = os.path.basename(test).replace(".txt", "")
        safe_copy(test, os.path.join(the_dir, cpu_in_dir, cpu, "code.txt"))
        if os.path.exists(os.path.join(the_dir, "tbs", f"{name}_tb.v")):
            safe_copy(os.path.join(the_dir, "tbs", f"{name}_tb.v"), os.path.join(the_dir, cpu_in_dir, cpu, "source", "mips_tb.v"))
            _fuse_task((cpu, os.path.join(the_dir, cpu_in_dir, cpu, "source"), the_dir, cpu_in_dir, 0, xilinx_path, fuse_path, asm_dir))
        if os.name != str("nt"):
            test_exe = os.path.join(".", "mips.exe")
        else:
            test_exe = "mips.exe"
        ext = [
            test_exe,
            "-nolog",
            "-tclbatch",
            "mips.tcl",
        ]
        ext = " ".join(ext)
        if os.name == str("nt"):
            os.environ["LD_LIBRARY_PATH"] = os.path.join(xilinx_path, "lib", "nt64")
            os.environ["XILINX"] = xilinx_path
        else:
            os.environ["LD_LIBRARY_PATH"] = os.path.join(xilinx_path, "lib", "lin64")
            os.environ["XILINX"] = xilinx_path
        safe_execute(ext, os.path.join(the_dir, cpu_in_dir, cpu, "output.txt"), cwd=os.path.join(the_dir, cpu_in_dir, cpu), retries=10, delay=0.1)
        contents = []
        with open(os.path.join(the_dir, cpu_in_dir, cpu, "output.txt"), "r", encoding="utf-8") as file:
            contents = file.readlines()
        if contents == []:
            ind += 1
            print_colored("WARNING: No output got", 33)
        reg_pat = re.compile(REGEX_REG_FLOW if is_flow else REGEX_REG, re.IGNORECASE)
        addr_pat = re.compile(REGEX_ADDR_FLOW if is_flow else REGEX_ADDR, re.IGNORECASE)
        matched = []
        for content in contents:
            m = reg_pat.search(content)
            if m:
                reg_str = m.group('reg')
                try:
                    reg_num = int(reg_str)
                except Exception:
                    try:
                        reg_num = int(reg_str, 16)
                    except Exception:
                        reg_num = 1
                if reg_num != 0:
                    matched.append(content)
                continue
            m = addr_pat.search(content)
            if m:
                matched.append(content)
        if is_flow == True:
            try:
                contents = [(int(content.split("@")[0].strip()), 1 if "*" in content.split("@")[1] else 0, "@" + content.split("@")[1]) for content in matched]
            except ValueError as e:
                print_colored("WARNING: Invalid timestamp in output", 33)
                raise
        else:
            contents = [(0, 0, "@" + content.split("@")[1]) for content in matched]
        filted = contents
        if is_flow == True:
            filted.sort(key=lambda x: (x[0], x[1]))
        filted = [fil[2] for fil in filted]
        with open(os.path.join(the_dir, cpu_in_dir, cpu, "output.txt"), "w", encoding="utf-8") as file:
            file.writelines(filted)
        safe_copy(os.path.join(the_dir, cpu_in_dir, cpu, "output.txt"), os.path.join(the_dir, "log", base_cpu, f"{name}-{base_cpu}-out.txt"))
    pass

class Runner :
    def __init__(self, path: str, mars:str, the_dir: str, isFlow: bool, Except: bool, pool: Optional[object]=None) :
        self._path = path
        self._dir = the_dir
        self._mars = mars
        self._is_flow = isFlow
        self._is_except = Except
        self._pool = pool
        self._java = self.__resolve_java()

    def __resolve_java(self) -> str:
        try:
            import shutil as _sh
            which = _sh.which("java")
            if which:
                return which
        except Exception:
            pass
        java_home = os.environ.get("JAVA_HOME", "")
        if java_home:
            candidate = os.path.join(java_home, "bin", "java.exe" if os.name == str("nt") else "java")
            if os.path.exists(candidate):
                return candidate
        local_jre = os.path.join("util", "jre", "bin", "java.exe" if os.name == str("nt") else "java")
        if os.path.exists(local_jre):
            return local_jre
        return "java"
        
    def dump_hex(self, src, hex_dst) :
        os.makedirs(hex_dst, exist_ok=True)
        print_colored()
        print_colored("Mars: ", 34, end="")
        print_colored("Start dumping datas...")
        tasks = []
        for code in src:
            hex_txt = os.path.join(hex_dst, f"{os.path.basename(code).replace('.asm', '.txt')}")
            tasks.append((code, hex_txt, self._mars, self._dir, self._java))
        if self._pool is not None:
            list(self._pool.map(_dump_hex_task, tasks))
        else:
            for params in tasks:
                _dump_hex_task(params)
        print_colored("Mars: ", 34, end="")
        print_colored("All dumped!!!")

    def _run_asm(self, src, out_log) :
        os.makedirs(out_log, exist_ok=True)
        print_colored()
        print_colored("Mars: ", 34, end="")
        print_colored("Start executing asm...")
        tasks = []
        for code in src:
            log_txt = os.path.join(out_log, f"{os.path.basename(code).replace('.asm', '.txt')}")
            tasks.append((code, log_txt, self._mars, self._is_flow, self._is_except, self._java))
        if self._pool is not None:
            list(self._pool.map(_run_asm_task, tasks))
        else:
            for params in tasks:
                _run_asm_task(params)
        print_colored("Mars: ", 34, end="")
        print_colored("All executed!!!")


    def run_mars(self, src, hex_dst, out_log) :
        self.dump_hex(src, hex_dst)    
        self._run_asm(src, out_log)

class LogisimRunner(Runner) :
    def __init__(self, path, mars, the_dir, isFlow, Except, pool=None) -> None: 
        super(LogisimRunner, self).__init__(path, mars, the_dir, isFlow, Except, pool)
        

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
            self._java,
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
    def __init__(self, path, mars, cpu_path, the_dir, isFlow, Except, tb, asm_dir, pool=None) :
        super(XilinxRunner, self).__init__(path, mars, the_dir, isFlow, Except, pool)
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
        base_cpus = []
        cpus_path = []
        for mips in mips_cpus:
            if os.path.dirname(mips) not in base_cpus:
                base_cpus.append(self.__cpu_in_dir + os.path.dirname(mips).replace(self.__cpu_path, "").replace(os.sep, "@"))
                cpus_path.append(os.path.dirname(mips))
        # decide replica count by tests and cores
        tests, _ = find_files(os.path.join(self._dir, "hex"))
        test_count = len(tests)
        cores = os.cpu_count() or 1
        replicas = min(4, min(test_count if test_count > 0 else 1, cores // len(base_cpus)))
        print_colored()
        print_colored("ISE: ", 34, end="")
        print_colored("Start fusing...")
        fuse_targets = []
        tasks = []
        for i, cpu in enumerate(base_cpus):
            for r in range(replicas):
                cpu_rep = f"{cpu}@@{r}"
                fuse_targets.append(cpu_rep)
                tasks.append((cpu_rep, cpus_path[i], self._dir, self.__cpu_in_dir, self.__tb, self._path, self.__fuse_path, self._asm_dir))
        results = []
        if self._pool is not None:
            results = list(self._pool.map(_fuse_task, tasks))
        else:
            results = [ _fuse_task(t) for t in tasks ]
        if not all(results):
            return False
        self.__cpus = fuse_targets
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
            "mips_tb",
            "-mt",
            "off",
        ]
        fuse = " ".join(fuse)
        if os.name == str("nt"):
            os.environ["LD_LIBRARY_PATH"] = os.path.join(self._path, "lib", "nt64")
            os.environ["XILINX"] = self._path
        else:
            os.environ["LD_LIBRARY_PATH"] = os.path.join(self._path, "lib", "lin64")
            os.environ["XILINX"] = self._path
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
        groups = {}
        for cpu in self.__cpus:
            base = cpu.split('@@')[0]
            groups.setdefault(base, []).append(cpu)
        tasks = []
        for base, replicas in groups.items():
            rcount = len(replicas)
            if rcount == 0:
                continue
            parts = [[] for _ in range(rcount)]
            for idx, t in enumerate(tests):
                parts[idx % rcount].append(t)
            for i, rep in enumerate(replicas):
                tasks.append((rep, base, self._dir, self.__cpu_in_dir, self._path, self.__fuse_path, self._is_flow, self._asm_dir, parts[i]))
        if self._pool is not None:
            list(self._pool.map(_isim_task, tasks))
        else:
            for params in tasks:
                _isim_task(params)
        for cpu in self.__cpus:
            safe_rmtree(os.path.join(self._dir, self.__cpu_in_dir, cpu), 20, 0.1)
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
                if isinstance(cmd, str):
                    subprocess.run(cmd, stdout=stdout, stderr=subprocess.STDOUT, cwd=cwd, shell=True)
                else:
                    subprocess.run(cmd, stdout=stdout, stderr=subprocess.STDOUT, cwd=cwd)
            return
        except (FileNotFoundError, PermissionError) :
            time.sleep(delay)
    try:
        if isinstance(cmd, list):
            parts = []
            for c in cmd:
                s = str(c)
                if os.name == str("nt"):
                    if any(ch in s for ch in [' ', '(', ')', '&', '^']):
                        s = f'"{s}"'
                else:
                    import shlex
                    s = shlex.quote(s)
                parts.append(s)
            cmd_str = " ".join(parts)
        else:
            cmd_str = str(cmd)
        out_name = os.path.basename(file)
        cmd_str = f'{cmd_str} > "{out_name}"'
        os.system(f'cd "{cwd}" && {cmd_str}')
    except :
        print_colored(f"ERROR: can't execute {cmd} correctly!!!", 31)
        raise Exception
    
def safe_rmtree(path, retries=5, delay=0.1):
    if os.path.exists(path):
        for _ in range(retries):
            try:
                shutil.rmtree(path)
                return
            except Exception:
                time.sleep(delay)
        try:
            if os.name == str("nt"):
                os.system(f'rmdir /S /Q "{path}"')
            else:
                os.system(f'rm -rf "{path}"')
        except Exception:
            pass
        if os.path.exists(path):
            print_colored(f"Failed to delete {path} after {retries} attempts.", 33)

def safe_remove(path, retries=5, delay=0.1):
    if os.path.exists(path):
        for _ in range(retries):
            try:
                os.remove(path)
                return
            except Exception:
                time.sleep(delay)
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
    encodings = ["utf-8", "GBK", "GB2312", "latin-1"]
    for _ in range(retries):
        for enc in encodings:
            try:
                with open(src, "r", encoding=enc) as file:
                    contents = file.readlines()
                return contents
            except UnicodeDecodeError:
                continue
            except (FileNotFoundError, PermissionError):
                time.sleep(delay)
                break
    try:
        print_colored(f"WARNING: Can not read {src} with {encodings.__str__()}, try to ignore errors.", 33)
        with open(src, "r", encoding="utf-8", errors="ignore") as file:
            contents = file.readlines()
        return contents
    except Exception:
        return contents

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
