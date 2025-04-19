import pandas as pd
import streamlit as st

data = pd.read_csv('data/cleaned_bookshelf_09042025.csv')

#reshuffle booktype list
booktype_list = pd.Series(data['BookType'].unique())
booktype_list = booktype_list.dropna()
booktype_list = pd.concat([pd.Series([None]),booktype_list]).reset_index(drop=True)

#List of actual pub years for slider
year_list = [int(x) for x in pd.Series(data['Pub Year'].unique()).sort_values().dropna().reset_index(drop=True).values]

col1, col2 = st.columns(2)
author_surname = (col1.text_input('Author Name', value = None), 'Author')
genre = (col2.text_input('Genre', value = None), 'Genres')
publisher_name = (col1.text_input('Publisher Name', value = None), 'Publisher')
booktype = (col2.selectbox('BookType', booktype_list), 'BookType')

page_number = (st.slider('Number of Pages', 
                        min_value = 0, 
                        max_value = int(data['Page number'].max()),
                        value = (0,int(data['Page number'].max()))
                        ),'Page number')

year_published = (st.select_slider(
                        "Year of Publication",
                        options=year_list,
                        value=(1899, 2024),
                        ),'Pub Year')

# For the text fields where searching via substrings
for col_val, col_name in [author_surname, publisher_name, genre, booktype]:
    if col_val not in (None, ''):
        data[col_name] = data[col_name].fillna('')
        data = data[data[col_name].str.contains(col_val, case=False)]

# For the numerical fields with a range
for col_val, col_name in [page_number, year_published]:
    data = data[(data[col_name] >= col_val[0]) & (data[col_name] <= col_val[1])]

# # For the fields where exact matches are okay
# for col_val, col_name in [min_page_number, max_page_number]:
#     if col_val not in (None, ''):
#         data = data[data[col_name] == col_val]

st.write(data.set_index(data.columns[0]).drop(['Primary Genre numerical', 'To/From', 'surname'],axis=1))