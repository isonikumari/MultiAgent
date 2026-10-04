from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv
import os
from rich import print
load_dotenv()


tavily = TavilyClient(api_key=os.getenv("TRAVILY_API_KEY"))
@tool
def web_search(query:str)->str:
     """Search the web for recent and reliable information on a topic. Returns titles, URLs, and snippets."""
     results = tavily.search(query=query, max_results=5)
     out = []
     for result in results["results"]:
          out.append(
               f"Title: {result['title']}\n"
               f"URL: {result['url']}\n"
               f"Snippet: {result['content'][:300]}"
          )
     return "\n_____\n".join(out)

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
                    resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
                    soup = BeautifulSoup(resp.text, "html.parser")
                    for tag in soup(["script", "style", "nav", "footer"]):
                              tag.decompose()
                    return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as error:
                    return f"Could not scrape URL: {error}"
    
# if __name__ == "__main__":
#      query = input("Ask a question: ")
#      print(web_search.invoke(query))