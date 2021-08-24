# 下载链接读取器

----

[1]: https://img.shields.io/badge/Issue-Welcome-brightgreen
[2]: https://github.com/Neurotoxin0/OpenWrt/issues/new
[3]: https://img.shields.io/badge/PRs-Welcome-brightgreen
[4]: https://github.com/Neurotoxin0/OpenWrt/pulls

[![欢迎发Issue][1]][2]
[![欢迎Pull Request][3]][4]
- [English Version](https://github.com/Neurotoxin0/Download_Link_Reader/blob/main/README_EN.md "English Version")

----

#### 一个可以从脚本所在目录的txt中寻找下载链接的Python程序
- 目前支持并通过测试的功能
    * 自动解压脚本所在目录以及子目录下单层压缩的ZIP压缩包
    * 遍历脚本所在目录以及子目录下的文件
    * 输出所有下载链接到output.txt
    * 去除输出文件中多余的空行
    * 忽略列表：指定需要忽略的文件夹，文件名以及文件内容
    * 输出文件中使用时间戳分割
    * 计数器：处理的文件数量 + 找到的链接数量
    * 支持处理带中文的文件(UTF-8)
    * 详细的日志：压缩包和文件被处理或忽略
    * 加入完整命令行
    * 语言选项: 中&英
    * 自动归档处理完成的文件
    * 添加 RAR 文件支持 (需要手动安装RAR包至Python)

----

#### 脚本样张:
![主菜单](Samples/Main_Menu.png)
![中文版菜单](Samples/Menj_CN.png)
![中文版日志](Samples/Log_CN.png)
![输出文件](Samples/Output.png)