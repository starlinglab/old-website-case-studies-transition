# starling-old-preserved

Starling Lab is transitioning to a new website. Rather than migrate the old WordPress instance, we are preserving a set of case studies and project pages as standalone static sites so that their URLs and any existing citations remain intact.

The pages below represent work that lives at specific, potentially-cited URLs. Moving them into a new WordPress instance turned out to be more effort than it was worth, so we repackaged them in their original visual style as self-contained static bundles — no server-side dependencies, no database, no plugin maintenance.

Each bundle is a flat directory with a simple `assets/{css,js,fonts,img}/` structure, ready to drop onto any static host at the same path.

## Preserved pages

| Directory | Original URL |
|-----------|-------------|
| `anita/` | [starlinglab.org/anita/](https://www.starlinglab.org/anita/) |
| `what-to-get-right-first/` | [starlinglab.org/what-to-get-right-first/](https://www.starlinglab.org/what-to-get-right-first/) |
| `78days/` | [starlinglab.org/78days/](https://www.starlinglab.org/78days/) (14 pages — see below) |

### 78days page tree

```
78days/
├── index.html                                    (main)
├── background/
├── challenges/
├── image-authentication/
├── reflections/
├── 78daysarchive/
├── 78daysarchive-mobile/
├── 78days-archive-mobile-day-4/
├── 78days-archive-mobile-transition/
├── 78days-archive-mobile-insurrection/
├── 78days-archive-mobile-inauguration/
├── reflections-authenticity-and-equity/
├── reflections-does-authenticity-guarantee-access/
└── reflections-trust-or-complacency/
```

## Raw mirror

`mirror/www.starlinglab.org/` contains the raw `wget --mirror` output (unconverted, original directory structure) from which the flat bundles were generated.

## wget commands

### anita

```bash
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent \
  -P mirror \
  https://www.starlinglab.org/anita/
```

### what-to-get-right-first

```bash
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent \
  -P mirror \
  https://www.starlinglab.org/what-to-get-right-first/
```

### 78days

The main page and its subpages were mirrored in separate passes as internal links were discovered.

```bash
# Main page
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent \
  -P mirror \
  https://www.starlinglab.org/78days/

# Primary subpages (linked from main)
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent \
  -P mirror \
  https://www.starlinglab.org/background/ \
  https://www.starlinglab.org/challenges/ \
  https://www.starlinglab.org/image-authentication/ \
  https://www.starlinglab.org/reflections/

# Archive pages (linked from challenges and image-authentication)
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent \
  -P mirror \
  https://www.starlinglab.org/78daysarchive/ \
  https://www.starlinglab.org/78daysarchive-mobile/

# Mobile archive chain (linked sequentially)
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent \
  -P mirror \
  https://www.starlinglab.org/78days-archive-mobile-day-4/ \
  https://www.starlinglab.org/78days-archive-mobile-transition/ \
  https://www.starlinglab.org/78days-archive-mobile-insurrection/ \
  https://www.starlinglab.org/78days-archive-mobile-inauguration/

# Reflections essays (linked from reflections/)
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent \
  -P mirror \
  https://www.starlinglab.org/reflections-authenticity-and-equity/ \
  https://www.starlinglab.org/reflections-does-authenticity-guarantee-access/ \
  https://www.starlinglab.org/reflections-trust-or-complacency/
```

## Flatten scripts

Each bundle was produced by a Python script that copies assets into `assets/{css,js,fonts,img}/`, rewrites all `src`/`href`/`url()` references, strips WordPress version query strings, and (for 78days) rewrites internal navigation links between subpages.

| Script | Output |
|--------|--------|
| `flatten.py` | `anita/` |
| `flatten_wtgrf.py` | `what-to-get-right-first/` |
| `flatten_78days.py` | `78days/` |

## Notes

- Photos in the 78days mobile archive grids are served dynamically from `images.starlinglab.org` via JSON and are **not** included in this preservation.
- The `reflections/` page buttons (TRUST / ACCESS / EQUITY) have been patched with direct `onclick` handlers since Elementor's column-click JS does not run in a static context.
