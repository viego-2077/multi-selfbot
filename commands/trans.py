import googletrans
from googletrans import Translator

name = "trans"

async def run(message, args):
    if len(args) < 2:
        await message.channel.send("Dùng cú pháp: `$translate <ngôn_ngữ_đích> <văn bản>`")
        return

    dest_lang = args[0].lower()
    text = " ".join(args[1:])

    translator = Translator()
    try:
        result = translator.translate(text, dest=dest_lang)
        await message.channel.send(f"**Dịch sang `{dest_lang}`:**\n> {result.text}")
    except Exception as e:
        await message.channel.send(f"error: `{e}`")
