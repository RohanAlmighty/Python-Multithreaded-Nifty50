import requests
from bs4 import BeautifulSoup


class WikiWorker:
    def __init__(self):
        self._url = "https://en.wikipedia.org/wiki/NIFTY_50"

    @staticmethod
    def _extract_company_symbols(page_html):
        soup = BeautifulSoup(page_html, "lxml")
        table = soup.find(id="constituents")
        table_rows = table.find_all("tr")
        for table_row in table_rows[1:]:
            symbol = table_row.find_all("td")[1].text.strip("\n")
            yield symbol

    def get_nifty_50_companies(self):
        response = requests.get(self._url)
        if response.status_code != 200:
            print("Couldn't get entries")
            return []

        yield from self._extract_company_symbols(response.text)


if __name__ == "__main__":
    wiki_worker = WikiWorker()
    for symbol in wiki_worker.get_nifty_50_companies():
        print(symbol)
