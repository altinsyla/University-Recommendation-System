import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from openai import OpenAI

# Leximi i file ne repository
current_dir = os.path.dirname(__file__)
datasets_dir = os.path.join(current_dir, '..', 'datasets')

analysis_path = os.path.join(datasets_dir, 'universities-dataset.csv')
prediction_path = os.path.join(datasets_dir, 'universities-degrees.csv')

analysis_df = pd.read_csv(analysis_path, encoding='latin1')
prediction_df = pd.read_csv(prediction_path, encoding='latin1')


st.sidebar.title("University Recommendation System")

if 'page' not in st.session_state:
    st.session_state.page = "Insights"

if st.sidebar.button("📊 Insights"):
    st.session_state.page = "Insights"

if st.sidebar.button("🔮 Predict Degree"):
    st.session_state.page = "Predict Degree"
    
if st.sidebar.button("University Degree"):
    st.session_state.page = "University Degree"

if st.session_state.page == "Insights":
    st.header("This page contains statistics about Degrees")

    if 'university_degree' not in analysis_df.columns or 'year' not in analysis_df.columns:
        st.error("The dataset does not contain the required columns: 'university_degree', 'year', 'Female', 'Male'.")
    else:
        universities = analysis_df['university_degree'].unique()
        selected_university = st.selectbox("Select a University degree", ["Select a Degree"] + list(universities))
        
        if selected_university == "Select a Degree":
            st.write("Please select a university degree to view statistics.")
        else:
            with st.spinner('Loading statistics...'):
                university_df = analysis_df[analysis_df['university_degree'] == selected_university]
                st.write(f"### Statistics for {selected_university}")

                try:
                    pivot_df = university_df.pivot(index="year", columns='university_degree', values=["Female", "Male"])
                    fig, ax = plt.subplots(figsize=(10, 6))
                    colors = ['tab:red', 'tab:blue']
                    pivot_df.plot(kind="bar", ax=ax, color=colors, edgecolor='black', alpha=0.9)

                    for container in ax.containers:
                        ax.bar_label(container, label_type='edge', color='black', fontsize=10, padding=5, weight='bold')

                    ax.set_title(f"Number of Students by Gender Over Years for {selected_university}")
                    ax.set_xlabel("Year")
                    ax.set_ylabel("Number of Students")
                    ax.legend(title="Gender")
                    st.pyplot(fig)
                    st.info('The statistics are taken from the Kosovo Agency of Statistics (ASK) and are 100% accurate.', icon="📝")
                except Exception as e:
                    st.error(f"Error generating pivot table or plot: {e}")

elif st.session_state.page == "Predict Degree":
    st.header("Find the Best Degree for You")

    avg_grade = st.number_input("Enter your average grade", min_value=3.0, max_value=5.0, step=0.1)

    if 'Category' not in prediction_df.columns or 'Skills' not in prediction_df.columns or 'Min Grade' not in prediction_df.columns:
        st.error("The prediction dataset does not contain the required columns: 'Category', 'Skills', 'Min Grade'.")
    else:
        
        categories = prediction_df['Category'].unique().tolist()
        selected_categories = st.multiselect("Select Categories", options=categories)

        if selected_categories:
            filtered_skills = prediction_df[prediction_df['Category'].isin(selected_categories)]['Skills']
            unique_skills = set(skill.strip() for sublist in filtered_skills for skill in sublist.split(','))
        else:
            unique_skills = []

        selected_skills = st.multiselect("Select Skills", options=list(unique_skills))

        if st.button("Predict"):
            if avg_grade == 0.0 or not selected_categories or not selected_skills:
                st.warning("Please fill in all fields before predicting.")
            else:
                
                def count_category_overlap(degree_categories):
                    return len(set(degree_categories.split(',')) & set(selected_categories))

                prediction_df['Category Overlap'] = prediction_df['Category'].apply(count_category_overlap)

                def count_skill_overlap(degree_skills):
                    degree_skills_set = set(degree_skills.split(',')) if pd.notna(degree_skills) else set()
                    return len(degree_skills_set & set(selected_skills))

                prediction_df['Skill Overlap'] = prediction_df['Skills'].apply(count_skill_overlap)

                recommendations = prediction_df[
                    (prediction_df['Min Grade'] <= avg_grade) & 
                    (prediction_df['Category Overlap'] > 0)
                ]

                recommendations = recommendations.sort_values(by=['Skill Overlap', 'Category Overlap'], ascending=False)

                if not recommendations.empty:
                    st.write("### Recommended degrees (based on the closest match):")
                    for _, degree in recommendations.iterrows():
                        st.write(f"#### Degree: **{degree['University Degree']}**")
                        st.write(f"- **Category**: {degree['Category']}")
                        st.write(f"- **Skills**: {degree['Skills']}")
                        st.write(f"- **Skill Matches**: {degree['Skill Overlap']}")
                        st.write(f"- **Minimum Grade**: {degree['Min Grade']}")
                        st.write("---")
                else:
                    st.warning("No programs match your criteria. Try selecting fewer skills or different categories.")

elif st.session_state.page == "University Degree":
    st.header("Explore University Degrees and Their Programs")
    
    degrees = [
        {
            "title": "Engineering",
            "image": "https://cdn.mos.cms.futurecdn.net/HFUAjfbamNhbM8dsNSQW3D-1200-80.jpg",
            "programs": ["Civil Engineering", "Mechanical Engineering", "Electrical Engineering", "Computer Science", "Telecommunication Engineering"],
            "min grade": [3.5, 3.5, 3.5, 4, 3.5]
        },
        {
            "title": "Education",
            "image": "https://cdn.elearningindustry.com/wp-content/uploads/2022/02/shutterstock_1112381495.jpg",
            "programs": ["Early Childhood Education", "Primary School Teaching", "Secodary School Teaching"],
            "min grade": [3, 3.5, 4]
        },
        {
            "title": "Art and Human Resources",
            "image": "https://www.shutterstock.com/image-vector/human-resources-vector-banner-design-260nw-584118919.jpg",
            "programs": ["Fine Arts", "Graphic Design", "Human Resources Management", "Performin Arts", "Public Relations"],
            "min grade": [3, 3.5, 3.5, 3, 3]
        },
        {
            "title": "Social Sciences",
            "image": "https://media.geeksforgeeks.org/wp-content/uploads/20231227161649/Branches-copy.webp",
            "programs": ["Psychology", "Sociology", "Political Science", "Anthroplogy"],
            "min grade": [3.5, 3, 3, 3]
        },
        {
            "title": "Business",
            "image": "https://www.marketing91.com/wp-content/uploads/2021/02/Business.jpg",
            "programs": ["Business Administration", "Finance", "Marketing", "International Business"],
            "min grade": [3.5, 3.5, 3, 3.5]
        },
        {
            "title": "Natural Science",
            "image": "https://img.freepik.com/premium-vector/natural-science-illustrations-with-leaves-surrounding-illustration_1280751-84079.jpg",
            "programs": ["Physics", "Chemistry", "Biology", "Environmental Science", "Geology"],
            "min grade": [3.5, 3.5, 3, 3, 3]
        },
        {
            "title": "Agriculture",
            "image": "https://stimulo.com/wp-content/uploads/2024/03/DALL%C2%B7E-2024-03-22-12.01.06-Create-a-realistic-banner-that-subtly-integrates-agrotech-elements-into-a-traditional-farming-scene.-The-image-should-include-a-farm-with-a-combinatio-1024x585.webp",
            "programs": ["Agronomy", "Horticulture", "Animal Science", "Agriculture Engineering", "Agriculture Economics"],
            "min grade": [3, 3, 3, 3.5, 3]
        },
        {
            "title": "Medicine",
            "image": "https://bernardmarr.com/wp-content/uploads/2023/11/The-Future-Of-Medicine_-How-AI-is-Shaping-Patient-Care-And-Drug-Discovery.jpg",
            "programs": ["Medicine (MBBS)", "Nursing", "Pharamacy", "Dentistry", "Public Health"],
            "min grade": [4, 4, 4, 4, 3.5]
        },
        {
            "title": "Services",
            "image": "https://www.aeccglobal.my/images/2023/01/31/study-culinary-arts-abroad.webp",
            "programs": ["Hospitality Management", "Culinary Arts", "Event Management", "Travel and Tourism", "Retail Management"],
            "min grade": [3.5, 3, 3, 3, 3]
        }
    ]
    
    if "selected_degree" not in st.session_state:
        st.session_state.selected_degree = None

    for i in range(0, len(degrees), 2):
        col1, col2 = st.columns(2)

        # For the first degree
        degree1 = degrees[i]
        with col1:
            st.markdown(f"<h5>{degree1['title']}</h5>", unsafe_allow_html=True)
            st.image(degree1["image"], width=300)
            with st.expander(f"Explore Programs ({degree1['title']})"):
                for program, min_grade in zip(degree1["programs"], degree1["min grade"]):
                    st.write(f"- **{program}** (Min Grade: {min_grade})")
        
        # For the second degree (if it exists)
        if i + 1 < len(degrees):
            degree2 = degrees[i + 1]
            with col2:
                st.markdown(f"<h5>{degree2['title']}</h5>", unsafe_allow_html=True)
                st.image(degree2["image"], width=300)
                with st.expander(f"Explore Programs ({degree2['title']})"):
                    for program, min_grade in zip(degree2["programs"], degree2["min grade"]):
                        st.write(f"- **{program}** (Min Grade: {min_grade})")
