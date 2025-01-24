import requests
import json

# URLs for the data
quiz_endpoint = "https://www.jsonkeeper.com/b/LLQT"  # Quiz Endpoint
submission_endpoint = "https://api.jsonserve.com/rJvd7g"  # Quiz Submission Data
historical_endpoint = "https://api.jsonserve.com/XgAgFJ"  # Historical Quiz Data

# Function to download data from a URL and save it as a JSON file
def download_data(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        # Save the response data as a JSON file
        with open(filename, 'w') as file:
            json.dump(response.json(), file, indent=4)
        print(f"Data downloaded and saved as {filename}")
    else:
        print(f"Failed to retrieve data from {url}")

# Download data from each URL
download_data(quiz_endpoint, "quiz_data.json")
download_data(submission_endpoint, "submission_data.json")
download_data(historical_endpoint, "historical_data.json")
