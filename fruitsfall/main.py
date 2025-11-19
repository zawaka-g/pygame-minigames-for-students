import pygame
import sys
import random

# 初期化
pygame.init()

# 定数
TILE_SIZE = 40
COLS = 6
ROWS = 12
WIDTH = TILE_SIZE * COLS
HEIGHT = TILE_SIZE * ROWS

# 色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# フルーツの読み込み
fruit_images = {
    "apple": pygame.image.load("apple.png"),
    "orange": pygame.image.load("orange.png"),
    "grape": pygame.image.load("grape.png")
}
# サイズを統一
for key in fruit_images:
    fruit_images[key] = pygame.transform.scale(fruit_images[key], (TILE_SIZE, TILE_SIZE))

# フルーツの種類リスト
fruit_types = list(fruit_images.keys())

# フィールド初期化（None = 空）
field = [[None for _ in range(COLS)] for _ in range(ROWS)]

# 画面・フォント
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ChatGPTでつくったぷ○ぷよでもなくス○カゲームでもないゲーム")
font = pygame.font.SysFont(None, 32)

# フルーツブロッククラス
class FruitBlock:
    def __init__(self):
        self.x = COLS // 2
        self.y = 0
        self.kind = random.choice(fruit_types)

    def move(self, dx):
        if 0 <= self.x + dx < COLS and field[self.y][self.x + dx] is None:
            self.x += dx

    def fall(self):
        if self.y + 1 < ROWS and field[self.y + 1][self.x] is None:
            self.y += 1
            return True
        return False

    def fix(self):
        field[self.y][self.x] = self.kind

# 初期状態
current_block = FruitBlock()
fall_timer = 0
fall_speed = 30

# メインループ
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(30)
    fall_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 操作
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        current_block.move(-1)
    if keys[pygame.K_RIGHT]:
        current_block.move(1)
    if keys[pygame.K_SPACE]:
        fall_timer += 5  # 加速

    # 落下処理
    if fall_timer >= fall_speed:
        fall_timer = 0
        if not current_block.fall():
            current_block.fix()
            current_block = FruitBlock()

            # ゲームオーバー判定（上段に詰まったら終了）
            if field[0][COLS // 2] is not None:
                screen.fill(BLACK)
                msg = font.render("GAME OVER", True, WHITE)
                screen.blit(msg, (WIDTH // 2 - 80, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False

    # 描画
    screen.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLS):
            fruit = field[y][x]
            if fruit:
                screen.blit(fruit_images[fruit], (x*TILE_SIZE, y*TILE_SIZE))

    # 現在のブロックを描画
    screen.blit(fruit_images[current_block.kind],
                (current_block.x*TILE_SIZE, current_block.y*TILE_SIZE))

    pygame.display.flip()

pygame.quit()
sys.exit()
