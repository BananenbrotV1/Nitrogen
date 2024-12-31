import os
import time
import threading
import requests
import random
import string

running = False
discord_webhook_url = "No webhook selected"
last_codes = []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_random_string(length=18):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_to_discord(webhook_url, message):
    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending to Discord: {e}")

def show_menu():
    print(f"Currently selected webhook: {discord_webhook_url}")
    print("===============================")
    print("1 | Select Webhook")
    if running:
        print("2 | Stop")
    elif discord_webhook_url != "No webhook selected":
        print("2 | Start")
    else:
        print("2 | Start (no webhook selected)")
    print("3 | Exit")
    print("===============================")
    print("Last generated codes:")

def update_display():
    clear_screen()
    show_menu()
    for entry in last_codes:
        print(entry)

def add_code_to_list(code, valid=False):
    global last_codes
    if len(last_codes) >= 10:
        last_codes.pop()
    status = "✅ Valid" if valid else "❌ Invalid"
    last_codes.insert(0, f"{code} {status}")
    update_display()

def code_generator():
    global running
    url_template = "https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"

    while running:
        random_code = generate_random_string(18)
        url = url_template.format(code=random_code)

        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                add_code_to_list(random_code, valid=True)
                send_to_discord(discord_webhook_url, f"Valid Nitro code found: {random_code}")
            else:
                add_code_to_list(random_code, valid=False)

        except requests.RequestException as e:
            print(f"Error requesting code {random_code}: {e}")

        time.sleep(0.5)

def main_menu():
    global running, discord_webhook_url
    update_display()
    option = input("\nSelect an option: ")
    return option

while True:
    option = main_menu()
    if option == '1':
        clear_screen()
        discord_webhook_url = input("What is your webhook? ")
        if not discord_webhook_url.startswith('http'):
            discord_webhook_url = "No webhook selected"
            print("Invalid webhook! Please enter a valid link.")
            time.sleep(1)
    elif option == '2':
        if discord_webhook_url == "No webhook selected":
            print("Please select a valid webhook first!")
            time.sleep(1)
            continue
        
        if running:
            running = False
            print("Stopping generator...")
        else:
            running = True
            thread = threading.Thread(target=code_generator)
            thread.start()
            print("Starting generator...")
        time.sleep(1)
    elif option == '3':
        running = False
        print("Exiting program...")
        time.sleep(1)
        break
    else:
        print("Invalid selection. Please try again.")
        time.sleep(1)
