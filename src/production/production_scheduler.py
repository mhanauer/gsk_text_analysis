import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_reviews(base_url):
    headers = {"User-Agent": "Mozilla/5.0"}

    reviews_list = []

    for page in range(1, 11):  # adjust range as necessary
        url = f"{base_url}?conditionid=&sortval=1&page={page}&next_page=true"
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")
        reviews = soup.find_all("div", class_="description")

        for review in reviews:
            review_dict = {}
            visible_text = review.find("span", class_="showSec")
            hidden_text = review.find("span", class_="hiddenSec")

            # If there's visible text, add it to the review dictionary
            if visible_text:
                review_dict["text"] = visible_text.text.strip()
            # If there's hidden text, append it to the review dictionary
            if hidden_text:
                review_dict["text"] += " " + hidden_text.text.strip()

            reviews_list.append(review_dict)

    return pd.DataFrame(reviews_list)


st.title('Web Scraper for Reviews')
base_url = st.text_input('Enter the base URL', '')
if base_url:
    df = get_reviews(base_url)
    df = df.dropna().reset_index(drop=True)
    st.dataframe(df)