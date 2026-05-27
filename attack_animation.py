import arcade
from enum import Enum

class AttackType(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

ATTACK_TEXTURES = {
    AttackType.ROCK: ("assets/srock.png", "assets/srock-attack.png"),
    AttackType.PAPER: ("assets/spaper.png", "assets/spaper-attack.png"),
    AttackType.SCISSORS: ("assets/scissors.png", "assets/scissors-close.png"),
}

class AttackAnimation(arcade.Sprite):
    def __init__(self, attack_type: AttackType):
        super().__init__()
        self.attack_type = attack_type
        self.textures = []
        for path in ATTACK_TEXTURES[attack_type]:
            self.textures.append(arcade.load_texture(path))
        self.current_texture = 0
        self.texture = self.textures[self.current_texture]
        self.animation_timer = 0
        self.animation_speed = 0.2
        self.animating = False

    def start_animation(self):
        self.animating = True

    def stop_animation(self):
        self.animating = False
        self.current_texture = 0
        self.texture = self.textures[self.current_texture]

    def show_attack_frame(self):
        self.current_texture = 1
        self.texture = self.textures[self.current_texture]

    def update(self, delta_time: float = 1 / 60):
        if not self.animating:
            return
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_texture = 1 - self.current_texture
            self.texture = self.textures[self.current_texture]