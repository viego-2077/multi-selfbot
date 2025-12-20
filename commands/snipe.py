name = "snipe"

from datetime import datetime

def format_time(iso_time: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except Exception:
        return iso_time

async def run(message, args):
    if not message.guild:
        await message.channel.send("Không dùng snipe trong DMS.")
        return

    from main import load_snipe_db

    db = load_snipe_db()
    key = f"{message.guild.id}:{message.channel.id}"

    messages = db.get(key)
    if not messages:
        await message.channel.send("Không có tin nhắn bị xoá.")
        return

    latest = messages[:10] 
    blocks = []

    for idx, msg in enumerate(latest, start=1):
        author = msg.get("author", "Unknown")
        deleted_at_raw = msg.get("deleted_at", "Unknown time")
        deleted_at = format_time(deleted_at_raw)

        content = msg.get("content") or "[No content]"
        attachments = msg.get("attachments", [])

        block_lines = [
            f"{idx}. **{author} - {deleted_at}**",
            content
        ]


        if attachments:
            block_lines.extend(attachments)

        block_lines.append("========================")

        blocks.append("\n".join(block_lines))

    result = "\n".join(blocks)


    if len(result) > 1900:
        result = result[:1900] + "\n...(còn nữa)"

    await message.channel.send(result)
