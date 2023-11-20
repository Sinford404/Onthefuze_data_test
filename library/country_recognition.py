import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim


def country_recognition(dataframe, column_name):
    """
    Recognizes countries based on city names in a DataFrame.

    Args:
    - dataframe (pd.DataFrame): The input DataFrame containing city names.
    - column_name (str): The name of the column containing city names.

    Returns:
    - pd.DataFrame: A DataFrame with unique city values and their recognized countries.
    """
    # Get unique values and filter out NaN
    unique_values = dataframe[column_name].unique()
    unique_values = [value for value in unique_values if pd.notna(value)]

    # Create a DataFrame with unique values
    df_unique_values = pd.DataFrame({'unique_values': unique_values})

    # Get the country for each city using geocoding
    geolocator = Nominatim(user_agent="my_geocoder")
    df_unique_values['country'] = df_unique_values['unique_values'].apply(
        lambda city: (lambda loc: loc.address.split(",")[-1].strip() if loc else None)(geolocator.geocode(str(city)))
    )

    # Replace specific values in the 'country' column
    df_unique_values['country'] = df_unique_values['country'].replace(
        {'Éire / Ireland': 'Ireland'}
    )

    # Create the 'city' column based on a condition
    df_unique_values['city'] = np.where(
        df_unique_values['country'] == df_unique_values['unique_values'],
        "",
        df_unique_values['unique_values']
    )

    # Set 'city' to an empty string where 'country' is 'England'
    df_unique_values.loc[df_unique_values['city'] == 'England', 'city'] = ""

    # Update the original DataFrame with recognized countries and cities
    dataframe['country'] = dataframe[column_name].replace(
        dict(zip(df_unique_values['unique_values'], df_unique_values['country']))
    )
    dataframe['city'] = dataframe[column_name].replace(
        dict(zip(df_unique_values['unique_values'], df_unique_values['city']))
    )

    # Create the 'country_tuple' column
    #dataframe['country_tuple'] = dataframe.apply(
        #lambda x: tuple([x["country"], x["city"]]) if pd.notna(x["country"]) else np.nan,
        #axis=1
    #)

    dataframe['country_tuple'] = dataframe.apply(
    lambda x: tuple(['England' if x["country"] == 'United Kingdom' else x["country"], x["city"]]) if pd.notna(x["country"]) else np.nan,
    axis=1
)

    return df_unique_values