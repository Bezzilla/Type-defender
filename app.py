import pygame
import copy
import random
from nltk.corpus import words
from Tracker import Tracker

pygame.init()

# WIDTH, HEIGHT = 800, 600  # WIDTH, HEIGHT = 1000, 800
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Type Defender')
timer = pygame.time.Clock()


class Dataset:
    def __init__(self):
        self.wordlist = words.words()  # Load English words from nltk
        self.wordlist.sort(key=len)  # Sort words by length
        self.len_indexes = self.get_length_indexes()  # Index positions where word length changes

    # Returns a list of indexes where word length increases in the sorted list
    def get_length_indexes(self):
        len_indexes = []
        length = 1
        for i in range(len(self.wordlist)):
            if len(self.wordlist[i]) > length:
                length += 1
                len_indexes.append(i)
        len_indexes.append(len(self.wordlist))
        return len_indexes

    # Generates a list of Enemy word objects based on the level and selected word lengths
    def get_words(self, level, choices):
        word_objs = []
        include = []
        vertical_spacing = (HEIGHT - 150) // level
        if True not in choices:
            choices[0] = True
        for i in range(len(choices)):
            if choices[i]:
                include.append((self.len_indexes[i], self.len_indexes[i + 1]))
        for i in range(level):
            speed = random.randint(3, 5)
            y_pos = random.randint(10 + (i * vertical_spacing),
                                   (i + 1) * vertical_spacing)
            x_pos = random.randint(WIDTH, WIDTH + 1000)
            ind_sel = random.choice(include)
            index = random.randint(ind_sel[0], ind_sel[1] - 1)
            text = self.wordlist[index].lower()
            if random.random() < 0.3:
                j = random.randint(0, len(text) - 1)
                text = text[:j] + text[j].upper() + text[j + 1:]
            word_objs.append(Enemy(text, speed, y_pos, x_pos))
        return word_objs


# Class representing a falling word (enemy) on the screen
class Enemy:
    def __init__(self, text, speed, y_pos, x_pos):
        self.text = text
        self.speed = speed
        self.y_pos = y_pos
        self.x_pos = x_pos

    # Draw the word and highlight matching prefix
    def draw(self, font, active_string):
        screen.blit(font.render(self.text, True, 'black'),
                    (self.x_pos, self.y_pos))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(font.render(active_string, True, (255, 198, 0)),
                        (self.x_pos, self.y_pos))

    # Move the word left based on its speed
    def update(self):
        self.x_pos -= self.speed


# Class responsible for drawing all menu and UI elements
class Menu:
    def __init__(self):
        self.header_font = pygame.font.SysFont('CALLUNA', 50)
        self.pause_font = pygame.font.SysFont('CALLUNA', 38)
        self.banner_font = pygame.font.SysFont('CALLUNA', 50)

    # Draws a circle button and returns True if clicked
    def draw_button(self, x, y, text, surf):
        clicked = False
        cir = pygame.draw.circle(surf, (45, 89, 135), (x, y), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.circle(surf, (190, 35, 35), (x, y), 35)
                clicked = True
            else:
                pygame.draw.circle(surf, (190, 89, 135), (x, y), 35)
        pygame.draw.circle(surf, 'black', (x, y), 35, 5)
        surf.blit(self.pause_font.render(text, True, 'white'),
                  (x - 15, y - 25))
        return clicked

    # Draws the HUD including level, score, and lives
    def draw_hud(self, level, active_string, score, high_score, lives):
        pygame.draw.rect(screen, (255, 198, 0), [0, HEIGHT - 100, WIDTH, 100])
        pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 5)
        pygame.draw.line(screen, 'black', (0, HEIGHT - 100),(WIDTH, HEIGHT - 100), 5)
        pygame.draw.line(screen, 'black', (300, HEIGHT - 100), (300, HEIGHT),5)
        pygame.draw.line(screen, 'black', (800, HEIGHT - 100), (800, HEIGHT),5)
        pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 5)
        screen.blit(self.header_font.render(f'Level: {level}', True, 'black'),(10, HEIGHT - 75))
        screen.blit(self.header_font.render(f'"{active_string}"', True, 'black'),(320, HEIGHT - 75))
        screen.blit(self.banner_font.render(f'Score: {score}', True, 'black'),(300, 10))
        screen.blit( self.banner_font.render(f'Best: {high_score}', True, 'black'),(550, 10))
        screen.blit(self.banner_font.render(f'Lives: {lives}', True, 'black'),(10, 10))

        return self.draw_button(948, HEIGHT - 52, 'II', screen)

    def draw_pause(self, choices):
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surface, (0, 0, 0, 100), [200, 200, 600, 400], 0, 5)
        pygame.draw.rect(surface, (0, 0, 0, 200), [200, 200, 600, 400], 5, 5)
        resume = self.draw_button(260, 300, '>', surface)
        quit_btn = self.draw_button(610, 300, 'X',surface)
        stat_btn = self.draw_button(950, 50, 'S',surface)
        surface.blit(self.header_font.render('MENU', True, 'white'),(210, 210))
        surface.blit(self.header_font.render('PLAY!', True, 'white'),(310, 275))
        surface.blit(self.header_font.render('QUIT', True, 'white'),(650, 275))
        surface.blit(self.header_font.render('Statistic', True, 'black'),(760, 30))
        surface.blit(self.header_font.render('Active Letter Lengths:', True, 'white'),(210, 350))

        changes = copy.deepcopy(choices)
        for i in range(len(choices)):
            btn = self.draw_button(260 + (i * 80), 450, str(i + 2),surface)
            if btn:
                changes[i] = not changes[i]
            if choices[i]:
                pygame.draw.circle(surface, (255, 198, 0),(260 + (i * 80), 450), 35, 5)

        screen.blit(surface, (0, 0))
        return resume, changes, quit_btn,stat_btn



# Main game class: runs the game loop and manages state
class Game:
    def __init__(self):
        self.dataset = Dataset()  # Manages word data
        self.menu = Menu()  # Manages UI and menu
        self.tracker = Tracker()
        self.font = pygame.font.SysFont(None, 48)
        self.score = 0
        self.high_score = self.load_high_score()
        self.level = 1
        self.lives = 5
        self.active_string = ''  # Current typed input
        self.submit = ''  # Word submitted (Enter or Space)
        self.word_objects = []  # List of active Enemy objects
        self.pause = True
        self.new_level = True
        self.choices = [False, True, False, False, False, False,
                        False]  # Word lengths toggle

    # Reads the high score from file
    def load_high_score(self):
        with open('high_score.txt', 'r') as f:
            return int(f.readline())

    # Writes the high score to file
    def save_high_score(self):
        with open('high_score.txt', 'w') as f:
            f.write(str(self.high_score))

    # Check if submitted word matches any enemy word
    def check_answer(self):
        matched = False
        for wrd in self.word_objects:
            if wrd.text == self.submit:
                points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 4)
                self.score += int(points)
                self.word_objects.remove(wrd)
                matched = True
                self.tracker.add_word(wrd.text)
                break
        if not matched:
            self.tracker.add_error()

    # Main game loop
    def run(self):
        running = True
        changes = None
        while running:
            screen.fill('gray')
            timer.tick(60)
            pause_click = self.menu.draw_hud(self.level, self.active_string,
                                             self.score, self.high_score,
                                             self.lives)

            if self.pause:
                resume, changes, quit_btn,stat_btn = self.menu.draw_pause(self.choices)
                if resume:
                    self.pause = False
                if quit_btn:
                    self.save_high_score()
                    break
                if stat_btn:
                    print("test")
                self.choices = changes

            if self.new_level and not self.pause:
                self.word_objects = self.dataset.get_words(self.level,
                                                           self.choices)
                for _ in self.word_objects:  # Track all newly spawned words
                    self.tracker.add_shown_word()
                self.new_level = False
            else:
                for word in self.word_objects[:]:
                    word.draw(self.font, self.active_string)
                    if not self.pause:
                        word.update()
                    if word.x_pos < -200:
                        self.tracker.add_missed_word()  # Track expired words
                        self.word_objects.remove(word)
                        self.lives -= 1

            if len(self.word_objects) <= 0 and not self.pause:
                self.level += 1
                self.new_level = True

            if self.submit:
                self.check_answer()
                self.submit = ''

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_high_score()
                    running = False

                if event.type == pygame.KEYDOWN:
                    # Track all keystrokes
                    if event.key == pygame.K_BACKSPACE:
                        self.tracker.add_keystroke(is_backspace=True)
                        self.active_string = self.active_string[:-1]
                    elif not self.pause:
                        self.tracker.add_keystroke()  # Count all keypresses

                        if event.unicode.isalpha():
                            # Check if keystroke matches any active word
                            is_correct = any(
                                word.text.startswith(
                                    self.active_string + event.unicode)
                                for word in self.word_objects
                            )
                            self.tracker.add_keystroke(correct=is_correct)
                            self.active_string += event.unicode

                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            self.submit = self.active_string
                            self.active_string = ''

                    if event.key == pygame.K_ESCAPE:
                        self.pause = not self.pause

                if event.type == pygame.MOUSEBUTTONUP and self.pause and event.button == 1:
                    self.choices = changes

            if pause_click:
                self.pause = True

            if self.lives < 0:
                self.tracker.save_to_csv(self.score)
                self.tracker.reset()
                self.pause = True
                self.level = 1
                self.lives = 5
                self.word_objects = []
                self.new_level = True
                self.save_high_score()
                self.score = 0

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    Game().run()
