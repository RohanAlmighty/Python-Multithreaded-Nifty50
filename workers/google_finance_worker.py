import threading
import requests
from bs4 import BeautifulSoup
from queue import Queue

GOOGLE_FINANCE = "https://www.google.com/finance/quote/"
EXCHANGE = "NSE"


class GoogleFinanceScheduler(threading.Thread):
    def __init__(self: "GoogleFinanceScheduler", input_queue: Queue, **kwargs) -> None:
        super(GoogleFinanceScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self: "GoogleFinanceScheduler") -> None:
        while True:
            val = self._input_queue.get()
            if val == "DONE":
                break
            google_finance_worker = GoogleFinanceWorker(symbol=val)
            price = google_finance_worker.get_price()
            print(price)


class GoogleFinanceWorker:
    def __init__(self: "GoogleFinanceWorker", symbol: str) -> None:
        self._symbol = symbol
        base_url = GOOGLE_FINANCE
        self._url = base_url + self._symbol + f":{EXCHANGE}"

    def get_price(self: "GoogleFinanceWorker") -> str:
        response = requests.get(self._url)
        if response.status_code != 200:
            return ""
        soup = BeautifulSoup(response.text, "lxml")
        name = soup.find("div", class_="zzDege").text
        price = soup.find("div", class_="YMlKec fxKbKc").text

        return f"({self._symbol}) {name} : {price}"


if __name__ == "__main__":
    google_finance_worker = GoogleFinanceWorker(symbol="ONGC")
