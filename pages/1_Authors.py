import pandas as pd
import streamlit as st

data = pd.read_csv('data/cleaned_bookshelf_27042025.csv')
st.write('## Authors')

st.write(f'Total number of authors in the catalogue: {data.Author.nunique()}')

author_substring = st.text_input('You can filter the Author Dropdown using a part of their name here.')
if author_substring is None:
    selected_author = st.selectbox('Select an Author', data.Author.value_counts().keys())
else:
    sub_selectbox = data[data.Author.str.lower().str.contains(author_substring.lower())].Author.value_counts().keys()
    selected_author = st.selectbox('Select an Author', sub_selectbox)



author_data = data.query('Author == @selected_author').reset_index(drop=True)

book_names = author_data.rename(columns = {'Name':'Books'})['Books'].value_counts().keys()
st.write(f'{len(book_names)} books belonging to {selected_author}')

st.write(book_names)

num_series = len(author_data.Series.value_counts().keys())
if num_series == 0:
    pass
else:
    st.write(f'{num_series} series belonging to {selected_author}', author_data.Series.value_counts().keys())

