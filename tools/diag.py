import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bot, config
me = bot.tg("getMe"); print("### bot:", me["username"], "| can read all group msgs:", me.get("can_read_all_group_messages"))
m = bot.tg("getChatMember", chat_id=config.CHANNEL, user_id=me["id"])
print("### in channel:", m["status"], "| can post:", m.get("can_post_messages"), "| can edit:", m.get("can_edit_messages"))
w = bot.tg("getWebhookInfo"); print("### webhook:", w.get("url") or "none", "| pending updates:", w.get("pending_update_count"))
for i, a in enumerate(bot.ADMIN_IDS, 1):
    try:
        c = bot.tg("getChat", chat_id=a); print(f"### approver #{i}: reachable ({c.get('type')})")
    except Exception as e:
        print(f"### approver #{i}: NOT reachable ({str(e)[:80]})")
try:
    acc = bot.telegraph("getAccountInfo", {}, fields='["short_name","page_count"]'); print("### telegraph:", acc)
except Exception as e:
    print("### telegraph ERROR:", e)
print("### facebook configured:", bool(bot.FB_PAGE_ID and bot.FB_TOKEN))
print("### anthropic key set:", bool(bot.ANTHROPIC_KEY), "| model:", config.MODEL)
