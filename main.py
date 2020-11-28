from random import randint
import shelve
import pygame
from pygame.locals import *

pygame.init()
screen_width = 1080
screen_height = 720
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)

# Подгрузка музыки, спрайтов, бэкграунда и прочих картинок и звуков
pygame.mixer.music.load('knights_theme.mp3')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

pause_in = pygame.mixer.Sound('pause_in.mp3')
pause_in.set_volume(0.01)
pause_out = pygame.mixer.Sound('pause_out.mp3')
pause_out.set_volume(0.02)

click_snd = pygame.mixer.Sound('click.mp3')
click_snd.set_volume(0.15)

pause_img = pygame.image.load('paused.png').convert_alpha()

info_img = pygame.image.load('info.png')

player_img = [pygame.image.load('golden1.png'), pygame.image.load('golden2.png'), pygame.image.load('golden3.png'),
              pygame.image.load('golden4.png'), pygame.image.load('golden5.png'), pygame.image.load('golden6.png'),
              pygame.image.load('golden7.png'), pygame.image.load('golden8.png'), pygame.image.load('golden9.png'),
              pygame.image.load('golden10.png'), pygame.image.load('golden11.png'), pygame.image.load('golden12.png'),
              pygame.image.load('golden13.png'), pygame.image.load('golden14.png'), pygame.image.load('golden15.png'),
              pygame.image.load('golden16.png'), pygame.image.load('golden17.png'), pygame.image.load('golden18.png')]

player2_img = [pygame.image.load('p1.png'), pygame.image.load('p2.png'), pygame.image.load('p3.png'), pygame.image.load('p4.png'),
               pygame.image.load('p5.png'), pygame.image.load('p6.png'), pygame.image.load('p7.png'), pygame.image.load('p8.png'),
               pygame.image.load('p9.png'), pygame.image.load('p10.png'), pygame.image.load('p1.png'), pygame.image.load('p2.png'),
               pygame.image.load('p3.png'), pygame.image.load('p4.png'), pygame.image.load('p5.png'), pygame.image.load('p6.png'),
               pygame.image.load('p7.png'), pygame.image.load('p8.png')]

mob_img = [pygame.image.load('mob1.png'), pygame.image.load('mob2.png'), pygame.image.load('mob3.png'), pygame.image.load('mob4.png'),
           pygame.image.load('mob1.png'), pygame.image.load('mob2.png'), pygame.image.load('mob3.png'), pygame.image.load('mob4.png')]

mob2_img = [pygame.image.load('mobl2_1.png'), pygame.image.load('mobl2_2.png'), pygame.image.load('mobl2_3.png'),
            pygame.image.load('mobl2_4.png'), pygame.image.load('mobl2_5.png'), pygame.image.load('mobl2_6.png'),
            pygame.image.load('mobl2_7.png'), pygame.image.load('mobl2_8.png')]

health_img = pygame.image.load('hp.png')

regen_img = pygame.image.load('regen.png')

cross_img = pygame.image.load('cross.png')

retry_img = pygame.image.load('retry.png')

background_image = pygame.image.load("background.jpg").convert()
background_image2 = pygame.image.load("background_l2.jpg").convert()
pygame.display.set_caption("Knights&Dragons")

# Константы
background_x = 0
background_y = 0
back_speed = 0.9

FPS = pygame.time.Clock()
pygame.display.flip()

mob_pos_x = randint(950, 3000)
mob_pos_y = 530

mob_width = 180
mob_height = 125

player_cnt = 0
pos_x = -65
pos_y = 450
p_width = 350
p_height = 250

value_crash = 3

black = (000, 000, 000)
white = (255, 255, 255)
grey = (80, 80, 80)

score = 0
max_score = 0
temp = score

alive = True

paused = False

game_over = False

pygame.mouse.set_visible(False)
cursor_img = pygame.image.load('cursor.png')
cursor_img_rect = cursor_img.get_rect()


# Класс бэкграунда


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = background_image
        self.x = background_x
        self.y = background_y
        self.width = self.image.get_rect().width
        self.height = screen_height
        self.speed = back_speed

    # отрисовка бэкграунда и его движение влево
    def draw_background(self):
        rel_x = self.x % self.image.get_rect().width
        screen.blit(self.image, [rel_x - self.image.get_rect().width, 0])

        if rel_x < screen_width:
            screen.blit(self.image, (rel_x, 0))
        self.x -= self.speed


# Класс для розочки, восстанавливающей хп


class Regen(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = regen_img
        self.x = randint(10000, 15000)
        self.y = 530
        self.width = mob_width
        self.height = mob_height
        self.speed = 5
        self.make_jump = False
        self.jump_cnt = 35

    # Логика прыжка

    def draw_jump(self):
        if self.jump_cnt >= -35:
            self.y -= self.jump_cnt
            self.jump_cnt -= 1
        else:
            self.jump_cnt = 35
            self.make_jump = False

    # Отрисовка розочки, восстанавливающей хп

    def draw_regen(self):
        screen.blit(self.image, (self.x, self.y))
        self.x -= self.speed

    # Возращение на исходную

    def restart(self):
        if self.x < -65:
            self.x = randint(10000, 15000)

    # Проверка по y, чтобы не падало под карту

    def check_regen_pos_y(self):
        if background.image == background_image:
            if self.y > 530:
                self.y = 530
        elif background.image == background_image2:
            if self.y > 580:
                self.y = 580


# Класс противника


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mob_img
        self.x = mob_pos_x
        self.y = mob_pos_y
        self.width = mob_width
        self.height = mob_height
        self.mob_cnt = 8
        self.speed = 5

    # Отрисовка мобов из списка

    def draw_mob(self):
        if self.mob_cnt == 8:
            self.mob_cnt = 0
        screen.blit(self.image[self.mob_cnt], (self.x, self.y))
        self.mob_cnt += 1
        self.x -= self.speed

    # Респаун моба после того, как прошёл по своей траектории. Увеличение скорости движение моба. Установка макс.рекорда.

    def speed_inc(self):
        global score, max_score
        if self.x < -65:
            self.x = randint(950, 3000)
            score += 1
            self.speed += 0.1
            if max_score < score:
                max_score = score

    # Проверка противника по y, чтобы не падал под карту.

    def check_mob_pos_y(self):
        if background.image == background_image:
            if self.y > 530 or self.y < 530:
                self.y = 530
        elif background.image == background_image2:
            if self.y > 580 or self.y < 580:
                self.y = 580

    # Возврат противника на исходную и дефолтной скорости

    def restart(self):
        self.x = mob_pos_x
        self.y = mob_pos_y
        self.speed = 5


# Класс для игрока


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.x = pos_x
        self.y = pos_y
        self.jump_cnt = 28
        self.make_jump = False
        self.player_cnt = 17

    # Отрисовка игрока из списка.

    def draw_player(self):
        if self.player_cnt == 17:
            self.player_cnt = 0
        screen.blit(self.image[self.player_cnt], (self.x, self.y))
        self.player_cnt += 1

    # Логика прыжка для игрока.

    def draw_jump(self):
        if self.jump_cnt >= -28:
            self.y -= self.jump_cnt
            self.jump_cnt -= 1
        else:
            self.jump_cnt = 28
            self.make_jump = False

    # Возрат игрока на исходную.

    def restart(self):
        self.x = pos_x
        self.y = pos_y

    # Проверка игрока по у, чтобы не падал под карту.

    def check_player_pos_y(self):
        if background.image == background_image:
            if self.y > 450:
                self.y = 450
        elif background.image == background_image2 and not player.make_jump and player.image == player_img:
            if self.y > 480 or self.y < 480:
                self.y = 480


# Класс сохранения.


class Save:

    # Открытие файла или создание нового.

    def __init__(self):
        self.file = shelve.open('data')

    # Сохранение в файл.
    def save_data(self):
        self.file['max'] = max_score

    # Добавление инфы.
    def add_data(self, name, value):
        self.file[name] = value

    # Получение инфы.
    def get_data(self, name):
        return self.file[name]

    def __del__(self):
        self.file.close()


# Класс кнопок

class Button:
    def __init__(self):
        self.width = 180
        self.height = 45
        self.active_color = white
        self.default_color = grey

    # Отрисовка кнопки. Реакция на мышь, клики. Звук при клике.
    def draw_button(self, x, y, lvl, action=None):
        global max_score
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
                if click[0] == 1:
                    pygame.mixer.Sound.play(click_snd)
                    pygame.time.delay(150)

                    # Константы под уровень, который присвоен кнопке.
                    if lvl == 2:
                        if max_score > 50:
                            player.image = player2_img
                            player.y = 550
                            player.x = 50

                        else:
                            player.image = player_img
                            player.y = 580
                            player.x = -65

                        background.image = background_image2
                        mob.image = mob2_img
                        mob.y = 580
                        reg.y = 580
                        mob.speed = 6.5

                    if lvl == 1:
                        player.image = player_img
                        player.y = 480
                        background.image = background_image
                        mob.image = mob_img
                    if action is not None:
                        action()
            else:
                pygame.draw.rect(screen, self.default_color, (x, y, self.width, self.height))


start_button = Button()
lvl1_button = Button()
lvl2_button = Button()
info_button = Button()
quit_button = Button()
save = Save()
reg = Regen()
player = Player()
mob = Mob()
background = Background()


# Проверка на столкновение игрока и противника.

def check_rect():
    global value_crash, score
    if player.image == player_img:
        if (mob.x < player.x + 200) and (player.y > 340) and (mob.x > player.x):
            value_crash -= 1
            mob.x = -300
            score -= 1
    elif player.image == player2_img:
        if (mob.x < player.x + 100) and (player.y > 340) and (mob.x > player.x):
            value_crash -= 1
            mob.x = -300
            score -= 1


# Проверка на столкновение игрока и розочкой, восстанавливающей хп.
def check_rect_hp():
    global value_crash
    if (reg.x < player.x + 200) and (player.y < reg.y + 50) and (player.y > reg.y - 50) and (reg.x > player.x):
        value_crash += 1
        reg.x = -300


# Отрисовка ХП.
def draw_health():
    screen.blit(health_img, [700, 20])
    screen.blit(health_img, [825, 20])
    screen.blit(health_img, [950, 20])


# Рестарт всего при нажатии на Retry.
def restart():
    global alive, game_over, value_crash, score, paused
    screen.blit(retry_img, [370, 280])
    key = pygame.key.get_pressed()
    if key[pygame.K_RETURN]:
        player.restart()
        mob.restart()
        reg.restart()
        value_crash = 3
        alive = True
        game_over = False
        score = 0


# Отрисовка крестов на хп, в зависимости от столкновений с противником.
def check_hp():
    global value_crash
    if value_crash > 3:
        value_crash = 3

    if value_crash == 2:
        screen.blit(cross_img, [700, 20])

    if value_crash == 1:
        screen.blit(cross_img, [825, 20])
        screen.blit(cross_img, [700, 20])

    if value_crash == 0:
        screen.blit(cross_img, [950, 20])
        screen.blit(cross_img, [825, 20])
        screen.blit(cross_img, [700, 20])


# Отрисовка очков.
def scoring():
    global score
    if score == -1:
        score = 0
    font = pygame.font.Font('12th.ttf', 36)

    text = font.render("Score: ", True, black)
    text2 = font.render(str(score), True, black)

    screen.blit(text, [40, 35])
    screen.blit(text2, [140, 35])


# При паузе отрисовка картинок и реагирование на нажатие кнопок.
def is_paused():
    global paused
    screen.blit(pause_img, (280, 300))
    paused = True
    font = pygame.font.SysFont('kacstbook', 20)
    start_text = font.render('PRESS "BACKSPACE" TO QUIT!', True, white)
    screen.blit(start_text, (425, 380))

    font = pygame.font.SysFont('kacstbook', 20)
    start_text = font.render('PRESS "M" TO GO BACK TO MENU', True, white)
    screen.blit(start_text, (425, 310))

    key = pygame.key.get_pressed()
    if key[pygame.K_BACKSPACE]:
        quit()
    if key[pygame.K_ESCAPE]:
        pause_in.play()
    if key[pygame.K_m]:
        is_unpaused()
        menu()


# Проверка смерть. Сохранение рекорда при смерти. Вывод рекорда на экран.
def is_alive():
    global value_crash, alive, game_over, max_score
    if value_crash == 0:
        alive = False
        game_over = True

        save.save_data()
        save.add_data('max', max_score)

        font = pygame.font.Font('12th.ttf', 36)

        text = font.render("YOUR RECORD IS: ", True, black)
        max_out = font.render(str(max_score), True, black)

        screen.blit(text, (320, 430))
        screen.blit(max_out, (765, 430))

        save.save_data()

        restart()


# Проигрывание музыки при выходе из паузы.
def is_unpaused():
    global paused
    paused = False
    key = pygame.key.get_pressed()
    if not paused and key[pygame.K_ESCAPE]:
        pause_out.play()


# Показ информации об управлении в главном меню.
def info():
    info_show = True
    while info_show:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(info_img, (350, 200))
        font = pygame.font.SysFont('arial', 13)
        text1 = font.render('Управление:', True, black)
        text2 = font.render('Прыжок: SPACE.', True, black)
        text3 = font.render('Пауза: ESCAPE.', True, black)
        text4 = font.render('Начать заново после смерти: ENTER.', True, black)
        text5 = font.render('Для начала игры выберите уровень или нажмите "Начать игру".', True, black)
        text6 = font.render('Для выхода из INFO нажмите ESCAPE.', True, black)
        screen.blit(text1, (500, 300))
        screen.blit(text2, (490, 350))
        screen.blit(text3, (490, 400))
        screen.blit(text4, (440, 450))
        screen.blit(text6, (440, 500))
        screen.blit(text5, (368, 540))

        pygame.display.update()


# Отрисовка меню с кнопками. Получение рекорда из файла.
def menu():
    global score, value_crash, max_score
    max_score = save.get_data('max')
    score = 0
    value_crash = 3
    menu_back_img = pygame.image.load("menu_back.png")
    menu_show = True
    while menu_show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(menu_back_img, (0, 0))

        start_button.draw_button(440, 45, 1, run)
        lvl2_button.draw_button(640, 145, 2, run)
        lvl1_button.draw_button(240, 145, 1, run)
        info_button.draw_button(880, 650, None, info)
        quit_button.draw_button(440, 245, None, quit)

        font = pygame.font.Font('12th.ttf', 36)
        start_text = font.render('START!', True, black)
        screen.blit(start_text, (440, 45))

        font = pygame.font.Font('12th.ttf', 36)
        start_text = font.render('LEVEL 1', True, black)
        screen.blit(start_text, (240, 145))

        font = pygame.font.Font('12th.ttf', 36)
        start_text = font.render('LEVEL 2', True, black)
        screen.blit(start_text, (640, 145))

        font = pygame.font.Font('12th.ttf', 39)
        start_text = font.render('  INFO!', True, black)
        screen.blit(start_text, (880, 650))

        font = pygame.font.Font('12th.ttf', 39)
        start_text = font.render(' QUIT!', True, black)
        screen.blit(start_text, (440, 245))

        cursor_img_rect.center = pygame.mouse.get_pos()
        screen.blit(cursor_img, cursor_img_rect)

        pygame.display.flip()


# Основная функция игры.
def run():
    global paused, game_over
    game = True

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

        key = pygame.key.get_pressed()
        if player.make_jump is True:
            player.draw_jump()

        if paused:
            is_paused()

        if not paused:
            is_unpaused()
            check_rect()
            is_alive()

            if not game_over:
                if key[pygame.K_SPACE]:
                    player.make_jump = True
                player.check_player_pos_y()
                mob.check_mob_pos_y()
                reg.check_regen_pos_y()
                background.draw_background()
                player.draw_player()
                mob.draw_mob()
                mob.speed_inc()
                reg.draw_regen()
                reg.draw_jump()
                check_rect_hp()
                draw_health()
                check_hp()
                scoring()

        pygame.display.update()
        FPS.tick(60)


menu()
