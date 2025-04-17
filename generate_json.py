import frontmatter
import json
from pathlib import Path

md_folder = Path("blog")
output_path = md_folder / "index.json"

data = []

for file in md_folder.glob("*.md"):
    post = frontmatter.load(file)
    meta = post.metadata
    data.append({
        "slug": meta.get("slug", file.stem),
        "title": meta.get("title", ""),
        "tipo": meta.get("tipo", ""),
        "h1": meta.get("h1", ""),
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
        "phone": meta.get("phone", ""),
        "images": meta.get("images", [])
    })

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
