from pyray import *  # type: ignore
from config import *
import imageio
import numpy as np

# --- Utility Functions ---


def parse_level(level):
    """
    Parses the level map, extracts all dynamic entities (coins, enemies),
    replaces their spawn points with air, and returns the modified collision map and entity lists.
    """
    coins = []
    enemies = []
    # Create a deep copy of the level to modify the tiles, leaving the original map intact
    new_level = [row[:] for row in level]

    for r in range(TILE_ROWS):
        for c in range(TILE_COLS):
            x = c * TILE_SIZE
            y = r * TILE_SIZE

            if new_level[r][c] == TILE_COIN:
                # Coin position is center
                coins.append((x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                new_level[r][c] = TILE_AIR

            elif new_level[r][c] == TILE_ENEMY:
                # Enemy position is top-left
                enemies.append(Enemy(x, y))
                new_level[r][c] = TILE_AIR

    return new_level, coins, enemies


# --- Game Object Classes ---


class Player:
    def __init__(self, x, y):
        # Store starting position for reset
        self.start_x = x
        self.start_y = y
        # Current position (top-left for collision)
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        # Physics
        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = False

    def get_rect(self):
        """Returns the player's collision bounding box (top-left, width, height)."""
        return (self.x, self.y, self.width, self.height)

    def update(self, delta_time, level):
        # 1. Handle Input (Horizontal Movement)
        self.vx = 0.0
        if is_key_down(KeyboardKey.KEY_LEFT) or is_key_down(KeyboardKey.KEY_A):
            self.vx = -PLAYER_SPEED
        if is_key_down(KeyboardKey.KEY_RIGHT) or is_key_down(KeyboardKey.KEY_D):
            self.vx = PLAYER_SPEED

        # --- Velocity Zeroing for Stability ---
        if self.is_grounded:
            self.vy = 0.0

        # 2. Handle Input (Jump)
        if (
            is_key_pressed(KeyboardKey.KEY_SPACE) or is_key_pressed(KeyboardKey.KEY_UP)
        ) and self.is_grounded:
            self.vy = JUMP_VELOCITY

        # 3. Apply Gravity
        self.vy += GRAVITY * delta_time
        if self.vy > 1000:
            self.vy = 1000

        # --- Reset grounded state at start of frame update ---
        self.is_grounded = False

        # 4. Apply Movement (Separated for X and Y collision checks)

        # Apply X movement
        self.x += self.vx * delta_time
        self.handle_tile_collision(level, "X")

        # Apply Y movement
        self.y += self.vy * delta_time
        self.handle_tile_collision(level, "Y")

        # --- Safety Clamp to World Bounds ---
        self.x = max(0, min(self.x, WORLD_WIDTH - self.width))

    def handle_tile_collision(self, level, axis):
        """Performs AABB collision checks against solid tiles and resolves the collision."""
        player_rect = self.get_rect()
        px, py, pw, ph = player_rect

        min_col = int(px / TILE_SIZE)
        max_col = int((px + pw) / TILE_SIZE)
        min_row = int(py / TILE_SIZE)
        max_row = int((py + ph) / TILE_SIZE)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):

                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue

                if level[row][col] == TILE_SOLID:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                    if check_collision_recs(player_rect, tile_rect):

                        if axis == "X":
                            if self.vx > 0:  # Moving Right
                                self.x = tile_rect[0] - self.width
                            elif self.vx < 0:  # Moving Left
                                self.x = tile_rect[0] + TILE_SIZE
                            self.vx = 0.0

                        elif axis == "Y":
                            if self.vy >= 0:  # Falling (Hitting Ground)
                                self.y = tile_rect[1] - self.height
                                self.is_grounded = True
                            elif self.vy < 0:  # Jumping (Hitting Ceiling)
                                self.y = tile_rect[1] + TILE_SIZE

                            self.vy = 0.0

                        player_rect = self.get_rect()
                        px, py, pw, ph = player_rect

    def check_collection(self, collectibles):
        """Checks for collision with coins and returns indices of collected coins."""
        collected_indices = []
        player_rect = self.get_rect()
        coin_collision_size = TILE_SIZE * 0.5

        for i, (cx, cy) in enumerate(collectibles):
            coin_x = cx - coin_collision_size / 2
            coin_y = cy - coin_collision_size / 2
            coin_rect = (coin_x, coin_y, coin_collision_size, coin_collision_size)

            if check_collision_recs(player_rect, coin_rect):
                collected_indices.append(i)

        return collected_indices

    def check_enemy_collision(self, enemies):
        """Checks for collision with enemies and determines outcome (stomp or death).
        Returns (hit_type, enemy_index) or (None, -1).
        hit_type: "STOMP" (safe kill) or "LETHAL" (death)
        """
        player_rect = self.get_rect()
        px, py, pw, ph = player_rect

        for i, enemy in enumerate(enemies):
            enemy_rect = enemy.get_rect()

            if check_collision_recs(player_rect, enemy_rect):

                # STOMP Condition:
                # 1. Player is falling (vy > 0)
                # 2. Player's bottom is above the enemy's mid-point (approximate stomping zone)
                is_stompable_zone = py + ph < enemy.y + enemy.height * 0.5

                if self.vy > 0 and is_stompable_zone:
                    return "STOMP", i
                else:
                    # Lethal collision (side, head, or missing the stomp zone)
                    return "LETHAL", i

        return None, -1

    def reset(self):
        """Resets the player to their starting position."""
        self.x = self.start_x
        self.y = self.start_y
        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = False

    def draw(self):
        """Draws the player at their world coordinates."""
        draw_rectangle(
            int(self.x), int(self.y), int(self.width), int(self.height), BLUE
        )
        if self.is_grounded:
            draw_rectangle_lines(
                int(self.x), int(self.y), int(self.width), int(self.height), WHITE
            )
        else:
            draw_rectangle_lines(
                int(self.x), int(self.y), int(self.width), int(self.height), GRAY
            )


class Enemy:
    def __init__(self, x, y):
        # Position (top-left for collision)
        self.x = x
        self.y = y
        self.width = TILE_SIZE * 0.7
        self.height = TILE_SIZE * 0.7

        # Physics/Movement
        self.vx = ENEMY_SPEED  # Start moving right
        self.vy = 0.0
        self.is_grounded = False

    def get_rect(self):
        """Returns the enemy's collision bounding box."""
        return (self.x, self.y, self.width, self.height)

    def update(self, delta_time, level):
        # 1. Apply Gravity
        if self.is_grounded:
            self.vy = 0.0
        self.vy += GRAVITY * delta_time
        self.is_grounded = False

        # 2. Apply Movement

        # Apply X movement
        self.x += self.vx * delta_time
        self.handle_tile_collision(level, "X")

        # Apply Y movement
        self.y += self.vy * delta_time
        self.handle_tile_collision(level, "Y")

    def handle_tile_collision(self, level, axis):
        """Enemy collision: reverses direction on horizontal wall contact, respects vertical floor contact."""
        enemy_rect = self.get_rect()
        px, py, pw, ph = enemy_rect

        min_col = int(px / TILE_SIZE)
        max_col = int((px + pw) / TILE_SIZE)
        min_row = int(py / TILE_SIZE)
        max_row = int((py + ph) / TILE_SIZE)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):

                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue

                if level[row][col] == TILE_SOLID:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

                    if check_collision_recs(enemy_rect, tile_rect):

                        if axis == "X":
                            # Reverses direction on horizontal collision
                            if self.vx > 0:
                                self.x = tile_rect[0] - self.width
                            elif self.vx < 0:
                                self.x = tile_rect[0] + TILE_SIZE
                            self.vx *= -1  # Reverse direction

                        elif axis == "Y":
                            if self.vy >= 0:  # Hitting Ground
                                self.y = tile_rect[1] - self.height
                                self.is_grounded = True

                            self.vy = 0.0

                        enemy_rect = self.get_rect()  # Update rect after resolution

    def draw(self):
        """Draws the enemy as a red rectangle with a directional indicator."""
        draw_rectangle(int(self.x), int(self.y), int(self.width), int(self.height), RED)
        draw_rectangle_lines(
            int(self.x), int(self.y), int(self.width), int(self.height), BLACK
        )

        # Draw a small indicator for direction
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        indicator_size = self.width * 0.2

        if self.vx > 0:  # Moving Right
            draw_triangle(
                Vector2(center_x + indicator_size, center_y),
                Vector2(center_x - indicator_size, center_y - indicator_size),
                Vector2(center_x - indicator_size, center_y + indicator_size),
                WHITE,
            )
        elif self.vx < 0:  # Moving Left
            draw_triangle(
                Vector2(center_x - indicator_size, center_y),
                Vector2(center_x + indicator_size, center_y - indicator_size),
                Vector2(center_x + indicator_size, center_y + indicator_size),
                WHITE,
            )


# --- Drawing and Camera Functions (Unchanged) ---


def draw_level(level):
    """Draws the solid tiles of the level map."""
    for row in range(TILE_ROWS):
        for col in range(TILE_COLS):
            tile_value = level[row][col]
            if tile_value == TILE_SOLID:
                x = col * TILE_SIZE
                y = row * TILE_SIZE

                draw_rectangle(x, y, TILE_SIZE, TILE_SIZE, DARKGRAY)
                draw_rectangle_lines(x, y, TILE_SIZE, TILE_SIZE, BLACK)


def coin_frame(frame) -> Rectangle:
    x = frame // SHINING_COIN_SPRITE_ROWS * SHINING_COIN_SPRITE_SIZE
    y = (
        frame % SHINING_COIN_SPRITE_COLS * SHINING_COIN_SPRITE_SIZE
        + SHINING_COIN_SPRITE_YT_OFFSET
    )

    return Rectangle(
        x,
        y,
        SHINING_COIN_SPRITE_SIZE,
        SHINING_COIN_SPRITE_SIZE,
    )


def draw_coins(coins, coin_texture, frame: int):
    """Draws the active coins as small yellow diamonds (polygons)."""
    for cx, cy in coins:
        draw_texture_pro(
            coin_texture,
            coin_frame(frame),
            Rectangle(cx - 20, cy - 20, 40, 40),
            Vector2(0, 0),
            0.0,
            WHITE,
        )


def update_camera(
    camera, player, world_width, world_height, screen_width, screen_height
):
    """Centers the camera on the player and clamps the camera's target to the world bounds."""

    camera.target.x = player.x + player.width / 2
    camera.target.y = player.y + player.height / 2

    min_x = screen_width / 2
    max_x = world_width - screen_width / 2

    if camera.target.x < min_x:
        camera.target.x = min_x
    if camera.target.x > max_x:
        camera.target.x = max_x

    min_y = screen_height / 2
    max_y = world_height - screen_height / 2

    if camera.target.y < min_y:
        camera.target.y = min_y
    if camera.target.y > max_y:
        camera.target.y = max_y

    camera.offset.x = screen_width / 2
    camera.offset.y = screen_height / 2


# --- Main Game Logic ---
def main():
    # --- Initialization ---
    init_window(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        "Raylib 2D Platformer Clone (Stomp Mechanic)",
    )
    set_target_fps(TARGET_FRAME)

    # Prepare Level Data: Separate collision map from dynamic entities
    game_level, collectibles, enemies = parse_level(LEVEL)

    # Game State Variables
    # Player starts at TILE_SIZE * 2, TILE_SIZE * 2
    player = Player(TILE_SIZE * 2, TILE_SIZE * 2)
    score = 0
    game_state = "PLAYING"

    # --- Camera Initialization ---
    camera = Camera2D()
    camera.target = Vector2(player.x, player.y)
    camera.offset = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    camera.rotation = 0.0
    camera.zoom = 1.0

    coin_texture = load_texture("./assets/shining_coin_sprite.png")
    duration_left = SHINING_COIN_SPRITE_DURATION
    cur = 0

    gif_recording = False
    gif_frame_counter = 0
    frames = []

    # --- Game Loop ---
    while not window_should_close():
        delta_time = get_frame_time()
        if delta_time > 1 / 30:
            delta_time = 1 / 30

        # record
        if is_key_down(KeyboardKey.KEY_LEFT_CONTROL) and is_key_pressed(
            KeyboardKey.KEY_R
        ):
            if gif_recording:
                gif_recording = False
                if frames:
                    imageio.mimsave("output.gif", frames, fps=GIF_SAVE_FPS)
                frames = []
            else:
                gif_recording = True
                gif_frame_counter = 0

        if gif_recording:
            gif_frame_counter += 1
            if gif_frame_counter >= GIF_CAPTURE_INTERVAL:
                im_screen = load_image_from_screen()
                size = im_screen.width * im_screen.height * 4
                buf = ffi.buffer(im_screen.data, size)
                frame_arr = (
                    np.frombuffer(buf, dtype=np.uint8)
                    .reshape((im_screen.height, im_screen.width, 4))
                    .copy()
                )
                frames.append(frame_arr)
                gif_frame_counter = 0
                unload_image(im_screen)

        # --- Update ---
        if game_state == "PLAYING":
            player.update(delta_time, game_level)

            # Update Enemies
            for enemy in enemies:
                enemy.update(delta_time, game_level)

            update_camera(
                camera, player, WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT
            )

            # Check for coin collection
            collected_indices = player.check_collection(collectibles)
            if collected_indices:
                for index in sorted(collected_indices, reverse=True):
                    collectibles.pop(index)
                    score += 10

            # Check for enemy collision (Stomp/Death/Reset)
            hit_type, enemy_index = player.check_enemy_collision(enemies)

            if hit_type == "STOMP":
                # Stomp mechanic: Remove enemy, score, and bounce
                enemies.pop(enemy_index)
                score += 100
                player.vy = STOMP_BOUNCE  # Player bounces up

            elif hit_type == "LETHAL":
                # Death/Reset mechanic: Penalty and restart
                player.reset()
                score -= 50
                if score < 0:
                    score = 0

        # --- Draw ---
        begin_drawing()
        clear_background(SKYBLUE)

        # Start the 2D camera mode
        begin_mode_2d(camera)

        # 1. Draw the Level
        draw_level(game_level)

        # 2. Draw Collectibles
        duration_left -= delta_time

        if duration_left <= 0:
            # print(cur, type)
            duration_left = SHINING_COIN_SPRITE_DURATION
            cur += 1  # step
            cur = cur % (SHINING_COIN_SPRITE_ROWS * SHINING_COIN_SPRITE_COLS)

        draw_coins(collectibles, coin_texture, cur)

        # 3. Draw Enemies
        for enemy in enemies:
            enemy.draw()

        # 4. Draw Player
        player.draw()

        # End the 2D camera mode
        end_mode_2d()

        # 5. Draw HUD (Drawn on screen, outside of BeginMode2D)
        score_text = f"Score: {score}"
        draw_text(
            score_text, SCREEN_WIDTH - measure_text(score_text, 20) - 10, 10, 20, BLACK
        )

        debug_text = f"Grounded: {player.is_grounded} | Enemies: {len(enemies)}"
        draw_text(debug_text, 10, 10, 20, BLACK)

        end_drawing()

    # --- De-Initialization ---
    close_window()


if __name__ == "__main__":
    main()
