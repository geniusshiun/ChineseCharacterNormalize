def hantoutf32(han):
    """Transfer chinese character to UTF-32
    
    By using json dump function to transfer chinese character to UTF-32
    
    Args:
        han: input chinese character
    Returns:
        upper UTF-32
    """
    import json
    import re
    if han == '\\':
        return '\\'
    if len(json.dumps(han)) <=3:
        return han
    else:
        codelist = re.findall(' ([a-z0-9]+)',json.dumps(han).replace('\\u',' '))
        if len(codelist) == 2:
            highbit = int(codelist[0],16) - int('D800',16)
            lowbit = int(codelist[1],16) - int('DC00',16)
            utf32 = hex((highbit<<10 | lowbit)+int('0x10000',16))[2:]
            return utf32.upper()
        else:
            return ''.join(codelist).upper()

def utf32toutf16(utf32):
    """Transfer UTF-32 character to UTF-16
    
    Args:
        utf32: UTF-32
    Returns:
        UTF-16
    """
    
    if len(utf32)>6:
        binary = "{0:b}".format(int(utf32,16)-int('0x10000',16))
        lowbit = int(binary[-10:], 2) +int('DC00',16)
        highbit = int(binary[:-10], 2) +int('D800',16)
        returnstr = (('"\\u'+hex(highbit)[2:]+'\\u'+hex(lowbit)[2:]+'"'))
        return (returnstr)
    else:
        init = int(utf32,16)
        returnstr = '"\\u'+hex(init)[2:]+'"'
        return returnstr

def rangereturn(character):
    """Find out where the character is.
    
    Get the region number of below 7 areas.
    
    Args:
        character: UTF-32
    Returns:
        region number(from 0 to 6)
    """
    start = ['0x3400', '0x4E00', '0xF900', '0x20000', '0x2A700','0x2B740','0x2B820']
    end = ['0x4DBF', '0x9FD5' , '0xFAFF', '0x2A6DF', '0x2B73F', '0x2B81F', '0x2CEA1']
    
    rangeCnt = {}
    for cnt in range(len(start)):
        rangeCnt[cnt] = 0

    findrange = False
    for cnt in range(len(start)):
        if len(hantoutf32(character)) >= 4:
            if int(hantoutf32(character),16)>int(start[cnt],16) and int(hantoutf32(character),16)<int(end[cnt],16):
                findrange = True
                return str(cnt)
        else:
            return 'NULL'
    if not findrange:
        return 'NULL'

def loaddict():
    """Load the data from unihaz download.
    
    Get variant table from Unihan_Variants; get frequency and grade level from Unihan_DictionaryLikeData;
    get kHanyuPinyin and kMandarin from Unihan_Readings
    
    Args:
        Null
    Returns:
        unicodeToVar(dict)
        unicodeToFrequency(dict)
        unicodeTokGradeLevel(dict)
        unicodeTokHanyuPinyin(dict)
        unicodeTokMandarin(dict)
    """
    
    
    classlist = []
    unicodeToVar = {}
    tmpdict = {}
    with open('Unihan_Variants.txt','r') as f:
        for line in [n.strip() for n in f.readlines()]:
            try:
                if line[0] == '#':
                    continue
                if not line.split('	')[0][2:] in unicodeToVar:
                    unicodeToVar[line.split('	')[0][2:]] = []
                tmpdict['type'] =  line.split('	')[1]
                tmpdict['mapping'] =  line.split('	')[2]
                unicodeToVar[line.split('	')[0][2:]].append(tmpdict)
                tmpdict = {}
                if not line.split('	')[1] in classlist:
                    classlist.append(line.split('	')[1])
            except:
                line = line

    unicodeToFrequency = {}
    with open('Unihan_DictionaryLikeData.txt','r',encoding='utf8') as f:
        #print(f.readlines()[:20])
        for line in f.readlines():
            line = line.strip()
            try:
                if line[0] == '#' or line =='':
                    continue
                if line.split('	')[1] == 'kFrequency':
                    unicodeToFrequency[line.split('	')[0][2:]] = {}
                    unicodeToFrequency[line.split('	')[0][2:]]['type'] = line.split('	')[1]
                    unicodeToFrequency[line.split('	')[0][2:]]['value'] = line.split('	')[2]
            except:
                line = line
    unicodeTokGradeLevel = {}
    with open('Unihan_DictionaryLikeData.txt','r',encoding='utf8') as f:
        #print(f.readlines()[:20])
        for line in f.readlines():
            line = line.strip()
            try:
                if line[0] == '#' or line =='':
                    continue
                if line.split('	')[1] == 'kGradeLevel':
                    unicodeTokGradeLevel[line.split('	')[0][2:]] = {}
                    unicodeTokGradeLevel[line.split('	')[0][2:]]['type'] = line.split('	')[1]
                    unicodeTokGradeLevel[line.split('	')[0][2:]]['value'] = line.split('	')[2]
            except:
                line = line
    unicodeTokHanyuPinyin = {}
    with open('Unihan_Readings.txt','r',encoding='utf8') as f:
        #print(f.readlines()[:20])
        for line in f.readlines():
            line = line.strip()
            try:
                if line[0] == '#' or line =='':
                    continue
                if line.split('	')[1] == 'kHanyuPinyin':
                    unicodeTokHanyuPinyin[line.split('	')[0][2:]] = {}
                    unicodeTokHanyuPinyin[line.split('	')[0][2:]]['type'] = line.split('	')[1]
                    unicodeTokHanyuPinyin[line.split('	')[0][2:]]['value'] = line.split('	')[2].split(' ')[0].split(':')[1].split(',')
            except:
                line = line
    unicodeTokMandarin = {}
    with open('Unihan_Readings.txt','r',encoding='utf8') as f:
        #print(f.readlines()[:20])
        for line in f.readlines():
            line = line.strip()
            try:
                if line[0] == '#' or line =='':
                    continue
                if line.split('	')[1] == 'kMandarin':
                    unicodeTokMandarin[line.split('	')[0][2:]] = {}
                    unicodeTokMandarin[line.split('	')[0][2:]]['type'] = line.split('	')[1]
                    unicodeTokMandarin[line.split('	')[0][2:]]['value'] = line.split('	')[2]
            except:
                line = line
    return unicodeToVar,unicodeToFrequency,unicodeTokGradeLevel,unicodeTokHanyuPinyin,unicodeTokMandarin