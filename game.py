"""Game"""
import os
import pygame
from pygame.math import Vector2

from car import Car
from audio_effect import AudioEffect

ASSET_DIR = 'assets'
ASSET_CAR = 'car.png'
ASSET_BATTERY = 'battery.png'
WIDTH = 1280
HEIGHT = 720
BATTERY_WIDTH = 100
BATTERY_HEIGHT = 20
BATTERY_X = WIDTH - BATTERY_WIDTH - 100
BATTERY_Y = 10
TICKS = 60
PPU = 32

class Game:
    """models the simulation"""

    def __init__(self):
        """initialisation"""
        pygame.init()
        pygame.mixer.set_num_channels(2)
        pygame.mixer.init()
        pygame.display.set_caption("RC Car")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.exit = False
        image_path = self._from_asset_dir(ASSET_CAR) # 173x82
        self.car_image = pygame.transform.scale(pygame.image.load(image_path),(50,25))
        self.car = Car(0, 0, self.play_audio)

    def run(self):
        """main loop"""
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            self.car.command(pygame.key.get_pressed(), self.clock.get_time()/1000)
            self._draw()
            self.clock.tick(TICKS)

        pygame.quit()

    def play_audio(self, audio:AudioEffect):
        """play sound"""
        sound = pygame.mixer.Sound(self._from_asset_dir(audio.value.path))
        pygame.mixer.Channel(audio.value.channel).play(sound)

    def _draw(self):
        """updates the screen"""
        self.screen.fill((50, 50, 50))
        rotated = pygame.transform.rotate(self.car_image, self.car.angle)
        rect = rotated.get_rect()
        self.screen.blit(rotated, self.car.position * PPU - (rect.width / 2, rect.height / 2))

        self._draw_battery()
        pygame.display.flip()

    def _draw_battery(self):
        """draw the battery bar and icon"""
        level = self.car.get_battery_level()
        (battery_rect_bg,battery_image_bg) = self._create_battery_bar_bg()
        (battery_rect,battery_image) = self._create_battery_bar(level)
        self.screen.blit(battery_image_bg, battery_rect_bg,
            (0, 0, battery_rect_bg.w, battery_rect_bg.h))
        self.screen.blit(battery_image, battery_rect,
            (0, 0, battery_rect.w/100*level, battery_rect.h))
        # icon
        image_path = self._from_asset_dir(ASSET_BATTERY)
        battery_image = pygame.transform.scale(pygame.image.load(image_path),(16,12))
        self.screen.blit(battery_image, Vector2(BATTERY_X-25, BATTERY_Y+5))

    def _create_battery_bar_bg(self):
        """creates the battery bar"""
        battery_image = pygame.Surface((BATTERY_WIDTH+2, BATTERY_HEIGHT+2))
        black = pygame.Color(0,0,0)
        for x in range(battery_image.get_width()):
            for y in range(battery_image.get_height()):
                battery_image.set_at((x, y), black)
        self.battery_bar = pygame.Surface((BATTERY_WIDTH+2, BATTERY_HEIGHT+2))
        battery_rect = self.battery_bar.get_rect(topleft=(BATTERY_X-1, BATTERY_Y-1))
        return (battery_rect, battery_image)

    def _create_battery_bar(self, level:float):
        """creates the battery bar"""
        battery_image = pygame.Surface((BATTERY_WIDTH, BATTERY_HEIGHT))
        color = pygame.Color(0, 0xff, 0) if level > 30 \
            else pygame.Color(0xff, 0xff, 0) if level>10 \
                else pygame.Color(0xff, 0, 0)
        for x in range(battery_image.get_width()):
            for y in range(battery_image.get_height()):
                battery_image.set_at((x, y), color)
        self.battery_bar = pygame.Surface((BATTERY_WIDTH, BATTERY_HEIGHT))
        battery_rect = self.battery_bar.get_rect(topleft=(BATTERY_X, BATTERY_Y))
        return (battery_rect, battery_image)

    def _from_asset_dir(self, asset_name):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(f'{base_dir}/{ASSET_DIR}', asset_name)
