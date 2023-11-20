import pandas as pd
import requests


def contact_collection(api_key, url, request_data):
    """
    Collects contact data from a paginated API endpoint.

    Args:
    - api_key (str): The API key for authentication.
    - url (str): The URL of the API endpoint.
    - request_data (dict): The data to be included in the API request.

    Returns:
    - pd.DataFrame: A pandas DataFrame containing the collected contact data.
    """
    
    # Set up headers for the API request
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': "Bearer {}".format(api_key)
    }

    # Initialize the 'after' value
    after_value = 0
    
    # List to store DataFrames
    data_frames_list = []

    # Infinite loop to fetch paginated data
    while True:
        # Update the 'after' value in the request data
        request_data["after"] = str(after_value)

        # Make a POST request to the API
        response = requests.post(url, headers=headers, json=request_data)
        json_response = response.json()

        # Extract 'results' from the JSON response
        results = json_response['results']

        # Convert results to a DataFrame
        data_frame = pd.json_normalize(results)

        # Add the DataFrame to the list
        data_frames_list.append(data_frame)

        # Check if there are more pages in the response
        if 'paging' in json_response:
            paging = json_response['paging']
            next_page = paging.get('next')

            # Update 'after' for the next page if available
            if next_page:
                after_value = next_page.get('after')
                print("Value of 'after' for the next page:", after_value)
            else:
                print("No more results available.")
                break
        else:
            print("The 'paging' property was not found in the response.")
            break

    # Concatenate all DataFrames into a final DataFrame
    final_data_frame = pd.concat(data_frames_list, ignore_index=True)
    
    return final_data_frame