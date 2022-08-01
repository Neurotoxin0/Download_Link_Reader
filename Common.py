import json, logging, os, shutil, sys, time
from logging import handlers

#Path = (os.path.split(os.path.realpath(__file__))[0] + "/").replace("\\\\", "/").replace("\\", "/")
Path = (os.path.dirname(os.path.realpath(sys.executable)) + "/").replace("\\\\", "/").replace("\\", "/")
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

# Read from config.json
def Read_Config():
    try:
        config = open(Path + "config.json", "r", encoding='utf-8')
        return json.loads(config.readlines()[0])
    except: return None

# Read input from interface
def Read():
    option = input("> ").strip()
    if (option == ""): Log.logger.info("\nINPUT: <Enter>") 
    else:                           Log.logger.info("\nINPUT: " + option)
    Log.logger.info("\n--------------------------------------------------\n")
    return option

# Pop Message
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
        10: ["取消删除", "Deletion Canceled"][Language],
        11: ["配置已损坏！", "Bad Config File!"][Language],
        12: ["关键字已存在! 输入新行数来修改, 或留空来返回", "Keyword Exist! Input New # Of Lines To Update, Or Input <SPACE> To Go Back"][Language],
        13: ["请输入行数 --- 找到关键字后的第几行;例如：1代表关键字后一行，-1代表关键字前一行，0代表关键字本身", "Please Input # Of Lines --- # of line after keyword matched; e.g. 1 -> 1 line after keyword, -1 -> line before keyword, 0 -> keyword line"][Language],
    }
    Log.logger.info(message[option])
    if back: Log.logger.info(["按任意键来返回", "Press Any Key To Go Back", "按任意键来返回 | Press Any Key To Go Back"][Language]); Read()

# Exit Method
def Exit(exit = True):
    try: shutil.rmtree(Path + "__pycache__"); 
    except: pass
    if exit: os._exit(0)
