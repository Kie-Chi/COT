# co_test_builder数据生成器思路汇总
[toc]

## 前言

## 单元数据生成器(Unit Test)
## 转发暂停数据生成器(Random Test)
## 异常数据生成器(Exc Test)
- `Ov`异常
  - **是否处于延时槽**
  - 一个使用极端数据，一个恰好令其溢出
  - 涉及指令`add`,`sub`,`addi`
- `PC`异常
  - 这里没有归入`AdEL`异常测试
  - 使用jr测试 
- `AdEL`异常与`AdES`异常
  - **是否处于延时槽**
  - 地址不对齐(lw, sw, lh, sh)
  - 地址异常(load, store)
  - 地址对于指令非法(lb, lh, sb, sh ,sw)
  - 
- `RI`异常
  - **是否处于延时槽**
  - 无法与mars对拍了，进入和队友对拍的环节
## 中断数据生成器(Int Test)