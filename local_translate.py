import json
import requests
import time

INPUT_FILE = "anunci/index2_translated.json"
OUTPUT_FILE = "anunci/index2_translated.json"
TRANSLATE_URL = "http://localhost:5000/translate"

LANGUAGES = ["en", "ru", "lt", "lv", "pl", "fi", "cs", "de", "fr", "es", "sv"]
FIELDS_TO_TRANSLATE = [
    "nomeAnunci", "h1", "h2t1", "h2t2", "h2t3", "h2t4", "h2t5", "h2t6",
    "text1", "text2", "text3", "text4", "text5", "text6",
    "descrizione", "tipo", "arredamenti", "prezzoDescrizione"
]

CHUNK_SIZE = 400
PAUSE_BETWEEN_REQUESTS = 3
PAUSE_BETWEEN_ENTRIES = 10
RETRY_COUNT = 3

def chunk_text(text, size=CHUNK_SIZE):
    text = text.strip()
    return [text[i:i+size] for i in range(0, len(text), size)]

def translate_chunked(text, lang):
    chunks = chunk_text(text)
    translated_chunks = []

    for chunk in chunks:
        for attempt in range(RETRY_COUNT):
            try:
                r = requests.post(TRANSLATE_URL, json={
                    "q": chunk,
                    "source": "auto",
                    "target": lang,
                    "format": "text"
                }, timeout=10)
                r.raise_for_status()
                result = r.json()
                translated_text = result.get("translatedText", "")
                if translated_text is None:
                    raise ValueError("Получен None от переводчика")
                translated_chunks.append(translated_text)
                time.sleep(PAUSE_BETWEEN_REQUESTS)
                break
            except Exception as e:
                print(f"❌ Ошибка (попытка {attempt+1}/{RETRY_COUNT}) для языка {lang}: {e}")
                time.sleep(2)
        else:
            translated_chunks.append(chunk)  # fallback: оригинал

    return ''.join(t if t is not None else "" for t in translated_chunks)

def save_data(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("💾 Прогресс сохранён")

# Загрузка данных
with open(INPUT_FILE, encoding="utf-8") as f:
    data = json.load(f)

# 🧩 Генерация original из translations.it
for entry in data:
    if "original" not in entry:
        entry["original"] = {}

    it_translations = entry.get("translations", {}).get("it", {})
    for field in FIELDS_TO_TRANSLATE:
        if field in it_translations and not entry["original"].get(field):
            entry["original"][field] = it_translations[field]

# Перевод
for idx, entry in enumerate(data):
    original = entry.get("original", {})
    translations = entry.setdefault("translations", {})
    slug = entry.get("slug", f"[{idx}]")

    for lang in LANGUAGES:
        lang_block = translations.setdefault(lang, {})
        updated = False

        for key in FIELDS_TO_TRANSLATE:
            if key in original:
                original_text = original[key]
                existing_translation = lang_block.get(key, "").strip()

                if not existing_translation:
                    print(f"🔤 [{slug}] Перевод {key} → {lang}")
                    translated = translate_chunked(original_text, lang)
                    lang_block[key] = translated
                    updated = True

        if updated:
            print(f"✅ Обновлено: {slug} → {lang}")
            save_data(data)  # сохраняем после каждой обновлённой языковой секции
            time.sleep(PAUSE_BETWEEN_ENTRIES)

print(f"\n✅ Всё готово! Финальный файл сохранён: {OUTPUT_FILE}")
