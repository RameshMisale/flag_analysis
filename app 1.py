import streamlit as st
import pandas as pd
from PIL import Image
import ast

flag_data = pd.read_csv("overallanalysis 3 1.csv")
all_keywords = sorted(set(flag_data['Keyword'].tolist())) 
st.set_page_config(page_title='Flag Data Viewer', layout='wide', initial_sidebar_state='expanded')
logo = Image.open('Logo.jpg')  
st.sidebar.image(logo, use_column_width=False, width=200)

st.markdown(
    """
    <style>
        .header {
            background-color: #78BE20;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 32px; /* Increased font size */
            margin-bottom: 10px;
        }
        .flag-name {
            font-size: 20px;
            font-weight: bold;
            display: inline-block;
            width: 200px; /* Adjust as needed */
        }
        .edit-button {
            font-size: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if 'selected_keyword' not in st.session_state:
    st.session_state.selected_keyword = None
    st.session_state.selected_3_keyword = None
    st.session_state.flag_checkboxes = {}  # Initialize flag_checkboxes attribute
    st.session_state.editing_flags = False  # Initialize editing_flags attribute

with st.sidebar:
    selected_keyword = st.selectbox("Select Keyword", all_keywords, key="select_keyword")
    
    if selected_keyword != st.session_state.selected_keyword:
        st.session_state.selected_keyword = selected_keyword
        filtered_keywords = sorted(set(flag_data[flag_data['Keyword'] == selected_keyword]['3 keywords'].tolist()))
        st.session_state.selected_3_keyword = None  # Reset selected 3 keyword if keyword changes
    else:
        filtered_keywords = sorted(set(flag_data[flag_data['Keyword'] == selected_keyword]['3 keywords'].tolist()))
    
    selected_3_keyword = st.selectbox("Select 3 Keyword", filtered_keywords, key="select_3_keyword")
    st.session_state.selected_3_keyword = selected_3_keyword  # Store selected 3 keyword in session state

if st.session_state.selected_keyword and st.session_state.selected_3_keyword:
    st.markdown('<div class="header">Profile Templatization for Selected Keyword</div>', unsafe_allow_html=True)

    keyword_data = flag_data[(flag_data['Keyword'] == st.session_state.selected_keyword) & (flag_data['3 keywords'] == st.session_state.selected_3_keyword)]
    if not keyword_data.empty:
        common_flags = keyword_data['Common flags'].iloc[0]
        changing_flags = keyword_data['changing flags'].iloc[0]

        st.write(f"### Common flags")
        st.write("Checked = '1'", " Unchecked = '0'")

        common_flags_dict = ast.literal_eval(common_flags)
        common_flags_dict = dict(sorted(common_flags_dict.items(), key=lambda x: x[1]))

        flag_names = list(common_flags_dict.keys())
        flag_values = list(common_flags_dict.values())

        # Calculate the number of flags per column
        num_flags_per_column = (len(flag_names) + 2) // 3

        columns = st.columns(3)

        edit_common_flags_button = st.button('Edit Common Flags', key="edit_common_flags_button")

        if edit_common_flags_button:
            st.session_state.flag_checkboxes = {}  
            st.session_state.editing_flags = True  

        for i in range(3):
            start_index = i * num_flags_per_column
            end_index = min((i + 1) * num_flags_per_column, len(flag_names))

            with columns[i]:
                for j in range(start_index, end_index):
                    flag_name = flag_names[j]
                    flag_value = common_flags_dict[flag_name]
                    st.write(f"{flag_name}:")
                    if st.session_state.editing_flags:
                        if flag_value not in (0, 1):
                            flag_value = st.text_input(label='', value=str(flag_value), key=f"{st.session_state.selected_keyword}_{flag_name}_textinput")
                        else:
                            flag_value = st.checkbox(label='', value=flag_value, key=f"{st.session_state.selected_keyword}_{flag_name}_checkbox_{flag_name}")
                            st.session_state.flag_checkboxes[f"{st.session_state.selected_keyword}_{flag_name}_checkbox_{flag_name}"] = flag_value
                    else:
                        if flag_value not in (0, 1):
                            flag_value = st.text(flag_value)
                        else:
                            flag_value = st.checkbox(label='', value=st.session_state.flag_checkboxes.get(f"{st.session_state.selected_keyword}_{flag_name}_checkbox_{flag_name}", False), disabled=True, key=f"{st.session_state.selected_keyword}_{flag_name}_checkbox_{flag_name}")

        st.write(f"### Changing flags")
        changing_flags_list = changing_flags.split(',')
        for i in range(0, len(changing_flags_list), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(changing_flags_list):
                    flag_col1, flag_col2 = cols[j].columns([0.1,1], gap='small')
                    
                    flag_col1.checkbox(label='', key=f"{st.session_state.selected_keyword}_{changing_flags_list[i + j].strip()}_checkbox")
                    flag_col2.write(f"{changing_flags_list[i + j].strip()}:")

        if st.button('Save Profile'):
            st.write("The profile is saved successfully.")

        st.markdown("____________________________________________________________________________________")
        st.write("*2024 Clean Earth")
