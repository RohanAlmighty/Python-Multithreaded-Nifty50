import time
from scraper_manager import ScraperManager

NUMBER_OF_WORKERS = 10


def main() -> None:
    scraper_manager = ScraperManager(num_workers=NUMBER_OF_WORKERS)
    scraper_start_time = time.time()
    scraper_manager.run()
    print("--------------------------------------------------------")
    print("Time Taken : ", round(time.time() - scraper_start_time, 1))


if __name__ == "__main__":
    main()
