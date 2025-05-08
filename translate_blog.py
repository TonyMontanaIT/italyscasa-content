
import json
import os
import requests
import time

SOURCE_FILE = 'blog/index.json'
TRANSLATED_FILE = 'blog/index_translated.json'
API_URL = 'https://libretranslate.com/translate'

TARGET_LANGS = [
    'en', 'ru', 'lt', 'lv', 'pl', 'fi', 'cs', 'de', 'ar', 'fr', 'es', 'sv'
]

FIELDS_TO_TRANSLATE = [
    'title', 'h1', 'h2', 'text', 'text1', 'text2', 'text3', 'text4', 'text5', 'text6', 'tipo'
]

def translate(text, target):
    if not text.strip():
        return text
    try:
        response = requests.post(API_URL, json={
            "q": text,
            "source": "it",
            "target": target,
            "format": "text"
        })
        data = response.json()
        return data.get("translatedText", text)
    except Exception as e:
        print(f"❌ Errore traducendo '{text}' → {target}: {e}")
        return text


def main():
    with open(SOURCE_FILE, encoding='utf-8') as f:
        source_data = json.load(f)

    if os.path.exists(TRANSLATED_FILE):
        with open(TRANSLATED_FILE, encoding='utf-8') as f:
            translated_data = json.load(f)
    else:
        translated_data = []

    translated_map = {item['slug']: item for item in translated_data}

    for entry in source_data:
        slug = entry['slug']
        base = translated_map.get(slug, entry.copy())

        if 'translations' not in base:
            base['translations'] = {}

        for lang in TARGET_LANGS:
            if lang not in base['translations']:
                base['translations'][lang] = {}

            for field in FIELDS_TO_TRANSLATE:
                original = entry.get(field, '')
                if original and field not in base['translations'][lang]:
                    translated = translate(original, lang)
                    base['translations'][lang][field] = translated
                    print(f"✅ Tradotto {field} → {lang}")
                    time.sleep(1)

        translated_map[slug] = base

    with open(TRANSLATED_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(translated_map.values()), f, ensure_ascii=False, indent=2)

    print("\n✅ File aggiornato:", TRANSLATED_FILE)


if __name__ == '__main__':
    main()
