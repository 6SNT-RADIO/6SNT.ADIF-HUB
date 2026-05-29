"""Generate the 6SNT.ADIF-HUB tactical app icon (.ico) and browser favicons.

Aesthetic: Obsidian Tactical — obsidian chassis, emerald frame, cyan broadcast
waves, an emerald "6S" monogram and a small amber telemetry LED.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
S = 1024  # supersampled master size

# Brand tokens
CHASSIS_TOP = (10, 14, 23)  # #0a0e17
CHASSIS_BOT = (5, 8, 12)  # #05080c
EMERALD = (16, 185, 129)  # #10b981
EMERALD_BRIGHT = (84, 224, 131)  # #54e083
CYAN = (101, 212, 249)  # #65d4f9
AMBER = (255, 186, 56)  # #ffba38


def _gradient(size: int) -> Image.Image:
    grad = Image.new("RGBA", (size, size))
    px = grad.load()
    for y in range(size):
        t = y / size
        r = int(CHASSIS_TOP[0] + (CHASSIS_BOT[0] - CHASSIS_TOP[0]) * t)
        g = int(CHASSIS_TOP[1] + (CHASSIS_BOT[1] - CHASSIS_TOP[1]) * t)
        b = int(CHASSIS_TOP[2] + (CHASSIS_BOT[2] - CHASSIS_TOP[2]) * t)
        for x in range(size):
            px[x, y] = (r, g, b, 255)
    return grad


def _glow(layer: Image.Image, radius: int) -> Image.Image:
    return layer.filter(ImageFilter.GaussianBlur(radius))


def build_master() -> Image.Image:
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    margin = int(S * 0.055)
    radius = int(S * 0.11)
    box = [margin, margin, S - margin, S - margin]

    # Chassis (gradient clipped to rounded square)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=radius, fill=255)
    img.paste(_gradient(S), (0, 0), mask)

    draw = ImageDraw.Draw(img)

    # Broadcast waves (cyan arcs) emanating from the upper-right node
    node = (int(S * 0.70), int(S * 0.34))
    for i, rad in enumerate((int(S * 0.10), int(S * 0.17), int(S * 0.24))):
        alpha = 235 - i * 70
        bbox = [node[0] - rad, node[1] - rad, node[0] + rad, node[1] + rad]
        draw.arc(bbox, start=150, end=300, fill=(*CYAN, alpha), width=int(S * 0.022))
    draw.ellipse(
        [node[0] - int(S * 0.018)] * 1
        + [node[1] - int(S * 0.018)]
        + [node[0] + int(S * 0.018), node[1] + int(S * 0.018)],
        fill=(*CYAN, 255),
    )

    # Emerald monogram "6S" with glow
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", int(S * 0.46))
    except OSError:
        font = ImageFont.load_default()
    text = "6S"
    glyph = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glyph)
    tb = gd.textbbox((0, 0), text, font=font)
    tx = (S - (tb[2] - tb[0])) / 2 - tb[0]
    ty = S * 0.50 - (tb[3] - tb[1]) / 2 - tb[1]
    gd.text((tx, ty), text, font=font, fill=(*EMERALD_BRIGHT, 255))
    img.alpha_composite(_glow(glyph, int(S * 0.012)))
    img.alpha_composite(glyph)

    # Amber telemetry LED (bottom-left interior) with glow
    led = (int(S * 0.30), int(S * 0.74))
    lr = int(S * 0.028)
    led_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(led_layer).ellipse(
        [led[0] - lr, led[1] - lr, led[0] + lr, led[1] + lr], fill=(*AMBER, 255)
    )
    img.alpha_composite(_glow(led_layer, int(S * 0.02)))
    img.alpha_composite(led_layer)

    # Emerald hardware frame (drawn last so it stays crisp on top)
    bw = int(S * 0.020)
    draw.rounded_rectangle(box, radius=radius, outline=(*EMERALD, 255), width=bw)
    inset = int(bw * 1.7)
    draw.rounded_rectangle(
        [box[0] + inset, box[1] + inset, box[2] - inset, box[3] - inset],
        radius=max(2, radius - inset),
        outline=(*EMERALD_BRIGHT, 150),
        width=max(1, bw // 3),
    )
    return img


def main() -> None:
    master = build_master()
    branding = ROOT / "branding"
    branding.mkdir(exist_ok=True)
    public = ROOT / "frontend" / "public"
    public.mkdir(parents=True, exist_ok=True)

    sizes = [256, 128, 64, 48, 32, 16]
    ico_imgs = [master.resize((s, s), Image.LANCZOS) for s in sizes]

    ico_path = branding / "6snt-icon.ico"
    ico_imgs[0].save(ico_path, format="ICO", sizes=[(s, s) for s in sizes])
    master.resize((512, 512), Image.LANCZOS).save(branding / "6snt-icon.png")

    # Browser favicons
    ico_imgs[0].save(public / "favicon.ico", format="ICO", sizes=[(s, s) for s in sizes])
    master.resize((180, 180), Image.LANCZOS).save(public / "apple-touch-icon.png")
    master.resize((32, 32), Image.LANCZOS).save(public / "favicon-32.png")

    print(f"icon  -> {ico_path}")
    print(f"png   -> {branding / '6snt-icon.png'}")
    print(f"favicon -> {public / 'favicon.ico'}")


if __name__ == "__main__":
    main()
