# Workshop Artwork

This folder contains a curated starter set for games made during the Phippy AI Game Workshop. It intentionally avoids copying entire source projects and does not include Pokemon character artwork or third-party RPG sheets with unclear reuse terms.

## Using the artwork in Godot

Godot sees files in this repository through `res://` paths. For example:

```text
res://assets/cncf-phippy/characters/phippy_full.svg
res://assets/pixel/phippy-rescue/phippy.png
res://assets/pixel/poketime/forest.png
```

For crisp pixel art, select the texture in Godot and use nearest-neighbor filtering. Keep the original files unchanged and adjust scale in the scene so future games can reuse the same assets.

## Official Phippy and Friends art

`cncf-phippy/characters/` contains color PNG and SVG artwork for:

Argi, Bitzy, Cappy, Captain Kube, Falkey, Goldie, Hazel, Indigo, Izzy, Keddy, Kuack, Ky, Linky, Obee, Owlina, Phippy, Tai, Tiago, and Zee.

`cncf-phippy/groups/` contains wide and square color group images in PNG and SVG formats.

Source: [CNCF artwork](https://github.com/cncf/artwork/tree/main/other/phippy-and-friends), imported from commit `6c39f12efdfdaf2225fb47bfa864b53f2b1215c2`.

The CNCF source repository makes the artwork available subject to Linux Foundation trademark usage guidelines. Using these characters does not imply that CNCF or the Linux Foundation sponsors or endorses a workshop or game. See `licenses/CNCF-artwork-LICENSE.md`.

## PhippyRescue pixel art

`pixel/phippy-rescue/` contains the artwork created for the PhippyRescue workshop:

- `phippy.png` is a 192 x 240 sprite sheet arranged in 3 columns and 8 rows.
- Captain Kube, Goldie, Hazel, Linky, Owlina, Tiago, and Zee are small character images.
- `podballoon.png` and `podballoon2.png` are 6-column by 8-row sheets.
- `podcarrier.png` and `podcarrier2.png` are 3-column by 7-row sheets.
- `podsitter.png` and `podsitter2.png` are 7-column by 4-row sheets.
- The remaining pod files provide alternate colors, poses, drops, and balloon-pop states.
- `island_background.png`, `sun.png`, and `phippywhistle.png` provide scenery and game items.

Source: [PhippyRescue](https://github.com/Tingsters/PhippyRescue), imported from commit `97d967673fc10621593334c3814ce993d2e50ea5`.

These files are distributed from an MIT-licensed repository. See `licenses/PhippyRescue-MIT.txt`.

## PokeTime pixel art

`pixel/poketime/` contains a small, non-Pokemon subset of reusable workshop art:

- `forest.png` and `battle_background.png` are game backgrounds.
- The six color-named player files are 96 x 192 walking sheets arranged in 3 columns and 4 rows.

Source: [PokeTime](https://github.com/Tingsters/PokeTime), imported from commit `cd017b17ed66d57cc089be26fc40cb31289b272d`.

These files are distributed from an MIT-licensed repository. See `licenses/PokeTime-MIT.txt`.

## Repository license

The workshop repository remains licensed under Apache-2.0. Imported artwork keeps the separate terms described above and in `assets/licenses/`.
