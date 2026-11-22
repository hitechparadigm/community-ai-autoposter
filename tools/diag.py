import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bot
s = bot.load_state()
print("### webhook:", {k: v for k, v in bot.tg("getWebhookInfo").items() if k in ("url", "pending_update_count", "last_error_message")})
for off in (0, s["tg_offset"]):
    ups = bot.tg("getUpdates", offset=off, timeout=0)
    print(f"### offset {'0' if off == 0 else 'state'}: {len(ups)} updates; kinds:",
          [ [k for k in u if k != 'update_id'][0] for u in ups ][:20],
          "ids:", [u["update_id"] for u in ups][:5], "state offset:", s["tg_offset"])
    for u in ups[:10]:
        cq = u.get("callback_query")
        if cq:
            print("###   tap data:", cq.get("data"), "from approver:", str(cq["from"]["id"]) in bot.ADMIN_IDS, "date:", cq.get("message", {}).get("date"))
