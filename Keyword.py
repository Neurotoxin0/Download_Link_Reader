from Common import Log, Read_Config

def Main(filepath):
    
    Keyword, Ignore_content = None, None
    links, count = [], 0

    # Load cfg
    Config = Read_Config()
    try:
        Keyword = Config['KeyWord']
        Ignore_content = Config['Ignore Content']
    except: return None, -1     # Bad Config
        
    # Read lines
    file = open(filepath, "r", encoding='utf-8')
    for line in file.readlines():
        link = any(key if key in line else False for key in Keyword)
        ignore = any(key if key in line else False for key in Ignore_content)

        if link and not ignore:
            line = line.strip("\n")
            Log.logger.info(line + "\n")
            links.append(line)
            count += 1

    links.append("")    # append line to seperate each file
    return links, count