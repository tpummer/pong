import pygame, sys, random, os
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Pygame init
pygame.init()
screen = pygame.display.set_mode((640,360),0,32)
clock = pygame.time.Clock()
pygame.key.set_repeat(20,1)
pygame.display.set_caption('Pong - nullpointer.at')

# Farben
BLACK = (0,0,0)
WHITE = (255,255,255)

# Schriftart
basicFont = pygame.font.SysFont(None, 48)
startFont = pygame.font.SysFont(None, 28)
playerFont = pygame.font.SysFont(None, 20)
punktFont = pygame.font.SysFont(None, 72)

#Win Loose Text
winText = basicFont.render('WIN', True, WHITE, BLACK)
looseText = basicFont.render('LOOSE', True, WHITE, BLACK)
winTextRect = winText.get_rect()
looseTextRect = looseText.get_rect()

# Starttext
restartBoolean = True
startText = startFont.render('press SPACE to start a new game', True, WHITE, BLACK)
startTextRect = startText.get_rect()

centerx = screen.get_rect().centerx
y = 240

startTextRect.centerx = centerx
startTextRect.y = y
musicText = startFont.render('m to mute music', True, WHITE, BLACK)
musicTextRect = musicText.get_rect()
musicTextRect.centerx = centerx
musicTextRect.y = y + 30
soundText = startFont.render('s to mute sounds', True, WHITE, BLACK)
soundTextRect = soundText.get_rect()
soundTextRect.centerx = centerx
soundTextRect.y = y + 60
backText = startFont.render('1-3 to switch soundtrack', True, WHITE, BLACK)
backTextRect = backText.get_rect()
backTextRect.centerx = centerx
backTextRect.y = y + 90

#Background
bif = "background.jpg" 
background = pygame.image.load(bif).convert()

# Flugrichtungen
speed = 0
startspeed = 100
speed_plus = 20
winkel = 0
# -1 up 1 down
ball_dir_updown = 1
# -1 left 1 down
ball_dir_leftright = 1

#Ball
ball_x = 302
ball_y = 162
ball_gr = (36,36)
ball_position_root = (ball_x,ball_y)
ball_position = (ball_x,ball_y)
ballif = "ball.png"
ball = pygame.image.load(ballif).convert_alpha()

#Balken
playerspeed = 250
#temporaere startpositionen
a_x = 30
a_y = 162
b_x = 595
b_y = 30
balken_gr = (16,95)
balkenif = "balken.png"
balken = pygame.image.load(balkenif).convert()

# Punkte
player_a = 0
player_a_pkt_pos = (60, 55)
player_b = 0
player_b_pkt_pos = (540, 55)

#Spielernamen
playeraText = playerFont.render('Computer', True, WHITE, BLACK)
playeraTextRect = playeraText.get_rect()
playeraTextRect.x = 50
playeraTextRect.y = 35

playerbText = playerFont.render('Spieler', True, WHITE, BLACK)
playerbTextRect = playerbText.get_rect()
playerbTextRect.x = 530
playerbTextRect.y = 35

#Punkteanzeige
punkt0Text = punktFont.render('0', True, WHITE, BLACK)
punkt1Text = punktFont.render('1', True, WHITE, BLACK)
punkt2Text = punktFont.render('2', True, WHITE, BLACK)
punkt3Text = punktFont.render('3', True, WHITE, BLACK)
punkt4Text = punktFont.render('4', True, WHITE, BLACK)
punkt5Text = punktFont.render('5', True, WHITE, BLACK)

# set up music
soundBoolean = True

balkenSound = pygame.mixer.Sound('balken.wav')
punktSound = pygame.mixer.Sound('punkt.wav')
wandSound = pygame.mixer.Sound('wand.wav')

def set_musik(music):
    if music == 1:
            pygame.mixer.music.load('back1.ogg')
    elif music == 2:
            pygame.mixer.music.load('back2.ogg')
    else:
            pygame.mixer.music.load('back3.ogg')

def draw_punkte(punkt, pos):
    punktText = punkt0Text
    if punkt == 1:
            punktText = punkt1Text
    elif punkt == 2:
            punktText = punkt2Text
    elif punkt == 3:
            punktText = punkt3Text
    elif punkt == 4:
            punktText = punkt4Text
    elif punkt == 5:
            punktText = punkt5Text
    screen.blit(punktText, pos)

def ball_hit_wall(ball_pos, ball_gr):
    global ball_dir_updown
    global ball_dir_leftright
    global ball_x
    global ball_y
    global player_a
    global player_b
    global speed
    global winkel

    # Ball trifft oberen Bereich
    if ball_pos[1] < 0:
            ball_dir_updown = 1
            winkel *= -1
            if soundBoolean:
                    wandSound.play()
    # Ball trifft unteren Bereich
    elif ball_pos[1] + ball_gr[1] > 360:
            ball_dir_updown = -1
            winkel *= -1
            if soundBoolean:
                    wandSound.play()

    # Punkt Spieler B
    if ball_pos[0] < 0:
            player_b += 1
            ball_dir_leftright = 1
            ball_x = 302
            ball_y = 162
            speed = startspeed
            winkel = 0
            if soundBoolean:
                    punktSound.play()
    # Punkt Spieler A
    elif ball_pos[0] + ball_gr[0] > 640:
            player_a += 1
            ball_dir_leftright = -1
            ball_x = 302
            ball_y = 162
            speed = startspeed
            winkel = 0
            if soundBoolean:
                    punktSound.play()

def move_player_a(ball_y):
    global a_y
    if a_y + 31 > ball_y and a_y > 0:
            #hoch
            a_y += seconds * playerspeed * -1
    elif a_y + 31 < ball_y and a_y + 95 < 360:
            #runter
            a_y += seconds * playerspeed * 1

def object_hit(a_pos, a_gr, b_pos, b_gr, seconds):
    global ball_dir_leftright
    global speed
    global winkel

    # errechne die 4 ecken von a
    aa = a_pos
    ab = tuple([a_pos[0] + a_gr[0], a_pos[1]])
    ac = tuple([a_pos[0] + a_gr[0], a_pos[1] + a_gr[1]])
    ad = tuple([a_pos[0], a_pos[1] + a_gr[1]])

    # errechne die 4 ecken von b
    ba = b_pos
    bb = tuple([b_pos[0] + b_gr[0], b_pos[1]])
    bc = tuple([b_pos[0] + b_gr[0], b_pos[1] + b_gr[1]])
    bd = tuple([b_pos[0], b_pos[1] + b_gr[1]])

    winkelmin = 1
    winkelmax = 10
    maxErreichterWinkel = 45

    #computerseite
    if aa[0] < 320:
            if punkt_innerhalb(aa, ba, bb, bc, bd) and punkt_innerhalb(ad, ba, bb, bc, bd):
                    ball_dir_leftright = 1
                    speed += speed_plus
                    if soundBoolean:
                            balkenSound.play()
            elif punkt_innerhalb(aa, ba, bb, bc, bd):
                    ball_dir_leftright = 1
                    speed += speed_plus
                    if winkel > maxErreichterWinkel * -1:
                            winkel += random.randint(winkelmax * -1, winkelmin * -1) * seconds * 5
                    if soundBoolean:
                            balkenSound.play()
            elif punkt_innerhalb(ad, ba, bb, bc, bd):
                    ball_dir_leftright = 1
                    speed += speed_plus
                    if winkel < maxErreichterWinkel:
                            winkel += random.randint(winkelmin, winkelmax) * seconds * 5
                    if soundBoolean:
                            balkenSound.play()
    #spielerseite
    else:
            if punkt_innerhalb(ab, ba, bb, bc, bd) and punkt_innerhalb(ac, ba, bb, bc, bd):
                    ball_dir_leftright = -1
                    speed += speed_plus
                    if soundBoolean:
                            balkenSound.play()
            elif punkt_innerhalb(ab, ba, bb, bc, bd):
                    ball_dir_leftright = -1
                    speed += speed_plus
                    if winkel > maxErreichterWinkel * -1:
                            winkel += random.randint(winkelmax * -1, winkelmin * -1) * seconds * 5
                    if soundBoolean:
                            balkenSound.play()
            elif punkt_innerhalb(ac, ba, bb, bc, bd):
                    ball_dir_leftright = -1
                    speed += speed_plus
                    if winkel < maxErreichterWinkel:
                            winkel += random.randint(winkelmin, winkelmax) * seconds * 5
                    if soundBoolean:
                            balkenSound.play()


def punkt_innerhalb(aa, ba, bb, bc, bd):
    if ba[0] < aa[0] < bb[0] and ba[1] < aa[1] < bd[1]:
            return True
    else:
            return False

def change_angle():
    pass

def change_direction():
    pass
            
#start musik
music = random.randint(1,3)
set_musik(music)
pygame.mixer.music.play(-1, 0.0)
musicPlaying = True


while True:

    for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYUP:
                    if event.key == ord('m'):
                       if musicPlaying:
                               pygame.mixer.music.stop()
                       else:
                               pygame.mixer.music.play(-1, 0.0)
                       musicPlaying = not musicPlaying
                    if event.key == ord('s'):
                       soundBoolean = not soundBoolean
                    if event.key == K_1:
                            pygame.mixer.music.stop()
                            set_musik(1)
                            pygame.mixer.music.play(-1, 0.0)
                    if event.key == K_2:
                            pygame.mixer.music.stop()
                            set_musik(2)
                            pygame.mixer.music.play(-1, 0.0)
                    if event.key == K_3:
                            pygame.mixer.music.stop()
                            set_musik(3)
                            pygame.mixer.music.play(-1, 0.0)
                    if restartBoolean:
                            if event.key == K_SPACE:
                                    player_a = 0
                                    player_b = 0
                                    speed = startspeed
                                    ball_x = 302
                                    ball_y = 162
                                    restartBoolean = False
##            if event.type == KEYDOWN:
##                    if event.key == K_DOWN and b_y + 95 < 360:
##                            b_y += seconds * playerspeed * 1
##                    if event.key == K_UP and b_y > 0:
##                            b_y += seconds * playerspeed * -1

    key_pressed = pygame.key.get_pressed()

    if key_pressed[K_DOWN] and b_y + 95 < 360:
        b_y += seconds * playerspeed * 1
    if key_pressed[K_UP] and b_y > 0:
        b_y += seconds * playerspeed * -1
        
    screen.blit(background, (0,0))
    screen.blit(playeraText, playeraTextRect)
    screen.blit(playerbText, playerbTextRect)

    
    balken_a_pos = (a_x, a_y)
    balken_b_pos = (b_x, b_y)
    draw_punkte(player_a, player_a_pkt_pos)
    draw_punkte(player_b, player_b_pkt_pos)
    
    screen.blit(balken, balken_a_pos)
    screen.blit(balken, balken_b_pos)
    screen.blit(ball, ball_position)

    milli = clock.tick()
    seconds = milli/1000.

    dmx = seconds * speed * ball_dir_leftright
    dmy = seconds * speed * ball_dir_updown
    ball_x += dmx
    ball_y += dmy + winkel
    
    ball_position = (ball_x,ball_y)

    # ball hits player a
    if object_hit(ball_position, ball_gr, balken_a_pos, balken_gr, seconds):
            change_direction()
            change_angle()
    # ball hits player b
    elif object_hit(ball_position, ball_gr, balken_b_pos, balken_gr, seconds):
            change_direction()
            change_angle()

    ball_hit_wall(ball_position, ball_gr)

    move_player_a(ball_y)

    if player_a == 5 or player_b == 5:
            speed = 0
            if player_a == 5:
                    winTextRect.x = 80
                    looseTextRect.x = 450
            else:
                    winTextRect.x = 450
                    looseTextRect.x = 80
            looseTextRect.y = 160
            winTextRect.y = 160
            screen.blit(winText, winTextRect)
            screen.blit(looseText, looseTextRect)
            restartBoolean = True

    if restartBoolean:
            screen.blit(startText, startTextRect)
            screen.blit(musicText, musicTextRect)
            screen.blit(soundText, soundTextRect)
            screen.blit(backText, backTextRect)
            
    pygame.display.flip()
