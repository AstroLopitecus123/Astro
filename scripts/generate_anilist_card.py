import requests
import json
import base64
import re
import os

def get_anilist_data(username):
    # Try fetching Currently Watching first
    query = '''
    query ($username: String) {
      MediaListCollection(userName: $username, type: ANIME, status: CURRENT) {
        lists {
          entries {
            media {
              title { romaji }
              coverImage { large }
              format
              seasonYear
              siteUrl
            }
          }
        }
      }
    }
    '''
    res = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': {'username': username}})
    data = res.json()
    try:
        anime = data['data']['MediaListCollection']['lists'][0]['entries'][0]['media']
        label = "Viendo actualmente en"
        return anime, label
    except:
        # Fallback to Favorites
        query = '''
        query ($username: String) {
          User(name: $username) {
            favourites {
              anime(page: 1, perPage: 1) {
                nodes {
                  title { romaji }
                  coverImage { large }
                  format
                  seasonYear
                  siteUrl
                }
              }
            }
          }
        }
        '''
        res = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': {'username': username}})
        data = res.json()
        label = "Anime favorito en"
        anime = data['data']['User']['favourites']['anime']['nodes'][0]
        return anime, label

try:
    anime, label = get_anilist_data("AstroGato14")
    title = anime['title']['romaji']
    cover_url = anime['coverImage']['large']
    year = anime.get('seasonYear') or ''
    fmt = anime.get('format') or ''
    subtitle = f"{fmt} - {year}" if year else fmt
    anilist_url = anime['siteUrl']

    img_data = requests.get(cover_url).content
    b64_img = base64.b64encode(img_data).decode('utf-8')
    mime_type = "image/jpeg" if ".jpg" in cover_url or ".jpeg" in cover_url else "image/png"

    with open('assets/spotify.svg', 'r', encoding='utf-8') as f:
        svg = f.read()

    # Replacements
    svg = re.sub(r'Now playing on', label, svg)
    # The spotify logo SVG path removal:
    svg = re.sub(r'<svg viewBox="0 0 16 16" width="16" height="16" xmlns="http://www.w3.org/2000/svg">.*?</svg>', '<b>AniList</b>', svg, flags=re.DOTALL)
    
    # Replace texts
    svg = re.sub(r'Moonlight Sonata 3rd Movement', title, svg)
    svg = re.sub(r'Ludwig van Beethoven', subtitle, svg)

    # Replace URLs
    svg = re.sub(r'https://open\.spotify\.com/track/[^"]+', anilist_url, svg)
    svg = re.sub(r'https://open\.spotify\.com/artist/[^"]+', anilist_url, svg)

    # Replace Image
    svg = re.sub(r'data:image/[^;]+;base64,[a-zA-Z0-9+/=]+', f'data:{mime_type};base64,{b64_img}', svg)

    # Replace Colors
    svg = svg.replace('rgb(30, 215, 96)', 'rgb(2, 169, 255)')
    svg = svg.replace('rgb(62,185,201)', 'rgb(2, 169, 255)') 
    svg = svg.replace('rgb(57,139,151)', 'rgb(2, 120, 200)') 

    with open('assets/anilist_custom.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("AniList custom SVG generated successfully!")
except Exception as e:
    print("Error:", e)
