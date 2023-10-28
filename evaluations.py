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
st.set_page_config(
    page_title="Evaluations",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.sidebar.markdown("![Alt Text](https://i.postimg.cc/gJzPdRYd/logio.png)")

eval_files = st.sidebar.file_uploader(':blue[**Upload File**:👇]',
                                     type=['xlsx', 'csv'],
                                     accept_multiple_files=True)
st.markdown("<h3 style='text-align: center; color: darkred;'>A-STEP Attended Modules Performance Evaluation 🧑🏼‍🎓 👨🏽‍🎓</h3>", unsafe_allow_html=True)

col1, col2 = st.columns([0.20, 0.80], gap='small')
with col1:
    st.write(' ')
    Eval = st.button(':red[Generate Report _ 🚀_ ]')
with col2:
    st.markdown("![Alt Text](https://i.postimg.cc/1tMyy904/eval-logo.png)")


# Your expander element
with st.expander(":blue[Read More ⤵️]"):
    st.write('Welcome to the Evaluation of A-STEP Attended Modules. Programme evaluation is a valuable tool for the coninued success of\
         A-STEP, positioned in the UFS academic faculties as a student academic support service.\
         This is particularly imperative when seeking to strengthen the quality of the programme and improve academic outcomes\
         for the programme, and the students it is serving. Therefore, programme evaluation provides basic questions about a programmes’s effectiveness,\
         and evaluation data can be used to improve programme services. At the core of the evaluation in the SLS programme is to give students a platform\
         to reflect on the experiences on the online tutorials they have attended, but it also allows those who did not attend a space to provide their views.\
         The practice is helping the programme to address common concerns that students might have regarding the service they obtain from the programme,\
         how it can benefit by improving quality assurance, monitoring, and optimizing student-learning opportunities.')
      

if eval_files:
    st.sidebar.success('File Uploaded', icon="✅")
else:
    st.write(' ')
if eval_files is not None:
    n_file = []
    f_name = []
    part_c = []
    Tutor_cnt = []
    N_com = []
    Pstv_com = []
    selected_tut = {}
    pop_q = {}
    factors = {}
    lang = {}
    Grade = {}
    Cont1 = {}
    Relate = {}
    Prep = {}
    Feedb = {}
    Mate = {}
    Tutprep = {}
    Audio = {}
    Enth = {}
    Treat = {}
    Supp = {}
    Van = {}
    for file in eval_files:
        df = pd.read_excel(file)  # You may use pd.read_csv(file) for CSV files
        fname = file.name[0:8]
        second_column = len(df.iloc[:, 1])
        selected_tutors = [col for col in df.columns if col.startswith('2:') and (df[col] == 1).any()]

        # Count the number of such columns and add to the dictionary
        tutor_cnts = len(selected_tutors)
        # Identify columns that start with '2' and have '1' in their cells
        for col in df.columns:
            if col.startswith('2:') and (df[col] == 1).any():
                tutor_name = col.replace('2:', '').strip()
                tutor_count = (df[col] == 1).sum()
                # Update the dictionary with the tutor name and count
                selected_tut[tutor_name] = selected_tut.get(tutor_name, 0) + tutor_count
        # Identify columns that start with '4' and have '1' in their cells
        for col in df.columns:
            if col.startswith('4:') and (df[col] == 1).any():
                mark_q = col.replace('4:', '').strip()
                pop_count = (df[col] == 1).sum()
                # Update the dictionary with the tutor name and count
                pop_q[mark_q] = pop_q.get(mark_q, 0) + pop_count
        # Identify columns that start with '5' and have '1' in their cells
        for col in df.columns:
            if col.startswith('5:') and (df[col] == 1).any():
                factor_q = col.replace('5:', '').strip()
                factor_count = (df[col] == 1).sum()
                # Update the dictionary with the tutor name and count
                factors[factor_q] = factors.get(factor_q, 0) + factor_count
        # Identify columns that start with '6' 
        for col in df.columns:
            if col.startswith('6:'):
                encourage = df[col].astype(str).dropna()
                n_com = len(encourage)
                # Positive Evaluations
                log1_indx = encourage.str.lower().str.contains('clarity|understanding|love|improve|help|tests|exam|prepare|helpful|achieve|learn|helpful|assist|pass|grades|understand|assistance|explanation|knowledge|clarification|content|information|engage|failing|tutor|clear|feedback')
                npv = encourage[log1_indx]
                psv_com = len(npv)
                N_com.append(n_com)
                Pstv_com.append(psv_com)
         # Identify columns that start with '7' and have '1' in their cells
        for col in df.columns:
            if col.startswith('7:') and (df[col] == 1).any():
                lang_q = col.replace('7:', '').strip()
                lang_count = (df[col] == 1).sum()
                # Update the dictionary with the tutor name and count
                lang[lang_q] = lang.get(lang_q, 0) + lang_count
         # Identify columns that start with '8' and have '1' in their cells
        for col in df.columns:
            if col.startswith('8:') and (df[col] == 1).any():
                grade_q = col.replace('8:', '').strip()
                grade_count = (df[col] == 1).sum()
                # Update the dictionary with the tutor name and count
                Grade[grade_q] = Grade.get(grade_q, 0) + grade_count                  
         # Identify columns that start with '9.1' 
        for col in df.columns:
            if col.startswith('9.1:'):
                # Get the unique values in the column
                unique_values = df[col].unique()
                # Loop through the unique values
                for value in unique_values:
                    value_str = str(value)
                    # Count the occurrences of each value in the column
                    ncount = (df[col] == value).sum()
        
                    # Update the dictionary with the count
                    Cont1[value_str] = Cont1.get(value_str, 0) + ncount
         # Identify columns that start with '9.2' 
        for col in df.columns:
            if col.startswith('9.2:'):
                # Get the unique values in the column
                uni_values = df[col].unique()
                # Loop through the unique values
                for relate in uni_values:
                    relate_str = str(relate)
                    # Count the occurrences of each value in the column
                    relate_count = (df[col] == relate).sum()
        
                    # Update the dictionary with the count
                    Relate[relate_str] = Relate.get(relate_str, 0) + relate_count
         # Identify columns that start with '9.3' 
        for col in df.columns:
            if col.startswith('9.3:'):
                # Get the unique values in the column
                prep_values = df[col].unique()
                # Loop through the unique values
                for prep in prep_values:
                    prep_str = str(prep)
                    # Count the occurrences of each value in the column
                    prep_count = (df[col] == prep).sum()
        
                    # Update the dictionary with the count
                    Prep[prep_str] = Prep.get(prep_str, 0) + prep_count
         # Identify columns that start with '9.4' 
        for col in df.columns:
            if col.startswith('9.4:'):
                # Get the unique values in the column
                feedb_values = df[col].unique()
                # Loop through the unique values
                for feedb in feedb_values:
                    feedb_str = str(feedb)
                    # Count the occurrences of each value in the column
                    feedb_count = (df[col] == feedb).sum()
        
                    # Update the dictionary with the count
                    Feedb[feedb_str] = Feedb.get(feedb_str, 0) + feedb_count
         # Identify columns that start with '9.5' 
        for col in df.columns:
            if col.startswith('9.5:'):
                # Get the unique values in the column
                mate_values = df[col].unique()
                # Loop through the unique values
                for mate in mate_values:
                    mate_str = str(mate)
                    # Count the occurrences of each value in the column
                    mate_count = (df[col] == mate).sum()
        
                    # Update the dictionary with the count
                    Mate[mate_str] = Mate.get(mate_str, 0) + mate_count
         # Identify columns that start with '10.1' 
        for col in df.columns:
            if col.startswith('10.1:'):
                # Get the unique values in the column
                tutprep_values = df[col].unique()
                # Loop through the unique values
                for tutprep in tutprep_values:
                    tutprep_str = str(tutprep)
                    # Count the occurrences of each value in the column
                    tutprep_count = (df[col] == tutprep).sum()
        
                    # Update the dictionary with the count
                    Tutprep[tutprep_str] = Tutprep.get(tutprep_str, 0) + tutprep_count
         # Identify columns that start with '10.2' 
        for col in df.columns:
            if col.startswith('10.2:'):
                # Get the unique values in the column
                aud_values = df[col].unique()
                # Loop through the unique values
                for aud in aud_values:
                    aud_str = str(aud)
                    # Count the occurrences of each value in the column
                    aud_count = (df[col] == aud).sum()
        
                    # Update the dictionary with the count
                    Audio[aud_str] = Audio.get(aud_str, 0) + aud_count
         # Identify columns that start with '10.3' 
        for col in df.columns:
            if col.startswith('10.3:'):
                # Get the unique values in the column
                enth_values = df[col].unique()
                # Loop through the unique values
                for enth in enth_values:
                    enth_str = str(enth)
                    # Count the occurrences of each value in the column
                    enth_count = (df[col] == enth).sum()
        
                    # Update the dictionary with the count
                    Enth[enth_str] = Enth.get(enth_str, 0) + enth_count
         # Identify columns that start with '10.4' 
        for col in df.columns:
            if col.startswith('10.4:'):
                # Get the unique values in the column
                treat_values = df[col].unique()
                # Loop through the unique values
                for treat in treat_values:
                    treat_str = str(treat)
                    # Count the occurrences of each value in the column
                    treat_count = (df[col] == treat).sum()
        
                    # Update the dictionary with the count
                    Treat[treat_str] = Treat.get(treat_str, 0) + treat_count
         # Identify columns that start with '10.5' 
        for col in df.columns:
            if col.startswith('10.5:'):
                # Get the unique values in the column
                supp_values = df[col].unique()
                # Loop through the unique values
                for supp in supp_values:
                    supp_str = str(supp)
                    # Count the occurrences of each value in the column
                    supp_count = (df[col] == supp).sum()
        
                    # Update the dictionary with the count
                    Supp[supp_str] = Supp.get(supp_str, 0) + supp_count
         # Identify columns that start with '10.6' 
        for col in df.columns:
            if col.startswith('10.6:'):
                # Get the unique values in the column
                van_values = df[col].unique()
                # Loop through the unique values
                for van in van_values:
                    van_str = str(van)
                    # Count the occurrences of each value in the column
                    van_count = (df[col] == van).sum()
        
                    # Update the dictionary with the count
                    Van[van_str] = Van.get(van_str, 0) + van_count
                
        Tutor_cnt.append(tutor_cnts)
        part_c.append(second_column)
        n_file.append(df)
        f_name.append(fname)
        st.write(':blue[Uploaded File Preview:👇]')
        st.write(df.head())
        #Eval = st.button(':red[Evaluate Module!!]')
    # Extract tutor names and counts
    tutor_names = list(selected_tut.keys())
    tutor_counts = list(selected_tut.values())
    # Extract market questions and counts
    market_q = list(pop_q.keys())
    mq_counts = list(pop_q.values())
    # Extract factor questions and counts
    fact_q = list(factors.keys())
    fact_counts = list(factors.values())
    # Extract language questions and counts
    langua_q = list(lang.keys())
    langua_counts = list(lang.values())
    # Extract language questions and counts
    grad_q = list(Grade.keys())
    grad_counts = list(Grade.values())
    # Extract content questions and counts
    Cnt1_q = list(Cont1.keys())
    Cnt1_counts = list(Cont1.values())
    # Extract content questions and counts
    Cnt2_q = list(Relate.keys())
    Cnt2_counts = list(Relate.values())
    # Extract content questions and counts
    Cnt3_q = list(Prep.keys())
    Cnt3_counts = list(Prep.values())
    # Extract content questions and counts
    Cnt4_q = list(Feedb.keys())
    Cnt4_counts = list(Feedb.values())
    # Extract content questions and counts
    Cnt5_q = list(Mate.keys())
    Cnt5_counts = list(Mate.values())
    # Extract teaching questions and counts
    Cnt6_q = list(Tutprep.keys())
    Cnt6_counts = list(Tutprep.values())
    # Extract teaching questions and counts
    Cnt7_q = list(Audio.keys())
    Cnt7_counts = list(Audio.values())
    # Extract teaching questions and counts
    Cnt8_q = list(Enth.keys())
    Cnt8_counts = list(Enth.values())
    # Extract teaching questions and counts
    Cnt9_q = list(Treat.keys())
    Cnt9_counts = list(Treat.values())
    # Extract teaching questions and counts
    Cnt10_q = list(Supp.keys())
    Cnt10_counts = list(Supp.values())
    # Extract teaching questions and counts
    Cnt11_q = list(Van.keys())
    Cnt11_counts = list(Van.values())
    
    if f_name:
        # Create a bar graph for q 3.1
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(tutor_names, tutor_counts, color='darkred')
        ax.set_xlabel('A-STEP Students')
        ax.set_ylabel('Tutor Names')
        ax.set_title('Please choose the name of the tutor that assisted you' +'\n'+ 'in your '+str(f_name[0])+' tutorial session(s) this semester.', fontsize = 15)

        # Add labels to the bars

        for bar in bars:
            width = bar.get_width()
            ax.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=15)

        plt.tight_layout()
        plt.savefig('tutors_plot.png')
        plt.close()
    
        # Create a bar graph for q 3.2
        fig, ax0 = plt.subplots(figsize=(10, 6))
        bars = ax0.barh(market_q, mq_counts, color='darkred')
        ax0.set_xlabel('A-STEP Students')
        ax0.set_ylabel('Where did you find out about A_STEP tutorials?')
        ax0.set_title('Where did you find out about A_STEP tutorials?', fontsize = 15)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax0.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=15)

        plt.tight_layout()
        plt.savefig('market_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.3
        fig, ax1 = plt.subplots(figsize=(10, 6))
        bars = ax1.barh(fact_q, fact_counts, color='darkred')
        ax1.set_xlabel('A-STEP Students')
        ax1.set_ylabel('What factors limit you from attending tutorials?')
        ax1.set_title('What factors limit you from attending tutorials?', fontsize = 15)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax1.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=15)

        plt.tight_layout()
        plt.savefig('factor_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.5
        fig, ax2 = plt.subplots(figsize=(10, 6))
        bars = ax2.barh(langua_q, langua_counts, color='darkred')
        ax2.set_xlabel('A-STEP Students')
        ax2.set_ylabel('What is the language of instruction used in the tutorial?')
        ax2.set_title('What is the language of instruction used in the tutorial?', fontsize = 15)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax2.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=15)

        plt.tight_layout()
        plt.savefig('lang_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.6
        fig, ax3 = plt.subplots(figsize=(10, 6))
        bars = ax3.barh(grad_q, grad_counts, color='darkred')
        ax3.set_xlabel('A-STEP Students')
        ax3.set_ylabel('What is your current academic year?')
        ax3.set_title('What is your current academic year?', fontsize = 15)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax3.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=15)

        plt.tight_layout()
        plt.savefig('grade_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.7
        fig, ax4 = plt.subplots(figsize=(6, 3))
        bars = ax4.barh(Cnt1_q, Cnt1_counts, color='darkred')
        ax4.set_xlabel('A-STEP Students')
        #ax4.set_ylabel('I understood the content of the tutorial')
        ax4.set_title('I understood the content of the tutorial', fontsize = 10)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax4.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('cont1_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.7
        fig, ax5 = plt.subplots(figsize=(6, 3))
        bars = ax5.barh(Cnt2_q, Cnt2_counts, color='darkred')
        ax5.set_xlabel('A-STEP Students')
        #ax5.set_ylabel('The content of the tutorial session(s) is related to the module content')
        ax5.set_title('The content of the tutorial session(s) is related to the module content', fontsize = 9)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax5.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('cont2_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.7
        fig, ax6 = plt.subplots(figsize=(6, 3))
        bars = ax6.barh(Cnt3_q, Cnt3_counts, color='darkred')
        ax6.set_xlabel('A-STEP Students')
        #ax5.set_ylabel('The content of the tutorial session(s) is related to the module content')
        ax6.set_title('The content of the tutorial prepared me for the assessment(s) implemented', fontsize = 9)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax6.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('cont3_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.7
        fig, ax7 = plt.subplots(figsize=(6, 3))
        bars = ax7.barh(Cnt4_q, Cnt4_counts, color='darkred')
        ax7.set_xlabel('A-STEP Students')
        #ax5.set_ylabel('The content of the tutorial session(s) is related to the module content')
        ax7.set_title('Feedback of assessments was covered in the tutorials', fontsize = 9)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax7.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('cont4_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.7
        fig, ax8 = plt.subplots(figsize=(6, 3))
        bars = ax8.barh(Cnt5_q, Cnt5_counts, color='darkred')
        ax8.set_xlabel('A-STEP Students')
        #ax5.set_ylabel('The content of the tutorial session(s) is related to the module content')
        ax8.set_title('The material in the tutorial session(s) helped me to learn', fontsize = 9)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax8.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('cont5_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.8.1
        fig, ax9 = plt.subplots(figsize=(6, 3))
        bars = ax9.barh(Cnt6_q, Cnt6_counts, color='darkred')
        ax9.set_xlabel('A-STEP Students')
        #ax5.set_ylabel('The content of the tutorial session(s) is related to the module content')
        ax9.set_title('The Tutor was well prepared and is well informed on the subject', fontsize = 9)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax9.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('teach1_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.8.2
        fig, ax10 = plt.subplots(figsize=(6, 3))
        bars = ax10.barh(Cnt7_q, Cnt7_counts, color='darkred')
        ax10.set_xlabel('A-STEP Students')
        #ax5.set_ylabel('The content of the tutorial session(s) is related to the module content')
        ax10.set_title('The tutor spoke clearly and audibly', fontsize = 9)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax10.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('teach2_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.8.3
        fig, ax11 = plt.subplots(figsize=(6, 3))
        bars = ax11.barh(Cnt8_q, Cnt8_counts, color='darkred')
        ax11.set_xlabel('A-STEP Students')
        #ax5.set_ylabel('The content of the tutorial session(s) is related to the module content')
        ax11.set_title('The tutor was enthusiastic and encouraged me to participate in the class', fontsize = 9)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax11.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('teach3_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.8.4
        fig, ax12 = plt.subplots(figsize=(6, 3))
        bars = ax12.barh(Cnt9_q, Cnt9_counts, color='darkred')
        ax12.set_xlabel('A-STEP Students')
        #ax5.set_ylabel('The content of the tutorial session(s) is related to the module content')
        ax12.set_title('The tutor treated all students respectfully and equally', fontsize = 9)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax12.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('teach4_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.8.5
        fig, ax13 = plt.subplots(figsize=(6, 3))
        bars = ax13.barh(Cnt10_q, Cnt10_counts, color='darkred')
        ax13.set_xlabel('A-STEP Students')
        #ax5.set_ylabel('The content of the tutorial session(s) is related to the module content')
        ax13.set_title('The tutorial sessions provided support that helped me succeed in this module', fontsize = 9)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax13.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('teach5_plot.png')
        plt.close()
        
        # Create a bar graph for q 3.8.6
        fig, ax14 = plt.subplots(figsize=(6, 3))
        bars = ax14.barh(Cnt11_q, Cnt11_counts, color='darkred')
        ax14.set_xlabel('A-STEP Students')
        #ax5.set_ylabel('The content of the tutorial session(s) is related to the module content')
        ax14.set_title('The tutorial venue was conductive for interactive group work', fontsize = 9)
        # Add labels to the bars
        for bar in bars:
            width = bar.get_width()
            ax14.annotate(f'{width}', xy=(width, bar.get_y() + bar.get_height() / 2), ha='left', va='center', fontsize=10)

        plt.tight_layout()
        plt.savefig('teach6_plot.png')
        plt.close() 
        
    else:
        st.write(' ')
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
        pdf.cell(0, 5, txt = 'Evaluation Report: 2232', align = 'C', ln=8)
        pdf.cell(0, 5, txt = '', ln =9)
        pdf.cell(0, 5, txt = 'A-STEP', align = 'C', ln=10)
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
        s1 = ('The majority of A-STEP students that participated in the evaluation of the module '+str(f_name[0])+', expressed satisfaction with \
the performance of A-STEP, simultenously highlighting challenges and improvements that could be implemented in future, as well as a general \
concensus that A-STEP is achieving its outcomes.').format()
        pdf.multi_cell(0, 5, txt = str(s1), align = 'L', fill = False)
        pdf.cell(0, 5, txt = '', ln =16, align = 'C')
        pdf.ln(0.25)
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '2. Introduction.', ln =17, align = 'L')
        pdf.cell(0, 5, txt = '', ln =18, align = 'C')
        pdf.ln(0.25)
        s2 = ('Frequent and consistent programme evaluation is a valuable tool for A-STEP, due to its role as a student academic support service for all the UFS academic faculties \
across the Bloemfontein and Qwa-qwa campuses. This is particularly imperative when seeking to strengthen and improve the quality and academic outcomes of the \
programme, as well as the academic impact of the students it is serving. For these reasons, the A-STEP programme evaluation provides basic questions about its effectiveness, and the collected data is \
used for reporting and to improve A-STEP services').format()
        pdf.set_font('Arial','',10.0)
        pdf.multi_cell(0, 5, txt = str(s2), align = 'L', fill = False)
        pdf.cell(0, 5, txt = '', ln =16, align = 'C')
        pdf.ln(0.25)
        s3 = ('The A-STEP evaluation model is comprised of questions aimed at finding out if A-STEP attendees are satisfied with the services of the programme, investigating \
and analysing student satisfaction with the A-STEP content, teaching, learning and more. Additionally, the model seeks challanges faced by students, as well as future recommendations, \
which are used to improve A-STEP sevices.').format()
        pdf.set_font('Arial','',10.0)
        pdf.multi_cell(0, 5, txt = str(s3), align = 'L', fill = False)
        pdf.cell(0, 5, txt = '', ln =16, align = 'C')
        pdf.ln(0.25)
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3. A-STEP Evaluation of the module '+str(f_name[0])+'. ', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =15, align = 'C')
        pdf.ln(0.25)
        pdf.set_font('Arial','',10.0)
        sa = ('The following section presents the findings from the evaluation analysis of the A-STEP module '+str(f_name[0])+', during the second term of the 2023 calendar year (2232). \
The data employed in this analysis was collected from A-STEP students of the module through QuestBack Essential survey forms, comprised of nearly a dozen evaluation questions. \
The aim of this report is to investigate if A-STEP attendees are satisfied with the services of the programme during the 2232 term, in relation with the content provided, tutor performance, \
teaching, learning and more. Additionally, we studied responses to identify attendance challanges, A-STEP marketability, as well as recommendations to be implemented in the future.').format()
        pdf.multi_cell(0, 5, txt = str(sa), align = 'L')
        pdf.cell(0, 5, txt = '', ln =15, align = 'C')
        pdf.ln(0.25)
        s5 = ('The module '+str(f_name[0])+' was evaluated by '+str(part_c[0])+' A-STEP students during the second term of 2023. Students indicated to have been hosted by '+str(Tutor_cnt[0])+' unique \
tutors.')
        pdf.multi_cell(0, 5, txt = str(s5), align = 'L')
        pdf.cell(0, 5, txt = '', ln =15, align = 'C')
        pdf.ln(0.25)
        pdf.add_page()
        pdf.set_font('Arial','B',12.0)
        pdf.cell(0, 5, txt = '3.1. Evaluation Questions', ln =14, align = 'L')
        pdf.cell(0, 5, txt = '', ln =15, align = 'C')
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '3.1.1. Please choose the name of the tutor that assisted you in your '+str(f_name[0])+' tutorial session(s) this semester.', ln =14, align = 'L')
        #pdf.ln(0.25)
        s6 = 'tutors_plot.png'
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
        pdf.cell(0, 5, txt = '3.1.2. Where did you find out about A_STEP tutorials?', ln =14, align = 'L')
        pdf.ln(0.25)
        s7 = 'market_plot.png'
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
        pdf.cell(0, 5, txt = '3.1.3. What factors limit you from attending tutorials?', ln =14, align = 'L')
        pdf.ln(0.25)
        s8 = 'factor_plot.png'
        pdf.image(str(s8), x = 50, y = 200, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '3.1.4. What encourages you to attend tutorials?', ln =14, align = 'L')
        pdf.ln(0.25)
        pdf.set_font('Arial','',10.0)
        s9 = (
            'There were '
            +str(N_com[0])
            + ' unique comments from A-STEP students in the '
            + str(f_name[0])
            + ' module. Many of these comments alluded to the academic help the A-STEP tutorial add to their academic success'
            ' in tests and exams as the main encouragement for attending tutorials. The most popular comments included keywords understanding,'
            ' improve, tests\exams, clarity, prepare, pass and learn, adding up to '
            + str(Pstv_com[0])
            + ' comments. Other encuraging factors mentioned included as tutor, or A-STEP tutors being specifically named.'
        ).format()
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.multi_cell(0, 5, txt = str(s9), align = 'L')
        pdf.cell(0, 5, txt = '', ln =15, align = 'C')
        pdf.set_font('Arial','B',10.0)
        #pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =20, align = 'C')
        #pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        pdf.cell(0, 5, txt = '3.1.5. What is the language of instruction used in the tutorial?', ln =14, align = 'L')
        pdf.ln(0.25)
        s10 = 'lang_plot.png'
        pdf.image(str(s10), x = 50, y = 65, w = 100, h = 70, type = 'PNG')
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
        pdf.cell(0, 5, txt = '3.1.6. What is your current academic year?', ln =14, align = 'L')
        pdf.ln(0.25)
        s11 = 'grade_plot.png'
        pdf.image(str(s11), x = 50, y = 145, w = 100, h = 70, type = 'PNG')
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
        pdf.cell(0, 5, txt = '3.1.7. Content of the tutorials', ln =14, align = 'L')
        pdf.ln(0.25)
        s12 = 'cont1_plot.png'
        pdf.image(str(s12), x = 5, y = 222, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        s13 = 'cont2_plot.png'
        pdf.image(str(s13), x = 106, y = 222, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)
        pdf.add_page()
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s14 = 'cont3_plot.png'
        pdf.image(str(s14), x = 5, y = 10, w = 100, h = 70, type = 'PNG')
        s15 = 'cont4_plot.png'
        pdf.image(str(s15), x = 105, y = 10, w = 100, h = 70, type = 'PNG')        
        pdf.ln(0.25)
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
        s16 = 'cont5_plot.png'
        pdf.image(str(s16), x = 50, y = 80, w = 100, h = 70, type = 'PNG')
        pdf.ln(0.25)        
        pdf.cell(0, 5, txt = '3.1.8. Teaching and Learning', ln =14, align = 'L')
        s17 = 'teach1_plot.png'
        pdf.image(str(s17), x = 5, y = 160, w = 100, h = 70, type = 'PNG')
        s18 = 'teach2_plot.png'
        pdf.image(str(s18), x = 105, y = 160, w = 100, h = 70, type = 'PNG')
        s19 = 'teach3_plot.png'
        pdf.image(str(s19), x = 5, y = 222, w = 100, h = 70, type = 'PNG')
        s20 = 'teach4_plot.png'
        pdf.image(str(s20), x = 105, y = 222, w = 100, h = 70, type = 'PNG')         
        pdf.ln(0.25)
        pdf.add_page()
        pdf.set_font('Arial','B',10.0)
        pdf.cell(0, 5, txt = '', ln =19, align = 'C')
        s21 = 'teach5_plot.png'
        pdf.image(str(s21), x = 5, y = 10, w = 100, h = 70, type = 'PNG')
        s22 = 'teach6_plot.png'
        pdf.image(str(s22), x = 105, y = 10, w = 100, h = 70, type = 'PNG')        
        pdf.ln(0.25)
        
        pdf.output('A_STEP_IR_2019_2022.pdf')
        with st.spinner('Wait for it...'):
                    time.sleep(3)
        with col1:
            progress_bar = st.progress(0)
            for perc_completed in range(100):
                time.sleep(0.001)
            progress_bar.progress(perc_completed+1)
            st.success(':orange[Module '+str(f_name[0])+' successfully Evaluated 👏🏼 👏🏾 👏🏿]', icon="✅")
            st.write(':blue[Survey : '+str(part_c[0])+' Participants 👥]')
        with open('A_STEP_IR_2019_2022.pdf', "rb") as file:
                btn = st.download_button(
                label=":red[Download PDF Report]",
                data=file,
                file_name='A_STEP_IR_2019_2022.pdf',
                mime="file/pdf"
                  )  
                st.success('Report Ready for Download', icon="✅")

else:
    st.sidebar.info(':red[ 🚩 Remember to Upload Files:]', icon="ℹ️") 

st.sidebar.markdown("<h1 style='text-align: center; color: #090257;'>Instructions</h1>", unsafe_allow_html=True)  

st.sidebar.write(':grey[**Prepare and Upload ***.xlsx*** Evaluation Survey Files**]')
st.sidebar.write('- :orange[Generate Report ⤵️]')
st.sidebar.write('- :orange[Download PDF Report 🛸]')
        
st.sidebar.markdown("<h1 style='text-align: center; color: #090257;'>Contact CTL & A-STEP</h1>", unsafe_allow_html=True)
st.sidebar.write('📭 E: :orange[mbonanits@ufs.ac.za]')
st.sidebar.write('📭 E: :orange[emohoanyane@ufs.ac.za]')
st.sidebar.write('🌐 :blue[www.ufs.ac.za/ctl]')
st.sidebar.info(':red[ 🚩 Web App Developer:] Tekano Mbonani', icon="ℹ️") 
