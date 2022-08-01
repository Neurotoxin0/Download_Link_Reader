from Common import Log, Read_Config

def Main(filepath):
    
    Pattern, Ignore_content = None, None
    lines, links, count,  = [], [], 0

    # Load cfg
    Config = Read_Config()
    try:
        Pattern = Config['Pattern']
        Ignore_content = Config['Ignore Content']
    except: return None, -1     # Bad Config
        
    # Read lines
    file = open(filepath, "r", encoding='utf-8')
    
    # Put all lines into @lines
    for line in file.readlines(): lines.append(line)

    # Iter over @lines
    index = 0
    for line in lines:
        match = []
        # 'any' lines: if patten found in current line: append into @match and return True
        if  any(key if key in line else False for key in Pattern.keys()):  
            any(match.append(key) if key in line else False for key in Pattern.keys())
            for key in match:
                line_num = index + Pattern.get(key)
                if line_num >= 0 and line_num < len(lines):
                    content = lines[line_num].strip("\n")
                    Ignore = any(key if key in content else False for key in Ignore_content)
                    if not Ignore: 
                        Log.logger.info(content)
                        links.append(key + ": " + content)
                        count += 1
        index +=1

    return links, count