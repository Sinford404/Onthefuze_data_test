import re
import numpy as np
import pycountry
import phonenumbers


def fix_phone_numbers(phone, country_name):
    """
    Fixes phone numbers by adding country codes and formatting.

    Args:
    - phone (str): The phone number to be fixed.
    - country_name (str): The name of the country associated with the phone number.

    Returns:
    - str or np.nan: The formatted phone number or np.nan if input is invalid.
    """
    # Check if input values are valid
    if phone is None or country_name is None or phone == "":
        return np.nan
    
    try:
        # Get the country code based on the country name using pycountry
        country = pycountry.countries.get(name=country_name)
        
        if country:
            # Get the alpha-2 country code and phone code for the region
            country_code = country.alpha_2
            phone_code = phonenumbers.country_code_for_region(country_code)
        else:
            return np.nan
    except LookupError:
        return np.nan

    # Remove non-digit characters and leading '0', then format the number
    digits = re.sub(r'\D', '', str(phone)).lstrip('0')
    formatted_number = f'(+{phone_code}) {digits[:4]} {digits[4:]}'

    return formatted_number