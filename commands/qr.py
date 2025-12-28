import os
import io
import aiohttp
from PIL import Image
 
name = "qr"
QR_DIR = "images/qr"

def ensure_dirs():
    os.makedirs(QR_DIR, exist_ok=True)


async def fetch_image_raw(url, timeout=10):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as resp:
                if resp.status == 200:
                    return await resp.read()
    except:
        pass
    return None


async def get_attachment_image_bytes(message):
    try:
        attachments = getattr(message, "attachments", []) or []
        for a in attachments:
            ctype = getattr(a, "content_type", "")
            if ctype and ctype.startswith("image"):
                return await fetch_image_raw(a.url)
        return None
    except:
        return None


def save_qr(uid: str, img_bytes: bytes):
    try:
        im = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
        path = os.path.join(QR_DIR, f"qr_{uid}.png")
        im.save(path, "PNG")
        return path
    except:
        return None


async def run(message, args):
    if isinstance(args, str):
        parts = args.strip().split()
    else:
        parts = args or []

    ensure_dirs()

    author = message.author
    uid = str(author.id)
    qr_path = os.path.join(QR_DIR, f"qr_{uid}.png")

    if len(parts) >= 1 and parts[0].lower() == "help":
        help_text = (
            "```md\n"
            "# QR COMMANDS\n"
            "• ,qr - Xem QR của bằn\n"
            "• ,qr edit - Lưu / cập nhật QR (đính kèm ảnh)\n"
            "• ,qr delete - Xóa QR\n"
            "```"
        )
        await message.channel.send(help_text)
        return


    if len(parts) >= 1 and parts[0].lower() == "delete":
        if os.path.exists(qr_path):
            try:
                os.remove(qr_path)
                await message.channel.send("✔ Đã xóa QR của bạn")
            except:
                await message.channel.send("✘ Không xóa được QR")
        else:
            await message.channel.send("⚠ Bạn chưa có QR để xóa")
        return

    if len(parts) >= 1 and parts[0].lower() == "edit":
        img_bytes = await get_attachment_image_bytes(message)

        if not img_bytes:
            await message.channel.send(
                "⚠ Hãy **đính kèm ảnh QR** khi dùng lệnh `,qr edit`."
            )
            return

        saved = save_qr(uid, img_bytes)
        if not saved:
            await message.channel.send("✘ Không lưu được ảnh QR.")
            return

        await message.channel.send("✔ Đã cập nhật ảnh QR của bạn.")
        return

    if not os.path.exists(qr_path):
        await message.channel.send(
            "⚠ Bạn **chưa có QR**.\n"
            "Dùng lệnh `,qr edit` và **đính kèm ảnh QR** để lưu."
        )
        return
    

    import discord
    await message.channel.send(
        file=discord.File(qr_path, filename="qr.png")
    )
