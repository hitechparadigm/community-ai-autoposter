import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bot
def raw(u):
    try: return bot.http(u, timeout=40).decode("utf-8", "replace")
    except Exception as e: return "ERR " + str(e)[:90]
U = [
 "https://esask.uregina.ca/entry/ukrainians.html",
 "https://www.encyclopediaofukraine.com/display.asp?linkpath=pages%5CU%5CK%5CUkrainiansinCanada.htm",
 "https://www.encyclopediaofukraine.com/display.asp?linkpath=pages%5CP%5CY%5CPylypiwIvan.htm",
 "https://www.encyclopediaofukraine.com/display.asp?linkpath=pages%5CI%5CN%5CInternmentofUkrainiansinCanada.htm",
 "https://thediscoverblog.com/2025/07/17/the-kapuskasing-internment-camp/",
 "https://www.internmentcanada.ca/",
 "http://www.biographi.ca/en/bio_of_the_day.html",
 "https://www.cbc.ca/archives/a-farmer-discovered-oil-on-his-ontario-farm-in-1879-a-century-later-it-was-still-flowing-1.5188814",
 "https://qahn.org/article/st-francis-college",
 "https://esask.uregina.ca/entry/bands.html",
 "https://www.mhs.mb.ca/docs/people/kasper_fj.shtml",
 "https://www.heritagetrust.on.ca/heritagematters/articles/massey-tower",
]
for u in U:
    page = raw(u)
    og = re.findall(r'<meta[^>]+(?:property|name)="og:image"[^>]+content="([^"]+)"', page) or re.findall(r'<meta[^>]+content="([^"]+)"[^>]+property="og:image"', page)
    imgs = re.findall(r'<img[^>]+src="([^"]+\.(?:jpe?g|png))"', page, re.I)
    ps = len(re.findall(r'(?is)<p[^>]*>', page))
    print(f"\n### {u[:100]}\n  {'ERR '+page[:90] if page.startswith('ERR') else len(page)} bytes, <p>: {ps}, og:image: {og[:1]}, imgs: {imgs[:2]}")
    if "bio_of_the_day" in u:
        print("  bio links:", re.findall(r'href="([^"]*bio/[^"]+)"', page)[:5])
    if "UkrainiansinCanada" in u:
        l = re.findall(r'href="(display\.asp\?linkpath=[^"]+)"', page)
        print("  EoU links:", len(l), l[:8])
        i = page.find("Ukrainians in Canada"); print("  RAW:", re.sub(r"\s+"," ",page[i:i+700]))
