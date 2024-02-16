import requests
import time

login_url = 'http://127.0.0.1:8000/login/'  # Update this with your actual login page URL

# Function to hit the login page
def hit_login_page():
    try:
        response = requests.get(login_url)  # Send a GET request to get the CSRF token
        csrf_token = response.cookies['csrftoken']  # Extract the CSRF token from the response cookies

# Send a POST request with the CSRF token
        response = requests.post(login_url, data={'email': 'authority@blockchain.com', 'password': 'authority'}, headers={'X-CSRFToken': csrf_token})
        if response.status_code == 200:  # Assuming 200 is the success status code for your login page
            return True
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return False

# Number of hits to the login page
num_hits = 0

# Number of hits before which the login is considered successful
threshold = 10

# Main loop to hit the login page
while num_hits < threshold:
    if hit_login_page():
        num_hits += 1
        print(f"Login hit {num_hits} times")
    time.sleep(1)  # Adjust the sleep time as needed
