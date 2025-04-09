import pandas as pd
import streamlit as st

data = pd.read_csv('cleaned_bookshelf_09042025.csv')
st.write(data)