import sys, os, pygame, random
from pygame.sprite import Group

from pygame.locals import *

# Инициализируем переменные
# Начальное положение корабля
x_coord = 1
y_coord = 320
# Начальная скорость корабля
x_speed = 0
y_speed = 0
# Количество жизненной энергии корабля
score = 100
# время миссии
time_mission = 0
# уровень
level = 1
# коэффициент скорости
speed = 1
# Переменная-счетчик
shag = 0
# количество пуль на уровень
bullets_allowed = 5

# Инициализируем pygame
pygame.init()
# Создаём игровое окно 800*570

screen_size = width, height = (800, 570)
window = pygame.display.set_mode(screen_size)
# Ставим свой заголовок окна
pygame.display.set_caption('Астероиды')
# иконка игры
icon = pygame.image.load('data/asteroid.png')
pygame.display.set_icon(icon)
FPS = 50
clock = pygame.time.Clock()
cycle = True
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

# добавлем звуки
# столкновение корабля и астероида
bdish_sound = pygame.mixer.Sound('data/Bdish.wav')
# звук, что мы достигли звезды
star_sound = pygame.mixer.Sound('data/hp+.wav')
# звук, появления звезды
star_new_sound = pygame.mixer.Sound('data/star.wav')
#  звук, когда закончились жизни
loss_sound = pygame.mixer.Sound('data/loss.wav')
# звук попадания наряда в астероид
bullet_sound=pygame.mixer.Sound('data/bullet.wav')

# Функция отображения картинок
def load_image(name, colorkey=None):
    # Добавляем к имени картинки имя папки
    fullname = os.path.join('data', name)
    # Загружаем картинку
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert()
    # Если второй параметр =-1 делаем прозрачным
    # цвет из точки 0,0
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image, image.get_rect()


def draw_background():
    # Получаем поверхность, на которой будем рисовать
    screen = pygame.display.get_surface()
    # загружаем картинку космоса для фона
    back, back_rect = load_image("cosmos1.jpg")
    # и рисуем ее
    screen.blit(back, (0, 0))
    pygame.display.flip()
    return back


def terminate():
    pygame.quit()
    quit()


def start_screen():
    # загружаем фон
    fon, b = load_image('cosmos1.jpg')
    # загружаем музыку
    pygame.mixer.music.load('data/space_menu.mp3')
    pygame.mixer.music.set_volume(0.3)  # 1 -100%  громкости звука
    pygame.mixer.music.play(-1)  # играть бесконечно -1

    # Создание кнопки Play.
    play_button = Button(280, 70, window)
    # Создание кнопки Показать правила
    rules_button = Button(280, 70, window)
    # кнопка завершить игру
    quit_btn = Button(280, 70, window)
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(play_button, mouse_x, mouse_y)
                check_rules_button(rules_button, mouse_x, mouse_y)
                check_quit_button(quit_btn, mouse_x, mouse_y)

        window.blit(fon, (0, 0))
        play_button.draw_button(500, 200, "Play")
        rules_button.draw_button(500, 300, "Rules")
        quit_btn.draw_button(500, 400, 'Quit')
        pygame.display.flip()
        clock.tick(FPS)


def check_play_button(button, mouse_x, mouse_y):
    """Запускает новую игру при нажатии кнопки Play."""
    if button.rect.collidepoint(mouse_x, mouse_y):
        start_game()


def check_rules_button(button, mouse_x, mouse_y):
    """Вызывает экран с правилами игры"""
    if button.rect.collidepoint(mouse_x, mouse_y):
        rules_show()


def check_quit_button(button, mouse_x, mouse_y):
    """Выход из игры."""
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        terminate()


def rules_show():
    """экран с правилами игры"""
    intro_text = ["Цель: как можно дольше продержаться в игре", "",
                  "Столкновение с астероидом уменьшает количество жизненной энергии ", "",
                  "Количество астероидов с каждым уровнем растет", "", "", "", "",
                  "Пересечение с синей зездой",
                  "увеличивает количество жизненной энергии на 50", "",
                  "На каждом уровне у игрока есть 5 пуль для стрельбы по астероидам", "",
                  "Для паузы в игре нажмите ESC"]

    fon, b = load_image('cosmos1.jpg')
    window.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        window.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def start_game():
    global cycle
    # добавляем музыку - только mp3
    pygame.mixer.music.load('data/space_game.mp3')
    pygame.mixer.music.set_volume(0.3)  # 1 -100%   звука
    pygame.mixer.music.play(-1)  # играть бесконечно -1, либо число означаюшее кличество циклов проигрывания
    bk = draw_background()
    cycle = True

    while cycle:
        action(bk)


def print_text(x, y, msg, font_color=(0, 0, 0), font_type='data/PingPong.ttf', font_size=50):
    """
    вывод текста на кнопке
    :param x:  координата начала сообщения по х
    :param y: координата начала сообщения по у
    :param font_color: цвет шрифта
    :param font_type: тип  шрифта
    :param font_size: размер шрифта
    :return:
    """
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(msg, True, font_color)
    window.blit(text, (x, y))


class Button():
    def __init__(self, width, heigth, screen):
        """
        Инициализирует атрибуты кнопки.
        :param width: -ширина кнопки
        :param heigth: -высота
        :param screen: -экран
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Назначение размеров и свойств кнопок.
        self.width, self.heigth = width, heigth
        self.button_color = (34, 113, 179)

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

    def draw_button(self, x, y, msg):
        # Отображение  кнопки
        self.rect = pygame.Rect(x, y, self.width, self.heigth)
        pygame.draw.rect(self.screen, self.button_color, self.rect)  # (x, y, self.width, self.heigth))
        print_text(x + 90, y + 10, msg)


# Класс описывающий летающие объекты
class Skything(pygame.sprite.Sprite):
    def __init__(self, img, cX, cY):
        # Создаем спрайт из картинки
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(img, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Перемещаем картинку в её начальные координаты
        self.rect.x = cX
        self.rect.y = cY


# Создаём дочерний класс корабля Ship
class Ship(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "ship.bmp", cX, cY)

    def update(self, x_coord, y_coord):
        # Обновляем координаты корабля
        self.rect.x = x_coord
        self.rect.y = y_coord


# Создаём дочерний класс звезды Star
class Star(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "star3.png", cX, cY)


# Создаём дочерний класс Asteroid
class Asteroid(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "asteroid.png", cX, cY)
        self.vx = random.randint(-2, 2)
        self.vy = random.randint(-2, 2)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        # было ли взаимодествие астероида с границей экрана
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


# Создаем класс пуль
class Bullet(pygame.sprite.Sprite):
    def __init__(self, ship):
        super().__init__()
        self.screen = pygame.display.get_surface()
        # Создание пули в позиции (0,0) и назначение правильной позиции.
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # Позиция пули хранится в вещественном формате.
        self.y = float(self.rect.y)
        self.color = 255, 0, 0
        self.speed_factor = 3

    def update(self):
        """Перемещает пулю вверх по экрану."""
        # Обновление позиции пули
        self.y -= self.speed_factor
        # Обновление позиции прямоугольника.
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод пули на экран."""
        pygame.draw.rect(self.screen, self.color, self.rect)


# Создаём класс с границами экрана
class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(pygame.sprite.Group())
        if x1 == x2:  # вериткальная граница экрана
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная граница экрана
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def input(events, ship):
    global x_coord, y_coord, x_speed, y_speed, life
    # Перехватываем нажатия клавиш на клавиатуре
    for event in events:
        if (event.type == QUIT):  # or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit(0)
        # Когда нажаты стрелки изменяем скорость корабля
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_speed = -2 * speed
            elif event.key == pygame.K_RIGHT:
                x_speed = 2 * speed
            elif event.key == pygame.K_UP:
                y_speed = -2 * speed
            elif event.key == pygame.K_DOWN:
                y_speed = 2 * speed
            elif event.key == pygame.K_SPACE:
                fire_bullet(ship, bullets)
            if event.key == pygame.K_ESCAPE:
                pause()
        # Когда стрелки не нажаты скорость ставим в ноль
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: x_speed = 0
            if event.key == pygame.K_RIGHT: x_speed = 0
            if event.key == pygame.K_UP: y_speed = 0
            if event.key == pygame.K_DOWN: y_speed = 0

    # Меняем положение корабля не выходя за рамки окна
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed
    if (x_coord < 0): x_coord = 0
    if (x_coord > 740): x_coord = 740
    if (y_coord < 0): y_coord = 0
    if (y_coord > 520): y_coord = 520


def pause():
    paused = True
    # музыка на паузу
    pygame.mixer.music.pause()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text(160, 300, 'Paused. Press enter to continue', font_color=(255, 255, 255), font_size=30)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # enter -продолжить
            paused = False

        pygame.display.update()
        clock.tick(15)
    # музыка  снять с паузы
    pygame.mixer.music.unpause()


def fire_bullet(ship, bullets):
    """Выпускает пулю, если максимум еще не достигнут."""
    # Создание новой пули и включение ее в группу bullets.
    global bullets_allowed
    if len(bullets) < bullets_allowed:
        new_bullet = Bullet(ship)
        bullets.add(new_bullet)
        bullets_allowed -= 1


def action(bk):
    global x_coord, y_coord, score, shag, time_mission, shag_star, level, speed, bullets, bullets_allowed

    # Инициализируем переменные
    # Начальное положение корабля
    x_coord = 1
    y_coord = 320
    # Начальная скорость корабля
    x_speed = 0
    y_speed = 0
    # Количество жизненной энергии корабля
    score = 100
    # время миссии
    time_mission = 0
    # уровень
    level = 1
    # коэффициент скорости
    speed = 1

    # Переменная-счетчик
    shag = 0
    # количество пуль на уровень
    bullets_allowed = 5

    screen = pygame.display.get_surface()

    Border(1, 1, width - 1, 1)
    Border(1, height - 1, width - 1, height - 1)
    Border(1, 1, 1, height - 1)
    Border(width - 1, 1, width - 1, height - 1)
    asteroid = []
    for i in range(3):
        asteroid.append(Asteroid(random.randint(25, 400), random.randint(25, 300)))
    for i in range(3):
        asteroid.append(Asteroid(random.randint(400, 795), random.randint(300, 575)))

    # Создаём корабль и астероиды
    ship = Ship(1, 320)

    air = []
    air.append(ship)

    st = []
    bullet = []
    # Рисуем их
    ships = pygame.sprite.RenderPlain(air)
    stars = pygame.sprite.RenderPlain(st)
    asteroids = pygame.sprite.RenderPlain(asteroid)
    # Создание группы для хранения пуль.
    bullets = Group()
    timer = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    game = True
    # Запускаем бесконечный цикл
    while game:
        # Создаем паузу
        timer.tick(100)
        # Ждём нажатий клавиатуры
        input(pygame.event.get(), ship)
        # Проверяем столкновения корабля и астероида
        blocks_hit_list = pygame.sprite.spritecollide(ship, asteroids, False)
        # Если есть столкновения уменьшаем жизнь
        if len(blocks_hit_list) > 0:
            # проигрываем звук столкновения
            pygame.mixer.Sound.play(bdish_sound)
            score -= len(blocks_hit_list)
            if (score < 1):
                # проигрываем звук окончания жизни
                pygame.mixer.Sound.play(loss_sound)
                game = False
        # столкновение пули и астероида
        hit_bullet = pygame.sprite.groupcollide(bullets, asteroids, True, True)
        if len(hit_bullet)>0:
            pygame.mixer.Sound.play(bullet_sound)
        # если пуля на границе, то ее удаляем
        for bullet in bullets.copy():
            if pygame.sprite.spritecollideany(bullet, horizontal_borders):
                bullets.remove(bullet)
            if pygame.sprite.spritecollideany(bullet, vertical_borders):
                bullets.remove(bullet)

        # проверяем столкновение со звездой, если есть, то удаляем звезу
        hit_star = pygame.sprite.spritecollide(ship, stars, True)
        if len(hit_star) > 0:
            # проигрываем звук столкновения со звездой
            pygame.mixer.Sound.play(star_sound)
            # увеличиваем количество жизней
            score += 50

        # Раз в 300 итераций добавляем время продолжения миссии
        if (shag % 300 == 0):
            if shag % 900 == 0 and shag > 1:
                # создаем звезду
                new_star = Star(random.randint(100, 700), random.randint(100, 500))
                # проигрываем звук появления звезды
                pygame.mixer.Sound.play(star_new_sound)

                stars.add(new_star)
            elif shag % 900 == 1 and len(stars) > 0:
                # удаляем звезду
                for star in stars.copy():
                    stars.remove(star)

            # увеличиваем время миссии
            time_mission += 1

            if time_mission % 5 == 0:
                # увеличиваем уровень
                level += 1
                # удаляем все пули
                bullets.empty()
                bullets_allowed = 10
                asteroids.empty()
                # добавляем астероиды
                for i in range(level + 6):
                    asteroids.add(Asteroid(random.randint(25, 795), random.randint(25, 575)))
                # увеличиваем коэффициент скорости
                speed += 0.2

        shag += 1

        # Заново прорисовываем объекты
        screen.blit(bk, (0, 0))
        font = pygame.font.Font(None, 25)
        white = (255, 255, 255)
        life = int(score)
        text = font.render("Жизнь: " + str(life), True, white)
        # Рисуем надпись с жизнями
        screen.blit(text, [10, 10])
        text3 = font.render("Пули: " + str(bullets_allowed), True, white)
        # Рисуем надпись с кол-вом пуль
        screen.blit(text3, [10, 30])
        text1 = font.render("Время миссии: " + str(time_mission), True, white)
        # Рисуем надпись с временем миссии
        screen.blit(text1, [650, 10])
        text2 = font.render("Уровень: " + str(level), True, white)
        # Рисуем надпись с уровнем
        screen.blit(text2, [300, 10])
        # Обновляем положение объектов
        ships.update(x_coord, y_coord)
        bullets.update()
        stars.update()
        asteroids.update()

        # Обновляем кадр
        ships.draw(screen)
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        stars.draw(screen)
        asteroids.draw(screen)

        pygame.display.flip()
    game_over()


def game_over():
    """
    завершение игры
    :return:
    """
    global time_mission, cycle, level

    stoped = True

    while stoped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text(40, 300, 'Game over. Press enter to play again. Esc to exit', font_color=(255, 255, 255),
                   font_size=30)
        print_text(300, 350, 'Mission time: ' + str(time_mission), font_color=(255, 255, 255), font_size=30)
        print_text(350, 400, 'Level: ' + str(level), font_color=(255, 255, 255), font_size=30)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # enter -продолжить
            cycle = True
            return True

        if keys[pygame.K_ESCAPE]:  # esc -выход
            pygame.mouse.set_visible(True)
            # загружаем музыку для меню
            pygame.mixer.music.load('data/space_menu.mp3')
            pygame.mixer.music.set_volume(0.3)  # 1 -100%  громкости звука
            pygame.mixer.music.play(-1)  # играть бесконечно -1, либо число означаюшее кличество циклов проигрывания
            cycle = False
            return False

        pygame.display.update()
        clock.tick(15)


def main():
    start_screen()


main()
