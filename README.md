# README OpenCV

## ImageAccess.py
* 保存済みの画像のランプ点灯を判別するプログラム
* iamge_* を探してきて処理をする。
* 一番最初に読んできたファイル名から、出力ファイル名を出すので日にち事の処理が必要
* 0210.txtなど日付の名前のファイルを吐き出す。
* 出力は、スペース区切りで %Y$m%D%H%M work NO1off No1on No2off No2on Htankfull Htankless Ltankfill HtankLow と９列になっている。

## monitor.py
* ImageAccessをリアルタイムで実行するプログラム
* webカメラからの画像をリアルタイムで処理して１秒毎にｔｘｔに書き込む

## MailSend.py
* image_comp.zip をpump.opencv@gmail.comに送信するプログラム 

