# Sudoku
This is a simple game about Sudoku 



# 基本背景：
1. 以前就很喜欢玩数独，突发奇想，搞了这个数独小游戏
2. 使用tkinter制作简易页面，主要基于GPT生成基础代码（其实GPT给的代码跑不起来，需要调整，但也节省了很多时间成本）
```
给GPT的语料提示词

帮我使用tkinter 制作一个数独的小游戏
1. 点击按钮，可以生成数独题目，
2. 点击按钮，可以显示数独题目的完整的答案，用红色字体显示
3. 点击按钮，可以隐藏数独题目的答案，
```
3. 回溯+递归，生成数独题目


# 基本结构
main.py：主程序
* LoadConfig类：配置文件读取类，读取一些配置文件里的数据
* DataCalculation类：数独的计算类，包含了基本的数据校验，数独生成，回溯算法
* SudokuGame类： 界面相关类， 主要是界面操作 和 数据互动

config.py：配置文件
```
1. 待填的数据 最小个数 到 最大个数 之间的一个随机值。回溯算法，理论生成的数独，都有一个唯一解
blank_min_num = 30
blank_max_num = 40
2. 界面宽度，高度，单元格字体大小，偏移量（比例尽量合适）
width = 650
height = 650
font_size = 26
font_padding = 30
 ```

# 运行与打包
## 1. 运行命令
项目全是使用python3 的基础库，使用python3环境 可以直接运行
> python main.py

## 2. 打包exe
可以使用pyinstaller第三方库，打包成exe文件，免去他人未安装环境无法运行的短处
安装环境
> pip install pyinstaller

相对路径下，执行命令：
> pyinstaller -F -w -i icon.ico main.py

相关参数，简单介绍
-F 代码打包都集成到一个文件 -w 无控制台 -i 图标

在dist目录下，生成main.exe文件

# 运行效果
简单演示一下功能
![Alt Text](./result.gif)