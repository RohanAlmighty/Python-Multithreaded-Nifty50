from queue import Queue
from typing import List
from workers.wiki_worker import WikiWorker
from workers.google_finance_worker import GoogleFinanceScheduler


class ScraperManager:
    def __init__(self: "ScraperManager", num_workers: int = 10) -> None:
        self.num_workers = num_workers
        self.symbol_queue = Queue()
        self.google_finance_scheduler_threads = []

    def initialize_workers(self: "ScraperManager") -> None:
        for _ in range(self.num_workers):
            google_finance_scheduler = GoogleFinanceScheduler(
                input_queue=self.symbol_queue
            )
            self.google_finance_scheduler_threads.append(google_finance_scheduler)

    def enqueue_symbols(self: "ScraperManager", symbols: List[str]) -> None:
        for symbol in symbols:
            self.symbol_queue.put(symbol)

    def signal_workers_to_exit(self: "ScraperManager") -> None:
        for _ in range(self.num_workers):
            self.symbol_queue.put("DONE")

    def join_workers(self: "ScraperManager") -> None:
        for thread in self.google_finance_scheduler_threads:
            thread.join()

    def run(self: "ScraperManager") -> None:
        self.initialize_workers()
        wiki_worker = WikiWorker()
        self.enqueue_symbols(wiki_worker.get_nifty_50_companies())
        self.signal_workers_to_exit()
        self.join_workers()


if __name__ == "__main__":
    scraper_manager = ScraperManager(num_workers=10)
    scraper_manager.run()
