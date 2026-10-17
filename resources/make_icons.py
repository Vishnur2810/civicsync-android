"""Generate CivicSync launcher icons and splash screens into the Capacitor Android project.

Usage: python make_icons.py android/app/src/main/res
"""
import io
import struct
import sys
from pathlib import Path

import cairosvg
from PIL import Image

RES = Path(sys.argv[1])
BLUE, VIOLET, NAVY = "#0a84ff", "#6f4fd8", "#0b1d2a"

# White map pin with a check, drawn in a 108x108 adaptive-icon canvas (safe zone = central 66)
PIN = """
<path d="M54 25c-11.6 0-21 9.1-21 20.4C33 60.4 54 77 54 77s21-16.6 21-31.6C75 34.1 65.6 25 54 25z" fill="#fff"/>
<circle cx="54" cy="45.5" r="10.5" fill="{blue}"/>
<path d="M49.2 45.8l3.4 3.4 6.6-6.8" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
""".format(blue=BLUE)
GRAD = f"""<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient></defs>"""


def svg(body, size=108):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">{body}</svg>'


def render(markup, px):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=markup.encode(), output_width=px, output_height=px))).convert("RGBA")


DENSITY = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}

foreground = svg(PIN)
legacy = svg(GRAD + '<rect x="4" y="4" width="100" height="100" rx="26" fill="url(#bg)"/><g transform="translate(54 51) scale(1.25) translate(-54 -51)">' + PIN + "</g>")
round_ = svg(GRAD + '<circle cx="54" cy="54" r="50" fill="url(#bg)"/><g transform="translate(54 51) scale(1.2) translate(-54 -51)">' + PIN + "</g>")

for name, scale in DENSITY.items():
    folder = RES / f"mipmap-{name}"
    folder.mkdir(parents=True, exist_ok=True)
    render(foreground, round(108 * scale)).save(folder / "ic_launcher_foreground.png")
    render(legacy, round(48 * scale)).save(folder / "ic_launcher.png")
    render(round_, round(48 * scale)).save(folder / "ic_launcher_round.png")

# Adaptive icon: gradient background drawable + white pin foreground
(RES / "drawable").mkdir(exist_ok=True)
(RES / "drawable" / "ic_launcher_bg.xml").write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient android:angle="315" android:startColor="{BLUE}" android:endColor="{VIOLET}" />
</shape>
""")
for name in ("ic_launcher.xml", "ic_launcher_round.xml"):
    (RES / "mipmap-anydpi-v26" / name).write_text("""<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_bg"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
""")

# Splash screens: brand gradient with the icon in the middle, at each existing splash size
mark = render(round_, 512)
for path in RES.glob("drawable*/splash.png"):
    w, h = struct.unpack(">II", path.read_bytes()[16:24])
    bg = render(svg(GRAD + '<rect width="108" height="108" fill="url(#bg)"/>'), max(w, h)).crop(
        ((max(w, h) - w) // 2, (max(w, h) - h) // 2, (max(w, h) - w) // 2 + w, (max(w, h) - h) // 2 + h)
    )
    size = round(min(w, h) * 0.28)
    icon = render(svg(PIN), size * 2)  # pin only, on the gradient
    bg.alpha_composite(icon, ((w - size * 2) // 2, (h - size * 2) // 2))
    bg.convert("RGB").save(path)

print("icons and splash screens written to", RES)
