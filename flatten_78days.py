#!/usr/bin/env python3
"""
Flatten the wget mirror of starlinglab.org/78days/ (and its 10 subpages)
into a flat static bundle.

Structure:
  78days/
    index.html                        (main 78days page)
    background/index.html
    challenges/index.html
    image-authentication/index.html
    reflections/index.html
    78daysarchive/index.html
    78daysarchive-mobile/index.html
    78days-archive-mobile-day-4/index.html
    78days-archive-mobile-transition/index.html
    78days-archive-mobile-insurrection/index.html
    78days-archive-mobile-inauguration/index.html
    assets/css/
    assets/js/
    assets/fonts/
    assets/img/
"""

import shutil
from pathlib import Path

SRC = Path("mirror/www.starlinglab.org")
DST = Path("78days")

# ---------------------------------------------------------------------------
# Pages: slug → (mirror_path, uncode_ver, post_css_id, post_css_ver)
# ---------------------------------------------------------------------------

PAGES = {
    # slug: (mirror slug, uncode version, post CSS id, post CSS ver)
    ".":                               ("78days",                          "1410911637", "88698", "1774475092"),
    "background":                      ("background",                      "183496954",  "88364", "1774479312"),
    "challenges":                      ("challenges",                      "1166474385", "88394", "1774488826"),
    "image-authentication":            ("image-authentication",            "1194263210", "88384", "1774479006"),
    "reflections":                     ("reflections",                     "1958034209", "90160", "1774516482"),
    "78daysarchive":                   ("78daysarchive",                   "1635830251", "88817", "1774496542"),
    "78daysarchive-mobile":            ("78daysarchive-mobile",            "552854975",  "89846", "1774516547"),
    "78days-archive-mobile-day-4":     ("78days-archive-mobile-day-4",     "939656386",  "89857", "1774516568"),
    "78days-archive-mobile-transition":("78days-archive-mobile-transition","22406702",   "89871", "1774499016"),
    "78days-archive-mobile-insurrection":("78days-archive-mobile-insurrection","1599767571","89879","1774516649"),
    "78days-archive-mobile-inauguration":("78days-archive-mobile-inauguration","820923414","89887","1774516657"),
    "reflections-authenticity-and-equity":        ("reflections-authenticity-and-equity",        "1242792185","90139","1774517741"),
    "reflections-does-authenticity-guarantee-access":("reflections-does-authenticity-guarantee-access","1275372932","90149","1774517766"),
    "reflections-trust-or-complacency":           ("reflections-trust-or-complacency",           "1237187491","90147","1774517774"),
}

# Shared elementor post CSS (post-88080 appears on every page)
SHARED_POST_CSS_VER = "1774473538"

# ---------------------------------------------------------------------------
# Shared asset FILE_MAP (disk path → dst path, relative to DST)
# ---------------------------------------------------------------------------

SHARED_ASSETS = {
    # --- Shared Elementor post CSS ---
    f"wp-content/uploads/elementor/css/post-88080.css?ver={SHARED_POST_CSS_VER}.css":
        "assets/css/elementor-post-88080.css",

    # --- Elementor plugin CSS ---
    "wp-content/plugins/elementor/assets/css/frontend.min.css?ver=3.35.9.css":
        "assets/css/elementor-frontend.min.css",
    "wp-content/plugins/elementor/assets/css/widget-divider.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-divider.min.css",
    "wp-content/plugins/elementor/assets/css/widget-heading.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-heading.min.css",
    "wp-content/plugins/elementor/assets/css/widget-icon-box.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-icon-box.min.css",
    "wp-content/plugins/elementor/assets/css/widget-icon-list.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-icon-list.min.css",
    "wp-content/plugins/elementor/assets/css/widget-image.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-image.min.css",
    "wp-content/plugins/elementor/assets/css/widget-menu-anchor.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-menu-anchor.min.css",
    "wp-content/plugins/elementor/assets/css/widget-spacer.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-spacer.min.css",
    "wp-content/plugins/elementor/assets/css/widget-text-editor.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-text-editor.min.css",
    "wp-content/plugins/elementor/assets/css/widget-video.min.css?ver=3.35.9.css":
        "assets/css/elementor-widget-video.min.css",
    # Elementor animations
    "wp-content/plugins/elementor/assets/lib/animations/styles/e-animation-grow.min.css?ver=3.35.9.css":
        "assets/css/elementor-animation-grow.min.css",
    "wp-content/plugins/elementor/assets/lib/animations/styles/e-animation-shrink.min.css?ver=3.35.9.css":
        "assets/css/elementor-animation-shrink.min.css",
    "wp-content/plugins/elementor/assets/lib/animations/styles/fadeIn.min.css?ver=3.35.9.css":
        "assets/css/elementor-animation-fadeIn.min.css",
    "wp-content/plugins/elementor/assets/lib/animations/styles/fadeInUp.min.css?ver=3.35.9.css":
        "assets/css/elementor-animation-fadeInUp.min.css",
    # Elementor icons
    "wp-content/plugins/elementor/assets/lib/eicons/css/elementor-icons.min.css?ver=5.47.0.css":
        "assets/css/elementor-icons.min.css",
    # Font Awesome
    "wp-content/plugins/elementor/assets/lib/font-awesome/css/fontawesome.min.css?ver=5.15.3.css":
        "assets/css/font-awesome.min.css",
    "wp-content/plugins/elementor/assets/lib/font-awesome/css/solid.min.css?ver=5.15.3.css":
        "assets/css/font-awesome-solid.min.css",
    "wp-content/plugins/elementor/assets/lib/font-awesome/css/brands.min.css?ver=5.15.3.css":
        "assets/css/font-awesome-brands.min.css",
    "wp-content/plugins/elementor/assets/lib/font-awesome/css/regular.min.css?ver=5.15.3.css":
        "assets/css/font-awesome-regular.min.css",
    # Other plugin CSS
    "wp-content/plugins/contact-form-7/includes/css/styles.css?ver=6.1.5.css":
        "assets/css/contact-form-7.css",
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

    # --- JS ---
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

    # --- Fonts ---
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
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-brands-400.eot":
        "assets/fonts/fa-brands-400.eot",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-brands-400.svg":
        "assets/fonts/fa-brands-400.svg",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-brands-400.ttf":
        "assets/fonts/fa-brands-400.ttf",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-brands-400.woff":
        "assets/fonts/fa-brands-400.woff",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-brands-400.woff2":
        "assets/fonts/fa-brands-400.woff2",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-regular-400.eot":
        "assets/fonts/fa-regular-400.eot",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-regular-400.svg":
        "assets/fonts/fa-regular-400.svg",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-regular-400.ttf":
        "assets/fonts/fa-regular-400.ttf",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-regular-400.woff":
        "assets/fonts/fa-regular-400.woff",
    "wp-content/plugins/elementor/assets/lib/font-awesome/webfonts/fa-regular-400.woff2":
        "assets/fonts/fa-regular-400.woff2",
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

    # --- Images ---
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
    # Content images
    "wp-content/uploads/2017/01/2021-01-20T205544Z_214090672_RC2WBL934CDH_RTRMADP_3_USA-BIDEN-INAUGURATION-cai-uai-258x173.jpg":
        "assets/img/inauguration-cai-258x173.jpg",
    "wp-content/uploads/2017/01/2021-01-20T205544Z_214090672_RC2WBL934CDH_RTRMADP_3_USA-BIDEN-INAUGURATION-cai2-uai-258x173.jpg":
        "assets/img/inauguration-cai2-258x173.jpg",
    "wp-content/uploads/2020/05/Stanford_Engineering.svg":
        "assets/img/Stanford_Engineering.svg",
    "wp-content/uploads/2020/05/Starling_Logo_white.png":
        "assets/img/Starling_Logo_white.png",
    "wp-content/uploads/2020/05/USC_SFI_transparent.svg":
        "assets/img/USC_SFI_transparent.svg",
    "wp-content/uploads/2021/01/CAI_claimdiagram-1024x722.png":
        "assets/img/CAI_claimdiagram-1024x722.png",
    "wp-content/uploads/2021/02/challenge1_caioverlay_2.png":
        "assets/img/challenge1_caioverlay_2.png",
    "wp-content/uploads/2021/02/challenge2_caioverlay_updated.png":
        "assets/img/challenge2_caioverlay_updated.png",
    "wp-content/uploads/2021/02/challenge3_caioverlay.png":
        "assets/img/challenge3_caioverlay.png",
    "wp-content/uploads/2021/02/deepfake.gif":
        "assets/img/deepfake.gif",
    "wp-content/uploads/2021/02/ezgif.com-gif-maker-3.gif":
        "assets/img/ezgif.com-gif-maker-3.gif",
    "wp-content/uploads/2021/02/homepageheader_dates3.svg":
        "assets/img/homepageheader_dates3.svg",
    "wp-content/uploads/2021/02/IA_diagram_base2.png":
        "assets/img/IA_diagram_base2.png",
    "wp-content/uploads/2021/02/IA_diagram_full2-1024x535.png":
        "assets/img/IA_diagram_full2-1024x535.png",
    "wp-content/uploads/2021/02/IA_diagram_Original.png":
        "assets/img/IA_diagram_Original.png",
    "wp-content/uploads/2021/02/reuterscasestudyvideo_thumb.jpg":
        "assets/img/reuterscasestudyvideo_thumb.jpg",
    "wp-content/uploads/2021/02/Reuterslogo_white.png":
        "assets/img/Reuterslogo_white.png",
    "wp-content/uploads/2021/02/Screen-Shot-2021-02-01-at-1.03.27-AM-e1612229965111.png":
        "assets/img/Screen-Shot-2021-02-01.png",
    "wp-content/uploads/2021/02/stanford_logo_white.svg":
        "assets/img/stanford_logo_white.svg",
    "wp-content/uploads/2021/02/starlinglogo_full_white_80-scaled.jpg":
        "assets/img/starlinglogo_full_white_80-scaled.jpg",
    "wp-content/uploads/2021/02/usc_logo_white.svg":
        "assets/img/usc_logo_white.svg",
    "wp-content/uploads/elementor/thumbs/arrow-p26zuil5f20m6biv3syv3ycm6ajeics9xg1mp7aa10.png":
        "assets/img/elementor-arrow-thumb.png",
}

# Add google font woff2 files
GOOGLE_FONTS_SRC = SRC / "wp-content/uploads/elementor/google-fonts/fonts"
for f in GOOGLE_FONTS_SRC.iterdir():
    if f.is_file():
        SHARED_ASSETS[f"wp-content/uploads/elementor/google-fonts/fonts/{f.name}"] = \
            f"assets/fonts/{f.name}"

# Add ilightbox images
ILIGHTBOX_SRC = SRC / "wp-content/themes/uncode/library/img/ilightbox"
for f in ILIGHTBOX_SRC.rglob("*"):
    if f.is_file():
        rel = f.relative_to(ILIGHTBOX_SRC)
        parts = rel.parts
        if parts[0] == "css":
            continue  # closedhand.cur handled above
        prefix = parts[0].replace("-skin", "").replace("_icons", "")
        new_name = f"ilightbox-{prefix}-{parts[-1]}"
        src_key = f"wp-content/themes/uncode/library/img/ilightbox/{'/'.join(parts)}"
        SHARED_ASSETS[src_key] = f"assets/img/{new_name}"

# ---------------------------------------------------------------------------
# CSS url() rewrites (applied to all CSS files)
# ---------------------------------------------------------------------------

CSS_URL_REWRITES = {
    # revslider.css
    "../fonts/revicons/revicons.eot%3F5510888": "../fonts/revicons.eot",
    "../fonts/revicons/revicons.woff%3F5510888": "../fonts/revicons.woff",
    "../fonts/revicons/revicons.ttf%3F5510888":  "../fonts/revicons.ttf",
    "../fonts/revicons/revicons.svg%3F5510888":  "../fonts/revicons.svg",
    "openhand.cur":  "../img/revslider-openhand.cur",
    "closedhand.cur": "../img/revslider-closedhand.cur",
    "../assets/gridtile.png":          "../img/revslider-gridtile.png",
    "../assets/gridtile_white.png":    "../img/revslider-gridtile_white.png",
    "../assets/gridtile_3x3.png":      "../img/revslider-gridtile_3x3.png",
    "../assets/gridtile_3x3_white.png":"../img/revslider-gridtile_3x3_white.png",
    "../assets/coloredbg.png":         "../img/revslider-coloredbg.png",
    "../assets/loader.gif":            "../img/revslider-loader.gif",
    # layerslider.css
    "../img/icon-muted-white.png":   "../img/layerslider-icon-muted-white.png",
    "../img/icon-unmuted-white.png": "../img/layerslider-icon-unmuted-white.png",
    # uncode-style.css
    "../img/preloader.svg":          "../img/uncode-preloader.svg",
    "../img/oval-anim-light.svg":    "../img/uncode-oval-anim-light.svg",
    "../img/oval-anim-dark.svg":     "../img/uncode-oval-anim-dark.svg",
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
    # elementor-icons.min.css: strip query strings
    "../fonts/eicons.eot%3F5.47.0":   "../fonts/eicons.eot",
    "../fonts/eicons.woff2%3F5.47.0": "../fonts/eicons.woff2",
    "../fonts/eicons.woff%3F5.47.0":  "../fonts/eicons.woff",
    "../fonts/eicons.ttf%3F5.47.0":   "../fonts/eicons.ttf",
    "../fonts/eicons.svg%3F5.47.0":   "../fonts/eicons.svg",
    # font-awesome: webfonts/ → fonts/
    "../webfonts/fa-solid-900.eot":    "../fonts/fa-solid-900.eot",
    "../webfonts/fa-solid-900.eot%3F": "../fonts/fa-solid-900.eot",
    "../webfonts/fa-solid-900.woff2":  "../fonts/fa-solid-900.woff2",
    "../webfonts/fa-solid-900.woff":   "../fonts/fa-solid-900.woff",
    "../webfonts/fa-solid-900.ttf":    "../fonts/fa-solid-900.ttf",
    "../webfonts/fa-solid-900.svg":    "../fonts/fa-solid-900.svg",
    "../webfonts/fa-brands-400.eot":    "../fonts/fa-brands-400.eot",
    "../webfonts/fa-brands-400.eot%3F": "../fonts/fa-brands-400.eot",
    "../webfonts/fa-brands-400.woff2":  "../fonts/fa-brands-400.woff2",
    "../webfonts/fa-brands-400.woff":   "../fonts/fa-brands-400.woff",
    "../webfonts/fa-brands-400.ttf":    "../fonts/fa-brands-400.ttf",
    "../webfonts/fa-brands-400.svg":    "../fonts/fa-brands-400.svg",
    "../webfonts/fa-regular-400.eot":    "../fonts/fa-regular-400.eot",
    "../webfonts/fa-regular-400.eot%3F": "../fonts/fa-regular-400.eot",
    "../webfonts/fa-regular-400.woff2":  "../fonts/fa-regular-400.woff2",
    "../webfonts/fa-regular-400.woff":   "../fonts/fa-regular-400.woff",
    "../webfonts/fa-regular-400.ttf":    "../fonts/fa-regular-400.ttf",
    "../webfonts/fa-regular-400.svg":    "../fonts/fa-regular-400.svg",
    # uncode-icons.css: strip bare ? query marker
    "../fonts/uncode-icons.eot%3F": "../fonts/uncode-icons.eot",
}

# ---------------------------------------------------------------------------
# Internal nav link rewrites
# Pages in this project that link to each other via absolute URLs.
# root_prefix: used from index.html (no leading ../)
# sub_prefix:  used from subpage HTML (adds ../)
# ---------------------------------------------------------------------------

INTERNAL_PAGES = [
    "78days",
    "background",
    "challenges",
    "image-authentication",
    "reflections",
    "78daysarchive",
    "78daysarchive-mobile",
    "78days-archive-mobile-day-4",
    "78days-archive-mobile-transition",
    "78days-archive-mobile-insurrection",
    "78days-archive-mobile-inauguration",
    "reflections-authenticity-and-equity",
    "reflections-does-authenticity-guarantee-access",
    "reflections-trust-or-complacency",
]

def internal_link_rewrites(is_root: bool) -> dict:
    """Build absolute→relative rewrites for internal navigation links."""
    prefix = "" if is_root else "../"
    rewrites = {}
    for slug in INTERNAL_PAGES:
        if slug == "78days":
            dst = f"{prefix}index.html" if not is_root else "index.html"
        else:
            dst = f"{prefix}{slug}/"
        rewrites[f"https://www.starlinglab.org/{slug}/"] = dst
        rewrites[f"https://www.starlinglab.org/{slug}"] = dst  # no trailing slash variant
    return rewrites

# ---------------------------------------------------------------------------
# Helper: build full rewrite map for a given page's HTML
# ---------------------------------------------------------------------------

def build_html_rewrites(slug: str, uncode_ver: str, post_id: str, post_ver: str) -> dict:
    is_root = (slug == ".")
    asset_prefix = "" if is_root else "../"

    rewrites = {}

    # 1. Shared assets: ../wp-content/... → {prefix}assets/...
    for old_key, new_dst in SHARED_ASSETS.items():
        html_url = "../" + old_key.replace("?", "%3F")
        rewrites[html_url] = f"{asset_prefix}{new_dst}"

    # 2. Per-page uncode CSS (3 files × 11 versions)
    page_label = slug if slug != "." else "78days"
    for css_name, flat_name in [
        ("style.css",        f"assets/css/uncode-style-{page_label}.css"),
        ("style-custom.css", f"assets/css/uncode-style-custom-{page_label}.css"),
        ("uncode-icons.css", f"assets/css/uncode-icons-{page_label}.css"),
    ]:
        old_key = f"../wp-content/themes/uncode/library/css/{css_name}%3Fver={uncode_ver}.css"
        rewrites[old_key] = f"{asset_prefix}{flat_name}"

    # 3. Per-page uncode JS (3 files × 11 versions)
    for js_name, flat_name in [
        ("app.js",     f"assets/js/uncode-app-{page_label}.js"),
        ("init.js",    f"assets/js/uncode-init-{page_label}.js"),
        ("plugins.js", f"assets/js/uncode-plugins-{page_label}.js"),
    ]:
        old_key = f"../wp-content/themes/uncode/library/js/{js_name}%3Fver={uncode_ver}"
        rewrites[old_key] = f"{asset_prefix}{flat_name}"

    # 4. Per-page elementor post CSS
    old_key = f"../wp-content/uploads/elementor/css/post-{post_id}.css%3Fver={post_ver}.css"
    rewrites[old_key] = f"{asset_prefix}assets/css/elementor-post-{post_id}.css"

    # 5. Internal navigation links
    rewrites.update(internal_link_rewrites(is_root))

    return rewrites


def apply_rewrites(text: str, rewrites: dict) -> str:
    # Apply longest keys first to prevent shorter keys from partially matching
    # substrings of longer keys (e.g. "78days" matching "78daysarchive-mobile").
    for old in sorted(rewrites, key=len, reverse=True):
        text = text.replace(old, rewrites[old])
    return text


def apply_css_url_rewrites(text: str) -> str:
    for old, new in CSS_URL_REWRITES.items():
        text = text.replace(f"url({old})", f"url({new})")
        text = text.replace(f"url('{old}')", f"url('{new}')")
        text = text.replace(f'url("{old}")', f'url("{new}")')
    return text


# ---------------------------------------------------------------------------
# Per-page uncode CSS/JS FILE_MAP entries
# ---------------------------------------------------------------------------

def per_page_assets() -> dict:
    assets = {}
    for slug, (mirror_slug, uncode_ver, post_id, post_ver) in PAGES.items():
        page_label = slug if slug != "." else "78days"
        # Uncode CSS
        for css_name, flat_name in [
            ("style.css",        f"assets/css/uncode-style-{page_label}.css"),
            ("style-custom.css", f"assets/css/uncode-style-custom-{page_label}.css"),
            ("uncode-icons.css", f"assets/css/uncode-icons-{page_label}.css"),
        ]:
            src_key = f"wp-content/themes/uncode/library/css/{css_name}?ver={uncode_ver}.css"
            assets[src_key] = flat_name
        # Uncode JS
        for js_name, flat_name in [
            ("app.js",     f"assets/js/uncode-app-{page_label}.js"),
            ("init.js",    f"assets/js/uncode-init-{page_label}.js"),
            ("plugins.js", f"assets/js/uncode-plugins-{page_label}.js"),
        ]:
            src_key = f"wp-content/themes/uncode/library/js/{js_name}?ver={uncode_ver}"
            assets[src_key] = flat_name
        # Per-page elementor post CSS
        src_key = f"wp-content/uploads/elementor/css/post-{post_id}.css?ver={post_ver}.css"
        assets[src_key] = f"assets/css/elementor-post-{post_id}.css"
    return assets


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir()

    pp_assets = per_page_assets()
    copied = 0
    skipped = 0

    # --- Copy shared assets (CSS, JS, fonts, images) ---
    for old_key, new_dst in {**SHARED_ASSETS, **pp_assets}.items():
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
            if new_dst.startswith("assets/css/"):
                text = apply_css_url_rewrites(text)
            dst_path.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(src_path, dst_path)
        copied += 1

    # --- Copy and rewrite each page's HTML ---
    for slug, (mirror_slug, uncode_ver, post_id, post_ver) in PAGES.items():
        src_html = SRC / mirror_slug / "index.html"
        dst_html = DST / ("index.html" if slug == "." else f"{slug}/index.html")

        if not src_html.exists():
            print(f"  MISSING HTML: {mirror_slug}/index.html")
            skipped += 1
            continue

        dst_html.parent.mkdir(parents=True, exist_ok=True)
        rewrites = build_html_rewrites(slug, uncode_ver, post_id, post_ver)
        text = src_html.read_text(encoding="utf-8", errors="replace")
        text = apply_rewrites(text, rewrites)
        dst_html.write_text(text, encoding="utf-8")
        print(f"  HTML: {dst_html}")
        copied += 1

    print(f"\nDone: {copied} files copied, {skipped} missing.")
    print(f"Output: {DST.resolve()}")

    print("\nOutput structure:")
    all_dsts = list(SHARED_ASSETS.values()) + list(pp_assets.values())
    for d in sorted({str(Path(v).parent) for v in all_dsts}):
        count = sum(1 for v in all_dsts if str(Path(v).parent) == d)
        print(f"  {d}/  ({count} files)")
    print(f"  [HTML pages: {len(PAGES)}]")


if __name__ == "__main__":
    main()
