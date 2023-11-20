import pandas as pd


def duplicate_management(input_dataframe):
    """
    Process the input DataFrame by combining and aggregating data.

    Args:
    - input_dataframe (pd.DataFrame): The input DataFrame to be processed.

    Returns:
    - pd.DataFrame: The processed DataFrame.
    """

    # Create a copy of the input DataFrame
    df_copy = input_dataframe.copy()

    # Create a 'Full name' column by concatenating 'firstname' and 'lastname'
    df_copy['Full name'] = df_copy['properties.firstname'] + ' ' + df_copy['properties.lastname']

    # Filter rows where 'fix_email' is NaN
    df_filtrado = df_copy[df_copy['fix_email'].isna()]

    # Sort the DataFrame by 'fix_email' and 'technical_test___create_date'
    df_copy.sort_values(["fix_email", "properties.technical_test___create_date"], ascending=[True, False], inplace=True)

    # Group by 'fix_email' and aggregate data
    processed_data1 = df_copy.groupby('fix_email').agg({
        'id': 'first',
        'createdAt': 'first',
        'updatedAt': 'first',
        'archived': 'first',
        'properties.address': 'first',
        'properties.country': 'first',
        'properties.createdate': 'first',
        'properties.firstname': 'first',
        'properties.lastname': 'first',
        'properties.hs_object_id': 'first',
        'properties.lastmodifieddate': 'first',
        'properties.phone': 'first',
        'properties.raw_email': 'first',
        'fix_phone': 'first',
        'country': 'first',
        'city': 'first',
        'country_tuple': 'first',
        'Full name': 'first',
        'properties.industry': lambda x: ';'.join(x.dropna().astype(str).unique()),
        'properties.technical_test___create_date': 'first'
    }).reset_index()

    # Concatenate the aggregated result with the filtered DataFrame
    df_concatenated = pd.concat([processed_data1, df_filtrado], ignore_index=True)

    # Sort the concatenated DataFrame by 'Full name' and 'technical_test___create_date'
    df_concatenated.sort_values(["Full name", "properties.technical_test___create_date"], ascending=[True, False], inplace=True)

    # Group by 'Full name' and 'fix_phone', and aggregate data
    processed_data2 = df_concatenated.groupby(['Full name', 'fix_phone']).agg({
        'id': 'first',
        'createdAt': 'first',
        'updatedAt': 'first',
        'archived': 'first',
        'properties.address': 'first',
        'properties.country': 'first',
        'properties.createdate': 'first',
        'properties.firstname': 'first',
        'properties.lastname': 'first',
        'properties.hs_object_id': 'first',
        'properties.lastmodifieddate': 'first',
        'properties.phone': 'first',
        'properties.raw_email': 'first',
        'country': 'first',
        'city': 'first',
        'country_tuple': 'first',
        'fix_email': 'first',
        'properties.industry': lambda x: ';'.join(x.dropna().astype(str).unique()),
        'properties.technical_test___create_date': 'first'
    }).reset_index()

    # Clean up the 'properties.industry' column by removing duplicates and sorting
    processed_data2['properties.industry'] = processed_data2['properties.industry'].apply(lambda x: ';'.join(sorted(set(x.split(';')), key=x.split(';').index)))

    return processed_data2