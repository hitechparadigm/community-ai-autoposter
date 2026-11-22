import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bot
last = None
for i in range(24):  # ~4 minutes, only looks, never takes updates
    w = bot.tg("getWebhookInfo")
    n = w.get("pending_update_count")
    if n != last:
        print(f"### t+{i*10}s waiting taps: {n}", flush=True)
        last = n
    time.sleep(10)
