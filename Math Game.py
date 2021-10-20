# -*- coding: utf-8 -*-
"""
IF YOU SEE THIS HI! I have made this program for a school project, I don't know why you looked in to the source code but
here it is. I will not be explaining this code in thai. I am also a terrible coder so don't expect much.
"""
# Imports
import pygame
import sys
from pygame.locals import *
import random
from fractions import Fraction
import webbrowser

pygame.init()  # Initialize
pygame.mixer.music.set_volume(0.7)  # Set volume

# Variables
num1 = 0  # the numbers getting rendered
num2 = 0  # for example num1 + num2 ( 1 + 1 )
difficulty = 'easy'  # easy normal or hard
symbol = ''
answer = 0
scene = 0  # which scene is getting rendered |0 = the start| |1 = options| |2 = the game| |3 = game over screen|
on_button = [False, 0]
on_text = [False, 0]
score = 000
options = []
question = 1
question_number = 10  # how many questions will the game provide
temp_var_loop = True
time_left = 35
volume_music = 0.7
volume_sound = 0.7

# Game Setup
FPS = 240
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
WIDTH = screen.get_width()
HEIGHT = screen.get_height()
pygame.mixer.init()

pygame.display.set_caption('Math Quiz')
font = 'arial'
backgrounds = ['Resources/Pictures/BACKGROUND.png', 'Resources/Pictures/BACKGROUND2.png',
               'Resources/Pictures/BACKGROUND3.png']
background = ''


class Button:  # CLASS FOR BUTTON
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.width = 0
        self.height = 0
        self.radius = 0
        self.type = ''  # DEBUG
        self.id = 0
        self.picture = ''

    def draw_rectangle(self, x, y, width, height, color=(68, 157, 209), identification=(-1),
                       curve=20):  # DRAW THE THING
        pygame.draw.rect(screen, color, [x - width / 2, y - height / 2, width, height], 0, curve)
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.type = 'rectangle'
        self.id = identification
        del self.radius, self.picture

    def draw_picture(self, identification, x, y, picture_name):
        image = pygame.image.load('Resources/Pictures/' + picture_name + '.png')
        self.height = image.get_height()
        self.width = image.get_width()
        self.x_pos = x
        self.y_pos = y
        self.type = 'picture'
        self.id = identification
        self.picture = picture_name  # Without including directory or file type
        del self.radius
        screen.blit(pygame.image.load(image), (x - self.width / 2, y - self.height / 2))

    def draw_circle(self, x, y, radius, color=(14, 14, 82)):  # WIP
        self.x_pos = x
        self.y_pos = y
        self.radius = radius
        del self.height, self.width, self.picture
        self.type = 'circle'
        pygame.draw.circle(screen, color, (x, y), radius)

    def mouse_on_button(self, mouse_pos):  # CHECK IF MOUSE IS ON THE BUTTON
        if self.type == 'rectangle':
            if self.x_pos - self.width / 2 < mouse_pos[
                0] < self.x_pos + self.width / 2 and self.y_pos - self.height / 2 < mouse_pos[
                1] < self.y_pos + self.height / 2:  # checking if mouse is in between the button area
                return [True, self.id]
            else:
                return [False, self.id]


class Text:
    def __init__(self):
        self.font = ''
        self.color = ''
        self.size = 0
        self.x_pos = 0
        self.y_pos = 0
        self.text = ''
        self.width = 0
        self.height = 0
        self.id = 0

    def draw_text(self, text, x, y, s, f, color=(0, 0, 0), identification=(-1)):
        self.font = f
        self.color = color
        self.size = s
        self.y_pos = y
        self.x_pos = x
        self.text = text
        self.width = pygame.font.SysFont(f, s).render(str(text), True, color).get_width()
        self.height = pygame.font.SysFont(f, s).render(str(text), True, color).get_height()
        self.id = identification
        text_area = pygame.font.SysFont(f, s).render(str(text), True, color).get_rect(center=(x, y))
        screen.blit(pygame.font.SysFont(f, s).render(str(text), True, color),
                    text_area)  # https://pygame.readthedocs.io/en/latest/4_text/text.html

    def mouse_on_text(self, mouse_pos):
        if self.x_pos - self.width / 2 < mouse_pos[
            0] < self.x_pos + self.width / 2 and self.y_pos - self.height / 2 < mouse_pos[
            1] < self.y_pos + self.height / 2:  # checking if mouse is in between the button area
            return [True, self.id]
        else:
            return [False, self.id]


def main():
    # Globalizing main variables
    global num1, num2, scene, difficulty, answer, on_button, on_text, score, options, question, WIDTH, HEIGHT, \
        temp_var_loop, time_left, volume_music, volume_sound
    options_choices = {'ADDITION [+]': [Text(), True],
                       'SUBTRACTION [-]': [Text(), True],
                       'MULTIPLICATION [x]': [Text(), False],
                       'DIVISION [÷]': [Text(), False],
                       'COMPARISON [>]': [Text(), True],
                       'FRACTION [/]': [Text(), False],
                       'MUSIC': [Text(), True],
                       'SOUND EFFECTS': [Text(), True]}

    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Resources/Sounds/chill_music.mp3'), -1)

    while True:  # MAIN LOOP

        pygame.mixer.Channel(0).set_volume(volume_music)
        pygame.mixer.Channel(1).set_volume(volume_sound)

        # Get inputs
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()
        mouse_pos = pygame.mouse.get_pos()

        # Checking stuff
        for event in pygame.event.get():

            if event.type == QUIT:
                oof()
            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse clicks
                if on_text[0] and on_text[1] == 21:
                    webbrowser.open_new_tab('https://github.com/theme222/Math-Game/tree/main')
                if on_text[0] and on_text[1] == 1:  # QUIT TEXT
                    oof()

                if on_text[0] and on_text[1] == 2:  # Options Button
                    scene = 1

                if on_text[0] and on_text[1] == 0:  # Play text
                    score = 0
                    question = 1
                    time_left = 20
                    # Make a new question
                    for i in (list(options_choices.values())):
                        if i[0].id < 11:
                            if i[1]:
                                temp_var_loop = True
                                scene = 2
                                break
                            else:
                                temp_var_loop = False

                    while temp_var_loop:
                        temp_var_choice = random.choice(list(options_choices.keys()))  # get a random key
                        if options_choices[temp_var_choice][1] and \
                                'MUSIC' not in temp_var_choice and \
                                'SOUND' not in temp_var_choice:  # check if the key is enabled and isn't a sound
                            make_question(temp_var_choice)
                            pygame.mixer.Channel(0).play(pygame.mixer.Sound('Resources/Sounds/game_music.mp3'), -1)
                            break

                    if not temp_var_loop:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Resources/Sounds/Buzzer.mp3'))

                if on_text[0] and on_text[1] == 3:  # BACK TEXT
                    if scene == -1:
                        scene = 1
                    else:
                        scene = 0

                if on_text[0] and on_text[1] == 4:  # NEXT TEXT
                    scene = -1

                if on_text[0] and 4 < on_text[1] < 13:  # OPTIONS TEXT
                    temp_list_idkwtf = list(options_choices.values())  # ima be honest i have no idea how this works
                    temp_list_idkwtf[on_text[1] - 5][1] = not temp_list_idkwtf[on_text[1] - 5][1]  # same with the first

                    if on_text[1] == 11:  # changing the music and sound effects volume
                        if volume_music == 0.7:
                            volume_music = 0
                        else:
                            volume_music = 0.7
                    elif on_text[1] == 12:
                        if volume_sound == 0.7:
                            volume_sound = 0
                        else:
                            volume_sound = 0.7

                if on_button[1] > 0 and on_button[0]:  # THE 4 MAIN BUTTONS
                    question += 1
                    if options[on_button[1] - 1] == answer:  # IF CORRECT ANSWER
                        time_left += 6
                        if symbol == '>':
                            time_left -= 4.5
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Resources/Sounds/correct.mp3'))
                        if time_left > 40:  # capping the maximum stored time to 40
                            time_left = 40
                        score += 1
                    else:
                        time_left -= 6
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Resources/Sounds/Buzzer.mp3'))

                    # Make a new question
                    while temp_var_loop:
                        temp_var_choice = random.choice(list(options_choices.keys()))  # get a random key
                        if options_choices[temp_var_choice][1] and \
                                'MUSIC' not in temp_var_choice and \
                                'SOUND' not in temp_var_choice:  # check if the key is enabled and isn't a sound
                            make_question(temp_var_choice)
                            break

                on_text = [False, 0]
                on_button = [False, 0]

            if time_left <= 0:  # If out of time
                scene = 3
                time_left = 20
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('Resources/Sounds/chill_music.mp3'), -1)

        # Render
        screen.fill((0, 0, 0))
        if scene == -1:  # SCENE -1 CREDITS

            # INITIALIZE
            back_text = Text()
            credits_text = Text()
            zapsplat_text = Text()
            me_text = Text()  # :D
            open_source_text = Text()

            # DRAW

            open_source_text.draw_text('Github : https://github.com/theme222/Math-Game/tree/main',
                                       (WIDTH / 2), (HEIGHT * 4 / 6), 65, font, (174, 198, 255), 21)

            zapsplat_text.draw_text('Sound effects from Zapsplat.com',
                                    (WIDTH / 2), (HEIGHT * 3 / 6), 70, font, (255, 255, 255))

            me_text.draw_text('Made by Sira Tongsima',
                              (WIDTH / 2), (HEIGHT * 2 / 6), 70, font, (255, 255, 255))

            credits_text.draw_text('CREDITS', (WIDTH / 2), (HEIGHT / 6), 120, font, (255, 255, 255))
            back_text.draw_text('< BACK', WIDTH / 8, HEIGHT - HEIGHT / 12, 60, font, (255, 255, 255), 3)

            # POSITION
            on_texts = [back_text.mouse_on_text(mouse_pos), open_source_text.mouse_on_text(mouse_pos)]
            for i in on_texts:
                if i[0]:
                    on_text = i
                    break
                else:
                    on_text = [False, 0]

        elif scene == 0:  # SCENE 0 MAIN MENU

            # INITIALIZE
            title_text = Text()
            options_text = Text()
            go_text = Text()
            quit_text = Text()

            # DRAW
            title_text.draw_text('MATH QUIZ', (WIDTH / 2), (HEIGHT / 6), 120, font, (255, 255, 255))
            go_text.draw_text('PLAY', WIDTH / 2, HEIGHT / 2, 80, font, (255, 255, 255), 0)
            quit_text.draw_text('QUIT', WIDTH - WIDTH / 8, HEIGHT - HEIGHT / 12, 60, font, (255, 255, 255), 1)
            options_text.draw_text('OPTIONS', WIDTH / 8, HEIGHT - HEIGHT / 12, 60, font, (255, 255, 255), 2)

            # POSITION
            on_texts = [go_text.mouse_on_text(mouse_pos), quit_text.mouse_on_text(mouse_pos),
                        options_text.mouse_on_text(mouse_pos)]
            for i in on_texts:
                if i[0]:
                    on_text = i
                    break
                else:
                    on_text = [False, 0]

        elif scene == 1:  # SCENE 1 OPTIONS

            # INITIALIZE
            back_text = Text()
            options_title_text = Text()
            options_next_text = Text()
            on_texts = []

            # DRAW
            back_text.draw_text('< BACK', WIDTH / 8, HEIGHT - HEIGHT / 12, 60, font, (255, 255, 255), 3)
            options_title_text.draw_text('OPTIONS', (WIDTH / 2), (HEIGHT / 6), 120, font, (255, 255, 255))
            options_next_text.draw_text('NEXT >', WIDTH - WIDTH / 8, HEIGHT - HEIGHT / 12, 60, font, (255, 255, 255), 4)

            # DRAW OPTIONS (this is going to be a pain to code)
            temp_var_height = HEIGHT * 11 / 32
            temp_var_width = WIDTH / 4
            temp_var_id = 4
            for i in options_choices:  # for each option will check if on or off and coloring it correctly
                temp_var_id += 1
                if options_choices[i][1]:
                    options_choices[i][0].draw_text(
                        i, temp_var_width, temp_var_height, 70, font, (136, 235, 136), temp_var_id)
                else:
                    options_choices[i][0].draw_text(
                        i, temp_var_width, temp_var_height, 70, font, (255, 105, 97), temp_var_id)

                temp_var_height += HEIGHT * 2 / 16  # making the text go in different positions on the y axis
                if temp_var_id == 8:
                    temp_var_height = HEIGHT * 11 / 32
                    temp_var_width = WIDTH * 3 / 4
                on_texts.append(options_choices[i][0].mouse_on_text(mouse_pos))

            # POSITION
            on_texts.append(back_text.mouse_on_text(mouse_pos))
            on_texts.append(options_next_text.mouse_on_text(mouse_pos))
            for i in on_texts:
                if i[0]:
                    on_text = i
                    break
                else:
                    on_text = [False, 0]

        elif scene == 2:  # SCENE 2 MAIN GAME

            # INITIALIZE
            timer_object = Button()
            num1_text = Text()
            num2_text = Text()
            symbol_text = Text()
            options_object = [[Button(), Text()], [Button(), Text()], [Button(), Text()], [Button(), Text()]]

            # DRAW
            num1_text.draw_text(num1, WIDTH * 3 / 8, HEIGHT * 5 / 16, 100, font, (255, 255, 255))
            num2_text.draw_text(num2, WIDTH * 5 / 8, HEIGHT * 5 / 16, 100, font, (255, 255, 255))
            symbol_text.draw_text(symbol, WIDTH / 2, HEIGHT * 5 / 16, 100, font, (255, 255, 255))

            timer_object.draw_rectangle(
                WIDTH / 2, HEIGHT / 22, WIDTH * time_left / 30, HEIGHT / 23, (211, 97, 53), curve=0)

            options_object[0][0].draw_rectangle(
                WIDTH * 1 / 8, HEIGHT * 14 / 18, WIDTH / 4 - WIDTH * 1 / 80, HEIGHT * 13 / 32, (219, 252, 255), 1)

            options_object[1][0].draw_rectangle(
                WIDTH * 3 / 8, HEIGHT * 14 / 18, WIDTH / 4 - WIDTH * 1 / 80, HEIGHT * 13 / 32, (166, 207, 213), 2)

            options_object[2][0].draw_rectangle(
                WIDTH * 5 / 8, HEIGHT * 14 / 18, WIDTH / 4 - WIDTH * 1 / 80, HEIGHT * 13 / 32, (127, 150, 255), 3)

            options_object[3][0].draw_rectangle(
                WIDTH * 7 / 8, HEIGHT * 14 / 18, WIDTH / 4 - WIDTH * 1 / 80, HEIGHT * 13 / 32, (229, 99, 153), 4)

            options_object[0][1].draw_text(options[0], WIDTH * 1 / 8, HEIGHT * 14 / 18, 80, font)
            options_object[1][1].draw_text(options[1], WIDTH * 3 / 8, HEIGHT * 14 / 18, 80, font)
            options_object[2][1].draw_text(options[2], WIDTH * 5 / 8, HEIGHT * 14 / 18, 80, font)
            options_object[3][1].draw_text(options[3], WIDTH * 7 / 8, HEIGHT * 14 / 18, 80, font)

            # POSITION
            on_buttons = [options_object[0][0].mouse_on_button(mouse_pos),  # CHECK IF THE BUTTONS ARE CLICKED
                          options_object[1][0].mouse_on_button(mouse_pos),
                          options_object[2][0].mouse_on_button(mouse_pos),
                          options_object[3][0].mouse_on_button(mouse_pos)]

            for i in on_buttons:  # CHECKING WHICH BUTTON WAS CLICKED
                if i[0]:
                    on_button = i
                    break
                else:
                    on_button = [False, 0]

            pass

        else:  # SCENE 3 GAME OVER SCREEN

            # INITIALIZE
            back_text = Text()
            game_over_text = Text()
            score_text = Text()

            # DRAW
            back_text.draw_text('< BACK', WIDTH / 8, HEIGHT - HEIGHT / 12, 60, font, (255, 255, 255), 3)
            game_over_text.draw_text("GAME OVER", WIDTH / 2, 200, 100, font, (255, 255, 255))
            score_text.draw_text('SCORE : ' + str(score), WIDTH / 2, 400, 90, font, (255, 255, 255))

            # POSITION
            on_text = back_text.mouse_on_text(mouse_pos)

        pygame.display.update()
        fpsClock.tick(FPS)

        if scene == 2:  # if playing update time
            time_left -= fpsClock.get_time() / 1000


def oof():  # short function to end the game
    pygame.quit()
    sys.exit()


def make_question(mode):  # A function to make options randomly
    global num1, num2, answer, options, symbol

    if '+' in mode:
        num1 = random.randint(1, 200)
        num2 = random.randint(1, 200)
        answer = num1 + num2
        symbol = '+'
    elif '-' in mode:
        num1 = random.randint(1, 150)
        num2 = random.randint(1, 100)
        answer = num1 - num2
        symbol = '-'
    elif 'x' in mode:
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 20)
        answer = num1 * num2
        symbol = 'x'
    elif 'DIVISION' in mode:
        while True:
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 9)
            answer = num1 / num2
            if len(list(str(answer).split('.'))[1]) <= 1 and answer != 1.0 and answer != num1:  # uhhhhhhhhhhhhhhhhhhhhh
                break
            symbol = '÷'
    elif '>' in mode:
        num1 = random.randint(1, 20000)
        num2 = random.randint(1, 20000)
        if num1 > num2:
            answer = True
        else:
            answer = False
        symbol = '>'
    elif '/' in mode:
        num1 = Fraction(str(random.randint(1, 9)) + '/' + str(random.randint(2, 15)))
        num2 = Fraction(str(random.randint(1, 9)) + '/' + str(random.randint(2, 15)))
        selection = random.choice(['+', '-', '*', '/'])
        if selection == '+':
            answer = num1 + num2
            symbol = '+'
        elif selection == '-':
            answer = num1 - num2
            symbol = '-'
        elif selection == '*':
            answer = num1 * num2
            symbol = 'x'
        else:
            answer = num1 / num2
            symbol = '÷'
    print(num1, num2)
    options = []
    for i in range(3):
        if type(answer) == float:
            if answer % 1 != 0:
                options.append(round(answer + random.randint(-10, 10) + (random.randint(-9, 9) / 10), 1))
            else:
                options.append(round(answer + random.randint(-10, 10), 1))
        elif type(answer) == int:
            options.append(round(answer + random.randint(-10, 10), 1))
        elif type(answer) == bool:
            options = ()
        elif type(answer) == Fraction:
            while True:
                temp_var_int = [random.randint(-12, 12), random.randint(1, 2)]
                if 0 not in temp_var_int:
                    break
            options.append(answer + Fraction(str(temp_var_int[0]) + '/' + str(temp_var_int[1])))
    try:
        options.append(answer)
        random.shuffle(options)
        exec('str(num1)\nstr(num2)\nfor i in options:\n    str(i)\nstr(answer)')
    except AttributeError:  # Im lazy ok? I just don't want to deal with more variables.
        options = ['', True, False, '']


if __name__ == '__main__':
    main()
