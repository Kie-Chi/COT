# co_test_builder
- logisim和反汇编文件塞不进去了！！
[toc]

## 前言
- 此测评机专门用于北航计组P3~P7的实验自动测评
- 更新日志
  - [x] 单周期数据构造
  - [x] P3对拍
  - [x] P4对拍
  - [x] 流水线数据构造
  - [x] P5对拍
  - [x] P6对拍
  - [x] P7数据构造
  - [x] P7对拍
  - [ ] 多进程加速
  - [ ] 网络API
---
## <font color = red>模式</font>
- 默认模式`norm`
- 模式`lazy-mode`
  - 懒惰模式开启后，只允许采取标准的`P3~P7`的测评配置，对于测评文件夹等等等等，将由测评机自动搜索返回，所以第一次开启会很慢（后面会想办法加快的），后续将自动读取第一次的配置，如果你希望重置懒惰模式的配置，请手动删除configs文件夹中的相应文件，例如`__default_p3.json`
  - 由于本测评机致力于自定义配置，导致有许多配置需要正确配置，为此此次更新增加了`lazy-mode`
    - 开启方式一：在`file_config.json`或者你的第一个配置文件中加入`lazy-mode: true`，测评机将忽略所有的配置直接进入懒惰模式
    - 开启方式二：在测评机开始询问`Option about source`时，`lazy`作为隐藏关键词（毕竟你都进入下面了还需要什么懒惰模式），输入`lazy`测评机进入懒惰模式
  - **开启懒模式**，你将不能选择测试的种类(unit、random。。。)，但是仍然可以选择比较的对象，懒模式将把当前cpu可以执行的所有测试都依次执行，所以确实不需要选择测试种类了
## 功能
```
  Option about source:
    with Mars(default)
    with Others(only when you have several cpus)
    exit(default)
    view config(default)
    cscore(Easter egg!!!)
    lazy(new !!!)

  Option about method:
    unit test(default)
    random test(default)
    self test(only when you have self-test utils)
    exc test(only when you set is_exc on)
    exit(default)
    back to last select(default)
```
- 对拍
  - 支持多`.circ`文件同时与`Mars`对拍
  - 支持多个`.circ`文件互相对拍(**仅在检测cpu有多个时开放**)
  - 支持多个`.v`项目同时与`Mars`对拍
  - 支持多个`.v`项目互相对拍(**仅在检测cpu有多个时开放**)
- 数据
  - 支持单元化测试(`unit test`)
    - 单周期目前已完备
    - 流水线预计可找出控制单元与数据通路的bug，暂无法找出与冲突单元有关的bug
  - 支持随机指令测试(`random test`)
    - 在P7以前可以测试转发暂停
    - P7可以测试转发暂停、异常、中断
  - 支持内部异常测试(`exc test`)
    - 对于异常中断的测试测评机单独开放一个测试环节共使用
    - **仅在设置属性`exc`为`true`时开放**
  - 支持外部中断测试(`int test`)
    - **仅在设置属性`exc`为`true`时开放**
  - 支持定制化测试(`self test`)
    - 使用者提供数据生成器测试
    - 使用者提供数据(asm，或16进制码，**测试点**)测试
    - **请保证您提供的数据是可行的**
    - **仅在正确设置属性`self_dir`或者`self_util`时开放**

  - **Attention**(<font color =red>更新</font>)：关于测试点的加载测试，主要针对异常与中断测试，需要遵循如下规则
    - 若只包含一个asm源码，请包含异常处理程序在内（**请以nop的方式填补空缺，而非.ktext**）
    - 可以将测试代码与异常处理程序分开，异常处理程序请包含关键词**handler**
    - 可以不包含tb，如果想要用tb进行中断测试请加入.v文件，命名无要求
    ```
      |- self
        |- testcode1
          |- a.asm
          |- the_handler.asm
          |- mytb.v
        |- btest.asm
        |- code.txt
        |- ...
        
    ```
  - **Attention**:如果你希望加载数据生成器请确保它是`exe` `jar` `py`中的一种，如果是`jar`或者`py`请确保你已经有`java`或者`python`环境变量
    运行程序直接输出你构造的数据
    ```py
      # 构造数据
      for mips in mips_code:
        ...
        print(mips)
    ```
    ```c
      char mips[400][40] = {0};
      //你的数据生成逻辑
      for(int i = 0; i < 400; i++) {
        printf("%s\n", mips[i]);
      }
    ```
---
## 使用
### 环境
- 可以使用的环境
  - 测试P3可以在`Windows`或者`Linux`环境下使用
  - 测试P4及以上目前可以在配有`ISE`的`Windows`下正常运行，对于`Linux`请按照如下步骤配置，以**课程组虚拟机为例**，请初步了解`mips.prj`里面写的内容
  - `mips.prj`(请包含自己的testbench文件)
    ```
      Verilog work "需要编译的文件路径"
      Verilog work "需要编译的文件路径"
      ......

      eg. ALU.v 与 mips.prj在同一目录下
      Verilog work "ALU.v"
    ```
  - 在当前目录开始运行指令  
    - 第一步大概是没问题的，运行如下指令
    ```bash
      /opt/Xilinx/14.7/ISE_DS/ISE/bin/lin64/fuse -nodebug -prj mips.prj -o mips.exe mips_tb
    ```
    - 第二步会出现一些配置问题，运行如下指令
    ```bash
      isim/mips.exe.isim/mips.exe
    ```
      - 问题1：如果有`**.so not find`类似错误，请找到`/opt/Xilinx/14.7/ISE_DS/ISE/lib/lin64`或者`/opt/Xilinx/14.7/ISE_DS/ISE/lib/lin64`查找里面是否有所需要的动态链接库，接着将此路径添加至用户或者系统变量中，请注意使用的`mips.exe`并不是当前目录的，而是`isim/mips.exe.isim/mips.exe`那里才是真的的isim窗口，但是**我们最终使用的是本目录下的mips.exe**
        ```bash
          # 使用ldd isim/mips.exe.isim/mips.exe观察是否还有动态库未链接
          # 使用下方命令可以在当前终端加入动态库路径，永久添加途径请上百度
          export LD_LIBRARY_PATH=$LD_LABRARY_PATH:/opt/Xilinx/14.7/ISE_DS/ISE/lib/lin64
        ```
      - 问题2：如果有`XILINX environment variable is not set or empty`
        ``` bash
          # 请将/opt/Xilinx/14.7/ISE_DS/ISE添加环境变量
          # 使用下方指令可以在当前终端加入临时环境变量，永久添加途径请上百度
          export XILINX=$XILINX=:/opt/Xilinx/14.7/ISE_DS/ISE
        ```
    - 运行指令
      ```bash
          ./mips.exe


          # 期望结果
          # ...什么一堆输出信息，然后
          isim > 
      ```
    
### <font color = red>配置(更新)</font>
- **懒惰模式下不需要除`lazy-mode`外任何其他配置！！！**
- 在使用本测评机前请保证你已经修改了相应的参数
- 打开`Config`文件夹下的配置文件，测评机器**默认读取**`file_config.json`。如没有，测评机只读取**第一个文件配置**
- 请优先设置如下几个参数
  - type
  - tb
  - flow
  - exc
- 测评机会根据上述内容确定你的测评类型，**自动提示你补全需要的所有的参数**
  - `P3/P4/P5/P6/P7`：代表标准测试内容
  - `??`：非标准测试内容，例如不使用测评机提供tb文件、logisim流水线cpu等等，会提示Warning
  - `XX`：错误测试类型，你填写的内容之间矛盾测评机提示你更改
  ```json
    //需要使用的测评机版本"logisim"、"verilog"
    "type": "verilog",

    //0 -> 不需要测评机为你添加tb文件，请确保为mips_tb
    //1 -> 正常tb文件，可以在util文件夹下查看内容或者更改，可以在P4、P5使用
    //2 -> 官方tb文件，课程组提供的接口，可以在P6使用
    //3 -> 官方tb文件，课程组提供的接口，可以在P7使用(仅仅内部异常)
    //4 -> 官方tb文件，课程组提供的接口，可以在P7使用(内部异常和外部中断)
    "tb": 2,

    //是否是流水线CPU，意味着支持logisim-flow
    "flow": true,

    //是否支持中断异常
    "exc": true,

    //你的ISE路径
    "xilinx_path": "D:\\Xilinx\\14.7\\ISE_DS\\ISE",

    //logisimCPU文件存放文件夹，默认在测评机目录下的circ
    "circ_dir": "circ",

    //verilogCPU文件存放文件夹，默认在测评机目录下的verilog
    "verilog_dir": "verilog",

    //定制测试中你需要提供的数据生成器的exe文件(非必需)
    "self_util": "util\\testcodeplus.exe",

    //定制测试中你存放数据的文件夹，请保证全是asm或者txt文件(非必需)
    "self_dir": "self",

    //你希望测评机测试的指令集，下面已经是目前能够提供的最大指令集
    //不用包含和异常相关指令，但是进行异常测试前请确保你实现了以下指令
    //mtc0, mfc0, eret, syscall
    "mips_set": ["add", "sub", "and", "or", "slt", "sltu", "ori", "addi", "andi", "lui", "sw", "sb", "sh", "lw", "lb", "lh","beq",
        "bne","mult", "multu", "div", "divu", "mfhi", "mflo", "mthi", "mtlo", "jal", "jr", "nop"]
    //random和self测试生成的文件数，使用unit、exe、int测试时不会生效，请提前设置好！！！
    "test_times": 3
  ```

### 各文件介绍
- `circ`
  - 标准格式
    ```
    |- circ
      |- a.circ
      |- b.circ
      |- ...
    ```
  - 默认存放需要对拍的`.circ`程序
    - **测评机不会对此文件夹内的文件进行更改，请放心使用**
    - 与`Mars`对拍中，会将此文件夹下所有文件都与`Mars`对拍
    - 同理，该文件夹下可以放置需要互相对拍的程序
- `verilog`
  - **请注意**不要在此文件夹下放入同名嵌套的文件夹（尽量不要嵌套，如果嵌套请不要同名），**测评机**将此目录下所有第一级的子文件夹识别为CPU项目
  - 标准格式
    ```
    |- verilog
      |- cpu1
        |- *.v
        |- ...其他文件或目录
      |- cpu2
      |- cpu3
      |- ...不能是目录
    ```
  - 错误格式
    ```
    |- verilog
      |- cpu
        |- cpu
          |- ALU.v
          |- GRF.v
          ...
    ```
  - 默认存放需要对怕的`.v`项目
    - **无需进行清洗，可以直接将ISE项目复制过来，测评机会自动选出所有的.v文件**，嫌麻烦甚至可以链接到你的ISE项目作为测评文件夹，**测评机不会对此文件夹内的文件进行更改，请放心使用**
    - 与`mars`对拍时，文件夹下的每一个子文件夹作为一个CPU项目测评
    - 相互对拍也同理
- `util`
  - 工具包，里面有各种测评机运行的工具
  - **请确保他们都在！！！！**
  - mars.jar
  - ~~logisim改版（为了压缩可能删了）~~
  - test_main.txt
  - dissam.exe（tsxb提供的反汇编器）
  - mips_tb_1.v
  - mips_tb_2.v
  - mips_tb_3.v
  - mips_tb_4.v
  - handler.asm
  - ~~可能还有我找到的学长的数据生成器，看起来效果还行~~
- `DataMaker.py`
  - 生成单元测试数据
    - 通过对某一类指令强数据测试达到目的
    - 使用已测试过的指令测试，所以需要按照顺序单元测试
    - 可以对单周期完备测试、对流水线数据通路测试
  - 生成随机测试数据
    - **根据测评需求进行随机测试，可包含异常与中断**
    - 枚举指令序列进行转发暂停测试
    - 某些极度奇怪的转发无法测试例如
      - `lw -> jr` `slt -> jr` `sltu -> jr`
  - 生成异常中断测试
- `Runner.py`
  - 下辖三个类`Runner`、`LogisimRunner`、`XilinxRunner`是测评机的运行类
  - 提供加强的os函数，可在`Linux`与`Windows`上流畅运行
  - 自动化运行`Mars`、`logisim`程序、`verilog`项目生成输出文件
- `Config.py`
  - 处理测评配置问题，尽可能简化用户需要配置的内容（）
- `Machine.py`
  - `Machine`类是测评机类，执行交互
  - 同上一代，自动生成测评文件夹
  - 如果没有发生错误将会自动清理测评文件夹
  - 如果出现bug，将会留下出现bug的一部分提供给使用者
- `start.py`
  - 测评机主体文件，运行此文件即可
---
### 运行时文件夹(<font color = red>更新</font>)
- 如果你的CPU们在运行是发生错误，你将会得到一个测评文件夹，大致目录如下
```
  |- year-month-day-time-src-mtd
    |- testcode1
    |- testcode2
    |-...

  //选择与mars对拍
    |- testcode1
      |- cpu1
        |- dif.log
        |- out.txt
        |- stdout.txt
      |- cpu2
      |- ...
      |- code.asm
      |- code.txt
      |- (tb.v)

  //选择互相对拍
    |- testcode1
      |- cpu1-cpu2
        |- dif.log
        |- cpu1-out.txt
        |- cpu2-out.txt
      |- cpu1-cpu3
      |- ...
      |- code.asm
      |- code.txt
      |- (tb.v)
```
- 测评文件夹下每一个第一级目录可以认为是一个测试点
- code.asm
  - 测试点使用的mips源码
- code.txt
  - 测试点使用的十六进制码
  - 一定会填满4096条指令，防止读取未定义部分！！！
- tb.v
  - 如果使用了**中断测试**，可能会有单独的tb文件，可供复现bug
- out.txt
  - 当前cpu输出的结果
- stdout.txt
  - mars输出的标准结果
- dif.log
  - CPU与mars的差异或者CPU们的差异
  - 第一行错误将指认为out.txt与stdout.txt中输出差异即753行
  - 随后指出是哪一个指令执行有问题，并给出该指令在code.asm中的位置即1290行
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