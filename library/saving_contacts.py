import pandas as pd
import requests


def saving_contacts(url, hubspot_api_key, data):
    """
    Creates contacts in HubSpot using the provided URL, HubSpot API key, and data.

    Args:
    - url (str): The HubSpot API endpoint for batch contact creation.
    - hubspot_api_key (str): The HubSpot API key for authentication.
    - data (pd.DataFrame): The DataFrame containing contact data.

    Returns:
    - None
    """

    # Fill missing values in the DataFrame with None
    cleaned_df = data.where(pd.notna(data), None)

    # Headers for the HubSpot API request
    hubspot_headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'authorization': f'Bearer {hubspot_api_key}'
    }

    # Iterate over the rows of the cleaned DataFrame
    for index, row in cleaned_df.iterrows():
        # Prepare data for the API request
        api_request_data = {
            "inputs": [
                {
                    "properties": {
                        "email": row["fix_email"],
                        "phone": row["fix_phone"],
                        "lastname": row["properties.lastname"],
                        "firstname": row["properties.firstname"],
                        "city": row["city"],
                        "country": row["country"],
                        "temporary_id": row["properties.hs_object_id"],
                        "original_industry": row["properties.industry"],
                        "original_create_date": row["properties.technical_test___create_date"]
                    },
                }
            ]
        }

        # Make the API request to HubSpot
        requests.post(url, headers=hubspot_headers, json=api_request_data)