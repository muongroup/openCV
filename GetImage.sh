#!/bin/sh

DATE=$(date +%Y%m%d_%H%M%S)
echo $DATE

mv temp image
python3 zipCreate.py
python3 MailSend.py
mv image_comp.zip ./$DATE.zip
