# -*- coding: utf8 -*-
import MySQLdb
import os
import sys
reload(sys)
import csv
import smtplib, time
import datetime
sys.setdefaultencoding('utf-8')

#获取巡检记录，写入csv文件
Sql = "SELECT   *  FROM checklist where date=curdate()"
today = datetime.datetime.now().strftime('%Y%m%d')

def DatabaseConnect(Sql):
    db = MySQLdb.connect("192.168.133.128", "root", "112233", "cptest")
    cursor = db.cursor()
    cursor.execute(Sql)
    results = cursor.fetchall()
    db.close()
    csvfile = file('/app/checklist/checklist_%s.csv' % today, 'wb')
    print dir(csv)
    writers = csv.writer(csvfile)
#    writers.writerow(['date', 'description', 'item', 'version', 'status', 'lock_about', 'lock_reason', 'errorlogcount', 'lastbackuptime', 'nextbackuptime', 'max_QPS', 'max_TPS', 'max_cpu', 'max_mem', 'diskusage', 'disktotal'])
    writers.writerow(['日期', '别名', '实例', '数据库版本', '状态', '锁情况', '锁理由', '错误日志数', '昨日备份情况', '下次备份时间', 'QPS峰值', 'TPS峰值', 'cpu峰值', '内存峰值', '磁盘使用量', '磁盘总量'])
    writers.writerows([])
    for i in results:
        print i
        writers.writerows([i])
    csvfile.close()
DatabaseConnect(Sql)

## 将csv文件内容转化为html格式
os.system('csv2html -o /app/checklist/checklist_%s.html /app/checklist/checklist_%s.csv ' % (today,today))

#发送邮件
def SentEmail():
        sender = "abc@qq.com"  #发件人地址
        rcpt = ['zhangsan@qq.com','lisi@qq.com']  #收件人列表
        msg = MIMEMultipart('alternatvie')
        msg['Subject'] = Header("%s-数据库巡检" % today,"utf-8") #组装信头
        msg['From'] = r"%s <abc@qq.com>" % Header("巡检邮件","utf-8") #使用国际化编码
        msg['To'] = ','.join(rcpt)
        html = open('/app/checklist/checklist_%s.html' % today).read() #读取HTML模板
        html_part = MIMEText(html,'html') #实例化为html部分
        html_part.set_charset('utf-8') #设置编码
        msg.attach(html_part) #绑定到message里

        try:
            s = smtplib.SMTP('smtp.exmail.qq.com') #登录SMTP服务器,发信
            s.login('abc@qq.com','XXXXXXX')
            s.sendmail(sender,rcpt,msg.as_string())
        except Exception,e:
            print e

SentEmail()

