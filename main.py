from app import Dataset, Menu
from Tracker import Tracker
from statistic_page import StatPage
import pygame

class Game:
    def __init__(self):
        self.dataset = Dataset()  # Manages word data
        self.menu = Menu()  # Manages UI and menu
        self.tracker = Tracker()
        self.font = pygame.font.SysFont(None, 48)
        self.score = 0
        self.level = 1
        self.lives = 5
        self.active_string = ''  # Current typed input
        self.submit = ''  # Word submitted (Enter or Space)
        self.word_objects = []  # List of active Enemy objects
        self.pause = True
        self.new_level = True
        self.choices = [False, False, True, True, True, False,
                        False]  # Word lengths toggle
        self.high_score_ = self.tracker.read_csv('statistics.csv')
        self.high_score = self.high_score_['Score'].max()


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
                resume, changes, quit_btn, stat_btn = self.menu.draw_pause(
                    self.choices)
                if resume:
                    self.pause = False
                if quit_btn:
                    break
                if stat_btn:
                    StatPage()
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

            if self.lives <= 0:
                pause_click = self.menu.draw_hud(self.level,
                                                 self.active_string,
                                                 self.score, self.high_score,
                                                 self.lives)

                self.tracker.save_to_csv(self.score)
                self.tracker.reset()
                self.pause = True
                self.level = 1
                self.lives = 5
                self.word_objects = []
                self.new_level = True
                self.score = 0

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    WIDTH, HEIGHT = 1000, 800
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Type Defender')
    timer = pygame.time.Clock()
    Game().run()

