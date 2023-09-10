import threading
import requests
from bs4 import BeautifulSoup


class GoogleFinanceWorker(threading.Thread):
    def __init__(self, symbol, **kwargs):
        super(GoogleFinanceWorker, self).__init__(**kwargs)
        self._symbol = symbol
        base_url = "https://www.google.com/finance/quote/"
        self._url = base_url + self._symbol + ":NSE"
        self.start()

    def run(self):
        response = requests.get(self._url)
        if response.status_code != 200:
            return
        soup = BeautifulSoup(response.text, "lxml")
        name = soup.find("div", class_="zzDege").text
        price = soup.find("div", class_="YMlKec fxKbKc").text
        print(f"({self._symbol}) {name} : {price}")


if __name__ == "__main__":
    google_finance_worker = GoogleFinanceWorker(symbol="ONGC")
