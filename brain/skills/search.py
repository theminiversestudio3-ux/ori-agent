from googlesearch import search

def web_search(query, num_results=5):
    try:
        results = search(query, num_results=num_results, advanced=True)
        formatted_results = []
        for r in results:
            formatted_results.append(f"Title: {r.title}\nURL: {r.url}\nSnippet: {r.description}\n")
        return "\n".join(formatted_results) if formatted_results else "No results found."
    except Exception as e:
        return f"Error searching the web: {str(e)}"
