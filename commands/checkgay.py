import random

name = "gay"

async def run(message, args):
    
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author

    
    gay_rate = random.randint(0, 100)

    
    if gay_rate < 30:
        emoji = "🧢"
        desc = "Cũng hơi thẳng đó 😎"
    elif gay_rate < 70:
        emoji = "🌈"
        desc = "Hơi cong nhẹ rồi nha 😏"
    else:
        emoji = "💅"
        desc = "Full màu cầu vồng luôn rồi 🌈✨"

    await message.channel.send(f"{emoji} | **{target.display_name}** gay {gay_rate}%\n{desc}")
