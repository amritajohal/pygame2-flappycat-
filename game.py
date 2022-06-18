import pygame, sys, random 


'''
hi!! this is my final project for comp programming 12
it is based off of the 'flappy bird' tutorial --> then i added 6 smaller customizations to the basic game 
these will be marked as MINI CHANGE
i also drew inspiration from the 'snake' and 'intro' tutorials --> i added 3 bigger unique changes i found thru there
these will be marked as MAJOR CHANGE

'''
pygame.display.set_caption("flappycat !!") #top text 

def draw_floor(): #dimensions 
	screen.blit(floor_surface,(floor_x_pos,900))
	screen.blit(floor_surface,(floor_x_pos + 576,900))

def create_floating_hearts(): #rectangles for floating hearts 
	random_floating_hearts_pos = random.choice(floating_hearts_height)
	bottom_floating_hearts = floating_hearts_surface.get_rect(midtop = (700,random_floating_hearts_pos))
	top_floating_hearts = floating_hearts_surface.get_rect(midbottom = (700,random_floating_hearts_pos - 300))
	return bottom_floating_hearts,top_floating_hearts 

def move_floating_heartss(floating_heartss): #controls how hearts move across the screen 
	for floating_hearts in floating_heartss:
		floating_hearts.centerx -= 5 #x-axis

		if floating_hearts.centerx < 100: #major change no. 1: hearts zigzag across the screen 
			floating_hearts.centery += 3 #y-axis 
		elif floating_hearts.centerx > 200 and floating_hearts.centerx < 300:
			floating_hearts.centery += 3
		elif floating_hearts.centerx > 400 and floating_hearts.centerx < 500:
			floating_hearts.centery += 3
		elif floating_hearts.centerx > 600 and floating_hearts.centerx < 700:
			floating_hearts.centery += 3
		elif floating_hearts.centerx > 800 and floating_hearts.centerx < 900:
			floating_hearts.centery += 3
		else:
			floating_hearts.centery -= 3 #up for every other #100, then down 

	return floating_heartss
  
def draw_floating_heartss(floating_heartss): #next few functions control/ draw hearts in rects 
	for floating_hearts in floating_heartss:
		if floating_hearts.bottom >= 1024:
			screen.blit(floating_hearts_surface,floating_hearts)
		else:
			flip_floating_hearts = pygame.transform.flip(floating_hearts_surface,False,True)
			screen.blit(flip_floating_hearts,floating_hearts
			)

def remove_floating_heartss(floating_heartss):
	for floating_hearts in floating_heartss:
		if floating_hearts.centerx == -600:
			floating_heartss.remove(floating_hearts)
	return floating_heartss

def check_collision(floating_heartss): #game ends when cat crashes into a heart 
	for floating_hearts in floating_heartss:
		if cat_rect.colliderect(floating_hearts):
			death_sound.play()
			return False

	if cat_rect.top <= -100 or cat_rect.bottom >= 900:
		return False

	return True

def rotate_cat(cat): #cat movement 
	new_cat = pygame.transform.rotozoom(cat,-cat_movement * 3,1)
	return new_cat 

def cat_animation():
	new_cat = cat_frames[cat_index]
	new_cat_rect = new_cat.get_rect(center = (100,cat_rect.centery))
	return new_cat,new_cat_rect

def score_display(game_state): #keeps track of scores and jump types. places text accordingly 
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
		global text
		text = game_font.render(f'{str(tipe)}', True, (255, 100, 100))
		pos = score_surface.get_rect(center = (80,50))
		screen.blit(text, pos) #major change no. 2: displays type of jump after each jump

	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,70))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score): #replaces higest score 
	if score > high_score:
		high_score = score
	return high_score

pygame.mixer.pre_init(frequency = 4100, size = 16, channels = 1, buffer = 12) #music controls 
pygame.init()
screen = pygame.display.set_mode((576,900))
clock = pygame.time.Clock()
game_font = pygame.font.Font('HeartyGeelynEditsMarker-le2d.ttf',60) #heart shaped font !!

#mini change no.1: game variables differ (the game is slightly easier now)
gravity = 0.3
cat_movement = 0
game_active = True
score = 0
high_score = 0
tipe = '' 

bg_surface = pygame.image.load('hearts2.png').convert() #backdrop 
bg_surface = pygame.transform.scale2x(bg_surface) 

width = 500
height = 40

floor_surface = pygame.image.load('base.png').convert() #base floor
floor_surface = pygame.transform.scale2x(floor_surface) #i am not showing the image, but using it to map out the distance 
floor_x_pos = 0

cat_downflap = pygame.transform.scale2x(pygame.image.load('cat4.png').convert_alpha()) #cat character 
cat_frames = [cat_downflap, cat_downflap, cat_downflap] #i made them all the same since i dont want my cat to change position
cat_index = 0 
cat_surface = cat_frames[cat_index]
cat_rect = cat_surface.get_rect(center = (100,512))

catFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(catFLAP,200)

floating_hearts_surface = pygame.image.load('float2.png') #major change no. 3: the cat can go above or below the obstables, instead of just over/under 
floating_hearts_surface = pygame.transform.scale2x(floating_hearts_surface)
floating_hearts_list = []
SPAWNfloating_hearts = pygame.USEREVENT 
pygame.time.set_timer(SPAWNfloating_hearts,1200) #spawning hearts automatically 
floating_hearts_height = [400,600,800] 

game_over_surface = pygame.transform.scale2x(pygame.image.load('mymessage.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,452)) #mini change no.2: displays my own intro image made in photoshop

death_sound = pygame.mixer.Sound('cat-meow-14536.mp3')
sound1 = pygame.mixer.Sound('Positive-soft-background-intro-music/Positive-soft-background-intro-music.mp3')
score_sound_countdown = 100

sound1.play() #mini change no.3: background music plays 

while True: #keys and user controls 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				cat_movement = 0
				cat_movement -= 6
				tipe = '     jump!'

			if event.key == pygame.K_1 and game_active:
				cat_movement = 0
				cat_movement -= 8 #mini change no.4: 1 key makes the cat double jump 
				tipe = 'double jump!'
				text = game_font.render("+1", True, (255, 255, 255))
				screen.blit(text, text.get_rect(center = (100,100)))

			if event.key == pygame.K_0 and game_active:
				cat_movement = 0
				cat_movement -= 3 #mini change no.5: 0 key is a half jump 
				tipe = 'small jump!'
			
			if event.key == pygame.K_0 and game_active:
				cat_movement = 0
				cat_movement -= 8
				
			if event.key == pygame.K_q and game_active:
				pygame.quit() #mini change no.6: q key automatically quits game
			
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				floating_hearts_list.clear()
				cat_rect.center = (100,512)
				cat_movement = 0
				score = 0

		if event.type == SPAWNfloating_hearts: #continuously spawns hearts
			floating_hearts_list.extend(create_floating_hearts())

		if event.type == catFLAP: 
			if cat_index < 2:
				cat_index += 1
			else:
				cat_index = 0

			cat_surface,cat_rect = cat_animation()
    
	screen.blit(bg_surface,(0,0))

	if game_active: #tells the other function the game continues
		#cat
		cat_movement += gravity
		rotated_cat = rotate_cat(cat_surface)
		cat_rect.centery += cat_movement
		screen.blit(rotated_cat,cat_rect)
		game_active = check_collision(floating_hearts_list)

		#floating_hearts
		floating_hearts_list = move_floating_heartss(floating_hearts_list)
		floating_hearts_list = remove_floating_heartss(floating_hearts_list)
		draw_floating_heartss(floating_hearts_list)
		
		#score keeper
		score += 0.01
		score_display('main_game')
		score_sound_countdown -= 1
		if score_sound_countdown <= 0:
			#score_sound.play()
			score_sound_countdown = 100

	else: #tells the other function the game is over 
		screen.blit(game_over_surface,game_over_rect)
		high_score = update_score(score,high_score)
		score_display('game_over')

	#floor moving
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -576:
		floor_x_pos = 0
	
	pygame.display.update()
	clock.tick(60)