import requests
from bs4 import BeautifulSoup

parks = {
    "yellowstone": [
        "https://www.nps.gov/yell/learn/nature/animals.htm",
        "https://www.nps.gov/yell/learn/nature/mammals.htm",
        "https://www.nps.gov/yell/planyourvisit/camping.htm",
        "https://www.nps.gov/yell/planyourvisit/hiking.htm",
        "https://www.nps.gov/yell/planyourvisit/visitorcenters.htm",
        "https://www.nps.gov/yell/learn/nature/yellowstonewildlife.htm",
    ],
    "grand_canyon": [
        "https://www.nps.gov/grca/learn/nature/animals.htm",
        "https://www.nps.gov/grca/planyourvisit/camping.htm",
        "https://www.nps.gov/grca/planyourvisit/hiking.htm",
        "https://www.nps.gov/grca/planyourvisit/permits.htm",
        "https://www.nps.gov/grca/planyourvisit/backcountry-permit.htm",
    ],
    "yosemite": [
        "https://www.nps.gov/yose/learn/nature/animals.htm",
        "https://www.nps.gov/yose/planyourvisit/camping.htm",
        "https://www.nps.gov/yose/planyourvisit/hiking.htm",
        "https://www.nps.gov/yose/planyourvisit/reservations.htm",
        "https://www.nps.gov/yose/planyourvisit/valleyhikes.htm",
    ],
    "zion": [
        "https://www.nps.gov/zion/learn/nature/animals.htm",
        "https://www.nps.gov/zion/planyourvisit/camping.htm",
        "https://www.nps.gov/zion/planyourvisit/hiking.htm",
        "https://www.nps.gov/zion/planyourvisit/permits.htm",
        "https://www.nps.gov/zion/planyourvisit/weather.htm",
    ],
    "great_smoky": [
        "https://www.nps.gov/grsm/learn/nature/animals.htm",
        "https://www.nps.gov/grsm/planyourvisit/camping.htm",
        "https://www.nps.gov/grsm/planyourvisit/hiking.htm",
        "https://www.nps.gov/grsm/planyourvisit/weather.htm",
        "https://www.nps.gov/grsm/learn/nature/black-bears.htm",
    ],
}

for name, urls in parks.items():
    print(f"Scraping {name}...")
    all_text = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            # Get main content area if possible
            main = soup.find("div", {"id": "cs_content"}) or soup.find("main") or soup
            text = main.get_text(separator="\n")
            lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 40]
            all_text.extend(lines)
            print(f"  Got {url}")
        except Exception as e:
            print(f"  Failed {url}: {e}")

    clean_text = "\n".join(all_text)
    with open(f"docs/{name}.txt", "w", encoding="utf-8") as f:
        f.write(clean_text)
    print(f"  Saved docs/{name}.txt ({len(clean_text)} chars)\n")

print("Done!")