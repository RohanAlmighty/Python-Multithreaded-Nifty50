import time

from workers.wiki_worker import WikiWorker
from workers.google_finance_worker import GoogleFinanceWorker


def main():
    scraper_start_time = time.time()

    current_workers = []

    wiki_worker = WikiWorker()
    for symbol in wiki_worker.get_nifty_50_companies():
        google_finance_worker = GoogleFinanceWorker(symbol=symbol)
        current_workers.append(google_finance_worker)

    for i in range(len(current_workers)):
        current_workers[i].join()

    print("--------------------------------------------------------")
    print("Time Taken : ", round(time.time() - scraper_start_time, 1))


if __name__ == "__main__":
    main()
