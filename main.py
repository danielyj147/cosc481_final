from game import Game
from pyray import *  # pyright: ignore[reportWildcardImportFromLibrary]
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS, TITLE

game = Game()

if __name__ == "__main__":
    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    set_target_fps(TARGET_FPS)
    init_audio_device()

    game.load_textures()
    game.load_audio()

    while not window_should_close():
        game.update()

        begin_drawing()
        clear_background(Color(10, 10, 30, 255))
        game.draw()
        end_drawing()

    game.shutdown()
    close_audio_device()
    close_window()
