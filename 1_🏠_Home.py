import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

# from streamlit_option_menu import option_menu

# from annotated_text import annotated_text

# import time


st.set_page_config(page_title="Home", page_icon="💰",layout="wide",menu_items={
        # 'Get Help': None,
        'Get Help': 'mailto:john@example.com',
        # 'Report a bug': None,
        'Report a bug': 'mailto:john@example.com',
        'About': "# About Stock Prediction App!"
    })
# st.set_page_config(page_title="Stock Prediction App", page_icon="💰",layout="wide")
# st.markdown("""
# <style>
# header{
#     visibility:hidden;
# }
# # .css-1rs6os.edgvbvh3{
# # visibility:hidden;
# # }
# footer{
#     visibility:hidden;
# }
# # footer:after{
# #     content:'Copyright @ 2022';
# #     display:block;
# #     position:relative;
# #     color:tomato;
# #     padding:5px;
# #     top:3px;
# # }

# # {
# #     visibility:hidden;
# # }

# # For padding top and bottom
# # div.block-container{
# #     padding-top:2rem !important;
# # }
# </style>
# """,unsafe_allow_html=True)
st.sidebar.success("# Welcome to Stock Prediction App! 👋")
# st.sidebar.success("# Welcome to Stock Prediction App! 👋",icon="✅")
# with st.sidebar:
#     st.write('hello')


# START = "2015-01-01"
# TODAY = date.today().strftime("%Y-%m-%d")
# START = st.date_input(
#     "From",
#     date.today())
# TODAY = st.date_input(
#     "To",
#     date.today())

bar = st.progress(0)
progress_status=st.empty()
progress_status.write("Please wait... "+str(0)+"%")

# selected = option_menu(
#     menu_title='Menu',
#     options=['Home','About'],
#     icons=["house","bank"],
#     menu_icon="cast",
#     orientation='horizontal',
# )
# if selected == "About":
#     from PIL import Image
#     image = Image.open('img.png')
#     # st.image(image, caption='About Us')
#     st.image(image)
#     st.video('https://youtu.be/GJBQ5xOmzWQ')
#     for i in range(99):
#         bar.progress(i+1)
#         progress_status.write("Please wait... "+str(i+1)+"%")
#         # time.sleep(0.00001)
#     bar.progress(100)
#     progress_status.write("✅ Completed... "+str(100)+"%")
#     st.stop()

st.title("Stock Prediction App")

# # stocks = {"AAPL","GOOG","MSFT","GME"}
# # selected_stock = st.selectbox("Select dataset for prediction", stocks);
# selected_stock = st.text_input('Enter stock ticker','AAPL')

# stocks = {"AAPL","GOOG","MSFT","GME"}
# selected_stock = st.selectbox("Select dataset for prediction", stocks);
selected_stock = st.text_input('Enter stock ticker','AAPL')
st.caption('The stock ticker field is case insensitive.')
if selected_stock=='':
    # st.error('The stock ticker field cannot be empty.', icon="🚨")
    st.warning('The default value (**AAPL**) of stock ticker field is being used.', icon="⚠️")
    selected_stock = 'AAPL'


START = st.date_input(
    "From",
    date(2015, 7, 6))
TODAY = st.date_input(
    "To",
    date.today())


# n_years = st.slider("Years of prediction",1,4)
n_years = st.slider("Years of prediction",1,10)
period = n_years * 365

@st.cache
def load_data(ticker):
    data = yf.download(ticker,START,TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Loading data...")
data = load_data(selected_stock)
data_load_state.text("Loading data...done!")

# data_load_state = st.text("Loading data...")
# with st.spinner('Wait for it...'):
#     data = load_data(selected_stock)
# data_load_state.text("Loading data...done!")

# data_load_state = st.markdown("_Loading data..._")
# with st.sidebar:
#     # with st.spinner('Wait for it...'):
#     data = load_data(selected_stock)
# data_load_state.markdown("_Loading data...done!_")

# data_load_state = st.markdown("_Loading data..._")
# data = load_data(selected_stock)
# data_load_state.markdown("_Loading data...done!_")

# st.subheader('Raw data')
# st.write(data.tail())
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

#Describing Data
st.subheader('Description of the data')
st.write(data.describe())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'],name='stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'],name='stock_close'))
    fig.layout.update(title_text="Time Series Data",xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Forecasting
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date":"ds","Close":"y"})

# m = Prophet()
# m.fit(df_train)
# future = m.make_future_dataframe(periods=period)
# forecast = m.predict(future)
m = Prophet()
try:
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
except ValueError:
    # st.error('Please select a valid range.')
    st.error('Please enter a valid stock ticker and select a valid range.', icon="🚨")


# st.subheader('Forecast data')
# # st.write(forecast.tail())
# st.write(forecast)

st.subheader('Forecast data')
# st.write(forecast.tail())
try:
    st.write(forecast)
except NameError:
    st.write('No data to show.')
    # annotated_text(("No data to show.","","#8ef"))


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

# csv = convert_df(forecast)

# st.download_button(
#     label="Download data as CSV",
#     data=csv,
#     file_name='large_df.csv',
#     mime='text/csv',
# )
try:
    csv = convert_df(forecast)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )
except NameError:
    st.write()


# # st.write('forecast data')
# st.subheader('Original vs Predicted')
# fig1 = plot_plotly(m, forecast)
# st.plotly_chart(fig1)

# st.write('forecast data')
st.subheader('Original vs Predicted')
try:
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)
except NameError:
    st.write('No figure to show.')
    # annotated_text(("No figure to show.","","#8ef"))

# # st.write('forecast components')
# st.subheader('Visualisation')
# fig2 = m.plot_components(forecast)
# st.write(fig2)

# st.write('forecast components')
st.subheader('Visualisation')
try:
    fig2 = m.plot_components(forecast)
    st.write(fig2)
except NameError:
    st.write('No figure to show.')
    # annotated_text(("No figure to show.","","#8ef"))


for i in range(99):
    bar.progress(i+1)
    progress_status.write("Please wait... "+str(i+1)+"%")
    # time.sleep(0.00001)
bar.progress(100)
progress_status.write("✅ Completed... "+str(100)+"%")

# To hide the footer and hamburger completely
# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

