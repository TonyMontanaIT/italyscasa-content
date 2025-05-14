import json
import os
import requests
import time

SOURCE_FILE = 'blog/index.json'
TRANSLATED_FILE = 'blog/index_translated.json'
API_URL = 'https://libretranslate-railway-production-e5c2.up.railway.app/translate'

TARGET_LANGS = [
    'en', 'ru', 'lt', 'lv', 'pl', 'fi', 'cs', 'de', 'ar', 'fr', 'es', 'sv'
]

FIELDS_TO_TRANSLATE = [
    'title', 'h1', 'h2', 'text', 'text1', 'text2', 'text3', 'text4', 'text5', 'text6', 'tipo'
]

CHUNK_SIZE = 400
RETRY_LIMIT = 3
DELAY_BETWEEN_CHUNKS = 3
DELAY_BETWEEN_REQUESTS = 10

def chunk_text(text, size):
    return [text[i:i+size] for i in range(0, len(text), size)]

def translate(text, target):
    if not text.strip():
        return text
    chunks = chunk_text(text, CHUNK_SIZE)
    translated_chunks = []

    for chunk in chunks:
        for attempt in range(RETRY_LIMIT):
            try:
                response = requests.post(API_URL, json={
                    "q": chunk,
                    "source": "it",
                    "target": target,
                    "format": "text"
                }, timeout=50)
                response.raise_for_status()
                data = response.json()
                translated = data.get("translatedText", "").strip()
                if translated:
                    translated_chunks.append(translated)
                else:
                    print(f"⚠️ Empty translation for chunk → {target}")
                    translated_chunks.append(chunk)
                time.sleep(DELAY_BETWEEN_CHUNKS)
                break
            except Exception as e:
                print(f"⚠️ Retry {attempt+1}/{RETRY_LIMIT} for chunk → {target} due to error: {e}")
                if attempt == RETRY_LIMIT - 1:
                    translated_chunks.append(chunk)
                time.sleep(DELAY_BETWEEN_CHUNKS)

    return ' '.join(translated_chunks)

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

        for lang in TARGET_LANGS:
            if lang not in base['translations']:
                base['translations'][lang] = {}

            for field in FIELDS_TO_TRANSLATE:
                original = entry.get(field, '')
                if original and field not in base['translations'][lang]:
                    translated = translate(original, lang)
                    base['translations'][lang][field] = translated
                    print(f"[{i+1}/{len(source_data)}] {slug} — {field} → {lang}: OK")
                    time.sleep(DELAY_BETWEEN_REQUESTS)

        translated_map[slug] = base

    with open(TRANSLATED_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(translated_map.values()), f, ensure_ascii=False, indent=2)

    print("\n✅ Translated file saved:", TRANSLATED_FILE)

if __name__ == '__main__':
    main()
