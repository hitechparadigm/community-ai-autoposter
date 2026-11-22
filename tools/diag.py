import re, urllib.request, gzip
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=40) as r:
            b = r.read()
            if b[:2] == b"\x1f\x8b": b = gzip.decompress(b)
            return r.status, b.decode("utf-8", "replace")
    except Exception as e:
        return str(e)[:80], ""
def show(name, url, pat=r'<loc>([^<]+)</loc>', n=8):
    st, html = get(url)
    links = re.findall(pat, html)
    print(f"\n### {name} | {st} | {len(html)} bytes | {len(links)} matches")
    for l in links[:n]: print("   ", l[:140])
show("Canada's History sitemap", "https://www.canadashistory.ca/sitemap.xml")
show("DCB sitemap", "http://www.biographi.ca/sitemap.xml")
show("DCB hrefs", "http://www.biographi.ca/en/", r'href="([^"]*bio[^"]*)"')
show("Pier21 sitemap", "https://pier21.ca/sitemap.xml")
show("Pier21 hrefs", "https://pier21.ca/research/immigration-history", r'href="(/research/[^"]+)"', 15)
show("NL sitemap", "https://www.heritage.nf.ca/sitemap.xml")
show("BCHF sitemap", "https://www.bchistory.ca/sitemap.xml")
show("OHT sitemap", "https://www.heritagetrust.on.ca/sitemap.xml")
show("NS Archives", "https://archives.novascotia.ca/", r'href="([^"]+)"', 15)
show("PEI Museum", "https://www.peimuseum.ca/", r'href="([^"]+)"', 15)
show("NB Archives", "https://archives.gnb.ca/Archives/default.aspx?culture=en-CA", r'href="([^"]+)"', 10)
show("Yukon Archives", "https://yukon.ca/en/yukon-archives", r'href="([^"]+)"', 10)
show("PWNHC NWT", "https://www.pwnhc.ca/", r'href="([^"]+)"', 15)
show("Inuit Heritage Trust", "https://www.ihti.ca/", r'href="([^"]+)"', 10)
show("Encyclopedia of Ukraine", "https://www.encyclopediaofukraine.com/display.asp?linkpath=pages%5CU%5CK%5CUkrainiansinCanada.htm", r'<p[^>]*>', 2)
show("TCE no-www", "https://thecanadianencyclopedia.ca/en/article/manitoba", r'<p[^>]*>', 2)
show("LAC feed", "https://thediscoverblog.com/feed/", r'<title>([^<]+)</title>', 4)
show("Parks Canada heritage", "https://parks.canada.ca/culture/designation", r'href="([^"]+)"', 5)
