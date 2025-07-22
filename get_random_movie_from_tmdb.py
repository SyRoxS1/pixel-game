import requests
import random
import os


with open('secret_tmdb_key', 'r') as file:
    API_KEY = file.read().strip()



def get_official_poster(movie_id, api_key):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/images'
    headers = {'Authorization': f'Bearer {api_key}'}
    params = {'language': 'en-US', 'include_image_language': 'en,null'}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")

    posters = response.json().get('posters', [])
    if not posters:
        return None

    # Sort by vote_count (or vote_average) to find the most "official"
    posters.sort(key=lambda p: (p['vote_count'], p['vote_average']), reverse=True)

    # Use the highest-rated English (or null) poster
    best_poster = posters[0]
    file_path = best_poster['file_path']
    full_url = f'https://image.tmdb.org/t/p/original{file_path}'

    return full_url

def get_random_popular_movie_id(api_key):
    # First, get the total number of pages (up to 500 max for popular endpoint)
    url = 'https://api.themoviedb.org/3/movie/popular'
    headers = {'Authorization': f'Bearer {api_key}'}
    params = {'language': 'en-US', 'page': 1}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")

    data = response.json()
    total_pages = min(data['total_pages'], 500)  # TMDB only allows up to 500 pages

    # Randomly choose a page
    random_page = random.randint(1, total_pages)
    params['page'] = random_page

    response = requests.get(url, headers=headers, params=params)
    movies = response.json().get('results', [])
    if not movies:
        return None

    movie = random.choice(movies)
    return movie['id'], movie['title']


def download_movie_poster(movie_id, api_key, save_path='posters'):
    poster_url = get_official_poster(movie_id, api_key)
    if not poster_url:
        print(f"No poster found for movie ID {movie_id}")
        return None

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    response = requests.get(poster_url)
    if response.status_code == 200:
        file_name = f"{movie_id}.jpg"
        file_path = os.path.join(save_path, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path
    else:
        print(f"Failed to download poster: {response.status_code}")
        return None
# Example usage:
movie_id, title = get_random_popular_movie_id(API_KEY)
print(f"Random Top Movie: {title} (ID: {movie_id})")



poster_url = get_official_poster(movie_id, API_KEY)
print("Official Poster URL:", poster_url)
