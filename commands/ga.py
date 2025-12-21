# dong nay duoc them chi de code tron 100 dong
import asyncio
from datetime import datetime, timedelta

name = "ga"

def format_duration(seconds):
    d, seconds = divmod(seconds, 86400)
    h, seconds = divmod(seconds, 3600)
    m, s = divmod(seconds, 60)

    text = []
    if d > 0:
        text.append(f"{d}d")
    if h > 0:
        text.append(f"{h}h")
    if m > 0:
        text.append(f"{m}m")
    if s > 0:
        text.append(f"{s}s")

    return " ".join(text)


async def run(message, args):
    if len(args) < 3:
        await message.channel.send(
            "`,ga <số_giải> <thời_gian> <phần_thưởng>`\n"
            "Ví dụ: `,ga 1 1h30m Nitro Boost`"
        )
        return

    try:
        winners_count = int(args[0])
    except ValueError:
        await message.channel.send("Số người thắng lớn hơn 0.")
        return

    time_str = args[1].lower()
    reward = " ".join(args[2:])

    seconds = 0
    num = ''
    for ch in time_str:
        if ch.isdigit():
            num += ch
        elif ch in ['s', 'm', 'h', 'd']:
            if num:
                val = int(num)
                if ch == 's':
                    seconds += val
                elif ch == 'm':
                    seconds += val * 60
                elif ch == 'h':
                    seconds += val * 3600
                elif ch == 'd':
                    seconds += val * 86400
                num = ''

    if seconds == 0:
        await message.channel.send(
            "Thời gian không hợp lệ. Ví dụ: `10s`, `5m`, `1h30m`, `1d`"
        )
        return

    time_left = format_duration(seconds)

    msg = await message.channel.send(
        f"# 🎉 [**GIVEAWAY**](https://tenor.com/view/undgretel-undgretelcosmetics-undgretelberlin-naturkosmetik-organicbeauty-gif-24197922) 🎉\n"
        f"> **Phần thưởng:** {reward}\n"
        f"> **Số giải thưởng:** {winners_count}\n"
        f"> **Kết thúc sau:** {time_left}\n"
        f"> **Người tạo:** {message.author.mention}\n"
    )

    await msg.add_reaction("🎉")

    await asyncio.sleep(seconds)

    msg = await message.channel.fetch_message(msg.id)
    users = [user async for user in msg.reactions[0].users()]

    users = [u for u in users if not u.bot and u.id != 1441614798419918858]

    if len(users) == 0:
        await msg.reply("Không có ai tham gia giveaway.")
        return

    import random
    winners = random.sample(users, min(winners_count, len(users)))

    winner_mentions = ", ".join([w.mention for w in winners])

    await msg.reply(
        f"# Giveaway kết thúc! 🎊\n"
        f"🎁 **Phần thưởng:** {reward}\n"
        f"🏆 **Người thắng:** {winner_mentions}\n"
        f"❤️ **Host:** {message.author.mention}",
        mention_author=False
    )