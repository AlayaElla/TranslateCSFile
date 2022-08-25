import requests

def translate(translist):
    trans_str = ''
    for _str in translist:
        trans_str += _str+"\n"
    data = {
        'q': trans_str,
        'from': 'Auto',
        'to': 'zh-CHS'
        }
    information = requests.post('https://aidemo.youdao.com/trans', data)
    json = information.json()
    if json['errorCode'] != '0':
        print('翻译错误！：'+ json['errorCode'])
        return trans_str
    return_list = {}
    index = 0
    for result in json['translation']:
        return_list[translist[index]] = result
        index+=1
    return return_list