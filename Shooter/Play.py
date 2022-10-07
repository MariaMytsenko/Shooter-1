# Підключаємо необхідні модулі
# from pygame import *
import pygame
from random import randint
# Підключаємо роботу зі шрифтами
pygame.font.init()
# Налаштовуємо шрифт
font1 = pygame.font.Font(None, 80)
# Робимо текст для виграшу
win = font1.render('YOU WIN!', True, (255, 255, 255))
# Робимо текст для програшу
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

# Налаштовуємо шрифт 2
font2 = pygame.font.Font(None, 36)

# Фонова музика
# Отримуємо доступ до звуків комп'ютера
pygame.mixer.init()
# Завантажуємо звук для фону
pygame.mixer.music.load('space.ogg')
# Запускаємо його
pygame.mixer.music.play()

# Завантажуємо звук для попадання
fire_sound = pygame.mixer.Sound('fire.ogg')

# шляхи для картинок
img_back = "galaxy.jpg"  # Фон для гри
 
img_bullet = "bullet.png"  # Патрон
img_hero = "rocket.png"  # Герой
img_enemy = "ufo.png"  # Ворог
 
score = 0  # Кількість збитих кораблів
goal = 10  # Скільки залишилося кораблів для перемоги
lost = 0  # Скільки кораблів ми пропустили
max_lost = 3  # Кількість пропущених кораблів, яка необхідна для програшу

bullets = pygame.sprite.Group()

# Загальний класс для спрайтів


class GameSprite(pygame.sprite.Sprite):
    # Метод, який викликається при створенні нового спрайту (об'єкта на основі цього класу)
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Викликаємо конструктор классу Sprite (щоби у нас з'явився наш спрайт)
        pygame.sprite.Sprite.__init__(self)  # технічна строка, щоби pygame створив нам спрайт

        # Графіка для нашого спрайту (картинка)
        self.image_base = pygame.image.load(player_image)
        self.image = pygame.transform.scale(self.image_base, (size_x, size_y))
        # Швидкість з якою рухається наш спрайт
        self.speed = player_speed

        # Модель для нашого спрайту (прямокутник навколо картинки)
        self.rect = self.image.get_rect()
        # Координати для лівого верхнього кута нашого спрайта
        self.rect.x = player_x
        self.rect.y = player_y
 
    # Метод для відмалювання героя на дисплеї
    def draw(self):
        # Відмалювання на дисплеї
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс для нашого головного героя (наслідується від GameSprite)


class Player(GameSprite):
    # Метод для оновлення спрайту
    def update(self):
        # Управління лівою і правою стрілочкою
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
# pygame.K_LEFT = "LEFT"
#     {
#         "LEFT": True,
#         "Down": False,
#         "W": False
#     }

    # Метод для створення пулі
    def fire(self):
        # Створюємо нашу пулю, для цього беремо позицію головного героя
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        # Додаємо нашу пулю до списку
        bullets.add(bullet)

# Класс спрайту ворога (наслідується від классу GameSprite)


class Enemy(GameSprite):
    # Оновлення спрайту ворога
    def update(self):
        # Йде по осі y вниз
        self.rect.y += self.speed
        # Беремо глобальну змінну lost
        global lost
        # Ворог зникає, коли доходить до кінця екрану
        if self.rect.y > win_height:
            # Випадкове положення для ворога по x
            self.rect.x = randint(80, win_width - 80)
            # Положення по y
            self.rect.y = 0
            # Додаємо до пропущених кораблів 1
            lost = lost + 1
 
# Класс спрайту пулі


class Bullet(GameSprite):
    # Оновлення спрайту пулі
    def update(self):
        # Рух пулі по осі y
        self.rect.y += self.speed  # self.speed буде мінусовим числом
        # Зникає, якщо досягає краю дисплею
        if self.rect.y < 0:
            # метод спрайту, який його видаляє
            self.kill()


# Створюємо параметри дисплею
win_width = 700
win_height = 500
# Створюємо заголовок гри
pygame.display.set_caption("Shooter")
# Створюємо дисплей
window = pygame.display.set_mode((win_width, win_height))
# Завантажуємо картинку фону
background_image = pygame.image.load(img_back)
background = pygame.transform.scale(background_image, (win_width, win_height))
 
# Створюємо нашого головного героя
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
# Приглушення звуку
pygame.mixer.music.set_volume(0.02)
# Створюємо нашим ворогів
monsters = pygame.sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

# Створюємо группу наших пуль


clock = pygame.time.Clock()

# Змінна, яка контролює чи продовжується у нас гра (Геймплей)
finish = False
# Змінна, яка контролює чи продовжується у нас гра (Всю программу)
run = True
# Запускаємо ігровий цикл
while run:
    # Подія на вихід з гри
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Подія на натискання клавіші Пробіл
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Запускаємо звук пострілу
                fire_sound.set_volume(0.02)
                fire_sound.play()
                # Запускаємо сам постріл
                ship.fire()
 
    # Поки гра не завершилася (Геймплей)
    if not finish:
        # Оновлюємо фон нашої гри
        window.blit(background, (0, 0))

        # Пишемо текст на дисплеї
        text = font2.render("Рахунок: " + str(score), True, (255, 255, 255))
        # Відмальовуємо цей текст
        window.blit(text, (10, 20))

        # Пишемо текст на дисплеї
        text_lose = font2.render("Пропущено: " + str(lost), True, (255, 255, 255))
        # Відмальовуємо цей текст
        window.blit(text_lose, (10, 50))

        # Оновлюємо всі наші спрайти по прописаним правилам
        ship.update()
        monsters.update()
        bullets.update()

        # Оновлюємо позиції наших спрайтів
        ship.draw()
        monsters.draw(window)
        bullets.draw(window)
 
        # Перевірка зіткнення наших ворогів і пуль
        collides = pygame.sprite.groupcollide(monsters, bullets, True, True)
        # Перевірка всіх підбитих ворогів
        for c in collides:
            # Додаємо 1, якщо підбито ворога
            score = score + 1
            # Створюємо нового ворога
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            # Додаємо його до группи ворогів
            monsters.add(monster)

        # Програш, якщо ми зіткнулися з ворогом або пропустили max_lost кораблів
        if pygame.sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True  # Завершуємо нашу гру (Геймплей)
            # Відмальовуємо текст поразки
            window.blit(lose, (200, 200))

        # Перевірка, чи ми виграли (чи збили goal кораблів)
        if score >= goal:
            finish = True  # Завершуємо нашу гру (Геймплей)
            # Відмальовуємо текст перемоги
            window.blit(win, (200, 200))

        # Оновлюємо наш дисплей
        pygame.display.update()
    # Цикл працює кожні 0.05 секунд
    clock.tick(30)

