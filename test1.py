import serial
import BaseMovement


ser=serial.Serial("COM2",115200,timeout=1)
# Send_Buff =[0x5A,0x5A,0x08,0x02,0x33,0x3D]
# Send_Buff =[0X01,0X03,0X00,0X00,0X00,0X01,0X84,0X0A]
# Send_Buff =['0xA5','0xA5','0x08','0x03','0x32','0x02','0x3F']
Send_Buff=[0xA5, 0xA5, 0x08, 0x03, 0x32, 0x01, 0x3E]

# Out_Send_Cot = BaseMovement.HeadRightLeftControl485Send(60, 100)
# Out_Send_Cot=[90, 90, 8, 6, 50, 60, 0, 100, 0, 224]


# myout=b'Z' #读取串口传过来的字节流，这里我根据文档只接收7个字节的数据
# datas =''.join(map(lambda x:('0x' if len(hex(x))>=4 else '0x0')+hex(x)[2:],myout))
# print(datas)  #/x5a/x5a/x08/x02/x33/x3d

		
for i in range(0,100-1):
	# myinput=[bytes(map(ord, x)) for x in Send_Buff]

	myinput = bytes(Send_Buff)
	ser.write(myinput)
	print(ser.readline())

ser.close()