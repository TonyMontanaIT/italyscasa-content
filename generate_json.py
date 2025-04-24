import frontmatter
import json
from pathlib import Path
from datetime import datetime

md_folder = Path("blog")
output_path = md_folder / "index.json"
structured_output_path = md_folder / "structured-blog.json"

data = []
structured_data = []

author = {
    "@type": "Person",
    "name": "Antonio Montano",
    "url": "https://www.instagram.com/tony_montana_it/profilecard/?igsh=eWU3MzBha2swMWVj"
}

now_iso = datetime.now().isoformat()

for file in md_folder.glob("*.md"):
    post = frontmatter.load(file)
    meta = post.metadata

    images_meta = meta.get("images", [])
    images = []
    for item in images_meta:
        if isinstance(item, dict):
            images.append({
                "src": item.get("src", ""),
                "alt": item.get("alt", "")
            })
        elif isinstance(item, str):
            images.append({
                "src": item,
                "alt": ""
            })

    blog_entry = {
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
        "images": images
    }
    data.append(blog_entry)

    first_image = images[0] if images else {"src": "uploads/default.jpg", "alt": ""}
    structured_data.append({
        "@type": "BlogPosting",
        "headline": blog_entry["title"] or blog_entry["h1"],
        "datePublished": now_iso,
        "author": author,
        "image": f"https://tonymontanait.github.io/italyscasa-content/{first_image['src']}",
        "description": blog_entry["text1"] or ""
    })

# Запись index.json
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Запись structured-blog.json
with open(structured_output_path, "w", encoding="utf-8") as f:
    json.dump({
        "@context": "https://schema.org",
        "@graph": structured_data
    }, f, ensure_ascii=False, indent=2)

print("✅ index.json и structured-blog.json обновлены.")
