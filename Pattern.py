from Common import Log, Read_Config



def Main(filepath):
    Pattern, Ignore_content = None, None
    lines, links, count = [], {}, 0

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
    file.close()

    # Iter over @lines
    index = 0
    for line in lines:
        line = lines[index]
        match = []

        # 'any' lines: if patten found in current line: append into @match and flag True
        if  any(key if key in line else False for key in Pattern.keys()):  
            any(match.append(key) if key in line else False for key in Pattern.keys())  # support multiple pattern for single line
            
            for pattern in match:
                pattern_value = Pattern[pattern]
                line_num = (index + 1) + pattern_value  # start from (pattern's next line) + (ignore line)

                while True:
                    content = lines[line_num].strip("\n")
                    if content == "": break
                    
                    ignore = any(key if key in content else False for key in Ignore_content)
                    if not ignore: 
                        Log.logger.info(content + "\n")
                        if not links.get(pattern): links[pattern] = [content]
                        else: 
                            tmp = links[pattern]
                            tmp.append(content)
                            links[pattern] = tmp
                        count += 1
                    line_num += 1

        index +=1

    return links, count

