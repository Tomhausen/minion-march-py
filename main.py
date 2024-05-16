@namespace
class SpriteKind:
    collider = SpriteKind.create()

# variables
levels = [
    assets.tilemap("level 1"),
    assets.tilemap("level 2"),
    assets.tilemap("level 3"),
    assets.tilemap("level 4"),
]

level = -1
wave_size = 14
speed = 20
escaped_minions = 0
spawning_phase = False

# sprites
cursor = sprites.create(image.create(2, 2))

def next_level():
    global level
    info.change_score_by(escaped_minions * 10)
    level += 1
    reset_level()
next_level()

def reset_level():
    global escaped_minions
    if not spawning_phase:
        for location in tiles.get_tiles_by_type(assets.tile("platform")):
            tiles.set_tile_at(location, assets.tile("empty"))
            tiles.set_wall_at(location, False)
        escaped_minions = 0
        sprites.destroy_all_sprites_of_kind(SpriteKind.player)
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
        tiles.place_on_random_tile(minion, assets.tile("spawn"))
        minion.vx = speed
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
    for minion in sprites.all_of_kind(SpriteKind.player):
        if minion.is_hitting_tile(CollisionDirection.LEFT):
            minion.vx = speed
        elif minion.is_hitting_tile(CollisionDirection.RIGHT):
            minion.vx = speed * -1
game.on_update(minion_movement)

def place_platform(x, y):
    if tiles.tile_at_location_equals(cursor.tilemap_location(), assets.tile("empty")):
        tiles.set_tile_at(cursor.tilemap_location(), assets.tile("platform"))
        tiles.set_wall_at(cursor.tilemap_location(), True)
browserEvents.mouse_left.on_event(browserEvents.MouseButtonEvent.PRESSED, place_platform)

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