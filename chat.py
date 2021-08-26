import itchat
from itchat.content import *

itchat.auto_login(hotReload=True)

MEMBERS = {}
chatroomName=u'鉴湖分校小学同学群'
itchat.get_chatrooms(update=True)
chatrooms = itchat.search_chatrooms(name=chatroomName)
if chatrooms is None:
    print(u'没有找到群聊：' + chatroomName)
else:
    chatroom = itchat.update_chatroom(chatrooms[0]['UserName'])
    for friend in chatroom['MemberList']:
        MEMBERS[friend['DisplayName']] = 0

@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING], isGroupChat = True)
def print_content(msg):
    print(msg['ActualNickName'],':',msg['Text'])
    MEMBERS[msg['ActualNickName']] +=1
    # print(MEMBERS)

    if msg['isAt']:
        return u'@%s\u2005 共计 %d 条信息' % (msg['ActualNickName'], MEMBERS[msg['ActualNickName']])

itchat.run()

# #coding=utf8
# import itchat, time

# itchat.auto_login(hotReload=True)

# REAL_SINCERE_WISH = u'祝%s新年快乐！！'

# chatroomName=u'鉴湖分校小学同学群'
# itchat.get_chatrooms(update=True)
# chatrooms = itchat.search_chatrooms(name=chatroomName)
# # if chatrooms is None:
# #     print(u'没有找到群聊：' + chatroomName)
# # else:
# #     chatroom = itchat.update_chatroom(chatrooms[0]['UserName'])
# #     print(chatroom)
# #     for friend in chatroom['MemberList']:
# #         # print(friend)
# #         # friend = itchat.search_friends(userName=friend['UserName'])
# #         # 如果是演示目的，把下面的方法改为print即可
# #         # itchat.send(REAL_SINCERE_WISH % (friend['DisplayName']
# #             # or friend['NickName']), friend['UserName'])
# #         print(friend['DisplayName'] or friend['NickName'])
# #         time.sleep(.5)