# ephone使用说明
- ## 使用环境
1. Python3.X
2. 安装安卓SDK
3. adb套件
4. 手机正常连接且处于USB调试模式
- ## 使用说明
1. 双击main.py，（如果有其它打开py文件的编辑器，需要选中main.py后用右键使用python打开
2. 点击执行Monkey按钮，默认会同时在列表中的机器中执行对应的Monkey命令并收集日志
- ## 参数配置
1. 主目录下的config.py为配置文件
2. `packages`为包的列表，依次Monkey执行列表中的包
3. `default_entry_event_num = "500"` 此数值为Monkey的事件数
4. `default_entry_event_path = "D:\\monkeytest"` 此项为Monkey日志的存放路径
