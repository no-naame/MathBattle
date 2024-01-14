import pygame
import  os
pygame.font.init()
pygame.mixer.init()

def say(text):
    os.system(f'say {text}')

WIDTH, Height = 900, 500
WIN = pygame.display.set_mode((WIDTH, Height))
pygame.display.set_caption("GameeGame")
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 60
VEL = 30
BULLET_VEL = 10
MAX_BULLETS = 42345600
BORDER = pygame.Rect(WIDTH//2 - 5,0,10,Height)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicscans',40)
WINNER_FONT = pygame.font.SysFont('comicscans',60)

YELLOW = (223,219,89)
RED = (200,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
FPS = 60
YELLOW_SPACESHIP_IMG = pygame.image.load(os.path.join('Assets', '1.1.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMG,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),0)
RED_SPACESHIP_IMG = pygame.image.load(os.path.join('Assets', '2.1.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),0)

YELLOW_HIT = pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT +2


SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'SoumitraSir1.jpeg')),(WIDTH,Height))



def draww(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < Height -10:
        yellow.y += VEL
def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.y:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < Height -10:
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def winner_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, Height//2 - draw_text.get_height()//2))

    pygame.display.update()
    pygame.time.delay(2000)

def main():
    red = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 1
    yellow_health = 1
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height//2-2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_0 and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""

        if yellow_health <= 0:
            winner_text = "10 Rupay Ki Pepsi Harshit Sir Sexy"
            say("das Rupay Ki Pepsi Harshi Sir Sexy")
        if red_health <= 0:
            winner_text = "10 Rupay Ki Pepsi Suri Sir Sexy"
            say("das Rupay Ki Pepsi Suri Sir Sexy")

        if winner_text != "":
            winner_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draww(red, yellow, red_bullets, yellow_bullets,red_health,yellow_health)

    main()

if __name__ == "__main__":
    main()