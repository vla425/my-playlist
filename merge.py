import requests
import sys

# --- ВАШИ ССЫЛКИ ---
PLAYLISTS = [
    "https://www.dropbox.com/scl/fi/gz94zy4gve1kos1ho5tmg/Surgut_RT.m3u?rlkey=hv093gf1qu1jfjogux45tsaiy&st=v4tktgk9&dl=1",
    "https://raw.githubusercontent.com/Dimonovich/TV/Dimonovich/FREE/TV"
]

# Категории для удаления (можно добавлять свои через запятую)
BLACKLIST = ["Реклама", "Эротика", "18+", "Для взрослых"]
# -------------------

print("--- НАЧАЛО РАБОТЫ СКРИПТА ---")
out = ["#EXTM3U"]
success_count = 0

for url in PLAYLISTS:
    print(f"\nПытаюсь скачать: {url}")
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        
        # ОТЛАДКА: Показываем первые 100 символов скачанного файла
        preview = r.text[:100].replace('\n', ' ').replace('\r', '')
        print(f"🔍 Начало скачанного файла: '{preview}'")
        
        if not r.text.strip().startswith("#EXTM3U"):
            print("⚠️ ВНИМАНИЕ: Файл не начинается с #EXTM3U. Возможно, ссылка ведет на HTML-страницу, а не на плейлист.")
        
        lines = r.text.splitlines()
        skip = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#EXTM3U"):
                continue
                
            if line.startswith("#EXTINF"):
                skip = any(word.lower() in line.lower() for word in BLACKLIST)
                if not skip:
                    out.append(line)
            elif not line.startswith("#"): # Ссылка на поток
                if not skip:
                    out.append(line)
            else: # Другие теги
                if not skip:
                    out.append(line)
                    
        success_count += 1
        print(f"✅ Успешно обработан.")
        
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")

print(f"\n--- ИТОГ: Обработано плейлистов: {success_count} из {len(PLAYLISTS)} ---")

if success_count == 0:
    print("❌ СКРИПТ ПРЕРВАН: Не удалось скачать ни одного плейлиста.")
    sys.exit(1)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("✅ Файл playlist.m3u успешно создан и сохранен!")
