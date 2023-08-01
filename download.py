import time
from src import http

if __name__ == '__main__':
    response_json = http.download_all()
    print(response_json)
    download_id = response_json["download_id"]
    download_results = http.get_download_url(download_id)
    while download_results["status"] in ("INITIALISED", "QUEUEING", "RUNNING") \
        or "download_url" not in download_results.keys():
        download_results = http.get_download_url(download_id)
        print("Download is not ready. Status of request is", download_results["status"])
        time.sleep(10)
    print("Download is ready. Status of request is", download_results["status"])
    print(download_results["download_url"])