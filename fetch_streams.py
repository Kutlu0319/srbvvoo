import os
import json
import requests

API_URL = os.getenv("API_URL", "https://api.bilyonersport.com/channel/")
API_KEY = os.getenv("eyJ1c2VySWQiOiJhZG1pbiJ9.cGGCvhLTzbal5oMubTkExL_8I9mJoLnM8mTR93O4as86P9OE8n2WaVFyr3UoEwrf5F5IqpXcjE2LPUmXTAR06w")

if not API_KEY:
    raise EnvironmentError("BILYONER_API_KEY environment variable is not set.")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

streams = [
    {"streaming_name": "BEIN SPORTS 1", "slug-code": "n2c7b8bfb"},
    {"streaming_name": "BEIN SPORTS 2", "slug-code": "n2c7b18f1"},
    {"streaming_name": "BEIN SPORTS 3", "slug-code": "n2c7aa492"},
    {"streaming_name": "BEIN SPORTS 4", "slug-code": "n2c7a3033"},
    {"streaming_name": "BEIN SPORTS 5", "slug-code": "n2c79bbd4"},
    {"streaming_name": "BEIN SPORTS MAX 1", "slug-code": "55ccbf54"},
    {"streaming_name": "BEIN SPORTS MAX 2", "slug-code": "63d9743a"},
    {"streaming_name": "S SPORT", "slug-code": "532e343d"},
    {"streaming_name": "SMARTSPOR", "slug-code": "25c8edb5"},
    {"streaming_name": "SMARTSPOR 2", "slug-code": "n6ca39dcf"},
    {"streaming_name": "TIVIBU SPOR 1", "slug-code": "n3e79302e"},
    {"streaming_name": "TIVIBU SPOR 2", "slug-code": "n3e78bbcf"},
    {"streaming_name": "TIVIBU SPOR 3", "slug-code": "n3e784770"},
    {"streaming_name": "TIVIBU SPOR 4", "slug-code": "n3e77d311"},
    {"streaming_name": "TRT SPOR", "slug-code": "4fb22bd4"},
    {"streaming_name": "TRT SPOR Yıldız", "slug-code": "n166ce315"},
    {"streaming_name": "TRT 1", "slug-code": "n4dcaecdd"},
    {"streaming_name": "A SPOR", "slug-code": "n4f37cc01"},
    {"streaming_name": "ATV", "slug-code": "n22d1a1c9"},
    {"streaming_name": "KANAL D", "slug-code": "n18c3ac0d"},
    {"streaming_name": "TV 8", "slug-code": "n257021c"},
    {"streaming_name": "TV 8,5", "slug-code": "381d3cbd"},
    {"streaming_name": "NBA TV", "slug-code": "50d04f64"},
    {"streaming_name": "EURO SPORT 1", "slug-code": "n43db7ec"},
    {"streaming_name": "EURO SPORT 2", "slug-code": "n43d438d"}
]

results = {}
m3u_lines = ['#EXTM3U']

for stream in streams:
    name = stream["streaming_name"]
    slug = stream["slug-code"]
    url = f"{API_URL}{slug}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Değişken ismi API'den alınan yanıta göre güncellenebilir!
        stream_url = data.get("stream_url") or data.get("url") or data.get("link")

        if not stream_url:
            print(f"⚠️  {name}: Stream URL bulunamadı.")
            results[slug] = {"name": name, "error": "Stream URL not found"}
            continue

        # JSON çıktıya ekle
        results[slug] = {
            "name": name,
            "url": stream_url
        }

        # M3U satırı oluştur
        m3u_lines.append(f'#EXTINF:-1 tvg-name="{name}" group-title="Sports",{name}')
        m3u_lines.append(stream_url)

    except Exception as e:
        print(f"❌ {name} için hata: {e}")
        results[slug] = {"name": name, "error": str(e)}

# JSON çıktısını yaz
with open("fetch_output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

# M3U dosyasını yaz
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(m3u_lines))

print("✅ fetch_output.json ve playlist.m3u oluşturuldu.")

