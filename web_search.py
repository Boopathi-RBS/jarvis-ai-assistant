import webbrowser

def search_web(query):

    query = query.replace("search ", "")

    url = (
        "https://www.google.com/search?q="
        + query
    )

    webbrowser.open(url)

    return f"Searching Google for: {query}"