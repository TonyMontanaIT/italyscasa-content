import json, os, requests, time

SOURCE_FILE = 'anunci/index2.json'
TRANSLATED_FILE = 'anunci/index2_translated.json'
API_URL = 'https://libretranslate-railway-production-e5c2.up.railway.app/translate'

TARGET_LANGS = ['en', 'ru', 'lt', 'lv', 'pl', 'fi', 'cs', 'de', 'ar', 'fr', 'es', 'sv']
FIELDS_TO_TRANSLATE = [
    'nomeAnunci', 'h1', 'h2t1', 'h2t2', 'h2t3', 'h2t4', 'h2t5', 'h2t6',
    'text1', 'text2', 'text3', 'text4', 'text5', 'text6',
    'descrizione', 'tipo', 'arredamenti'
]

def smart_split(text, max_length=400):
    parts, buffer = [], ''
    for sentence in text.split('. '):
        if len(buffer) + len(sentence) + 1 <= max_length:
            buffer += sentence + '. '
        else:
            parts.append(buffer.strip())
            buffer = sentence + '. '
    if buffer: parts.append(buffer.strip())
    return parts

def translate_chunk(text, target):
    for attempt in range(1, 4):
        try:
            response = requests.post(API_URL, json={
                "q": text, "source": "it", "target": target, "format": "text"
            }, timeout=50)
            response.raise_for_status()
            result = response.json().get("translatedText", "").strip()
            if result: return result
        except Exception as e:
            print(f"⚠️ Retry {attempt}/3 for chunk → {target}: {e}")
            time.sleep(2)
    return text

def translate_text(text, target):
    return ' '.join([translate_chunk(part, target) for part in smart_split(text)])

def main():
    with open(SOURCE_FILE, encoding='utf-8') as f:
        source = json.load(f)

    if os.path.exists(TRANSLATED_FILE):
        with open(TRANSLATED_FILE, encoding='utf-8') as f:
            translated = json.load(f)
    else:
        translated = []

    result_map = {item['riferimento']: item for item in translated}

    for i, entry in enumerate(source):
        rif = entry['riferimento']
        base = result_map.get(rif, entry.copy())
        base.setdefault('translations', {})

        for lang in TARGET_LANGS:
            base['translations'].setdefault(lang, {})
            for field in FIELDS_TO_TRANSLATE:
                if field not in base['translations'][lang] and entry.get(field):
                    translated = translate_text(entry[field], lang)
                    base['translations'][lang][field] = translated
                    print(f"[{i+1}/{len(source)}] {rif} — {field} → {lang}: OK")
                    time.sleep(3)

        result_map[rif] = base

    with open(TRANSLATED_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(result_map.values()), f, ensure_ascii=False, indent=2)

    print("\n✅ Translated file saved:", TRANSLATED_FILE)

if __name__ == '__main__':
    main()
