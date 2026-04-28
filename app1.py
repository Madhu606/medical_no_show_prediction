import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Medical Appointment No Show Prediction")

# -----------------------
# Load Data
# -----------------------
df = pd.read_csv("medical appointment no show prediction.csv")

# -----------------------
# FIX COLUMNS
# -----------------------
if 'Hipertension' in df.columns:
    df.rename(columns={'Hipertension': 'Hypertension'}, inplace=True)

# -----------------------
# SHOW ORIGINAL FULL DATA
# -----------------------
st.subheader("📋 Full Dataset")
st.dataframe(df)

# -----------------------
# USE ORIGINAL VALUES (YES/NO)
# -----------------------
df['Status'] = df['No-show']   

# -----------------------
# PREPROCESSING
# -----------------------
df = df.drop(['PatientId', 'AppointmentID'], axis=1, errors='ignore')

if 'ScheduledDay' in df.columns:
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
    df['Sched_day'] = df['ScheduledDay'].dt.day

if 'AppointmentDay' in df.columns:
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
    df['App_day'] = df['AppointmentDay'].dt.day

df = df.drop(['ScheduledDay', 'AppointmentDay'], axis=1, errors='ignore')

df = df.dropna()

# -----------------------
# SHOW vs NO-SHOW TABLES
# -----------------------
show_df_full = df[df['Status'] == 'No'].copy()     
noshow_df_full = df[df['Status'] == 'Yes'].copy()  

st.subheader("Show vs No-Show Details")

num_show = st.slider("Show Patients Rows", 1, len(show_df_full), 5)
num_noshow = st.slider("No-Show Patients Rows", 1, len(noshow_df_full), 5)

show_df = show_df_full.head(num_show).copy()
noshow_df = noshow_df_full.head(num_noshow).copy()

# Add labels
show_df['Status'] = "Show"
noshow_df['Status'] = "No-Show"

# Convert SMS to Yes/No
if 'SMS_received' in show_df.columns:
    show_df['SMS_received'] = show_df['SMS_received'].map({1: 'Yes', 0: 'No'})
    noshow_df['SMS_received'] = noshow_df['SMS_received'].map({1: 'Yes', 0: 'No'})

# Columns to show
columns = ['Status', 'No-show', 'SMS_received', 'Diabetes', 'Alcoholism', 'Hypertension', 'Age']
columns = [col for col in columns if col in show_df.columns]

col1, col2 = st.columns(2)

with col1:
    st.success("✅ Show Patients")
    st.dataframe(show_df[columns])

with col2:
    st.error("❌ No-Show Patients")
    st.dataframe(noshow_df[columns])

# -----------------------
# GRAPHS
# -----------------------
st.subheader("📊 Data Visualizations")

# Graph 1 (Using Yes/No)
fig1, ax1 = plt.subplots()
df['Status'].value_counts().plot(kind='bar', ax=ax1)
ax1.set_title("Appointment Status (Show vs No-Show)")
ax1.set_xticklabels(['No-Show', 'Show'], rotation=0)
st.pyplot(fig1)

# Graph 2
if 'Age' in df.columns:
    fig2, ax2 = plt.subplots()
    df['Age'].value_counts().head(20).plot(kind='bar', ax=ax2)
    ax2.set_title("Age Distribution")
    st.pyplot(fig2)

# Graph 3
if 'Gender' in df.columns:
    fig3, ax3 = plt.subplots()
    pd.crosstab(df['Gender'], df['Status']).plot(kind='bar', ax=ax3)
    ax3.set_title("Gender vs Appointment Status")
    st.pyplot(fig3)

# Graph 4
if 'SMS_received' in df.columns:
    fig4, ax4 = plt.subplots()
    pd.crosstab(df['SMS_received'], df['Status']).plot(kind='bar', ax=ax4)
    ax4.set_title("SMS Reminder vs Appointment Status")
    st.pyplot(fig4)