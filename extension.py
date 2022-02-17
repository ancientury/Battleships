import arcade
import arcade.gui
from battleships import Fleet

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Battleships game for PoP I Project by Abdurahman Baalache"

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 50
HEIGHT = 50

# This sets the margin between each cell
MARGIN = 10


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # background
        self.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")

        # sprite lists
        self.gui_list = arcade.SpriteList()
        self.grid_sprite_list = arcade.SpriteList()

        self.banner_sprite = arcade.Sprite("sprites/banner.png", 0.7)
        self.banner_sprite.center_x = 400
        self.banner_sprite.center_y = 720
        self.gui_list.append(self.banner_sprite)

        # set up the grid
        self.grid_xy = (0, 0)
        self.grid = []  # 10x10 grid
        for row in range(10):
            self.grid.append([])
            for column in range(10):
                self.grid[row].append(0)

        # fill the grid box with default unknown sprite
        for row in range(10):
            for column in range(10):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN) + 100
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 80
                sprite = arcade.Sprite("sprites/button_unknown.png", 1, 0, 0, WIDTH, HEIGHT)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)

        # set up battleship game object
        self.current_fleet = Fleet()

    # updates the grid box with conditional sprites e.g. ship is hit, missed or unknown sprites
    def resync_grid_with_sprites(self):
        for row in range(10):
            for column in range(10):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN) + 100
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 80
                pos = row * 10 + column

                if (row, column) in self.current_fleet.ships:
                    location = (row, column)
                    ship = self.current_fleet.ships[location]

                    sprite = arcade.Sprite("sprites/button_unknown.png", 1, 0, 0, WIDTH, HEIGHT)

                    if ship.is_sunk():
                        sprite = arcade.Sprite("sprites/ships/button_" + ship.ship_type + ".png", 1, 0, 0, WIDTH,
                                               HEIGHT)
                    elif (row, column) in ship.hits:
                        sprite = arcade.Sprite("sprites/button_hit.png", 1, 0, 0, WIDTH, HEIGHT)

                    sprite.center_x = x
                    sprite.center_y = y

                    self.grid_sprite_list[pos] = sprite
                else:
                    if (row, column) in self.current_fleet.hit_locations:
                        sprite = arcade.Sprite("sprites/button_missed.png", 1, 0, 0, WIDTH, HEIGHT)

                        sprite.center_x = x
                        sprite.center_y = y

                        self.grid_sprite_list[pos] = sprite

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()

        # draw background
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        # draw grid box and headers
        self.grid_sprite_list.draw()
        c_header = False
        for row in range(10):
            y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 60
            arcade.draw_text(f"{row}", 80, y, arcade.color.WHITE, 22)
            for column in range(10):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN) + 90
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 20
                if not c_header:
                    arcade.draw_text(f"{column}", x, y, arcade.color.WHITE, 22)
            c_header = True

        # grid coordinates
        arcade.draw_text(f"Coordinates: {self.grid_xy}", 10, SCREEN_HEIGHT - 40, arcade.color.AQUAMARINE, 16)

        # game status text
        arcade.draw_text(f"{self.current_fleet.game_status}",
                         SCREEN_WIDTH / 2, 30, arcade.color.AQUA, 25, width=SCREEN_WIDTH, align="center",
                         anchor_x="center", anchor_y="center")

        # score text
        arcade.draw_text(f"Score: {self.current_fleet.sunk_ships}", 10, 10, arcade.color.WHITE, 18)

        # credit text
        arcade.draw_text(f"Written by Abdurahman Baalache", SCREEN_WIDTH - 190, 5, arcade.color.ASH_GREY, 11)

        # draw gui elements
        self.gui_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # change the x/y screen coordinates to grid coordinates
        column = int((x - 100) // (WIDTH + MARGIN))
        row = int((y - 80) // (HEIGHT + MARGIN))

        if row in range(0, 10) and column in range(0, 10):
            self.grid_xy = (column, row)  # update coordinates for reference

    def on_mouse_press(self, x, y, button, modifiers):
        # change the x/y screen coordinates to grid coordinates
        column = int((x - 100) // (WIDTH + MARGIN))
        row = int((y - 80) // (HEIGHT + MARGIN))

        if row in range(0, 10) and column in range(0, 10):
            if not self.current_fleet.game_over:  # check if game is over before shooting
                self.current_fleet.shots += 1
                self.current_fleet.check_if_hits(row, column)

        # update changes on the grid
        self.resync_grid_with_sprites()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
