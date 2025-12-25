import time
import psutil
import shutil

name = "stats"

START_TIME = time.time()

async def run(message, args):
    uptime_seconds = int(time.time() - START_TIME)
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    cpu_percent = psutil.cpu_percent(interval=0.5)

    mem = psutil.virtual_memory()
    mem_used = mem.used / (1024 ** 2)
    mem_total = mem.total / (1024 ** 2)
    mem_percent = mem.percent

    disk = shutil.disk_usage("/")
    disk_used = disk.used / (1024 ** 2)
    disk_total = disk.total / (1024 ** 2)
    disk_percent = (disk.used / disk.total) * 100

    net = psutil.net_io_counters()
    net_in = net.bytes_recv / (1024 ** 2)
    net_out = net.bytes_sent / (1024 ** 2)

    await message.channel.send(
        f"📊 **HOSTING STATS**\n"
        f"⏱️ Uptime: `{days}d {hours}h {minutes}m {seconds}s`\n\n"
        f"🖥️ CPU: `{cpu_percent:.2f}%`\n"
        f"🧠 RAM: `{mem_used:.2f} MiB / {mem_total:.2f} MiB` ({mem_percent}%)\n"
        f"💾 DISK: `{disk_used:.2f} MiB / {disk_total:.2f} MiB` ({disk_percent:.2f}%)\n\n"
        f"🌐 Net IN: `{net_in:.2f} MiB`\n"
        f"🌐 Net OUT: `{net_out:.2f} MiB`"
    )
