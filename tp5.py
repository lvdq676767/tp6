"""
tp5- dessiner avec arcade
code par ludovic bodson 401
"""

import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_TITLE = "Le magnifique Parc National de Banff - TP5"


def dessiner_ciel_et_soleil():
    arcade.draw_circle_filled(150, 500, 45, arcade.color.AMBER)


def dessiner_montagnes_rocheuses():
    arcade.draw_triangle_filled(
        50, 300, 250, 520, 450, 300, arcade.color.LIGHT_SLATE_GRAY
    )
    arcade.draw_triangle_filled(
        250, 300, 500, 560, 750, 300, arcade.color.SLATE_GRAY
    )
    arcade.draw_triangle_filled(
        420, 470, 500, 560, 580, 470, arcade.color.WHITE
    )


def dessiner_lac_turquoise():
    arcade.draw_lrbt_rectangle_filled(
        0, SCREEN_WIDTH, 0, 300, arcade.color.TURQUOISE_BLUE
    )
    arcade.draw_line(0, 300, SCREEN_WIDTH, 300, arcade.color.DARK_SLATE_GRAY, 2)


def dessiner_rive_et_foret():
    arcade.draw_lrbt_rectangle_filled(
        0, SCREEN_WIDTH, 220, 300, arcade.color.DARK_GREEN
    )

    # Sapin 1 (Gauche)
    r1 = arcade.rect.XYWH(60, 240, 20, 50)
    arcade.draw_rect_filled(r1, arcade.csscolor.BROWN)
    arcade.draw_polygon_filled([(20, 270), (120, 270), (70, 350)], arcade.color.LIME_GREEN)

    # Sapin 2 (Gauche - Arrière)
    r2 = arcade.rect.XYWH(140, 250, 15, 45)
    arcade.draw_rect_filled(r2, arcade.csscolor.BROWN)
    arcade.draw_polygon_filled([(110, 280), (185, 280), (147, 345)], arcade.color.LIME_GREEN)

    # Sapin 3 (Centre Gauche)
    r3 = arcade.rect.XYWH(240, 235, 18, 50)
    arcade.draw_rect_filled(r3, arcade.csscolor.BROWN)
    arcade.draw_polygon_filled([(200, 265), (290, 265), (249, 335)], arcade.color.LIME_GREEN)

    # Sapin 4 (Centre Droit)
    r4 = arcade.rect.XYWH(560, 235, 18, 50)
    arcade.draw_rect_filled(r4, arcade.csscolor.BROWN)
    arcade.draw_polygon_filled([(520, 265), (610, 265), (569, 345)], arcade.color.LIME_GREEN)

    # Sapin 5 (Droite - Arrière)
    r5 = arcade.rect.XYWH(650, 250, 15, 40)
    arcade.draw_rect_filled(r5, arcade.csscolor.BROWN)
    arcade.draw_polygon_filled([(620, 280), (695, 280), (657, 340)], arcade.color.LIME_GREEN)

    # Sapin 6 (Droite)
    r6 = arcade.rect.XYWH(730, 240, 22, 55)
    arcade.draw_rect_filled(r6, arcade.csscolor.BROWN)
    arcade.draw_polygon_filled([(690, 275), (790, 275), (741, 360)], arcade.color.LIME_GREEN)


def dessiner_texte():
    arcade.draw_text(
        "Parc National de Banff - Lac Louise",
        35,
        540,
        arcade.color.DARK_SLATE_GRAY,
        22,
        bold=True
    )


class FenetreDessin(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.LIGHT_CYAN)

    def on_draw(self):
        self.clear()
        dessiner_ciel_et_soleil()
        dessiner_montagnes_rocheuses()
        dessiner_lac_turquoise()
        dessiner_rive_et_foret()
        dessiner_texte()


def main():
    FenetreDessin(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()