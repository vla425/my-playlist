import re
import requests
import sys

# --- НАСТРОЙКИ: ЗАМЕНИТЕ ССЫЛКИ НА РЕАЛЬНЫЕ ---
PLAYLISTS = [
    "https://www.dropbox.com/scl/fi/gz94zy4gve1kos1ho5tmg/Surgut_RT.m3u?rlkey=hv093gf1qu1jfjogux45tsaiy&st=v4tktgk9&dl=1",
    "https://raw.githubusercontent.com/Dimonovich/TV/Dimonovich/FREE/TV"
]
BLACKLIST = ["Реклама", "Эротика", "18+", "Для взрослых"]
# -----------------------------------------------

def should_skip(extinf_line: str) -> bool:
    for word in BLACKLIST:
        if re.search(rf'group-title="[^"]*{re.escape(word)}[^"]*"', extinf_line, re.IGNORECASE):
            return True
        if re.search(re.escape(word), extinf_line, re.IGNORECASE):
            return True
    return False

def main():
    out = ["#EXTM3U"]
    success_count = 0
    
    for url in PLAYLISTS:
        try:
            print(f"Скачиваю: {url}")
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            
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
                elif not line.startswith("#"): 
                    if not skip:
                        out.append(line)
                else: 
                    if not skip:
                        out.append(line)
            success_count += 1
            print(f"Успешно: {url}")
        except Exception as e:
            print(f"ОШИБКА загрузки {url}: {e}")
            
    if success_count == 0:
        print("КРИТИЧЕСКАЯ ОШИБКА: Не удалось скачать ни один плейлист!")
        sys.exit(1) # Принудительно останавливаем с понятной ошибкой

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("Плейлист успешно создан!")

if __name__ == "__main__":
    main()
