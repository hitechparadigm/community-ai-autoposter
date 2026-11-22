import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bot
for u in ["https://qahn.org/article/dr-maude-abbott-1869-1940-pioneer-woman-doctor",
          "http://www.biographi.ca/en/bio/rye_maria_susan_14E.html",
          "https://www.cbc.ca/archives/a-farmer-discovered-oil-on-his-ontario-farm-in-1879-a-century-later-it-was-still-flowing-1.5188814",
          "https://www.mhs.mb.ca/docs/people/kasper_fj.shtml",
          "https://esask.uregina.ca/entry/bands.html"]:
    text, img = bot.fetch_page(u)
    print(f"### {u[:70]}: text {len(text)}, image: {img or 'NONE'}")
for q in ["Maude Abbott", "Maria Rye", "Filip Konowal", "Halifax Explosion"]:
    print(f"### commons {q}: {bot.commons_image(q)}")
