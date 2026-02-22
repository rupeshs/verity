import requests


# https://docs.searxng.org/dev/search_api.html
def search_query(
    query: str,
    num_results: int = 10,
    searxng_base_url: str = "http://localhost:8080",
):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Referer": "http://localhost:8080/",
    }
    query = f"{query} -filetype:pdf -filetype:doc -filetype:docx -filetype:ppt -filetype:pptx -site:spotify.com"
    params = {
        "q": query,
        "format": "json",
        "language": "en",
        "categories": ["general"],
        "safesearch": 0,
        # "engines": ["google"],
    }
    try:
        searxng_url = f"{searxng_base_url}/search"
        response = requests.post(
            searxng_url, headers=headers, params=params, timeout=10
        )
        response.raise_for_status()
        results = response.json()["results"]
    except requests.exceptions.Timeout:
        raise Exception("SearXNG request timed out,please ensure it is running")
    except requests.exceptions.ConnectionError:
        raise Exception("Could not connect to SearXNG,please ensure it is running")
    except Exception as e:
        raise Exception(f"Unexpected error in search: {e}")

    return results[:num_results]
