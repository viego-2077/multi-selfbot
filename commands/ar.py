name = "ar"

import os
import json
import asyncio
import time

DATA_FILE = "auto_responses.json"
ITEMS_PER_PAGE = 5
WAIT_TIMEOUT = 60 


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


async def wait_user_reply_obj(orig_message, last_id, timeout=WAIT_TIMEOUT):
    """Chờ tin nhắn tiếp theo"""
    channel = orig_message.channel
    author = orig_message.author
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        try:
            async for m in channel.history(limit=20):
                if m.author.id == author.id and m.id > last_id:
                    return m
        except Exception:
            pass
        await asyncio.sleep(1)
    return None


async def run(message, args):
    if len(args) == 0:
        await message.channel.send("`$ar add` | `$ar list <trang>` | `$ar remove <id>`")
        return

    sub = args[0].lower()
    data = load_data()

    if sub == "add":
        await message.channel.send("Nhập trigger:")
        reply_msg = await wait_user_reply_obj(message, message.id)
        if reply_msg is None:
            await message.channel.send("Đã hết thời gian chờ. Hủy thao tác.")
            return
        trigger = reply_msg.content.strip()

        await message.channel.send("Nhập response:")
        reply_msg2 = await wait_user_reply_obj(message, reply_msg.id)
        if reply_msg2 is None:
            await message.channel.send("Đã hết thời gian chờ. Hủy thao tác.")
            return
        response = reply_msg2.content.strip()

        next_id = 1
        if data:
            try:
                next_id = max(int(item.get("id", 0)) for item in data) + 1
            except Exception:
                next_id = len(data) + 1

        entry = {
            "id": next_id,
            "guild_id": str(message.guild.id) if message.guild else None,
            "channel_id": str(message.channel.id),
            "trigger": trigger,
            "response": response,
        }
        data.append(entry)
        save_data(data)
        await message.channel.send("đã lưu auto response.")

    elif sub == "list":
        page = 1
        if len(args) >= 2:
            try:
                page = int(args[1])
                if page < 1:
                    page = 1
            except:
                page = 1

        guild_id = str(message.guild.id) if message.guild else None
        items = [it for it in data if it.get("guild_id") == guild_id]
        total = len(items)
        if total == 0:
            await message.channel.send("Không có auto response nào.")
            return

        max_page = max(1, (total + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
        if page > max_page:
            page = max_page
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        page_items = items[start:end]

        lines = ["Auto response list"]
        for it in page_items:
            tid = it.get("id")
            t = it.get("trigger", "")
            r = it.get("response", "")
            if len(t) > 80:
                t = t[:77] + "..."
            if len(r) > 80:
                r = r[:77] + "..."
            lines.append(f"{tid}. `{t}` -> `{r}`")
        lines.append(f"[{page}/{max_page}]")
        await message.channel.send("\n".join(lines))

    elif sub == "remove":
        if len(args) < 2:
            await message.channel.send("`$ar remove <id>`")
            return
        try:
            rid = int(args[1])
        except:
            await message.channel.send("ID không hợp lệ.")
            return

        guild_id = str(message.guild.id) if message.guild else None
        new_data = []
        found = False
        for it in data:
            try:
                if int(it.get("id", 0)) == rid and it.get("guild_id") == guild_id:
                    found = True
                    continue
            except:
                pass
            new_data.append(it)

        if not found:
            await message.channel.send("Không tìm thấy ID.")
            return

        save_data(new_data)
        await message.channel.send("Đã xóa auto response.")

    else:
        await message.channel.send("`$ar add` | `$ar list <trang>` | `$ar remove <id>`")
