import json
import requests

def print_response(response: dict):
    for k,v in response.items():
        if isinstance(v, dict):
            print_response(v)
        else:
            print(k, v)

def safe_get(url, params=None):
    try:
        resp = requests.get(url, params)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as err:
        print("HTTP error:", err)
    except requests.exceptions.RequestException as err:
        print("Request failed:", err)
    except ValueError:
        print("Failed to decode JSON")

def write_data_in_file(filepath: str, data: dict):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            try:
                data_list = json.load(file)
            except:
                data_list = []
    except FileNotFoundError:
        data_list = []

    data_list.append(data)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data_list, file, indent=4, ensure_ascii=False)

"""Fetch and display the list of available currencies with their codes and full names"""
response_1 = safe_get("https://api.frankfurter.dev/v1/currencies")
print("Fetch and display the list of available currencies with their codes and full names")
print_response(response_1)
write_data_in_file("convertions_history.json", response_1)

"""Retrieve the current exchange rates (for example, relative to EUR or USD) and display them on the screen."""
response_2 = safe_get("https://api.frankfurter.dev/v1/latest")
print("\nRetrieve the current exchange rates (for example, relative to EUR or USD) and display them on the screen.")
print_response(response_2)
write_data_in_file("convertions_history.json", response_2)

amount = int(input("What amount would you like to convert? \n"))
start_currency = input("Enter currency code(USD, EUR, GBP): ").upper()
finish_currency = input("Enter currency code(GBP, USD, AUD): ").upper()
user_response = safe_get(f"http://api.frankfurter.dev/v1/latest?base={start_currency}&amount={amount}&symbols={finish_currency}")
print_response(user_response)
write_data_in_file("convertions_history.json", user_response)

post_url = "https://httpbin.org/post"
answer = requests.post(post_url, json=user_response)
print_response(answer.json().get("json"))

exit_str = input("Do you wanna calculate more? \n")
while exit_str.upper() == "YES":
    amount = int(input("What amount would you like to convert? \n"))
    start_currency = input("Enter currency code(USD, EUR, GBP): ").upper()
    finish_currency = input("Enter currency code(GBP, USD, AUD): ").upper()
    user_response = safe_get(f"http://api.frankfurter.dev/v1/latest?base={start_currency}&amount={amount}&symbols={finish_currency}")
    print_response(user_response)
    write_data_in_file("convertions_history.json", user_response)
    exit_str = input("Do you wanna calculate more? \n")
