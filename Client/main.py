import requests

# The API endpoint
url = "10.1.15.79"

# A GET request to the API
response = requests.get(url)

# Print the response
response_json = response.json()
print(response_json)

#10.1.15.79