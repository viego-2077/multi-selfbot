name = "waifu"

import aiohttp
import discord
import random

API_URL = "https://api.waifu.pics/sfw/waifu"

async def run(message, args):
    captions = [
    "✨ Waifu của bạn đây ~",
    "💖 Có ai đáng yêu hơn không nào?",
    "🌸 Xin hãy đối xử tốt với cô ấy!",
    "💞 Một waifu tuyệt đẹp vừa xuất hiện!",
    "🩷 Đây là định mệnh của bạn đó!",
    "🎀 Nụ cười này đáng giá nghìn like!",
    "💕 Đừng nhìn lâu quá, kẻo yêu mất đó ~",
    "💫 Có vẻ ai đó vừa trúng tiếng sét ái tình!",
    "🌷 Vẻ đẹp này khiến thời gian ngừng trôi...",
    "🎐 Một làn gió waifu tươi mới đang thổi qua đây!",
    "🌈 Cẩn thận, waifu này có thể làm tan chảy trái tim bạn!",
    "🌻 Hãy chiêm ngưỡng kiệt tác của thế giới 2D!",
    "💘 Đây là waifu dành riêng cho bạn, số phận đã chọn!",
    "💮 Mỗi khi bạn buồn, cô ấy sẽ làm bạn cười đấy ~",
    "🌹 Không cần tìm nữa, đây chính là chân ái của bạn!",
    "🍓 Dễ thương cấp độ MAX!!!",
    "🧸 Hãy nói 'kawaii' đi nào!",
    "🎶 Trái tim bạn vừa 'ping' một cái!",
    "📸 Waifu vừa online, bạn có muốn mời cô ấy đi chơi không?",
    "💌 Bạn nhận được 1 waifu từ vũ trụ gửi đến 💫",
    "🌟 Cô ấy không chỉ xinh đẹp mà còn biết nấu ăn (trong tưởng tượng 😆)",
    "🩵 Nếu bạn cười, cô ấy cũng cười cùng bạn 💫",
    "🎇 Một waifu hiếm vừa xuất hiện, hãy bắt lấy cô ấy!",
    "🥰 Khi bạn cô đơn, cô ấy sẽ xuất hiện ở đây ~",
    "💎 Không phải waifu nào cũng được chọn, nhưng bạn vừa được chọn rồi!",
    ]
    caption = random.choice(captions)

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as resp:
            if resp.status != 200:
                await message.channel.send("error API waifu.pics.")
                return
            data = await resp.json()
            img_url = data.get("url")

    if not img_url:
        await message.channel.send("API no response.")
        return

    await message.channel.send(f"{caption}\n[your waifu]({img_url})")
