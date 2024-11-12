import os
import json

class Config :
    def __init__(self) :
        self.__file_config = {
            "mars_path": "/mars.jar",
            "test_path": "/test",
            "output_path": "/out",
            "input_path": ""
        }
        self.__instr_config = {
            "add": {"opcode": "000000", }
        }

    def __create_default(self, file_config) :
        print("将自动为您创建默认配置")
        try :
            os.system(f"sudo touch {file_config}")
            json.dump(self.__file_config, open(file_config, "w", encoding="utf-8"))
        except TypeError as e :
            print("生成配置文件错误")

    def all_init(self) :
        configs = "configs"
        file_config = "/configs/file_config.json"
        instr_config = "/configs/instr_config.json"

        # 获取当前目录
        current_dict = os.getcwd()
        file_config = current_dict + file_config
        instr_config = current_dict + instr_config

        # 打印验证内容
        # print(file_config)
        # print(instr_config)

        # 判断是否是文件
        if os.path.isfile(file_config) :
            try :
                self.__file_config = json.load(open(file_config, "r", encoding="utf-8"))
            except json.JSONDecodeError as e :
                self.__create_default(file_config)
        else :
            if not os.path.exists(configs) :
                os.system(f"sudo mkdir {configs}")

            sel = input("是否添加已有配置(Y/n):")
            if sel == "Y" :
                path = input("输入配置文件路径")
                os.system(f"mv {path} {file_config}")
            else :
                self.__create_default(file_config)
            

if __name__ == "__main__" :
    config = Config()
    config.all_init()
