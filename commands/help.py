name = "help"
import os

async def run(message, args):
    all_cmds = [f[:-3] for f in os.listdir("commands") if f.endswith(".py")]
    await message.channel.send(f"**Lệnh có sẵn:** {', '.join(all_cmds)}")