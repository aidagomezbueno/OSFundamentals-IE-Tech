from threading import Thread, Semaphore
from datetime import datetime
import time

INITIAL_TIMESTAMP = datetime.now()

def get_elapsed_seconds() -> float:
    return round((datetime.now() - INITIAL_TIMESTAMP).total_seconds(), 1)

def simulate_store(customers: [dict], ticket_price: float, max_occupancy: int, n_vips: int) -> float:
    global earnings
    earnings = 0.0
    occupancy_semaphore = Semaphore(max_occupancy)
    earnings_semaphore = Semaphore(1)  
    vip_done_semaphore = Semaphore(0) if n_vips > 0 else Semaphore(1)  

    def customer_behavior(customer_info):
        global earnings
        time.sleep(customer_info['joinDelay'])
        
        if not customer_info['VIP']:
            vip_done_semaphore.acquire()  
            vip_done_semaphore.release()  
        
        # Protecting store access
        occupancy_semaphore.acquire()
        print(f"{get_elapsed_seconds()}s: {customer_info['name']} (entering)")
        time.sleep(customer_info['timeInStore'])
        
        # Protecting earnings update
        earnings_semaphore.acquire()
        earnings += customer_info['ticketCount'] * ticket_price
        earnings_semaphore.release()
        
        print(f"{get_elapsed_seconds()}s: {customer_info['name']} (leaving)")
        occupancy_semaphore.release()

    vip_customers = [customer for customer in customers if customer['VIP']]
    non_vip_customers = [customer for customer in customers if not customer['VIP']]

    threads = [Thread(target=customer_behavior, args=(customer,), name=customer['name']) for customer in customers]

    # Starting all threads (customers) to properly handle joinDelay - since the start of the execution
    for thread in threads:
        thread.start()

    # Joining VIP threads first
    n_vips_processed = 0
    for thread in [t for t in threads if t.name in [c['name'] for c in vip_customers]]:
        thread.join()
        n_vips_processed += 1
    
    # Ensuring no regular customers (non-VIP) enter the store until all VIPs have left
    if n_vips == n_vips_processed:
        vip_done_semaphore.release()

    # Joining non-VIP threads once all VIP threads have already joined - if any
    for thread in [t for t in threads if t.name in [c['name'] for c in non_vip_customers]]:
        thread.join()

    return earnings