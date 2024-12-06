import requests

class AnilistClient:
    
    # This Class used to interact with Anilist GraphQL
    API_URL= 'https://graphql.anilist.co'

    @staticmethod
    def anime_search_by_name(name= ''):
        query = '''
        query ($search: String) {
          Media(search: $search, type: ANIME) {
            id
            title {
              romaji
              english
              native
            }
            genres
            popularity
          }
        }
        '''
        variables= {'search':name}
        try:
            # Make the request to AniList GraphQL API
            response = requests.post(AnilistClient.API_URL, json={'query': query, 'variables': variables})
            response.raise_for_status()
            data = response.json()

            # Return the API response
            return data

        except requests.exceptions.RequestException as e:
            return f"error: {str(e)}"
        
    @staticmethod
    def anime_search_by_genre(genre= None):
        query= '''
        query ($genre: String) {
          Page(page: 1, perPage: 10) { # Define pagination (optional)
            media(genre_in: [$genre], type: ANIME) {
              id
              title {
                romaji
                english
                native
              }
              genres
              popularity
            }
          }
        }

        '''

        variables= {'genre': genre}
        try:
            response = requests.post(AnilistClient.API_URL, json={'query': query, 'variables': variables})
            response.raise_for_status()
            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            return f"error: {str(e)}"