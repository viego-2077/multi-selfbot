name = "cat"

import aiohttp
import discord

API_URL = "https://some-random-api.com/animal/cat"

async def run(message, args):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as resp:
            if resp.status != 200:
                await message.channel.send("Error cat API.")
                return
            data = await resp.json()

    cat_url = data.get("image")
    fact = data.get("fact")

    if not cat_url:
        await message.channel.send("không có con mèo nào cả.")
        return

    if not fact:
        fact = "🐱 Một chú mèo dễ thương đã xuất hiện!"

    await message.channel.send(f"{fact}\n{cat_url}")
