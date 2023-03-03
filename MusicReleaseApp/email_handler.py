import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from email import encoders

def send_mail(gmail,password,to,subject,text,filename):
    charset = 'iso-2022-jp'
    if filename:
        filename = os.getcwd() + filename.url
    # メール作成
    msg = MIMEMultipart()
    msg['From'] = gmail
    msg['To'] = to
    msg['Subject'] = subject
    # メール本文を追加
    msg.attach(MIMEText(text, 'plain',charset))
    # 添付ファイルを追加
    if filename:
        attachment = open(filename, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(filename))
        msg.attach(p)

    # SMTPサーバーに接続してメールを送信
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(gmail, password)
    text = msg.as_string()
    s.sendmail(gmail, to, msg.as_string())
    s.quit()
    