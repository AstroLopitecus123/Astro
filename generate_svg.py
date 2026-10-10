from PIL import Image
import base64
import urllib.request
from io import BytesIO
import re

# Fetch original SVG
req = urllib.request.Request('https://novatorem2-nu.vercel.app/api/orchestrator?background_color=0d1117&border_color=FFA2FE', headers={'User-Agent': 'Mozilla/5.0'})
svg = urllib.request.urlopen(req).read().decode('utf-8')

img = Image.open(r'C:\Users\USER\.gemini\antigravity\brain\17dd5471-1603-40d4-8355-8836ab0203ac\beethoven_cover_1791600528130.jpg')
img = img.crop((120, 120, 890, 890))
img = img.resize((150, 150))
buffer = BytesIO()
img.save(buffer, format='JPEG', quality=85)
b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

svg = re.sub(r'<div class="song [^>]+>.*?</div>', r'<div class="song " title="Moonlight Sonata 3rd Movement">\nMoonlight Sonata 3rd Movement</div>', svg, flags=re.DOTALL)
svg = re.sub(r'<div class="artist [^>]+>.*?</div>', r'<div class="artist " title="Ludwig van Beethoven">\nLudwig van Beethoven</div>', svg, flags=re.DOTALL)
svg = re.sub(r'data:image/jpeg;base64,[^\"]+', f'data:image/jpeg;base64,{b64}', svg)

with open('assets/spotify.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
print('Done!')
