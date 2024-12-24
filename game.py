#game.py
import pygame
import random
from models import Figure
from ui import Button, Label
import time


class Game:
    def __init__(self, screen, background_image, cylinder_image, crosshair_image):
        self.screen = screen
        self.background_image = background_image
        self.cylinder_image = cylinder_image
        self.crosshair_image = crosshair_image
        self.crosshair_image = pygame.transform.scale(crosshair_image, (30, 30))  # Инициализируем размер изображения
        self.crosshair_rect = self.crosshair_image.get_rect()
        self.player_figure = None
        self.computer_figure = None
        self.crosshair_rect = None
        self.player_score = 0
        self.computer_score = 0
        self.player_turn = True
        self.font = pygame.font.Font(None, 36)
        self.player_label = Label(screen.get_width() - 150, 10, "Игрок", self.font, (255, 255, 255))
        self.computer_label = Label(10, 10, "Компьютер", self.font, (255, 255, 255))
        self.player_score_label = Label(screen.get_width() - 150, 40, f"Счет: {self.player_score}", self.font,
                                        (255, 255, 255))
        self.computer_score_label = Label(10, 40, f"Счет: {self.computer_score}", self.font, (255, 255, 255))
        self.game_over = False
        self.restart_button = Button(screen.get_width() // 2 - 100, screen.get_height() // 2 + 50, 200, 50,
                                     "Начать заново", (0, 128, 255), (255, 255, 255), self.font, self.reset)
        self.exit_button = Button(screen.get_width() // 2 - 100, screen.get_height() // 2 + 120, 200, 50, "Выйти",
                                  (200, 200, 200), (0, 0, 0), self.font, self.exit_game)
        self.computer_turn_delay = 0.5
        self.computer_turn_timer = 0
        self.log_file = open("game_log.txt", "w", encoding="utf-8")
        self.log_event("Игра началась")

    def log_event(self, message):
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] {message}\n"
            self.log_file.write(log_message)
            self.log_file.flush()

    def reset(self):
        self.player_figure = None
        self.computer_figure = None
        self.crosshair_rect = None
        self.player_score = 0
        self.computer_score = 0
        self.player_turn = True
        self.game_over = False
        self.computer_turn_timer = 0
        self.start_game()
        self.log_event("Игра перезапущена")

    def exit_game(self):
        self.log_event("Игра завершена")
        self.log_file.close()
        pygame.quit()
        exit()

    def start_game(self):
        player_x = self.screen.get_width() * 3 / 4
        computer_x = self.screen.get_width() * 1 / 4
        y = self.screen.get_height() * 0.8
        self.player_figure = Figure(player_x, y, self.cylinder_image)
        self.computer_figure = Figure(computer_x, y, self.cylinder_image)
        self.crosshair_rect = self.crosshair_image.get_rect()
        pygame.mouse.set_visible(False)
        self.log_event(f"Начало игры")

    def update_scores(self):
        self.player_score_label.set_text(f"Счет: {self.player_score}")
        self.computer_score_label.set_text(f"Счет: {self.computer_score}")

    def handle_player_turn(self):
        if self.game_over:
            return

        mouse_pos = pygame.mouse.get_pos()
        self.crosshair_rect.center = mouse_pos

        if pygame.mouse.get_pressed()[0]:  # Check for left mouse button click
            target_cylinder = self.player_figure.get_cylinder_by_rect(self.crosshair_rect)
            if target_cylinder:
                self.log_event(f"Игрок сбил цилиндр на позиции {target_cylinder.rect.center}")
                self.remove_cylinder_with_stack(self.player_figure, target_cylinder)
            else:
                # Проверяем, кликнул ли игрок на цилиндр
                is_miss = False
                for cylinder in self.player_figure.get_cylinders():
                    if cylinder.rect.collidepoint(mouse_pos):
                        is_miss = True
                        break

                if is_miss:
                    self.log_event("Игрок промахнулся")
            self.player_turn = False
            self.computer_turn_timer = time.time()

    def handle_computer_turn(self):
        if self.game_over or self.player_turn:
            return

        if time.time() - self.computer_turn_timer >= self.computer_turn_delay:

            if not self.computer_figure.get_cylinders():
                self.player_turn = True
                return

            # Вероятность промаха 1 из 5
            if random.randint(1, 5) == 1:
                self.log_event("Компьютер промахнулся")
                self.player_turn = True
            else:
                target_cylinder = random.choice(self.computer_figure.get_cylinders())
                self.log_event(f"Компьютер сбил цилиндр на позиции {target_cylinder.rect.center}")
                self.remove_cylinder_with_stack(self.computer_figure, target_cylinder, is_computer=True)
                self.player_turn = True

    def remove_cylinder_with_stack(self, figure, target_cylinder, is_computer=False):

        stack = []
        stack.append(target_cylinder)
        removed_count = 0
        while len(stack):
            cylinder = stack.pop()
            figure.remove_cylinder(cylinder)
            removed_count += 1
            for next_cylinder in figure.get_cylinders():
                if next_cylinder.stack_level == cylinder.stack_level - 1 and next_cylinder.rect.centerx == cylinder.rect.centerx:
                    stack.append(next_cylinder)

        if is_computer:
            self.computer_score += removed_count
        else:
            self.player_score += removed_count
        if is_computer:
            self.log_event(
                f"Компьютер сбил цилиндр {target_cylinder.rect.center}. Всего удалено {self.computer_score} цилиндров")
        else:
            self.log_event(f"Игрок сбил цилиндр {target_cylinder.rect.center}. Всего удалено {self.player_score} цилиндров")

        self.update_scores()
        self.check_game_over()

    def check_game_over(self):
        if not self.player_figure.get_cylinders() or not self.computer_figure.get_cylinders():
            self.game_over = True
            pygame.mouse.set_visible(True)
        if self.game_over:
            if self.player_score > self.computer_score:
                self.log_event("Игра окончена. Победил игрок!")
            elif self.computer_score > self.player_score:
                self.log_event("Игра окончена. Победил компьютер!")
            else:
                self.log_event("Игра окончена. Ничья!")

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))

        if self.player_figure:
            for cylinder in self.player_figure.get_cylinders():
                self.screen.blit(cylinder.image, cylinder.rect)

        if self.computer_figure:
            for cylinder in self.computer_figure.get_cylinders():
                self.screen.blit(cylinder.image, cylinder.rect)

        self.player_label.draw(self.screen)
        self.computer_label.draw(self.screen)
        self.player_score_label.draw(self.screen)
        self.computer_score_label.draw(self.screen)

        if self.crosshair_rect and not self.game_over:
            self.screen.blit(self.crosshair_image, self.crosshair_rect)

        if self.game_over:
            winner_text = "Победил игрок!" if self.player_score > self.computer_score else "Победил компьютер!" if self.computer_score > self.player_score else "Ничья!"
            winner_label = Label(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 100, winner_text,
                                 self.font, (255, 255, 255))
            winner_label.draw(self.screen)
            player_score_text = f"Счет игрока: {self.player_score}"
            player_score_label = Label(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 50,
                                       player_score_text, self.font, (255, 255, 255))
            player_score_label.draw(self.screen)
            computer_score_text = f"Счет компьютера: {self.computer_score}"
            computer_score_label = Label(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 20,
                                         computer_score_text, self.font, (255, 255, 255))
            computer_score_label.draw(self.screen)
            self.restart_button.draw(self.screen)
            self.exit_button.draw(self.screen)

    def handle_events(self, event):
        if self.game_over:
            self.restart_button.handle_event(event)
            self.exit_button.handle_event(event)