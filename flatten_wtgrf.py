#!/usr/bin/env python3
"""
Flatten the wget mirror of starlinglab.org/what-to-get-right-first/ into a flat static bundle.

Input:  mirror/www.starlinglab.org/
Output: what-to-get-right-first/
"""

import os
import re
import shutil
from pathlib import Path

SRC = Path("mirror/www.starlinglab.org")
DST = Path("what-to-get-right-first")

FILE_MAP = {
    # HTML
    "what-to-get-right-first/index.html": "index.html",

    # CSS
    "wp-content/plugins/contact-form-7/includes/css/styles.css?ver=6.1.5.css":
        "assets/css/contact-form-7.css",
    "wp-content/plugins/elementor/assets/css/frontend.min.css?ver=3.35.9.css":
        "assets/css/elementor-frontend.min.css",
    "wp-content/plugins/elementor/assets/css/widget-divider.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-divider.min.css",
    "wp-content/plugins/elementor/assets/css/widget-heading.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-heading.min.css",
    "wp-content/plugins/elementor/assets/css/widget-image.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-image.min.css",
    "wp-content/plugins/elementor/assets/css/widget-spacer.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-spacer.min.css",
    "wp-content/plugins/elementor/assets/lib/eicons/css/elementor-icons.min.css?ver=5.47.0.css":
        "assets/css/elementor-icons.min.css",
    "wp-content/plugins/elementor/assets/lib/font-awesome/css/fontawesome.min.css?ver=5.15.3.css":
        "assets/css/font-awesome.min.css",
    "wp-content/plugins/elementor/assets/lib/font-awesome/css/solid.min.css?ver=5.15.3.css":
        "assets/css/font-awesome-solid.min.css",
    "wp-content/plugins/LayerSlider/assets/static/layerslider/css/layerslider.css?ver=6.11.2.css":
        "assets/css/layerslider.css",
    "wp-content/plugins/modulobox/public/assets/css/modulobox.min.css?ver=1.6.0.css":
        "assets/css/modulobox.min.css",
    "wp-content/plugins/responsive-youtube-vimeo-popup/assets/css/wp-video-popup.css?ver=2.10.4.css":
        "assets/css/wp-video-popup.css",
    "wp-content/plugins/revslider/public/assets/css/rs6.css?ver=6.3.3.css":
        "assets/css/revslider.css",
    "wp-content/plugins/uncode-privacy/assets/css/uncode-privacy-public.css?ver=2.1.2.css":
        "assets/css/uncode-privacy.css",
    "wp-content/plugins/youtube-embed-plus/styles/ytprefs.min.css?ver=14.2.5.css":
        "assets/css/ytprefs.min.css",
    # Uncode theme — version 317656103 for this page
    "wp-content/themes/uncode/library/css/style.css?ver=317656103.css":
        "assets/css/uncode-style.css",
    "wp-content/themes/uncode/library/css/style-custom.css?ver=317656103.css":
        "assets/css/uncode-style-custom.css",
    "wp-content/themes/uncode/library/css/uncode-icons.css?ver=317656103.css":
        "assets/css/uncode-icons.css",
    # Elementor per-post CSS
    "wp-content/uploads/elementor/css/post-88080.css?ver=1774473538.css":
        "assets/css/elementor-post-88080.css",
    "wp-content/uploads/elementor/css/post-90433.css?ver=1774480841.css":
        "assets/css/elementor-post-90433.css",
    # Google fonts CSS
    "wp-content/uploads/elementor/google-fonts/css/baskervville.css?ver=1742249244.css":
        "assets/css/font-baskervville.css",
    "wp-content/uploads/elementor/google-fonts/css/librebaskerville.css?ver=1742246368.css":
        "assets/css/font-librebaskerville.css",
    "wp-content/uploads/elementor/google-fonts/css/newscycle.css?ver=1742246368.css":
        "assets/css/font-newscycle.css",
    "wp-content/uploads/elementor/google-fonts/css/roboto.css?ver=1742246370.css":
        "assets/css/font-roboto.css",
    "wp-content/uploads/elementor/google-fonts/css/robotomono.css?ver=1742246371.css":
        "assets/css/font-robotomono.css",

    # JS
    "wp-content/plugins/aweber-web-form-widget/src/js/aweber-wpn-script.js?ver=v7.3.30":
        "assets/js/aweber.js",
    "wp-content/plugins/contact-form-7/includes/js/index.js?ver=6.1.5":
        "assets/js/contact-form-7.js",
    "wp-content/plugins/contact-form-7/includes/swv/js/index.js?ver=6.1.5":
        "assets/js/contact-form-7-swv.js",
    "wp-content/plugins/elementor/assets/js/frontend.min.js?ver=3.35.9":
        "assets/js/elementor-frontend.min.js",
    "wp-content/plugins/elementor/assets/js/frontend-modules.min.js?ver=3.35.9":
        "assets/js/elementor-frontend-modules.min.js",
    "wp-content/plugins/elementor/assets/js/webpack.runtime.min.js?ver=3.35.9":
        "assets/js/elementor-webpack-runtime.min.js",
    "wp-content/plugins/LayerSlider/assets/static/layerslider/js/layerslider.kreaturamedia.jquery.js?ver=6.11.2":
        "assets/js/layerslider-kreaturamedia.jquery.js",
    "wp-content/plugins/LayerSlider/assets/static/layerslider/js/layerslider.transitions.js?ver=6.11.2":
        "assets/js/layerslider-transitions.js",
    "wp-content/plugins/LayerSlider/assets/static/layerslider/js/layerslider.utils.js?ver=6.11.2":
        "assets/js/layerslider-utils.js",
    "wp-content/plugins/modulobox/public/assets/js/modulobox.min.js?ver=1.6.0":
        "assets/js/modulobox.min.js",
    "wp-content/plugins/responsive-youtube-vimeo-popup/assets/js/wp-video-popup.js?ver=2.10.4":
        "assets/js/wp-video-popup.js",
    "wp-content/plugins/revslider/public/assets/js/rbtools.min.js?ver=6.3.3":
        "assets/js/revslider-rbtools.min.js",
    "wp-content/plugins/revslider/public/assets/js/rs6.min.js?ver=6.3.3":
        "assets/js/revslider.min.js",
    "wp-content/plugins/uncode-privacy/assets/js/js-cookie.min.js?ver=2.2.0":
        "assets/js/js-cookie.min.js",
    "wp-content/plugins/uncode-privacy/assets/js/uncode-privacy-public.min.js?ver=2.1.2":
        "assets/js/uncode-privacy.min.js",
    "wp-content/plugins/youtube-embed-plus/scripts/fitvids.min.js?ver=14.2.5":
        "assets/js/fitvids.min.js",
    "wp-content/plugins/youtube-embed-plus/scripts/ytprefs.min.js?ver=14.2.5":
        "assets/js/ytprefs.min.js",
    # Uncode theme JS — version 317656103
    "wp-content/themes/uncode/library/js/app.js?ver=317656103":
        "assets/js/uncode-app.js",
    "wp-content/themes/uncode/library/js/init.js?ver=317656103":
        "assets/js/uncode-init.js",
    "wp-content/themes/uncode/library/js/plugins.js?ver=317656103":
        "assets/js/uncode-plugins.js",
    "wp-includes/js/dist/hooks.min.js?ver=dd5603f07f9220ed27f1":
        "assets/js/wp-hooks.min.js",
    "wp-includes/js/dist/i18n.min.js?ver=c26c3dc7bed366793375":
        "assets/js/wp-i18n.min.js",
    "wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1":
        "assets/js/jquery-migrate.min.js",
    "wp-includes/js/jquery/jquery.min.js?ver=3.7.1":
        "assets/js/jquery.min.js",
    "wp-includes/js/jquery/ui/core.min.js?ver=1.13.3":
        "assets/js/jquery-ui-core.min.js",
    "wp-includes/js/mediaelement/mediaelement-and-player.min.js?ver=4.2.17":
        "assets/js/mediaelement-and-player.min.js",
    "wp-includes/js/mediaelement/mediaelement-migrate.min.js?ver=6.9.4":
        "assets/js/mediaelement-migrate.min.js",
    "wp-includes/js/mediaelement/wp-mediaelement.min.js?ver=6.9.4":
        "assets/js/wp-mediaelement.min.js",

    # Fonts
    "wp-content/plugins/elementor/assets/lib/eicons/fonts/eicons.eot?5.47.0":
        "assets/fonts/eicons.eot",
    "wp-content/plugins/elementor/assets/lib/eicons/fonts/eicons.svg?5.47.0":
        "assets/fonts/eicons.svg",
    "wp-content/plugins/elementor/assets/lib/eicons/fonts/eicons.ttf?5.47.0":
        "assets/fonts/eicons.ttf",
    "wp-content/plugins/elementor/assets/lib/eicons/fonts/eicons.woff?5.47.0":
        "assets/fonts/eicons.woff",
    "wp-content/plugins/elementor/assets/lib/eicons/fonts/eicons.woff2?5.47.0":
        "assets/fonts/eicons.woff2",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-solid-900.eot":
        "assets/fonts/fa-solid-900.eot",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-solid-900.svg":
        "assets/fonts/fa-solid-900.svg",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-solid-900.ttf":
        "assets/fonts/fa-solid-900.ttf",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-solid-900.woff":
        "assets/fonts/fa-solid-900.woff",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-solid-900.woff2":
        "assets/fonts/fa-solid-900.woff2",
    "wp-content/plugins/revslider/public/assets/fonts/revicons/revicons.eot?5510888":
        "assets/fonts/revicons.eot",
    "wp-content/plugins/revslider/public/assets/fonts/revicons/revicons.svg?5510888":
        "assets/fonts/revicons.svg",
    "wp-content/plugins/revslider/public/assets/fonts/revicons/revicons.ttf?5510888":
        "assets/fonts/revicons.ttf",
    "wp-content/plugins/revslider/public/assets/fonts/revicons/revicons.woff?5510888":
        "assets/fonts/revicons.woff",
    "wp-content/themes/uncode/library/fonts/uncode-icons.eot":
        "assets/fonts/uncode-icons.eot",
    "wp-content/themes/uncode/library/fonts/uncode-icons.svg":
        "assets/fonts/uncode-icons.svg",
    "wp-content/themes/uncode/library/fonts/uncode-icons.ttf":
        "assets/fonts/uncode-icons.ttf",
    "wp-content/themes/uncode/library/fonts/uncode-icons.woff":
        "assets/fonts/uncode-icons.woff",
    "wp-content/themes/uncode/library/fonts/uncode-icons.woff2":
        "assets/fonts/uncode-icons.woff2",
}

# Google font woff2 files
GOOGLE_FONTS_SRC = SRC / "wp-content/uploads/elementor/google-fonts/fonts"
for f in GOOGLE_FONTS_SRC.iterdir():
    if f.is_file():
        FILE_MAP[f"wp-content/uploads/elementor/google-fonts/fonts/{f.name}"] = \
            f"assets/fonts/{f.name}"

# Images
FILE_MAP.update({
    "wp-content/plugins/LayerSlider/assets/static/layerslider/img/icon-muted-white.png":
        "assets/img/layerslider-icon-muted-white.png",
    "wp-content/plugins/LayerSlider/assets/static/layerslider/img/icon-unmuted-white.png":
        "assets/img/layerslider-icon-unmuted-white.png",
    "wp-content/plugins/responsive-youtube-vimeo-popup/assets/img/wp-video-popup-close.png":
        "assets/img/wp-video-popup-close.png",
    "wp-content/plugins/revslider/public/assets/assets/coloredbg.png":
        "assets/img/revslider-coloredbg.png",
    "wp-content/plugins/revslider/public/assets/assets/gridtile_3x3_white.png":
        "assets/img/revslider-gridtile_3x3_white.png",
    "wp-content/plugins/revslider/public/assets/assets/gridtile_3x3.png":
        "assets/img/revslider-gridtile_3x3.png",
    "wp-content/plugins/revslider/public/assets/assets/gridtile_white.png":
        "assets/img/revslider-gridtile_white.png",
    "wp-content/plugins/revslider/public/assets/assets/gridtile.png":
        "assets/img/revslider-gridtile.png",
    "wp-content/plugins/revslider/public/assets/assets/loader.gif":
        "assets/img/revslider-loader.gif",
    "wp-content/plugins/revslider/public/assets/css/closedhand.cur":
        "assets/img/revslider-closedhand.cur",
    "wp-content/plugins/revslider/public/assets/css/openhand.cur":
        "assets/img/revslider-openhand.cur",
    "wp-content/themes/uncode/library/img/ilightbox/css/closedhand.cur":
        "assets/img/ilightbox-closedhand.cur",
    "wp-content/themes/uncode/library/img/oval-anim-dark.svg":
        "assets/img/uncode-oval-anim-dark.svg",
    "wp-content/themes/uncode/library/img/oval-anim-light.svg":
        "assets/img/uncode-oval-anim-light.svg",
    "wp-content/themes/uncode/library/img/preloader.svg":
        "assets/img/uncode-preloader.svg",
    "wp-content/uploads/2020/12/cropped-starlingbird_favicon-1-192x192.png":
        "assets/img/favicon-192x192.png",
    "wp-content/uploads/2020/12/cropped-starlingbird_favicon-1-32x32.png":
        "assets/img/favicon-32x32.png",
    "wp-content/uploads/2020/12/cropped-starlingbird_favicon-1-uai-258x258.png":
        "assets/img/favicon-258x258.png",
    "wp-content/uploads/2021/09/GettyImages-1295941207.jpg":
        "assets/img/GettyImages-1295941207.jpg",
})

# ilightbox images
ILIGHTBOX_SRC = SRC / "wp-content/themes/uncode/library/img/ilightbox"
for f in ILIGHTBOX_SRC.rglob("*"):
    if f.is_file():
        rel = f.relative_to(ILIGHTBOX_SRC)
        parts = rel.parts
        if parts[0] == "css":
            continue  # handled above
        prefix = parts[0].replace("-skin", "").replace("_icons", "")
        new_name = f"ilightbox-{prefix}-{parts[-1]}"
        src_key = f"wp-content/themes/uncode/library/img/ilightbox/{'/'.join(parts)}"
        FILE_MAP[src_key] = f"assets/img/{new_name}"

# ---------------------------------------------------------------------------
# CSS url() rewrites (same as anita, plus eot%3F fix for font-awesome)
# ---------------------------------------------------------------------------

CSS_URL_REWRITES = {
    # revslider.css
    "../fonts/revicons/revicons.eot%3F5510888": "../fonts/revicons.eot",
    "../fonts/revicons/revicons.woff%3F5510888": "../fonts/revicons.woff",
    "../fonts/revicons/revicons.ttf%3F5510888": "../fonts/revicons.ttf",
    "../fonts/revicons/revicons.svg%3F5510888": "../fonts/revicons.svg",
    "openhand.cur": "../img/revslider-openhand.cur",
    "closedhand.cur": "../img/revslider-closedhand.cur",
    "../assets/gridtile.png": "../img/revslider-gridtile.png",
    "../assets/gridtile_white.png": "../img/revslider-gridtile_white.png",
    "../assets/gridtile_3x3.png": "../img/revslider-gridtile_3x3.png",
    "../assets/gridtile_3x3_white.png": "../img/revslider-gridtile_3x3_white.png",
    "../assets/coloredbg.png": "../img/revslider-coloredbg.png",
    "../assets/loader.gif": "../img/revslider-loader.gif",
    # layerslider.css
    "../img/icon-muted-white.png": "../img/layerslider-icon-muted-white.png",
    "../img/icon-unmuted-white.png": "../img/layerslider-icon-unmuted-white.png",
    # uncode-style.css
    "../img/preloader.svg": "../img/uncode-preloader.svg",
    "../img/oval-anim-light.svg": "../img/uncode-oval-anim-light.svg",
    "../img/oval-anim-dark.svg": "../img/uncode-oval-anim-dark.svg",
    "../img/ilightbox/css/closedhand.cur": "../img/ilightbox-closedhand.cur",
    "../img/ilightbox/social_icons/facebook_16.png":  "../img/ilightbox-social-facebook_16.png",
    "../img/ilightbox/social_icons/digg_16.png":      "../img/ilightbox-social-digg_16.png",
    "../img/ilightbox/social_icons/twitter_16.png":   "../img/ilightbox-social-twitter_16.png",
    "../img/ilightbox/social_icons/delicious_16.png": "../img/ilightbox-social-delicious_16.png",
    "../img/ilightbox/social_icons/reddit_16.png":    "../img/ilightbox-social-reddit_16.png",
    "../img/ilightbox/social_icons/google_plus_16.png": "../img/ilightbox-social-google_plus_16.png",
    "../img/ilightbox/black-skin/alert.png":              "../img/ilightbox-black-alert.png",
    "../img/ilightbox/black-skin/buttons.png":            "../img/ilightbox-black-buttons.png",
    "../img/ilightbox/black-skin/fullscreen-icon-64.png": "../img/ilightbox-black-fullscreen-icon-64.png",
    "../img/ilightbox/black-skin/fullscreen-icon-ie.png": "../img/ilightbox-black-fullscreen-icon-ie.png",
    "../img/ilightbox/black-skin/x-mark-icon-64.png":    "../img/ilightbox-black-x-mark-icon-64.png",
    "../img/ilightbox/black-skin/x-mark-icon-ie.png":    "../img/ilightbox-black-x-mark-icon-ie.png",
    "../img/ilightbox/black-skin/arrow-next-icon-64.png": "../img/ilightbox-black-arrow-next-icon-64.png",
    "../img/ilightbox/black-skin/arrow-next-icon-ie.png": "../img/ilightbox-black-arrow-next-icon-ie.png",
    "../img/ilightbox/black-skin/arrow-prev-icon-64.png": "../img/ilightbox-black-arrow-prev-icon-64.png",
    "../img/ilightbox/black-skin/arrow-prev-icon-ie.png": "../img/ilightbox-black-arrow-prev-icon-ie.png",
    "../img/ilightbox/black-skin/play-icon-64.png":  "../img/ilightbox-black-play-icon-64.png",
    "../img/ilightbox/black-skin/play-icon-ie.png":  "../img/ilightbox-black-play-icon-ie.png",
    "../img/ilightbox/black-skin/pause-icon-64.png": "../img/ilightbox-black-pause-icon-64.png",
    "../img/ilightbox/black-skin/pause-icon-ie.png": "../img/ilightbox-black-pause-icon-ie.png",
    "../img/ilightbox/black-skin/thumb-overlay-play.png": "../img/ilightbox-black-thumb-overlay-play.png",
    "../img/ilightbox/black-skin/arrows_vertical.png":   "../img/ilightbox-black-arrows_vertical.png",
    "../img/ilightbox/black-skin/arrows_horizontal.png": "../img/ilightbox-black-arrows_horizontal.png",
    "../img/ilightbox/white-skin/alert.png":              "../img/ilightbox-white-alert.png",
    "../img/ilightbox/white-skin/buttons.png":            "../img/ilightbox-white-buttons.png",
    "../img/ilightbox/white-skin/fullscreen-icon-64.png": "../img/ilightbox-white-fullscreen-icon-64.png",
    "../img/ilightbox/white-skin/fullscreen-icon-ie.png": "../img/ilightbox-white-fullscreen-icon-ie.png",
    "../img/ilightbox/white-skin/x-mark-icon-64.png":    "../img/ilightbox-white-x-mark-icon-64.png",
    "../img/ilightbox/white-skin/x-mark-icon-ie.png":    "../img/ilightbox-white-x-mark-icon-ie.png",
    "../img/ilightbox/white-skin/arrow-next-icon-64.png": "../img/ilightbox-white-arrow-next-icon-64.png",
    "../img/ilightbox/white-skin/arrow-next-icon-ie.png": "../img/ilightbox-white-arrow-next-icon-ie.png",
    "../img/ilightbox/white-skin/arrow-prev-icon-64.png": "../img/ilightbox-white-arrow-prev-icon-64.png",
    "../img/ilightbox/white-skin/arrow-prev-icon-ie.png": "../img/ilightbox-white-arrow-prev-icon-ie.png",
    "../img/ilightbox/white-skin/play-icon-64.png":  "../img/ilightbox-white-play-icon-64.png",
    "../img/ilightbox/white-skin/play-icon-ie.png":  "../img/ilightbox-white-play-icon-ie.png",
    "../img/ilightbox/white-skin/pause-icon-64.png": "../img/ilightbox-white-pause-icon-64.png",
    "../img/ilightbox/white-skin/pause-icon-ie.png": "../img/ilightbox-white-pause-icon-ie.png",
    "../img/ilightbox/white-skin/thumb-overlay-play.png": "../img/ilightbox-white-thumb-overlay-play.png",
    "../img/ilightbox/white-skin/arrows_vertical.png":   "../img/ilightbox-white-arrows_vertical.png",
    "../img/ilightbox/white-skin/arrows_horizontal.png": "../img/ilightbox-white-arrows_horizontal.png",
    # elementor-icons.min.css
    "../fonts/eicons.eot%3F5.47.0":   "../fonts/eicons.eot",
    "../fonts/eicons.woff2%3F5.47.0": "../fonts/eicons.woff2",
    "../fonts/eicons.woff%3F5.47.0":  "../fonts/eicons.woff",
    "../fonts/eicons.ttf%3F5.47.0":   "../fonts/eicons.ttf",
    "../fonts/eicons.svg%3F5.47.0":   "../fonts/eicons.svg",
    # font-awesome: webfonts/ → fonts/, both with and without %3F
    "../webfonts/fa-solid-900.eot":    "../fonts/fa-solid-900.eot",
    "../webfonts/fa-solid-900.eot%3F": "../fonts/fa-solid-900.eot",
    "../webfonts/fa-solid-900.woff2":  "../fonts/fa-solid-900.woff2",
    "../webfonts/fa-solid-900.woff":   "../fonts/fa-solid-900.woff",
    "../webfonts/fa-solid-900.ttf":    "../fonts/fa-solid-900.ttf",
    "../webfonts/fa-solid-900.svg":    "../fonts/fa-solid-900.svg",
    # uncode-icons.css
    "../fonts/uncode-icons.eot%3F": "../fonts/uncode-icons.eot",
}

# ---------------------------------------------------------------------------
# HTML rewrites
# ---------------------------------------------------------------------------

def build_html_rewrites():
    rewrites = {}
    for old_key, new_dst in FILE_MAP.items():
        if old_key == "what-to-get-right-first/index.html":
            continue
        html_url = "../" + old_key.replace("?", "%3F")
        rewrites[html_url] = new_dst
    return rewrites


def apply_rewrites(text, rewrites):
    for old, new in rewrites.items():
        text = text.replace(old, new)
    return text


def apply_css_url_rewrites(text):
    for old, new in CSS_URL_REWRITES.items():
        text = text.replace(f"url({old})", f"url({new})")
        text = text.replace(f"url('{old}')", f"url('{new}')")
        text = text.replace(f'url("{old}")', f'url("{new}")')
    return text


def main():
    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir()

    html_rewrites = build_html_rewrites()

    copied = 0
    skipped = 0

    for old_key, new_dst in FILE_MAP.items():
        src_path = SRC / old_key
        dst_path = DST / new_dst

        if not src_path.exists():
            print(f"  MISSING: {old_key}")
            skipped += 1
            continue

        dst_path.parent.mkdir(parents=True, exist_ok=True)

        ext = src_path.suffix.lower().lstrip(".")
        is_text = ext in ("html", "css", "js", "svg", "txt")

        if is_text:
            text = src_path.read_text(encoding="utf-8", errors="replace")
            if new_dst == "index.html":
                text = apply_rewrites(text, html_rewrites)
            if new_dst.startswith("assets/css/"):
                text = apply_css_url_rewrites(text)
            dst_path.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(src_path, dst_path)

        copied += 1

    print(f"\nDone: {copied} files copied, {skipped} missing.")
    print(f"Output: {DST.resolve()}")

    print("\nOutput structure:")
    for d in sorted({str(Path(v).parent) for v in FILE_MAP.values()}):
        count = sum(1 for v in FILE_MAP.values() if str(Path(v).parent) == d)
        print(f"  {d}/  ({count} files)")


if __name__ == "__main__":
    main()
