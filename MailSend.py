from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
from os.path import basename

# SMTP認証情報
account  = "********@gmail.com"
password = "********"

# 送受信先
to_email = "*********@gmail.com"
from_email = "********@gmail.com"

# MIMEの作成
subject = "Pump Room Image"
message = "Look at these."
msg = MIMEMultipart()
msg["Subject"] = subject
msg["To"] = to_email
msg["From"] = from_email
msg.attach(MIMEText(message))

# ファイルを添付
path = "./image_comp.zip"
with open(path, "rb") as f:
    part = MIMEApplication(
        f.read(),
        Name=basename(path)
    )

part['Content-Disposition'] = 'attachment; filename="%s"' % basename(path)
msg.attach(part)

# メール送信処理
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(account, password)
server.send_message(msg)
server.quit()
