import time

from multiprocessing import Queue

from workers.wiki_worker import WikiWorker
from workers.google_finance_worker import GoogleFinanceScheduler


def main():
    symbol_queue = Queue()
    scraper_start_time = time.time()

    wiki_worker = WikiWorker()
    google_finance_scheduler_threads = []

    num_google_finance_worker = 10
    for i in range(num_google_finance_worker):
        google_finance_scheduler = GoogleFinanceScheduler(input_queue=symbol_queue)
        google_finance_scheduler_threads.append(google_finance_scheduler)

    for symbol in wiki_worker.get_nifty_50_companies():
        symbol_queue.put(symbol)

    for i in range(len(google_finance_scheduler_threads)):
        symbol_queue.put("DONE")

    for i in range(len(google_finance_scheduler_threads)):
        google_finance_scheduler_threads[i].join()

    print("--------------------------------------------------------")
    print("Time Taken : ", round(time.time() - scraper_start_time, 1))


if __name__ == "__main__":
    main()
