import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv('data/cleaned_bookshelf_27042025.csv')

st.write('Library catalogue last updated 27th April 2025')


### Data prep for charts - move to data prep notebook eventually..
## Pub Year Pie Chart
pub_year_years = list(df['Pub Year'].value_counts().keys())
pub_year_counts = list(df['Pub Year'].value_counts().values)

pub_year_df = pd.DataFrame({
    'pub_year': pub_year_years,
    'frequency': pub_year_counts
}).sort_values('pub_year', ascending=False).reset_index(drop=True)

pub_year_df['pub_year'] = pub_year_df['pub_year'].astype(int)
pub_year_df['pseudo_pub_year'] = pub_year_df['pub_year']
pub_year_df.loc[pub_year_df.query("pub_year < 2017").index, 'pseudo_pub_year'] = 2016

pub_year_df = pub_year_df.groupby(['pseudo_pub_year'])['frequency'].sum().reset_index(drop=False).sort_values('pseudo_pub_year', ascending=False)
pub_year_df['pseudo_pub_year'] = pub_year_df['pseudo_pub_year'].replace(2016, 'previous years')

## Fiction/Non-Fiction
fic_nonfic = df.groupby('Fiction / non-fiction').size().reset_index(drop=False)
fic_nonfic.columns = ['fiction', 'frequency']


PageN = df.groupby('page_number_group').size().reset_index(drop=False)
PageN.columns = ['PageN', 'frequency']

## Genre
prim_gen = df.groupby(['Primary Genre']).size().reset_index(drop=False)
prim_gen.columns = ['genre', 'frequency']

## Cost of books
price_df = df.groupby('price').size().reset_index(drop=False)
price_df.columns = ['price', 'frequency']


## Book Type
df['BookType'] = df['BookType'].str.replace("Paperback With Flaps", "Paperback").replace("Flexiback", "Paperback").replace("Butchered Hardback", "Hardback")

booktype_df_keys = list(df['BookType'].value_counts().keys())
booktype_df_vals = list(df['BookType'].value_counts().values)

booktype_df = pd.DataFrame({
    'BookType': booktype_df_keys,
    'frequency': booktype_df_vals
}).sort_values('BookType', ascending=False).reset_index(drop=True)

## Define chart configs
charts_config = [
    {
        'title': 'Year of Publication',
        'type': 'pie',
        'labels': pub_year_df['pseudo_pub_year'],
        'values': pub_year_df['frequency'],
        'figsize':(4,4.48)
    },
    {
        'title': 'Fiction/Non-Fiction Split',
        'type': 'pie',
        'labels': fic_nonfic['fiction'],
        'values': fic_nonfic['frequency'],
        'figsize':(4,4)
    },
    {
        'title': 'Book Length',
        'type': 'pie',
        'labels': PageN['PageN'],
        'values': PageN['frequency'],
        'figsize':(4,4)
    },
    {
        'title': 'Cost of Books',
        'type': 'pie',
        'labels': price_df['price'],
        'values': price_df['frequency'],
        'figsize':(4,4)
    },
    {
        'title': 'Genre',
        'type': 'barh',
        'labels': prim_gen.sort_values('frequency', ascending=False).genre,
        'values': prim_gen.sort_values('frequency', ascending=False).frequency,
        'figsize':(4,7)
    },
    {
        'title': 'Book Type',
        'type': 'barh',
        'labels': booktype_df.sort_values('frequency', ascending=False).BookType,
        'values': booktype_df.sort_values('frequency', ascending=False).frequency,
        'figsize':(4,5.6)
    },
]

col1, col2 = st.columns(2)
for i, chart in enumerate(charts_config):
    fig, ax = plt.subplots(figsize=chart.get('figsize'))

    if chart['type'] == 'pie':
        ax.pie(chart['values'], labels=chart['labels'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_position([0.1, 0.1, 0.8, 0.8])
    elif chart['type'] == 'bar':
        ax.bar(chart['labels'], chart['values'], color='skyblue')
        ax.set_ylabel('Value')
        ax.set_position([0.1, 0.1, 0.8, 0.8])
    elif chart['type'] == 'barh':
        ax.barh(chart['labels'], chart['values'], color='skyblue')
        ax.set_ylabel('Value')
        ax.set_position([0.1, 0.1, 0.8, 0.8])

    # Assign to correct column
    with (col1 if i % 2 == 0 else col2):
        st.subheader(chart['title'])
        st.pyplot(fig)