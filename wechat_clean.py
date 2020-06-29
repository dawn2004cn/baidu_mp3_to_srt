#encoding=utf-8
from wxpy import *
import time
import random

bot = None

def login_wechat():
    global bot
    bot = Bot()  # window
    # bot = Bot(console_qr=2,cache_path="botoo.pkl")#linux环境上使用

def send_news():
    if bot == None:
        login_wechat()
    try:
        #my_friend = bot.friends().search(u'老范')[0]  # 老范 表示微信昵称
        #my_friend.send(get_news()[0])
        #my_friend.send(get_news()[1][5:])
        #my_friend.send(u"咦？我是自动人！！")
        #t = Timer(5, send_news)  #5是秒数:5秒发送一次
        #t.start()
        all_friends = bot.friends()
        myself = bot.self
        print('----------------BEGIN----------------')
        print("检测到你联系人共计: "+ str(len(all_friends)) + " 人")
        index = 1
        for user in all_friends:
            #time.sleep(random.randint(0, 9))
            try:
                if user != myself:
                    if user.sex == 1:
                        sex = "man"
                    elif user.sex == 2:
                        sex = "female"
                    print("[" + str(index) + "/" + str(len(all_friends)) + "] " + user.name+";sex:"+sex)
                    # user.send('能看到我发的吗 జ్ఞా ')
            except ResponseError as e:
                print(e.err_code, e.err_msg)
            index += 1
        print("检测已执行完毕请到手机微信app中处理")

        print('----------------END----------------')
    except:
        print(u"失败！")
if __name__ == "__main__":
    send_news()
