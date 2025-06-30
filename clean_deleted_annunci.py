import json

INPUT_CURRENT = "anunci/index2.json"
INPUT_TRANSLATED = "anunci/index2_translated.json"
OUTPUT_TRANSLATED = "anunci/index2_translated.json"

# Загружаем актуальные объявления (source)
with open(INPUT_CURRENT, encoding="utf-8") as f:
    current_data = json.load(f)
current_slugs = {entry["slug"] for entry in current_data}

# Загружаем переведённые (старые) данные
with open(INPUT_TRANSLATED, encoding="utf-8") as f:
    translated_data = json.load(f)

# Фильтруем только существующие
cleaned_data = [entry for entry in translated_data if entry["slug"] in current_slugs]

removed = len(translated_data) - len(cleaned_data)

# Сохраняем
with open(OUTPUT_TRANSLATED, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

print(f"🧹 Удалено устаревших объявлений: {removed}")
print(f"✅ Обновлён файл: {OUTPUT_TRANSLATED}")
