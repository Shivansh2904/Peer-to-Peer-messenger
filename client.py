{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "95bde31b-4cdd-4719-a6b5-09a605ee1b86",
   "metadata": {},
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Enter your username:  Shivansh\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Shivansh joined the chat.\n",
      "\n",
      "Welcome, Shivansh! Type '@username message' for private message or 'broadcast message' for broadcast.\n",
      "Shivansh> "
     ]
    }
   ],
   "source": [
    "import socket\n",
    "import threading\n",
    "import os\n",
    "\n",
    "def create_user_directory(username):\n",
    "    os.makedirs(username, exist_ok=True)\n",
    "\n",
    "def receive_messages(client_socket, stop_event, username):\n",
    "    while not stop_event.is_set():\n",
    "        try:\n",
    "            message = client_socket.recv(1024).decode('utf-8', errors='ignore')\n",
    "            if \"Start of file\" in message:\n",
    "                filename = message.split()[3]  # Extract filename from start message\n",
    "                download_file(client_socket, filename, username)\n",
    "                print(f\"\\n{username}> \", end='', flush=True)  # Prompt after file download\n",
    "            else:\n",
    "                print(message, end=f'\\n{username}> ', flush=True)\n",
    "        except ConnectionAbortedError:\n",
    "            break\n",
    "        except Exception as e:\n",
    "            print(f\"Error receiving message: {e}\")\n",
    "\n",
    "def download_file(client_socket, filename, username):\n",
    "    filepath = os.path.join(username, f\"downloaded_{filename}\")\n",
    "    try:\n",
    "        downloaded_data = b''\n",
    "        while True:\n",
    "            chunk = client_socket.recv(1024)\n",
    "            if \"End of file\" in chunk.decode('utf-8', errors='ignore'):\n",
    "                break\n",
    "            downloaded_data += chunk\n",
    "\n",
    "        with open(filepath, 'wb') as f:\n",
    "            f.write(downloaded_data)\n",
    "        print(f\"File '{filename}' downloaded successfully to {filepath}!\")\n",
    "    except Exception as e:\n",
    "        print(f\"Error downloading file: {e}\")\n",
    "\n",
    "def send_messages(client_socket, stop_event, username):\n",
    "    while not stop_event.is_set():\n",
    "        try:\n",
    "            message = input(f\"{username}> \")\n",
    "            if message.lower() == 'exit':\n",
    "                stop_event.set()\n",
    "                client_socket.sendall(\"exit\".encode('utf-8'))\n",
    "                client_socket.close()\n",
    "                print(\"Exiting chat...\")\n",
    "                break\n",
    "            elif message.lower() == 'help':\n",
    "                print_help_commands()\n",
    "            else:\n",
    "                client_socket.sendall(message.encode('utf-8'))\n",
    "\n",
    "                if message.lower().startswith('download'):\n",
    "                    filename = message.split()[1]  # Extract filename from user input\n",
    "                    print(f\"Downloading {filename}...\")\n",
    "\n",
    "        except IndexError:\n",
    "            print(\"Invalid input. Please provide a filename or type 'help' for assistance.\")\n",
    "        except Exception as e:\n",
    "            print(f\"Error sending message: {e}\")\n",
    "\n",
    "def print_help_commands():\n",
    "    print(\"\\nAvailable commands:\")\n",
    "    print(\"  @username <message> - Send a private message to a user\")\n",
    "    print(\"  broadcast <message> - Send a message to all users\")\n",
    "    print(\"  listfiles - List all available files for download\")\n",
    "    print(\"  download <filename> - Download a file\")\n",
    "    print(\"  exit - Exit the chat\\n\")\n",
    "\n",
    "def main():\n",
    "    host = '127.0.0.1'\n",
    "    port = 12000\n",
    "\n",
    "    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n",
    "    client_socket.connect((host, port))\n",
    "\n",
    "    username = input(\"Enter your username: \")\n",
    "    create_user_directory(username)\n",
    "    client_socket.sendall(username.encode('utf-8'))\n",
    "\n",
    "    welcome_message = client_socket.recv(1024).decode('utf-8')\n",
    "    print(welcome_message)\n",
    "\n",
    "    stop_event = threading.Event()\n",
    "\n",
    "    send_thread = threading.Thread(target=send_messages, args=(client_socket, stop_event, username))\n",
    "    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, stop_event, username))\n",
    "\n",
    "    send_thread.start()\n",
    "    receive_thread.start()\n",
    "\n",
    "    send_thread.join()\n",
    "    receive_thread.join()\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    main()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b0ad299b-891e-4842-ac06-6c7eaf20e4a1",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
