# GH1 - Jump pads
# BH1 - Limit platforms
# BH2 - Flying enemies to attack minions
# BH3 - Create more levels

@namespace
class SpriteKind:
    collider = SpriteKind.create()
    # GH1
    jump = SpriteKind.create()
    # /GH1

# variables
levels = [
    assets.tilemap("level 1"),
    assets.tilemap("level 2"),
    assets.tilemap("level 3"),
    assets.tilemap("level 4"),
    #BH3
    # simply designing a new tilemap and entering it into the levels list
    # assets.tilemap("level 5")
    assets.tilemap("level 5"),
    # /BH3
    #GH1
    # maybe invite coders in the last step to produce their own tilemap that requires a jump pad
]
level = -1
wave_size = 14
speed = 20
escaped_minions = 0
# BH1
platforms_available = 0
# /BH1
spawning_phase = False

# sprites
cursor = sprites.create(image.create(2, 2))
# BH1
platforms_counter = textsprite.create(str(platforms_available))
platforms_counter.set_flag(SpriteFlag.RELATIVE_TO_CAMERA, True)
# /BH1

# BH1
def update_platforms_counter():
    platforms_counter.set_text(str(platforms_available + " platforms"))
    platforms_counter.left = 0
    platforms_counter.bottom = 120
update_platforms_counter()
# /BH1

def next_level():
    global level
    info.change_score_by(escaped_minions * 10)
    level += 1
    reset_level()
next_level()

def reset_level():
    global escaped_minions, platforms_available # bh1 edit line
    if not spawning_phase:
        # BH1
        platforms_available = level + 3
        # /BH1
        escaped_minions = 0
        sprites.destroy_all_sprites_of_kind(SpriteKind.player)
        # GH1
        sprites.destroy_all_sprites_of_kind(SpriteKind.jump)
        # /GH1
        # BH2
        sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
        # /BH2
        for location in tiles.get_tiles_by_type(assets.tile("platform")):
            tiles.set_tile_at(location, assets.tile("empty"))
            tiles.set_wall_at(location, False)
        tiles.set_current_tilemap(levels[level])
        music.beam_up.play()
        timer.background(spawn_minions)
controller.B.on_event(ControllerButtonEvent.PRESSED, reset_level)

def spawn_minions():
    global spawning_phase
    spawning_phase = True
    pause(1250)
    for i in range(wave_size):
        pause(750)
        minion = sprites.create(assets.image("minion"), SpriteKind.player)
        sprites.set_data_number(minion, "x_vel", speed)
        tiles.place_on_random_tile(minion, assets.tile("spawn"))
        minion.ay = 120
        characterAnimations.loop_frames(minion, assets.animation("walk right"), 100, Predicate.MOVING_RIGHT)
        characterAnimations.loop_frames(minion, assets.animation("walk left"), 100, Predicate.MOVING_LEFT)
    music.power_up.play()
    spawning_phase = False

def mouse_behaviour():
    cursor.x = browserEvents.get_mouse_scene_x()
    cursor.y = browserEvents.get_mouse_scene_y()

def camera_movement():
    camera_x = scene.camera_property(CameraProperty.X)
    camera_y = scene.camera_property(CameraProperty.Y)
    if browserEvents.get_mouse_camera_x() < 15:
        scene.center_camera_at(camera_x - 1, camera_y)
    elif browserEvents.get_mouse_camera_x() > 145:
        scene.center_camera_at(camera_x + 1, camera_y)
    if browserEvents.get_mouse_camera_y() < 15:
        scene.center_camera_at(camera_x, camera_y - 1)
    elif browserEvents.get_mouse_camera_y() > 105:
        scene.center_camera_at(camera_x, camera_y + 1)

def minion_movement():
    number = 0
    for minion in sprites.all_of_kind(SpriteKind.player):
        if minion.is_hitting_tile(CollisionDirection.LEFT):
            sprites.set_data_number(minion, "x_vel", speed)
        elif minion.is_hitting_tile(CollisionDirection.RIGHT):
            sprites.set_data_number(minion, "x_vel", speed * -1)
        minion.vx = sprites.read_data_number(minion, "x_vel")
game.on_update(minion_movement)

def place_platform(x, y):
    # BH1
    global platforms_available
    if platforms_available < 1:
        return
    # /BH1
    if tiles.tile_at_location_equals(cursor.tilemap_location(), assets.tile("empty")):
    # BH1
        platforms_available -= 1
        update_platforms_counter()
    # /BH1
        tiles.set_tile_at(cursor.tilemap_location(), assets.tile("platform"))
        tiles.set_wall_at(cursor.tilemap_location(), True)
browserEvents.mouse_left.on_event(browserEvents.MouseButtonEvent.PRESSED, place_platform)

# BH2
def spawn_bat():
    if len(sprites.all_of_kind(SpriteKind.player)) < 1:
        return
    bat = tilesAdvanced.create_pathfinder_sprite(assets.image("bat"), SpriteKind.enemy)
    animation.run_image_animation(bat, assets.animation("bat flight"), 50, True)
    map_width = tilesAdvanced.get_tilemap_width()
    tiles.place_on_tile(bat, tiles.get_tile_location(randint(0, map_width), 0))
    target = sprites.all_of_kind(SpriteKind.player)._pick_random()
    tilesAdvanced.follow_using_pathfinding(bat, target, 15)
game.on_update_interval(10000, spawn_bat)

def minion_caught(minion, bat):
    minion.destroy()
    bat.destroy()
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, minion_caught)

def hit_bat(collider, bat):
    info.change_score_by(10)
    bat.destroy()
sprites.on_overlap(SpriteKind.collider, SpriteKind.enemy, hit_bat)
# /BH2

# GH1
def place_jump_pad():
    cursor_location = cursor.tilemap_location()
    if tiles.tile_at_location_equals(cursor_location, assets.tile("empty")):
        pad = sprites.create(assets.image("jump pad light"), SpriteKind.jump)
        sprites.set_data_number(pad, "jump_strength", -100)
        tiles.place_on_tile(pad, cursor_location)
controller.A.on_event(ControllerButtonEvent.PRESSED, place_jump_pad)

def jump(sprite, pad):
    jump_strength = sprites.read_data_number(pad, "jump_strength")
    sprite.vy = jump_strength
sprites.on_overlap(SpriteKind.player, SpriteKind.jump, jump)

def cycle_jump_pad(collider, pad):
    if pad.image.equals(assets.image("jump pad light")):
        pad.set_image(assets.image("jump pad strong"))
        sprites.set_data_number(pad, "jump_strength", -150)
    else:
        pad.set_image(assets.image("jump pad light"))
        sprites.set_data_number(pad, "jump_strength", -75)
    collider.destroy()
sprites.on_overlap(SpriteKind.collider, SpriteKind.jump, cycle_jump_pad)

# ---- Also required for BH2
def click_interact(x, y):
    collider = sprites.create(image.create(5, 5), SpriteKind.collider)
    collider.set_position(cursor.x, cursor.y)
    collider.image.fill(2)
    collider.set_flag(SpriteFlag.INVISIBLE, True)
    collider.lifespan = 500
browserEvents.mouse_wheel.on_event(browserEvents.MouseButtonEvent.PRESSED, click_interact)
# /GH1

def end_reached(minion, location):
    global escaped_minions
    escaped_minions += 1
    minion.destroy()
scene.on_overlap_tile(SpriteKind.player, assets.tile("end"), end_reached)

def spike_hit(minion, location):
    minion.destroy()
scene.on_overlap_tile(SpriteKind.player, assets.tile("spike"), spike_hit)

def check_remaining_minions():
    if len(sprites.all_of_kind(SpriteKind.player)) < 1:
        if escaped_minions > 3:
            if level > len(levels) - 1:
                game.over(True)
            else:
                next_level()
        else:
            reset_level()
sprites.on_destroyed(SpriteKind.player, check_remaining_minions)

def tick():
    mouse_behaviour()
    camera_movement()
game.on_update(tick)