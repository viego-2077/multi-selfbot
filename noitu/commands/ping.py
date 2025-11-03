name = "ping"

async def run(message, args):
    await message.channel.send("pong!")