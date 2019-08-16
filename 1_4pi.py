import requests
from bs4 import BeautifulSoup
import time
import smtplib      # 导入 smtplib 邮件处理库
from email.mime.text import MIMEText
from email.header import Header
import random
import os

mail_server = "smtp.qq.com"        
port = "465"  # 服务端口
sender = "778349156@qq.com"     
sender_passw = "rejgndistmjabfch"
receiver = "1014616248@qq.com"      

def getHTMLText(url,kv):
    try:
        r=requests.get(url,headers=kv,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        #print("页面获取成功")
        #print(r.apparent_encoding)
        #print(r.text[0:1000])
        #print('__________________')
        return r.text
    except:
        print("源代码获取失败")
    

def parsePage(html):
    try:
        soup=BeautifulSoup(html, "html.parser")
        content = soup.find_all('div', attrs={'class':'stock-info'})
        for wrap in content:    #在一级标题中找二级标题
            wrap2 = wrap.find_all('div', attrs={'class':'stock-bets'})
            for wrap3 in wrap2:     #在二级标题中找三级标题
                wrap4 = wrap3.find_all('div', attrs={'class':'price'})
                for price_tag in wrap4:   #在三级标题中找四级标题
                    price_num=price_tag.find('strong').get_text()
                    return price_num
    except:
        print("商品信息输出失败")

def sendMail(mail_server, port, sender,sender_passw, receiver,name):
    msg = MIMEText("", "plain", "utf-8")     # 邮件内容（正文）
    msg['From'] = Header("夜半疾风", "utf-8")        # 发件人信息
    msg['To'] = Header("llong", "utf-8")        # 收件人信息
    msg['Subject'] = str(name)              # 邮件的主题
    try:
        mail = smtplib.SMTP_SSL(mail_server, port)  # 使用SMTP()方法指向服务器（使用QQ邮箱服务器时，需改用 SMTP_SSL()方法）
        print(mail.login(sender, sender_passw) )    # 请求服务器，登录帐号
        mail.sendmail(sender, receiver, msg.as_string() )   # 发送邮件
        mail.quit()     # 断开连接
        print("邮件发送成功！")
    except:
        mail.quit()
        print("邮件发送失败！")


def main():
    goods='名字'
    depth=9
    kv = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}
    baiduurl=['https://gupiao.baidu.com/stock/sh600600.html',
              'https://gupiao.baidu.com/stock/sh603369.html',
              'https://gupiao.baidu.com/stock/sz300313.html',
              'https://gupiao.baidu.com/stock/sz002230.html',
              'https://gupiao.baidu.com/stock/sz002507.html',
              'https://gupiao.baidu.com/stock/sz000860.html',
              'https://gupiao.baidu.com/stock/sh600751.html',
              'https://gupiao.baidu.com/stock/sh603038.html',
              'https://gupiao.baidu.com/stock/sz000877.html']
    
    price=[0,0,0,0,0,0,0,0,0]
    path="/home/yczheng/python_program"
    filename=path+'/'+'stock.txt'
    while True:
        hour=time.strftime("%H",time.localtime())     #获取小时和周几
        day=time.strftime("%A",time.localtime())
        if(int(hour)>=9 and int(hour)<16 and day!="Saturday"and day!="Sunday"):
            for i in range(depth):  
                url=baiduurl[i]
                try:
                    html=getHTMLText(url,kv)
                    price[i]=parsePage(html)             
                except:
                    continue
            content=time.ctime()+'-----青岛啤酒:'+str(price[0])+'--今世缘'+str(price[1])+'--天山生物'+str(price[2]+'--科大讯飞'+str(price[3])
                  +'--涪陵榨菜'+str(price[4])+'--顺鑫农业'+str(price[5])+'--海航科技'+str(price[6])+'--华立股份'+str(price[7])+'--天山股份'+str(price[8]))
            print(content) #打印当前时间和价格
 
            infolist=''
            try:
                if(float(str(price[0]))<=40):
                    infolist=infolist+'青岛啤酒:'+(str(price[0]))
                if(float(str(price[1]))>=29.5):
                    infolist=infolist+'--今世缘:'+(str(price[1]))
                if(float(str(price[2]))<=5):
                    infolist=infolist+'--天山生物:'+(str(price[2]))
                if(float(str(price[3]))<=28):
                    infolist=infolist+'--科大讯飞:'+(str(price[3]))
                if(float(str(price[4]))<=21):
                    infolist=infolist+'--涪陵榨菜:'+(str(price[4]))
                if(float(str(price[5]))<=37.6):
                    infolist=infolist+'--顺鑫农业:'+(str(price[5]))
                if(float(str(price[6]))<=2.75):
                    infolist=infolist+'--海航科技:'+(str(price[6]))
                if(float(str(price[7]))<=12.5):
                    infolist=infolist+'--华立股份:'+(str(price[7]))
                if(float(str(price[8]))<=9.0):
                    infolist==infolist+'--天山股份:'+(str(price[8])) 
            except:
                time.sleep(random.randint(70, 120))
                continue
            if(infolist!=''):    
                sendMail(mail_server, port, sender, sender_passw, receiver,infolist)
            f=open(filename,'a+')
            f.write(content+'\n')
            f.close()
            time.sleep(random.randint(70, 120))   #随机70-120秒的时间
        else:
            print("现在不是开市时间")
            time.sleep(600)
        
        
main()
            
