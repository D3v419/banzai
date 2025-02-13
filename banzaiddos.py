import requests
import concurrent.futures
import time

# Meminta masukan URL dari pengguna
url = input("Masukkan URL target: ")

# Jumlah request per menit
requests_per_minute = 10000000  # 10 juta request per menit

# Durasi pengujian dalam menit
duration_minutes = 60

# Fungsi untuk mengirim request
def send_request():
    try:
        # Gunakan POST request dengan data besar untuk meningkatkan beban
        response = requests.post(url, data={"payload": "x" * 10000})  # Data besar
        print(f"Response: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Error: {e}")
        return str(e)

# Fungsi untuk menjalankan pengujian
def run_load_test():
    start_time = time.time()
    total_requests = 0

    print(f"Starting load test for {duration_minutes} minutes...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100000) as executor:  # Meningkatkan max_workers
        while time.time() - start_time < duration_minutes * 60:
            futures = [executor.submit(send_request) for _ in range(requests_per_minute // 60)]
            for future in concurrent.futures.as_completed(futures):
                total_requests += 1
                if total_requests % 1000000 == 0:  # Notifikasi setiap 100.000 request
                    print(f"Total requests sent: {total_requests}")

    print(f"Load test completed. Total requests sent in {duration_minutes} minutes: {total_requests}")

if __name__ == "__main__":
    run_load_test()
