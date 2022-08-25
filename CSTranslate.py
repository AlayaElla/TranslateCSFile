from math import fabs
import os
import sys
import re
#import TranslateBaidu as TranslateModule
import TranslateYoudao as TranslateModule
import CSTranslateTools

#文件后缀
endswith = '.cs'
#注释关键字
keylist = [
    r'.*/// (.*)']
insplist = [
    r'.*\[Tooltip\("(.*)"\)\]',
    r'.*\[Header\("(.*)"\)\]']
#忽略注释关键字
ignorekeylist = ['<param','</param>','<summary>',' </summary>','<returns>','<typeparam','<exception ','<footer>','{','}',';']
#忽略的文件夹
ignorefolderlist = ['TextMesh Pro']

charcount = 0
filecount = 0

def setTranslateString(match,finishtransStringList):
    if (any (kw in match.group() for kw in ignorekeylist)):
        return match.group()
    transString = CSTranslateTools.getGroupValue(match.groups())
    if(transString == ""):
        return match.group()
    if(not transString in finishtransStringList):
        return match.group()
    _returnStr = match.group()
    _translateStr = str(finishtransStringList[transString])

    tips_regex = '|'.join(reg for reg in insplist)
    if(re.match(tips_regex, _returnStr)):
        _returnStr = _returnStr.replace(transString,transString + '\\n' + _translateStr)    #tips
    else:
        _returnStr += '\n' + _returnStr.replace(transString,_translateStr)    #comment
    return _returnStr

def doTranslate(fullname,tok_regex,data,transStringList):
    global charcount
    global filecount

    if(len(transStringList) == 0):
        return
    print(f"正在翻译:{fullname}")
    filecount+=1
    finishtransStringList = TranslateModule.translate(transStringList)
    write_data =  re.sub(tok_regex, lambda match: setTranslateString(match, finishtransStringList), data)   
    
    file3=open(fullname, 'w', encoding="utf-8")
    file3.write(write_data)
    file3.close()

    #count total char
    transStr = ''
    for _str in transStringList:
        transStr += _str
    charcount += len(transStr)

def getAllTranlateString(fullname,tok_regex):
    file3 = open(fullname,'r', encoding="utf-8")
    data = file3.read()
    pattern = re.compile(tok_regex)
    transStr = '';lastStr = ''
    transStringList = []
    for m in pattern.finditer(data):
        if (not any (kw in m.group() for kw in ignorekeylist)):
            transStr = CSTranslateTools.getGroupValue(m.groups())
            if(transStr == ""):
                continue
            #如果是注释且这条是中文，这上一条是英文
            tips_regex = '|'.join(reg for reg in insplist)
            if(not re.match(tips_regex, m.group())):
                if(CSTranslateTools.isContainsChinese(transStr) and not CSTranslateTools.isContainsChinese(lastStr)):
                    if(lastStr in transStringList):
                        transStringList.remove(lastStr)
                    continue
            #Inspector面板中文可能和注释一样，跳过省汉化字符
            if(transStr == lastStr):
                continue
            if(CSTranslateTools.isContainsChinese(transStr)):
                continue
            lastStr = transStr
            transStringList.append(transStr)
    file3.close()
    return data,transStringList

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        if(any (folder in root for folder in ignorefolderlist)):
            continue
        for f in fs:
            if f.endswith(endswith):
                fullname = os.path.join(root, f)
                yield fullname

def main():
    base = sys.path[0]
    key_regex = '|'.join(reg for reg in keylist)
    tips_regex = '|'.join(reg for reg in insplist)
    tok_regex =''
    if(tips_regex!=""):
        tok_regex = key_regex+'|'+tips_regex
    for i in findAllFile(base):
        data,transStringList = getAllTranlateString(i,tok_regex)
        doTranslate(i,tok_regex,data,transStringList)
    
    print(f"翻译文件数:{filecount}")
    print(f"翻译总字数:{charcount}")
    os.system("pause")

if __name__ == '__main__':
    main()