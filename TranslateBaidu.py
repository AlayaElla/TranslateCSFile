import hashlib
import random
import requests

#APP ID
appID = ''
#密钥
secretKey = ''
apiURL = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

def translate(translist):
    trans_str = ''
    for _str in translist:
        trans_str += _str+"\n"
    salt = str(random.randint(32768, 65536))
    pre_sign = appID + trans_str + salt + secretKey
    sign = hashlib.md5(pre_sign.encode()).hexdigest()
    data = {
        'q': trans_str,
        'from': 'auto',
        'to': 'zh',
        'appid': appID,
        'salt':salt,
        'sign': sign
    }
    information = requests.get(apiURL, params=data)
    return_list = {}
    if(information.status_code == 200):
        json = information.json()
        if 'trans_result' in json:   
            for result in json['trans_result']:
                #return_list.append(result['dst'])
                return_list[result['src']] = result['dst']
            return return_list
        else:
            print('翻译错误！：'+ json['error_code'])
            return return_list
    else:
        print('网络错误！：'+ str(information.status_code))
        return return_list
