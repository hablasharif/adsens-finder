import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def extract_adsense_id(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for the AdSense client ID pattern
        adsense_script = soup.find('script', {'src': re.compile(r'https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js.*')})

        if adsense_script:
            # Extract the client ID using regular expressions
            match = re.search(r'client=(ca-pub-\d+)', adsense_script['src'])
            if match:
                adsense_id = match.group(1)
                return adsense_id

        return None  # AdSense ID not found

    except Exception as e:
        raise e  # Raise the exception to be handled by streamlit

# Create a title for the app
st.title("AdSense ID Extractor")

# Create a text input widget for the user to enter a website URL
url = st.text_input("Enter a website URL")

# Create a button widget to run the function
if st.button("Extract AdSense ID"):
    # Try to run the function and display the output or error
    try:
        adsense_id = extract_adsense_id(url)
        if adsense_id:
            st.write(f"The AdSense client ID for the website is: {adsense_id}")
        else:
            st.write("AdSense ID not found on the website.")
    except Exception as e:
        st.exception(e)  # Display the exception as an alert
