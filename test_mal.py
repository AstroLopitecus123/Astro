import requests, json, re
try:
    res = requests.get('https://myanimelist.net/animelist/Xinil?status=1', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    print('Status:', res.status_code)
    match = re.search(r'data-items="([^"]+)"', res.text)
    if match:
        data_str = match.group(1).replace('&quot;', '"')
        data = json.loads(data_str)
        print('Found items:', len(data))
        if len(data) > 0: print(data[0]['anime_title'], data[0]['anime_image_path'])
    else:
        print("No match")
except Exception as e:
    print('Error:', e)
