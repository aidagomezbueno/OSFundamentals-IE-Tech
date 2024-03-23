import socket
import threading
import signal
import sys
import time

shopping_list = []
active_connections = []
client_threads = []
shutdown_flag = False 

HOST = '127.0.0.1'  
PORT = 4321  
MAX_CONNECTED_REQUESTS = 5  # Server queuing up to 5 connection requests

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Function monitoring the shutdown_flag and closing connections when the flag is set
def shutdown_watcher():
    global shutdown_flag
    while not shutdown_flag:
        time.sleep(1) 
    close_connections() 
    
# Thread monitoring the shutdown process
shutdown_thread = threading.Thread(target=shutdown_watcher)
shutdown_thread.start()

# Function closing the server socket and all active client connections
def close_connections():
    global server_socket
    server_socket.close()  
    while active_connections:  
        conn = active_connections.pop()
        try:
            conn.close()
        except Exception as e:
            print(f"Error closing connection: {e}.")

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    global shutdown_flag
    shutdown_flag = True  
    print("\nClosing all connections and performing the backup...")
    
    # Performing backup by writing the shopping list items to a file
    with open("backup.txt", "w") as file:
        for item in shopping_list:
            file.write(f"{item}\n")
    close_connections()  
    
    # Ensuring all threads have finished before (gracefully) shutting down
    for thread in client_threads:
        thread.join()
    shutdown_thread.join()
    sys.exit(0) 
    
# Signal handlers for termination and interrupt signals
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Function handling each client connection in a separate thread
def handle_client_connection(c_socket, addr):
    global active_connections
    active_connections.append(c_socket) 
    try:
        while not shutdown_flag:
            try:
                data = c_socket.recv(1024).decode('ascii')
                if not data: 
                    print(f"Client {addr} closed the connection.")
                    break
                
                command, _, message = data.partition(':')
                
                # Processing different requests from the client, and coming up with a response
                if command == "ADD":
                    shopping_list.append(message)
                    response = "Item added!"
                elif command == "RETRIEVE":
                    if len(shopping_list) == 0:
                        response = "Empty shopping list"
                    else:
                        response = "[" + ", ".join(f'"{item}"' for item in shopping_list) + "]" 
                else:
                    response = "Invalid command"

                c_socket.send(response.encode('ascii'))
            except socket.error as e:
                break
    except Exception as e:
        pass
    finally:
        
        # Cleaning up the connection
        if c_socket in active_connections:
            active_connections.remove(c_socket)
        c_socket.close()
        print(f"Closed connection with {addr}.")

# Function starting the server and listening for incoming connections
def start_server():
    global server_socket
    server_socket.bind((HOST, PORT))  
    server_socket.listen(MAX_CONNECTED_REQUESTS)  # Listening for incoming connections - queuing up to 5 requests
    print(f"Listening as {HOST}:{PORT}...")
    while not shutdown_flag: 
        try:
            c_socket, addr = server_socket.accept() 
            print(f"Accepted connection from {addr}.")
            # Starting a new thread to handle each client connection
            thread = threading.Thread(target=handle_client_connection, args=(c_socket, addr))
            thread.start()
            client_threads.append(thread) 
        except Exception as e:
            print(f"No longer accepting new connections. {e}.")
    close_connections() 

start_server()  