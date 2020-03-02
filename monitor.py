import cv2
import os
import glob
import datetime
from matplotlib import pyplot as plt

def binaryCvt(image,thresh):
	gray  = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
	ret, binary =cv2.threshold(gray,thresh,255,cv2.THRESH_BINARY)
	# ret, binary =cv2.threshold(gray,thresh,1,cv2.THRESH_OTSU)
	return binary
	# return gray

def showRectangle(image,pWork,pPump,pTanks):
    cv2.rectangle(image,(pWork['x1'],pWork['y1']),(pWork['x2'],pWork['y2']),230,1)	
    cv2.rectangle(image,(pPump['1offx1'],pPump['y1']),(pPump['1offx2'],pPump['y2']),230,1)	
    cv2.rectangle(image,(pPump['1onx1'] ,pPump['y1']),(pPump['1onx2'] ,pPump['y2']),230,1)	
    cv2.rectangle(image,(pPump['2offx1'],pPump['y1']),(pPump['2offx2'],pPump['y2']),230,1)	
    cv2.rectangle(image,(pPump['2onx1'] ,pPump['y1']),(pPump['2onx2'] ,pPump['y2']),230,1)	
    cv2.rectangle(image,(pTanks['Hx1'],pTanks['fully1']),(pTanks['Hx2'],pTanks['fully2']),230,1)	
    cv2.rectangle(image,(pTanks['Hx1'],pTanks['lowy1'] ),(pTanks['Hx2'],pTanks['lowy2'] ),230,1)	
    cv2.rectangle(image,(pTanks['Lx1'],pTanks['fully1']),(pTanks['Lx2'],pTanks['fully2']),230,1)	
    cv2.rectangle(image,(pTanks['Lx1'],pTanks['lowy1'] ),(pTanks['Lx2'],pTanks['lowy2'] ),230,1)	

    return image

def cutLamp(binary,pWork,pPump,pTanks):
    working=binary[pWork['y1']:pWork['y2'],pWork['x1']	  :pWork['x2']]
    no1_off=binary[pPump['y1']:pPump['y2'],pPump['1offx1']:pPump['1offx2']]
    no1_on =binary[pPump['y1']:pPump['y2'],pPump['1onx1'] :pPump['1onx2'] ]
    no2_off=binary[pPump['y1']:pPump['y2'],pPump['2offx1']:pPump['2offx2']]
    no2_on =binary[pPump['y1']:pPump['y2'],pPump['2onx1'] :pPump['2onx2'] ]
    H_full =binary[pTanks['fully1']:pTanks['fully2'],pTanks['Hx1']:pTanks['Hx2']]
    H_low  =binary[pTanks['lowy1'] :pTanks['lowy2'], pTanks['Hx1']:pTanks['Hx2']]
    L_full =binary[pTanks['fully1']:pTanks['fully2'],pTanks['Lx1']:pTanks['Lx2']]
    L_low  =binary[pTanks['lowy1'] :pTanks['lowy2'], pTanks['Lx1']:pTanks['Lx2']]
    
    
    return [working,no1_off,no1_on,no2_off,no2_on,H_full,H_low,L_full,L_low]

def calcBW(bw_image,percent):
    image_size = bw_image.size
    whitePixels = cv2.countNonZero(bw_image)
    blackPixels = bw_image.size - whitePixels
    whiteAreaRatio = (whitePixels/image_size)*100#[%]
    # blackAreaRatio = (blackPixels/image_size)*100#[%]
    # print("White Area [%] : ", whiteAreaRatio)
    # print("Black Area [%] : ", blackAreaRatio)
    if whiteAreaRatio > percent:
        return '1'
    else:
        return '0'

def fileCreate(date,flag):
    if not os.path.exists(str(date[4:8])+'.txt'):
        if flag == 0:
            f=open(str(date[4:8])+'.txt',mode='w+')
            f.write("wrok No1_off No1_on No2_off No2_on HTank_full HTank_low LTank_full LTank_low\n")
            flag = 1
            return f
        f.close()
        # f=open(tmp[4:10]+'.txt',mode='w')
        f=open(str(date[4:8])+'.txt',mode='a+')
        f.write("wrok No1_off No1_on No2_off No2_on HTank_full HTank_low LTank_full LTank_low\n")
        return f

def writeFile(date,lamplist,f,percent):
    lampFlag=[]
    lampFlag.append(date[4:14])

    for bw_image in lampList:
        lampFlag.append(calcBW(bw_image,percent))
        f=open(str(date[4:8])+'.txt',mode='a')
    print(lampFlag)
    f.writelines(' '.join(lampFlag))
    f.writelines('\n')

pWork={
    'y1':75, 'y2':95,
    'x1':345,'x2':365}
pPump={
    'y1'    :175,'y2'    :195,
    '1offx1':330,'1offx2':350,
    '1onx1' :360,'1onx2' :380,
    '2offx1':385,'2offx2':405,
    '2onx1' :410,'2onx2' :430}
pTanks={
    'fully1':250,"fully2":270,
    "lowy1" :275,'lowy2' :300,
    "Hx1"   :345,'Hx2'   :365,
    'Lx1'	:400,'Lx2'	 :420}

os.makedirs('data', exist_ok=True)
cap = cv2.VideoCapture(0)

flag = 0
n    = 0
m    = 0

while True:
    ret, image = cap.read()
    showRectangle(image,pWork,pPump,pTanks)
    cv2.imshow('frame',image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if n == 30:
        date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        f = fileCreate(date,flag)
        binary = binaryCvt(image,240)
        binary = showRectangle(binary,pWork,pPump,pTanks)
        cv2.imshow('binary_Frame',binary)
        lampList = cutLamp(binary,pWork,pPump,pTanks)
        writeFile(date,lampList,f,10)
        n = 0
    if m == 1800:
        cv2.imwrite('{}_{}.{}'.format('data/image', datetime.datetime.now().strftime('%Y%m%d%H%M'), 'jpg'), image)
        m=0


    n +=1
    m +=2

cv2.destroyWindow('frame')

    