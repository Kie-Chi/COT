import json
import subprocess
import time
import sys
from dateutil.relativedelta import relativedelta
import numpy as np
import logging
from datetime import datetime
import os
from Printer import Printer
import curses

class Gift:
    def __init__(self):
        self.log = None
        self.__get_log()
        self.printer = Printer()

    def __get_log(self):
        hidden_folder = ""
        if os.name == str("nt"):
            hidden_folder = os.path.join(os.environ['LOCALAPPDATA'], ".COT")
        else:
            hidden_folder = os.path.join(os.environ['HOME'], ".COT")
        self.log = json.load(open(os.path.join(hidden_folder, "log.json"), "r", encoding="utf-8"))
        # print(self.log)

    def gift(self):
        func_list = [
            "introduction",
            "max_cpu_time",
            "first",
            "ak_total",
            "time_total",
            "max_day",
            "conclude"
        ]
        self.printer.class_start(self, *func_list)

    def introduction(self, printer):
        printer.pre_print()
        printer.print_out(" Hi~ 我是COT！")
        printer.pre_print()
        printer.print_out(" 首先祝贺你通过了我设下的所有考验qaq，想必你已经顺利通关计算机组成了！(没有也快了)")
        printer.pre_print()
        printer.print_out(" 为了庆祝(提前庆祝)你的成功，我专门为你准备了一份礼物")
        printer.stop()

    def max_cpu_time(self, printer):
        cpu_model = None
        if os.name != str('nt'):
            cpu_info = '/proc/cpuinfo'
            try:
                with open(cpu_info, 'r') as file:
                    for line in file:
                        if line.startswith('model name'):
                            cpu_model = line.split(':')[1].strip()
            except FileNotFoundError:
                printer.stop()
        else:
            result = subprocess.run("wmic cpu get name", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            cpu_info = result.stdout
            cpu_model = cpu_info.strip().replace('\n', ' ').replace('\r', ' ').split(" ")
            cpu_model = cpu_model[-1]
        
        if cpu_model != None:
            log = self.log["log"][0]["log"]
            max_time = -1
            max_time_type = None
            for block in log:
                # Printer.print_out(stdscr, block)
                if block["time"] > max_time:
                    max_time = block["time"]
                    max_time_type = block["type"]
            printer.pre_print()
            printer.print_out(f" 你的电脑在对{max_time_type}进行测试时运行了{max_time}秒")
            printer.pre_print()
            printer.print_out(' 看起来你的', end="")
            printer.print_out(f'{cpu_model}', "red", end="")
            printer.print_out('被你搭建的cpu折磨惨了')
            printer.stop()


    def first(self, printer):
        first = self.log["max"]["first"]
        month = first["stamp"].split("-")[1]
        dalta = datetime.strptime(first["stamp"].split(" ")[1], "%H:%M:%S")
        _type = first["type"] if first["type"] != "??" else "??(你猜是什么呀)"
        # print(first)
        printer.pre_print()
        printer.print_out(" 还记得我们第一次相遇吗？")
        said = ""
        timenow = datetime.now()
        firstday = datetime.strptime(first["stamp"], "%Y-%m-%d %H:%M:%S")
        dif = timenow - firstday
        # printer.pre_print()
        # if dif.days != 0:
        #     printer.print_out(f"{dif.days}天前，我们第一次相遇")
        # else:
        #     Printer.pre_print(stdscrf"就在今天，我们第一次相遇")
        if int(dalta.hour) < 3:
            said = "凌晨"
        elif int(dalta.hour) < 7:
            said = "清晨"
        elif int(dalta.hour) < 11:
            said = "上午"
        elif int(dalta.hour) < 13:
            said = "晌午"
        elif int(dalta.hour) < 17:
            said = "下午"
        elif int(dalta.hour) < 19:
            said = "傍晚"
        elif int(dalta.hour) < 23:
            said = "晚上"
        else:
            said = "深夜"

        season = ""
        month = int(month)
        if month == 1:
            season = "晚冬"
        elif month == 2:
            season = "隆冬"
        elif month == 3:
            season = "早春"
        elif month == 4:
            season = "仲春"
        elif month == 5:
            season = "暮春"
        elif month == 6:
            season = "长夏"
        elif month == 7:
            season = "仲夏"
        elif month == 8:
            season = "夏末"
        elif month == 9:
            season = "初秋"
        elif month == 10:
            season = "金秋"
        elif month == 11:
            season = "深秋"
        elif month == 12:
            season = "寒冬"
        printer.pre_print()
        printer.print_out(f" 那是{season}的一个{said}，你第一次成功启动了COT完成了测评，",end="")
        dif = relativedelta(timenow, firstday)
        said = ""
        if dif.days == 0 and dif.months == 0 and dif.years == 0:
            if dif.hours != 0:
                said = f"{dif.hours}小时"
            if dif.minutes != 0:
                said += f"{dif.minutes}分钟"
        else:
            if dif.years != 0:
                said = f"{dif.years}年"
            if dif.months != 0:
                said += f"{dif.months}月"
            if dif.days != 0:
                said += f"{dif.days}天"
        printer.print_out(f"距现在已有", end="")
        printer.print_out(said, "blue")
        printer.pre_print()
        said = ""
        if first["status"] == 1:
            said = '第一次就成功了，真棒！'
        elif first["pass"]/first["times"] >= 0.8:
            said = f'第一次就通过了超过{round(100*(first["pass"]/first["times"]))}%的测试点，棒棒哒！'
        else:
            said = f"虽然结果不是那么好，但没有人能保证一遍过不debug，只要课上不debug都好说呀！"
        printer.print_out(f" 我还记得你当时测评的是{_type}，{said}")
        printer.pre_print()
        printer.print_out(f" 那天我们度过了第一个", end="")
        printer.print_out(f"{first['time']}秒", "blue", end="")
        printer.print_out("，是不是觉得有点煎熬hhh，不过肯定没有课上等待的煎熬(doge)")
        printer.stop()

    def ak_total(self, printer):
        total = self.log["total"]
        aks = self.log["aks"]
        timenow = datetime.now()
        firstday = datetime.strptime(self.log["max"]["first"]["stamp"], "%Y-%m-%d %H:%M:%S")
        dif_days = timenow - firstday
        dif = relativedelta(timenow, firstday)
        said = ""
        if dif_days.days == 0:
            if dif.hours != 0:
                said = f"{dif.hours}小时"
            if dif.minutes != 0:
                said += f"{dif.minutes}分钟"
        else:
            said = f"{dif_days.days}天"
        printer.pre_print()
        printer.print_out(f" 在这{said}中，你一共测试了", end="")
        printer.print_out(f"{total['use']}次", "red", end="")
        printer.print_out("CPU")
        printer.pre_print()
        rate = total["ak"]/total["use"]
        rate = round(100 * rate, 2)
        color = 97
        if total["ak"] == total["use"]:
            said = ["AK率达到","！！！无敌，CO不败者！！！"]
            color = "green"
        elif rate >= 90:
            said = ["AK率高达","，嘻嘻，CPU搭得很好啊"]
            color = "green"
        elif rate >= 80:
            said = ["AK率达到","以上，棒棒的呀"]
            color = "yellow"
        else:
            said = ["AK率达到","，继续加油哦"]
            color = "red"
        printer.print_out(" AK了",end="")
        printer.print_out(f"{total['ak']}次", "red", end="")
        printer.print_out("，",end="")
        printer.print_out(said[0], end="")
        printer.print_out(f"{rate}%", color, end="")
        printer.print_out(said[1])
        if [ak for ak in aks.keys() if aks[ak] != 0] != []:
            printer.pre_print()
            printer.print_out(" 其中，", end="")
            for ak in [ak for ak in aks.keys() if aks[ak] != 0] :
                printer.print_out(f"{ak}一共AK了", end="")
                printer.print_out(f"{aks[ak]}次", "red", end="")
                printer.print_out("，", end="")
            biggest = "??"
            for ak in aks.keys():
                if aks[ak] >= aks[biggest]:
                    biggest = ak
            printer.print_out(f"看来你真的很喜欢{biggest}呢!")
        printer.stop()

    def time_total(self, printer):
        total = self.log["total"]
        timenow = datetime.now()
        firstday = datetime.strptime(self.log["max"]["first"]["stamp"], "%Y-%m-%d %H:%M:%S")
        dif_days = timenow - firstday
        choice = np.random.randint(0, 10)
        said = ""
        num = 0
        if choice == 0:
            said = ["如同看了","流星雨"]
            num = f"{round(total['time']/16)}场"
        elif choice == 1:
            said = ["如同晚风掠过",""]
            num = f"{round(total['time']/13.3)}人"
        elif choice == 2:
            said = ["如同看来","烟花"]
            num = f"{round(total['time']/35)}场"
        elif choice == 3:
            said = ["如同雪花飘落",""]
            num = f"{round(total['time']/1.5)}米"
        elif choice == 4:
            said = ["如同鱼儿吐了","泡泡"]
            num = f"{round(total['time']/604)}次"
        elif choice == 5:
            said = ["如同蝴蝶振翅",""]
            num = f"{round(total['time'] * 2)}次"
        elif choice == 6:
            said = ["如同樱花绽放",""]
            num = f"{round(total['time']/11.25)}次"
        elif choice == 7:
            said = ["如同看了","日出"]
            num = f"{round(total['time']/80)}次"
        elif choice == 8:
            said = ["如同风筝飞翔",""]
            num = f"{round(total['time']/6.6)}米"
        elif choice == 9:
            said = ["如同花香飘过","街"]
            num = f"{round(total['time']/8.5)}条"
        printer.pre_print()
        printer.print_out(f" 在COT存在以来的{dif_days.seconds + dif_days.days * 24 * 3600}秒内，有", end="")
        printer.print_out(f"{total['time']}秒", "blue", end="")
        printer.print_out("在陪伴你进步")
        printer.pre_print()
        printer.print_out(" "+said[0], end="")
        printer.print_out(num, "red", end="")
        printer.print_out(said[1])
        printer.pre_print()
        printer.print_out(f" 占据你生命从{firstday.year}年{firstday.month}月{firstday.day}日{firstday.hour}点{firstday.minute}分到现在的", end="")
        rate = round(100*(total['time']/(dif_days.seconds + dif_days.days * 24 * 3600)), 10)
        color = 97
        if rate >= 36.2:
            said = "超过了你用来睡觉的时间"
            color = "green"
        elif rate >= 14.7:
            said = "超过了你用来工作学习的时间"
            color = "green"
        elif rate >= 11:
            said = "超过了你用来陪伴手机的时间"
            color = "yellow"
        elif rate >= 5.6:
            said = "超过了你用来吃饭喝水的时间"
            color = "yellow"
        elif rate >= 3:
            said = "超过了你用来梳妆打扮的时间"
            color = "red"
        elif rate >= 1:
            said = "超过了你用来通勤的时间"
            color = "red"
        else:
            said = "虽然不多但是依旧是我生命中宝贵的一部分"
            color = "red"
        printer.print_out(f"{rate}%", color, end="")
        printer.print_out("，"+said)
        printer.stop()

    def max_day(self, printer):
        max_day = self.log["max"]["max@day"]
        day_log = ""
        for log in self.log["log"]:
            if log["stamp"] == max_day:
                day_log = log
                break
        max_day = datetime.strptime(max_day, "%Y-%m-%d")
        printer.pre_print()
        printer.print_out(f" {max_day.year}年{max_day.month}月{max_day.day}日", "blue", end="")
        printer.print_out("，那天你又在想什么呢？")
        printer.pre_print()
        printer.print_out(f" 你启动了", end="")
        printer.print_out(f"{day_log['total']['use']}次", "red", end="")
        printer.print_out("COT，花费了", end="")
        seconds = day_log['total']['time']
        hours = seconds // 3600  # 1小时 = 3600秒
        minutes = (seconds % 3600) // 60  # 剩余的分钟
        remaining_seconds = seconds % 60  # 剩余的秒数
        said = ""
        if hours != 0:
            said = f"{hours}小时"
        if minutes != 0:
            said += f"{minutes}分"
        if remaining_seconds != 0:
            said += f"{remaining_seconds}秒"
        printer.print_out(said, "blue", end="")
        printer.print_out("创造了", end="")
        printer.print_out(f"{day_log['total']['times']}个", "red", end="")
        printer.print_out("测试点")
        printer.pre_print()
        if day_log['total']['pass'] == day_log['total']['times']:
            printer.print_out(" 看起来你对自己的CPU不是很有自信呀，要相信自己！")
        elif day_log['total']['pass'] / day_log['total']['times'] >= 0.98:
            printer.print_out(" 看起来是在寻找一些什么刁钻的bug，不知道COT是否有帮助到你。")
        else:
            printer.print_out(" 看起来是在对自己的CPU进行覆盖测试，包在我身上了！")
        printer.stop()

    def conclude(self, printer):

        printer.pre_print()
        printer.print_out(" 请允许我献上最真挚的祝福")
        printer.pre_print()
        printer.print_out(" 希君生羽翼，一化")
        printer.pre_print()  
        printer.print_out(" WARNING: NO BATTERY!","red", delay=0)
        time.sleep(.5)
        printer.pre_print()
        printer.print_out(" WARNING: NO BATTERY!","red", delay=0)
        time.sleep(.5)
        printer.pre_print()  
        printer.print_out(" WARNING: NO BATTERY!","red", delay=0)
        time.sleep(.5)
        printer.end()
if __name__ == "__main__":
    gift = Gift()
    gift.gift()
