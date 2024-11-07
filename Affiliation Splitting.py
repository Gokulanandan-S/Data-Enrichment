import pandas as pd
import re

# Load the CSV file with a specified encoding
df = pd.read_csv(r'C:\Users\Anandan Suresh\Documents\Roche\Data enrichment\cleaned_data.csv', encoding='iso-8859-1')

# Define a function to extract the organization and other details from affiliation
def extract_affiliation_details(affiliation):
    if isinstance(affiliation, str):  # Check if the affiliation is a string
        # List of keywords in the order of preference
        organization_keywords = ['university', 'hospital', 'college', 'institute', 'school', 'center', 'universitat', 'universidad', 
                                 'universitaria', 'universiteit', 'universitas', 'univ', 'instituto', 'institut', 'health', 'medical sciences', 
                                 'research', 'sciences', 'laboratory', 'foundation', 'medical', 'clinical', 'bio', 'science', 'innovation', 
                                 'techno', 'museum', 'centre', 'consulting']
        
        # Split the affiliation string into parts and clean up extra spaces
        parts = [part.strip() for part in affiliation.split(',')]
        
        # Initialize dictionary for the extracted data
        affiliation_details = {
            'department': None,
            'organization': None,
            'city': None,
            'state': None,
            'country': None,
            'zip_code': None
        }

        # Extract organization name based on the defined keywords
        for keyword in organization_keywords: 
            for part in parts:
                if keyword in part.lower():  # Case insensitive check
                    affiliation_details['organization'] = part.strip()
                    break  # Once the first matching organization is found, stop checking

        # If organization is found, attempt to extract the department
        if affiliation_details['organization']:
            # Look for department in the part before the organization, or other nearby parts
            org_index = parts.index(affiliation_details['organization'])
            if org_index > 0:  # If there is a part before the organization
                affiliation_details['department'] = parts[org_index - 1].strip()

        # For city, state, and country, use regex to identify common patterns
        pattern = re.compile(r'(\b\w+\b(?:[\s-]\w+)*),\s*(\b\w+\b(?:[\s-]\w+)*),\s*(\b\w+\b(?:[\s-]\w+)*),\s*(\d{5}|\d{5}-\d{4})?')
        match = pattern.search(affiliation)
        
        if match:
            affiliation_details['city'] = match.group(1)
            affiliation_details['state'] = match.group(2)
            affiliation_details['country'] = match.group(3)
            affiliation_details['zip_code'] = match.group(4)
        
        return affiliation_details
    else:
        # Return None or an empty dictionary if the affiliation is not a string
        return {
            'department': None,
            'organization': None,
            'city': None,
            'state': None,
            'country': None,
            'zip_code': None
        }

# Apply the function to the 'affiliation' column and expand the dictionary into separate columns
affiliation_data = df['affiliation'].apply(extract_affiliation_details)
affiliation_df = pd.json_normalize(affiliation_data)

# Combine the original dataframe with the extracted details
df = pd.concat([df, affiliation_df], axis=1)

# Save the updated DataFrame back to a CSV file
df.to_csv('Updated_Affiliation.csv', index=False)  # Adjust the path as necessary

