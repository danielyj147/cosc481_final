import math
import os
from enum import Enum
import random
from pyray import *  # pyright: ignore[reportWildcardImportFromLibrary]
from config import *  # noqa: F403

# Enables VS Code execute button
ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# Collision box for the professor. Smaller than the sprite so he doesn't
# look like he's hovering next to walls.
PLAYER_HALF_W = 12
PLAYER_HALF_H = 14


class GameScreen(Enum):
    START = 0
    PLAYING = 1
    PAUSED = 2
    COMPLETE = 3


class SoundType(Enum):
    HOOK_SHOOT = "hook_shoot"
    HOOK_ATTACH = "hook_attach"
    REEL = "reel"
    WHOOSH = "whoosh"
    THUD = "thud"


class MusicType(Enum):
    BACKGROUND = "background"


# Asset paths
SOUNDS: dict[SoundType, str] = {
    SoundType.HOOK_SHOOT: os.path.join(ASSET_DIR, "sound", "grappling_hook.mp3"),
    SoundType.HOOK_ATTACH: os.path.join(ASSET_DIR, "sound", "metal_clank.mp3"),
    SoundType.REEL: os.path.join(ASSET_DIR, "sound", "rope_under_tension.wav"),
    SoundType.WHOOSH: os.path.join(ASSET_DIR, "sound", "whoosh.mp3"),
    SoundType.THUD: os.path.join(ASSET_DIR, "sound", "thud.mp3"),
}

MUSICS: dict[MusicType, str] = {
    MusicType.BACKGROUND: os.path.join(ASSET_DIR, "sound", "bgm_1.mp3"),
}

game_sounds: dict[SoundType, Sound] = {}
game_musics: dict[MusicType, Music] = {}


def collide_walls(pos_x, pos_y, vel_x, vel_y, level):
    """AABB tile collision. Pushes the player out of any wall they overlap.

    Two passes because resolving one overlap can nudge you into another
    (corners). One pass works 99% of the time but that 1% is really annoying.
    """
    on_ground = False
    hw = PLAYER_HALF_W
    hh = PLAYER_HALF_H

    for _pass in range(2):
        col_left = int((pos_x - hw) // TILE_SIZE)
        col_right = int((pos_x + hw) // TILE_SIZE)
        row_top = int((pos_y - hh) // TILE_SIZE)
        row_bot = int((pos_y + hh) // TILE_SIZE)

        for r in range(row_top, row_bot + 1):
            for c in range(col_left, col_right + 1):
                if level.is_solid(c, r):
                    tile_x = c * TILE_SIZE
                    tile_y = r * TILE_SIZE

                    # overlap from each direction
                    ol = (pos_x + hw) - tile_x  # player's right vs tile's left
                    orr = (tile_x + TILE_SIZE) - (
                        pos_x - hw
                    )  # tile's right vs player's left
                    ot = (pos_y + hh) - tile_y  # player's bottom vs tile's top
                    ob = (tile_y + TILE_SIZE) - (
                        pos_y - hh
                    )  # tile's bottom vs player's top

                    if ol > 0 and orr > 0 and ot > 0 and ob > 0:
                        m = min(ol, orr, ot, ob)
                        if m == ol:
                            pos_x = tile_x - hw
                            vel_x = 0
                        elif m == orr:
                            pos_x = tile_x + TILE_SIZE + hw
                            vel_x = 0
                        elif m == ot:
                            pos_y = tile_y - hh
                            vel_y = 0
                            on_ground = True
                        elif m == ob:
                            pos_y = tile_y + TILE_SIZE + hh
                            vel_y = 0

    return pos_x, pos_y, vel_x, vel_y, on_ground


class Level:
    def __init__(self, tilemap) -> None:
        self.tilemap = tilemap
        self.rows = len(tilemap)
        self.cols = len(tilemap[0])
        self.world_width = self.cols * TILE_SIZE
        self.world_height = self.rows * TILE_SIZE
        self.brick_texture: Texture | None = None

    def load_texture(self, brick_texture) -> None:
        self.brick_texture = brick_texture

    def draw(self) -> None:
        if self.brick_texture is None:
            return
        for r in range(self.rows):
            for c in range(self.cols):
                tile = self.tilemap[r][c]
                x = c * TILE_SIZE
                y = r * TILE_SIZE

                if tile == TILE_WALL:
                    # alpha-mask
                    draw_rectangle(x, y, TILE_SIZE, TILE_SIZE, Color(25, 45, 35, 255))
                    tile_index = (c + r) % BRICK_TILE_COUNT
                    src = Rectangle(tile_index * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
                    dst = Rectangle(x, y, TILE_SIZE, TILE_SIZE)
                    draw_texture_pro(
                        self.brick_texture, src, dst, Vector2(0, 0), 0.0, WHITE
                    )

                elif tile == TILE_REFLECT:
                    draw_rectangle(x, y, TILE_SIZE, TILE_SIZE, Color(*REFLECT_COLOR))
                    # 1px highlight on top/left, shadow on bottom/right (bevel)
                    draw_rectangle(x, y, TILE_SIZE, 2, Color(*REFLECT_HIGHLIGHT))
                    draw_rectangle(x, y, 2, TILE_SIZE, Color(*REFLECT_HIGHLIGHT))
                    draw_rectangle(
                        x, y + TILE_SIZE - 2, TILE_SIZE, 2, Color(*REFLECT_SHADOW)
                    )
                    draw_rectangle(
                        x + TILE_SIZE - 2, y, 2, TILE_SIZE, Color(*REFLECT_SHADOW)
                    )

                elif tile == TILE_ANCHOR:
                    cx = x + TILE_SIZE // 2
                    cy = y + TILE_SIZE // 2
                    draw_circle(cx, cy, ANCHOR_RADIUS, Color(*ANCHOR_COLOR))
                    draw_circle_lines(
                        cx, cy, ANCHOR_RADIUS + 1, Color(120, 110, 80, 255)
                    )

                elif tile == TILE_ENTRANCE:
                    # the glow: level 1 exit / level 2 enterance
                    cx_t = x + TILE_SIZE // 2
                    cy_t = y + TILE_SIZE // 2
                    draw_circle(cx_t, cy_t, 30, Color(255, 245, 220, 30))
                    draw_circle(cx_t, cy_t, 24, Color(255, 245, 220, 70))
                    draw_circle(cx_t, cy_t, 20, Color(255, 245, 220, 110))

    def _in_bounds(self, col, row) -> bool:
        return 0 <= col < self.cols and 0 <= row < self.rows

    def is_wall(self, col, row) -> bool:
        if not self._in_bounds(col, row):
            return True
        return self.tilemap[row][col] == TILE_WALL

    def is_reflect(self, col, row) -> bool:
        if not self._in_bounds(col, row):
            return False
        return self.tilemap[row][col] == TILE_REFLECT

    def is_solid(self, col, row) -> bool:
        if not self._in_bounds(col, row):
            return True
        return self.tilemap[row][col] in (TILE_WALL, TILE_REFLECT)

    def is_hookable(self, col, row) -> bool:
        if not self._in_bounds(col, row):
            return False
        return self.tilemap[row][col] == TILE_ANCHOR

    def get_spawn(self) -> tuple[float, float]:
        for r in range(self.rows):
            for c in range(self.cols):
                if self.tilemap[r][c] == TILE_SPAWN:
                    return (
                        c * TILE_SIZE + TILE_SIZE // 2,
                        r * TILE_SIZE + TILE_SIZE // 2,
                    )
        return (self.world_width // 2, self.world_height - TILE_SIZE * 2)


class GameCamera:
    """Camera that follows the player with lerp smoothing. Without the lerp
    the camera snaps to the player and it feels like a security cam."""

    def __init__(self, world_width, world_height) -> None:
        self.camera = Camera2D()
        self.camera.zoom = 1.0
        self.world_width = world_width
        self.world_height = world_height

    def setup(self, target_x, target_y) -> None:
        self.camera.target = Vector2(target_x, target_y)
        self.camera.offset = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def update(self, target_x, target_y) -> None:
        goal_x = target_x
        goal_y = target_y

        min_x = SCREEN_WIDTH / 2
        max_x = self.world_width - SCREEN_WIDTH / 2
        min_y = SCREEN_HEIGHT / 2
        max_y = self.world_height - SCREEN_HEIGHT / 2

        if max_x > min_x:
            goal_x = max(min_x, min(goal_x, max_x))
        else:
            goal_x = self.world_width / 2
        if max_y > min_y:
            goal_y = max(min_y, min(goal_y, max_y))
        else:
            goal_y = self.world_height / 2

        self.camera.target.x += (goal_x - self.camera.target.x) * CAMERA_LERP
        self.camera.target.y += (goal_y - self.camera.target.y) * CAMERA_LERP

    def begin(self) -> None:
        begin_mode_2d(self.camera)

    def end(self) -> None:
        end_mode_2d()


class Player:
    def __init__(self) -> None:
        self.pos_x: float = 0.0
        self.pos_y: float = 0.0
        self.vel_x: float = 0.0
        self.vel_y: float = 0.0
        self.facing_right: bool = True
        self.on_ground: bool = False
        self.sprite_texture: Texture | None = None
        self.anim_row: int = ANIM_IDLE
        self.anim_frame: int = 0
        self.anim_timer: float = 0.0

    def setup(self, spawn_x, spawn_y) -> None:
        self.pos_x = spawn_x
        self.pos_y = spawn_y
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.on_ground = False

    def load_texture(self, texture) -> None:
        self.sprite_texture = texture

    def update(self, dt, level, hooked, dev_fly=False) -> None:
        # When not hooked, the professor is just a falling object.
        if not hooked:
            if dev_fly:
                # Inspired by Edgar's dev mode / GOD mode
                speed = 320.0
                self.vel_x = 0.0
                self.vel_y = 0.0
                if is_key_down(KeyboardKey.KEY_A) or is_key_down(KeyboardKey.KEY_LEFT):
                    self.vel_x = -speed
                if is_key_down(KeyboardKey.KEY_D) or is_key_down(KeyboardKey.KEY_RIGHT):
                    self.vel_x = speed
                if is_key_down(KeyboardKey.KEY_W) or is_key_down(KeyboardKey.KEY_UP):
                    self.vel_y = -speed
                if is_key_down(KeyboardKey.KEY_S) or is_key_down(KeyboardKey.KEY_DOWN):
                    self.vel_y = speed
                if self.vel_x > 0:
                    self.facing_right = True
                elif self.vel_x < 0:
                    self.facing_right = False
                self.pos_x += self.vel_x * dt
                self.pos_y += self.vel_y * dt
                self.on_ground = False
            else:
                self.vel_y += GRAVITY * dt
                if self.vel_y > 1200:
                    self.vel_y = 1200

                # Without this the professor slides forever
                if self.on_ground:
                    self.vel_x *= 0.85

                self.pos_x += self.vel_x * dt
                self.pos_y += self.vel_y * dt

                self.on_ground = False
                self.pos_x, self.pos_y, self.vel_x, self.vel_y, self.on_ground = (
                    collide_walls(self.pos_x, self.pos_y, self.vel_x, self.vel_y, level)
                )

                if self.on_ground and abs(self.vel_x) < 5:
                    self.vel_x = 0

        self.anim_timer += dt
        if self.anim_timer >= 1.0 / ANIM_FPS:
            self.anim_timer -= 1.0 / ANIM_FPS
            self.anim_frame = (self.anim_frame + 1) % SPRITE_COLS

    def draw(self) -> None:
        if self.sprite_texture is None:
            return
        src_x = self.anim_frame * SPRITE_FRAME_W
        src_y = self.anim_row * SPRITE_FRAME_H
        # Negative width = horizontal flip
        w = SPRITE_FRAME_W if self.facing_right else -SPRITE_FRAME_W
        src = Rectangle(src_x, src_y, w, SPRITE_FRAME_H)
        dst = Rectangle(
            self.pos_x - PLAYER_DRAW_W // 2,
            self.pos_y - PLAYER_DRAW_H // 2,
            PLAYER_DRAW_W,
            PLAYER_DRAW_H,
        )
        draw_texture_pro(self.sprite_texture, src, dst, Vector2(0, 0), 0.0, WHITE)


class Hook:
    """
    Same idea as how objects slide along walls, but the "wall" is a circle.

    The swing physics use position-based constraint projection, not angular math.
    Basically lets the player move freely, then if they're too far from the anchor,
    snap them back to the edge of a circle (the rope length) and remove the velocity
    that was pulling them outward. What's left is tangential velocity = swinging.

    For more: https://code.tutsplus.com/swinging-physics-for-player-movement-as-seen-in-spider-man-2-and-energy-hook--gamedev-8782t
    """

    STATE_IDLE = 0  # not doing anything, waiting for left click
    STATE_FLYING = 1  # hook is in the air traveling toward the cursor
    STATE_ATTACHED = 2  # hooked onto an anchor, player swings as a pendulum

    def __init__(self) -> None:
        self.state: int = Hook.STATE_IDLE
        self.pos_x: float = 0.0
        self.pos_y: float = 0.0
        self.vel_x: float = 0.0
        self.vel_y: float = 0.0
        self.anchor_x: float = 0.0
        self.anchor_y: float = 0.0
        self.rope_length: float = 0.0
        self.origin_x: float = 0.0
        self.origin_y: float = 0.0

    def setup(self) -> None:
        self.state = Hook.STATE_IDLE

    def shoot(self, origin_x, origin_y, target_x, target_y) -> None:
        # Direction from player to mouse, normalized to unit vector
        dx = target_x - origin_x
        dy = target_y - origin_y
        dist = math.sqrt(dx * dx + dy * dy)

        dx /= dist
        dy /= dist
        self.pos_x = origin_x
        self.pos_y = origin_y
        self.vel_x = dx * HOOK_SHOOT_SPEED
        self.vel_y = dy * HOOK_SHOOT_SPEED
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.state = Hook.STATE_FLYING

    def release(self) -> None:
        self.state = Hook.STATE_IDLE

    def update(self, dt, level, player) -> None:
        if self.state == Hook.STATE_FLYING:
            self._update_flying(dt, level, player)
        elif self.state == Hook.STATE_ATTACHED:
            self._update_attached(dt, level, player)

    def _update_flying(self, dt, level, player) -> None:
        prev_x = self.pos_x
        prev_y = self.pos_y
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt

        # Rope has a max length. No infinite grapples.
        traveled_x = self.pos_x - self.origin_x
        traveled_y = self.pos_y - self.origin_y
        if math.sqrt(traveled_x**2 + traveled_y**2) > HOOK_MAX_RANGE:
            self.state = Hook.STATE_IDLE
            return

        col = int(self.pos_x // TILE_SIZE)
        row = int(self.pos_y // TILE_SIZE)

        if level.is_hookable(col, row):
            # Snap anchor to tile center. Without this, it looks very crooked.
            self.anchor_x = col * TILE_SIZE + TILE_SIZE // 2
            self.anchor_y = row * TILE_SIZE + TILE_SIZE // 2
            # Initial rope length = current distance from player to anchor
            dx = player.pos_x - self.anchor_x
            dy = player.pos_y - self.anchor_y
            self.rope_length = math.sqrt(dx * dx + dy * dy)
            self.state = Hook.STATE_ATTACHED
            return

        # Reflective surface
        if level.is_reflect(col, row):
            prev_col = int(prev_x // TILE_SIZE)
            prev_row = int(prev_y // TILE_SIZE)
            crossed_x = prev_col != col
            crossed_y = prev_row != row
            if crossed_x and crossed_y:
                tile_x = col * TILE_SIZE
                tile_y = row * TILE_SIZE
                pen_x = (
                    self.pos_x - tile_x
                    if self.vel_x > 0
                    else tile_x + TILE_SIZE - self.pos_x
                )
                pen_y = (
                    self.pos_y - tile_y
                    if self.vel_y > 0
                    else tile_y + TILE_SIZE - self.pos_y
                )
                if pen_x < pen_y:
                    self.vel_x = -self.vel_x
                else:
                    self.vel_y = -self.vel_y
            elif crossed_x:
                self.vel_x = -self.vel_x
            elif crossed_y:
                self.vel_y = -self.vel_y
            self.pos_x = prev_x
            self.pos_y = prev_y
            return

        # Hit a wall = hook drops.
        if level.is_wall(col, row):
            self.state = Hook.STATE_IDLE

    def _update_attached(self, dt, level, player) -> None:
        """
        Order:
        1. Adjust rope length (W/S)
        2. Apply gravity + player swing input (A/D)
        3. "Dampen" velocity so swings don't go forever(basically ball gravity)
        4. Move player to new position
        5. If new position is outside the rope circle, move back in
           and remove the radial velocity (the part pulling away from anchor).
           What remains is tangential velocity = the actual swing.
        6. Check wall collisions so you don't swing through bricks
        """
        # W/S: reel in / let out rope
        if is_key_down(KeyboardKey.KEY_W) or is_key_down(KeyboardKey.KEY_UP):
            self.rope_length -= REEL_SPEED * dt
            if self.rope_length < ROPE_MIN_LENGTH:
                self.rope_length = ROPE_MIN_LENGTH
        if is_key_down(KeyboardKey.KEY_S) or is_key_down(KeyboardKey.KEY_DOWN):
            self.rope_length += REEL_SPEED * dt
            if self.rope_length > HOOK_MAX_RANGE:
                self.rope_length = HOOK_MAX_RANGE

        # Gravity still applies while hooked
        player.vel_y += GRAVITY * dt

        # A/D: pump the swing.
        swing_input = 0.0
        if is_key_down(KeyboardKey.KEY_A) or is_key_down(KeyboardKey.KEY_LEFT):
            swing_input -= 1.0
        if is_key_down(KeyboardKey.KEY_D) or is_key_down(KeyboardKey.KEY_RIGHT):
            swing_input += 1.0
        player.vel_x += SWING_FORCE * swing_input * dt

        # Damping: without this, swings build up energy and go crazy
        player.vel_x *= SWING_DAMPING
        player.vel_y *= SWING_DAMPING

        # new position (before constraint)
        new_x = player.pos_x + player.vel_x * dt
        new_y = player.pos_y + player.vel_y * dt

        # !!! The constraint
        # If the player drifted beyond rope_length from the anchor,
        # pull them back onto the circle edge.
        diff_x = new_x - self.anchor_x
        diff_y = new_y - self.anchor_y
        dist = math.sqrt(diff_x * diff_x + diff_y * diff_y)

        if dist > self.rope_length and dist > 0:
            # Project position back onto the rope circle
            scale = self.rope_length / dist
            new_x = self.anchor_x + diff_x * scale
            new_y = self.anchor_y + diff_y * scale

            # Velocity decomposition: split into radial (along rope) and
            # tangential (perpendicular to rope). Kill the radial part if
            # it's pulling outward. The tangential part IS the swing.
            norm_x = diff_x / dist
            norm_y = diff_y / dist
            radial = player.vel_x * norm_x + player.vel_y * norm_y
            if radial > 0:  # only kill outward, not inward (reeling)
                player.vel_x -= radial * norm_x
                player.vel_y -= radial * norm_y

        # Still need wall collision
        new_x, new_y, player.vel_x, player.vel_y, _ = collide_walls(
            new_x, new_y, player.vel_x, player.vel_y, level
        )

        player.pos_x = new_x
        player.pos_y = new_y

        if player.vel_x > 0:
            player.facing_right = True
        elif player.vel_x < 0:
            player.facing_right = False

    def draw(self, player) -> None:
        if self.state == Hook.STATE_FLYING:
            draw_line_ex(
                Vector2(player.pos_x, player.pos_y),
                Vector2(self.pos_x, self.pos_y),
                ROPE_THICKNESS,
                Color(*ROPE_COLOR),
            )
            draw_circle(int(self.pos_x), int(self.pos_y), 4, Color(200, 200, 200, 255))

        elif self.state == Hook.STATE_ATTACHED:
            draw_line_ex(
                Vector2(player.pos_x, player.pos_y),
                Vector2(self.anchor_x, self.anchor_y),
                ROPE_THICKNESS,
                Color(*ROPE_COLOR),
            )
            draw_circle(
                int(self.anchor_x), int(self.anchor_y), 5, Color(200, 200, 200, 255)
            )


class Fog:
    """Fog overlay drawn screen-space. Texture uses MIRROR_REPEAT wrap so we
    can scroll the source rect indefinitely without a visible seam — raylib
    flips the sample direction at the boundary, so edge values always match.
    """

    def __init__(self) -> None:
        self.texture: Texture | None = None
        self.scroll_x: float = 0.0

    def load_texture(self, fog_texture) -> None:
        self.texture = fog_texture

    def update(self, dt) -> None:
        self.scroll_x += FOG_SCROLL_SPEED * dt
        if self.texture:
            cycle = self.texture.width * 2  # mirror cycle
            if self.scroll_x >= cycle:
                self.scroll_x -= cycle

    def draw(self) -> None:
        if not self.texture:
            return
        th = self.texture.height
        tint = Color(255, 255, 255, FOG_ALPHA)
        src = Rectangle(self.scroll_x, 0, SCREEN_WIDTH, th)
        dst = Rectangle(0, SCREEN_HEIGHT - th, SCREEN_WIDTH, th)
        draw_texture_pro(self.texture, src, dst, Vector2(0, 0), 0.0, tint)


class Game:
    def __init__(self) -> None:
        self.screen: GameScreen = GameScreen.START
        self.debug: bool = False

        self.current_level: int = 0
        self.level: Level = Level(LEVELS[self.current_level])
        self.cam: GameCamera = GameCamera(
            self.level.world_width, self.level.world_height
        )
        self.player: Player = Player()
        self.hook: Hook = Hook()
        self.fog: Fog = Fog()

        self.spawn: tuple[float, float] = self.level.get_spawn()

        # Textures (loaded after window init)
        self.brick_texture: Texture | None = None
        self.char_texture: Texture | None = None
        self.fog_texture: Texture | None = None

        # Background
        self.stars = []

        # Escape anchor
        self.escape_anchor: Vector2 | None = None

    def startup(self) -> None:
        self.screen = GameScreen.PLAYING
        self.player.setup(self.spawn[0], self.spawn[1])
        self.hook.setup()
        self.cam.setup(self.spawn[0], self.spawn[1])
        self.stars = [
            (
                Vector2(
                    random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
                ),
                random.randint(0, 2),  # radius
                random.randint(80, 255),  # base alpha
                random.uniform(0, math.tau),  # phase
                random.uniform(1.5, 3.5),  # twinkle speed
            )
            for _ in range(100)
        ]
        play_music_stream(game_musics[MusicType.BACKGROUND])

    def _load_level(self, idx: int) -> None:
        if idx < 0 or idx >= len(LEVELS):
            return
        self.current_level = idx
        self.level = Level(LEVELS[idx])
        self.level.load_texture(self.brick_texture)
        self.cam = GameCamera(self.level.world_width, self.level.world_height)
        self.spawn = self.level.get_spawn()
        self.player.setup(self.spawn[0], self.spawn[1])
        self.hook.setup()
        self.cam.setup(self.spawn[0], self.spawn[1])
        if idx == 1:  # dome & escape anchor for level 2
            cx = self.level.world_width // 2
            base_y = self._dome_base_y()
            band_h = 6
            radius = self.level.world_width // 2
            self.escape_anchor = Vector2(cx, base_y - band_h - radius - 14)
        else:
            self.escape_anchor = None
        self.screen = GameScreen.PLAYING

    def load_textures(self) -> None:
        brick_img = load_image(
            os.path.join(ASSET_DIR, "img", "brown_bricks_sprite.png")
        )
        # alpha masking to make bricks green
        image_format(brick_img, PixelFormat.PIXELFORMAT_UNCOMPRESSED_GRAYSCALE)
        green_img = gen_image_color(
            brick_img.width, brick_img.height, Color(*BRICK_COLOR)
        )
        image_alpha_mask(green_img, brick_img)
        self.brick_texture = load_texture_from_image(green_img)
        unload_image(brick_img)
        unload_image(green_img)

        self.char_texture = load_texture(
            os.path.join(ASSET_DIR, "img", "character_sprite.png")
        )

        # generate fog
        # Resource Provided by Professor Elodie: https://www.raylib.com/examples/textures/loader.html?name=textures_image_generation
        fog_w = SCREEN_WIDTH * 2
        fog_h = SCREEN_HEIGHT
        mask = gen_image_color(fog_w, fog_h, Color(120, 120, 120, 255))
        noise_img = gen_image_perlin_noise(fog_w, fog_h, 0, 0, 4)
        image_alpha_mask(noise_img, mask)
        self.fog_texture = load_texture_from_image(noise_img)
        unload_image(noise_img)
        set_texture_wrap(self.fog_texture, TextureWrap.TEXTURE_WRAP_MIRROR_REPEAT)

        self.level.load_texture(self.brick_texture)
        self.player.load_texture(self.char_texture)
        self.fog.load_texture(self.fog_texture)

    def load_audio(self) -> None:
        for sound_type, path in SOUNDS.items():
            game_sounds[sound_type] = load_sound(path)
        for music_type, path in MUSICS.items():
            game_musics[music_type] = load_music_stream(path)

    def update(self) -> None:
        dt = get_frame_time()
        if dt > 1.0 / 30:
            dt = 1.0 / 30

        update_music_stream(game_musics[MusicType.BACKGROUND])
        self.fog.update(dt)

        if self.screen == GameScreen.START:
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                self.startup()
            return

        # Level switching (1 = L1, 2 = L2). Available in any post-start state.
        if is_key_pressed(KeyboardKey.KEY_ONE):
            self._load_level(0)
            return
        if is_key_pressed(KeyboardKey.KEY_TWO):
            self._load_level(1)
            return

        if self.screen == GameScreen.PAUSED:
            if is_key_pressed(KeyboardKey.KEY_P):
                self.screen = GameScreen.PLAYING
            return

        if self.screen == GameScreen.COMPLETE:
            if is_key_pressed(KeyboardKey.KEY_R):
                self._load_level(0)
                self.screen = GameScreen.START
            return

        # Play
        if is_key_pressed(KeyboardKey.KEY_P):
            self.screen = GameScreen.PAUSED
            return

        if is_key_pressed(KeyboardKey.KEY_E):
            self.debug = not self.debug

        self._handle_hook_input()

        prev_vel_y = self.player.vel_y
        prev_hook_state = self.hook.state
        hooked = self.hook.state == Hook.STATE_ATTACHED

        self.hook.update(dt, self.level, self.player)
        self._check_escape_attach()
        self.player.update(dt, self.level, hooked, dev_fly=self.debug)

        self._handle_sfx(prev_hook_state, prev_vel_y)

        self.cam.update(self.player.pos_x, self.player.pos_y)

        if self._check_level_complete():
            if self.current_level + 1 < len(LEVELS):
                self._load_level(self.current_level + 1)
            else:
                self.screen = GameScreen.COMPLETE

    def _handle_hook_input(self) -> None:
        # Left click shoots when idle, releases when attached.
        # On release, the player keeps their current velocity, this is the
        # "launch" that makes the game feel like Getting Over It.
        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
            if self.hook.state == Hook.STATE_IDLE:
                world_mouse = get_screen_to_world_2d(
                    get_mouse_position(), self.cam.camera
                )
                self.hook.shoot(
                    self.player.pos_x, self.player.pos_y, world_mouse.x, world_mouse.y
                )
                play_sound(game_sounds[SoundType.HOOK_SHOOT])
            elif self.hook.state == Hook.STATE_ATTACHED:
                self.hook.release()
                if abs(self.player.vel_y) > FALL_SPEED_THRESHOLD:
                    play_sound(game_sounds[SoundType.WHOOSH])

    def _handle_sfx(self, prev_hook_state, prev_vel_y) -> None:
        # Hook just attached
        if (
            prev_hook_state == Hook.STATE_FLYING
            and self.hook.state == Hook.STATE_ATTACHED
        ):
            play_sound(game_sounds[SoundType.HOOK_ATTACH])

        # Rope tension while actively using the rope
        ROPE_KEYS = [
            KeyboardKey.KEY_W,
            KeyboardKey.KEY_UP,
            KeyboardKey.KEY_S,
            KeyboardKey.KEY_DOWN,
            KeyboardKey.KEY_A,
            KeyboardKey.KEY_LEFT,
            KeyboardKey.KEY_D,
            KeyboardKey.KEY_RIGHT,
        ]
        using_rope = self.hook.state == Hook.STATE_ATTACHED and any(
            is_key_down(k) for k in ROPE_KEYS
        )
        rope_sound = game_sounds[SoundType.REEL]
        if using_rope and not is_sound_playing(rope_sound):
            play_sound(rope_sound)
        elif not using_rope and is_sound_playing(rope_sound):
            stop_sound(rope_sound)

        # Landed hard TODO: exclude pivot. exclude side wall?
        if self.player.on_ground and prev_vel_y > FALL_SPEED_THRESHOLD:
            play_sound(game_sounds[SoundType.THUD])

    def _check_escape_attach(self) -> None:
        a = self.escape_anchor
        if a is None or self.hook.state != Hook.STATE_FLYING:
            return
        dx = self.hook.pos_x - a.x
        dy = self.hook.pos_y - a.y
        if dx * dx + dy * dy >= 16 * 16:  # checking distnace
            return
        pdx = self.player.pos_x - a.x
        pdy = self.player.pos_y - a.y
        self.hook.anchor_x, self.hook.anchor_y = a.x, a.y
        self.hook.rope_length = math.sqrt(pdx * pdx + pdy * pdy)
        self.hook.state = Hook.STATE_ATTACHED

    def _check_level_complete(self) -> bool:
        col = int(self.player.pos_x // TILE_SIZE)
        row = int(self.player.pos_y // TILE_SIZE)
        if self.level.tilemap[row][col] == TILE_ENTRANCE:
            return True
        return False

    def draw(self) -> None:
        if self.screen == GameScreen.START:
            self._draw_start_screen()
            return

        self._draw_background()

        self.cam.begin()
        self._draw_dome()
        self._draw_escape_anchor()
        self.level.draw()
        self.hook.draw(self.player)
        self.player.draw()
        self.cam.end()

        self.fog.draw()

        if self.screen == GameScreen.PAUSED:
            self._draw_pause_overlay()
        elif self.screen == GameScreen.COMPLETE:
            self._draw_complete_screen()

        if self.debug:
            self._draw_debug()

    def _draw_centered(self, text: str, y: int, size: int, color: Color) -> None:
        draw_text(
            text, SCREEN_WIDTH // 2 - measure_text(text, size) // 2, y, size, color
        )

    def _draw_background(self) -> None:
        t = get_time()
        for center, radius, base_alpha, phase, speed in self.stars:
            a = int(base_alpha * (0.5 + 0.5 * math.sin(t * speed + phase)))
            draw_circle_v(center, radius, Color(255, 255, 255, a))

        # Moon
        draw_circle_v((75, 75), 50, Color(255, 255, 255, 200))
        draw_circle_v((65, 75), 50, Color(0, 0, 0, 50))
        draw_circle_v((65, 50), 5, Color(0, 0, 0, 50))
        draw_circle_v((45, 90), 4, Color(0, 0, 0, 50))
        draw_circle_v((80, 75), 3, Color(0, 0, 0, 50))
        draw_circle_v((87, 90), 7, Color(0, 0, 0, 50))
        draw_circle_v((100, 60), 4, Color(0, 0, 0, 50))

    def _draw_start_screen(self) -> None:
        self._draw_background()
        self.fog.draw()

        self._draw_centered(TITLE, SCREEN_HEIGHT // 3, 40, Color(220, 200, 160, 255))
        self._draw_centered(
            "Click to begin", SCREEN_HEIGHT // 3 + 60, 20, Color(180, 170, 140, 200)
        )
        self._draw_centered(
            "An astronomy professor falls into the Foggy Bottom Observatory.",
            SCREEN_HEIGHT // 3 + 100,
            16,
            Color(140, 130, 110, 180),
        )
        self._draw_centered(
            "Legs broken. The only way out is up. Hook and rope.",
            SCREEN_HEIGHT // 3 + 120,
            16,
            Color(140, 130, 110, 180),
        )
        self._draw_centered(
            "Press  P for controls",
            SCREEN_HEIGHT // 3 + 170,
            22,
            Color(240, 220, 160, 255),
        )

    def _draw_pause_overlay(self) -> None:
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Color(0, 0, 0, 160))

        self._draw_centered("PAUSED", 100, 36, Color(220, 200, 160, 255))

        controls = [
            "Left Click  -  Shoot / Release hook",
            "W / Up      -  Reel in rope",
            "S / Down    -  Let out rope",
            "A / D       -  Pump swing",
            "Mouse       -  Aim hook",
            "P           -  Pause / Resume",
            "1 / 2       -  Switch levels",
            "E           -  Debug overlay (fly mode)",
        ]
        y = 160
        for line in controls:
            lw = measure_text(line, 18)
            draw_text(
                line, SCREEN_WIDTH // 2 - lw // 2, y, 18, Color(200, 190, 160, 220)
            )
            y += 26

    def _dome_base_y(self) -> int:
        """World y of the topmost row containing walls, so the dome rests on them."""
        for r in range(self.level.rows):
            for c in range(self.level.cols):
                if self.level.tilemap[r][c] in (TILE_WALL, TILE_REFLECT):
                    return r * TILE_SIZE
        return 0

    def _draw_dome(self) -> None:
        # Observatory dome
        if self.current_level != 1:
            return
        cx = self.level.world_width // 2
        base_y = self._dome_base_y()
        radius = self.level.world_width // 2

        # Base
        band_h = 6
        draw_rectangle(
            cx - radius,
            base_y - band_h,
            radius * 2,
            band_h,
            Color(140, 140, 155, 255),
        )
        draw_rectangle(
            cx - radius,
            base_y - band_h,
            radius * 2,
            1,
            Color(225, 225, 240, 255),
        )

        # silver dome
        dome_y = base_y - band_h
        dome_center = Vector2(cx, dome_y)
        draw_circle_sector(dome_center, radius, 180, 360, 64, Color(*DOME_COLOR))

        # Right shadow
        draw_circle_sector(dome_center, radius, 290, 360, 32, Color(110, 110, 125, 70))
        # Left side light
        draw_circle_sector(
            Vector2(cx - 8, dome_y - 6),
            radius - 14,
            200,
            250,
            24,
            Color(230, 230, 245, 80),
        )

        # Outline
        draw_circle_sector_lines(
            dome_center, radius, 180, 360, 64, Color(120, 120, 135, 220)
        )

        # Vertical slit
        slit_w = 10
        slit_h = radius
        draw_rectangle(
            cx - slit_w // 2,
            dome_y - slit_h,
            slit_w,
            slit_h,
            Color(15, 15, 25, 235),
        )
        draw_rectangle(
            cx - slit_w // 2 - 1,
            dome_y - slit_h,
            1,
            slit_h,
            Color(200, 200, 215, 220),
        )
        draw_rectangle(
            cx + slit_w // 2,
            dome_y - slit_h,
            1,
            slit_h,
            Color(200, 200, 215, 220),
        )

        # spire
        spire_h = 12
        spire_y = dome_y - radius - spire_h
        draw_rectangle(cx - 1, spire_y, 2, spire_h, Color(110, 110, 125, 255))
        draw_circle(cx, spire_y, 3, Color(200, 200, 215, 255))

    def _draw_escape_anchor(self) -> None:
        # escape anchor + halo
        if self.escape_anchor is None:
            return
        cx = int(self.escape_anchor.x)
        cy = int(self.escape_anchor.y)
        draw_circle(cx, cy, 14, Color(255, 245, 200, 60))
        draw_circle(cx, cy, 10, Color(255, 245, 200, 110))
        draw_circle(cx, cy, ANCHOR_RADIUS, Color(*ANCHOR_COLOR))
        draw_circle_lines(cx, cy, ANCHOR_RADIUS + 1, Color(120, 110, 80, 255))

    def _draw_complete_screen(self) -> None:
        draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, Color(0, 0, 0, 180))
        self._draw_centered(
            "You escaped the Foggy Bottom!",
            SCREEN_HEIGHT // 3,
            30,
            Color(240, 220, 140, 255),
        )
        self._draw_centered(
            "Press R to return to title",
            SCREEN_HEIGHT // 3 + 50,
            20,
            Color(180, 170, 140, 200),
        )

    def _draw_debug(self) -> None:
        y = 10
        c = Color(0, 255, 0, 200)
        state_names = {
            Hook.STATE_IDLE: "IDLE",
            Hook.STATE_FLYING: "FLYING",
            Hook.STATE_ATTACHED: "ATTACHED",
        }

        stats = [
            f"FPS: {get_fps()}",
            f"Pos: ({self.player.pos_x:.0f}, {self.player.pos_y:.0f})",
            f"Vel: ({self.player.vel_x:.0f}, {self.player.vel_y:.0f})",
            f"Hook: {state_names.get(self.hook.state, '?')}",
            f"Ground: {self.player.on_ground}",
        ]
        if self.hook.state == Hook.STATE_ATTACHED:
            stats.insert(4, f"Rope: {self.hook.rope_length:.0f}")

        for line in stats:
            draw_text(line, 10, y, 16, c)
            y += 18

    def shutdown(self) -> None:
        if self.brick_texture:
            unload_texture(self.brick_texture)
        if self.char_texture:
            unload_texture(self.char_texture)
        if self.fog_texture:
            unload_texture(self.fog_texture)

        for sound in game_sounds.values():
            unload_sound(sound)
        for music in game_musics.values():
            unload_music_stream(music)

        game_sounds.clear()
        game_musics.clear()
