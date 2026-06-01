from enum import Enum

class Speed(Enum):
    SPEED_1 = 1
    SPEED_2 = 2
    SPEED_3 = 3
    SPEED_4 = 4
    SPEED_5 = 5

    @staticmethod
    def from_value(value: int):
        values = {
            1: Speed.SPEED_1,
            2: Speed.SPEED_2,
            3: Speed.SPEED_3,
            4: Speed.SPEED_4,
            5: Speed.SPEED_5,
        }
        if value in list(values.keys()):
            return values[value]
        else :
            print("warning: unable to find specified speed, using Speed 5")
            return Speed.SPEED_5 # default value

class Brightness(Enum):
    BRIGHTNESS_0 = 0x00
    BRIGHTNESS_1 = 0X01
    BRIGHTNESS_2 = 0X02
    BRIGHTNESS_3 = 0X03
    BRIGHTNESS_4 = 0X04
    BRIGHTNESS_5 = 0X05

    @staticmethod
    def from_value(value: int):
        values = {
            0: Brightness.BRIGHTNESS_0,
            1: Brightness.BRIGHTNESS_1,
            2: Brightness.BRIGHTNESS_2,
            3: Brightness.BRIGHTNESS_3,
            4: Brightness.BRIGHTNESS_4,
            5: Brightness.BRIGHTNESS_5,
        }
        if value in list(values.keys()):
            return values[value]
        else :
            print("warning: unable to find specified brightness, using Brightness 5")
            return Brightness.BRIGHTNESS_5 # default value

class RainbowMode(Enum):
    OFF = 0x00
    ON = 0x07

    @staticmethod
    def from_value(value: bool):
        if value:
            return RainbowMode.ON
        else :
            return RainbowMode.OFF

class Sleep(Enum):
    SLEEP_5_MIN = 0x01
    SLEEP_10_MIN = 0x02
    SLEEP_20_MIN = 0x03
    SLEEP_30_MIN = 0x04
    SLEEP_NEVER = 0x05

    @staticmethod
    def from_value(value: int):
        values = {
            1: Sleep.SLEEP_5_MIN,
            2: Sleep.SLEEP_10_MIN,
            3: Sleep.SLEEP_20_MIN,
            4: Sleep.SLEEP_30_MIN,
            5: Sleep.SLEEP_NEVER,
        }
        if value in list(values.keys()):
            return values[value]
        else :
            print("warning: unable to find specified sleep value, using Never Sleep")
            return Sleep.SLEEP_NEVER # default value

class Animation(Enum):
    RETRO_SNAKE = 0x01
    NEON_STREAM = 0x02
    REACTION = 0x03
    SINE_WAVE = 0x04 
    STEADY = 0x05
    BREATHING = 0x06
    RAINBOW = 0x07
    FLASH_AWAY = 0x08
    RAINDROPS = 0x09
    RAINBOW_WHEEL = 0x0a
    RIPPLES_SHINING = 0x0b
    STARS_TWINKLE = 0x0c
    SHADOW_DISAPPEAR = 0x0d
    # GAME_MODE = 0x0e

    @staticmethod
    def from_value(value: str):
        values = {
            "retro_snake": Animation.RETRO_SNAKE,
            "neon_stream": Animation.NEON_STREAM,
            "reaction": Animation.REACTION,
            "sine_wave": Animation.SINE_WAVE,
            "steady": Animation.STEADY,
            "breathing": Animation.BREATHING,
            "rainbow": Animation.RAINBOW,
            "flash_away": Animation.FLASH_AWAY,
            "raindrops": Animation.RAINDROPS,
            "rainbow_wheel": Animation.RAINBOW_WHEEL,
            "ripples_shining": Animation.RIPPLES_SHINING,
            "stars_twinkle": Animation.STARS_TWINKLE,
            "shadow_disappear": Animation.SHADOW_DISAPPEAR,
            # "game_mode": Animation.GAME_MODE
        }
        if value in list(values.keys()):
            return values[value]
        else :
            print("warning: unable to find specified animation, using Steady")
            return Animation.STEADY # default value