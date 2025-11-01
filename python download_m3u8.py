import requests
import re
import os

def download_m3u8(streamID):
    target_url = f"https://popcdn.day/on.php?stream={streamID}"

    headers = {
        'Host': 'popcdn.day',
        'Connection': 'keep-alive',
        'User-Agent': 'okhttp/4.12.0',
        'Accept': '*/*',
        'Referer': 'https://freeshot.live/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    resp = requests.get(target_url, headers=headers)
    resp.raise_for_status()

    html = resp.text.replace('embed.html', 'tracks-v1/index.fmp4.m3u8').replace('&remote=no_check_ip', '')

    match = re.search(r'frameborder="0" src="(.*?)"', html)
    if not match:
        raise Exception("Stream link bulunamadı!")

    stream_link = match.group(1)

    m3u8_resp = requests.get(stream_link)
    m3u8_resp.raise_for_status()

    filename = f"{streamID}.m3u8"
    with open(filename, "w") as f:
        f.write(m3u8_resp.text)

    print(f"{filename} başarıyla indirildi!")

if __name__ == "__main__":
    streamID = os.getenv("STREAM_ID", "").strip()
    if not streamID:
        print("ID girilmedi. Çıkılıyor...")
    else:
        download_m3u8(streamID)
