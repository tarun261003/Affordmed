from flask import Flask, request, jsonify
import requests
import time

import os



app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
TEST_SERVER_URLS = {
    "prime": "http://20.244.56.144/test/primes",
    "fibonacci": "http://20.244.56.144/test/fibo",
    "even": "http://20.244.56.144/test/even",
    "random": "http://20.244.56.144/test/rand"
}
QUALIFIED_IDS = {"p": "prime", "f": "fibonacci", "e": "even", "r": "random"}
window = []

# Get the access token from the environment variables
ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE5MjEzNjYyLCJpYXQiOjE3MTkyMTMzNjIsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6ImRlYWZmODUwLThiZTgtNDJjZS1iOGYyLTE0NDEwNGUyNWJhMCIsInN1YiI6InRhcnVubWFuZ2FsYW1wYWxsaUBnbWFpbC5jb20ifSwiY29tcGFueU5hbWUiOiJBZmZvcmRNZWQiLCJjbGllbnRJRCI6ImRlYWZmODUwLThiZTgtNDJjZS1iOGYyLTE0NDEwNGUyNWJhMCIsImNsaWVudFNlY3JldCI6IlBNTUJlenhldXpLZWRFc1QiLCJvd25lck5hbWUiOiJNYW5nYWxhbXBhbGxpIFRhcnVuIiwib3duZXJFbWFpbCI6InRhcnVubWFuZ2FsYW1wYWxsaUBnbWFpbC5jb20iLCJyb2xsTm8iOiIyMUtOMUE0NDM5In0.SbP4lZT0khtWrbUZoE9hinpc2XPq-G_lv8jgKC3G6wc'

def fetch_numbers(qualifier):
    url = TEST_SERVER_URLS[qualifier]
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    try:
        response = requests.get(url, headers=headers, timeout=0.5)
        print(f"Request to {url} returned status code {response.status_code}")
        if response.status_code == 200:
            print(f"Response JSON: {response.json()}")
            return response.json().get("numbers", [])
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except requests.exceptions.Timeout:
        print(f"Request to {url} timed out")
    except Exception as e:
        print(f"An error occurred: {e}")
    return []

@app.route('/numbers/<qualifier>', methods=['GET'])
def get_numbers(qualifier):
    if qualifier not in QUALIFIED_IDS:
        return jsonify({"error": "Invalid qualifier"}), 400

    qualifier_key = QUALIFIED_IDS[qualifier]
    numbers = fetch_numbers(qualifier_key)
    
    global window
    previous_window = window[:]
    
    for number in numbers:
        if number not in window:
            if len(window) >= WINDOW_SIZE:
                window.pop(0)
            window.append(number)

    avg = sum(window) / len(window) if window else 0

    response = {
        "numbers": numbers,
        "windowPrevState": previous_window,
        "windowCurrState": window,
        "avg": round(avg, 2)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=9876)
