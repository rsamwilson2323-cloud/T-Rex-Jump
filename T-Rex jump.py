import warnings
warnings.filterwarnings("ignore")

import pygame, random, os, time, sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 450
FPS = 60
GROUND_Y = 350

WHITE = (255,255,255)
BLACK = (0,0,0)
SKY_DAY = (235,235,235)
SKY_NIGHT = (20,20,40)
GROUND_COLOR = (83,83,83)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game — Clean One Obstacle")
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 32)
BIG = pygame.font.Font(None, 48)

HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            return int(open(HIGHSCORE_FILE).read())
        except:
            return 0
    return 0

def save_highscore(val):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(val))


# -----------------------------------------------------
# 🦖 DINO (Drawn sprite, no images needed)
# -----------------------------------------------------
class Dino:
    def __init__(self):
        self.width = 50
        self.height = 55
        self.x = 80
        self.y_origin = GROUND_Y - self.height
        self.rect = pygame.Rect(self.x, self.y_origin, self.width, self.height)
        self.vel = 0
        self.jumping = False
        self.ducking = False
        self.anim = 0

    def jump(self):
        if not self.jumping:
            self.vel = -17
            self.jumping = True

    def start_duck(self):
        if not self.jumping:
            self.ducking = True
            self.rect.height = 35
            self.rect.y = GROUND_Y - self.rect.height

    def stop_duck(self):
        if self.ducking:
            self.ducking = False
            self.rect.height = self.height
            self.rect.y = GROUND_Y - self.rect.height

    def update(self):
        self.vel += 1
        self.rect.y += self.vel

        if self.rect.y >= GROUND_Y - self.rect.height:
            self.rect.y = GROUND_Y - self.rect.height
            self.jumping = False

        self.anim = (self.anim + 1) % 20

    def draw(self, surf):
        x,y,w,h = self.rect

        pygame.draw.rect(surf, (40,150,40), (x,y,w,h))      # Body
        pygame.draw.circle(surf, BLACK, (x + 38, y + 12), 4)  # Eye

        if self.ducking:
            pygame.draw.rect(surf, (30,100,30), (x, y+20, w, 15))
            return

        if not self.jumping:
            if self.anim < 10:
                pygame.draw.rect(surf, (30,100,30), (x + 10, y + h - 10, 12, 10))
            else:
                pygame.draw.rect(surf, (30,100,30), (x + 28, y + h - 10, 12, 10))


# -------------------------------------------------
# 🌵 CACTUS
# -------------------------------------------------
class Cactus:
    def __init__(self, x, speed):
        self.h = random.randint(40,70)
        self.w = random.randint(20,30)
        self.rect = pygame.Rect(x, GROUND_Y - self.h, self.w, self.h)

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, surf):
        x,y,w,h = self.rect
        pygame.draw.rect(surf, (70,200,70), (x,y,w,h))
        pygame.draw.rect(surf, (60,180,60), (x-5,y+20,10,20))
        pygame.draw.rect(surf, (60,180,60), (x+w-5,y+15,10,18))


# -----------------------------------------
# 🐦 BIRD
# -----------------------------------------
class Bird:
    def __init__(self, x, speed):
        heights = [GROUND_Y - 120, GROUND_Y - 90, GROUND_Y - 150]
        self.y = random.choice(heights)
        self.rect = pygame.Rect(x, self.y, 45, 30)
        self.anim = 0

    def update(self, speed):
        self.rect.x -= speed + 1.5
        self.anim = (self.anim + 1) % 20

    def draw(self, surf):
        x,y,w,h = self.rect
        pygame.draw.ellipse(surf, (90,90,90), (x,y,w,h))

        if self.anim < 10:
            pygame.draw.ellipse(surf, (70,70,70), (x+10,y+5,20,10))
        else:
            pygame.draw.ellipse(surf, (70,70,70), (x+10,y+10,20,10))


# -----------------------------------------
# ☁ CLOUD
# -----------------------------------------
class Cloud:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(20, 140)
        self.s = random.uniform(0.7, 1.4)
        self.speed = random.uniform(0.2,0.7)

    def update(self):
        self.x -= self.speed
        if self.x < -200:
            self.x = WIDTH + random.randint(100,300)

    def draw(self, surf):
        w = int(80*self.s)
        h = int(40*self.s)
        pygame.draw.ellipse(surf, WHITE, (self.x,self.y,w,h))
        pygame.draw.ellipse(surf, WHITE, (self.x+20,self.y-10,w,h))


# -------------------------------------------------
# GAME STATE
# -------------------------------------------------
def reset(state):
    state["dino"] = Dino()
    state["obstacle"] = None
    state["clouds"] = [Cloud() for _ in range(5)]
    state["score"] = 0
    state["speed"] = 8
    state["spawn_t"] = 0
    state["over"] = False
    state["time"] = 0

state = {}
reset(state)
state["high"] = load_highscore()

MIN_GAP = 350

def can_spawn(state):
    ob = state["obstacle"]
    if ob is None:
        return True
    return ob.rect.x < WIDTH - MIN_GAP


# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------
running = True
while running:
    dt = clock.tick(FPS) / 1000

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_SPACE, pygame.K_UP):
                if state["over"]:
                    if state["score"] > state["high"]:
                        state["high"] = state["score"]
                        save_highscore(state["high"])
                    reset(state)
                else:
                    state["dino"].jump()

            if e.key == pygame.K_DOWN:
                state["dino"].start_duck()

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_DOWN:
                state["dino"].stop_duck()

    # ---------------------------
    # UPDATE GAME
    # ---------------------------
    if not state["over"]:
        dino = state["dino"]
        dino.update()
        state["spawn_t"] += dt
        state["time"] += dt * 0.06

        # SPAWN ONE OBSTACLE ONLY
        if state["obstacle"] is None and state["spawn_t"] > 1.0:
            if can_spawn(state):
                if random.random() < 0.7:
                    state["obstacle"] = Cactus(WIDTH + 20, state["speed"])
                else:
                    state["obstacle"] = Bird(WIDTH + 20, state["speed"])
                state["spawn_t"] = 0

        # UPDATE obstacle
        if state["obstacle"]:
            ob = state["obstacle"]
            ob.update(state["speed"])

            if ob.rect.right < 0:
                state["score"] += 1
                state["speed"] += 0.3
                state["obstacle"] = None

            # collision
            if dino.rect.colliderect(ob.rect):
                if isinstance(ob, Bird) and dino.ducking:
                    pass  # duck avoids bird
                else:
                    state["over"] = True

        for c in state["clouds"]:
            c.update()

    # ---------------------------
    # DRAW EVERYTHING
    # ---------------------------
    sky = SKY_DAY if (state["time"] % 2) < 1 else SKY_NIGHT
    screen.fill(sky)

    for c in state["clouds"]:
        c.draw(screen)

    pygame.draw.rect(screen, GROUND_COLOR, (0,GROUND_Y,WIDTH,HEIGHT-GROUND_Y))

    state["dino"].draw(screen)

    if state["obstacle"]:
        state["obstacle"].draw(screen)

    screen.blit(FONT.render(f"Score: {state['score']}", True, BLACK), (10,10))
    screen.blit(FONT.render(f"High Score: {state['high']}", True, BLACK), (10,40))

    if state["over"]:
        overlay = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        screen.blit(overlay,(0,0))

        t = BIG.render("GAME OVER", True, WHITE)
        screen.blit(t, (WIDTH//2 - t.get_width()//2, HEIGHT//2 - 50))

        sub = FONT.render("Press SPACE or UP to Restart", True, WHITE)
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2))

    pygame.display.flip()

pygame.quit()
sys.exit()
