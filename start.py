from Machine import Machine
import Runner
import sys
import json
import os
from datetime import datetime
import time
import Serect
import traceback
class Test:
    def __init__(self):
        self.machine = None
        self.log = None
        self.running_time = 0
        self.__log = None

    def __init_log(self):
        
        _type = {
            "norm": 0,
            "lazy": 0,
            "randomTest": 0,
            "unitTest": 0,
            "excTest": 0,
            "intTest": 0,
            "selfTest": 0,
            "withMars": 0,
            "withOthers": 0,
        }
        _total = {
            "use": 0,
            "ak": 0,
            "time": 0,
            "times": 0,
            "pass": 0,
        }

        _points = {
            "P3": 0,
            "P4": 0,
            "P5": 0,
            "P6": 0,
            "P7": 0,
            "??": 0
        }

        _passes = {
            "P3": 0,
            "P4": 0,
            "P5": 0,
            "P6": 0,
            "P7": 0,
            "??": 0
        }
        _aks = {
            "P3": 0,
            "P4": 0,
            "P5": 0,
            "P6": 0,
            "P7": 0,
            "??": 0
        }
        _max = {
            "max@once": {},
            "max@day": "",
            "latest": {},
            "first": {},
        }
        self.log = {
            "type": _type,
            "total": _total,
            "points": _points,
            "passes": _passes,
            "aks": _aks,
            "max": _max,
            "log": []
        }

    def __update(self):
        self.__get_daylog()
        self.__update_log()
    
    def __update_log(self):
        test_dir = getattr(self.machine, "_Machine__test_dir", None)
        config = getattr(self.machine, "_Machine__config", None)
        lazy = getattr(config, "_Config__lazy", None)
        src = test_dir.split('-')[-2]
        mtd = test_dir.split('-')[-1]
        session = getattr(config, "session", None)
        if lazy:
            self.log["type"]["lazy"] += 1
        else:
            self.log["type"]["norm"] += 1
        self.log["type"][src] += 1
        if mtd != "lazyTest":
            self.log["type"][mtd] += 1
        
        self.log["points"][session] += self.__log["times"]
        self.log["passes"][session] += self.__log["pass"]
        self.log["aks"][session] += self.__log["status"]

        self.log["total"]["use"] += 1
        self.log["total"]["ak"] += self.__log["status"]
        self.log["total"]["time"] += self.__log["time"]
        self.log["total"]["times"] += self.__log["times"]
        self.log["total"]["pass"] += self.__log["pass"]
        
        if self.log["max"]["max@once"] == {}:
            self.log["max"]["max@once"] = self.__log
            self.log["max"]["max@day"] = self.log["log"][-1]["stamp"]
            self.log["max"]["first"] = self.__log
        else:
            if self.__log["times"] >= self.log["max"]["max@once"]["times"]:
                self.log["max"]["max@once"] = self.__log
            log = {}
            for _log in self.log["log"]:
                if _log["stamp"] == self.log["max"]["max@day"]:
                    log = _log
                    break
            if self.log["log"][-1]["total"]["times"] >= log["total"]["times"]:
                self.log["max"]["max@day"] = self.log["log"][-1]["stamp"]
        self.log["max"]["latest"] = self.__log

    def __update_daylog(self):
        self.log["log"][-1]["total"]["use"] += 1
        self.log["log"][-1]["total"]["ak"] += self.__log["status"]
        self.log["log"][-1]["total"]["time"] += self.__log["time"]
        self.log["log"][-1]["total"]["times"] += self.__log["times"]
        self.log["log"][-1]["total"]["pass"] += self.__log["pass"]
        self.log["log"][-1]["log"].append(self.__log)

    def __get_daylog(self):
        test_dir = getattr(self.machine, "_Machine__test_dir", None)
        date_stamp = "-".join(test_dir.split('-')[0:3])
        flag = False
        if self.log["log"] == []:
            flag = True
        else:
            dates = [log["stamp"] for log in self.log["log"]]
            if date_stamp not in dates:
                flag = True
        if flag:
            _total = {
                "use": 0,
                "ak": 0,
                "time": 0,
                "times": 0,
                "pass": 0,
                }
            day_info = {
                "stamp": date_stamp,
                "total": _total,
                "log": []
            }
            self.log["log"].append(day_info)
        self.__update_daylog()

    def __get_log(self):
            test_dir = getattr(self.machine, "_Machine__test_dir", None)
            time = "-".join(test_dir.split("-")[0:3]) + " " + ":".join(test_dir.split("-")[3:6])            
            test_times = getattr(self.machine, "_Machine__test_times", None)
            config = getattr(self.machine, "_Machine__config", None)
            _type = getattr(config, "session", None)
            status = 1
            _pass = test_times
            if os.path.exists(test_dir):
                status = 0
                dirs, useless = Runner.find_dirs(test_dir)
                dirs = [_dir for _dir in dirs if _dir.split(os.sep)[-2] == test_dir]
                _pass = test_times - len(dirs)
            self.__log = {
                "type": _type,
                "status": status,
                "stamp": time,
                "times": test_times,
                "pass": _pass,
                "time": self.running_time
            }
            # Runner.print_colored(self.__log)
            

    def test(self):
        self.machine = Machine()
        try:
            start = datetime.now()
            self.machine.create_test()
            self.machine.start_test()
            end = datetime.now()
            self.running_time = round((end - start).total_seconds())
            self.__get_log()
            hidden_folder = os.path.join(os.environ['LOCALAPPDATA'], ".COT")
            if not os.path.exists(hidden_folder):
                Runner.safe_makedirs(hidden_folder)
            if os.path.exists(os.path.join(hidden_folder, "log.json")):
                self.log = json.load(open(os.path.join(hidden_folder, "log.json"), "r", encoding="utf-8"))
            else:
                self.__init_log()
            self.__update()
            json.dump(self.log, open(os.path.join(hidden_folder, "log.json"), "w", encoding="utf-8"))
        except Exception as e:
            Runner.print_colored(f"Error: {type(e).__name__}\"{e}\"", 91)
            Runner.print_colored(f"Detailed Stacktree:", 91)
            Runner.print_colored(traceback.format_exc(), 91)
            test_dir = getattr(self.machine, "_Machine__test_dir", None)
            if os.path.exists(test_dir):
                Runner.safe_rmtree(test_dir, retries=10, delay=0.3)
        Runner.print_colored("Press Enter to exit...", 93, end="")
        input()
        sys.exit()
        
if __name__ == "__main__" :
    Test().test()