name = "help"

async def run(message, args):
    
    full_msg = message.content.strip()
    prefix = ""
    if full_msg and not full_msg[0].isalnum():
        prefix = full_msg[0] 
    else:
        prefix = "$"

    help_text = (
        f"  **Danh sách lệnh hiện có:**\n"
        f"`{prefix}help` — Hiển thị bảng lệnh\n"
        f"`{prefix}ping` — Sống không bot ơi\n"
        f"`{prefix}add <từ1> <từ2>` — Thêm cặp từ mới\n"
        f"`{prefix}whelp <từ>` — Hiển thị 10 từ có thể nối tiếp\n"
    )

    await message.channel.send(help_text)
