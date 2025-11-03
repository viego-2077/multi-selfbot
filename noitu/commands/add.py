name = "add"

async def run(message, args):
    if len(args) < 2:
        await message.channel.send("Dùng cú pháp: !add <từ1> <từ2>")
        return

    first, second = args[0].lower(), args[1].lower()
    with open("word.txt", "a", encoding="utf-8") as f:
        f.write(f"{first} {second}\n")

    await message.channel.send(f"Đã thêm cặp từ: `{first} → {second}`")
