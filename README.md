# 下载链接读取器 | Download_Link_Reader

----

[1]: https://img.shields.io/badge/Issue-Welcome-brightgreen
[2]: https://github.com/Neurotoxin0/OpenWrt/issues/new
[3]: https://img.shields.io/badge/PRs-Welcome-brightgreen
[4]: https://github.com/Neurotoxin0/OpenWrt/pulls

[![Issue Welcome][1]][2]
[![PRs Welcome][3]][4]

----

#### 一个可以从脚本所在目录的txt中寻找下载链接的Python程序
#### A Python script that reads all txt files in current dir to looking for downloadable links

- 目前支持并通过测试的功能 | Supported & Tested Features: 
    * 自动解压脚本所在目录以及子目录下单层压缩的ZIP压缩包 | Auto unzip single-zipped "zip" file in working dir and its sub dirs
    * 遍历脚本所在目录以及子目录下的文件 | Walkthrough dirs and sub-dirs in working dir
    * 输出所有下载链接到output.txt | Write all links found into output.txt
    * 去除输出文件中多余的空行 | Strip empty line from the output file
    * 忽略列表：指定需要忽略的文件夹，文件名以及文件内容 | Ignore list: ignore certain dirs, file names ,and specific contents
    * 输出文件中使用时间戳分割 | Use time stamp to separate each run
    * 计数器：处理的文件数量 + 找到的链接数量 | Counter: processed file + links found
    * 支持处理带中文的文件(UTF-8) | Add support for files with Chinese character(UTF-8)
    * 详细的日志：压缩包和文件被处理或忽略 | Detailed Log on which zip files and txt files were processed or ignore

