import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.markdown("""
    <style>
        /* Custom Sidebar Styling */
        .css-18e3th9 {
            background-color: #f0f8ff;
            color: #1f1f1f;
        }
        
        #Sidebar Style
        .css-1d391kg {
            background-color: #ff0000; 
        }

        
        .css-1e2t2qt button {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            margin-bottom: 10px;
            text-align: center;
            background-color: #00bcd4;
            border: none;
            border-radius: 8px;
            color: white;
        }

        /* Custom Page Header */
        .main .block-container {
            padding-top: 2rem;
        }
        h1 {
            font-family: 'Arial', sans-serif;
            color: #4b0082;
        }
        h2 {
            font-family: 'Helvetica', sans-serif;
            color: #2f4f4f;
        }

        /* Custom text styling */
        .stMarkdown p {
            font-size: 18px;
            color: #333;
        }

        /* Styling the Plot */
        .matplotlib-figure {
            border: 2px solid #add8e6;
            border-radius: 10px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }

        /* Sidebar font color */
        .css-1wa3eu0 {
            color: #1f1f1f;
        }

        /* Add padding between different sections */
        .css-1g5jz3o {
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("University Recommendation System")

data = pd.read_csv(r'C:\Users\PULSE Electronics\OneDrive\Desktop\universities-dataset.csv')
df = pd.DataFrame(data)

df['year'] = df['year'].astype(int)

df_filtered = df[df['year'].isin([2022, 2023, 2024])]

if 'page' not in st.session_state:
    st.session_state.page = "Insights" 

if st.sidebar.button('📊 Insights'):
    st.session_state.page = "Insights"

if st.sidebar.button('🔮 Predict Degree'):
    st.session_state.page = "Predict Degree"

if st.session_state.page == "Insights":
    st.header("This page contains statistics about Degrees")

    
    universities = df_filtered['university_degree'].unique()

   
    selected_university = st.selectbox("Select a University degree", universities)

    
    university_df = df_filtered[df_filtered['university_degree'] == selected_university]

   
    st.write(f"### Statistics for {selected_university}")

    
    pivot_df = university_df.pivot(index="year", columns='university_degree', values=["Female", "Male"])

   
    fig, ax = plt.subplots(figsize=(10, 6))
    colors=['tab:red', 'tab:blue']
    pivot_df.plot(kind="bar", ax=ax, color=colors, edgecolor='black', alpha=0.9)

    
    ax.set_title(f"Number of Students by Gender Over Years for {selected_university}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Students")
    ax.legend(title="Gender")

   
    st.pyplot(fig)


elif st.session_state.page == "Predict Degree":
    st.header("🔮 Predict Degree")
    st.write("This feature is under development. Stay tuned for degree prediction functionality!")
