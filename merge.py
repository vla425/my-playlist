import re
import requests

# --- НАСТРОЙКИ ---
PLAYLISTS = [
    "https://www.dropbox.com/scl/fi/gz94zy4gve1kos1ho5tmg/Surgut_RT.m3u?rlkey=hv093gf1qu1jfjogux45tsaiy&st=v4tktgk9&dl=1",
    "https://bit.ly/dimonovich-tv"
]
# Категории для удаления (точное совпадение или часть названия)
BLACKLIST = ["Реклама", "Эротика", "18+", "Для взрослых"]
# -----------------

def should_skip(extinf_line: str) -> bool:
    for word in BLACKLIST:
        # Ищем слово внутри group-title="..." или просто в строке EXTINF
        if re.search(rf'group-title="[^"]*{re.escape(word)}[^"]*"', extinf_line, re.IGNORECASE):
            return True
        if re.search(re.escape(word), extinf_line, re.IGNORECASE):
            return True
    return False

def main():
    out = ["#EXTM3U"]
    
    for url in PLAYLISTS:
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
        except Exception as e:
            print(f"Ошибка загрузки {url}: {e}")
            continue
            
        lines = r.text.splitlines()
        skip = False
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith("#EXTM3U"):
                continue
                
            if line.startswith("#EXTINF"):
                skip = should_skip(line)
                if not skip:
                    out.append(line)
            elif not line.startswith("#"): # Это ссылка на поток
                if not skip:
                    out.append(line)
            else: # Другие теги (#EXTVLCOPT и т.д.)
                if not skip:
                    out.append(line)

    # Сохраняем результат в файл
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Плейлист успешно обновлен!")

if __name__ == "__main__":
    main()
