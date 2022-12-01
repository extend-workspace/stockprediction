import streamlit as st

st.set_page_config(page_title="About", page_icon="🌍",layout="wide",menu_items={
        # 'Get Help': None,
        'Get Help': 'mailto:john@example.com',
        # 'Report a bug': None,
        'Report a bug': 'mailto:john@example.com',
        'About': "# About *Stock Prediction App*!"
    })

# st.markdown("""
# <style>
# # #MainMenu{
# # visibility:hidden;
# # }
# footer{
#     visibility:hidden;
# }
# # header{
# #     visibility:hidden;
# # }
# # footer:after{
# #     content:'Copyright @ 2022';
# #     display:block;
# #     position:relative;
# #     color:tomato;
# #     padding:5px;
# #     top:3px;
# # }
# </style>
# """,unsafe_allow_html=True)
st.sidebar.info('Learn more about us.', icon="ℹ️")

bar = st.progress(0)
progress_status=st.empty()
progress_status.write("Please wait... "+str(0)+"%")

from PIL import Image
image = Image.open('img.png')

# st.image(image, caption='About Us')
st.image(image)


st.video('https://youtu.be/GJBQ5xOmzWQ')
for i in range(99):
        bar.progress(i+1)
        progress_status.write("Please wait... "+str(i+1)+"%")
        # time.sleep(0.00001)
bar.progress(100)
progress_status.write("✅ Completed... "+str(100)+"%")








# 1_🏠_Home.py
# app.py