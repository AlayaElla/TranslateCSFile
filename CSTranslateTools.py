def isContainsChinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def getKeywordByList(_str,_list):
    for kw in _list:
        if(kw in _str) :
            return kw
    return ""

def getGroupValue(groups):
    for value in groups:
        if(value!=None):
            return value
    return ""