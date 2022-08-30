from threading import Thread

from nike_monitor.nike_monitor import Monitor


def main():
    monitors = {
        "PL": "https://discord.com/api/webhooks/965556784544763936/LPriyjQX4Eoc3AVMgJNw6FuC7Ym6y7kN8L7-QFCq4hp8Bi3cL_SFkXOVXZvSV8toeBfh",
        "DE": "https://discord.com/api/webhooks/965556784544763936/LPriyjQX4Eoc3AVMgJNw6FuC7Ym6y7kN8L7-QFCq4hp8Bi3cL_SFkXOVXZvSV8toeBfh",
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
