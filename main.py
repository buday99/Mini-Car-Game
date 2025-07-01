import pygame
import random
import os

# --- Inisialisasi Pygame ---
pygame.init()

# --- Pengaturan Layar ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hindari Mobil!")

# --- Warna ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GREY = (200, 200, 200) # Warna baru untuk tombol
DARK_GREY = (150, 150, 150) # Warna hover untuk tombol

# --- Path Aset ---
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# --- Muat Gambar (Gunakan fallback jika gambar tidak ada) ---
try:
    player_car_img = pygame.image.load(os.path.join(ASSETS_DIR, 'car.png')).convert_alpha()
    obstacle_img = pygame.image.load(os.path.join(ASSETS_DIR, 'obstacle.png')).convert_alpha()
    background_img = pygame.image.load(os.path.join(ASSETS_DIR, 'background.png')).convert()

    # Sesuaikan ukuran gambar jika perlu
    player_car_img = pygame.transform.scale(player_car_img, (50, 80))
    obstacle_img = pygame.transform.scale(obstacle_img, (50, 80))
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

except pygame.error:
    print("Warning: Could not load image assets. Using rectangles instead.")
    player_car_img = None
    obstacle_img = None
    background_img = None

# --- Kelas Pemain (Mobil Kita) ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if player_car_img:
            self.image = player_car_img
        else:
            self.image = pygame.Surface((50, 80))
            self.image.fill(BLUE) # Warna biru jika tidak ada gambar
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 100 # Naikkan sedikit agar ada ruang untuk tombol
        self.speed = 5
        self.move_left = False # Status pergerakan tombol
        self.move_right = False # Status pergerakan tombol

    def update(self):
        # Pergerakan dari keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Pergerakan dari tombol
        if self.move_left:
            self.rect.x -= self.speed
        if self.move_right:
            self.rect.x += self.speed

        # Batasi pergerakan di dalam layar
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# --- Kelas Rintangan (Mobil Lain/Obstacle) ---
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if obstacle_img:
            self.image = obstacle_img
        else:
            self.image = pygame.Surface((50, 80))
            self.image.fill(RED) # Warna merah jika tidak ada gambar
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -50) # Mulai dari atas layar
        # --- PERUBAHAN DI SINI: Kecepatan Obstacle diperlambat ---
        self.speed = random.randrange(2, 5) # Dari 3-7 jadi 2-5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT: # Jika keluar layar, reset posisi
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -50)
            self.speed = random.randrange(2, 5) # Pastikan kecepatan juga direset dengan rentang baru

# --- Kelas Button ---
class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_surface = font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.color = color
        self.hover_color = hover_color
        self.current_color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10) # Bulatkan sedikit sudut
        screen.blit(self.text_surface, self.text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos): # Klik kiri
                return True
        return False

# --- Fungsi untuk mereset game ---
def reset_game():
    global score, game_over
    game_over = False
    score = 0
    player.rect.centerx = SCREEN_WIDTH // 2
    player.rect.bottom = SCREEN_HEIGHT - 100
    # Hapus semua obstacle yang ada
    for obs in obstacles:
        obs.kill() # Menghapus sprite dari grup
    # Tambahkan obstacle baru
    for _ in range(5):
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

# --- Grup Sprite ---
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Tambahkan beberapa rintangan awal
for _ in range(5):
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

# --- Variabel Game ---
score = 0
font = pygame.font.Font(None, 36) # Font default, ukuran 36
game_over = False

# --- Inisialisasi Tombol Kontrol ---
button_font = pygame.font.Font(None, 40)
button_width = 80
button_height = 50
button_padding = 20 # Jarak antar tombol dan dari tepi

# Posisi tombol kiri
left_button_x = SCREEN_WIDTH // 2 - button_width - button_padding // 2
left_button_y = SCREEN_HEIGHT - button_height - 20 # Jarak dari bawah layar
left_button = Button(left_button_x, left_button_y, button_width, button_height, "<", button_font, LIGHT_GREY, DARK_GREY)

# Posisi tombol kanan
right_button_x = SCREEN_WIDTH // 2 + button_padding // 2
right_button_y = SCREEN_HEIGHT - button_height - 20
right_button = Button(right_button_x, right_button_y, button_width, button_height, ">", button_font, LIGHT_GREY, DARK_GREY)

# --- Inisialisasi Tombol Restart (akan muncul saat Game Over) ---
restart_button_width = 150
restart_button_height = 60
restart_button_x = (SCREEN_WIDTH - restart_button_width) // 2
restart_button_y = (SCREEN_HEIGHT // 2) + 70 # Di bawah teks "Press R to Restart" atau "GAME OVER!"
restart_button_font = pygame.font.Font(None, 50)
restart_button = Button(restart_button_x, restart_button_y, restart_button_width, restart_button_height, "RESTART", restart_button_font, GREEN, DARK_GREY, WHITE)


# --- Loop Game Utama ---
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over: # Restart game dengan keyboard 'R'
                reset_game()

        # Penanganan event mouse untuk tombol
        if not game_over:
            # Handle klik tombol kontrol
            if left_button.handle_event(event):
                player.move_left = True
            if right_button.handle_event(event):
                player.move_right = True

            # Handle mouse up (saat tombol dilepas)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    player.move_left = False
                    player.move_right = False
        else: # Jika game_over adalah True
            if restart_button.handle_event(event): # Handle klik tombol restart
                reset_game()


    # Perubahan warna tombol kontrol saat di-hover (hanya jika game tidak over)
    if not game_over:
        mouse_pos = pygame.mouse.get_pos()
        if left_button.is_hovered(mouse_pos):
            left_button.current_color = left_button.hover_color
        else:
            left_button.current_color = left_button.color

        if right_button.is_hovered(mouse_pos):
            right_button.current_color = right_button.hover_color
        else:
            right_button.current_color = right_button.color
    else: # Jika game_over adalah True, periksa hover untuk tombol restart
        mouse_pos = pygame.mouse.get_pos()
        if restart_button.is_hovered(mouse_pos):
            restart_button.current_color = restart_button.hover_color
        else:
            restart_button.current_color = restart_button.color


    if not game_over:
        # Update
        all_sprites.update()

        # Deteksi tabrakan
        hits = pygame.sprite.spritecollide(player, obstacles, False) # False: obstacle tidak hilang saat tabrakan
        if hits:
            game_over = True

        # Tambah skor seiring waktu
        score += 1

    # Gambar
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(GREEN) # Latar belakang hijau jika tidak ada gambar

    all_sprites.draw(screen)

    # Tampilkan skor
    score_text = font.render(f"Score: {score // 60}", True, BLACK) # Bagi 60 untuk skor per detik (jika 60 FPS)
    screen.blit(score_text, (10, 10))

    # Tampilkan Game Over
    if game_over:
        game_over_text = font.render("GAME OVER!", True, RED)
        # restart_text = font.render("Press 'R' to Restart", True, BLACK) # Dihapus atau dipertimbangkan
        
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        # restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)) # Dihapus atau dipertimbangkan
        
        screen.blit(game_over_text, text_rect)
        # screen.blit(restart_text, restart_rect) # Dihapus atau dipertimbangkan
        
        # Gambar tombol Restart
        restart_button.draw(screen)
    else:
        # Gambar tombol kontrol hanya jika game sedang berjalan
        left_button.draw(screen)
        right_button.draw(screen)

    # Refresh layar
    pygame.display.flip()

    # Batasi FPS
    clock.tick(60)

pygame.quit()