
import json
import sys

INDEX_FILE = "index.jsonl"

def search(query):
    results = []

    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as file:
            for line in file:
                page = json.loads(line)

                title = page.get("title", "")
                url = page.get("url", "")

                if query.lower() in title.lower():
                    results.append({
                        "title": title,
                        "url": url
                    })

    except FileNotFoundError:
        print("OMNINX INDEX NOT FOUND")
        return []

    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("OMNINX SEARCH: ")

    results = search(query)

    print("\nOMNINX SEARCH RESULTS")
    print("---------------------")

    if results:
        for page in results:
            print("\n" + page["title"])
            print(page["url"])
    else:
        print("No results found.")
