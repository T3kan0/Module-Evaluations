#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  19 08:37:00 2021

@author: nt4-nani
"""


import streamlit as st
import pandas as pd
import time
from fpdf import FPDF
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import string

st.set_page_config(
    page_title="Evaluations",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.sidebar.markdown("![Alt Text](https://i.postimg.cc/gJzPdRYd/logio.png)")


eval_files = st.sidebar.file_uploader(' ',
                                     type=['xlsx', 'csv'],
                                     accept_multiple_files=True)


st.markdown("""
<style>
.header-card {
    text-align: center;
    padding: 20px;
    margin-bottom: 15px;
    border-radius: 12px;
    background: linear-gradient(to right, #1E1A4D, #440E03); /* L→R */
    box-shadow: 0 4px 10px rgba(0,0,0,0.25);
    border: 3px solid #1C398E;  /* 👈 adds border */
}
.header-card h3 {
    margin: 0;
    font-weight: 700;
    color: #E2E8F0;
}
.header-card h4 {
    margin-top: 6px;
    font-weight: 500;
    color: #E2E8F0;
}
</style>
<div class="header-card">
  <h3>A_STEP Tutorial & Tutor Evaluations</h3>
  <h4>A.T & T.E.</h4>
</div>
""", unsafe_allow_html=True)



st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.postimg.cc/1tMyy904/eval-logo.png" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)


# Your expander element
with st.expander(":blue[Read More ⤵️]"):
    st.write('Welcome to the Evaluation of A_STEP Tutorials and Tutors. Programme evaluation is a valuable tool for the coninued success of\
         A_STEP, positioned in the UFS academic faculties as a student academic support service.\
         This is particularly imperative when seeking to strengthen the quality of the programme and improve academic outcomes\
         for the programme, and the students it is serving. Therefore, programme evaluation provides basic questions about a programmes’s effectiveness,\
         and evaluation data can be used to improve programme services. At the core of the evaluation in the SLE programme is to give students a platform\
         to reflect on the experiences on the online tutorials they have attended, but it also allows those who did not attend a space to provide their views.\
         The practice is helping the programme to address common concerns that students might have regarding the service they obtain from the programme,\
         how it can benefit by improving quality assurance, monitoring, and optimizing student-learning opportunities.')
      
cola = st.columns([1.00], gap='small')
if eval_files:
    st.sidebar.success('File Uploaded', icon="✅")
    Eval = st.sidebar.button("🚀 Generate Report", key="generate_btn")

else:        
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.postimg.cc/hP87QCG1/people-hold-arrow.png" alt="Logo">
        </div>
        """,
        unsafe_allow_html=True
    )


if eval_files is not None:
    n_file = []
    f_name = []
    camp = []
    Tutor_cnt = []
    gend = []
    Prog = []
    Lang = []
    for file in eval_files:
        df = pd.read_excel(file)  # You may use pd.read_csv(file) for CSV files
        fname = file.name[0:8]
        tutor_column = df['2: Kindly enter your student number'].nunique()
        Cmp = df['3.0: Which campus are you enrolled at?'].unique()
        Gend = df['4.0: What is your gender?'].nunique()
        prog = df['6.0: Which programme are you enrolled in?'].unique()
        ProgN = df['6.0: Which programme are you enrolled in?'].nunique()
        lang = df['5.0: What is your home language?'].nunique()
        
        Tutor_cnt.append(tutor_column)
        camp.append(Cmp)
        f_name.append(fname)
        gend.append(Gend)
        Prog.append(prog)
        Lang.append(lang)

        # Groupby Gender
        gend_data = df.groupby('4.0: What is your gender?').agg({'2: Kindly enter your student number': 'nunique',
                                                                 '5.0: What is your home language?': 'nunique',
                                                                 '6.0: Which programme are you enrolled in?':'nunique'}).reset_index()
        color_palette = {
        'Red': '#FF5733',
        'Orange': '#FF8D1A',
        'Yellow': '#FFC300',
        'Green': '#28B463',
        'Blue': '#3498DB',
        'Purple': '#9B59B6',
        'Pink': '#FF69B4',
        'Brown': '#8B4513',
        'Gray': '#95A5A6',
        'Black': '#2C3E50'}

        def collapse_outcome(counts):
            """
            Collapse Likert responses into a single outcome.
            counts: dict with keys like {"Strongly Disagree": x, "Disagree": y, "Neutral": z, "Agree": a, "Strongly Agree": b}
            Returns one of: Strongly Disagree, Disagree, Neutral, Agree, Strongly Agree
            """
            # Likert scale mapping
            likert_map = {
                "Strongly Disagree": 1,
                "Disagree": 2,
                "Neutral": 3,
                "Agree": 4,
                "Strongly Agree": 5
            }
            
            # Ensure all 5 labels are present
            labels = list(likert_map.keys())
            counts = counts.reindex(labels, fill_value=0)

            
            total_votes = counts.sum()
            if total_votes == 0:
                return "Neutral"  # fallback if no responses
    
            # Weighted average
            score_sum = sum(likert_map[label] * count for label, count in counts.items())
            avg_score = score_sum / total_votes
    
            # Convert back to label by rounding
            if avg_score < 1.5:
                return "Strongly Disagree"
            elif avg_score < 2.5:
                return "Disagree"
            elif avg_score < 3.5:
                return "Neutral"
            elif avg_score < 4.5:
                return "Agree"
            else:
                return "Strongly Agree"

        
        ### Categoric labels to characterize data outcomes

        positive_scale = ["Agree", "Strongly Agree"]
        neutral_scale = ["Neutral"]
        negative_scale = ["Disagree", "Strongly Disagree"]

        
         # Plotting the bar graph
        fig0, ax0 = plt.subplots()
        # Bar plot for number of unique students
        
        ax0.bar(gend_data['4.0: What is your gender?'], gend_data['2: Kindly enter your student number'], color=list(color_palette.values()), label='A_STEP Students', edgecolor='darkblue')
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)
        # Set labels and title
        ax0.set_xlabel('Gender')
        ax0.set_ylabel('A_STEP Students')
        ax0.tick_params('y', colors='darkblue')
        # Set y-axis limits for the first subplot

  
        # Line plot for mean final marks
        # Create a second y-axis for mean final marks
        ax2 = ax0.twinx()
    
        ax2.plot(gend_data['4.0: What is your gender?'], gend_data['5.0: What is your home language?'], color='firebrick', marker='o', label='Home Languages')
        ax2.set_ylabel('Home Languages', color='k')
        ax2.tick_params('y', colors='firebrick')
        # Set y-axis limits for the second subplot
        ax2.set_ylim(0, 15)  # Adjust the multiplier as needed


        plt.title('Comparison of Students and Home Languages per Gender')
        fig0.tight_layout(rect=[0, 0, 1.0, 1])  # Adjust the rect parameter as needed
        # Manually set the legend position
        fig0.legend(loc='upper right', bbox_to_anchor=(0.9, .93))
        # Add text annotations to the line plot
        for i, value in enumerate(gend_data['5.0: What is your home language?']):
            plt.text(x=gend_data['4.0: What is your gender?'][i], y=value + 1, s='%.2f' % value,
                 fontsize=10, ha='center', color='purple')
        plt.grid(axis='y', linestyle='--', alpha=0.7)            
        plt.savefig('marksVstd.png')

        # Groupby Language
        lang_data = df.groupby('5.0: What is your home language?').agg({'2: Kindly enter your student number': 'nunique',
                                                                 '6.0: Which programme are you enrolled in?':'nunique'}).reset_index()

        # Define a color palette using Seaborn
        num_colors = len(lang_data)
        palette = sns.color_palette("husl", num_colors)

        # Plot the bar graph
        fig, ax = plt.subplots()
        bars = ax.bar(lang_data['5.0: What is your home language?'], lang_data['2: Kindly enter your student number'], color=palette, edgecolor='darkblue', label='Home Languages')

        # Add title and labels
        ax.set_title('Number of Students by Home Languages')
        #ax.set_xlabel('Home Language')
        ax.set_ylabel('Number of Students')
        # Add bar labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:.0f}',  # Format the label with no decimal places
                ha='center', 
                va='bottom'
            )

        # Show plot
        plt.xticks(rotation=25)
        plt.legend()
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)        
        plt.savefig('lang.png')

        # Groupby prog
        prog_data = df.groupby('6.0: Which programme are you enrolled in?').agg({'2: Kindly enter your student number': 'nunique'}).reset_index()

        # Define a color palette using Seaborn
        num_colors = len(prog_data)
        palette = sns.color_palette("husl", num_colors)

        # Plot the bar graph
        fig, ax = plt.subplots()
        bars = ax.bar(prog_data['6.0: Which programme are you enrolled in?'], prog_data['2: Kindly enter your student number'], color=palette, edgecolor='darkblue', label='Academic Programmes')
        # Add title and labels
        ax.set_title('Number of Students by Academic Programmes')
        #ax.set_xlabel('Home Language')
        ax.set_ylabel('Number of Students')
        # Add bar labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:.0f}',  # Format the label with no decimal places
                ha='center', 
                va='bottom'
            )

        # Show plot
        plt.xticks(rotation=25)
        plt.legend()
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)        
        plt.savefig('prog.png')

        # Groupby prog
        enroll_data = df.groupby('7.0: What academic year are you in for the qualification you are currently enrolled in?').agg({'2: Kindly enter your student number': 'nunique'}).reset_index()

        # Define a color palette using Seaborn
        num_colors = len(enroll_data)
        palette = sns.color_palette("husl", num_colors)

        # Plot the bar graph
        fig, ax = plt.subplots()
        bars = ax.bar(enroll_data['7.0: What academic year are you in for the qualification you are currently enrolled in?'], enroll_data['2: Kindly enter your student number'], color=palette, edgecolor='darkblue', label='Academic Years')
        # Add title and labels
        ax.set_title('Number of Students by Academic Years')
        #ax.set_xlabel('Home Language')
        ax.set_ylabel('Number of Students')
        # Add bar labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:.0f}',  # Format the label with no decimal places
                ha='center', 
                va='bottom'
            )

        # Show plot
        plt.xticks(rotation=25)
        plt.legend()
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)        
        plt.savefig('enroll.png')

        # Groupby mark
        market_data = df.groupby('9.0: How did you hear about A_STEP tutorials for this module?').agg({'2: Kindly enter your student number': 'nunique'}).reset_index()

        # Define a color palette using Seaborn
        num_colors = len(market_data)
        palette = sns.color_palette("husl", num_colors)

        # Plot the bar graph
        fig, ax = plt.subplots()
        bars = ax.bar(market_data['9.0: How did you hear about A_STEP tutorials for this module?'], market_data['2: Kindly enter your student number'], color=palette, edgecolor='darkblue', label='A_STEP Marketing')
        # Add title and labels
        ax.set_title('A_STEP Popularity')
        #ax.set_xlabel('Home Language')
        ax.set_ylabel('Number of Students')
        # Add bar labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:.0f}',  # Format the label with no decimal places
                ha='center', 
                va='bottom'
            )

        # Show plot
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        # Adjust layout to ensure everything fits
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)        
        plt.savefig('market.png')


        # Filter columns starting with '9:' and exclude the first column
        columns_to_include = [col for col in df.columns if col.startswith('10:') and col != '10: What motivated you to attend tutorials? (Select all options that apply)  ']

        # Ensure the selected columns are numeric
        motiv_data = df[columns_to_include].apply(pd.to_numeric, errors='coerce')
        # Aggregate counts for each column
        reasons = motiv_data.sum().sort_values(ascending=False)
        
        # Define a color palette using Seaborn
        palette = sns.color_palette("husl", len(reasons))
        # Define new labels with line breaks for better readability
        new_labels = [
            'To better\nunderstand content\ncovered in class',
            'To prepare for\ntests and assessments',
            'To build\nrelationships with\npeers',
            #'Referred by\nlecturer',
            'Was encouraged\nto attend by\nsomeone else',
            #'Referred by\nAcademic advisor',
            #'Referred by\nGPS success coach',
            'Other'
        ]

        # Plot the bar graph
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(new_labels, reasons.values, color=palette, edgecolor='darkblue', label='Motivations for Attending Tutorials')

        # Add title and labels
        ax.set_title('Motivations for Attending Tutorials')
        ax.set_ylabel('Number of Students')
        #ax.set_xlabel('Reasons')

        # Add bar labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:.0f}',  # Format the label with no decimal places
                ha='center', 
                va='bottom'
            )

        # Show plot
        plt.xticks(rotation=20, ha='center')
        plt.legend()
        # Adjust layout to ensure everything fits
        plt.tight_layout()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig('motiv.png')

        multi_counts = df['11.0: Are you familiar with the concept of multilingualism or the use of multiple languages (in addition to English) in tutorial sessions?'].value_counts()

        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        multi_counts.plot(kind='bar', color=['cadetblue', 'turquoise'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('Are you familiar with the concept of multilingualism?')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('mutiling.png')   


####### Perception on Tutorial Sessions

        conduci_counts = df['16.1: The following questions are on the perception of the tutorial sessions.: Tutorial sessions helped me understand the concepts better'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        conduci_counts.plot(kind='bar', color=['springgreen', 'orangered', 'olivedrab', 'steelblue', 'crimson'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('Tutorial sessions helped me understand the concepts better')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('concepts.png')

        spacious_counts = df['16.2: The following questions are on the perception of the tutorial sessions.: I found the tutorial sessions helpful to my learning'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        spacious_counts.plot(kind='bar', color=['saddlebrown', 'wheat', 'powderblue', 'hotpink', 'lightgray'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('I found the tutorial sessions helpful to my learning')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('tuthelp.png')



        inter_counts = df['16.3: The following questions are on the perception of the tutorial sessions.: The tutorial sessions help me improve my academic performance'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        inter_counts.plot(kind='bar', color=['aquamarine', 'dodgerblue', 'peachpuff', 'saddlebrown', 'powderblue'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The tutorial sessions help me improve my academic performance')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('improve.png')

        interct_counts = df['16.4: The following questions are on the perception of the tutorial sessions.: I found the tutorial sessions well-planned'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        interct_counts.plot(kind='bar', color=['peachpuff', 'powderblue', 'crimson', 'gold', 'ivory'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('I found the tutorial sessions well-planned')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('plan.png')

        light_counts = df['16.5: The following questions are on the perception of the tutorial sessions.: I found the tutorial sessions well structured'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        light_counts.plot(kind='bar', color=['lightcoral', 'darkgoldenrod', 'springgreen', 'navy', 'fuchsia'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('I found the tutorial sessions well structured')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('structure.png')

        vent_counts = df['16.6: The following questions are on the perception of the tutorial sessions.: Tutorial sessions helped me feel prepared for assessments'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vent_counts.plot(kind='bar', color=['bisque', 'indigo', 'whitesmoke', 'thistle', 'lavenderblush'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('Tutorial sessions helped me feel prepared for assessments')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('prep.png')


        vent2_counts = df['16.7: The following questions are on the perception of the tutorial sessions.: The tutorial sessions helped me improve my communication skills'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vent2_counts.plot(kind='bar', color=['whitesmoke', 'indigo', 'bisque', 'thistle', 'crimson'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The tutorial sessions helped me improve my communication skills')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('comm.png')


        vent3_counts = df['16.8: The following questions are on the perception of the tutorial sessions.: I would recommend tutorials to other students.'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vent3_counts.plot(kind='bar', color=['whitesmoke', 'indigo', 'bisque', 'thistle', 'crimson'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('I would recommend tutorials to other students')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('recc.png')

############# Tutor Perception  


        conduci1_counts = df['17.1: The following questions are on the perception of the tutor: My tutor was on time'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        conduci1_counts.plot(kind='bar', color=['lavenderblush', 'fuchsia', 'ivory', 'crimson', 'lightgray'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('My tutor was on time')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('punc.png')


        spacious1_counts = df['17.2: The following questions are on the perception of the tutor: My tutor helped me with difficulties I encountered in the module'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        spacious1_counts.plot(kind='bar', color=['red', 'darkseagreen', 'rosybrown', 'peru', 'mistyrose'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title(' My tutor helped me with difficulties I encountered in the module')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('diffc.png')


        inter1_counts = df['17.3: The following questions are on the perception of the tutor: My tutor recognized that students are different'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        inter1_counts.plot(kind='bar', color=['honeydew', 'lavender', 'cyan', 'turquoise', 'orangered'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('My tutor recognized that students are different')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('diffr.png')


        interct1_counts = df['17.4: The following questions are on the perception of the tutor: My tutor made an effort to help me'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        interct1_counts.plot(kind='bar', color=['darkgoldenrod', 'ivory', 'olivedrab', 'aliceblue', 'lightcoral'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('My tutor made an effort to help me')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('efft.png')

        light1_counts = df['17.5: The following questions are on the perception of the tutor: My tutor gave me confidence to complete my assessments'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        light1_counts.plot(kind='bar', color=['darkgoldenrod', 'indigo', 'bisque', 'indigo', 'steelblue'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('My tutor gave me confidence to complete my assessments')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('conf.png')

        vent1_counts = df['17.6: The following questions are on the perception of the tutor: My tutor was interested in my academic progress'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vent1_counts.plot(kind='bar', color=['lavenderblush', 'ivory', 'mistyrose', 'hotpink', 'rebeccapurple'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('My tutor was interested in my academic progress')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('intr.png')


        conduci2_counts = df['17.7: The following questions are on the perception of the tutor: My tutor allowed me to use my home language to express myself'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        conduci2_counts.plot(kind='bar', color=['mistyrose', 'peru', 'darkseagreen', 'lavenderblush', 'lightgray'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('My tutor allowed me to use my home language to express myself')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('hlangu.png')


        # This list will be used for determining the string to be used to choose the paragraph that describes the tutorial quality evaluations outcome.
        # Applying the collapse function on the tutorial organisation questions Q16.
        
        tutorial_organisation_outcome = [
            collapse_outcome(conduci_counts),
            collapse_outcome(spacious_counts),
            collapse_outcome(inter_counts),
            collapse_outcome(interct_counts),
            collapse_outcome(light_counts),
            collapse_outcome(vent_counts),
            collapse_outcome(vent2_counts),
            collapse_outcome(vent3_counts)
        ]        
        
        # Applying the collapse function on the tutorial quality questions Q17.
        tutorial_quality_outcome = [
            collapse_outcome(conduci1_counts),
            collapse_outcome(spacious1_counts),
            collapse_outcome(inter1_counts),
            collapse_outcome(interct1_counts),
            collapse_outcome(light1_counts),
            collapse_outcome(vent1_counts),
            collapse_outcome(conduci2_counts)
        ]



########## Tutor Types

        conduci3_counts = df['18: Blackboard collaborate'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        conduci3_counts.plot(kind='bar', color=['mintcream', 'fuchsia', 'turquoise', 'peachpuff', 'rebeccapurple'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('Blackboard collaborate')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('mode.png')


        interct3_counts = df['18: Face-to-face'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        interct3_counts.plot(kind='bar', color=['hotpink', 'rebeccapurple', 'peru', 'lightgray', 'ivory'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('Face-to-face')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('mode2.png')


        interct3_counts = df['18: Both (face-to-face and blackboard collaborate)'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        interct3_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('Both (face-to-face and blackboard collaborate)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('mode3.png')


####### Face - to - Face tutorials sessions

        vanue1_counts = df['19.1: The following questions are on the perception of the tutorial venue (Face-to-face sessions): The venue where the tutorials took place was conducive to learning'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue1_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The venue where the tutorials took place was conducive to learning')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('conducive.png')


        vanue2_counts = df['19.2: The following questions are on the perception of the tutorial venue (Face-to-face sessions): The venue was spacious enough to accommodate the student(s).'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue2_counts.plot(kind='bar', color=['grey', 'darkkhaki', 'mediumslateblue', 'lightsalmon', 'peru'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The venue was spacious enough to accommodate the student(s)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('spacious.png')

        vanue3_counts = df['19.3: The following questions are on the perception of the tutorial venue (Face-to-face sessions): The venue made you comfortable to interact with the tutor'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue3_counts.plot(kind='bar', color=['mediumslateblue', 'thistle', 'plum', 'silver', 'turquoise', 'cyan'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The venue made you comfortable to interact with the tutor')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('inter.png')

        vanue4_counts = df['19.4: The following questions are on the perception of the tutorial venue (Face-to-face sessions): The venue made you comfortable to interact with your classmates'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue4_counts.plot(kind='bar', color=['bisque', 'darkorange', 'burlywood', 'antiquewhite', 'gold'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The platform made you comfortable to interact with the classmates?')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('interct.png')

        vanue5_counts = df['19.5: The following questions are on the perception of the tutorial venue (Face-to-face sessions): The venue had proper lighting'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue5_counts.plot(kind='bar', color=['fuchsia', 'mediumvioletred', 'hotpink', 'pink', 'lavenderblush'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The venue had proper lighting')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('light.png')

        vanue6_counts = df['19.6: The following questions are on the perception of the tutorial venue (Face-to-face sessions): The venue had proper ventilation'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue6_counts.plot(kind='bar', color=['azure', 'lavender', 'ghostwhite', 'cornsilk', 'mistyrose'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The venue had proper ventilation')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('vent.png')

############ Hybrid Venue Tutorial sessions

        vanue7_counts = df['20.1: The following questions are on the perception of the tutorial hybrid (face-to-face & online sessions): The venue where the tutorials took place was conducive to learning'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue7_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The venue where the tutorials took place was conducive to learning')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('conducive1.png')

        vanue8_counts = df['20.2: The following questions are on the perception of the tutorial hybrid (face-to-face & online sessions): The venue was spacious enough to accommodate the student(s).'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue8_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The venue was spacious enough to accommodate the student(s)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('spacious1.png')

        vanue9_counts = df['20.3: The following questions are on the perception of the tutorial hybrid (face-to-face & online sessions): The venue made you comfortable to interact with the tutor'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue9_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The venue made you comfortable to interact with the tutor')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('inter1.png')
        
        vanue10_counts = df['20.4: The following questions are on the perception of the tutorial hybrid (face-to-face & online sessions): The venue made you comfortable to interact with your classmates'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue10_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The venue made you comfortable to interact with your classmates')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('interct1.png')        
        
        vanue11_counts = df['20.5: The following questions are on the perception of the tutorial hybrid (face-to-face & online sessions): The venue had proper lighting'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue11_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The venue had proper lighting')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('light1.png') 

        vanue12_counts = df['20.6: The following questions are on the perception of the tutorial hybrid (face-to-face & online sessions): The venue had proper ventilation'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue12_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The venue had proper ventilation')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('vent1.png')         
 
        vanue13_counts = df['20.7: The following questions are on the perception of the tutorial hybrid (face-to-face & online sessions): The platform where the tutorials took place was conducive to learning'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue13_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The platform where the tutorials took place was conducive to learning')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('conducive2.png')          
 
        vanue14_counts = df['20.8: The following questions are on the perception of the tutorial hybrid (face-to-face & online sessions): The platform made you comfortable to interact with the tutor'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue14_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The platform made you comfortable to interact with the tutor')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('inter2.png')
        
        vanue15_counts = df['20.9: The following questions are on the perception of the tutorial hybrid (face-to-face & online sessions): The platform made you comfortable to interact with your classmates'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue15_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The platform made you comfortable to interact with the classmates')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('interct2.png')        
        
        vanue16_counts = df['20.10: The following questions are on the perception of the tutorial hybrid (face-to-face & online sessions): The platform was easy to navigate'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue16_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The platform was easy to navigate')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('navi.png')  

################### Online vanue ############

        vanue17_counts = df['21.1: The following questions are on the perception of the tutorial Platform (online sessions): The platform where the tutorials took place was conducive to learning'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue17_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The platform where the tutorials took place was conducive to learning')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('conducive3.png') 
        

        vanue18_counts = df['21.2: The following questions are on the perception of the tutorial Platform (online sessions): The platform made you comfortable to interact with the tutor'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue18_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The platform made you comfortable to interact with the tutor')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('inter3.png')


        vanue19_counts = df['21.3: The following questions are on the perception of the tutorial Platform (online sessions): The platform made you comfortable to interact with your classmates'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue19_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The platform made you comfortable to interact with the classmates?')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('interct3.png')

        vanue20_counts = df['21.4: The following questions are on the perception of the tutorial Platform (online sessions): The platform was easy to navigate'].value_counts()
        # Create a bar plot
        fig0, ax0 = plt.subplots(figsize=(8, 5))
        vanue20_counts.plot(kind='bar', color=['aquamarine', 'aliceblue', 'powderblue', 'bisque', 'mediumvioletred'], edgecolor='darkblue')  # Specify colors for 'yes' and 'no'
        ax0.bar_label(ax0.containers[0], fmt='%0.0f', label_type='edge', fontsize=10)


        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.title('The platform was easy to navigate')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.xticks(rotation=0)  # Rotate x-    
        plt.savefig('navi1.png')



        
        # Filter columns that start with '14:'
        factmode_df = df.filter(regex='^22:')
        # Ensure all data are numeric and fill NaNs with 0
        factmode_df = factmode_df.apply(pd.to_numeric, errors='coerce').fillna(0)
        # Sum the values of each filtered column
        sum_dat = factmode_df.sum()
        # Plot the bar graph
        # Define new labels with line breaks for better readability
        new_labela = [
            'Clashes with other \n tutorial sessions',
            'I was not aware when \n to attend tutorials',
            'The tutorials \n were disorganized',
            'The tutorials took \n place too early',
            'My academic workload \n prevented me',
            'Campus unrest \n or disruptions',
            'The tutorials took \n place too late',
            'Poor network \n connectivity issues',
            'Lack of basic technical \n skills to participate',
            'I did not \n have data',
            'I do not have an \n internet-enabled device',
            'Power cuts \n (loadshedding)',
            'I do not need \n additional support'
        ]


        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=new_labela, y=sum_dat.values, palette='husl', edgecolor='darkblue')
        plt.title('Count of Selections for Each Factor')
        plt.xlabel(' ')
        plt.ylabel('Count (Students)')
        plt.xticks(rotation=45, ha='right')

        # Add labels on top of bars
        for i, v in enumerate(sum_dat.values):
            plt.text(i, v + 0.1, str(v), ha='center', va='bottom')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('factor.png')

        
            # Statemments to present as a collage
        df2 = df.dropna(subset=['23: How can tutorials be structured in a way that can encourage you to attend?'])

        # Specify the column name
        column_name = '23: How can tutorials be structured in a way that can encourage you to attend?'
        # Check if the column exists and has at least one non-NaN, non-empty string
        if column_name in df2.columns and len(df2[column_name].dropna()) > 0:

            statements = df2['23: How can tutorials be structured in a way that can encourage you to attend?'].astype(str)
            # Join all the statements into a single string
            text = " ".join(statements)

            # Create the word cloud object
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)


            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.savefig('encourage.png')

            dff = df.dropna(subset=['23: How can tutorials be structured in a way that can encourage you to attend?'])


            
            comments = dff['23: How can tutorials be structured in a way that can encourage you to attend?'].astype(str)
            comments = comments.str.lower()
            # Define a translation table to remove punctuation
            remove_punctuation = str.maketrans('', '', string.punctuation)

            # Apply the translation to remove punctuation
            comments = comments.apply(lambda x: x.translate(remove_punctuation))

            # Tokenize the comments into individual words
            tokens = comments.apply(word_tokenize)

            # Flatten the list of tokens into a single list
            all_words = [word for sublist in tokens for word in sublist]

            # Join the list of words into a single string
            text = ' '.join(all_words)
   
            # Count the frequency of each word
            word_freq = Counter(all_words)

            # Convert to a dataframe for easier manipulation
            word_freq_df = pd.DataFrame.from_dict(word_freq, orient='index', columns=['Frequency'])

            #    Sort the dataframe by frequency in descending order
            word_freq_df = word_freq_df.sort_values(by='Frequency', ascending=False)



            # Get the English stopwords
            stop_words = set(stopwords.words('english'))

            # Filter out stopwords
            word_freq_df = word_freq_df[~word_freq_df.index.isin(stop_words)]

            # Plot the top N words
            top_n = 20  # Adjust as needed
            fig, ax0 = plt.subplots(figsize=(10, 6))
            bar_plot = word_freq_df.head(top_n)['Frequency'].plot(kind='bar', color='yellowgreen')

            # Set x-axis ticks to the center of the bars
            bar_plot.set_xticks(range(len(word_freq_df.head(top_n))))
            bar_plot.set_xticklabels(word_freq_df.head(top_n).index, rotation=45, ha='center')
            for bars in ax0.containers:
                ax0.bar_label(bars, fontsize = 15)
            plt.xlabel('Words')
            plt.ylabel('Frequency')
            plt.title('Top {} Words in Comments'.format(top_n))
            plt.tight_layout()
            plt.savefig('word_count1.png')

        else:

            statements = 'No Answer'
            # Join all the statements into a single string
            text = " ".join(statements)

            # Create the word cloud object
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)


            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.savefig('encourage.png')

            
            comments = 'No Answer.'
            comments = comments.lower()
            # Define a translation table to remove punctuation
            remove_punctuation = str.maketrans('', '', string.punctuation)

            # Apply the translation to remove punctuation
            #comments = comments.apply(lambda x: x.translate(remove_punctuation))
            
            comments = comments.translate(remove_punctuation)
            # Tokenize the comments into individual words
            tokens = word_tokenize(comments)

            # Flatten the list of tokens into a single list
            all_words = [word for sublist in tokens for word in sublist]

            # Join the list of words into a single string
            text = ' '.join(all_words)

            # Count the frequency of each word
            word_freq = Counter(all_words)

            # Convert to a dataframe for easier manipulation
            word_freq_df = pd.DataFrame.from_dict(word_freq, orient='index', columns=['Frequency'])

            #    Sort the dataframe by frequency in descending order
            word_freq_df = word_freq_df.sort_values(by='Frequency', ascending=False)



            # Get the English stopwords
            stop_words = set(stopwords.words('english'))

            # Filter out stopwords
            word_freq_df = word_freq_df[~word_freq_df.index.isin(stop_words)]

            # Plot the top N words
            top_n = 20  # Adjust as needed
            fig, ax0 = plt.subplots(figsize=(10, 6))
            bar_plot = word_freq_df.head(top_n)['Frequency'].plot(kind='bar', color='yellowgreen')

            # Set x-axis ticks to the center of the bars
            bar_plot.set_xticks(range(len(word_freq_df.head(top_n))))
            bar_plot.set_xticklabels(word_freq_df.head(top_n).index, rotation=45, ha='center')
            for bars in ax0.containers:
                ax0.bar_label(bars, fontsize = 15)
            plt.xlabel('Words')
            plt.ylabel('Frequency')
            plt.title('Top {} Words in Comments'.format(top_n))
            plt.tight_layout()
            plt.savefig('word_count1.png')


            

        # Statemments to present as a collage
        df3 = df.dropna(subset=['24: How do you think A_STEP tutorials can be improved?'])

        statements = df3['24: How do you think A_STEP tutorials can be improved?'].astype(str)
        # Join all the statements into a single string
        text = " ".join(statements)

        # Create the word cloud object
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)


        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('improve2.png')



        df4 = df.dropna(subset=['24: How do you think A_STEP tutorials can be improved?'])


        comments = df4['24: How do you think A_STEP tutorials can be improved?'].astype(str)
        comments = comments.str.lower()
        # Define a translation table to remove punctuation
        remove_punctuation = str.maketrans('', '', string.punctuation)

        # Apply the translation to remove punctuation
        comments = comments.apply(lambda x: x.translate(remove_punctuation))

        # Tokenize the comments into individual words
        tokens = comments.apply(word_tokenize)

        # Flatten the list of tokens into a single list
        all_words = [word for sublist in tokens for word in sublist]

        # Join the list of words into a single string
        text = ' '.join(all_words)

        # Count the frequency of each word
        word_freq = Counter(all_words)

        # Convert to a dataframe for easier manipulation
        word_freq_df = pd.DataFrame.from_dict(word_freq, orient='index', columns=['Frequency'])

        #    Sort the dataframe by frequency in descending order
        word_freq_df = word_freq_df.sort_values(by='Frequency', ascending=False)



        # Get the English stopwords
        stop_words = set(stopwords.words('english'))

        # Filter out stopwords
        word_freq_df = word_freq_df[~word_freq_df.index.isin(stop_words)]

        # Plot the top N words
        top_n = 20  # Adjust as needed
        fig, ax0 = plt.subplots(figsize=(10, 6))
        bar_plot = word_freq_df.head(top_n)['Frequency'].plot(kind='bar', color='yellowgreen')

        # Set x-axis ticks to the center of the bars
        bar_plot.set_xticks(range(len(word_freq_df.head(top_n))))
        bar_plot.set_xticklabels(word_freq_df.head(top_n).index, rotation=45, ha='center')
        for bars in ax0.containers:
            ax0.bar_label(bars, fontsize = 15)
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title('Top {} Words in Comments'.format(top_n))
        plt.tight_layout()
        plt.savefig('word_count2.png')

### Automated Paragraphs: Narratives
        # Q 16
        tutorial_organisation_paragraphs = {
                "Strongly Disagree": "Tutorial organisation was perceived as very poor. Students strongly disagreed that the sessions contributed to their understanding, performance, or preparation. This indicates serious concerns regarding planning, structure, and effectiveness of the tutorials. Immediate redesign and stronger academic alignment are required.",
    
                "Disagree": "Tutorial organisation was poor. Many students felt that the sessions did not adequately support their learning, academic performance, or assessment preparation. While some elements may have been partially effective, the overall perception was negative. Significant improvements in planning, structure, and delivery are needed.",
    
                "Neutral": "Tutorial organisation was moderate. Students expressed mixed opinions, with no strong consensus on whether the sessions improved understanding, performance, or preparedness. This suggests inconsistency across tutorials: while some sessions were well planned and supportive, others fell short. Greater standardisation and quality assurance are needed.",
    
                "Agree": "Tutorial organisation was good. Students generally agreed that the sessions improved their understanding of concepts, supported academic performance, and prepared them for assessments. Most sessions were well planned and structured, though there is still room for refinement to ensure consistency across all tutorials.",
    
                "Strongly Agree": "Tutorial organisation was excellent. Students strongly agreed that the sessions were helpful, well-planned, and well-structured. They reported improvements in academic performance, communication skills, and assessment preparedness. The tutorials were widely valued and are recommended as a best-practice model to sustain going forward."
        }
        
        # Count frequency of each outcome
        tutorial_org_outcome_counts = Counter(tutorial_organisation_outcome)

        # Convert to Series
        tutorial_org_distribution = pd.Series(tutorial_org_outcome_counts)

        # Reindex to ensure all 5 Likert labels exist
        labels = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
        tutorial_org_distribution = tutorial_org_distribution.reindex(labels, fill_value=0)

        # Convert counts to percentages
        tutorial_org_distribution = tutorial_org_distribution / tutorial_org_distribution.sum() * 100
        print(tutorial_org_distribution)

        # Collapse the likert-scale distribution into a single variable
        tutorial_org_final_outcome = collapse_outcome(tutorial_org_distribution)

        # map the final outcome to the paragraph to be written in the report
        tutorial_org_final_paragraph = tutorial_organisation_paragraphs[tutorial_org_final_outcome]

        # Q 17

        tutorial_quality_paragraphs = {
            "Strongly Disagree": "Overall tutorial quality was very poor. Students strongly disagreed with the effectiveness of the tutorials, "
                         "indicating serious concerns with tutor preparedness, support, and facilitation. Immediate intervention and "
                         "comprehensive tutor development are urgently required.",
            "Disagree": "Tutorial quality was poor. Many students felt that the tutorials did not adequately support their learning needs. "
                        "While some aspects may have been partially effective, the overall perception was negative, highlighting the need "
                        "for targeted improvements in tutor performance and facilitation.",
            "Neutral": "Tutorial quality was moderate. Students expressed mixed opinions, with no clear consensus on strengths or weaknesses. "
                       "This suggests inconsistency in tutorial delivery, where some sessions may have been effective while others fell short. "
                       "Focused efforts are needed to ensure greater consistency and reliability across all tutorials.",
            "Agree": "Overall tutorial quality was good. Students generally agreed that the tutorials were effective, supportive, and beneficial "
                     "to their academic progress. While there is still room for refinement, the majority of students experienced positive outcomes "
                     "from the tutorial program.",
            "Strongly Agree": "Tutorial quality was excellent. Students strongly agreed that the tutorials met their academic needs, with tutors "
                      "providing effective support, inclusivity, and encouragement. The program demonstrated a high standard of facilitation, "
                      "and maintaining this level of quality should be a priority."
        }

        # Count frequency of each outcome
        tutorial_qual_outcome_counts = Counter(tutorial_quality_outcome)

        # Convert to Series
        tutorial_qual_distribution = pd.Series(tutorial_qual_outcome_counts)

        # Reindex to ensure all 5 Likert labels exist
        labels = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
        tutorial_qual_distribution = tutorial_qual_distribution.reindex(labels, fill_value=0)

        # Convert counts to percentages
        tutorial_qual_distribution = tutorial_qual_distribution / tutorial_qual_distribution.sum() * 100
        print(tutorial_qual_distribution)

        # Collapse the likert-scale distribution into a single variable
        tutorial_qual_final_outcome = collapse_outcome(tutorial_qual_distribution)

        # map the final outcome to the paragraph to be written in the report
        tutorial_final_paragraph = tutorial_quality_paragraphs[tutorial_qual_final_outcome]




else:
    st.write(' ')
        
if f_name:
    if Eval:
        pdf = FPDF()
        pdf.page_no()
        # Add a page
        pdf.add_page()

        # set style and size of font
        # that you want in the pdf
        pdf.set_font("Times", 'B', size = 13)
        pdf.image('ctl.png', x = 80, y = 5, w = 50, h = 50, type = 'PNG')
        pdf.cell(0, 5, txt = '', ln =1)
        pdf.cell(0, 5, txt = '', ln =1)
        pdf.cell(0, 5, txt = '', ln =1)
        pdf.cell(0, 5, txt = '', ln =1)
        pdf.cell(0, 5, txt = '', ln =2)
        pdf.cell(0, 5, txt = '', ln =4)
        pdf.cell(0, 5, txt = '', ln =5)
        pdf.cell(0, 5, txt = '', ln =6)
        pdf.cell(0, 5, txt = '', ln =7)
        pdf.cell(0, 5, txt = '', ln =7)
        pdf.cell(0, 5, txt = 'Evaluation Report: 2241', align = 'C', ln=8)
        pdf.cell(0, 5, txt = '', ln =9)
        pdf.cell(0, 5, txt = 'A_STEP: A.T&T.E.', align = 'C', ln=10)
        pdf.cell(0, 5, txt = '', ln =11)
        today = date.today()
        print('Today\'s date:', today)
        pdf.cell(0, 5, txt = str(today), ln =12, align = 'C')
        pdf.cell(0, 5, txt = ' ', ln =13, align = 'C') 
        pdf.ln(0.25)
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '1. Executive Summary.', ln=14, align='L')
        pdf.cell(0, 5, txt = '', ln =15, align = 'C')
        pdf.ln(0.25)
        pdf.set_font('Arial','',10.0)
        s1 = ('The majority of A_STEP students that participated in the evaluation of the module '+str(f_name[0])+', expressed satisfaction with \
the performance of A_STEP, simultenously highlighting challenges and improvements that could be implemented in future, as well as a general \
concensus that A_STEP is achieving its outcomes.').format()
        pdf.multi_cell(0, 5, txt = str(s1), align = 'L', fill = False)
        pdf.cell(0, 5, txt = '', ln =16, align = 'C')
        pdf.ln(0.25)
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '2. Introduction.', ln =17, align = 'L')
        pdf.cell(0, 5, txt = '', ln =18, align = 'C')
        pdf.ln(0.25)
        s2 = ('Frequent and consistent programme evaluation is a valuable tool for A_STEP, due to its role as a student academic support service for all the UFS academic faculties \
across the Bloemfontein and Qwa-qwa campuses. This is particularly imperative when seeking to strengthen and improve the quality and academic outcomes of the \
programme, as well as the academic impact of the students it is serving. For these reasons, the A_STEP programme evaluation provides basic questions about its effectiveness, and the collected data is \
used for reporting and to improve A_STEP services.').format()
        pdf.set_font('Arial','',10.0)
        pdf.multi_cell(0, 5, txt = str(s2), align = 'L', fill = False)
        pdf.cell(0, 5, txt = '', ln =16, align = 'C')
        pdf.ln(0.25)
        s3 = ('The A_STEP evaluation model is comprised of questions aimed at finding out if A_STEP attendees are satisfied with the services of the programme, investigating \
and analysing student satisfaction with the A_STEP content, teaching, learning and more. Additionally, the model seeks challanges faced by students, as well as future recommendations, \
which are used to improve A_STEP sevices.').format()
        pdf.set_font('Arial','',10.0)
        pdf.multi_cell(0, 5, txt = str(s3), align = 'L', fill = False)
        pdf.cell(0, 5, txt = '', ln =16, align = 'C')
        pdf.ln(0.25)
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3. A_STEP Evaluation of '+str(f_name[0])+'. ', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =15, align = 'C')
        pdf.ln(0.25)
        pdf.set_font('Arial','',10.0)
        sa = ('The following section presents the findings from the evaluation analysis of the A_STEP module '+str(f_name[0])+', during the first term of the 2024 calendar year (2241). \
The data employed in this analysis was collected from A_STEP students of the module through QuestBack Essential survey forms, comprised of nearly a dozen evaluation questions. \
The aim of this report is to investigate if A_STEP attendees are satisfied with the services of the programme during the 2241 term, in relation with the content provided, tutor performance, \
teaching, learning and more. Additionally, we studied responses to identify attendance challanges, A_STEP marketability, as well as recommendations to be implemented in the future.').format()
        pdf.multi_cell(0, 5, txt = str(sa), align = 'L')
        pdf.cell(0, 5, txt = '', ln =15, align = 'C')
        pdf.ln(0.25)
        if ProgN >= 2:
            s5 = ('The module '+str(f_name[0])+' was evaluated by '+str(Tutor_cnt[0])+' A_STEP students during the first term of 2024. The participants were enrolled on the \
'+str(camp[0][0])+', in the '+str(Prog[0][0])+' and '+str(Prog[0][1])+' programmes. They speak '+str(Lang[0])+' languages, and came in '+str(gend[0])+' various genders.')
        else:
            s5 = ('The module '+str(f_name[0])+' was evaluated by '+str(Tutor_cnt[0])+' A_STEP students during the first term of 2024. The participants were enrolled on the \
'+str(camp[0][0])+', in the '+str(Prog[0][0])+' programme. They speak '+str(Lang[0])+' languages, and came in '+str(gend[0])+' various genders.')
        pdf.multi_cell(0, 5, txt = str(s5), align = 'L')
        pdf.cell(0, 5, txt = '', ln =15, align = 'C')
        pdf.ln(0.25)
        pdf.add_page()
        pdf.set_font('Arial','B',12.0)
        pdf.cell(0, 5, txt = '3.1. Evaluation Questions', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =15, align = 'C')
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.1. Gender and Languages in '+str(f_name[0])+' tutorial session(s) this semester.', ln =14, align = 'L')
        #pdf.ln(0.25)
        s6 = 'marksVstd.png'
        pdf.image(str(s6), x = 50, y = 30, w = 100, h = 70, type = 'PNG')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.2. What is your Home Language?', ln =14, align = 'L')
        pdf.ln(0.25)
        s7 = 'lang.png'
        pdf.image(str(s7), x = 50, y = 115, w = 100, h = 70, type = 'PNG')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '3.1.3. Which programme are you enrolled in?', ln =14, align = 'L')
        pdf.ln(0.25)
        s8 = 'prog.png'
        pdf.image(str(s8), x = 50, y = 200, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '3.1.4.  What academic year are you in for the qualification you are currently enrolled in?', ln =14, align = 'L')
        pdf.ln(0.25)
        s10 = 'enroll.png'
        pdf.image(str(s10), x = 50, y = 20, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '3.1.6. How did you hear about A_STEP tutorials for this module?', ln =14, align = 'L')
        pdf.ln(0.25)
        s11 = 'market.png'
        pdf.image(str(s11), x = 50, y = 105, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '3.1.7. What motivated you to attend tutorials? (Select all options that apply)', ln =14, align = 'L')
        pdf.ln(0.25)
        s12 = 'motiv.png'
        pdf.image(str(s12), x = 50, y = 185, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        txt = '3.1.8. Are you familiar with the concept of multilingualism or the use of multiple languages (in addition to \n English) in tutorial sessions?'
        pdf.multi_cell(0, 5, txt = str(txt), align = 'L', fill = False)
        s13 = 'mutiling.png'
        pdf.image(str(s13), x = 50, y = 25, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.9. The following questions are on the perception of the tutorial sessions:', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.set_font('Arial','',10.0)
        pdf.multi_cell(0, 5, txt = str(tutorial_org_final_paragraph), align = 'L', fill = False) 
        # Corresponding questions
        qual_questions = [
            "Q1: Tutorial sessions helped me understand the concepts better",
            "Q2: I found the tutorial sessions helpful to my learning",
            "Q3: The tutorial sessions helped me improve my academic performance",
            "Q4: I found the tutorial sessions well-planned",
            "Q5: I found the tutorial sessions well-structured",
            "Q6: Tutorial sessions helped me feel prepared for assessments",
            "Q7: The tutorial sessions helped me improve my communication skills",
            "Q8: I would recommend tutorials to other students"
        ]
        # Title
        pdf.cell(200, 10, "Tutorial Quality Distribution", ln=True, align="C")
        # Table headers
        pdf.set_font("Arial", "B", 12)
        pdf.cell(120, 10, "Questions", border=1, align="C")
        pdf.cell(70, 10, "Weighted Outcomes", border=1, align="C")
        pdf.ln()

        pdf.set_font("Arial", size=10)
        for q, outcome in zip(qual_questions, tutorial_organisation_outcome):
            pdf.cell(120, 10, q, border=1, align="C")
            pdf.cell(70, 10, outcome, border=1, align="C")
            pdf.ln()

        pdf.add_page()
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.9.1. Tutorial sessions helped me understand the concepts better?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s14 = 'concepts.png'
        pdf.image(str(s14), x = 50, y = 20, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.9.2. I found the tutorial sessions helpful to my learning?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s15 = 'tuthelp.png'
        pdf.image(str(s15), x = 50, y = 90, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')         
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '3.1.9.3. The tutorial sessions help me improve my academic performance?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s16 = 'improve.png'
        pdf.image(str(s16), x = 50, y = 130, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.add_page()
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.9.4. I found the tutorial sessions well-planned?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s17 = 'plan.png'
        pdf.image(str(s17), x = 50, y = 105, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')       
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.9.5. I found the tutorial sessions well structured?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s18 = 'structure.png'
        pdf.image(str(s18), x = 50, y = 180, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '3.1.9.5. Tutorial sessions helped me feel prepared for assessments?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s19 = 'prep.png'
        pdf.image(str(s19), x = 50, y = 30, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')       
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.9.6. The tutorial sessions helped me improve my communication skills?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s20 = 'comm.png'
        pdf.image(str(s20), x = 50, y = 105, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')       
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.9.7. I would recommend tutorials to other students?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s21 = 'recc.png'
        pdf.image(str(s21), x = 50, y = 180, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)      
        pdf.add_page()
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.10. The following outcomes are on the perception of the tutor:', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.set_font('Arial','',10.0)
        pdf.multi_cell(0, 5, txt = str(tutorial_final_paragraph), align = 'L', fill = False)
        # Corresponding questions
        questions = [
            "Q1: My tutor was on time",
            "Q2: My tutor helped me with difficulties that I encountered in the module",
            "Q3: My tutor recognized that students are different",
            "Q4: My tutor made an effort to help me",
            "Q5: My tutor gave me confidence to complete my assessment",
            "Q6: My tutor was interested in my academic progress",
            "Q7: My tutor allowed me to use my ome language to express myself"
        ]
        # Title
        pdf.cell(200, 10, "Tutorial Quality Distribution", ln=True, align="C")
        pdf.ln(0.25)

        # Table headers
        pdf.set_font("Arial", "B", 12)
        pdf.cell(120, 10, "Questions", border=1, align="C")
        pdf.cell(70, 10, "Weighted Outcomes", border=1, align="C")
        pdf.ln()

        pdf.set_font("Arial", size=10)
        for q, outcome in zip(questions, tutorial_quality_outcome):
            pdf.cell(120, 10, q, border=1, align="C")
            pdf.cell(70, 10, outcome, border=1, align="C")
            pdf.ln()

        
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '3.1.10.1. My tutor was on time?', ln =14, align = 'L')                
        pdf.ln(0.25)
        s22 = 'punc.png'
        pdf.image(str(s22), x = 50, y = 140, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')       
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.10.2. My tutor helped me with difficulties I encountered in the module?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s23 = 'diffc.png'
        pdf.image(str(s23), x = 50, y = 220, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
      # pdf.cell(0, 5, txt = '', ln =20, align = 'C')
       # pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
      #  pdf.cell(0, 5, txt = '', ln =20, align = 'C')
       # pdf.cell(0, 5, txt = '', ln =20, align = 'C')
      #  pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
       # pdf.cell(0, 5, txt = '', ln =20, align = 'C')
       # pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
       #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)
        pdf.add_page()
        pdf.cell(0, 5, txt = '3.1.10.3. My tutor recognized that students are different?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s24 = 'diffr.png'
        pdf.image(str(s24), x = 50, y = 20, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.10.4. My tutor made an effort to help me', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C') 
        s25 = 'efft.png'
        pdf.image(str(s25), x = 50, y = 90, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.10.5. My tutor gave me confidence to complete my assessments?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s26 = 'conf.png'
        pdf.image(str(s26), x = 50, y = 170, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.add_page()
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.10.6. My tutor was interested in my academic progress?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s27 = 'intr.png'
        pdf.image(str(s27), x = 50, y = 20, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.10.7. My tutor allowed me to use my home language to express myself?', ln =14, align = 'L')        
        pdf.ln(0.25)
        s28 = 'hlangu.png'
        pdf.image(str(s28), x = 50, y = 90, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.11. Select the tutorial mode used.', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C') 
        s29 = 'mode.png'
        s291 = 'mode2.png'
        s292 = 'mode3.png'        
        pdf.image(str(s29), x = 20, y = 20, w = 60, h = 60, type = 'PNG')
        pdf.image(str(s291), x = 80, y = 20, w = 60, h = 60, type = 'PNG')
        pdf.image(str(s292), x = 140, y = 20, w = 60, h = 60, type = 'PNG')        
        pdf.ln(0.25)        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.12. The following questions are on the perception of the tutorial venue (Face-to-face sessions):', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C') 
        pdf.cell(0, 5, txt = '3.1.12.1. The venue where the tutorials took place was conducive to learning?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')         
        pdf.ln(0.25)
        s30 = 'conducive.png'
        pdf.image(str(s30), x = 50, y = 115, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.12.2. The venue was spacious enough to accommodate the student(s)?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s31 = 'spacious.png'
        pdf.image(str(s31), x = 50, y = 190, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.12.3. The venue made you comfortable to interact with your tutors?', ln =14, align = 'L')
        s32 = 'inter.png'
        pdf.image(str(s32), x = 50, y = 20, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)        
        pdf.cell(0, 5, txt = '3.1.12.4. The venue made you comfortable to interact with your classmates?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s33 = 'interct.png'
        pdf.image(str(s33), x = 50, y = 90, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.12.5. The venue had proper lighting?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s34 = 'light.png'
        pdf.image(str(s34), x = 50, y = 170, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.12.6. The venue had proper ventilation?', ln =14, align = 'L')
        s35 = 'vent.png'
        pdf.image(str(s35), x = 50, y = 20, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.13. The following questions are on the perception of the tutorial hybrid (face-to-face & online sessions):', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '3.1.13.1. The venue where the tutorials took place was conducive to learning?', ln =14, align = 'L')
        s36 = 'conducive1.png'
        pdf.image(str(s36), x = 50, y = 100, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.13.2. The venue was spacious enough to accommodate the student(s)?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s37 = 'spacious1.png'
        pdf.image(str(s37), x = 50, y = 175, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.13.3. The venue made you comfortable to interact with your tutors?', ln =14, align = 'L')
        s38 = 'inter1.png'
        pdf.image(str(s38), x = 50, y = 20, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25) 
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)        
        pdf.cell(0, 5, txt = '3.1.13.4. The venue made you comfortable to interact with your classmates?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s39 = 'interct1.png'
        pdf.image(str(s39), x = 50, y = 90, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.13.5. The venue had proper lighting?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s40 = 'light1.png'
        pdf.image(str(s40), x = 50, y = 170, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.13.6. The venue had proper ventilation?', ln =14, align = 'L')
        s41 = 'vent1.png'
        pdf.image(str(s41), x = 50, y = 20, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.cell(0, 5, txt = '3.1.13.7. The platform where the tutorials took place was conducive to learning?', ln =14, align = 'L')
        s42 = 'conducive2.png'
        pdf.image(str(s42), x = 50, y = 90, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)        
        pdf.cell(0, 5, txt = '3.1.13.8. The platform made you comfortable to interact with your tutors?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s43 = 'inter2.png'
        pdf.image(str(s43), x = 50, y = 160, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.13.9. The platform was easy to navigate?', ln =14, align = 'L')
        s44 = 'navi.png'
        pdf.image(str(s44), x = 50, y = 20, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)        
        pdf.cell(0, 5, txt = '3.1.14. The following questions are on the perception of the tutorial Platform (online sessions):', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '3.1.14.1. The platform where the tutorials took place was conducive to learning?', ln =14, align = 'L')
        s45 = 'conducive3.png'
        pdf.image(str(s45), x = 50, y = 100, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)        
        pdf.cell(0, 5, txt = '3.1.14.2. The platform made you comfortable to interact with the tutor?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s46 = 'inter3.png'
        pdf.image(str(s46), x = 50, y = 180, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()               
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.14.3. The platform made you comfortable to interact with the classmates?', ln =14, align = 'L')
        s47 = 'interct3.png'
        pdf.image(str(s47), x = 50, y = 20, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)        
        pdf.cell(0, 5, txt = '3.1.14.4. The platform was easy to navigate?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s48 = 'navi1.png'
        pdf.image(str(s48), x = 50, y = 95, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')               
        pdf.set_font('Arial','B',10.0)        
        pdf.cell(0, 5, txt = '3.1.15. Factors limiting your tutorial attendance?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s49 = 'factor.png'
        pdf.image(str(s49), x = 50, y = 170, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()                             
        pdf.set_font('Arial','B',10.0)        
        pdf.cell(0, 5, txt = '3.1.16. How can tutorials be structured in a way that can encourage you to attend?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s50 = 'encourage.png'
        pdf.image(str(s50), x = 35, y = 20, w = 130, h = 70, type = 'PNG')
        pdf.ln(0.25)
        s51 = 'word_count1.png'
        pdf.image(str(s51), x = 50, y = 100, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C') 
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')         
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')        
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')   
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')             
        pdf.set_font('Arial','B',10.0)        
        pdf.cell(0, 5, txt = '3.1.15. How do you think A_STEP tutorials can be improved?', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s52 = 'improve2.png'
        pdf.image(str(s52), x = 35, y = 190, w = 130, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()                             
        s53 = 'word_count2.png'
        pdf.image(str(s53), x = 50, y = 20, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)


        
        pdf.output('A_STEP_IR_2019_2022.pdf')
        with st.spinner('Wait for it...'):
                    time.sleep(3)
        #with col1:
        progress_bar = st.progress(0)
        for perc_completed in range(100):
            time.sleep(0.001)
        progress_bar.progress(perc_completed+1)
        st.success(':orange[Module '+str(f_name[0])+' successfully Evaluated 👏🏼 👏🏾 👏🏿]', icon="✅")
        st.write(':blue[Survey : '+str(Tutor_cnt[0])+' Participants 👥]')
        with open('A_STEP_IR_2019_2022.pdf', "rb") as file:
                btn = st.download_button(
                label=":red[Download PDF Report]",
                data=file,
                file_name='A_STEP_IR_2019_2022.pdf',
                mime="file/pdf"
                  )  
                st.success('Report Ready for Download', icon="✅")

   
else:
    st.sidebar.info(':red[ 🚩 Upload Files]', icon="ℹ️") 

st.sidebar.markdown("""
<style>
.sidebar-box {
    padding: 15px;
    margin: 10px 0;
    border-radius: 12px;
    background: linear-gradient(135deg, #F9FAFC, #F9FAFC);
    border: 3px solid #1C398E;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.sidebar-box h1 {
    text-align: center;
    font-size: 20px;
    color: #090257;
    margin-bottom: 12px;
}
.sidebar-box ul {
    list-style-type: none;
    padding-left: 0;
}
.sidebar-box li {
    font-size: 15px;
    margin: 8px 0;
    padding: 6px 10px;
    border-radius: 8px;
    background-color: #f3f4f6;
    transition: all 0.3s ease;
}
.sidebar-box li:hover {
    background-color: #e0e7ff;
    transform: translateX(4px);
}
.sidebar-box li span {
    color: #ff6b35;
    font-weight: 600;
}
</style>

<div class="sidebar-box">
    <h1>📑 Instructions</h1>
    <p style="color:#374151; font-size:14px; text-align:center;">
        Upload An <b>.xlsx</b> File
    </p>
    <ul>
        <li><span>Press Generate Report ⏳</span></li>
        <li><span>Download PDF Report ✅</span></li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.sidebar.info(':red[ 🚩 Developer:] Tekano Mbonani', icon="ℹ️") 
