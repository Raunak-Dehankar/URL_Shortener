from app.utils import generate_short_code

url_store = {}

def create_short_url(original_url):
    code = generate_short_code()
    url_store[code] = original_url
    return code

def get_original_url(code):
    return url_store.get(code)