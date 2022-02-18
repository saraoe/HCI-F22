'''
Exercise 2:
- Add another three plots (you choose what to plot) and arrange them
    in a grid (two columns)
- Add controls that allow the user to decide on aspects of the
    visualization:
    - E.g. whether to color by country or not, whether to show data from a
        particular year, etc. 
'''
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# import data
df = pd.DataFrame(px.data.gapminder())

st.title('Exercise 2')

min_year = min(df['year'])
max_year = max(df['year'])

year = st.sidebar.slider('Choose maximum year', min_year, max_year, max_year)
df = df[df['year']<=year]

if st.sidebar.checkbox("Show data frame"):
    st.dataframe(df)

# plots
continents = df['continent'].unique()
continent = st.sidebar.selectbox('Select a continent', continents)
dfc = df[df['continent']==continent]
fig1 = px.line(dfc, x="year", y="lifeExp", color='country')
st.plotly_chart(fig1)

countries = dfc['country'].unique()
country = st.sidebar.selectbox('Select a country', countries)
country_df = df[df['country']==country]

fig2, (ax1, ax2) = plt.subplots(1,2)
fig2.suptitle('Life Expectancy according to...')
ax1.plot(country_df['gdpPercap'], country_df['lifeExp'], label=country)
ax1.set_title('gdpPercap')
ax2.plot(country_df['pop'], country_df['lifeExp'])
ax2.set_title('pop')
fig2.legend()
st.pyplot(fig2)