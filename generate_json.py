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
        "images": meta.get("images", [])
    })

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
