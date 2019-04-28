# coding=utf-8
import serial
import threading
import time
import sys

from thd import MyThread
from facedetect import FaceRecon
import BaseMovement

Send_Buff = []
ser =serial.Serial('COM3',115200,timeout=1)#这是我的串口，测试连接成功，没毛病


class Movement(FaceRecon):
	def __init__(self,path):
		FaceRecon.__init__(self,path)
		self.activate=False
		self.init_act = BaseMovement.HeadRightLeftControl485Send(0,100)
		ser.write(bytes(self.init_act))
		time.sleep(1)



	@classmethod
	def run(cls):
		return cls('database/haarcascades/haarcascade_frontalface_alt2.xml')


	def get_attr(self):
		t = MyThread(self.imag_show)
		t.start()

	def turn_or_not(self):

		buffer_index = 0
		NUM_WINDOW_CHUNKS = 30
		buff_flags = [0] * NUM_WINDOW_CHUNKS
		while True:
			print("x的坐标", self.x)
			self.turn = False
			time.sleep(0.1)
			if self.x < 100 or self.x > 400:
				self.active = True
			else:
				self.active = False
			# sys.stdout.write('1' if self.active else '_')
			buff_flags[buffer_index] = 1 if self.active else 0
			buffer_index += 1
			buffer_index %= NUM_WINDOW_CHUNKS
			# print(buff_flags)
			num_leftright = sum(buff_flags)
			if num_leftright > 0.96 * NUM_WINDOW_CHUNKS:  # 检测到的人脸在一定时间内均在一个方向，开始发动转动信号
				print("yes")
				self.turn = True
				break

	def movement(self):
		# while True:
			# time.sleep(3)
		if self.x < 100 and self.turn == True:
			# time.sleep(3)
			print("向左转")
			Out_Send_Cot = BaseMovement.HeadRightLeftControl485Send(15, 100)
			print(Out_Send_Cot)
			ser.write(bytes(Out_Send_Cot))
			time.sleep(3)
			Out_Send_Pos = BaseMovement.HeadRightLeftPosAngle()
			ser.write(bytes(Out_Send_Pos))
			time.sleep(0.1)

		if self.x > 400 and self.turn == True:
			print("向右转")
			Out_Send_Cot = BaseMovement.HeadRightLeftControl485Send(-15, 100)
			ser.write(bytes(Out_Send_Cot))
			time.sleep(3)
			Out_Send_Pos = BaseMovement.HeadRightLeftPosAngle()
			ser.write(bytes(Out_Send_Pos))
			time.sleep(0.1)

		if self.x >= 100 and self.x <= 400 and self.turn == False:
			print("在中间")
			BaseMovement.HeadRightLeftPosAngle()

class Receive():
	def __init__(self):
		self.state_machine =0  # 状态机 作为协议状态机的转换状态
		self.sumchkm =0  # 接收数据累加和
		self.m_ucData = []  # 接收数据保存
		self.lencnt = 0  # 接收数据计数器
		self.rcvcount = 0  # 数据包长度


	def jieshou(self):#接收函数
		# while True:
			while ser.inWaiting()>0:
				myout=ser.read(1) #串口接收数据,逐一字节接收
				print(myout)
				rcvdat =ord(myout)
				# rcvdat =''.join(map(lambda x:('0x' if len(hex(x))>=4 else '0x0')+hex(x)[2:],myout))
				# print(rcvdat==0xa5)
				if self.state_machine == 0:
					if rcvdat == 0xA5:  #接收到帧头第一个数据0xA5
						print("rcvdat0x",hex(rcvdat))
						self.state_machine =1
					else:
						self.state_machine =0  #状态机复位
				elif self.state_machine ==1:
					if rcvdat ==0xA5:  #接收到帧头第二个数据0xA5
						print("rcvdat0x", hex(rcvdat))
						self.state_machine = 2
					else:
						self.state_machine = 0  # 状态机复位
				elif self.state_machine ==2:
					self.sumchkm += rcvdat
					if rcvdat == 0x08: # 接收到帧头第三个数据ID0x08（摄像头）
						print("rcvdat0x", hex(rcvdat))
						self.state_machine = 3
					else:
						self.state_machine=0
				elif self.state_machine ==3:
					self.sumchkm += rcvdat  #接收到帧头第四个数据，数据包长度
					print("rcvdat0x", hex(rcvdat))
					self.rcvcount = rcvdat  # 数据包长度
					print("rcvcount0x",hex(self.rcvcount))
					self.state_machine =4
				elif self.state_machine ==4:
					self.sumchkm += rcvdat
					self.lencnt +=1
					self.m_ucData.append(rcvdat)   #数据保存
					print("rcvdat0x",hex(rcvdat))
					print("lencnt0x", hex(self.lencnt))
					if self.lencnt == int(self.rcvcount)-1:
						self.state_machine =5
				elif self.state_machine == 5:
					print("rcvdat0x",hex(rcvdat))
					print("sumchkm:0x",int(self.sumchkm))
					if self.sumchkm == rcvdat:  #判断校验和是否正确
						retval =1  #置标志，表示一个数据包接收到
						if self.m_ucData[0] == 0x31 and self.lencnt == 0x02:
							print("头部上下转动执行情况成功返回输出：")
							for i in range(0, self.lencnt):
								print("0x",hex(self.m_ucData[i]))
						elif self.m_ucData[0] == 0x32 and self.lencnt == 0x02:
							print("头部左右转动执行情况成功返回输出：")
							for i in range(0, self.lencnt):
								print("0x",hex(self.m_ucData[i]))
						elif self.m_ucData[0] == 0x33 and self.lencnt == 0x03:
							print("头部上下转动位置数据返回输出：")
							for i in range(0, self.lencnt):
								print("0x",hex(self.m_ucData[i]))
						elif self.m_ucData[0] == 0x34 and self.lencnt == 0x03:
							print("头部左右转动位置数据返回输出：")
							for i in range(0, self.lencnt):
								print("0x",hex(self.m_ucData[i]))

if __name__ == '__main__':
	rc = Receive()
	t1 = threading.Thread(target=rc.jieshou())
	t1.start()

	mv = Movement.run()
	mv.get_attr()
	while True:
		time.sleep(1)
		mv.turn_or_not()
		mv.movement()
		# rc.jieshou()


	# while True:
	# 	time.sleep(3)
	# 	movement(180)

	# while True:
	# 	rc.jieshou()
















