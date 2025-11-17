name = "wiki"

import aiohttp
import asyncio
import json
import urllib.parse

def shorten(text, limit=600):
    if not text:
        return ""
    if len(text) <= limit:
        return text
    cut = text[:limit]
    last_space = cut.rfind(" ")
    if last_space > 0:
        cut = cut[:last_space]
    return cut + "…"

async def fetch_json(session, url, timeout=10, headers=None):
    headers = headers or {"User-Agent": "WikiBot/1.0 (https://example/)"}
    try:
        async with session.get(url, timeout=timeout, headers=headers, allow_redirects=True) as resp:
            if resp.status == 200:
                return await resp.json()
            return None
    except Exception:
        return None

def parse_query(args):
    if isinstance(args, list):
        s = " ".join(args).strip()
    else:
        s = (args or "").strip()
    return s

async def run(message, args):
    query = parse_query(args)
    if not query:
        try:
            await message.channel.send("Cách dùng: `,wiki <từ khóa>` — bot chỉ tra bằng tiếng Việt.")
        except Exception:
            pass
        return

    qenc = urllib.parse.quote(query)
    base = "https://vi.wikipedia.org"
    summary_url = f"{base}/api/rest_v1/page/summary/{qenc}"
    opensearch_url = f"{base}/w/api.php?action=opensearch&search={qenc}&limit=5&format=json"

    async with aiohttp.ClientSession() as session:
        data = await fetch_json(session, summary_url)
        if data and isinstance(data, dict):
            # If straightforward summary (not disambiguation), use it
            typ = data.get("type")
            if typ and typ != "disambiguation":
                title = data.get("title", query)
                extract = data.get("extract") or data.get("description") or ""
                page_url = data.get("content_urls", {}).get("desktop", {}).get("page") or f"{base}/wiki/{qenc}"
                short = shorten(extract, 600)
                msg = f"**{title}**\n{short}\n{page_url}"
                try:
                    await message.channel.send(msg)
                except Exception:
                    pass
                return
            # if disambiguation -> fallthrough to try first search result
        # either no summary or disambiguation: try opensearch and pick first result only
        search = await fetch_json(session, opensearch_url)
        if search and isinstance(search, list) and len(search) >= 1:
            titles = search[1] if len(search) > 1 else []
            urls = search[3] if len(search) > 3 else []
            if titles:
                first_title = titles[0]
                first_url = urls[0] if urls else None
                first_q = urllib.parse.quote(first_title)
                first_summary_url = f"{base}/api/rest_v1/page/summary/{first_q}"
                first_data = await fetch_json(session, first_summary_url)
                if first_data and isinstance(first_data, dict):
                    title = first_data.get("title", first_title)
                    extract = first_data.get("extract") or first_data.get("description") or ""
                    page_url = first_data.get("content_urls", {}).get("desktop", {}).get("page") or first_url or f"{base}/wiki/{first_q}"
                    short = shorten(extract, 600)
                    msg = f"**{title}**\n{short}\n{page_url}"
                    try:
                        await message.channel.send(msg)
                    except Exception:
                        pass
                    return
                else:
                    # fallback: send first title + url only (single line)
                    if first_url:
                        try:
                            await message.channel.send(f"**{first_title}**\n{first_url}")
                        except Exception:
                            pass
                        return
        # nothing found
        try:
            await message.channel.send(f"Không tìm thấy kết quả cho: {query}")
        except Exception:
            pass
