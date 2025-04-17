import frontmatter
import json
from pathlib import Path

md_folder = Path("anunci")
output_path = md_folder / "index2.json"

output_path.parent.mkdir(parents=True, exist_ok=True)

data = []

for file in md_folder.glob("*.md"):
    post = frontmatter.load(file)
    meta = post.metadata
    data.append({
        "slug": meta.get("riferimento", file.stem),
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
        "floor": meta.get("floor", ""),
        "elevator": meta.get("elevator", ""),
        "terrazzo": meta.get("terrazzo", ""),
        "prezzo": meta.get("prezzo", ""),
        "giardino": meta.get("giardino", ""),
        "garage": meta.get("garage", ""),
        "arredamenti": meta.get("arredamenti", ""),
        "patio": meta.get("patio", ""),
        "corte": meta.get("corte", ""),
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
        "images": meta.get("images", []),
        "latitude": meta.get("latitude", ""),
        "longitude": meta.get("longitude", "")
    })

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
