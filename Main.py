# 待办:
# 移动完成文件到 archive
# 输出log
# 保存配置
# RAR, 7z, tar, gz支持
# finished:全局忽略 archive, __pycache__ 文件夹


import os, sys, shutil
path = (os.path.split(os.path.realpath(__file__))[0] + "/").replace("\\\\", "/").replace("\\", "/")
os.chdir(path) 


if __name__ == "__main__":
    while True:
        os.system('cls')
        
        print("\
选择语言 | Select Language: \n\
    1\t中文\n\
    2\tEnglish\n\
    3\t退出 | Exit\n\
            ")
        
        lan = input(">")

        if lan not in ["1", "2", "3", "debug"]:
            print("\n-------------------------\n无效选项 | Invalid Command", end = '')
            input("按任意键来返回 | Press Any Key To Go Back")
        else:
            if lan == "1" or lan == "2":
                import Read_Files
                Read_Files.CLI(int(lan) - 1)
                
                os.chdir(path) 
                shutil.rmtree("__pycache__")
        
            # ------------------------- TEST & DEBUG ONLY ------------------------
            elif lan == "debug":
                sys.path.append('..')
            
                try:        
                    import Test 
                    Test.main()
                except:     print("\n-------------------------\nDebug Module Missing\n-------------------------\n")
                else:       print("\n-------------------------\nSuccess\n-------------------------\n")
                finally:    input("按任意键来返回 | Press Any Key To Go Back"); continue
            # ------------------------- END -------------------------      

            break