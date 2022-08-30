from threading import Thread

from nike_monitor.nike_monitor import Monitor


def main():
    monitors = {
        "PL": "webhook-url",
        "DE": "webhook-url",
    }
    threads = []
    for (country, webhook_url) in monitors.items():
        thread = Thread(target=Monitor(webhook_url, country).run)
        threads.append(thread)
        thread.start()
    thread: Thread
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
