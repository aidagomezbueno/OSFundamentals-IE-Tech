# OSFundamentals-IE-Tech

Welcome to my repository for the Operating Systems course at IE School of Science & Technology. This repository is a collection of hands-on projects that illustrate the fundamental concepts of operating systems.

## Projects

### AssemblyCalculatorOS
This subdirectory contains an assembly language program for an arithmetic calculator. It demonstrates basic arithmetic operations, showcasing low-level programming and the execution of programs close to the hardware level.

**How to execute:**
To run the AssemblyCalculatorOS, use the Mars4_5.jar MIPS simulator. Open the `.asm` file in MARS, assemble the program, and execute it within the simulator to perform arithmetic operations.

### NetworkedShoppingList
In this section, a client-server model is implemented to manage a shopping list over the network. This application is capable of handling multiple client connections concurrently, illustrating the use of sockets for network communication and threading for handling simultaneous interactions.

**How to execute:**
Start by running `server.py` to launch the server, which listens for incoming connections and manages the shopping list. Then, on one or more different terminals, run `client.py` to operate the client interface. Through the client, you can add items to the shopping list or retrieve the current list. The server can handle multiple clients at the same time, demonstrating the handling of concurrent network connections in a practical scenario.

### VIPStoreSimulator
This project simulates a store's operations with an emphasis on VIP customer management. It uses threads and semaphores to handle concurrent customer service within a store and is a practical application of interprocess communication.

**How to execute:**
Execute the `main.py` to begin the store simulation. The script loads customer data from `customers.json` and starts the simulation of VIP and regular customers visiting the store. Monitor the console output to follow the customer interactions and the store's ticket earnings.

## Learning Objectives
- Understanding the structure and operation of OS
- Exploring threads, processes, and virtual memory
- Implementing interprocess communication
- Managing file systems and compiled code

Enjoy navigating through the intricacies of operating systems!
