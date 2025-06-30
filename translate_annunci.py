import json

INPUT_FILE = "anunci/index2.json"               # берём данные из сгенерированного index2
OUTPUT_FILE = "anunci/index2_translated.json"   # сохраняем в переводной файл

LANGUAGES = ["en", "ru", "lt", "lv", "pl", "fi", "cs", "de", "fr", "es", "sv"]
FIELDS_TO_TRANSLATE = [
    "nomeAnunci", "h1", "h2t1", "h2t2", "h2t3", "h2t4", "h2t5", "h2t6",
    "text1", "text2", "text3", "text4", "text5", "text6",
    "descrizione", "tipo", "arredamenti", "prezzoDescrizione"
]

# Загружаем данные
with open(INPUT_FILE, encoding="utf-8") as f:
    data = json.load(f)

for entry in data:
    # Сохраняем оригинал из итальянского блока
    it_translations = entry.get("translations", {}).get("it", {})
    entry["original"] = {
        field: it_translations.get(field, "") for field in FIELDS_TO_TRANSLATE
    }

    # Готовим пустые переводы
    translations = entry.setdefault("translations", {})
    for lang in LANGUAGES:
        if lang == "it":
            continue  # итальянский — источник, не трогаем
        lang_block = translations.setdefault(lang, {})
        for field in FIELDS_TO_TRANSLATE:
            lang_block.setdefault(field, "")  # если нет — создаём пустое

# Сохраняем результат
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Файл сохранён: {OUTPUT_FILE}")
