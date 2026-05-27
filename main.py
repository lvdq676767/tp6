"""
ecrit par Ludovic Bodson
TP6
"""

import arcade
import random
from game_state import GameState
from attack_animation import AttackAnimation, AttackType

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_TITLE = "Roche, papier, ciseaux"

SCORE_TO_WIN = 3

WINS = {
    AttackType.ROCK: AttackType.SCISSORS,
    AttackType.PAPER: AttackType.ROCK,
    AttackType.SCISSORS: AttackType.PAPER,
}

PLAYER_ATTACK_POSITIONS = [
    (170, 160),
    (260, 160),
    (350, 160),
]

COMPUTER_ATTACK_X = 620
COMPUTER_ATTACK_Y = 160


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        self.game_state = GameState.NOT_STARTED
        self.player_score = 0
        self.computer_score = 0
        self.player_choice = None
        self.computer_choice = None
        self.round_result_text = ""

        self.player_avatar = None
        self.computer_avatar = None

        # SpriteList to group and draw the avatars together (Arcade 3.0+ compliance)
        self.avatar_sprites = arcade.SpriteList()

        self.rock = AttackAnimation(AttackType.ROCK)
        self.paper = AttackAnimation(AttackType.PAPER)
        self.scissors = AttackAnimation(AttackType.SCISSORS)

        self.computer_attack_sprite = None

        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.rock)
        self.player_sprites.append(self.paper)
        self.player_sprites.append(self.scissors)

    def setup(self):
        self.player_score = 0
        self.computer_score = 0
        self.player_choice = None
        self.computer_choice = None
        self.round_result_text = ""
        self.game_state = GameState.NOT_STARTED
        self.computer_attack_sprite = None

        # Reset the avatar sprite list
        self.avatar_sprites = arcade.SpriteList()

        # Configure and add the player avatar
        self.player_avatar = arcade.Sprite("assets/faceBeard.png")
        self.player_avatar.center_x = 260
        self.player_avatar.center_y = 360
        self.player_avatar.scale = 0.5
        self.avatar_sprites.append(self.player_avatar)

        # Configure and add the computer avatar
        self.computer_avatar = arcade.Sprite("assets/compy.png")
        self.computer_avatar.center_x = 620
        self.computer_avatar.center_y = 360
        self.computer_avatar.scale = 0.5
        self.avatar_sprites.append(self.computer_avatar)

        # Initial positions for attack choice buttons
        for sprite, pos in zip(self.player_sprites, PLAYER_ATTACK_POSITIONS):
            sprite.center_x = pos[0]
            sprite.center_y = pos[1]
            sprite.scale = 0.6
            sprite.stop_animation()

    def on_draw(self):
        self.clear()

        # 1. Draw static elements (Avatars drawn through SpriteList)
        self.avatar_sprites.draw()

        # Outlines for weapon boxes
        for pos in PLAYER_ATTACK_POSITIONS:
            arcade.draw.draw_rect_outline(arcade.XYWH(pos[0], pos[1], 75, 75), arcade.color.LIGHT_GRAY, 2)

        arcade.draw.draw_rect_outline(arcade.XYWH(COMPUTER_ATTACK_X, COMPUTER_ATTACK_Y, 75, 75),
                                      arcade.color.LIGHT_GRAY, 2)

        # Title and scores
        arcade.draw_text(WINDOW_TITLE, WINDOW_WIDTH / 2, 450, arcade.color.GOLD, 24, anchor_x="center",
                         font_name="Arial Bold")
        arcade.draw_text(f"Joueur: {self.player_score}", 260, 280, arcade.color.CYAN, 14, anchor_x="center")
        arcade.draw_text(f"Ordinateur: {self.computer_score}", 620, 280, arcade.color.ORANGE, 14, anchor_x="center")

        # 2. Draw based on the active GameState
        if self.game_state == GameState.NOT_STARTED:
            arcade.draw_text("Appuyer sur 'ESPACE' pour débuter une ronde!", WINDOW_WIDTH / 2, 230, arcade.color.WHITE,
                             14, anchor_x="center")

        elif self.game_state == GameState.ROUND_ACTIVE:
            arcade.draw_text("Cliquez sur une image pour faire une attaque!", WINDOW_WIDTH / 2, 230, arcade.color.WHITE,
                             14, anchor_x="center")
            self.player_sprites.draw()

        elif self.game_state == GameState.ROUND_DONE:
            arcade.draw_text(self.round_result_text, WINDOW_WIDTH / 2, 240, arcade.color.YELLOW, 16, anchor_x="center",
                             bold=True)
            arcade.draw_text("Appuyer sur 'ESPACE' pour commencer une nouvelle ronde!", WINDOW_WIDTH / 2, 210,
                             arcade.color.WHITE, 12, anchor_x="center")

            # Use a temporary SpriteList to safely draw the chosen sprites in Arcade 3.0+
            revealed_sprites = arcade.SpriteList()

            player_sprite = self.player_choice_sprite()
            if player_sprite:
                revealed_sprites.append(player_sprite)
            if self.computer_attack_sprite:
                revealed_sprites.append(self.computer_attack_sprite)

            revealed_sprites.draw()

        elif self.game_state == GameState.GAME_OVER:
            if self.player_score >= SCORE_TO_WIN:
                end_text = "Vous avez gagné la partie !"
            else:
                end_text = "L'ordinateur a gagné la partie !"
            arcade.draw_text(end_text, WINDOW_WIDTH / 2, 240, arcade.color.RED, 18, anchor_x="center", bold=True)
            arcade.draw_text("Appuyer sur 'ESPACE' pour rejouer", WINDOW_WIDTH / 2, 200, arcade.color.WHITE, 12,
                             anchor_x="center")

    def on_update(self, delta_time):
        self.player_sprites.update(delta_time)
        if self.computer_attack_sprite:
            self.computer_attack_sprite.update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.game_state == GameState.NOT_STARTED:
                self._start_round()
            elif self.game_state == GameState.ROUND_DONE:
                self._start_round()
            elif self.game_state == GameState.GAME_OVER:
                self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_state != GameState.ROUND_ACTIVE:
            return

        for sprite in self.player_sprites:
            if sprite.collides_with_point((x, y)):
                self.player_choice = sprite.attack_type
                self._resolve_round()
                break

    def player_choice_sprite(self):
        for sprite in self.player_sprites:
            if sprite.attack_type == self.player_choice:
                return sprite
        return None

    def _start_round(self):
        self.player_choice = None
        self.computer_choice = None
        self.computer_attack_sprite = None
        self.round_result_text = ""
        self.game_state = GameState.ROUND_ACTIVE

        for sprite in self.player_sprites:
            sprite.start_animation()

    def _resolve_round(self):
        for sprite in self.player_sprites:
            sprite.stop_animation()

        player_sprite = self.player_choice_sprite()
        if player_sprite:
            player_sprite.show_attack_frame()

        # Computer AI choice
        self.computer_choice = random.choice(list(AttackType))

        # Instantiate the computer weapon sprite dynamically
        self.computer_attack_sprite = AttackAnimation(self.computer_choice)
        self.computer_attack_sprite.center_x = COMPUTER_ATTACK_X
        self.computer_attack_sprite.center_y = COMPUTER_ATTACK_Y
        self.computer_attack_sprite.scale = 0.6
        self.computer_attack_sprite.show_attack_frame()

        # Scoring logic
        if self.player_choice == self.computer_choice:
            self.round_result_text = "Égalité !"
        elif WINS[self.player_choice] == self.computer_choice:
            self.player_score += 1
            self.round_result_text = "Vous avez gagné la ronde !"
        else:
            self.computer_score += 1
            self.round_result_text = "L'ordinateur a gagné la ronde !"

        if self.player_score >= SCORE_TO_WIN or self.computer_score >= SCORE_TO_WIN:
            self.game_state = GameState.GAME_OVER
        else:
            self.game_state = GameState.ROUND_DONE


if __name__ == "__main__":
    game = MyGame()
    game.setup()
    arcade.run()