"""
二、主摄像头舵机通讯协议
控制上下的舵机ID为1，上下运动范围为（-60°- 60°），向下为正向上为负，
控制左右的舵机ID为2，左右运动范围为（-60°- 60°），向左为正向右为负，
速度范围（1—200）该值最大值可为0x3ff，表示角速度 114 RPM。最小角速度设为 1。如设为 0，舵机将以电压能提供的最大速度运动。
1、设定1号舵机的运动角度和速度
5A 5A 08 06 31 aL aH sL sH SUM
前两个字节表示角度，后两个字节表示速度。
向下40°速度100：5A 5A 08 06 31 28 00 64 00 CB
向上40°速度100：5A 5A 08 06 31 D8 FF 64 00 7A
复位状态速度100：5A 5A 08 06 31 00 00 64 00 A3
当舵机转到位时控制器回复：A5 A5 08 03 31 01 3D
如果转动过程中出现无法转到位的情况回复：A5 A5 08 03 31 02 3E
2、设定2号舵机的运动角度和速度
5A 5A 08 06 32 aL aH sL sH SUM
前两个字节表示角度，后两个字节表示速度。
向左40°速度100：5A 5A 08 06 32 28 00 64 00 CC
向右40°速度100：5A 5A 08 06 32 D8 FF 64 00 7B
复位状态速度100：5A 5A 08 06 32 00 00 64 00 A4
当舵机转到位时控制器回复：A5 A5 08 03 32 01 3E
如果转动过程中出现无法转到位的情况回复：A5 A5 08 03 32 02 3F
3、读取1号舵机当前位置
5A 5A 08 02 33 3D
1号舵机收到指令后立刻回复当前位置：A5 A5 08 04 33 aL aH SUM
4、读取2号舵机当前位置
5A 5A 08 02 34 3E
2号舵机收到指令后立刻回复当前位置：A5 A5 08 04 34 aL aH SUM
"""


def Get_Sum(Send_Buff, len):
	sum = 0
	for i in range(0, len):
		sum += Send_Buff[i+2]  # 将16进制转化为10进制进行计算求和
		# print(sum)

	return sum

def HeadRightLeftControl485Send(m_Angle,m_rotatespeed):
	Send_Buff = []
	if m_Angle >= 0:
		# in_buff_m_Angle = hex(m_Angle) # 将数据转成十六进制字符串
		move_attr = [0x5A, 0x5A, 0x08, 0x06, 0x32, m_Angle, 0x00, m_rotatespeed, 0x00]
		for i in range(0,9):
			Send_Buff.append(move_attr[i])

	if m_Angle < 0:
		# in_buff_m_Angle = hex(16 ** 7 - 15)[-2:]
		m_Angle = 256 + m_Angle
		move_attr = [0x5A, 0x5A, 0x08, 0x06, 0x32, m_Angle, 0xFF, m_rotatespeed, 0x00]

		for i in range(0, 9):
			Send_Buff.append(move_attr[i])

	# SUM =0
	SUM = Get_Sum(Send_Buff, 7)
	Send_Buff.append(SUM)
	Send_Buff_End= ''.join(map(lambda x: ('0x' if len(hex(x)) >= 4 else '0x0') + hex(x)[2:], Send_Buff))
	return Send_Buff_End

def HeadUpDownPosAngle(Send_Buff):
	Send_Buff = []
	move_attr =[0x5A,0x5A,0x08,0x02,0x33,0x3D]
	for i in range (0, 5):
		Send_Buff.append(move_attr[i])
	Send_Buff_End = ''.join(map(lambda x: ('0x' if len(hex(x)) >= 4 else '0x0') + hex(x)[2:], Send_Buff))
	return Send_Buff_End


def HeadRightLeftPosAngle():
	Send_Buff = []
	move_attr = [0x5A, 0x5A, 0x08, 0x02, 0x34, 0x3E]
	for i in range(0, 5):
		Send_Buff.append(move_attr[i])
	Send_Buff_End = ''.join(map(lambda x: ('0x' if len(hex(x)) >= 4 else '0x0') + hex(x)[2:], Send_Buff))
	return Send_Buff_End

if __name__ == '__main__':
	Send_Buff=[]
	OUT_Sendbuff=HeadRightLeftControl485Send(60,100)
	print(OUT_Sendbuff)


	# OUT_Sendbuff1 = HeadRightLeftPosAngle()
	# print(OUT_Sendbuff1)



