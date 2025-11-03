import os


name = "whelp"

async def run(message, args):
    if not args:
        await message.channel.send("Dùng cú pháp: `$whelp <từ>`")
        return

    target = args[0].lower()
    if not os.path.exists("word.txt"):
        await message.channel.send("Chưa có từ điển (word.txt trống).")
        return

    results = []
    with open("word.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().lower().split()
            if len(parts) == 2 and parts[0] == target:
                results.append(parts[1])

    if results:
        preview = ", ".join(results[:10])
        await message.channel.send(f"🔗 Từ nối sau `{target}`: {preview}")
    else:
        await message.channel.send(f"Không có từ nào nối sau `{target}`.")
