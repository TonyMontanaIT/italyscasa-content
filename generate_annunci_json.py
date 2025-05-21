import frontmatter
import json
from pathlib import Path

md_folder = Path("anunci")
output_path = md_folder / "index2.json"

data = []

for file in md_folder.glob("*.md"):
    post = frontmatter.load(file)
    meta = post.metadata
    riferimento = meta.get("riferimento") or meta.get("RIF1") or file.stem

    # Приводим изображения к нужному виду: [{src: "...", alt: "..."}]
    images = meta.get("images", [])
    if isinstance(images, list) and all(isinstance(i, str) for i in images):
        images = [{"src": i, "alt": ""} for i in images]

    data.append({
        "slug": riferimento,
        "riferimento": riferimento,
        "rif1": meta.get("RIF1", ""),
        "nomeAnunci": meta.get("nomeAnunci", ""),
        "nomeZona": meta.get("nomeZona", ""),
        "city1": meta.get("city1", ""),
        "street1": meta.get("street1", ""),
        "prezzo1": meta.get("prezzo1", ""),
        "tipo": meta.get("tipo", ""),
        "totalrooms": meta.get("totalrooms", ""),
        "rooms": meta.get("rooms", ""),
        "bagni": meta.get("bagni", ""),
        "zonam2": meta.get("zonam2", ""),
        "floor": str(meta.get("floor", "")),
        "elevator": str(meta.get("elevator", "")),
        "terrazzo": str(meta.get("terrazzo", "")),
        "prezzo": meta.get("prezzo", ""),
        "prezzoDescrizione": meta.get("prezzoDescrizione", ""),
        "giardino": str(meta.get("giardino", "")),
        "garage": str(meta.get("garage", "")),
        "arredamenti": str(meta.get("arredamenti", "")),
        "patio": str(meta.get("patio", "")),
        "corte": str(meta.get("corte", "")),
        "descrizione": meta.get("descrizione", ""),
        "h2t1": meta.get("h2t1", ""),
        "text1": meta.get("text1", ""),
        "h2t2": meta.get("h2t2", ""),
        "text2": meta.get("text2", ""),
        "h2t3": meta.get("h2t3", ""),
        "text3": meta.get("text3", ""),
        "h2t4": meta.get("h2t4", ""),
        "text4": meta.get("text4", ""),
        "h2t5": meta.get("h2t5", ""),
        "text5": meta.get("text5", ""),
        "h2t6": meta.get("h2t6", ""),
        "text6": meta.get("text6", ""),
        "video": meta.get("video", ""),
        "video360": meta.get("video360", ""),
        "images": images,
        "latitude": meta.get("latitude", ""),
        "longitude": meta.get("longitude", "")
    })

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
