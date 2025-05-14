import json
import os
import requests
import time

SOURCE_FILE = 'anunci/index2.json'
TRANSLATED_FILE = 'anunci/index2_translated.json'
API_URL = 'https://libretranslate-railway-production-e5c2.up.railway.app/translate'

TARGET_LANGS = [
    'en', 'ru', 'lt', 'lv', 'pl', 'fi', 'cs', 'de', 'ar', 'fr', 'es', 'sv'
]

FIELDS_TO_TRANSLATE = [
    'nomeAnunci', 'h1', 'h2t1', 'h2t2', 'h2t3', 'h2t4', 'h2t5', 'h2t6',
    'text1', 'text2', 'text3', 'text4', 'text5', 'text6',
    'descrizione', 'tipo', 'arredamenti'
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
        }, timeout=50)
        response.raise_for_status()
        data = response.json()
        translated = data.get("translatedText", "").strip()
        if translated:
            return translated
        else:
            print(f"⚠️ Empty translation for '{text}' → {target}")
            return text
    except Exception as e:
        print(f"❌ Error translating '{text}' → {target}: {e}")
        return text

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

        for lang in TARGET_LANGS:
            if lang not in base['translations']:
                base['translations'][lang] = {}

            for field in FIELDS_TO_TRANSLATE:
                original = entry.get(field, '')
                if original and field not in base['translations'][lang]:
                    translated = translate(original, lang)
                    base['translations'][lang][field] = translated
                    print(f"[{i+1}/{len(source_data)}] {rif} — {field} → {lang}: OK")
                    time.sleep(1.5)  # чуть больше пауза для стабильности

        translated_map[rif] = base

    with open(TRANSLATED_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(translated_map.values()), f, ensure_ascii=False, indent=2)

    print("\n✅ Translated file saved:", TRANSLATED_FILE)


if __name__ == '__main__':
    main()
