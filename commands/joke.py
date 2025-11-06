name = "joke"

import aiohttp
import discord

JOKE_API = "https://v2.jokeapi.dev/joke/Any"
TRANS_API = "https://api.mymemory.translated.net/get"

async def run(message, args):
    async with aiohttp.ClientSession() as session:
        async with session.get(JOKE_API) as resp:
            if resp.status != 200:
                await message.channel.send("Error Joke API.")
                return
            data = await resp.json()

        if data.get("type") == "single":
            joke_text = data.get("joke")
        else:
            joke_text = f"{data.get('setup')}\n{data.get('delivery')}"

        if not joke_text:
            await message.channel.send("😢 no jokes today.")
            return

        params = {"q": joke_text, "langpair": "en|vi"}
        async with session.get(TRANS_API, params=params) as t:
            trans_data = await t.json()
            vi_joke = trans_data.get("responseData", {}).get("translatedText")

        if not vi_joke:
            await message.channel.send(f"🗣️ {joke_text}")
            return

        await message.channel.send(f"🤣 {vi_joke}")
