# 移动完成文件到 archive
# process 忽略 archive 文件夹
# 融合unzip, process, etc.
# 输出log
# 保存配置
# finished:


import os

if __name__ == '__main__':
    while True:
        os.system('cls')
        
        print("\
选择语言 | Select Language: \n\
    1\t中文\n\
    2\tEnglish\n\
    3\t退出 | Exit\n\
            ")
        
        cmd = input(">")
        
        if cmd == "1":
            import Read_Files_CN
            Read_Files_CN.CLI()
            break
        elif cmd == "2":
            import Read_Files_EN
            Read_Files_EN.CLI()
            break
        elif cmd == "3":
            break
        else:
            print("\n-------------------------\n无效选项 | Invalid Command", end = '')
            input("按任意键来返回 | Press Any Key To Go Back")
        
        