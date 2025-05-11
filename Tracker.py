import time
import csv
import pandas as pd


class Tracker:
    def __init__(self):
        self.start_time = time.time()
        self.words_typed = 0
        self.correct_words = 0
        self.incorrect_words = 0
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.backspace_count = 0
        self.word_streak = 0
        self.longest_streak = 0
        self.chars_typed = 0
        self.words_shown = 0
        self.words_missed = 0
        self.total_word_length = 0
        self.last_word_time = self.start_time
        self.word_times = []

    def add_word(self, word):
        self.words_typed += 1
        self.correct_words += 1
        self.word_streak += 1
        self.longest_streak = max(self.word_streak, self.longest_streak)
        self.chars_typed += len(word)
        self.total_word_length += len(word)
        self.word_times.append(time.time() - self.last_word_time)
        self.last_word_time = time.time()

    def add_error(self):
        self.incorrect_words += 1
        self.word_streak = 0

    def add_keystroke(self, correct=False, is_backspace=False):
        self.total_keystrokes += 1
        if is_backspace:
            self.backspace_count += 1
        elif correct:
            self.correct_keystrokes += 1

    def add_shown_word(self):
        self.words_shown += 1

    def add_missed_word(self):
        self.words_missed += 1

    def calculate_wpm(self, net=True):
        elapsed = (time.time() - self.start_time) / 60
        if net:
            return self.correct_words / elapsed if elapsed > 0 else 0
        return (self.correct_words + self.incorrect_words) / elapsed if elapsed > 0 else 0

    def calculate_kpm(self):
        elapsed = (time.time() - self.start_time) / 60
        return self.total_keystrokes / elapsed if elapsed > 0 else 0

    def accuracy(self, word_level=False):
        if word_level:
            total_attempts = self.correct_words + self.incorrect_words
            return (self.correct_words / total_attempts) * 100 if total_attempts > 0 else 0
        else:
            total_chars = self.total_keystrokes - self.backspace_count
            return (self.correct_keystrokes / total_chars) * 100 if total_chars > 0 else 0

    def error_rate(self):
        total_chars = self.total_keystrokes - self.backspace_count
        errors = total_chars - self.correct_keystrokes
        return (errors / total_chars) * 100 if total_chars > 0 else 0

    def average_word_length(self):
        return self.total_word_length / self.correct_words if self.correct_words > 0 else 0

    def average_word_time(self):
        return sum(self.word_times) / len(
            self.word_times) if self.word_times else 0

    def total_time_played(self):
        return time.time() - self.start_time

    def reset(self):
        self.__init__()

    @staticmethod
    def read_csv(path):
        return pd.read_csv(path)

    def save_to_csv(self, score):
        with open('statistics.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                round(self.calculate_wpm(net=True), 2),
                round(self.calculate_wpm(net=False), 2),
                round(self.calculate_kpm(), 2),
                round(self.accuracy(word_level=True), 2),
                round(self.accuracy(word_level=False), 2),
                round(self.error_rate(), 2),
                score,
                self.words_typed,
                self.correct_words,
                self.incorrect_words,
                self.chars_typed,
                self.correct_keystrokes,
                self.backspace_count,
                self.longest_streak,
                round(self.average_word_length(), 2),
                round(self.average_word_time(), 3),
                round(self.total_time_played(), 2),
                self.words_shown,
                self.words_missed
            ])
