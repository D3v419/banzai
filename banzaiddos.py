import requests
import concurrent.futures
import time

# URL target (ganti dengan URL yang Anda miliki izin untuk diuji)
url = "http://example.com"

# Jumlah request per menit
requests_per_minute = 1000000

# Durasi pengujian dalam menit
duration_minutes = 60

# Fungsi untuk mengirim request
def send_request():
    try:
        response = requests.get(url)
        return response.status_code
    except Exception as e:
        return str(e)

# Fungsi untuk menjalankan pengujian
def run_load_test():
    start_time = time.time()
    total_requests = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        while time.time() - start_time < duration_minutes * 60:
            futures = [executor.submit(send_request) for _ in range(requests_per_minute // 60)]
            for future in concurrent.futures.as_completed(futures):
                total_requests += 1
                if total_requests % 1000 == 0:
                    print(f"Total requests sent: {total_requests}")

    print(f"Total requests sent in {duration_minutes} minutes: {total_requests}")

if __name__ == "__main__":
    run_load_test()