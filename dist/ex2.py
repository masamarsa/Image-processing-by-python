import os
os.environ["OPENCV_VIDEOID_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import numpy

# 保存先のフォルダ (フルパス指定) #
## 課題1 ##
FOLDER_PATH1 = "C:/Users/ce2s/Desktop/Thu12/img/ex1"
## 課題2 ##
FOLDER_PATH2 = "C:/Users/ce2s/Desktop/Thu12/img/ex2"
## 課題3 ##
FOLDER_PATH3 = "C:/Users/ce2s/Desktop/Thu12/img/ex3"
# conda terminalのカーネルの変更: conda activate 変更先のカーネル名 #

# カメラの設定 #
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc("M", "P", "4", "V"))

# 課題1 #
def Subject1():
	# ここから -------------------------------------------------------------------------
	def changeValue(s, a):
		while True:
			s = int(input(f"sampleLow is equal to {s}. Input the number of sampleLow."))
			a = float(input(f"areaLow is equal to {a}. Input the number of areaLow."))
			print(f"sampleLow is equal to {s}.")
			print(f"areaLow is equal to {a}.")
			che = input("Do you agree this change? [y/n]>")
			if che == "y":
				break
		return s, a
	# ここまでは、レポートには不要 ---------------------------------------------------------

	sampleLow = 700
	areaLow = 12000.0
	back = None
	while True:
		rtn, frame = cap.read()
		if not rtn:
			print("Read failed!")
			return
		# まず背景を取り込む #
		if back is None:
			cv2.imshow("frame", frame)
			key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
				break
			if key == ord('b'):
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				back = gray.copy().astype("float")
			continue
		# グレースケールして、ガウスのブラーする #
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray, (1, 1), 1)
		# 移動平均を更新 #
		cv2.accumulateWeighted(blur, back, 0.6)
		# 差分処理 #
		frameDelta = cv2.absdiff(blur, cv2.convertScaleAbs(back))
		# 二値化 #
		thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]
		# 白の領域を探す #
		contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
		# 四角の枠を付ける #
		for i in range(len(contours)):
			if len(contours[i]) > sampleLow:
				if cv2.contourArea(contours[i]) < areaLow:
					continue
				x, y, w, h = cv2.boundingRect(contours[i])
				cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
		# 結果表示 #
		cv2.imshow("frame", frame)
		cv2.imshow("thresh", thresh)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			break
		# ここから ----------------------------------------------------------
		if key == ord('s'):
			cv2.imwrite(f"{FOLDER_PATH1}/frame1.jpg", frame)
			cv2.imwrite(f"{FOLDER_PATH1}/thresh1.jpg", thresh)
			f = open(f"{FOLDER_PATH1}/values1.txt", 'w', encoding='UTF-8')
			f.writelines("result:")
			f.writelines(f"sampleLow= {sampleLow}")
			f.writelines(f"areaLow=   {areaLow}")
			f.close()
		if key == ord('c'):
			sampleLow, areaLow = changeValue(sampleLow, areaLow)
		# ここまでは、レポートには不要 ----------------------------------------
	cv2.destroyAllWindows()

def Subject1_2():
	# ここから -------------------------------------------------------------------------
	def changeValue(s, a, t):
		while True:
			s = int(input(f"sampleLow is equal to {s}. Input the number of sampleLow."))
			a = float(input(f"areaLow is equal to {a}. Input the number of areaLow."))
			t = float(input(f"areaLow is equal to {t}. Input the number of areaLow."))
			print(f"sampleLow is equal to {s}.")
			print(f"areaLow is equal to {a}.")
			che = input("Do you agree this change? [y/n]>")
			if che == "y":
				break
		return s, a, t
	# ここまでは、レポートには不要 ---------------------------------------------------------

	sampleLow = 700
	areaLow = 12000.0
	th = 30
	back = None
	fileNum = 1
	while True:
		rtn, frame = cap.read()
		if not rtn:
			print("Read failed!")
			return
		# まず背景を取り込む #
		if back is None:
			cv2.imshow("frame", frame)
			key = cv2.waitKey(1) & 0xFF
			if key == ord('q'):
				break
			if key == ord('b'):
				back = frame.copy()
			continue
		# グレースケールして、ガウスのブラーでぼかし処理する #
		# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# blur = cv2.GaussianBlur(frame, (1, 1), 1).astype("float32")
		# 移動平均を更新 #
		# cv2.accumulateWeighted(blur, back, 0.6)
		# 差分処理 #
		absDiff = cv2.absdiff(frame, back)
		absDiff_gray = cv2.cvtColor(absDiff, cv2.COLOR_BGR2GRAY)
		mask = cv2.threshold(absDiff_gray, th, 255, cv2.THRESH_BINARY)[1]
		withoutBack = cv2.bitwise_and(frame, frame, mask=mask)
		# 二値化 #
		# thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]
		# # 白の領域を探す #
		# contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
		# # 四角の枠を付ける #
		# for i in range(len(contours)):
		# 	if len(contours[i]) > sampleLow:
		# 		if cv2.contourArea(contours[i]) < areaLow:
		# 			continue
		# 		x, y, w, h = cv2.boundingRect(contours[i])
		# 		cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
		# 結果表示 #
		cv2.imshow("frame", frame)
		cv2.imshow("frame", withoutBack)
		# cv2.imshow("thresh", thresh)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			break
		# ここから ----------------------------------------------------------
		if key == ord('s'):
			cv2.imwrite(f"{FOLDER_PATH1}/frame{fileNum}.jpg", frame)
			cv2.imwrite(f"{FOLDER_PATH1}/withoutBack{fileNum}.jpg", withoutBack)
			f = open(f"{FOLDER_PATH1}/values{fileNum}.txt", 'w', encoding='UTF-8')
			f.writelines("result:\n")
			f.writelines(f"sampleLow= {sampleLow}\n")
			f.writelines(f"areaLow=   {areaLow}\n")
			f.writelines(f"th=        {th}\n")
			f.close()
			fileNum += 1
		if key == ord('c'):
			sampleLow, areaLow, th = changeValue(sampleLow, areaLow, th)
		# ここまでは、レポートには不要 ----------------------------------------
	cv2.destroyAllWindows()

# 課題2 #
def Subject2():
	# ここから ---------------------------------------------------------------------------
	def changeValues(th, l, u):
		while True:
			th = int(input(f"thresh is equal to {th}. Input the number of thresh.>"))
			l = int(input(f"areaLow is equal to {l}. Input the number of areaLow.>"))
			u = int(input(f"areaUp is equal to {u}. Input the number of areaUp.>"))
			print(f"thresh = {th}.")
			print(f"sampleLow = {l}.")
			print(f"areaLow = {u}.")
			che = input("Do you agree this change? [y/n]>")
			if che == "y":
				break
		return th, l, u
	# ここまでは、レポートには不要 ---------------------------------------------------------

	areaLow = 7
	areaUp = 10
	thresh = 100
	fileNum = 1
	while True:
		rtn, frame = cap.read()
		if not rtn: # 読み込めなかったら終了 #
			print("Read failed!")
			break
		# 色を反転
		reverse = cv2.bitwise_not(frame)
		# マスクのしきい値
		lower = numpy.array([0, 0, 0])
		upper = numpy.array([thresh, thresh, thresh])
		mask = cv2.inRange(frame, lower, upper)
		# フレームをマスク #
		frameOut = cv2.bitwise_and(reverse, reverse, mask=mask)
		# グレースケールして二値化 #
		frameOut = cv2.cvtColor(frameOut, cv2.COLOR_BGR2GRAY)
		frameBin = cv2.threshold(frameOut, 0, 255, cv2.THRESH_BINARY)[1]
		# 白の領域を探す #
		contours = cv2.findContours(frameBin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
		frameOut = frame.copy()
		count = 0
		# 個数のカウントとマーク #
		for i in range(len(contours)):
			approx = cv2.approxPolyDP(contours[i], cv2.arcLength(contours[i], True) * 0.02, True)
			if areaLow <= len(approx) <= areaUp:
				x, y, w, h = cv2.boundingRect(contours[i])
				frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
				frameOut = cv2.drawContours(frameOut, [approx], 0, (0, 255, 0), 2)
				count += 1
		# 結果出力 #
		cv2.putText(frame, f"Black: {count}", (3, 35), cv2.FONT_HERSHEY_PLAIN, 3.0, (255, 0, 0), 4, cv2.LINE_AA)
		cv2.imshow("frame", frame)
		cv2.imshow("frameOut", frameOut)
		cv2.imshow("frameBin", frameBin)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'): # 終了する #
			break
		# ここから ----------------------------------------------------------
		if key == ord('s'): # 結果保存 #
			cv2.imwrite(f"{FOLDER_PATH2}/frame{fileNum}.jpg", frame)
			cv2.imwrite(f"{FOLDER_PATH2}/frameOut{fileNum}.jpg", frameOut)
			cv2.imwrite(f"{FOLDER_PATH2}/frameBin{fileNum}.jpg", frameBin)
			f = open(f"{FOLDER_PATH2}/values{fileNum}.txt", 'w', encoding='UTF-8')
			f.writelines("result:\n")
			f.writelines(f"thresh= {thresh}\n")
			f.writelines(f"areaLow= {areaLow}\n")
			f.writelines(f"areaUp= {areaUp}\n")
			f.close()
			fileNum += 1
		if key == ord('c'): # 実験のためだけの便利機能のため、レポートには不要 #
			thresh, areaLow, areaUp= changeValues(thresh, areaLow, areaUp)
		# ここまでは、レポートには不要 ----------------------------------------
	cv2.destroyAllWindows()

# 課題3 #
def Subject3():
	# 赤色の範囲 #
	lowerR = numpy.array([0, 90, 0])
	upperR = numpy.array([13, 255, 255])
	# 青色の範囲 #
	lowerB = numpy.array([80, 70, 0])
	upperB = numpy.array([150, 255, 255])

	# ここから -----------------------------------------------------------------------------------------------
	def changeValue(l, u):
		while True:
			for i in range(3):
				lowerR[i] = int(input(f"lowerR[{i}] is equal to {lowerR[i]}. Input the number of lowerR[{i}].>"))
			for i in range(3):
				upperR[i] = int(input(f"upperR[{i}] is equal to {upperR[i]}. Input the number of upperR[{i}].>"))
			for i in range(3):
				lowerB[i] = int(input(f"lowerB[{i}] is equal to {lowerB[i]}. Input the number of lowerB[{i}].>"))
			for i in range(3):
				upperB[i] = int(input(f"upperB[{i}] is equal to {upperB[i]}. Input the number of upperB[{i}].>"))
			l = int(input(f"areaLow is equal to {l}. Input the number of areaLow.>"))
			u = int(input(f"areaUp is equal to {u}. Input the number of areaUp.>"))
			print("lowerR:  [{:3}, {:3}, {:3}]".format(lowerR[0], lowerR[1], lowerR[3]))
			print("lowerR:  [{:3}, {:3}, {:3}]".format(upperR[0], upperR[1], upperR[3]))
			print("lowerR:  [{:3}, {:3}, {:3}]".format(lowerB[0], lowerB[1], lowerB[3]))
			print("lowerR:  [{:3}, {:3}, {:3}]".format(upperB[0], upperB[1], upperB[3]))
			print(f"areaLow: {l}")
			print(f"areaUp:  {u}")
			che = input("Do you agree this change? [y/n]>")
			if che == "y":
				break
		return l, u
	# ここまでは、レポートには不要 -----------------------------------------------------------------------------

	areaLow = 7
	areaUp = 9
	while True:
		ret, frame = cap.read()
		if not ret: # 読み込めなかったら終了 #
			print("Read failed!")
			return
		# BGRからHSVへ変換 #
		frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		# 赤と青でそれぞれマスク #
		maskR = cv2.inRange(frame_hsv, lowerR, upperR)
		maskB = cv2.inRange(frame_hsv, lowerB, upperB)
		# 赤と青の領域を探す #
		contoursR = cv2.findContours(maskR, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
		contoursB = cv2.findContours(maskB, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
		counterR = 0
		counterB = 0
		frameOut = frame.copy()
		# 赤の個数をカウントしてマーク #
		for i in range(len(contoursR)):
			approx = cv2.approxPolyDP(contoursR[i], cv2.arcLength(contoursR[i], True) * 0.02, True)
			if areaLow <= len(approx) <= areaUp:
				x, y, w, h = cv2.boundingRect(contoursR[i])
				frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 4)
				frameOut = cv2.drawContours(frameOut, [approx], 0, (0, 0, 255), 2)
				counterR += 1
		# 青の個数をカウントしてマーク #
		for i in range(len(contoursB)):
			approx = cv2.approxPolyDP(contoursB[i], cv2.arcLength(contoursB[i], True) * 0.02, True)
			if areaLow <= len(approx) <= areaUp:
				x, y, w, h = cv2.boundingRect(contoursB[i])
				frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
				frameOut = cv2.drawContours(frameOut, [approx], 0, (255, 0, 0), 2)
				counterB += 1
		# 結果出力 #
		cv2.putText(frame, f"Red : {counterR}", (3, 35), cv2.FONT_HERSHEY_PLAIN, 3.0, (0, 0, 255), 4, cv2.LINE_AA)
		cv2.putText(frame, f"Blue: {counterB}", (3, 70), cv2.FONT_HERSHEY_PLAIN, 3.0, (255, 0, 0), 4, cv2.LINE_AA)
		cv2.imshow("frame", frame)
		cv2.imshow("frameOut", frameOut)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			break
		# ここから ----------------------------------------------------------
		if key == ord('s'): # 結果保存 #
			cv2.imwrite(f"{FOLDER_PATH3}/frame.jpg", frame)
			cv2.imwrite(f"{FOLDER_PATH3}/frameOut.jpg", frameOut)
			f = open(f"{FOLDER_PATH3}/values.txt", 'w', encoding='UTF-8')
			f.writelines("result:\n")
			f.writelines(f"lowerR=  {lowerR}\n")
			f.writelines(f"upperR=  {upperR}\n")
			f.writelines(f"lowerB=  {lowerB}\n")
			f.writelines(f"upperR=  {upperB}\n")
			f.writelines(f"areaLow= {areaLow}\n")
			f.writelines(f"areaUp=  {areaUp}\n")
			f.close()
		if key == ord('c'): # 実験のためだけの便利機能のため、レポートには不要 #
			areaLow, areaUp = changeValue(areaLow, areaUp)
		# ここまでは、レポートには不要 ----------------------------------------
	cv2.destroyAllWindows()

def main():
	# 画像の読み込みはフルパス #
	startMenu = cv2.imread("C:/Users/ce2s/Desktop/Thu12/img/mainMenu.jpg")
	cv2.imshow("Start Menu", startMenu)
	while True:
		key = cv2.waitKey(1) & 0xFF
		if key == 27: # ESCキーで終了 #
			break
		if key == ord('1'): # 課題1 #
			cv2.destroyWindow("Start Menu")
			Subject1()
			cv2.imshow("Start Menu", startMenu)
		if key == ord('4'): # 課題1 #
			cv2.destroyWindow("Start Menu")
			Subject1_2()
			cv2.imshow("Start Menu", startMenu)
		if key == ord('2'): # 課題2 #
			cv2.destroyWindow("Start Menu")
			Subject2()
			cv2.imshow("Start Menu", startMenu)
		if key == ord('3'): # 課題3 #
			cv2.destroyWindow("Start Menu")
			Subject3()
			cv2.imshow("Start Menu", startMenu)
	cap.release()
	cv2.destroyAllWindows()

main()