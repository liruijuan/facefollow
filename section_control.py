# -*- coding: utf-8 -*-
'''
@auther: Li
@summary: section_control
'''
offset_dead_block = 0.2  # 偏移量死区大小
rightlef_kp = 40  # 控制舵机旋转的比例系数
last_rigthtleft_degree =0 # 上一次左右旋转舵机的角度
last_updown_degree = 0  # 上一次上下旋转舵机的角度

class SectionControl():
	def __init__(self):
		self.next_rightleft_degree = 0

	def HeadRightLeftControl(self, offset_x):
		'''
		头部左右旋转舵机的比例控制
		这里舵机使用开环控制
		'''

		# 设置最小阈值
		if abs(offset_x) < offset_dead_block:
			offset_x = 0
		# offset范围在-60 到60左右
		delta_degree = offset_x * rightlef_kp
		# 计算得到新的左右旋转舵机的角度
		self.next_rightleft_degree = last_rigthtleft_degree + delta_degree
		# 添加边界检测
		if self.next_rightleft_degree < -60:
			self.next_rightleft_degree = 0
		elif self.next_rightleft_degree > 60:
			self.next_rightleft_degree = 60

		return int(self.next_rightleft_degree)


	def HeadupdownControl(self, offset_y):
		'''
		头部上下旋转舵机的比例控制
		这里舵机使用开环控制
		'''

		# 设置最小阈值
		if abs(offset_y) < offset_dead_block:
			offset_y = 0
		# offset范围在-60 到60左右
		delta_degree = offset_y * rightlef_kp
		# 计算得到新的左右旋转舵机的角度
		next_updown_degree = last_updown_degree + delta_degree
		# 添加边界检测
		if next_updown_degree < -60:
			next_updown_degree = 0
		elif next_updown_degree > 60:
			next_updown_degree = 60
		return int(next_updown_degree)


