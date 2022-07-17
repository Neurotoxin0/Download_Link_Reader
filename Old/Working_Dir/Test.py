import os, shutil

def main():
    path = (os.path.split(os.path.realpath(__file__))[0] + "/").replace("\\\\", "/").replace("\\", "/")           
    
    os.chdir(path + "Test_Env/")
    for item in os.listdir():
        if os.path.isfile(item) and (item != "Main.py"): os.remove(item)
        if os.path.isdir(item) and (item != "Working_Dir"): shutil.rmtree(item)

    os.chdir(path + "Test_Env/Working_Dir")
    for item in os.listdir():
        if os.path.isfile(item) and (item != "Read_Files.py"): os.remove(item)
        if os.path.isdir(item): shutil.rmtree(item)

    os.chdir(path)
    shutil.copytree("Materials", "Test_Env/Materials")