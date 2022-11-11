import turtle as tr
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
from ui import UI
from bricks import Bricks
import time


screen = tr.Screen()
screen.setup(width=1200, height=600)
screen.bgcolor('black')
screen.title('Breakout')
screen.tracer(0)


ui = UI()
ui.header()

score = Scoreboard(lives=5)
paddle = Paddle()
bricks = Bricks()


ball = Ball()

game_paused = False
playing_game = True


def pause_game():
	global game_paused
	game_paused = not game_paused

def restart_game():
	global playing_game, score, ui, bricks
	time.sleep(0.5)
	score.reset()
	score.set_lives(5)
	# bricks.bricks.clear()
	ball.reset()
	paddle.reset()
	bricks.reset()
	ui.clear()
	ui.header()
	# empty the list of bricks then refill it
	# bricks = Bricks()
	screen.update()
	playing_game = True
	print('Game Restarted', playing_game)
	game_loop()

screen.listen()
screen.onkey(key='Left', fun=paddle.move_left)
screen.onkey(key='Right', fun=paddle.move_right)
screen.onkey(key='space', fun=pause_game)
screen.onkey(key='r', fun=restart_game)

def game_reset():
	global ball, score, playing_game, ui
	ball.reset()
	paddle.reset()
	score.decrease_lives()
	if score.lives == 0:
		playing_game = False
		ui.game_over(win=False, score=score.score)
		score.reset()
		return
	ui.change_color()
	return

def check_collision_with_walls():

	global ball, score, playing_game, ui

	# detect collision with left and right walls:
	if ball.xcor() < -580 or ball.xcor() > 570:
		ball.bounce(x_bounce=True, y_bounce=False)
		return

	# detect collision with upper wall
	if ball.ycor() > 270:
		ball.bounce(x_bounce=False, y_bounce=True)
		return

	# detect collision with bottom wall
	# In this case, user failed to hit the ball
	# thus he loses. The game resets.
	if ball.ycor() < -280:
		game_reset()


def check_collision_with_paddle():

	global ball, paddle
	# record x-axis coordinates of ball and paddle
	paddle_x = paddle.xcor()
	ball_x = ball.xcor()

	# check if ball's distance(from its middle)
	# from paddle(from its middle) is less than
	# width of paddle and ball is below a certain
	#coordinate to detect their collision
	if ball.distance(paddle) < 110 and ball.ycor() < -250:

		# If Paddle is on Right of Screen
		if paddle_x > 0:
			if ball_x > paddle_x:
				# If ball hits paddles left side it
				# should go back to left
				ball.bounce(x_bounce=True, y_bounce=True)
				return
			else:
				ball.bounce(x_bounce=False, y_bounce=True)
				return

		# If Paddle is left of Screen
		elif paddle_x < 0:
			if ball_x < paddle_x:
				# If ball hits paddles left side it
				# should go back to left
				ball.bounce(x_bounce=True, y_bounce=True)
				return
			else:
				ball.bounce(x_bounce=False, y_bounce=True)
				return

		# Else Paddle is in the Middle horizontally
		else:
			if ball_x > paddle_x:
				ball.bounce(x_bounce=True, y_bounce=True)
				return
			elif ball_x < paddle_x:
				ball.bounce(x_bounce=True, y_bounce=True)
				return
			else:
				ball.bounce(x_bounce=False, y_bounce=True)
				return


def check_collision_with_bricks():
	global ball, score, bricks

	for brick in bricks.bricks:
		if ball.distance(brick) < 40:
			score.increase_score()
			brick.quantity -= 1
			# if brick.quantity == 0:
			# 	brick.clear()
			# 	brick.goto(3000, 3000)
			# 	bricks.bricks.remove(brick)
			brick.clear()
			brick.goto(3000, 3000)
			bricks.bricks.remove(brick)

			# detect collision from left
			if ball.xcor() < brick.left_wall:
				ball.bounce(x_bounce=True, y_bounce=False)

			# detect collision from right
			elif ball.xcor() > brick.right_wall:
				ball.bounce(x_bounce=True, y_bounce=False)

			# detect collision from bottom
			elif ball.ycor() < brick.bottom_wall:
				ball.bounce(x_bounce=False, y_bounce=True)

			# detect collision from top
			elif ball.ycor() > brick.upper_wall:
				ball.bounce(x_bounce=False, y_bounce=True)


def game_loop():
	while playing_game:
		# print('Game Running')

		if not game_paused:
			# print('game is not paused')
			# UPDATE SCREEN WITH ALL THE MOTION THAT HAS HAPPENED
			screen.update()
			time.sleep(0.01)
			ball.move()

			# DETECTING COLLISION WITH WALLS
			check_collision_with_walls()

			# DETECTING COLLISION WITH THE PADDLE
			check_collision_with_paddle()

			# DETECTING COLLISION WITH A BRICK
			check_collision_with_bricks()
			
			# DETECTING USER'S VICTORY
			if len(bricks.bricks) == 0:
				ui.game_over(win=True, score=score.score)
				break

		else:
			# print('Game Paused')
			ui.paused_status()

game_loop()

tr.mainloop()
