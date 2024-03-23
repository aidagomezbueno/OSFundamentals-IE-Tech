import socket

# Client menu function
def client_menu():
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 4321)
    connection_established = False
    
    # Trying to connect to the server
    try:
        c_socket.connect(server_address)
        connection_established = True
    except Exception as e:
        print(f"Server not running. Error: {e}.")   
        
    # If connection established, entering then the menu loop
    if connection_established:
        try:        
            while True:
                print("\n1) Add item\n2) Retrieve items\n3) Exit")
                choice = input("\nWhat do you want to do? ")
                
                if choice == '3':
                    print("Exiting...")
                    break
                
                if choice == '1':
                    item = input("What item do you want to add? ")
                    message = f"ADD:{item}"
                elif choice == '2':
                    message = "RETRIEVE"
                else:
                    message = "INVALID"
                    
                # Sending the message to the server
                c_socket.send(message.encode('ascii'))
                
                # Trying to receive a response from the server
                try:
                    response = c_socket.recv(1024).decode('ascii')
                    if response:
                        if response == "Invalid command":
                            continue
                        else:
                            print(f"Server replied: {response}")
                    else:
                        break
                    
                # Handling specific network errors during reception
                except OSError as e:
                    if e.errno == socket.errno.ECONNREFUSED:
                        print("Connection refused by the server. Is the server running and accepting connections?")
                    elif e.errno == socket.errno.ETIMEDOUT:
                        print("Connection timed out. The server might be too slow to respond or down.")
                    else:
                        print(f"An unexpected network error occurred: {e}.")
                    break

        except Exception as e:
            print(f"An unexpected error occurred: {e}. Closing the connection.")
            c_socket.close()
            
        # Ensuring the connection is closed
        finally:
            print("Connection closed.")
            c_socket.close()

client_menu()
