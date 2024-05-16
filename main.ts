namespace SpriteKind {
    export const collider = SpriteKind.create()
}

//  variables
let levels = [assets.tilemap`level 1`, assets.tilemap`level 2`, assets.tilemap`level 3`, assets.tilemap`level 4`]
let level = -1
let wave_size = 14
let speed = 20
let escaped_minions = 0
let spawning_phase = false
//  sprites
let cursor = sprites.create(image.create(2, 2))
function next_level() {
    
    info.changeScoreBy(escaped_minions * 10)
    level += 1
    reset_level()
}

next_level()
function reset_level() {
    
    if (!spawning_phase) {
        for (let location of tiles.getTilesByType(assets.tile`platform`)) {
            tiles.setTileAt(location, assets.tile`empty`)
            tiles.setWallAt(location, false)
        }
        escaped_minions = 0
        sprites.destroyAllSpritesOfKind(SpriteKind.Player)
        tiles.setCurrentTilemap(levels[level])
        music.beamUp.play()
        timer.background(function spawn_minions() {
            let minion: Sprite;
            
            spawning_phase = true
            pause(1250)
            for (let i = 0; i < wave_size; i++) {
                pause(750)
                minion = sprites.create(assets.image`minion`, SpriteKind.Player)
                tiles.placeOnRandomTile(minion, assets.tile`spawn`)
                minion.vx = speed
                minion.ay = 120
                characterAnimations.loopFrames(minion, assets.animation`walk right`, 100, Predicate.MovingRight)
                characterAnimations.loopFrames(minion, assets.animation`walk left`, 100, Predicate.MovingLeft)
            }
            music.powerUp.play()
            spawning_phase = false
        })
    }
    
}

controller.B.onEvent(ControllerButtonEvent.Pressed, reset_level)
function mouse_behaviour() {
    cursor.x = browserEvents.getMouseSceneX()
    cursor.y = browserEvents.getMouseSceneY()
}

function camera_movement() {
    let camera_x = scene.cameraProperty(CameraProperty.X)
    let camera_y = scene.cameraProperty(CameraProperty.Y)
    if (browserEvents.getMouseCameraX() < 15) {
        scene.centerCameraAt(camera_x - 1, camera_y)
    } else if (browserEvents.getMouseCameraX() > 145) {
        scene.centerCameraAt(camera_x + 1, camera_y)
    }
    
    if (browserEvents.getMouseCameraY() < 15) {
        scene.centerCameraAt(camera_x, camera_y - 1)
    } else if (browserEvents.getMouseCameraY() > 105) {
        scene.centerCameraAt(camera_x, camera_y + 1)
    }
    
}

game.onUpdate(function minion_movement() {
    for (let minion of sprites.allOfKind(SpriteKind.Player)) {
        if (minion.isHittingTile(CollisionDirection.Left)) {
            minion.vx = speed
        } else if (minion.isHittingTile(CollisionDirection.Right)) {
            minion.vx = speed * -1
        }
        
    }
})
browserEvents.MouseLeft.onEvent(browserEvents.MouseButtonEvent.Pressed, function place_platform(x: any, y: any) {
    if (tiles.tileAtLocationEquals(cursor.tilemapLocation(), assets.tile`empty`)) {
        tiles.setTileAt(cursor.tilemapLocation(), assets.tile`platform`)
        tiles.setWallAt(cursor.tilemapLocation(), true)
    }
    
})
scene.onOverlapTile(SpriteKind.Player, assets.tile`end`, function end_reached(minion: Sprite, location: tiles.Location) {
    
    escaped_minions += 1
    minion.destroy()
})
scene.onOverlapTile(SpriteKind.Player, assets.tile`spike`, function spike_hit(minion: Sprite, location: tiles.Location) {
    minion.destroy()
})
sprites.onDestroyed(SpriteKind.Player, function check_remaining_minions() {
    if (sprites.allOfKind(SpriteKind.Player).length < 1) {
        if (escaped_minions > 3) {
            if (level > levels.length - 1) {
                game.over(true)
            } else {
                next_level()
            }
            
        } else {
            reset_level()
        }
        
    }
    
})
game.onUpdate(function tick() {
    mouse_behaviour()
    camera_movement()
})
