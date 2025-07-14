
# P2P File Sharing System

## Overview

This project implements a simple peer-to-peer (P2P) file sharing system using Python sockets. It allows multiple peers to share files among themselves, with a central Distributed Hash Table (DHT) server that keeps track of which peer has which file. Peers can register files they want to share, search for files available in the network, and download files from other peers.

## Architecture

- **DHT Server (`DHT_Server.py`)**:  
  Acts as a central registry. Peers register the files they are sharing, and the DHT server keeps a mapping of filenames to the IP and port of the peer sharing them. It handles two main commands:
  - `REGISTER`: Register a file with the server.
  - `SEARCH`: Search for a file and return the peer's address if found.

- **Peer Main (`peer_main.py`)**:  
  The main entry point for a peer. Handles user interaction:
  - Register a file (from the `shared` folder) with the DHT server.
  - Search for a file in the network and download it if found.
  - Runs a server thread to serve files to other peers.

- **Peer Server (`peer_server.py`)**:  
  Runs on each peer to serve files from the `shared` folder to other peers upon request.

- **Peer Client (`peer_client.py`)**:  
  Handles downloading files from other peers by connecting to their server and saving the file to the `downloads` folder.

- **Utils (`utils.py`)**:  
  Contains utility functions, such as hashing filenames.

- **Folders**:
  - `shared/`: Place files here that you want to share with the network.
  - `downloads/`: Files downloaded from other peers are saved here.

## How It Works

1. **Start the DHT Server**:  
   Run `DHT_Server.py` on a central machine accessible to all peers.

2. **Start a Peer**:  
   Run `peer_main.py` on each peer machine. Each peer:
   - Registers files it wants to share.
   - Can search for files and download them from other peers.

3. **File Registration**:  
   When a peer registers a file, the DHT server records which peer has the file.

4. **File Search and Download**:  
   When a peer searches for a file, the DHT server returns the address of the peer sharing it. The searching peer then connects directly to the sharing peer to download the file.

## Usage

1. **Start the DHT Server**:
   ```
   python DHT_Server.py
   ```

2. **Start a Peer**:
   ```
   python peer_main.py
   ```
   - Enter a port number when prompted.
   - Use the menu to register files or download files.

3. **Sharing Files**:
   - Place files you want to share in the `shared/` folder.
   - Register them using the menu.

4. **Downloading Files**:
   - Search for a file by name.
   - If found, it will be downloaded to the `downloads/` folder.

## File Descriptions

- **DHT_Server.py**: Central server for file registration and lookup.
- **peer_main.py**: Peer interface for registering, searching, and downloading files.
- **peer_server.py**: Handles incoming file requests from other peers.
- **peer_client.py**: Downloads files from other peers.
- **utils.py**: Utility functions (e.g., hashing).

## Notes

- All communication is done over TCP sockets.
- The DHT server must be running before any peers can register or search for files.
- The system is designed for a local network or environments where all peers and the DHT server can reach each other.

---

