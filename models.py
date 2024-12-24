#models.py
import pygame


class Cylinder(pygame.sprite.Sprite):
    def __init__(self, image, x, y, stack_level=0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.stack_level = stack_level


class Figure:
    def __init__(self, x, y, cylinders_image):
        self.cylinders = []
        self.base_x = x
        self.base_y = y
        self.cylinder_image = cylinders_image
        self.create_figure()

    def create_figure(self):
        positions = [
            (0, 0),  # Нижний слой
            (0, -55),  # Второй слой
            (40, -55),  # Третий слой
            (-40, -55),  # Третий слой
            (0, -110)  # Верхний слой
        ]
        for i, (offset_x, offset_y) in enumerate(positions):
            x = self.base_x + offset_x
            y = self.base_y + offset_y
            cylinder = Cylinder(self.cylinder_image, x, y, stack_level=i)
            self.cylinders.append(cylinder)

    def get_cylinder_by_rect(self, rect):
        for cylinder in self.cylinders:
            if cylinder.rect.colliderect(rect):
                return cylinder
        return None

    def remove_cylinder(self, cylinder):
        self.cylinders.remove(cylinder)

    def get_cylinders(self):
        return self.cylinders