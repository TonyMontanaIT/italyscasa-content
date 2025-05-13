

import json
from xml.etree.ElementTree import Element, SubElement, ElementTree
from xml.dom import minidom

DOMAIN = "https://italyscasa.com"
LANGS = ["it", "en", "ru", "lt", "lv", "pl", "fi", "cs", "de", "ar", "fr", "es", "sv"]

SITEMAP_FILE = "sitemap.xml"
BLOG_JSON = "blog/index.json"
ANNUNCI_JSON = "anunci/index2.json"
AFFITTI_JSON = "affitti/index.json"  # если будет


def prettify(elem):
    rough_string = ElementTree(elem).write("_temp.xml", encoding="utf-8")
    with open("_temp.xml", "r", encoding="utf-8") as f:
        parsed = minidom.parse(f)
        return parsed.toprettyxml(indent="  ")


def add_url(urlset, path):
    url = SubElement(urlset, "url")
    loc = SubElement(url, "loc")
    loc.text = f"{DOMAIN}{path}"
    for lang in LANGS:
        alt = SubElement(url, "xhtml:link")
        alt.set("rel", "alternate")
        alt.set("hreflang", lang)
        alt.set("href", f"{DOMAIN}{path}")


def main():
    urlset = Element("urlset", {
        "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "xmlns:xhtml": "http://www.w3.org/1999/xhtml"
    })

    # Главные страницы
    static_paths = [
        "/", "/property/", "/blog/", "/valut/", "/cerca/", "/cookies/", "/lavoro/"
    ]
    for path in static_paths:
        add_url(urlset, path)

    # Блог
    with open(BLOG_JSON, encoding="utf-8") as f:
        blog = json.load(f)
        for post in blog:
            add_url(urlset, f"/blogpage/{post['slug']}/")

    # Объявления
    with open(ANNUNCI_JSON, encoding="utf-8") as f:
        annunci = json.load(f)
        for item in annunci:
            rif = item.get("riferimento") or item.get("slug")
            add_url(urlset, f"/anunci/dynamic/?rif={rif}")

    # Опционально: affitti (если есть)
    # with open(AFFITTI_JSON, encoding="utf-8") as f:
    #     affitti = json.load(f)
    #     for item in affitti:
    #         add_url(urlset, f"/affittipage/{item['slug']}/")

    # Сохраняем
    xml_str = prettify(urlset)
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(xml_str)

    print(f"✅ sitemap.xml создан и содержит все языковые версии ({SITEMAP_FILE})")


if __name__ == "__main__":
    main()
