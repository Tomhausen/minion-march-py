// Auto-generated code. Do not edit.
namespace myTiles {
    //% fixedInstance jres blockIdentity=images._tile
    export const transparency16 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile1 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile3 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile4 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile6 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile2 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile5 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile7 = image.ofBuffer(hex``);
    //% fixedInstance jres blockIdentity=images._tile
    export const tile8 = image.ofBuffer(hex``);

    helpers._registerFactory("tilemap", function(name: string) {
        switch(helpers.stringTrim(name)) {
            case "level 1":
            case "level4":return tiles.createTilemap(hex`0d0008000404040404040404040404040402040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404040404030101010101010104010104010101010101010101050101050101`, img`
. . . . . . . . . . . . . 
. . . . . . . . . . . . . 
. . . . . . . . . . . . . 
. . . . . . . . . . . . . 
. . . . . . . . . . . . . 
. . . . . . . . . . . . . 
2 2 2 2 2 2 2 . 2 2 . 2 2 
2 2 2 2 2 2 2 . 2 2 . 2 2 
`, [myTiles.transparency16,myTiles.tile1,myTiles.tile3,myTiles.tile4,myTiles.tile2,myTiles.tile5], TileScale.Sixteen);
            case "level 3":
            case "level2":return tiles.createTilemap(hex`0d00100002040404040404040404040406050404040404040404040404060501010101010404040404040605040404040404040404040406050404040404040404040404060504040404010101010101040605040404040404040404040406050404040404040404040404060501010101010104040404040605040404040404040404040406050404040404040404040404060504040404040101010101040605040404040404040404040406050404040404040304040404060504010101010101040404040605040404040404040404040406`, img`
. . . . . . . . . . . . . 
. . . . . . . . . . . . . 
. 2 2 2 2 2 . . . . . . . 
. . . . . . . . . . . . . 
. . . . . . . . . . . . . 
. . . . . 2 2 2 2 2 2 . . 
. . . . . . . . . . . . . 
. . . . . . . . . . . . . 
. 2 2 2 2 2 2 . . . . . . 
. . . . . . . . . . . . . 
. . . . . . . . . . . . . 
. . . . . . 2 2 2 2 2 . . 
. . . . . . . . . . . . . 
. . . . . . . . . . . . . 
. . 2 2 2 2 2 2 . . . . . 
. . . . . . . . . . . . . 
`, [myTiles.transparency16,myTiles.tile1,myTiles.tile3,myTiles.tile4,myTiles.tile2,sprites.builtin.forestTiles9,sprites.builtin.forestTiles11], TileScale.Sixteen);
            case "level 4":
            case "level 4":return tiles.createTilemap(hex`1000160005050505050505050505050505050505050205050505050505050505050505050505050505050505050505050505050505050505050505050505050505050505010101010101010105050505050505050101010101010101010101010505050505050505050505050505050505050505050505050505050505050505050505050505050505050505050505010505050505050505050505050505050505050505050505050505050505050505050505050505050505050505050505010505050505050505050505050505050505050505050505050505050505050505050505050505050505050505050505010505050505050505050505050505050505050505050505050505050505050505050505050505050505050505050505010405050505050505050505050505050504050505050505050505050505050503040505050505050505050505050505010405050506060606060606060606060606060606`, img`
................
................
................
................
22222222........
222222222222....
................
................
...........2....
................
................
...........2....
................
................
...........2....
................
................
...........22...
............2...
............2...
...........22...
................
`, [myTiles.transparency16,myTiles.tile1,myTiles.tile3,myTiles.tile4,myTiles.tile6,myTiles.tile2,myTiles.tile5], TileScale.Sixteen);
            case "level 2":
            case "level1":return tiles.createTilemap(hex`0a000e000101010101010101010101020302020202020201010202020202020202010102020202020202020101020101010101010101010201010101010101010102020202020202020101020202020202020201010101010202010102010101010105050101020101020202020202020201010402020202020202010101010102010201010101010101050105010101`, img`
2 2 2 2 2 2 2 2 2 2 
2 . . . . . . . . 2 
2 . . . . . . . . 2 
2 . . . . . . . . 2 
2 . 2 2 2 2 2 2 2 2 
2 . 2 2 2 2 2 2 2 2 
2 . . . . . . . . 2 
2 . . . . . . . . 2 
2 2 2 2 . . 2 2 . 2 
2 2 2 2 . . 2 2 . 2 
2 . . . . . . . . 2 
2 . . . . . . . . 2 
2 2 2 2 . 2 . 2 2 2 
2 2 2 2 . 2 . 2 2 2 
`, [myTiles.transparency16,myTiles.tile1,myTiles.tile2,myTiles.tile3,myTiles.tile4,myTiles.tile5], TileScale.Sixteen);
        }
        return null;
    })

    helpers._registerFactory("tile", function(name: string) {
        switch(helpers.stringTrim(name)) {
            case "transparency16":return transparency16;
            case "dirt":
            case "tile1":return tile1;
            case "spawn":
            case "tile3":return tile3;
            case "end":
            case "tile4":return tile4;
            case "platform":
            case "tile6":return tile6;
            case "empty":
            case "tile2":return tile2;
            case "spike":
            case "tile5":return tile5;
            case "trap danger":
            case "tile7":return tile7;
            case "trap safe":
            case "tile8":return tile8;
        }
        return null;
    })

}
// Auto-generated code. Do not edit.
