import os
import time
import tracemalloc
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from src.zetoken.zetoken import Zetoken

def run_stress_test(iterations=100000):
    os.environ['ZETOKEN_ACCESS_KEY_ID'] = 'test_access_key_123'
    os.environ['ZETOKEN_SECRET_KEY'] = 'test_secret_key_456'
    os.environ['ZETOKEN_ITERATIONS'] = '1000'

    zetoken = Zetoken()
    payload = "Data rahasia untuk stress test 2026!"
    
    print("==================================================")
    print(f"MEMULAI ULTIMATE STRESS TEST: {iterations} ITERASI (PURE PYTHON)")
    print("==================================================")

    tracemalloc.start()
    start_total = time.time()

    total_enc_time = 0.0
    total_dec_time = 0.0
    max_latency = 0.0
    failures = 0

    for i in range(iterations):
        t0 = time.time()
        token = zetoken.encode(payload)
        t1 = time.time()
        
        enc_duration = (t1 - t0) * 1000 
        total_enc_time += enc_duration
        if enc_duration > max_latency:
            max_latency = enc_duration

        if not token:
            failures += 1
            continue

        t2 = time.time()
        decoded = zetoken.decode(token)
        t3 = time.time()
        
        dec_duration = (t3 - t2) * 1000  
        total_dec_time += dec_duration
        if dec_duration > max_latency:
            max_latency = dec_duration

        if decoded != payload:
            failures += 1

    end_total = time.time()
    
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    total_exec_time = end_total - start_total
    avg_enc = total_enc_time / iterations
    avg_dec = total_dec_time / iterations
    delta_mem_kb = peak_mem / 1024.0

    print("\nHasil Akhir:")
    print(f"- Total Waktu Eksekusi : {total_exec_time:.2f} detik")
    print(f"- Rata-rata Enkripsi   : {avg_enc:.5f} ms")
    print(f"- Rata-rata Dekripsi   : {avg_dec:.5f} ms")
    print(f"- Latensi Terburuk     : {max_latency:.4f} ms")
    print(f"- Total Kegagalan      : {failures}")
    print(f"- Delta Memori Python  : {delta_mem_kb:.2f} KB")
    print("==================================================")

if __name__ == "__main__":
    run_stress_test(100000)