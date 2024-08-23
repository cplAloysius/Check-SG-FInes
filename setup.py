import json

plate_no = input("Enter your vehicle plate number: ")
interval = input("Enter your desired interval for checking in whole minutes: ")
chat_id = input("Enter your telegram chat id: ")
token = input("Enter your telegram bot token: ")

output = {
    "plate_no": plate_no,
    "interval": interval,
    "chat_id": chat_id,
    "token": token
}

file_path = 'config.json'

with open(file_path, 'w') as file:
    json.dump(output, file, indent=4)

print("config file created successfully")