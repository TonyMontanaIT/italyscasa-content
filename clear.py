import json

TRANSLATED_FILE = 'anunci/index2_translated.json'

TARGET_LANGS = [
    'en', 'ru', 'lt', 'lv', 'pl', 'fi', 'cs', 'de', 'ar', 'fr', 'es', 'sv'
]

FIELDS_TO_TRANSLATE = [
    'nomeAnunci', 'h1', 'h2t1', 'h2t2', 'h2t3', 'h2t4', 'h2t5', 'h2t6',
    'text1', 'text2', 'text3', 'text4', 'text5', 'text6',
    'descrizione', 'tipo', 'arredamenti', 'prezzoDescrizione'
]

def main():
    # Загружаем уже переведённые данные
    with open(TRANSLATED_FILE, encoding='utf-8') as f:
        translated_data = json.load(f)

    for i, entry in enumerate(translated_data):
        rif = entry.get('riferimento', 'unknown')

        print(f"[{i+1}/{len(translated_data)}] {rif} — очищаю переводы...")

        if 'translations' not in entry:
            entry['translations'] = {}

        for lang in TARGET_LANGS:
            if lang not in entry['translations']:
                entry['translations'][lang] = {}

            lang_dict = entry['translations'][lang]

            for field in FIELDS_TO_TRANSLATE:
                lang_dict[field] = ""  # Очищаем поле

    # Сохраняем обновлённый файл
    with open(TRANSLATED_FILE, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)

    print("\n✅ Все переводы очищены. Файл сохранён:", TRANSLATED_FILE)

if __name__ == '__main__':
    main()