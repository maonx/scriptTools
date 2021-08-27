import requests
import itchat
import time
from itchat.content import *


itchat.auto_login(hotReload=True)

def get_day():
    day = time.strftime("%d",time.localtime())
    return day

MEMBERS = {}
MESSAGE = 0
TODAY = get_day()

def init():
    global MESSAGE, MEMBERS
    MESSAGE = 0
    chatroomName=u'鉴湖分校小学同学群'
    itchat.get_chatrooms(update=True)
    chatrooms = itchat.search_chatrooms(name=chatroomName)
    if chatrooms is None:
        print(u'没有找到群聊：' + chatroomName)
    else:
        chatroom = itchat.update_chatroom(chatrooms[0]['UserName'])
        for friend in chatroom['MemberList']:
            MEMBERS[friend['DisplayName'] or friend['NickName']] = 0
            
init()

def get_ownthink_robot(text, userid=""):
    """
    思知机器人，接口地址:<https://www.ownthink.com/>
    https://api.ownthink.com/bot?appid=xiaosi&userid=user&spoken=姚明多高啊？
    :param text: 发出的消息
    :param userid: 收到的内容
    :return:
    """
    try:
        app_key = ''

        params = {
            # 'appid': app_key,
            # 'userid': userid,
            'spoken': text
        }
        url = 'https://api.ownthink.com/bot'
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            # print(resp.text)
            content_dict = resp.json()
            if content_dict['message'] == 'success':
                data = content_dict['data']
                if data['type'] == 5000:
                    reply_text = data['info']['text']
                    return reply_text
                else:
                    print('返回的数据不是文本数据！')
            else:
                print('思知机器人获取数据失败:{}'.format(content_dict['msg']))

        print('获取数据失败')
        return None
    except Exception as exception:
        print(str(exception))


@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING], isGroupChat = True)
def print_content(msg):
    if TODAY != get_day():
        init()

    print(msg['ActualNickName'],':',msg['Text'])
    global MESSAGE, MEMBERS
    MEMBERS[msg['ActualNickName']] +=1
    MESSAGE += 1
    # print(MEMBERS)

    if msg['isAt']:
        # print(msg['Text'])
        if u'我聊了' in msg['Text']:
            return u'@%s\u2005 你好，今天你在本群发言 %d 次' % (msg['ActualNickName'], MEMBERS[msg['ActualNickName']])
        elif u'总计聊天' in msg['Text']:
            return u'今天本群共发言 %d 次。' % MESSAGE
        elif u'聊天排行榜' in msg['Text']:
            phb = sorted(MEMBERS.items(), key = lambda kv:(kv[1],kv[0]))
            phb.reverse()
            phb5 = phb[:5]
            string = ''
            for i in phb5:
                string += u'%s: %d 条聊天记录\n' % (i[0], i[1])
            return string            
        else:
            myself = u'@小助手\u2005'
            text = msg['Text'].replace(myself,"")
            if text == "":
                return u'@%s\u2005 你可以发送 “我聊了”、“总计聊天”、“聊天排行榜” 给我试试，也可以和我聊天玩。' % msg['ActualNickName']
            else:
                return u'@%s\u2005 %s' % (msg['ActualNickName'], get_ownthink_robot(text))

itchat.run()