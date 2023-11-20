import re
import numpy as np
import pandas as pd


def found_email(email):
    """
    Finds and extracts email addresses from the given email.

    Args:
    - email (str): The input email to search for email addresses.

    Returns:
    - str or np.nan: The found email address or np.nan if none is found.
    """
    # Check if the input email is null
    if pd.isnull(email):
        return np.nan
    
    # Define the email pattern using a regular expression
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    
    # Search for the email pattern in the email
    match = re.search(email_pattern, email)
    
    # Check if a match is found
    if match:
        return match.group()  # Return the found email address
    else:
        return np.nan  # Return np.nan if no email address is found