import time
import psutil
import shutil
import os

name = "stats"
START_TIME = time.time()

def get_docker_memory():
    try:
        with open("/sys/fs/cgroup/memory/memory.limit_in_bytes") as f:
            limit = int(f.read())
        with open("/sys/fs/cgroup/memory/memory.usage_in_bytes") as f:
            used = int(f.read())
        return used / 1024 / 1024, limit / 1024 / 1024
    except:
        return None, None

async def run(message, args):
    uptime = int(time.time() - START_TIME)
    d, r = divmod(uptime, 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)

    cpu = psutil.cpu_percent(interval=0.5)

    mem_used, mem_total = get_docker_memory()
    if mem_used is None:
        mem = psutil.virtual_memory()
        mem_used = mem.used / 1024 / 1024
        mem_total = mem.total / 1024 / 1024

    disk = shutil.disk_usage("/")
    disk_used = disk.used / 1024 / 1024
    disk_total = disk.total / 1024 / 1024

    net = psutil.net_io_counters()
    net_in = net.bytes_recv / 1024 / 1024
    net_out = net.bytes_sent / 1024 / 1024

    await message.channel.send(
        "📊 HOSTING STATS\n"
        f"⏱️ Uptime: {d}d {h}h {m}m {s}s\n"
        f"🖥️ CPU: {cpu:.2f}%\n"
        f"🧠 RAM: {mem_used:.2f} MiB / {mem_total:.2f} MiB\n"
        f"💾 Disk: {disk_used:.2f} MiB / {disk_total:.2f} MiB\n"
        f"🌐 Net IN: {net_in:.2f} MiB\n"
        f"🌐 Net OUT: {net_out:.2f} MiB"
    )
