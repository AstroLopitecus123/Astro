import requests
import json

query = '''
query {
  User(name: "AstroGato14") {
    favourites {
      anime(page: 1, perPage: 1) {
        nodes {
          title { romaji }
          coverImage { large }
        }
      }
    }
  }
}
'''

try:
    res = requests.post('https://graphql.anilist.co', json={'query': query})
    print(json.dumps(res.json(), indent=2))
except Exception as e:
    print('Error:', e)
