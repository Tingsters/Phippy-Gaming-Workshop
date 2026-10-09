# Artwork maintenance

The artwork itself needs no Python packages and works offline.

From the repository root, check the image inventory, PNG integrity, dimensions,
checksums, relative links, animation metadata, and license notices with:

```sh
python tools/check_assets.py
```

For maintainers with [Pillow](https://python-pillow.org/) installed, compare every
included sheet against its separate frames and rebuild the picture guides with:

```sh
python tools/check_assets.py --pixels
python tools/build_asset_catalog.py
```

The generator uses `assets/pixel/manifest.json` and `assets/sources.json`.
It writes the category guides, the pixel catalog README, and preview PNGs.
The credits and animation guide are maintained separately. It never downloads
artwork or changes the original art PNGs. Install DejaVu Sans for matching
preview typography; otherwise the generator uses a fallback font.

Before adding more art, verify its original source and redistribution terms,
inspect every selected image for workshop suitability, retain license notices,
and update the manifest, source records, and credits. A “free download” label
alone does not establish reuse or redistribution rights. These scripts check
file consistency; visual and licensing review still need a person or assistant.
