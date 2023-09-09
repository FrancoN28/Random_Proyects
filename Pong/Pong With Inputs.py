import pygame,sys
import random

#display variables:
height = 600
width = 800

# Colours
WHITE = (255,255,255)
GREY = (161,161,161)

pygame.init()

bit_font = pygame.font.Font('8-BIT WONDER.ttf',45)
bit_font_lower = pygame.font.Font('8-BIT WONDER.ttf',30)
bit_font_mini = pygame.font.Font('8-BIT WONDER.ttf',15)

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Pong')

class Player(pygame.sprite.Sprite):
	def __init__(self,player):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface((15,100))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()

		initial_posx = [(width-50),(50)]

		self.rect.centerx = initial_posx[player-1]
		self.rect.centery = height/2

		self.speed = 12

		self.score = 0
		self.score_text = bit_font.render(str(self.score),0,(255,255,255),(0,0,0))

		if player == 1:
				self.name = 'Player 1'
		else:
			self.name = 'Player 2'

		self.name_text = bit_font_mini.render(self.name,0,(255,255,255),(0,0,0))
		

	def move(self,direction):
		if direction == 'up':
			self.rect.centery -= self.speed

		elif direction == 'down':
			self.rect.centery += self.speed

		self.check_display()

	def check_display(self): # check if the bar is in the margin
		if self.rect.top < 0:
			self.rect.top = 0
		elif self.rect.bottom > height:
			self.rect.bottom = height

class Ball(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.Surface((15,15))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()

		self.initial_position = (width/2,height/2)

		self.rect.center = self.initial_position

		#directionx = 1 --> right
		#directionx = -1 --> left
		self.direction_x = random.choice([-1,1])
		#directiony > 0 --> down
		#directiony < 0 --> up
		self.direction_y = round(random.random(),3)

		self.speed = 10     
		
	def bouncex(self,player):

		if player.name == 'Player 1':
			self.direction_x = -1
		else: self.direction_x = 1

		self.direction_y = (self.rect.centery-player.rect.centery)/50 #the bigger the divider, the smaller the angle of bounce (64 = 45%)

	def check_bouncey(self):
		if self.rect.top <= 0: 
			self.direction_y *= -1
			self.rect.top = 1
		elif self.rect.bottom >= 600:
			self.direction_y *= -1
			self.rect.bottom = 599
	
	def move(self):
		self.rect.centerx += self.direction_x*self.speed
		self.rect.centery += self.direction_y*self.speed

	def check_point(self,player1,player2): 
		if self.rect.right <= 0:
			player1.score += 1
			player1.score_text = bit_font.render(str(player1.score),0,(255,255,255),(0,0,0))
			self.reappear()
		elif self.rect.left >= 800:
			player2.score += 1
			player2.score_text = bit_font.render(str(player2.score),0,(255,255,255),(0,0,0))
			self.reappear()

	def reappear(self):
		self.rect.center = self.initial_position
		self.direction_x = random.choice([-1,1])
		self.direction_y = round(random.random(),3)

class InputBox:
	def __init__(self, x, y, w, h, text = ''):

		self.text = text
		self.colour = GREY
		self.txt_surface = bit_font_lower.render(self.text,True,WHITE) #render the text
		self.rect = pygame.Rect(x,y,h,w)
		self.rect.w = self.txt_surface.get_width()+10
		self.rect.h = self.txt_surface.get_height()+10
		self.active = False
		
	def handle_event(self,event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos): #check if cursor is on the box
				self.active = not self.active
			else:
				self.active = False
			self.colour = WHITE if self.active else GREY
		if event.type == pygame.KEYDOWN:
			if self.active:
				if event.key == pygame.K_BACKSPACE:
					self.text  = self.text[:-1]
				else: 
					self.text += event.unicode #add the corresponding letter

				self.txt_surface = bit_font_lower.render(self.text,True,WHITE) #change the text
				#resize the box
				self.rect.w = self.txt_surface.get_width()+10

	def draw(self,screen):
		screen.blit(self.txt_surface , (self.rect.x+7,self.rect.y+5))
		pygame.draw.rect(screen,self.colour,self.rect,2)


def pong(): #game

	clock = pygame.time.Clock()

	all_sprites = pygame.sprite.Group()
	players_sprites = pygame.sprite.Group()

	player1 = Player(1)
	all_sprites.add(player1)
	player2 = Player(2)
	all_sprites.add(player2)

	players_sprites.add(player1)
	players_sprites.add(player2)

	ball = Ball()
	all_sprites.add(ball)

	input_ball_s = InputBox(100,400,50,40,'10')
	input_player_s = InputBox(600,400,50,40,'12')
	input_boxes = [input_ball_s,input_player_s]

	running = True
	pause = False
	ended = False
	intro = True
	playing = False

	while running:
		# Loop at 30 fps
		clock.tick(60)

		screen.fill((0,0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if intro:
						intro = False
						playing = True
						ball.speed = int(input_ball_s.text)
						player1.speed = int(input_player_s.text)
						player2.speed = int(input_player_s.text)
					elif pause:
						pause = False
						playing = True
					elif ended:
						pong()
					elif playing:
						pause = True
						playing = False
			
			if intro:
				for box in input_boxes:
					box.handle_event(event)

		if playing:
			# Bouncing on the players:
			for player in players_sprites:
				if ball.rect.colliderect(player.rect):
					ball.bouncex(player)
				if player.score == 10:
					winner = player.name
					playing = False
					ended = True

			# Getting a list with the pressed keys
			key_states = pygame.key.get_pressed()

			if key_states[pygame.K_k]:# Player1
				player1.move('up')
			if key_states[pygame.K_m]:
				player1.move('down')

			if key_states[pygame.K_s]:# Player2
				player2.move('up')
			if key_states[pygame.K_x]:
				player2.move('down')

			#bouncing on roof or floor
			ball.check_bouncey()

			#check if the ball passed the limits
			ball.check_point(player1,player2)

			ball.move()

			# Draw 
			all_sprites.draw(screen)
			pygame.draw.line(screen,WHITE,(width/2,0),(width/2,height),3)

		# Check status of the game
		if ended:
			end_text = bit_font.render('Game has ended',0,(255,255,255),(0,0,0))
			end_text2 = bit_font.render(winner+ ' won',0,(255,255,255),(0,0,0))
			replay = bit_font_lower.render('Press SPACE to play again',0,(255,255,255),(0,0,0))
			screen.blit(end_text,(100,250))
			screen.blit(end_text2,(150,300))
			screen.blit(replay,(75,375))

		if intro:
			start_game = bit_font_lower.render('Press SPACE to start playing',0,(255,255,255),(0,0,0))
			screen.blit(start_game, (25,250))
			start_game = bit_font_mini.render('Change ball speed',0,(255,255,255),(0,0,0))
			screen.blit(start_game, (30,375))
			start_game = bit_font_mini.render('Change player speed',0,(255,255,255),(0,0,0))
			screen.blit(start_game, (500,375))
			start_game = bit_font_mini.render('Player 1 moves with S and X ',0,(255,255,255),(0,0,0))
			screen.blit(start_game, (225,475))
			start_game = bit_font_mini.render('Player 2 moves with K and M',0,(255,255,255),(0,0,0))
			screen.blit(start_game, (225,500))         
            
			for box in input_boxes:
				box.draw(screen)


		if pause:
			start_game = bit_font_lower.render('Press SPACE to resume',0,(255,255,255),(0,0,0))
			screen.blit(start_game, (100,300))

		# Print text with names and scores
		screen.blit(player1.score_text,(575,100))
		screen.blit(player2.score_text,(175,100))
		screen.blit(player1.name_text,(675,25))
		screen.blit(player2.name_text,(25,25))

		# Update the display
		pygame.display.update()


if __name__ == '__main__': 
    pong()
 

