# -*- coding: utf-8 -*-
# author: Ethosa

import sys

from pygame import display, image
import pygame

from pygamegui.gui import View, Manager

pygame.init()


class Game:
    def __init__(self, width=1024, height=720, name="window",
                 icon="icon.jpg"):
        self.width = width
        self.height = height
        self.size = [self.width, self.height]

        display.set_caption(name)
        if icon:
            display.set_icon(image.load(icon))

        self.display = display.set_mode(self.size)
        self.screen = pygame.Surface((width, height))
        self.screen = self.screen.convert_alpha()
        self.clock = pygame.time.Clock()

        self.manager = Manager(self)
        view = View(background_color=(155, 201, 175, 255))

        view.set_border_width(5)
        view.set_border_color("#21212155")

        view1 = View(width=155, height=155)
        view1.move(50, 50)
        view1.set_background_color("#21212155")
        view1.set_ripple_color("#ffffff")

        view2 = View()
        view2.move(75, 75)
        view2.set_background_color("#91eda455")
        view2.set_ripple_color("#ffffff")
        view2.set_border(1, "#33333344")

        view.set_ripple_color("#ffffff")
        view1.set_shadow((0, 0, 0, 128), (0, 0), 1.2)

        view3 = View(width=155)
        view3.move(256, 256)
        view3.set_background("#e0e0e0")
        view3.set_ripple_color((45, 45, 255))
        view3.set_shadow((0, 0, 0, 128), (0, 0), 1.2)

        view3.set_gradient((128, 0), (256-64, 128), "#212121", "#e0e0e0")

        self.manager.add(view, view1, view2, view3)

        def clicked(pos):
            view3.set_gradient((128, 128), pos, "#212121", "#e0e0e0")
            self.manager.take_screenshot("hello_world.png")
        view3.on_click(clicked)

    def render(self):
        self.manager.draw()
        self.display.blit(self.screen, (0, 0))

    def start_loop(self):
        while 1:
            self.clock.tick(60)
            self.handle_events()
            self.render()
            display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.manager.event()


if __name__ == '__main__':
    game = Game(670, 512)
    game.start_loop()
