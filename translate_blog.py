import json
import os
import time

SOURCE_FILE = 'blog/index.json'
TRANSLATED_FILE = 'blog/index_translated.json'

TARGET_LANGS = [
    'en', 'ru', 'lt', 'lv', 'pl', 'fi', 'cs', 'de', 'ar', 'fr', 'es', 'sv'
]

FIELDS_TO_TRANSLATE = [
    'title', 'h1', 'h2', 'text', 'text1', 'text2', 'text3', 'text4', 'text5', 'text6', 'tipo'
]

ENTRY_PAUSE = 10

def main():
    with open(SOURCE_FILE, encoding='utf-8') as f:
        source_data = json.load(f)

    if os.path.exists(TRANSLATED_FILE):
        with open(TRANSLATED_FILE, encoding='utf-8') as f:
            translated_data = json.load(f)
    else:
        translated_data = []

    translated_map = {item['slug']: item for item in translated_data}

    for i, entry in enumerate(source_data):
        slug = entry['slug']
        base = translated_map.get(slug, entry.copy())

        if 'translations' not in base:
            base['translations'] = {}

        if 'it' not in base['translations']:
            base['translations']['it'] = {}

        updated = False

        for field in FIELDS_TO_TRANSLATE:
            new_val = entry.get(field, '')
            old_val = base['translations']['it'].get(field, '')

            if new_val != old_val:
                base['translations']['it'][field] = new_val
                updated = True
                for lang in TARGET_LANGS:
                    if lang not in base['translations']:
                        base['translations'][lang] = {}
                    base['translations'][lang][field] = new_val  # пока без реального перевода
                print(f"[{i+1}/{len(source_data)}] {slug} — {field}: UPDATED")
            else:
                print(f"[{i+1}/{len(source_data)}] {slug} — {field}: SKIPPED")

        translated_map[slug] = base

        if updated:
            with open(TRANSLATED_FILE, 'w', encoding='utf-8') as f:
                json.dump(list(translated_map.values()), f, ensure_ascii=False, indent=2)

            time.sleep(ENTRY_PAUSE)

    print("\n✅ Translated file saved:", TRANSLATED_FILE)

if __name__ == '__main__':
    main()
