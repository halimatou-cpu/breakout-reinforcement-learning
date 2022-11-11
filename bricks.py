from turtle import Turtle
import random

COLOR_LIST = ['light blue', 'royal blue',
			'light steel blue', 'steel blue',
			'light cyan', 'light sky blue',
			'violet', 'salmon', 'tomato',
			'sandy brown', 'purple', 'deep pink',
			'medium sea green', 'khaki']

weights = [1, 2, 1, 1, 3, 2, 1, 4, 1,
		3, 1, 1, 1, 4, 1, 3, 2, 2,
		1, 2, 1, 2, 1, 2, 1]


class Brick(Turtle):
	def __init__(self, x_cor, y_cor):
		super().__init__()
		self.penup()
		self.shape('square')
		self.shapesize(stretch_wid=1.5, stretch_len=3)
		self.color(random.choice(COLOR_LIST))
		self.goto(x=x_cor, y=y_cor)

		self.quantity = random.choice(weights)

		# Defining borders of the brick
		self.left_wall = self.xcor() - 30
		self.right_wall = self.xcor() + 30
		self.upper_wall = self.ycor() + 15
		self.bottom_wall = self.ycor() - 15


class Bricks:
	def __init__(self):
		self.y_start = 0
		self.y_end = 240
		self.bricks = []
		self.create_all_lanes()

	def create_lane(self, y_cor):
		for i in range(-570, 570, 63):
		# for i in range(-450, 450, 63):
			brick = Brick(i, y_cor)
			self.bricks.append(brick)

	def create_all_lanes(self):
		for i in range(self.y_start, self.y_end, 32):
			print(i)
			self.create_lane(i)

	def reset(self):
		for brick in self.bricks:
			brick.clear()
			brick.goto(3000, 3000)
		self.bricks.clear()
		self.create_all_lanes()
