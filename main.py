# GH1 - Jump pads
# BH1 - Limit platforms
# BH2 - Flying enemies to attack minions
# BH3 - Create more levels

# GH2 - Teleport (with extra step at the end asking them to create a tilemap requiring portals to solve)
# BH4 - Stun minions upon right clicking
# BH5 - Timed Trap (with extra step at the end asking them to create a tilemap featuring trap spawns)
# BH6 - Degradeable platforms

@namespace
class SpriteKind:
    collider = SpriteKind.create()
    jump = SpriteKind.create()
# GH2
    portal = SpriteKind.create()
# /GH2

# variables
levels = [
    assets.tilemap("level 1"),
    assets.tilemap("level 2"),
    assets.tilemap("level 3"),
    assets.tilemap("level 4"),
    assets.tilemap("level 5"),
]
# BH6
platforms_to_reset: List[tiles.Location] = []
# /BH6
level = -1
wave_size = 14
speed = 20
escaped_minions = 0
platforms_available = 0
spawning_phase = False
# BH5
traps_active = False
# /BH5

# sprites
cursor = sprites.create(image.create(2, 2))
platforms_counter = textsprite.create(str(platforms_available))
platforms_counter.set_flag(SpriteFlag.RELATIVE_TO_CAMERA, True)
# GH2
blue_portal = sprites.create(assets.image("blue portal"), SpriteKind.portal)
orange_portal = sprites.create(assets.image("orange portal"), SpriteKind.portal)
portal_to_place = blue_portal
# /GH2

def update_platforms_counter():
    platforms_counter.set_text(str(platforms_available + " platforms"))
    platforms_counter.left = 0
    platforms_counter.bottom = 120
update_platforms_counter()

def next_level():
    global level
    info.change_score_by(escaped_minions * 10)
    level += 1
    reset_level()
next_level()

# GH2
def reset_portals():
    orange_portal.set_position(-10, -10)
    blue_portal.set_position(-10, -10)
    sprites.set_data_boolean(orange_portal, "active", False)
    sprites.set_data_boolean(blue_portal, "active", False)
# /GH2

def reset_level():
    global escaped_minions, platforms_available # bh1 edit line
    if not spawning_phase:
        platforms_available = level + 3
        escaped_minions = 0
        sprites.destroy_all_sprites_of_kind(SpriteKind.player)
        sprites.destroy_all_sprites_of_kind(SpriteKind.jump)
        sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
        # GH2
        reset_portals()
        # /GH2
        for location in tiles.get_tiles_by_type(assets.tile("platform")):
            tiles.set_tile_at(location, assets.tile("empty"))
            tiles.set_wall_at(location, False)
        tiles.set_current_tilemap(levels[level])
        music.beam_up.play()
        timer.background(spawn_minions)
controller.B.on_event(ControllerButtonEvent.PRESSED, reset_level)

# BH5
def trap_behaviour():
    for trap_safe in tiles.get_tiles_by_type(assets.tile("trap safe")):
        tiles.set_tile_at(trap_safe, assets.tile("trap danger"))
    pause(2000)
    for trap_danger in tiles.get_tiles_by_type(assets.tile("trap danger")):
        tiles.set_tile_at(trap_danger, assets.tile("trap safe"))
    pause(6000)
    trap_behaviour()
timer.background(trap_behaviour)

def trap_hit(minion, location):
    minion.destroy()
scene.on_overlap_tile(SpriteKind.player, assets.tile("trap danger"), trap_hit)
# /BH5

# GH2
def place_portal():
    global portal_to_place
    cursor_location = cursor.tilemap_location()
    if tiles.tile_at_location_is_wall(cursor_location):
        return
    tiles.place_on_tile(portal_to_place, cursor_location)
    sprites.set_data_boolean(portal_to_place, "active", True)
    if portal_to_place is blue_portal:
        portal_to_place = orange_portal
    else:
        portal_to_place = blue_portal
browserEvents.T.on_event(browserEvents.KeyEvent.PRESSED, place_portal)
# /GH2

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

# BH6
def reset_platform():
    global platforms_available # leave this line if didnt do bh1
    if len(platforms_to_reset) < 1:
        return
    location = platforms_to_reset[0]
    platforms_to_reset.shift()
    tiles.set_tile_at(location, assets.tile("empty"))
    tiles.set_wall_at(location, False)
    music.knock.play()
    platforms_available += 1 # leave this line if didnt do bh1
# /BH6

def place_platform(x, y):
    global platforms_available
    if platforms_available < 1:
        return
    if tiles.tile_at_location_equals(cursor.tilemap_location(), assets.tile("empty")):
        platforms_available -= 1
        update_platforms_counter()
        tiles.set_tile_at(cursor.tilemap_location(), assets.tile("platform"))
        tiles.set_wall_at(cursor.tilemap_location(), True)
        # BH6
        platforms_to_reset.push(cursor.tilemap_location())
        timer.after(8000, reset_platform)
        # /BH6
browserEvents.mouse_left.on_event(browserEvents.MouseButtonEvent.PRESSED, place_platform)

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

# potentially in BH4
def click_interact(x, y):
    collider = sprites.create(image.create(5, 5), SpriteKind.collider)
    collider.set_position(cursor.x, cursor.y)
    collider.image.fill(2)
    collider.set_flag(SpriteFlag.INVISIBLE, True)
    collider.lifespan = 500
browserEvents.mouse_wheel.on_event(browserEvents.MouseButtonEvent.PRESSED, click_interact)

# BH4
def stun_minion(collider, minion):
    if not sprites.read_data_boolean(minion, "stunned"):
        sprites.set_data_boolean(minion, "stunned", True)
        old_vx = minion.vx
        minion.vx = 0
        minion.say_text("!", 2000)
        collider.destroy()
        pause(2000)
        minion.vx = old_vx
        sprites.set_data_boolean(minion, "stunned", False)
sprites.on_overlap(SpriteKind.collider, SpriteKind.player, stun_minion)
# /BH4

# GH2
def enter_portal(minion, portal):
    if sprites.read_data_boolean(minion, "recently teleported"):
        return
    if sprites.read_data_boolean(blue_portal, "active") and sprites.read_data_boolean(orange_portal, "active"):
        if portal.image.equals(assets.image("blue portal")):
            minion.set_position(orange_portal.x, orange_portal.y)
        else:
            minion.set_position(blue_portal.x, blue_portal.y)
        sprites.set_data_boolean(minion, "recently teleported", True)
        pause(1000)
        sprites.set_data_boolean(minion, "recently teleported", False)
sprites.on_overlap(SpriteKind.player, SpriteKind.portal, enter_portal)
# /GH2

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