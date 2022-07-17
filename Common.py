import json, logging, os, sys, time
from logging import handlers

Path = (os.path.split(os.path.realpath(__file__))[0] + "/").replace("\\\\", "/").replace("\\", "/")
#Path = (os.path.dirname(os.path.realpath(sys.executable)) + "/").replace("\\\\", "/").replace("\\", "/")
Time = time.strftime("%Y.%m.%d@%H_%M_%S", time.localtime()) 

# Logger
class Logger(object):
    level_relations =  { 'info': logging.INFO }

    def __init__(self, log_file, level = 'info', format = "%(message)s"):
        self.logger = logging.getLogger(log_file)
        self.logger.setLevel(self.level_relations.get(level))
        format = logging.Formatter(format)
        
        # Output on CLI interface
        CLI = logging.StreamHandler()
        CLI.setFormatter(format)
        self.logger.addHandler(CLI)

        # Output to log file
        LOG = handlers.TimedRotatingFileHandler(filename = log_file, encoding = 'utf-8')
        LOG.setFormatter(format)
        self.logger.addHandler(LOG)

log_path = Path + "Log/"
if not os.path.exists(log_path): os.makedirs(log_path)
Log = Logger(log_path + Time + ".log")

# 读取config.json | Read from config.json
def Read_Config():
    try:
        config = open(Path + "config.json", "r", encoding='utf-8')
        return json.loads(config.readlines()[0])
    except: return None

# 读取用户输入 | Read input from interface
def Read():
    option = input("> ").strip()
    if (option == ""): Log.logger.info("\nINPUT: <Enter>") 
    else:                           Log.logger.info("\nINPUT: " + option)
    Log.logger.info("\n--------------------------------------------------\n")
    return option

# 返回信息 | Pop Message
def Message(option, back, Language = -1):
    message = {
        1: ["无效选项", "Invalid Command", "无效选项 | Invalid Command"][Language],
        2: ["已保存", "Saved"][Language],
        3: ["请输入一个关键字，留空来返回: ", "Please Enter A Keyword, Input <SPACE> To Go Back: "][Language],
        4: ["关键字已存在!", "Keyword Exist!"][Language],
        5: ["关键字不存在!", "Keyword Not Exist!"][Language],
        6: ["请输入名称: ", "Please Enter The Name: "][Language],
        7: ["无效名称", "Invalid Name"][Language],
        8: ["输入'y' 来确定删除", "Input 'y' To Confirm Deletion?"][Language],
        9: ["已删除, 将在下次启动时使用默认配置", "Deleted, Will Use Default Setting On Next Run"][Language],
        10: ["取消删除", "Deletion Canceled"][Language]
    }
    Log.logger.info(message[option])
    if back: Log.logger.info(["按任意键来返回", "Press Any Key To Go Back", "按任意键来返回 | Press Any Key To Go Back"][Language]); Read()
    
