# co_test_builder
- 测评机带着util工具下的`logisim.jar`交不上去，所以去除了这个包:sob:
## 前言
- 此测评机专门用于北航计组P3~P6的实验自动测评
- 更新日志
  - [x] 单周期数据构造
  - [x] P3对拍
  - [x] P4对拍
  - [x] 流水线数据构造
  - [x] P5对拍
  - [x] P6对拍
---
## 功能
- 对拍
  - 支持多`.circ`文件同时与`Mars`对拍
  - 支持多个`.circ`文件互相对拍
  - 支持多个`.v`项目同时与`Mars`对拍
  - 支持多个`.v`项目互相对拍
- 数据
  - 支持单元化测试
    - 单周期目前已完备
    - 流水线预计可找出控制单元与数据通路的bug，暂无法找出与冲突单元有关的bug
  - 支持随机指令测试
    - `load/store`类、`branch`类、`jump`类指令由代码块的方式给出，不易出现bug
    - 死循环测试(目前仅支持beq死循环)
  - 支持定制化测试
    - 使用者提供数据生成器测试
    - 使用者提供数据(asm，或16进制码)测试
    - **请保证您提供的数据是可行的，本测评机目前没有设置防止Mars卡死的措施**
---
## 使用
### 环境
- 要求Python环境(尽量3.9以上吧但是不需要最新)，需要安装`numpy`
- 由于想要将单周期和流水线的强数据全部统一构造出来，耽误了很多时间也没有完成流水线的数据构造，所以目前只有源码可以直接使用（没有时间pyinstaller）
- 可以使用的环境
  - 测试P3可以在`Windows`或者`Linux`环境下使用
  - 测试P4及以上目前可以在配有`ISE`的`Windows`下正常运行，对于`Linux`环境，请配置好动态链接库以及环境变量，确保在终端可以运行如下指令得到结果
  ```bash
    /opt/Xilinx/14.7/ISE_DS/ISE/bin/lin64/fuse -nodebug -prj mips.prj -o mips.exe mips_tb
  ```
  ```bash
    ./mips.exe -nolog -tclbatch mips.tcl > output.txt
    # 经笔者检验，课程组虚拟机配置相当清澈，没有与ISE命令行相关的配置

    # 如果有...so not find类似错误，请找到/opt/Xilinx/14.7/ISE_DS/ISE/lib/lin64或者/opt/Xilinx/14.7/ISE_DS/ISE/lib/lin64查找里面是否有所需要的动态链接库，接着将此路径添加至用户或者系统变量中
    # 使用ldd mips.exe观察是否还有动态库未链接

    # 如果有Xilinx environment variable is not set or empty
    # 请将/opt/Xilinx/14.7/ISE_DS添加环境变量
    
    # 因为笔者莫名将动态库路径和环境变量配的一团糟，导致虚拟机输入账号密码也没法开机了，所以已有经验到此中断
    # 若需要在Linux上运行虚拟机，只要保证上述两条指令可正常运行得到输出即可
  ```
### <font color = red>配置</font>
- 在使用本测评机前请保证你已经修改了相应的参数
- 打开`Config`文件夹下的配置文件，如有多个，测评机只读取第一个文件配置
  ```json
    //需要使用的测评机版本"logisim"、"verilog"
    "type": "verilog",

    //是否是流水线CPU，意味着支持logisim-flow
    "is_flow": true,

    //你的ISE路径
    "xilinx_path": "D:\\Xilinx\\14.7\\ISE_DS\\ISE",

    //你需要使用的logisim路径，默认已经配置好windows
    "logisim_path": "util\\logisim-generic-2.7.1.jar",

    //你需要使用的魔改mars路径，请不要改动，使用测评机自带的即可
    "mars_path": "util\\mars.jar",

    //logisimCPU文件存放文件夹，默认在测评机目录下的circ
    "circ_dir": "circ",

    //verilogCPU文件存放文件夹，默认在测评机目录下的verilog
    "verilog_dir": "verilog",

    //定制测试中你需要提供的数据生成器的exe文件
    "self_util": "util\\testcodeplus.exe",

    //定制测试中你存放数据的文件夹，请保证全是asm或者txt文件
    "self_dir": "self",

    //你希望测评机测试的指令集，下面已经是目前能够提供的最大指令集
    "random_set": {
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
    },

    //单元测试的指令集，是根据上方分类，所以请优先设置好random_set
    "unit_set": {
        "set_test": ["cal_i", "lui", "mt", "mf"],
        "arth_test": ["cal_r", "md"],
        "mem_test": ["store", "load"],
        "branch_test": ["branch"],
        "jump_test": ["j_l", "j_r"]
    },

    //0 -> 不需要测评机为你添加tb文件，请确保为mips_tb
    //1 -> 正常tb文件，可以在util文件夹下查看内容或者更改，可以在P4、P5使用
    //2 -> 官方tb文件，课程组提供的接口，可以在P6使用
    "tb": 2,

    //random测试生成的文件数，使用unit测试时不会生效，请提前设置好！！！
    "test_times": 3
  ```
- 目前测评机默认为测试P6环境
- 请重点关注如下几个参数，如果没有配置正确，将影响测评机启动
  - `type`
  - `is_flow`
  - `xlinx_path`
  - `random_test` `unit_set`
  - `tb`

### 各文件介绍
- `circ`
  - 默认存放需要对拍的`.circ`程序
    - **测评机不会对此文件夹内的文件进行更改，请放心使用**
    - 与`Mars`对拍中，会将此文件夹下所有文件都与`Mars`对拍
    - 同理，该文件夹下可以放置需要互相对拍的程序
- `verilog`
  - 默认存放需要对怕的`.v`项目
    - **无需进行清洗，可以直接将ISE项目复制过来，测评机会自动选出所有的.v文件**，嫌麻烦甚至可以链接到你的ISE项目作为测评文件夹，**测评机不会对此文件夹内的文件进行更改，请放心使用**
    - 与`mars`对拍时，文件夹下的每一个子文件夹作为一个CPU项目测评
    - 相互对拍也同理
- `util`
  - 工具包，里面有各种测评机运行的工具
  - **请确保他们都在！！！！**
  - 魔改版的mars
  - ~~logisim改版（为了压缩可能删了）~~
  - test_main.txt
  - dissam.exe（tsxb提供的反汇编器）
  - mips_tb1.txt
  - mips_tb2.txt
  - 可能还有我找到的学长的数据生成器，看起来效果还行
- `DataMaker.py`
  - 生成单元测试数据
    - 通过对某一类指令强数据测试达到目的
    - 使用已测试过的指令测试，所以需要按照顺序单元测试
    - 可以对单周期完备测试、对流水线数据通路测试
  - 生成随机测试数据
    - 枚举指令序列进行转发暂停测试
    - 某些极度奇怪的转发无法测试例如
      - `lw -> jr` `slt -> jr` `sltu -> jr`
- `Runner.py`
  - 下辖三个类`Runner`、`LogisimRunner`、`XilinxRunner`是测评机的运行类
  - 提供加强的os函数，可在`Linux`与`Windows`上流畅运行
  - 自动化运行`Mars`、`logisim`程序、`verilog`项目生成输出文件
- `Machine.py`
  - `Machine`类是测评机类，执行交互
  - 同上一代，自动生成测评文件夹
  - 如果没有发生错误将会自动清理测评文件夹
  - 如果出现bug，将会留下出现bug的一部分提供给使用者
- `start.py`
  - 测评机主体文件，运行此文件即可
---
### 运行时文件夹
- 如果你的CPU们在运行是发生错误，你将会得到一个测评文件夹，大致目录如下
```
  |- year-month-day-time-src-mtd
    |- random/unit
    |- stdout
    |- hex
    |- log
    |- dif
```
- random/unit
  - 存放了本次生成的所有数据（.asm）
- stdout
  - 如果你和mars对拍，将会得到mars的标准输出
- hex
  - 你的数据转为的16进制码
- log
  - 你的CPU们运行后留下的日志
- dif
  - CPU与mars的差异或者CPU们的差异
  - 第一行错误将指认为log与stdout中输出差异即753行
  - 随后指出是哪一个指令执行有问题，并给出该指令在random/stdout中的位置即1290行
  - 最后给出最近一条完全一致的命令与输出
  ```log
    First error in line 753
    ------the first different Mips code "ac05000c"-----
    Mips Code: "sw $5, 12($0)" in line 1290
    Mars: "@00004044: *0000000c <= 00000044"
    wtycpu: "@00004044: *0000000c <= 00000000"
    ---------------------------------------
    the most recent same Mips code output is: "lw $5, 9($31)" in line 1289 
    the most recent same Mips code output is: "@00004040: $ 5 <= 00000044"
  ```