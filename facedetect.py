# -*- coding: utf-8 -*-
'''
@auther: Liya guo
@summary: 人脸检测
'''
import cv2
import os
import time
import threading
# 实例化人脸分类器
# face_cascade = cv2.CascadeClassifier('../database/haarcascades/haarcascade_frontalface_default.xml')
import numpy as np



class FaceRecon():
	def __init__(self,path):
		self.face_cascade= cv2.CascadeClassifier(path)
		self.video = cv2.VideoCapture(0)
		# print("width",self.video.get(3),"height", self.video.get(4))  # 默认width 640.0，height 480.0
		self.frame =None
		self.is_face = False
		self.quit = False
		self.num=1

	def capture_image(self):
		# 抓取一帧视频q
		ret, self.frame = self.video.read()
		# 在这个视频中循环遍历每个人人脸
		self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)


	def detection(self):
		self.faces = self.face_cascade.detectMultiScale(self.gray, 1.2, 8)
		if isinstance(self.faces,np.ndarray):
			self.is_face = True
			for (x, y, w, h) in self.faces:
				cv2.rectangle(self.frame, (x,y), (x+w,y+h), (0, 0, 255),4)
				return (x, y, w, h)
				# print("leftright",self.x,"  updown",self.y)
				# self.followface()

				# 将当前帧保存为图片
				# img_name = "%s/%d.jpg" % ('database\pic', self.num)
				# # print(img_name)
				# image = self.frame[self.y - 10: self.y + h + 10, self.x - 10: self.x + w + 10]
				# cv2.imwrite(img_name, image, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
				# self.num += 1
				# if self.num > 20:  # 如果超过指定最大保存数量退出循环
				#     self.quit= True
		else:
			self.is_face = False

	def calculate_offset(self):
		'''
		计算人脸再画面中的偏移量，
		偏移量取值范围：[-1, 1]
		'''
		if self.detection() is not None:
			x, y, w, h = self.detection()
			img_width = self.video.get(3)
			img_height = self.video.get(4)
			face_x = float(x + w/2.0)
			face_y = float(y + h/2.0)
			# 人脸再画面中心x轴上的偏移量
			offset_x = float(face_x / img_width - 0.5) * 2
			# 人脸再画面中心y轴上的偏移量
			offset_y = float(face_y / img_height - 0.5) * 2
			return (offset_x, offset_y)
		else:
			(offset_x, offset_y) = 0, 0
			return (offset_x, offset_y)



	def close(self):
		self.quit = True
		self.video.release()
		cv2.destroyAllWindows()

	def img_show(self):
		num = 1
		while not self.quit:
			# if not self.quit:
			self.capture_image()
			self.detection()
			cv2.imshow('Video', self.frame)
			# print(self.is_face)
			cv2.waitKey(1)
			# else:
			#     self.close()


if __name__ == '__main__':
	fr = FaceRecon('database/haarcascades/haarcascade_frontalface_default.xml')
	t = threading.Thread(target=fr.img_show)
	t.start()
	# t = threading.Thread(target=fr.imag_show)
    # t.start()

    # while 1:
    #     time.sleep(3)