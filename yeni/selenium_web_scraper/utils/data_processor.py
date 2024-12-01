import pandas as pd
import re

def clean_text(text):
    """Clean and normalize text data
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text
    """
    if not isinstance(text, str):
        return text
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text.strip()

def extract_numeric(text):
    """Extract numeric values from text
    
    Args:
        text (str): Input text containing numbers
        
    Returns:
        float: Extracted numeric value
    """
    if not isinstance(text, str):
        return text
    
    # Find all numbers in the text
    numbers = re.findall(r'\d+\.?\d*', text)
    
    if numbers:
        return float(numbers[0])
    return None

def process_data(raw_data):
    """Process and clean scraped data
    
    Args:
        raw_data (dict): Raw scraped data
        
    Returns:
        dict: Processed data
    """
    processed_data = {}
    
    for key, value in raw_data.items():
        # Clean text fields
        cleaned_value = clean_text(value)
        
        # Extract numbers for numeric fields
        if any(field in key.lower() for field in ['price', 'rating', 'number', 'count']):
            processed_value = extract_numeric(cleaned_value)
        else:
            processed_value = cleaned_value
            
        processed_data[key] = processed_value
    
    return processed_data

def create_dataframe(data_list):
    """Convert list of processed data to DataFrame
    
    Args:
        data_list (list): List of dictionaries containing processed data
        
    Returns:
        pandas.DataFrame: Structured DataFrame
    """
    df = pd.DataFrame(data_list)
    
    # Convert numeric columns
    for col in df.columns:
        if any(field in col.lower() for field in ['price', 'rating', 'number', 'count']):
            df[col] = pd.to_numeric(df[col], errors='ignore')
    
    return df