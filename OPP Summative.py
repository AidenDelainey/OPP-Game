##-----------------##
#) OPP Summative   (#
#) Aiden Delainey  (#
#) jan 14/2026     (#
##-----------------##


import pygame
import random

WIDTH = 1200
HEIGHT = 650
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 200, 255)
DARK_BLUE = (0, 0, 255)
MAX_RED = 200

MENU = "menu"
PLAYING = "playing"
# Functions

DEATH_MSG = ['YOU DIED',
             'Could have done better',
             'WASTED',
             'Needed to take a break huh',
             "I've seen better",
             'YOU WIN... not',
             '"insert death message"',
             'awooga',
             'Man you suck',
             "I've seen a toddler do better",
             ]

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 1000
    BAR_HEIGHT = 50
    fill = (pct / 200) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, DARK_BLUE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 4)

def backround_color(health):
    if health >= 75:
        return(0, 0, 0)
    if health <= 0:
        return(255, 0, 0)
    ratio = (75 - health) / 75
    red = int(MAX_RED * ratio)
    return(red, 0, 0)

def get_shake_offset(health):
    if health > 75:
        return 0, 0
    
    ratio = (75 - health) / 75
    max_shake = 15
    shake = int(max_shake * ratio)
    
    offset_x = random.randint( -shake, shake)
    offset_y = random.randint( -shake, shake)
    
    return offset_x, offset_y

def apply_crt_effect(surface):
    """Apply CRT effect to the surface without hiding sprites and keeping scanlines."""
    # Start with a copy of the game surface
    shifted = surface.copy()

    # Step 1: RGB ghosting
    r = shifted.copy()
    g = shifted.copy()
    b = shifted.copy()

    r.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
    g.fill((0, 255, 0), special_flags=pygame.BLEND_MULT)
    b.fill((0, 0, 255), special_flags=pygame.BLEND_MULT)

    # Combine channels onto a temp surface
    temp = pygame.Surface(surface.get_size())
    temp.fill((0, 0, 0))
    temp.blit(r, (-2, 0))
    temp.blit(g, (2, 0))
    temp.blit(b, (0, 0))

    # Step 2: Flicker (mid-gray overlay)
    flicker = random.randint(-15, 15)
    flicker_color = max(0, min(255, 128 + flicker))
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((flicker_color, flicker_color, flicker_color))
    overlay.set_alpha(30)
    temp.blit(overlay, (0, 0))

    # Step 3: Merge the CRT effect on top of the original game surface
    shifted.blit(temp, (0, 0), special_flags=pygame.BLEND_ADD)

    # Step 4: Draw **scanlines** on top so they remain visible
    SCANLINE_COLOR = (30, 30, 30)  # dark gray, softer than black
    for y in range(0, HEIGHT, 4):
        pygame.draw.line(shifted, SCANLINE_COLOR, (0, y), (WIDTH, y), 1)

    return shifted

def draw_menu(screen):
    menu_surface = pygame.Surface((WIDTH, HEIGHT))
    menu_surface.fill(BLACK)
    draw_text(menu_surface, "OPP", 80, WIDTH / 2, HEIGHT / 4, WHITE)
    draw_text(menu_surface, "Press SPACE to Start", 40, WIDTH / 2, HEIGHT / 2, WHITE)
    draw_text(menu_surface, "WASD to Move", 30, WIDTH / 2, HEIGHT / 2 + 60, WHITE)

    crt_surface = apply_crt_effect(menu_surface)
    screen.blit(crt_surface, (0, 0))
    
def reset_game():
    global all_sprites, mobs, goal, player, score
    
    all_sprites.empty()
    mobs.empty()
    goal.empty()
    
    player = Player()
    all_sprites.add(player)
    
    g = Goal()
    goal.add(g)
    all_sprites.add(g)
    
    for i in range(35):
        newmob()
        
    score = 0
    
# Classes

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = 10
        self.speedx = 0
        self.speedy = 0
        self.health = 200
        self.loss_cooldown = 50
        self.last_damage = pygame.time.get_ticks()
    
    def update(self):
        now = pygame.time.get_ticks()
        self.speedx = 0
        self.speedy = 0
        #if now - self.last_damage > self.loss_cooldown:
            #self.last_damage = now
        if state == PLAYING:
            self.health -= 1
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -self.speed
        if keystate[pygame.K_d]:
            self.speedx = self.speed
        if keystate[pygame.K_w]:
            self.speedy = -self.speed
        if keystate[pygame.K_s]:
            self.speedy = self.speed
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
    
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        if random.random() > 0.90:
            self.image.fill(GREEN)
            self.type = 'heal'
        else:
            self.image.fill(RED)
            self.type = 'damage'
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = HEIGHT + random.randrange(40, 100)
        self.speedy = -random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < -10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = HEIGHT + random.randrange(40, 100)
            self.speedy = -random.randrange(4, 8)
            self.speedx = random.randrange(-3, 3)

class Goal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(50, WIDTH - 50)
        self.rect.y = random.randrange(50, HEIGHT - 50)
    
    def update(self):
        pass
    
        
        
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
goal = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
g = Goal()
goal.add(g)
all_sprites.add(goal)
for i in range(35):
    newmob()

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("OOP")
clock = pygame.time.Clock()
score = 0
MENU_MUSIC = 'Static.mp3'
GAME_MUSIC = 'Let the Fire Die.mp3'

game_over = pygame.mixer.Sound('game over.mp3')
state = MENU
pygame.mixer.music.load(MENU_MUSIC)
pygame.mixer.music.play(-1)


# Game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if state == MENU and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                state = PLAYING
                pygame.mixer.music.load(GAME_MUSIC)
                pygame.mixer.music.play(-1, 0.0, 2000)
                
    if state == MENU:
        draw_menu(screen)
        pygame.display.flip()
        continue
        
    if state == PLAYING:


    # Update
        all_sprites.update()
        
    # Check collion
        hits = pygame.sprite.spritecollide(player, mobs, True)
        for hit in hits:
            if hit.type == 'damage':
                player.health -= 75
            if hit.type == 'heal':
                player.health += 30
                if player.health > 200:
                    player.health = 200
            newmob()
        hits = pygame.sprite.spritecollide(player, goal, True)
        if hits:
            score += 1
            player.health += 75
            if player.health >= 200:
                player.health = 200
            g = Goal()
            all_sprites.add(g)
            goal.add(g)
        
        if player.health <= 0:
            death_msg = random.choice(DEATH_MSG)
            
            pygame.mixer.music.stop()
            pygame.mixer.music.load(MENU_MUSIC)
            pygame.mixer.music.play(-1, 0.0, 10000)
            
            death_surface = pygame.Surface((WIDTH, HEIGHT))
            death_surface.fill(WHITE)
            all_sprites.draw(death_surface)
            draw_text(death_surface, death_msg , 50, WIDTH / 2, HEIGHT / 2, BLACK)
            
            crt_death_surface = apply_crt_effect(death_surface)
            screen.blit(crt_death_surface, (0, 0))
            pygame.display.flip()
            pygame.time.wait(5000)
            
            reset_game()
            
            state = MENU
            continue
            
        # Draw / render
        game_surface.fill(backround_color(player.health))
        all_sprites.draw(game_surface)
        draw_health_bar(game_surface, 100, 15, player.health) 
        draw_text(game_surface, str(score), 50, WIDTH/2, 10, WHITE)
        
        crt_game_surface = apply_crt_effect(game_surface)
        shake_x, shake_y = get_shake_offset(player.health)
        screen.blit(crt_game_surface, (shake_x, shake_y))
        # *after* drawing everything, flip the display
        pygame.display.flip()

pygame.quit() #saaaaaaaaddsad