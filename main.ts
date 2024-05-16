//  GH1 - Jump pads
//  BH1 - Limit platforms
//  BH2 - Flying enemies to attack minions
//  BH3 - Create more levels
//  GH2 - Teleport (with extra step at the end asking them to create a tilemap requiring portals to solve)
//  BH4 - Stun minions upon right clicking
//  BH5 - Timed Trap (with extra step at the end asking them to create a tilemap featuring trap spawns)
//  BH6 - Degradeable platforms
namespace SpriteKind {
    export const collider = SpriteKind.create()
    export const jump = SpriteKind.create()
    //  GH2
    export const portal = SpriteKind.create()
}

//  /GH2
//  variables
let levels = [assets.tilemap`level 1`, assets.tilemap`level 2`, assets.tilemap`level 3`, assets.tilemap`level 4`, assets.tilemap`level 5`]
//  BH6
let platforms_to_reset : tiles.Location[] = []
//  /BH6
let level = -1
let wave_size = 14
let speed = 20
let escaped_minions = 0
let platforms_available = 0
let spawning_phase = false
//  BH5
let traps_active = false
//  /BH5
//  sprites
let cursor = sprites.create(image.create(2, 2))
let platforms_counter = textsprite.create("" + platforms_available)
platforms_counter.setFlag(SpriteFlag.RelativeToCamera, true)
//  GH2
let blue_portal = sprites.create(assets.image`blue portal`, SpriteKind.portal)
let orange_portal = sprites.create(assets.image`orange portal`, SpriteKind.portal)
let portal_to_place = blue_portal
//  /GH2
function update_platforms_counter() {
    platforms_counter.setText("" + (platforms_available + " platforms"))
    platforms_counter.left = 0
    platforms_counter.bottom = 120
}

update_platforms_counter()
function next_level() {
    
    info.changeScoreBy(escaped_minions * 10)
    level += 1
    reset_level()
}

next_level()
//  GH2
function reset_portals() {
    orange_portal.setPosition(-10, -10)
    blue_portal.setPosition(-10, -10)
    sprites.setDataBoolean(orange_portal, "active", false)
    sprites.setDataBoolean(blue_portal, "active", false)
}

//  /GH2
function reset_level() {
    
    //  bh1 edit line
    if (!spawning_phase) {
        platforms_available = level + 3
        escaped_minions = 0
        sprites.destroyAllSpritesOfKind(SpriteKind.Player)
        sprites.destroyAllSpritesOfKind(SpriteKind.jump)
        sprites.destroyAllSpritesOfKind(SpriteKind.Enemy)
        //  GH2
        reset_portals()
        //  /GH2
        for (let location of tiles.getTilesByType(assets.tile`platform`)) {
            tiles.setTileAt(location, assets.tile`empty`)
            tiles.setWallAt(location, false)
        }
        tiles.setCurrentTilemap(levels[level])
        music.beamUp.play()
        timer.background(function spawn_minions() {
            let minion: Sprite;
            
            spawning_phase = true
            pause(1250)
            for (let i = 0; i < wave_size; i++) {
                pause(750)
                minion = sprites.create(assets.image`minion`, SpriteKind.Player)
                sprites.setDataNumber(minion, "x_vel", speed)
                tiles.placeOnRandomTile(minion, assets.tile`spawn`)
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
//  BH5
function trap_behaviour() {
    for (let trap_safe of tiles.getTilesByType(assets.tile`trap safe`)) {
        tiles.setTileAt(trap_safe, assets.tile`trap danger`)
    }
    pause(2000)
    for (let trap_danger of tiles.getTilesByType(assets.tile`trap danger`)) {
        tiles.setTileAt(trap_danger, assets.tile`trap safe`)
    }
    pause(6000)
    trap_behaviour()
}

timer.background(trap_behaviour)
scene.onOverlapTile(SpriteKind.Player, assets.tile`trap danger`, function trap_hit(minion: Sprite, location: tiles.Location) {
    minion.destroy()
})
//  /BH5
//  GH2
browserEvents.T.onEvent(browserEvents.KeyEvent.Pressed, function place_portal() {
    
    let cursor_location = cursor.tilemapLocation()
    if (tiles.tileAtLocationIsWall(cursor_location)) {
        return
    }
    
    tiles.placeOnTile(portal_to_place, cursor_location)
    sprites.setDataBoolean(portal_to_place, "active", true)
    if (portal_to_place === blue_portal) {
        portal_to_place = orange_portal
    } else {
        portal_to_place = blue_portal
    }
    
})
//  /GH2
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
    let number = 0
    for (let minion of sprites.allOfKind(SpriteKind.Player)) {
        if (minion.isHittingTile(CollisionDirection.Left)) {
            sprites.setDataNumber(minion, "x_vel", speed)
        } else if (minion.isHittingTile(CollisionDirection.Right)) {
            sprites.setDataNumber(minion, "x_vel", speed * -1)
        }
        
        minion.vx = sprites.readDataNumber(minion, "x_vel")
    }
})
//  BH6
//  leave this line if didnt do bh1
//  /BH6
//  /BH6
browserEvents.MouseLeft.onEvent(browserEvents.MouseButtonEvent.Pressed, function place_platform(x: any, y: any) {
    
    if (platforms_available < 1) {
        return
    }
    
    if (tiles.tileAtLocationEquals(cursor.tilemapLocation(), assets.tile`empty`)) {
        platforms_available -= 1
        update_platforms_counter()
        tiles.setTileAt(cursor.tilemapLocation(), assets.tile`platform`)
        tiles.setWallAt(cursor.tilemapLocation(), true)
        //  BH6
        platforms_to_reset.push(cursor.tilemapLocation())
        timer.after(8000, function reset_platform() {
            let location: tiles.Location;
            
            //  leave this line if didnt do bh1
            if (platforms_to_reset.length < 1) {
                return
            }
            
            location = platforms_to_reset[0]
            platforms_to_reset.shift()
            tiles.setTileAt(location, assets.tile`empty`)
            tiles.setWallAt(location, false)
            music.knock.play()
            platforms_available += 1
        })
    }
    
})
game.onUpdateInterval(10000, function spawn_bat() {
    if (sprites.allOfKind(SpriteKind.Player).length < 1) {
        return
    }
    
    let bat = tilesAdvanced.createPathfinderSprite(assets.image`bat`, SpriteKind.Enemy)
    animation.runImageAnimation(bat, assets.animation`bat flight`, 50, true)
    let map_width = tilesAdvanced.getTilemapWidth()
    tiles.placeOnTile(bat, tiles.getTileLocation(randint(0, map_width), 0))
    let target = sprites.allOfKind(SpriteKind.Player)._pickRandom()
    tilesAdvanced.followUsingPathfinding(bat, target, 15)
})
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function minion_caught(minion: Sprite, bat: Sprite) {
    minion.destroy()
    bat.destroy()
})
sprites.onOverlap(SpriteKind.collider, SpriteKind.Enemy, function hit_bat(collider: Sprite, bat: Sprite) {
    info.changeScoreBy(10)
    bat.destroy()
})
controller.A.onEvent(ControllerButtonEvent.Pressed, function place_jump_pad() {
    let pad: Sprite;
    let cursor_location = cursor.tilemapLocation()
    if (tiles.tileAtLocationEquals(cursor_location, assets.tile`empty`)) {
        pad = sprites.create(assets.image`jump pad light`, SpriteKind.jump)
        sprites.setDataNumber(pad, "jump_strength", -100)
        tiles.placeOnTile(pad, cursor_location)
    }
    
})
sprites.onOverlap(SpriteKind.Player, SpriteKind.jump, function jump(sprite: Sprite, pad: Sprite) {
    let jump_strength = sprites.readDataNumber(pad, "jump_strength")
    sprite.vy = jump_strength
})
sprites.onOverlap(SpriteKind.collider, SpriteKind.jump, function cycle_jump_pad(collider: Sprite, pad: Sprite) {
    if (pad.image.equals(assets.image`jump pad light`)) {
        pad.setImage(assets.image`jump pad strong`)
        sprites.setDataNumber(pad, "jump_strength", -150)
    } else {
        pad.setImage(assets.image`jump pad light`)
        sprites.setDataNumber(pad, "jump_strength", -75)
    }
    
    collider.destroy()
})
//  potentially in BH4
browserEvents.MouseWheel.onEvent(browserEvents.MouseButtonEvent.Pressed, function click_interact(x: any, y: any) {
    let collider = sprites.create(image.create(5, 5), SpriteKind.collider)
    collider.setPosition(cursor.x, cursor.y)
    collider.image.fill(2)
    collider.setFlag(SpriteFlag.Invisible, true)
    collider.lifespan = 500
})
//  BH4
sprites.onOverlap(SpriteKind.collider, SpriteKind.Player, function stun_minion(collider: Sprite, minion: Sprite) {
    let old_vx: number;
    if (!sprites.readDataBoolean(minion, "stunned")) {
        sprites.setDataBoolean(minion, "stunned", true)
        old_vx = minion.vx
        minion.vx = 0
        minion.sayText("!", 2000)
        collider.destroy()
        pause(2000)
        minion.vx = old_vx
        sprites.setDataBoolean(minion, "stunned", false)
    }
    
})
//  /BH4
//  GH2
sprites.onOverlap(SpriteKind.Player, SpriteKind.portal, function enter_portal(minion: Sprite, portal: Sprite) {
    if (sprites.readDataBoolean(minion, "recently teleported")) {
        return
    }
    
    if (sprites.readDataBoolean(blue_portal, "active") && sprites.readDataBoolean(orange_portal, "active")) {
        if (portal.image.equals(assets.image`blue portal`)) {
            minion.setPosition(orange_portal.x, orange_portal.y)
        } else {
            minion.setPosition(blue_portal.x, blue_portal.y)
        }
        
        sprites.setDataBoolean(minion, "recently teleported", true)
        pause(1000)
        sprites.setDataBoolean(minion, "recently teleported", false)
    }
    
})
//  /GH2
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
