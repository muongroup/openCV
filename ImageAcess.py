import cv2
import glob
from matplotlib import pyplot as plt

def substImage(path):
    img_src1 = cv2.imread("../SubstImage.jpg", 1)
    img_src2 = cv2.imread(path, 1)

    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    fgmask = fgbg.apply(img_src1)
    fgmask = fgbg.apply(img_src2)

    return fgmask

def binaryCvt(path,thresh):
	image = cv2.imread(path,1)
	gray  = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

	ret, binary =cv2.threshold(gray,thresh,255,cv2.THRESH_BINARY)
	# ret, binary =cv2.threshold(gray,thresh,1,cv2.THRESH_OTSU)

	return binary
	# return gray

def cutLamp(binary):
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

	# print(pWork,pPump,pTanks)
 
	working=binary[pWork['y1']:pWork['y2'],pWork['x1']	  :pWork['x2']]
	no1_off=binary[pPump['y1']:pPump['y2'],pPump['1offx1']:pPump['1offx2']]
	no1_on =binary[pPump['y1']:pPump['y2'],pPump['1onx1'] :pPump['1onx2'] ]
	no2_off=binary[pPump['y1']:pPump['y2'],pPump['2offx1']:pPump['2offx2']]
	no2_on =binary[pPump['y1']:pPump['y2'],pPump['2onx1'] :pPump['2onx2'] ]
	H_full =binary[pTanks['fully1']:pTanks['fully2'],pTanks['Hx1']:pTanks['Hx2']]
	H_low  =binary[pTanks['lowy1'] :pTanks['lowy2'], pTanks['Hx1']:pTanks['Hx2']]
	L_full =binary[pTanks['fully1']:pTanks['fully2'],pTanks['Lx1']:pTanks['Lx2']]
	L_low  =binary[pTanks['lowy1'] :pTanks['lowy2'], pTanks['Lx1']:pTanks['Lx2']]

	cv2.rectangle(binary,(pWork['x1'],pWork['y1']),(pWork['x2'],pWork['y2']),230,1)	
	cv2.rectangle(binary,(pPump['1offx1'],pPump['y1']),(pPump['1offx2'],pPump['y2']),230,1)	
	cv2.rectangle(binary,(pPump['1onx1'] ,pPump['y1']),(pPump['1onx2'] ,pPump['y2']),230,1)	
	cv2.rectangle(binary,(pPump['2offx1'],pPump['y1']),(pPump['2offx2'],pPump['y2']),230,1)	
	cv2.rectangle(binary,(pPump['2onx1'] ,pPump['y1']),(pPump['2onx2'] ,pPump['y2']),230,1)	
	cv2.rectangle(binary,(pTanks['Hx1'],pTanks['fully1']),(pTanks['Hx2'],pTanks['fully2']),230,1)	
	cv2.rectangle(binary,(pTanks['Hx1'],pTanks['lowy1'] ),(pTanks['Hx2'],pTanks['lowy2'] ),230,1)	
	cv2.rectangle(binary,(pTanks['Lx1'],pTanks['fully1']),(pTanks['Lx2'],pTanks['fully2']),230,1)	
	cv2.rectangle(binary,(pTanks['Lx1'],pTanks['lowy1'] ),(pTanks['Lx2'],pTanks['lowy2'] ),230,1)	
 
	return [working,no1_off,no1_on,no2_off,no2_on,H_full,H_low,L_full,L_low],binary

def calcBW(bw_image,percent):
  image_size = bw_image.size
  whitePixels = cv2.countNonZero(bw_image)
  blackPixels = bw_image.size - whitePixels
  whiteAreaRatio = (whitePixels/image_size)*100#[%]
  blackAreaRatio = (blackPixels/image_size)*100#[%]
  print("White Area [%] : ", whiteAreaRatio)
  print("Black Area [%] : ", blackAreaRatio)
  if whiteAreaRatio > percent:
	  return '1'
  else:
	  return '0'

def draw(image):
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	ax1.imshow(binary, cmap = 'gray')
	ax1.tick_params(labelbottom = False, bottom = False)
	ax1.tick_params(labelleft = False, left = False)
	fig.tight_layout()
	plt.show()
	plt.close()

def writeFile(path,lamplist,f,percent):
	lampFlag=[]
	lampFlag.append(path[10:20])

	for bw_image in lampList:
		lampFlag.append(calcBW(bw_image,percent))
		# f=open(path[10:14]+'.txt','a')
	print(lampFlag)
	f.writelines(' '.join(lampFlag))
	f.writelines('\n')

pathList = glob.glob('image_*')
print(pathList)
print(pathList[0][10:14])

f=open(pathList[0][10:14]+'.txt',mode='w')
f.write("wrok No1_off No1_on No2_off No2_on HTank_full HTank_low LTank_full LTank_low\n")
f=open(pathList[0][10:14]+'.txt',mode='a')

for path in pathList:
  binary = binaryCvt(path,245)
#   binary = substImage(path)
  lampList,binary = cutLamp(binary)
#   draw(binary)
  writeFile(path,lampList,f,12)

f.close()