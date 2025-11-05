name = "love"

import random, io, aiohttp, os, time
from PIL import Image, ImageDraw, ImageFont
import discord

user_cooldowns = {}
COOLDOWN_SECONDS = 10
BAR_LEN = (700, 28)

def circle_crop(im, size):
    im = im.resize((size, size)).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((0, 0, size, size), fill=255)
    im.putalpha(mask)
    return im

async def fetch_avatar_image(url):
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data = await r.read()
            return Image.open(io.BytesIO(data)).convert("RGBA")

def get_nonbot_members(message):
    try:
        return [m for m in message.guild.members if not m.bot]
    except Exception:
        return []

def get_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except Exception:
            return ImageFont.load_default()

def measure_text(draw, text, font):
    if hasattr(draw, "textbbox"):
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        return w, h
    elif hasattr(draw, "textsize"):
        return draw.textsize(text, font=font)
    elif hasattr(font, "getbbox"):
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    else:
        return font.getsize(text)

async def run(message, args):
    now = time.time()
    user_id = message.author.id

    if user_id in user_cooldowns:
        remaining = user_cooldowns[user_id] - now
        if remaining > 0:
            await message.channel.send(f"Colddown {remaining:.1f}s!")
            return

    user_cooldowns[user_id] = now + COOLDOWN_SECONDS

    a = message.author
    mentions = message.mentions or []
    members = get_nonbot_members(message)

    if len(mentions) >= 1:
        b = mentions[0]
    else:
        pool = [m for m in members if m.id != a.id]
        b = random.choice(pool) if pool else a

    pct = 100 if a.id == b.id else random.randint(0, 100)

    try:
        av_a = await fetch_avatar_image(str(a.display_avatar.url))
    except Exception:
        av_a = Image.new("RGBA", (256, 256), (120, 120, 120, 255))
    try:
        av_b = await fetch_avatar_image(str(b.display_avatar.url))
    except Exception:
        av_b = Image.new("RGBA", (256, 256), (120, 120, 120, 255))

    AV_SIZE = 220
    BORDER = 8

    def with_border(circ):
        out = Image.new("RGBA", (circ.width + BORDER * 2, circ.height + BORDER * 2), (0, 0, 0, 0))
        dtmp = ImageDraw.Draw(out)
        dtmp.ellipse((0, 0, out.width - 1, out.height - 1), fill=(255, 182, 193, 255))
        out.paste(circ, (BORDER, BORDER), circ)
        return out

    circ_a = with_border(circle_crop(av_a, AV_SIZE))
    circ_b = with_border(circle_crop(av_b, AV_SIZE))

    W, H = 1000, 520
    bg = Image.new("RGBA", (W, H), (34, 34, 38, 255))
    draw = ImageDraw.Draw(bg)

    left_x = 80
    right_x = W - circ_b.width - 80
    top_y = 80
    bg.paste(circ_a, (left_x, top_y), circ_a)
    bg.paste(circ_b, (right_x, top_y), circ_b)

    img_path = "images/love/50.jpg" if pct >= 50 else "images/love/49.jpg"
    if os.path.exists(img_path):
        try:
            love_img = Image.open(img_path).convert("RGBA")
            max_size = 180
            w, h = love_img.size
            scale = min(max_size / max(w, h), 1.0)
            new_size = (int(w * scale), int(h * scale))
            love_img = love_img.resize(new_size, Image.LANCZOS)
            cx = W // 2 - love_img.width // 2
            cy = top_y + circ_a.height // 2 - love_img.height // 2
            bg.paste(love_img, (cx, cy), love_img)
        except Exception as e:
            print("error:", e)
    else:
        print(f"không tìm được ảnh {img_path}")

    bar_w, bar_h = BAR_LEN
    bar_x = (W - bar_w) // 2
    bar_y = H - 110
    draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), radius=14, fill=(60, 60, 65, 255))
    fill_w = int(bar_w * pct / 100)
    if fill_w > 0:
        draw.rounded_rectangle((bar_x, bar_y, bar_x + fill_w, bar_y + bar_h), radius=14, fill=(255, 105, 180, 255))

    font_pct = get_font(28)
    pct_text = f"{pct}%"
    w_txt, h_txt = measure_text(draw, pct_text, font_pct)
    draw.text((W // 2 - w_txt // 2, bar_y + (bar_h - h_txt) // 2), pct_text, font=font_pct, fill=(255, 255, 255, 255))

    font_name = get_font(26)
    name_a = a.display_name
    name_b = b.display_name
    wa, ha = measure_text(draw, name_a, font_name)
    wb, hb = measure_text(draw, name_b, font_name)
    draw.text((left_x + circ_a.width // 2 - wa // 2, top_y + circ_a.height + 10), name_a, font=font_name, fill=(255, 255, 255, 255))
    draw.text((right_x + circ_b.width // 2 - wb // 2, top_y + circ_b.height + 10), name_b, font=font_name, fill=(255, 255, 255, 255))

    out = io.BytesIO()
    bg.save(out, "PNG")
    out.seek(0)
    await message.channel.send(file=discord.File(out, "love.png"))