"""End-to-end flow with the network faked: a news draft is written, sent for approval, approved and published."""
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.parse
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autoposter import approval, core, drafts, news  # noqa: E402
import config  # noqa: E402

RSS = """<rss><channel><item><title>Ottawa pauses refugee program</title>
<link>https://globalnews.ca/news/1/pause/</link><description>The federal government paused a program.</description>
<pubDate>{date}</pubDate></item></channel></rss>"""
ARTICLE = "<html><body><article>" + "<p>" + ("The federal government paused the program today. " * 30) + "</p></article></body></html>"


class FakeNet:
    def __init__(self):
        self.telegram, self.updates = [], []

    def __call__(self, req, timeout=0):
        url = req.full_url if hasattr(req, "full_url") else req
        body = json.loads(req.data) if getattr(req, "data", None) else {}
        if "api.anthropic.com" in url:
            return self.claude(body)
        if "api.telegram.org" in url:
            method = url.rsplit("/", 1)[1]
            self.telegram.append((method, body))
            result = self.updates if method == "getUpdates" else {"message_id": len(self.telegram)}
            if method == "getUpdates":
                self.updates = []
            return self.reply({"ok": True, "result": result})
        if url.endswith("/feed/") or "rss" in url or "outboundfeeds" in url or "bing.com" in url:
            date = core.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
            return self.reply(RSS.format(date=date).encode() if "globalnews.ca/canada" in url else b"<rss/>", raw=True)
        return self.reply(ARTICLE.encode(), raw=True)

    def claude(self, body):
        tool = (body.get("tools") or [{}])[0].get("input_schema", {})
        props = tool.get("properties", {})
        if "ids" in props:
            data = {"ids": [0]}
        elif "verdict" in props:
            data = {"verdict": "ok", "problems": []}
        elif "id" in props:
            data = {"id": None}
        else:
            data = {"title": "Оттава призупинила програму", "body": "Федеральний уряд призупинив програму сьогодні. "
                    "Це стосується спонсорів.", "image_query": "", "emoji": "🛂"}
        content = [{"type": "tool_use", "name": "answer", "input": data}]
        return self.reply({"content": content, "usage": {}})

    @staticmethod
    def reply(data, raw=False):
        payload = data if raw else json.dumps(data).encode()
        r = io.BytesIO(payload)
        r.__enter__ = lambda *a: r
        r.__exit__ = lambda *a: None
        return r


class Flow(unittest.TestCase):
    def test_draft_then_publish(self):
        net = FakeNet()
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch("urllib.request.urlopen", net), \
                mock.patch.object(core, "STATE_FILE", os.path.join(tmp, "state.json")), \
                mock.patch.object(core, "TG_TOKEN", "t"), \
                mock.patch.object(news, "ADMIN_IDS", ["1"]), mock.patch.object(drafts, "ADMIN_IDS", ["1"]), \
                mock.patch.object(approval, "ADMIN_IDS", ["1"]), mock.patch.object(core, "ADMIN_IDS", ["1"]), \
                mock.patch("autoposter.ai.ANTHROPIC_KEY", "k"), \
                mock.patch.object(config, "FEEDS", [("Global News", "https://globalnews.ca/canada/feed/", "Canada")]):
            news.cmd_draft()
            s = core.load_state()
            self.assertEqual(len(s["pending"]), 1)
            did, d = next(iter(s["pending"].items()))
            self.assertIn("🛂 Оттава призупинила програму", d["text"])
            self.assertIn("📊", [b for m, b in net.telegram if m == "sendMessage"][0]["text"])

            net.updates = [{"update_id": 10, "callback_query": {"id": "q", "from": {"id": 1, "first_name": "D"},
                                                                 "data": f"pub:{did}"}}]
            approval.cmd_approve()
            s = core.load_state()
            self.assertEqual(s["pending"], {})
            channel_posts = [b for m, b in net.telegram if m == "sendMessage" and b.get("chat_id") == config.CHANNEL]
            self.assertEqual(len(channel_posts), 1)
            self.assertEqual(s["learn"][-1]["event"], "published")
            self.assertEqual(s["tg_offset"], 11)


if __name__ == "__main__":
    unittest.main()
