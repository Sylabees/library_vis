import pandas as pd
import streamlit as st

data = pd.read_csv('data/cleaned_bookshelf_09042025.csv')
st.write('## Authors')

st.write(f'Total number of authors in the catalogue: {data.Author.nunique()}')

author_substring = st.text_input('You can filter the Author Dropdown using a part of their name here.')
if author_substring is None:
    selected_author = st.selectbox('select an Author', data.Author.value_counts().keys())
else:
    sub_selectbox = data[data.Author.str.lower().str.contains(author_substring.lower())].Author.value_counts().keys()
    selected_author = st.selectbox('select an Author', sub_selectbox)

author_data = data.query('Author == @selected_author').reset_index(drop=True)

st.write(author_data.rename(columns = {'Name':'Books'}).Books.str.title().unique())

if len(author_data.Series.value_counts().keys()) == 0:
    pass
else:
    st.write('aa', author_data.Series.value_counts().keys())

