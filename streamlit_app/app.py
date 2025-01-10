import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

analysis_df = pd.read_csv(r'C:\Users\PULSE Electronics\OneDrive\Desktop\universities-dataset.csv', encoding='latin1')
prediction_df = pd.read_csv(r'C:\Users\PULSE Electronics\OneDrive\Desktop\universities-degrees.csv', encoding='latin1')

st.sidebar.title("University Recommendation System")
if 'page' not in st.session_state:
    st.session_state.page = "Insights"

if st.sidebar.button("📊 Insights"):
    st.session_state.page = "Insights"

if st.sidebar.button("🔮 Predict Degree"):
    st.session_state.page = "Predict Degree"

if st.session_state.page == "Insights":
    st.header("This page contains statistics about Degrees")

    if 'university_degree' not in analysis_df.columns or 'year' not in analysis_df.columns:
        st.error("The dataset does not contain the required columns: 'university_degree', 'year', 'Female', 'Male'.")
    else:
        universities = analysis_df['university_degree'].unique()
        selected_university = st.selectbox("Select a University degree", universities)
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
        except Exception as e:
            st.error(f"Error generating pivot table or plot: {e}")

elif st.session_state.page == "Predict Degree":
    st.header("Find the Best Degree for You")

    avg_grade = st.number_input("Enter your average grade", min_value=3.0, max_value=5.0, step=0.1)

    if 'Category' not in prediction_df.columns or 'Skills' not in prediction_df.columns or 'Min Grade' not in prediction_df.columns:
        st.error("The prediction dataset does not contain the required columns: 'Category', 'Skills', 'Min Grade'.")
    else:
        categories = prediction_df['Category'].unique()
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
                    degree_skills_set = set(degree_skills.split(','))
                    return len(degree_skills_set & set(selected_skills))

                prediction_df['Skill Overlap'] = prediction_df['Skills'].apply(count_skill_overlap)

                recommendations = prediction_df[
                    (prediction_df['Min Grade'] <= avg_grade) &
                    (prediction_df['Category Overlap'] > 0) &
                    (prediction_df['Skill Overlap'] > 0)
                ]

                recommendations = recommendations.sort_values(by=['Category Overlap', 'Skill Overlap'], ascending=False)

                if not recommendations.empty:
                    best_skills_count = recommendations.iloc[0]['Skill Overlap']

                    # Check for multiple degrees with the same number of matching skills
                    matching_degrees = recommendations[recommendations['Skill Overlap'] == best_skills_count]

                    if len(matching_degrees) > 1:
                        st.write("### You fit on multiple degrees:")

                        for _, degree in matching_degrees.iterrows():
                            st.write(f"#### Degree: **{degree['University Degree']}**")
                            st.write(f"- **Category**: {degree['Category']}")
                            st.write(f"- **Skills**: {degree['Skills']}")
                            st.write(f"- **Minimum Grade**: {degree['Min Grade']}")
                            st.write("---")
                    else:
                        best_degree = recommendations.iloc[0]
                        st.write(f"### Based on the categories and skills you offered, the best matching degree is **{best_degree['University Degree']}**.")
                        st.write(f"**Reason**: This degree has the most categories and skills that match your preferences.")
                        st.write(f"#### Degree Details:")
                        st.write(f"- **Category**: {best_degree['Category']}")
                        st.write(f"- **Skills**: {best_degree['Skills']}")
                        st.write(f"- **Minimum Grade**: {best_degree['Min Grade']}")
                else:
                    st.warning("No programs match your criteria.")
