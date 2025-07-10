import pygame
import random

pygame.init()
win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("Scoop Saver")

# Load images
walkRight = [pygame.transform.scale(pygame.image.load(f'cone{i}.png'), (48, 64)) for i in range(1, 10)]
walkLeft = [pygame.transform.scale(pygame.image.load(f'coneL{i}.png'), (48, 64)) for i in range(1, 10)]
char = pygame.transform.scale(pygame.image.load('cone_stand.png'), (48, 64))
good_scoop_img = pygame.transform.scale(pygame.image.load('good_scoop.png'), (36, 28))
bad_scoop_img = pygame.transform.scale(pygame.image.load('bad_scoop.png'), (36, 28))

# Load sounds (comment out if you don't have these files)
good_sound = pygame.mixer.Sound("good.wav")
bad_sound = pygame.mixer.Sound("bad.wav")
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

font = pygame.font.SysFont('comicsans', 30)

class Player:
    def __init__(self):
        self.x = 220
        self.y = 400
        self.width = 64
        self.height = 64
        self.vel = 7
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            win.blit(char, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Scoop:
    def __init__(self):
        self.x = random.randint(0, 460)
        self.y = -40
        self.speed = random.randint(4, 7)
        self.type = random.choice(["good", "bad"])

    def draw(self, win):
        if self.type == "good":
            win.blit(good_scoop_img, (self.x, self.y))
        else:
            win.blit(bad_scoop_img, (self.x, self.y))
        self.y += self.speed

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 40, 40)

def redrawGameWindow():
    win.fill((200, 200, 255))  # Light blue background
    man.draw(win)
    for scoop in scoops:
        scoop.draw(win)
    text = font.render(f"Score: {score}", 1, (0,0,0))
    win.blit(text, (10, 10))
    lives_text = font.render(f"Lives: {lives}", 1, (255, 0, 0))
    win.blit(lives_text, (400, 10))
    pygame.display.update()

man = Player()
scoops = []
score = 0
lives = 3
clock = pygame.time.Clock()
frame_count = 0
run = True

while run:
    clock.tick(27)
    frame_count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    # Add new scoop every 45 frames
    if frame_count % 45 == 0:
        scoops.append(Scoop())

    # Check collisions
    player_rect = man.get_rect()
    for scoop in scoops[:]:
        scoop_rect = scoop.get_rect()
        if scoop_rect.colliderect(player_rect):
            if scoop.type == "good":
                score += 1
                good_sound.play()
            else:
                lives -= 1
                bad_sound.play()
            scoops.remove(scoop)
        elif scoop.y > 480:
            scoops.remove(scoop)

    if lives <= 0:
        run = False

    redrawGameWindow()

pygame.quit()


