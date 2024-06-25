import os
import subprocess
import time

def read_wifi_credentials(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            credentials = {}
            for line in lines:
                key, value = line.strip().split('=')
                credentials[key] = value
            return credentials
    else:
        return None



def disconnect_current_network():
    try:
        # Get the currently active connection
        result = subprocess.run(['nmcli', '-t', '-f', 'NAME', 'con', 'show', '--active'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        active_connections = result.stdout.decode().strip().split('\n')

        for connection in active_connections:
            if connection:  # Check if there is an active connection
                subprocess.run(['nmcli', 'con', 'down', connection], check=True)
                print(f"Disconnected from {connection}")

    except subprocess.CalledProcessError as e:
        print(f"Failed to disconnect from current network: {e}")

def connect_to_wifi(ssid, password):
    try:
        # Attempt to connect to the Wi-Fi network
        result = subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            print(f"Connected to {ssid}")
            return True
        else:
            print(f"Failed to connect to {ssid}: {result.stderr.decode().strip()}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while trying to connect: {e}")
        return False


def main():
    wifi_credentials = read_wifi_credentials('wifi.txt')


    if wifi_credentials:
        ssid = wifi_credentials.get('SSID')
        password = wifi_credentials.get('PASSWORD')

        while True:
            if connect_to_wifi(ssid, password):
                break
            else:
                disconnect_current_network()
                print("Retrying in 5 seconds...")
                time.sleep(5)

    else:
        print("No Wi-Fi or hotspot configuration found.")

if __name__ == '__main__':
    main()
