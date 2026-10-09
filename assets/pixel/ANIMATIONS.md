# Make your pictures move

[Back to all artwork](README.md)

SunnyLand includes **20 animation and pose sequences**. The files named `frame-01`, `frame-02`, and so on are already separate pictures. Three sequences are single poses.

## In Godot 4

1. Add an `AnimatedSprite2D` and create its `SpriteFrames` resource.
2. Create an animation such as `fox-run`.
3. Add the individual frame PNGs in the order shown by their numbered filenames (or the exact order in [animations.json](animations.json)).
4. Try **8 frames per second** as a starting point. This speed is a workshop suggestion, not timing metadata from the artist.
5. Loop idle, running, and flying sequences. Play jump, hurt, victory, and sparkle sequences when the game needs them; choose looping to suit your game.
6. Use **Nearest** texture filtering for crisp pixels.

A single-frame pose can use `Sprite2D`. Some frame files have transparent padding; keep their original dimensions so the animation stays aligned.

## Frame sizes and sheets

All included sheets below have **one row**, no spacing, and no outer margin. Their horizontal frame count is listed. Each included sheet was checked pixel-for-pixel against its individual frames. You can use Godot's “Add frames from a sprite sheet” with the listed columns and one row.

| Sequence | Frames / sheet columns | Frame pixels | First frame | Verified sheet |
| --- | ---: | --- | --- | --- |
| fox-dizzy | 6 | 33 x 32 | [Frame 01](characters/sunnyland/fox-dizzy-frame-01.png) | [PNG](characters/sunnyland/fox-dizzy-sheet.png) |
| fox-tumble | 1 | 33 x 32 | [Frame 01](characters/sunnyland/fox-tumble-frame-01.png) | [PNG](characters/sunnyland/fox-tumble-sheet.png) |
| fox-look-up | 1 | 33 x 32 | [Frame 01](characters/sunnyland/fox-look-up-frame-01.png) | [PNG](characters/sunnyland/fox-look-up-sheet.png) |
| fox-roll | 4 | 33 x 32 | [Frame 01](characters/sunnyland/fox-roll-frame-01.png) | [PNG](characters/sunnyland/fox-roll-sheet.png) |
| fox-victory | 1 | 33 x 32 | [Frame 01](characters/sunnyland/fox-victory-frame-01.png) | [PNG](characters/sunnyland/fox-victory-sheet.png) |
| fox-wall-grab | 2 | 33 x 32 | [Frame 01](characters/sunnyland/fox-wall-grab-frame-01.png) | [PNG](characters/sunnyland/fox-wall-grab-sheet.png) |
| fox-climb | 4 | 33 x 32 | [Frame 01](characters/sunnyland/fox-climb-frame-01.png) | [PNG](characters/sunnyland/fox-climb-sheet.png) |
| fox-crouch | 3 | 33 x 32 | [Frame 01](characters/sunnyland/fox-crouch-frame-01.png) | [PNG](characters/sunnyland/fox-crouch-sheet.png) |
| fox-hurt | 2 | 33 x 32 | [Frame 01](characters/sunnyland/fox-hurt-frame-01.png) | [PNG](characters/sunnyland/fox-hurt-sheet.png) |
| fox-idle | 4 | 33 x 32 | [Frame 01](characters/sunnyland/fox-idle-frame-01.png) | [PNG](characters/sunnyland/fox-idle-sheet.png) |
| fox-jump | 2 | 33 x 32 | [Frame 01](characters/sunnyland/fox-jump-frame-01.png) | [PNG](characters/sunnyland/fox-jump-sheet.png) |
| fox-run | 6 | 33 x 32 | [Frame 01](characters/sunnyland/fox-run-frame-01.png) | [PNG](characters/sunnyland/fox-run-sheet.png) |
| opossum-run | 6 | 36 x 28 | [Frame 01](animals/sunnyland/opossum-run-frame-01.png) | [PNG](animals/sunnyland/opossum-run-sheet.png) |
| eagle-fly | 4 | 40 x 41 | [Frame 01](animals/sunnyland/eagle-fly-frame-01.png) | [PNG](animals/sunnyland/eagle-fly-sheet.png) |
| frog-idle | 4 | 35 x 32 | [Frame 01](animals/sunnyland/frog-idle-frame-01.png) | [PNG](animals/sunnyland/frog-idle-sheet.png) |
| frog-jump | 2 | 35 x 32 | [Frame 01](animals/sunnyland/frog-jump-frame-01.png) | Use individual frames |
| magic-poof | 6 | 40 x 41 | [Frame 01](effects/sunnyland/magic-poof-frame-01.png) | [PNG](effects/sunnyland/magic-poof-sheet.png) |
| collect-sparkle | 4 | 32 x 32 | [Frame 01](effects/sunnyland/collect-sparkle-frame-01.png) | Use individual frames |
| cherry-spin | 7 | 21 x 21 | [Frame 01](items/sunnyland/cherry-spin-frame-01.png) | Use individual frames |
| gem-sparkle | 5 | 15 x 13 | [Frame 01](items/sunnyland/gem-sparkle-frame-01.png) | [PNG](items/sunnyland/gem-sparkle-sheet.png) |

**Why some sheets are missing:** the original frog-jump, collect-sparkle, and cherry-spin sheets differ from their supplied individual frames. This collection uses the checked individual frames for those sequences and omits those mismatched sheets.

The animated fox's hurt/tumble pictures are cartoon reactions with no blood. The magic-poof sequence is a star-and-cloud effect, renamed from the source's enemy-disappearance effect.

Other packs contain individual poses and tiles. Their filenames do not promise a particular animation speed or frame sequence. [Credits](../CREDITS.md) travel with copied artwork.
