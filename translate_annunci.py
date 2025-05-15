import json
import os
import requests
import time

SOURCE_FILE = 'anunci/index2.json'
TRANSLATED_FILE = 'anunci/index2_translated.json'
API_URL = 'https://translate-api.italyscasa-api.workers.dev'

TARGET_LANGS = [
    'en', 'ru', 'lt', 'lv', 'pl', 'fi', 'cs', 'de', 'ar', 'fr', 'es', 'sv'
]

FIELDS_TO_TRANSLATE = [
    'nomeAnunci', 'h1', 'h2t1', 'h2t2', 'h2t3', 'h2t4', 'h2t5', 'h2t6',
    'text1', 'text2', 'text3', 'text4', 'text5', 'text6',
    'descrizione', 'tipo', 'arredamenti'
]

CHUNK_SIZE = 200
CHUNK_PAUSE = 3
ENTRY_PAUSE = 10
MAX_RETRIES = 3

def split_text(text, size=CHUNK_SIZE):
    return [text[i:i+size] for i in range(0, len(text), size)]

def translate(text, target, field=""):
    chunks = split_text(text)
    translated_chunks = []

    for chunk in chunks:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(f"[DEBUG] Sending → lang: {target}, field: {field}, chunk: {chunk[:100]}")
                response = requests.post(API_URL, json={
                    "text": chunk,
                    "sourceLang": "it",
                    "targetLang": target
                }, timeout=50)
                response.raise_for_status()
                data = response.json()
                translated = data.get("translatedText", "").strip()
                if translated:
                    translated_chunks.append(translated)
                    break
                else:
                    print(f"⚠️ Empty translation (try {attempt}) for chunk → {target}")
            except Exception as e:
                print(f"⚠️ Retry {attempt}/{MAX_RETRIES} for chunk → {target} due to error: {e}")
                time.sleep(CHUNK_PAUSE)
        else:
            print(f"❌ Final failure for chunk → {target}")
            translated_chunks.append(chunk)
        time.sleep(CHUNK_PAUSE)

    return ' '.join(translated_chunks)




def main():
    with open(SOURCE_FILE, encoding='utf-8') as f:
        source_data = json.load(f)

    if os.path.exists(TRANSLATED_FILE):
        with open(TRANSLATED_FILE, encoding='utf-8') as f:
            translated_data = json.load(f)
    else:
        translated_data = []

    translated_map = {item['riferimento']: item for item in translated_data}

    for i, entry in enumerate(source_data):
        rif = entry['riferimento']
        base = translated_map.get(rif, entry.copy())

        if 'translations' not in base:
            base['translations'] = {}

        if 'it' not in base['translations']:
            base['translations']['it'] = {}

        for lang in TARGET_LANGS:
            if lang not in base['translations']:
                base['translations'][lang] = {}

            for field in FIELDS_TO_TRANSLATE:
                original = entry.get(field, '')
                base['translations']['it'][field] = original

                prev_original = base['translations']['it'].get(field, '')
                if (
                    field in base['translations'][lang]
                    and original == prev_original
                ):
                    continue

                if original:
                    translated = translate(original, lang)
                    base['translations'][lang][field] = translated
                    print(f"[{i+1}/{len(source_data)}] {rif} — {field} → {lang}: OK")

        translated_map[rif] = base

        with open(TRANSLATED_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(translated_map.values()), f, ensure_ascii=False, indent=2)

        time.sleep(ENTRY_PAUSE)

    print("\n✅ Translated file saved:", TRANSLATED_FILE)

if __name__ == '__main__':
    main()
