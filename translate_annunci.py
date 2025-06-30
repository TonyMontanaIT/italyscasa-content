import json
import os

INPUT_FILE = "anunci/index2.json"
TRANSLATED_FILE = "anunci/index2_translated.json"

LANGUAGES = ["en", "ru", "lt", "lv", "pl", "fi", "cs", "de", "fr", "es", "sv"]
FIELDS_TO_TRANSLATE = [
    "nomeAnunci", "h1", "h2t1", "h2t2", "h2t3", "h2t4", "h2t5", "h2t6",
    "text1", "text2", "text3", "text4", "text5", "text6",
    "descrizione", "tipo", "arredamenti", "prezzoDescrizione"
]

# Загрузка уже переведённого файла
if os.path.exists(TRANSLATED_FILE):
    with open(TRANSLATED_FILE, encoding="utf-8") as f:
        translated_data = json.load(f)
else:
    translated_data = []

# Создаём карту уже существующих slug'ов
existing_slugs = {entry["slug"]: entry for entry in translated_data}

# Загружаем свежий список всех объявлений
with open(INPUT_FILE, encoding="utf-8") as f:
    new_data = json.load(f)

added = 0

for entry in new_data:
    slug = entry.get("slug")
    if not slug:
        continue

    if slug in existing_slugs:
        continue  # Уже есть — пропускаем

    # Генерация original
    it_translations = entry.get("translations", {}).get("it", {})
    original = {field: it_translations.get(field, "") for field in FIELDS_TO_TRANSLATE}

    # Генерация translations
    translations = {}
    for lang in LANGUAGES:
        translations[lang] = {field: "" for field in FIELDS_TO_TRANSLATE}
    translations["it"] = it_translations

    new_entry = {
        **entry,
        "original": original,
        "translations": translations
    }

    translated_data.append(new_entry)
    added += 1
    print(f"➕ Добавлено новое объявление: {slug}")

# Сохраняем итог
with open(TRANSLATED_FILE, "w", encoding="utf-8") as f:
    json.dump(translated_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Добавлено новых: {added}")
print(f"✅ Файл обновлён: {TRANSLATED_FILE}")
