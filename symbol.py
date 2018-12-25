def strQ2B(ustring):
    """把字串全形轉半形"""
    rstring = []
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code==0x3000:
            inside_code=0x0020
        else:
            if (inside_code-0xfee0 > 0):
                inside_code-=0xfee0

        if inside_code<0x0020 or inside_code>0x7e:   #轉完之後不是半形字元返回原來的字元
            rstring.append(uchar)
        else:
            rstring.append(chr(inside_code))

    return ''.join(rstring)

def strB2Q(ustring):
    """把字串半形轉全形"""
    rstring = []
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:   #不是半形字元就返回原來的字元
            rstring.append(uchar)
            continue
        if inside_code==0x0020: #除了空格其他的全形半形的公式為:半形=全形-0xfee0
            inside_code=0x3000
        else:
            inside_code +=0xfee0
        rstring.append(chr(inside_code))
    return ''.join(rstring)

if __name__ == '__main__':
    newword = strB2Q('。天abc123!@#$%^&*()_+[]\/.,~`}{":?><')
    #print(newword)
    #print(strQ2B(newword))
    #print(strQ2B('ＡＢＣ！！！$@#＠＃＄＠＃％）（＠＊!!１２３４５!!•╳'))
    specialmapping = {'•':'§','╳':'§'}
    othersymbol = [';','[',']','*','%',"'",'`','=','#','^','@','<','>','\\','$','}','{']
    mappingtable = {'（':'(','）':')','－':'-','＿':'_','，':',','＋':'+','—':'-','／':'/','“':'"', '”':'"','？':'?',
                '　':' ','	':' ','‧':'.','！':'!','．':'.','＆':'&','：':':','ㄟ':'誒','ㄉ':'的','㖈':'老','～':'~'}
    for full,half in mappingtable.items():
        if strQ2B(full) != half:
            print(full,half,strQ2B(full))
    
    
