import enum

class GameState(enum.Enum):
    NOT_STARTED = 0
    ROUND_ACTIVE = 1
    ROUND_DONE = 2
    GAME_OVER = 3
    import arcade

    class AttackAnimation(arcade.Sprite):
        def __init__(self, sprite_files):
            super().__init__(sprite_files[0])
            self.sprite_files = sprite_files
            self.current_frame = 0
            self.frame_count = len(sprite_files)
            self.set_texture(0)
            self.is_animating = False

        def start(self):
            self.current_frame = 0
            self.is_animating = True

        def update(self):
            if self.is_animating:
                self.set_texture(self.current_frame)
                self.current_frame += 1
                if self.current_frame >= self.frame_count:
                    self.is_animating = False

import arcade
import random
from game_state import GameState
from attack_animation import AttackAnimation

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Roche, Papier, Ciseaux"

# Les chemins vers les assets
ASSET_PATH = "assets/"

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
        self.game_state = GameState.NOT_STARTED
        self.player_score = 0
        self.computer_score = 0
        self.message = "Appuyez sur ENTER pour commencer"
        self.player_choice = None
        self.computer_choice = None

        # Charger les textures
        self.rock_texture = arcade.load_texture(ASSET_PATH + "rock.png")
        self.paper_texture = arcade.load_texture(ASSET_PATH + "paper.png")
        self.scissors_texture = arcade.load_texture(ASSET_PATH + "scissors.png")
        self.font_size = 20

        # Sprites pour animations
        self.attack_sprite = None

        # Position des choix
        self.choices_positions = {
            "rock": (200, 200),
            "paper": (400, 200),
            "scissors": (600, 200)
        }

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()
        # Afficher le message
        arcade.draw_text(self.message, 50, 550, arcade.color.WHITE, self.font_size)
        # Afficher les scores
        score_text = f"Player: {self.player_score}  -  Computer: {self.computer_score}"
        arcade.draw_text(score_text, 50, 520, arcade.color.WHITE, self.font_size)

        # Afficher les options si le jeu n'a pas commencé ou est en cours
        if self.game_state in [GameState.NOT_STARTED, GameState.ROUND_ACTIVE]:
            # Dessiner les options de choix
            arcade.draw_text("Roche", self.choices_positions["rock"][0] - 20, self.choices_positions["rock"][1] - 40, arcade.color.WHITE, self.font_size)
            arcade.draw_text("Papier", self.choices_positions["paper"][0] - 20, self.choices_positions["paper"][1] - 40, arcade.color.WHITE, self.font_size)
            arcade.draw_text("Ciseaux", self.choices_positions["scissors"][0] - 30, self.choices_positions["scissors"][1] - 40, arcade.color.WHITE, self.font_size)

        # Si une attaque est en cours, la dessiner
        if self.attack_sprite:
            self.attack_sprite.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_state == GameState.ROUND_ACTIVE:
            # Déterminer quelle option le clic correspond
            for choice, pos in self.choices_positions.items():
                rect = arcade.get_rectangle(center_x=pos[0], center_y=pos[1], width=100, height=100)
                if rect and arcade.check_for_collision_point_list((x, y), [rect]):
                    self.player_choice = choice
                    self.start_computer_choice()

    def start_computer_choice(self):
        self.computer_choice = random.choice(["rock", "paper", "scissors"])
        self.determine_winner()

    def determine_winner(self):
        result = None
        if self.player_choice == self.computer_choice:
            result = "Égalité"
        elif (self.player_choice == "rock" and self.computer_choice == "scissors") or \
             (self.player_choice == "scissors" and self.computer_choice == "paper") or \
             (self.player_choice == "paper" and self.computer_choice == "rock"):
            result = "Vous gagnez cette ronde!"
            self.player_score += 1
        else:
            result = "L'ordinateur gagne cette ronde!"
            self.computer_score += 1

        self.message = f"Vous avez choisi {self.player_choice}. L'ordinateur a choisi {self.computer_choice}. {result}\nAppuyez sur ESPACE pour continuer."
        self.game_state = GameState.ROUND_DONE

        # Charger et lancer l'animation ici si nécessaire
        self.show_attack_animation()

    def show_attack_animation(self):
        # En fonction de la victoire, charger la bonne animation
        # Exemple: animations pour chaque attaque
        pass

    def on_key_press(self, key, modifiers):
        if self.game_state == GameState.NOT_STARTED:
            if key == arcade.key.ENTER:
                self.message = "Choisissez votre attaque: Roche, Papier, ou Ciseaux."
                self.game_state = GameState.ROUND_ACTIVE
        elif self.game_state == GameState.ROUND_DONE:
            if key == arcade.key.SPACE:
                # Vérifier si la partie est finie
                if self.player_score >= 3:
                    self.message = "Félicitations! Vous avez gagné la partie! Appuyez sur ENTER pour rejouer."
                    self.game_state = GameState.GAME_OVER
                elif self.computer_score >= 3:
                    self.message = "L'ordinateur a gagné la partie! Appuyez sur ENTER pour rejouer."
                    self.game_state = GameState.GAME_OVER
                else:
                    self.message = "Choisissez votre attaque: Roche, Papier, ou Ciseaux."
                    self.game_state = GameState.ROUND_ACTIVE
        elif self.game_state == GameState.GAME_OVER:
            if key == arcade.key.ENTER:
                # Reset des scores et de l'état
                self.player_score = 0
                self.computer_score = 0
                self.message = "Appuyez sur ENTER pour commencer une nouvelle partie."
                self.game_state = GameState.NOT_STARTED

    def update(self, delta_time):
        # Mettre à jour animations si nécessaires
        if self.attack_sprite:
            self.attack_sprite.update()

def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()