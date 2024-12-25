import os
import json
import Runner
import re
import sys
class Config :
    def __init__(self) :
        self.xilinx_path = ""
        self.cir_dir = ""
        self.verilog_dir = ""

        self.config_name = ""
        self.type = None
        self.flow = False
        self.exc = False
        self.session = ""
        self.info = ""
        self.tb = 0
        self.test_times = 0

        self.self_util = ""
        self.self_dir = ""

        self.random_set = ""
        self.unit_set = ""

        self.logisim_path = os.path.join("util","logisim-generic-2.7.1.jar")
        self.mars_path = os.path.join("util", "mars.jar")

        self.src_slt = {}
        self.default_src = {
            "q": "exit",
            "w": "view config"
        }
        self.mtd_slt = {}
        self.default_mtd = {
            "q": "exit",
            "r": "back to last select"
        }
        self.src = ""
        self.mtd = ""

        self.__lazy = False
        self.__default_p3 = {
            "type": "logisim",
            "flow": False,
            "exc": False,
            "test_times": 10,
            "random_set": {
                "cal_r": ["add", "sub"],
                "cal_i": ["ori"],
                "lui": ["lui"],
                "store": ["sw"],
                "load": ["lw"],
                "branch": ["beq"],
                "nop": ["nop"]
            },
            "unit_set": {
                "set_test": ["cal_i", "lui"],
                "arth_test": ["cal_r"],
                "mem_test": ["store", "load"],
                "branch_test": ["branch"],
            }
        }

        self.__default_p4 = {
            "type": "verilog",
            "flow": False,
            "exc": False,
            "tb": 1,
            "test_times": 10,
            "random_set": {
                "cal_r": ["add", "sub"],
                "cal_i": ["ori"],
                "lui": ["lui"],
                "store": ["sw"],
                "load": ["lw"],
                "branch": ["beq"],
                "j_l": ["jal"],
                "j_r": ["jr"],
                "nop": ["nop"]
            },
            "unit_set": {
                "set_test": ["cal_i", "lui"],
                "arth_test": ["cal_r"],
                "mem_test": ["store", "load"],
                "branch_test": ["branch"],
                "jump_test": ["j_l", "j_r"]
            }
        }

        self.__default_p5 = {
            "type": "verilog",
            "flow": True,
            "exc": False,
            "tb": 1,
            "test_times": 10,
            "random_set": {
                "cal_r": ["add", "sub"],
                "cal_i": ["ori"],
                "lui": ["lui"],
                "store": ["sw"],
                "load": ["lw"],
                "branch": ["beq"],
                "j_l": ["jal"],
                "j_r": ["jr"],
                "nop": ["nop"]
            },
            "unit_set": {
                "set_test": ["cal_i", "lui"],
                "arth_test": ["cal_r"],
                "mem_test": ["store", "load"],
                "branch_test": ["branch"],
                "jump_test": ["j_l", "j_r"]
            }
        }

        self.__default_p6 = {
            "type": "verilog",
            "flow": True,
            "exc": False,
            "tb": 2,
            "test_times": 10,
            "random_set": {
                "cal_r": ["add", "sub", "andr", "orr", "slt", "sltu"],
                "cal_i": ["ori", "addi", "andi"],
                "lui": ["lui"],
                "store": ["sw", "sb", "sh"],
                "load": ["lw", "lb", "lh"],
                "branch": ["beq", "bne"],
                "md": ["mult", "multu", "div", "divu"],
                "mf": ["mfhi", "mflo"],
                "mt": ["mthi", "mtlo"],
                "j_l": ["jal"],
                "j_r": ["jr"],
                "nop": ["nop"]
            },
            "unit_set": {
                "set_test": ["cal_i", "lui", "mt", "mf"],
                "arth_test": ["cal_r", "md"],
                "mem_test": ["store", "load"],
                "branch_test": ["branch"],
                "jump_test": ["j_l", "j_r"]
            }
        }

        self.__default_p7 = {
            "type": "verilog",
            "flow": True,
            "exc": True,
            "tb": 3,
            "test_times": 7,
            "random_set": {
                "cal_r": ["add", "sub", "andr", "orr", "slt", "sltu"],
                "cal_i": ["ori", "addi", "andi"],
                "lui": ["lui"],
                "store": ["sw", "sb", "sh"],
                "load": ["lw", "lb", "lh"],
                "branch": ["beq", "bne"],
                "md": ["mult", "multu", "div", "divu"],
                "mf": ["mfhi", "mflo"],
                "mt": ["mthi", "mtlo"],
                "j_l": ["jal"],
                "j_r": ["jr"],
                "nop": ["nop"]
            },
            "unit_set": {
                "set_test": ["cal_i", "lui", "mt", "mf"],
                "arth_test": ["cal_r", "md"],
                "mem_test": ["store", "load"],
                "branch_test": ["branch"],
                "jump_test": ["j_l", "j_r"]
            }
        }
        self.__init()

    def find_ise(self) :
        result = []
        if os.name == "nt" :
            drives = []
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if os.path.exists(f"{letter}:\\"):
                    drives.append(f"{letter}:\\")
            for drive in drives:
                result.extend(find_directory_with_depth(drive, "Xilinx"))
        else :
            result.extend(find_directory_with_depth("/", "Xilinx"))
        path = ""
        result = [os.path.join(res, "14.7", "ISE_DS", "ISE") for res in result]
        slt = {str(i+1):result[i] for i in range(len(result))}
        if len(result) > 1 :
            while True:
                Runner.print_colored()
                Runner.print_colored("-------------------------", 37)
                for key in slt.keys():
                    Runner.print_colored(f"[{key}]> ", 34, end="")
                    Runner.print_colored(f"{slt[key]}")
                Runner.print_colored("-------------------------", 37)
                Runner.print_colored("choose one you want: ", 32, end="")
                the_slt = input()
                if the_slt in slt.keys():
                    path = slt[the_slt]
                    break
                else:
                    Runner.print_colored("ERROR: Invalid slt", 31)
            return path
            return path
        elif len(result) == 1 :
            path = result[0]
            return path
        else :
            Runner.print_colored("ERROR: Machine can't find valid ISE_path", 31)
            while True:
                Runner.print_colored("You want set xilinx_path as(q for exit): ", 32, end="")
                path = input()
                if path == "q":
                    self.__exit()
                elif not os.path.exists(path):
                    Runner.print_colored("ERROR: Invalid path, Please try again or exit")
                else:
                    break
            return path

    def find_circ(self) :
        result = []
        if os.name == "nt" :
            drives = []
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if os.path.exists(f"{letter}:\\"):
                    drives.append(f"{letter}:\\")
            for drive in drives:
                possible_circ = find_option_with_depth(drive, ".circ", max_depth=4)
                result.extend(possible_circ)
        else:
            result.extend(find_option_with_depth("/", ".circ", max_depth=4))
        
        circ_path = []
        for possible in result :
            if os.path.dirname(possible) not in circ_path :
                circ_path.append(os.path.dirname(possible))

        slt = {str(i+1):circ_path[i] for i in range(len(circ_path))}
        path = ""
        if len(circ_path) > 1:
            while True:
                Runner.print_colored()
                Runner.print_colored("-------------------------", 37)
                for key in slt.keys():
                    Runner.print_colored(f"[{key}]> ", 34, end="")
                    Runner.print_colored(f"{slt[key]}")
                Runner.print_colored("-------------------------", 37)
                Runner.print_colored("choose one you want: ", 32, end="")
                the_slt = input()
                if the_slt in slt.keys():
                    path = slt[the_slt]
                    break
                else:
                    Runner.print_colored("ERROR: Invalid slt", 31)
            return path
        elif len(circ_path) == 1:
            path = circ_path[0]
            return path
        else:
            Runner.print_colored("ERROR: Machine find no valid .circ can be used", 31)
            while True:
                Runner.print_colored("You want set circ_path as(q for exit): ", 32, end="")
                path = input()
                if path == "q":
                    self.__exit()
                elif not os.path.exists(path):
                    Runner.print_colored("ERROR: Invalid path, Please try again or exit")
                else:
                    break
            return path
    def find_verilog(self) :
        result = []
        if os.name == "nt" :
            drives = []
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if os.path.exists(f"{letter}:\\"):
                    drives.append(f"{letter}:\\")
            for drive in drives:
                possible_verilog = find_file_with_depth(drive, "mips.v", max_depth=4)
                result.extend(possible_verilog)
        else:
            result.extend(find_file_with_depth("/", "mips.v", max_depth=4))
            result.extend(find_file_with_depth(os.path.expanduser("~"), "mips.v", max_depth=4))
        verilog_path = []
        for possible in result :
            if os.path.dirname(possible) not in verilog_path :
                verilog_path.append(os.path.dirname(possible))

        cpu_path = []
        # print(result)
        # print(verilog_path)
        for verilog in verilog_path :
            if os.path.dirname(verilog) not in cpu_path :
                cpu_path.append(os.path.dirname(verilog))

        slt = {str(i+1):cpu_path[i] for i in range(len(cpu_path))}
        path = ""
        if len(cpu_path) > 1:
            while True:
                Runner.print_colored()
                Runner.print_colored("-------------------------", 37)
                for key in slt.keys():
                    Runner.print_colored(f"[{key}]> ", 34, end="")
                    Runner.print_colored(f"{slt[key]}")
                Runner.print_colored("-------------------------", 37)
                Runner.print_colored("choose one you want: ", 32, end="")
                the_slt = input()
                if the_slt in slt.keys():
                    path = slt[the_slt]
                    break
                else:
                    Runner.print_colored("ERROR: Invalid slt", 31)
            return path
        elif len(cpu_path) == 1:
            path = cpu_path[0]
            return path
        else:
            Runner.print_colored("ERROR: Machine find no valid .v can be used", 31)
            while True:
                Runner.print_colored("You want set verilog_path as(q for exit): ", 32, end="")
                path = input()
                if path == "q":
                    self.__exit()
                elif not os.path.exists(path):
                    Runner.print_colored("ERROR: Invalid path, Please try again or exit")
                else:
                    break
            return path

            # Runner.print_colored(verilog_path)    
            # Runner.print_colored(cpu_path)

    def __init(self) :
        self.__prepare()
        self.__draw_normal()

    def __prepare(self) :
        self.__read_config()
        if self.__lazy :    
            self.__draw_lazy()
        self.__verify_config()
        self.__init_select()


    def __draw_lazy(self) :
        Runner.print_colored("Welcome~ lazy-mode on!")
        slt = 0
        slts = [str(i+1) for i in range(5)]
        slts.append("q")
        slts.append("norm")
        while True :
            Runner.print_colored()
            Runner.print_colored("Options~")
            Runner.print_colored("-------------------------", 37)
            for i in range(1, 6):
                Runner.print_colored(f"[{i}]> ", 34, end="")
                Runner.print_colored(f"P{i+2}")
            Runner.print_colored("[q]> ", 31, end="")
            Runner.print_colored("exit")
            Runner.print_colored("-------------------------", 37)
            Runner.print_colored("You want: ", 32, end="")
            proj = input()

            if proj in slts:
                if proj == "q":
                    self.__exit()
                elif proj == "norm":
                    pass
                else:
                    slt = int(proj) + 2
                break
                    
            else:
                Runner.print_colored("ERROR: Invalid slt", 31)
        config = getattr(self, "_Config" + f"__default_p{slt}", None)
        if os.path.exists(os.path.join("configs", f"__default_p{slt}.json")):
            default_config = json.load(open(os.path.join("configs", f"__default_p{slt}.json"), "r", encoding="utf-8"))
            if slt == 3 :
                self.cir_dir = default_config["circ_dir"]
            else :
                self.xilinx_path = default_config["xilinx_path"]
                self.verilog_dir = default_config["verilog_dir"]
        else:
            if slt == 3 :
                self.cir_dir = self.find_circ()
                self.__default_p3["circ_dir"] = self.cir_dir
                json.dump({"circ_dir": self.cir_dir}, open(os.path.join("configs", f"__default_p{slt}.json"), "w", encoding="utf-8"))
                os.chmod(os.path.join("configs", f"__default_p{slt}.json"), 0o444)
            else :
                self.xilinx_path = self.find_ise()
                self.verilog_dir = self.find_verilog()
                temp = {
                    "xilinx_path": self.xilinx_path,
                    "verilog_dir": self.verilog_dir
                }
                json.dump(temp, open(os.path.join("configs", f"__default_p{slt}.json"), "w", encoding="utf-8")) 
                os.chmod(os.path.join("configs", f"__default_p{slt}.json"), 0o444)
        
        self.__set_attr(config, True)


    def __set_attr(self, file_config, lazy_call=False) :
        if not lazy_call :
            if "lazy-mode" in file_config.keys():
                    self.__lazy = file_config["lazy-mode"]
            if not isinstance(self.__lazy, bool):
                Runner.print_colored("ERROR: Please check attribute \"lazy-mode\" in config", 31)
                self.__exit()
            
            if self.__lazy :
                return 

        if "type" in file_config.keys():
            self.type = file_config["type"]
        if self.type != "logisim" and self.type != "verilog":
            Runner.print_colored("ERROR: Please check atttribute \"type\" in config", 31)
            self.__exit()
        
        if "flow" in file_config.keys():
            self.flow = file_config["flow"]
        if not isinstance(self.flow, bool):
            Runner.print_colored("ERROR: Please check attribute \"flow\" in config", 31)
            self.__exit()

        if "exc" in file_config.keys():
            self.exc = file_config["exc"]
        if not isinstance(self.exc, bool):
            Runner.print_colored("ERROR: Please check attribute \"exc\" in config", 31)
            self.__exit()

        if "tb" in file_config.keys():
            self.tb = file_config["tb"]
        if not (int(self.tb) >= 0 and int(self.tb) <= 3) and self.type == "verilog":
            Runner.print_colored("ERROR: Please check attribute \"tb\" in config", 31)
            self.__exit()

        if "xilinx_path" in file_config.keys():
            self.xilinx_path = file_config["xilinx_path"]
        if not os.path.exists(self.xilinx_path) and self.type == "verilog":
            Runner.print_colored("ERROR: Please check attribute \"xilinx_path\" in config", 31)
            self.__exit()
        
        if "circ_dir" in file_config.keys():
            self.cir_dir = file_config["circ_dir"]
        if not os.path.exists(self.cir_dir) and self.type == "logisim":
            Runner.print_colored("ERROR: Please check attribute \"circ_dir\" in config", 31)
            self.__exit()

        if "verilog_dir" in file_config.keys():
            self.verilog_dir = file_config["verilog_dir"]
        if not os.path.exists(self.verilog_dir) and self.type == "verilog":
            Runner.print_colored("ERROR: Please check attribute \"verilog_dir\" in config", 31)
            self.__exit()

        if "test_times" in file_config.keys():
            self.test_times = file_config["test_times"]
        if not str(self.test_times).isalnum():
            Runner.print_colored("ERROR: Please check attribute \"test_times\" in config", 31)
            self.__exit()

        if "self_util" in file_config.keys():
            self.self_util = file_config["self_util"]
        if not os.path.exists(self.self_util) and self.self_util != "":
            Runner.print_colored("ERROR: Please check attribute \"self_util\" in config", 31)
            self.__exit()

        if "self_dir" in file_config.keys():
            self.self_dir = file_config["self_dir"]
        if not os.path.exists(self.self_dir) and self.self_dir != "":
            Runner.print_colored("ERROR: Please check attribute \"self_dir\" in config", 31)
            self.__exit()

        if "random_set" in file_config.keys():
            self.random_set = file_config["random_set"]

        if "unit_set" in file_config.keys():
            self.unit_set = file_config["unit_set"]

        if not os.path.exists(self.logisim_path) and self.type == "logisim" :
            Runner.print_colored(f"ERROR: Can't find Logisim({self.logisim_path})", 31)
            self.__exit()
        
        if not os.path.exists(self.mars_path) :
            Runner.print_colored(f"ERROR: Can't find Mars({self.mars_path})", 31)
            self.__exit()

    def __read_config(self) :
        Runner.print_colored()
        config = []
        for root, dirs, files in os.walk("configs") :
            for file in files :
                if file.endswith(".json") :
                    config.append(os.path.join(root, file))
        file_config = {}
        if config :
            the_read = ""
            for con in config:
                if os.path.basename(con) == "file_config.json":
                    the_read = con
                    break
            if not the_read :
                the_read = config[0] 

            self.config_name = os.path.basename(the_read)
            with open(the_read, "r", encoding="utf-8") as file :
                try:
                    file_config:dict = json.load(file)
                except Exception as e:
                    Runner.print_colored("ERROR: Invalid config", 31)
                    Runner.print_colored(e, 31)
                    self.__exit()
            file_config = self.__format_set(file_config)
            self.__set_attr(file_config)
        else :
            Runner.print_colored("ERROR: No file can be used in .\\configs", 31)
            self.__exit()
    
    def __format_set(self, file_config:dict):
        trans_set = {
            "cal_r": ["add", "sub", "and", "or", "slt", "sltu"],
            "cal_i": ["ori", "addi", "andi"],
            "lui": ["lui"],
            "store": ["sw", "sb", "sh"],
            "load": ["lw", "lb", "lh"],
            "branch": ["beq", "bne"],
            "md": ["mult", "multu", "div", "divu"],
            "mf": ["mfhi", "mflo"],
            "mt": ["mthi", "mtlo"],
            "j_l": ["jal"],
            "j_r": ["jr"],
            "nop": ["nop"]
        }
        unit_set = {
            "set_test": ["cal_i", "lui", "mt", "mf"],
            "arth_test": ["cal_r", "md"],
            "mem_test": ["store", "load"],
            "branch_test": ["branch"],
            "jump_test": ["j_l", "j_r"]
        }

        trans = {}
        unit = {}

        mips_set = []
        if "mips_set" in file_config.keys():
            mips_set = file_config["mips_set"]
            del file_config["mips_set"]
        else:
            Runner.print_colored("ERROR: Please check attribute \"mips_set\" in config", 31)
        
        for mips in mips_set:
            for key in trans_set.keys():
                if mips in trans_set[key]:
                    if mips == "and" or mips == "or":
                        mips = mips + "r"
                    try:
                        trans[key].append(mips)
                    except:
                        trans[key] = []
                        trans[key].append(mips)
                    break
        for kide in trans.keys():
            for key in unit_set.keys():
                if kide in unit_set[key]:
                    try:
                        unit[key].append(kide)
                    except:
                        unit[key] = []
                        unit[key].append(kide)
                    break
        file_config["random_set"] = trans
        file_config["unit_set"] = unit
        return file_config

    def __init_select(self, src=""):
        self.src_slt = {}
        self.mtd_slt = {}
        self.src_slt["1"] = "with Mars"
        ind = 1
        self.mtd_slt[f"{ind}"] = "random test"
        ind += 1
        self.mtd_slt[f"{ind}"] = "unit test"
        ind += 1
        if self.type == "logisim":
            cpus, useless = Runner.find_files(self.cir_dir, ".circ")
            if len(cpus) > 1:
                self.src_slt["2"] = "with Others"
        else:
            cpus, useless = Runner.find_dirs(self.verilog_dir)
            cpus = [cpu for cpu in cpus if os.path.exists(os.path.join(self.verilog_dir, os.path.basename(cpu)))]
            if len(cpus) > 1:
                self.src_slt["2"] = "with Others"

        if self.exc :
            self.mtd_slt[f"{ind}"] = "exc test"
            ind += 1
            if src != "with Mars":
                self.mtd_slt[f"{ind}"] = "int test"
                ind += 1

        if self.self_dir != "" or self.self_util != "" :
            self.mtd_slt[f"{ind}"] = "self test"
            ind += 1
        self.src_slt.update(self.default_src)
        self.mtd_slt.update(self.default_mtd)

    def __verify_config(self) :
        self.info = [self.type,"flow" if self.flow else "single", "exc" if self.exc else "simple"]
        if self.type == "logisim":
            self.session = "P3"
            if self.flow == True:
                self.session = "??"
                Runner.print_colored("WARNING: You want to test a flow-based cpu built with Logisim", 33)
            if  self.exc == True:
                self.session = "??"
                Runner.print_colored("WARNING: You want to test a exception-handling cpu built with Logisim", 33)
            cpus, useless = Runner.find_files(self.cir_dir, ".circ")
            if cpus == []:
                Runner.print_colored("ERROR: You have no valid cpu for test", 31)
                self.__view_config()
                self.__exit()
        elif self.type == "verilog":
            self.session = "XX"
            if self.tb == 0:
                self.session = "??"
                cpus, useless = Runner.find_dirs(self.verilog_dir)
                cpus = [cpu for cpu in cpus if os.path.exists(os.path.join(self.verilog_dir, os.path.basename(cpu)))]
                has_tb = True
                for cpu in cpus:
                    files, useless = Runner.find_files(cpu, ".v")
                    has_mipt_tb = False
                    for file in files:
                        if "tb" in os.path.basename(file):
                            content = ""
                            with open(file, "r", encoding="utf-8") as the_file :
                                content = the_file.read()
                            name = re.findall(r"module (.*?)[\;\(]", content)[0]
                            if name == "mips_tb":
                                has_mipt_tb = True
                                break
                    if not has_mipt_tb:
                        has_tb = False 
                if not has_tb:
                    self.session = "XX"
                    Runner.print_colored("ERROR: You don't have testbench, and you won't accept a testbench added by Machine", 31)
                    self.__view_config()
                    self.__exit()
            if self.flow == True:
                if self.tb == 1:
                    if not self.exc:
                        self.session = "P5"
                    else:
                        self.session = "XX"
                        Runner.print_colored("ERROR: Seems your cpu can't handle exception but you set \"is_exc\" True", 31)
                        self.__view_config()
                        self.__exit()
                elif self.tb == 2:
                    if not self.exc:
                        self.session = "P6"
                    else:
                        self.session = "XX"
                        Runner.print_colored("ERROR: Seems your cpu can't handle exception but you set \"is_exc\" True", 31)
                        self.__view_config()
                        self.__exit()
                elif self.tb >= 3:
                    if self.exc:
                        self.session = "P7"
                    else:
                        self.session = "XX"
                        Runner.print_colored("ERROR: Seems you want to test a exception-handling cpu but you set \"is_exc\" False", 31)
                        self.__view_config()
                        self.__exit()
            else:
                if self.tb == 1:
                    if self.exc == True:
                        self.session = "??"
                        Runner.print_colored("WARNING: You want to test a exception-handling cpu but not a flow-based one", 33)
                    else:
                        self.session = "P4"
                else:
                    self.session = "XX"
                    Runner.print_colored("ERROR: You choose a wrong testbench for single-cycle cpu", 31)
                    self.__view_config()
                    self.__exit()
            cpus, useless = Runner.find_dirs(self.verilog_dir)
            cpus = [cpu for cpu in cpus if os.path.isdir(os.path.join(self.verilog_dir, cpu))]
            cpus = [cpu for cpu in cpus if os.sep not in cpu.replace(self.verilog_dir + os.sep, "")]            
            if cpus == []:
                Runner.print_colored("ERROR: You have no valid cpu for test", 31)
                self.__view_config()
                self.__exit()

        if self.session == "??":
            self.__view_config()
            Runner.print_colored("Press Enter to go on...", 32, end="")
            input()
    def __exit(self) :
        Runner.print_colored("Press Enter to exit...", 33, end="")
        input()        
        sys.exit()

    def __view_config(self) :
        Runner.print_colored()
        Runner.print_colored("---------", 37, end="")
        Runner.print_colored(f"{self.config_name}", end="")
        Runner.print_colored("----------", 37)
        Runner.print_colored(f"    type: ", 34, end="")
        Runner.print_colored(f"{self.session}")
        Runner.print_colored(f"    info: ", 34, end="")
        Runner.print_colored(f"{', '.join(self.info)}")
        if self.type == "logisim":
            cpus, useless = Runner.find_files(self.cir_dir, ".circ")
            Runner.print_colored(f"    cpus: ", 34, end="")
            Runner.print_colored(f"{self.cir_dir}")
            if cpus == []:
                Runner.print_colored(f"         no valid cpu", 31)
            ind = 0
            for cpu in cpus:
                ind += 1
                Runner.print_colored(f"         cpu{ind}: ", 36, end="")
                Runner.print_colored(f" {cpu}")
        elif self.type == "verilog" :
            tb_str = ""
            if self.tb == 0:
                tb_str = "not used"
            elif self.tb == 1:
                tb_str = "P4/P5"
            elif self.tb == 2:
                tb_str = "P6"
            elif self.tb >= 3:
                tb_str = "P7"
            Runner.print_colored(f"    tb: ", 34, end='')
            Runner.print_colored(f"{self.tb}({tb_str})")
            cpus, useless = Runner.find_dirs(self.verilog_dir)
            cpus = [cpu for cpu in cpus if os.path.isdir(os.path.join(self.verilog_dir, cpu))]
            cpus = [cpu for cpu in cpus if os.sep not in cpu.replace(self.verilog_dir + os.sep, "")]            
            Runner.print_colored(f"    cpus: ", 34, end="")
            Runner.print_colored(f"{self.verilog_dir}")
            if cpus == []:
                Runner.print_colored(f"         no valid cpu", 31)
            ind = 0
            for cpu in cpus:
                ind += 1
                Runner.print_colored(f"         cpu{ind}: ", 36, end="")
                Runner.print_colored(f"{cpu}")
            
            Runner.print_colored(f"    ISE: ", 34, end="")
            Runner.print_colored(f"{self.xilinx_path}")

        Runner.print_colored(f"    times:", 34, end="")
        Runner.print_colored(f" {self.test_times}")
        Runner.print_colored(f"---------{''.join(['-' for _ in range(len(self.config_name))])}----------", 37)


    def __draw_normal(self) :
        src_slt = ""
        mtd_slt = ""
        name = """ ____    ___    _____ 
/ ___|  / _ \  |_   _|
| |    | | | |   | |  
| |___ | |_| |   | |  
\____|  \___/    |_|  """
        Runner.print_colored(name, 36)
        while True:
            one_flag = False
            two_flag = False
            while True:
                Runner.print_colored()
                Runner.print_colored("Options about source")
                Runner.print_colored("-------------------------", 37)
                for key in self.src_slt.keys():
                    if key.isdigit():
                        Runner.print_colored(f"[{key}]> ", 34, end="")
                    elif key == "q":
                        Runner.print_colored(f"[{key}]> ", 31, end="")
                    elif key == "w":
                        Runner.print_colored(f"[{key}]> ", 33, end="")
                    Runner.print_colored(f"{self.src_slt[key]}")
                Runner.print_colored("-------------------------", 37)
                Runner.print_colored("the source you want is: ", 32, end="")
                the_slt_one = input()
                if the_slt_one in self.src_slt.keys() or the_slt_one == "cscore" or the_slt_one == "lazy":
                    if the_slt_one == "lazy":
                        self.__lazy = True
                        self.__prepare()
                    elif the_slt_one == "cscore":
                        pass
                    elif the_slt_one == "q":
                        self.__exit()
                    elif the_slt_one == "w":
                        self.__view_config()
                        Runner.print_colored("Press Enter to go on...", 32, end="")
                        input()
                    else:
                        src_slt = self.src_slt[the_slt_one]
                        one_flag = True
                        break
                else:
                    Runner.print_colored("ERROR: Invalid select, Please try again or exit", 31)
            if self.__lazy == True:
                mtd_slt = "lazy test"
                break
            self.__init_select(src_slt)
            while True:
                Runner.print_colored()
                Runner.print_colored("Options about method")
                Runner.print_colored("-------------------------", 37)
                for key in self.mtd_slt.keys():
                    if key.isdigit():
                        Runner.print_colored(f"[{key}]> ", 34, end="")
                    elif key == "q":
                        Runner.print_colored(f"[{key}]> ", 31, end="")
                    elif key == "r":
                        Runner.print_colored(f"[{key}]> ", 33, end="")
                    Runner.print_colored(f"{self.mtd_slt[key]}")
                Runner.print_colored("-------------------------", 37)
                Runner.print_colored("the method you want is: ", 32, end="")
                the_slt_two = input()
                if the_slt_two in self.mtd_slt.keys():
                    if the_slt_two == "q":
                        self.__exit()
                    elif the_slt_two == "r":
                        break
                    else:
                        mtd_slt = self.mtd_slt[the_slt_two]
                        two_flag = True
                        break
                else:
                    Runner.print_colored("ERROR: Invalid select, Please try again or exit/back", 31)
            if one_flag and two_flag:
                break
        
        if src_slt == "with Mars" :
            self.src = "withMars"
        elif src_slt == "with Others" :
            self.src = "withOthers"
        
        if mtd_slt == "unit test" :
            self.mtd = "unitTest"
        elif mtd_slt == "random test" :
            self.mtd = "randomTest"
        elif mtd_slt == "self test" :
            self.mtd = "selfTest"
        elif mtd_slt == "exc test" :
            self.mtd = "excTest"
        elif mtd_slt == "int test" :
            self.mtd = "intTest"
        elif mtd_slt == "lazy test" :
            self.mtd = "lazyTest"

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


if __name__ == "__main__" :

    # Runner.print_colored(find_directory_with_depth("D:\\", "Xilinx", max_depth=3))
    # possible_ise = find_path_with_depth("D:\\", "Xilinx\\14.7", max_depth=5)
    # possible_verilog = find_file_with_depth("D:\\code", "mips.v", max_depth=6)
    # possible_circ = find_option_with_depth("D:\\code", ".circ", max_depth=6)

    # ise_path = os.path.join(possible_ise[0], "ISE_DS", "ISE")
    # Runner.print_colored(ise_path)
    # verilog_path = []
    # for possible in possible_verilog :
    #     if possible.replace(os.sep + "mips.v", "") not in verilog_path :
    #         verilog_path.append(possible.replace(os.sep + "mips.v", ""))
    # Runner.print_colored(verilog_path)

    # circ_path = []
    # for possible in possible_circ :
    #     if os.path.dirname(possible) not in circ_path :
    #         circ_path.append(os.path.dirname(possible))
    # Runner.print_colored(circ_path)

    config = Config()
    # config.find_ise()
    # config.find_circ()
    config.find_verilog()