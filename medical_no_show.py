import pandas as pd
import matplotlib.pyplot as plt

# -----------------------
# Load Data
# -----------------------
print("Loading data...")
df = pd.read_csv("medical appointment no show prediction.csv")
print("Data loaded successfully!")

print("\n=== Medical Appointment No Show Prediction ===\n")

# -----------------------
# Fix column
# -----------------------
if 'No-show' in df.columns:
    df['No_show'] = df['No-show'].map({'Yes': 1, 'No': 0})

# Drop unwanted columns
df = df.drop(['PatientId', 'AppointmentID'], axis=1, errors='ignore')

# Convert dates
if 'ScheduledDay' in df.columns:
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
    df['Sched_day'] = df['ScheduledDay'].dt.day

if 'AppointmentDay' in df.columns:
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
    df['App_day'] = df['AppointmentDay'].dt.day

df = df.drop(['ScheduledDay', 'AppointmentDay'], axis=1, errors='ignore')

# Dummies
df = pd.get_dummies(df, drop_first=True)

# Remove nulls
df = df.dropna()

# -----------------------
# FIXED VALUES (NO INPUT)
# -----------------------
num_rows = 10
num_show = 5
num_noshow = 5

# -----------------------
# PATIENT DATA
# -----------------------
print("\n--- Patient Data ---")
print(df.head(num_rows))

# -----------------------
# SHOW vs NO-SHOW
# -----------------------
print("\n--- Show vs No-Show Details ---")

show_df = df[df['No_show'] == 0].copy()
noshow_df = df[df['No_show'] == 1].copy()

show_df = show_df.head(num_show)
noshow_df = noshow_df.head(num_noshow)

show_df['Status'] = "Show"
noshow_df['Status'] = "No-Show"

if 'SMS_received' in show_df.columns:
    show_df['SMS_received'] = show_df['SMS_received'].map({1: 'Yes', 0: 'No'})
    noshow_df['SMS_received'] = noshow_df['SMS_received'].map({1: 'Yes', 0: 'No'})

columns = ['Status', 'SMS_received', 'Diabetes', 'Alcoholism', 'Hypertension', 'Age']
columns = [col for col in columns if col in show_df.columns]

print("\n✅ Show Patients:")
print(show_df[columns])

print("\n❌ No-Show Patients:")
print(noshow_df[columns])

# -----------------------
# GRAPHS
# -----------------------

# Graph 1: Show vs No-Show
df['No_show'].value_counts().plot(kind='bar')
plt.title("Appointment Show vs No Show")
plt.show()

# Graph 2: Age Distribution
if 'Age' in df.columns:
    df['Age'].value_counts().head(20).plot(kind='bar')
    plt.title("Age Distribution")
    plt.show()

# Graph 3: Gender vs No Show
gender_col = None
for col in df.columns:
    if "gender" in col.lower():
        gender_col = col

if gender_col:
    pd.crosstab(df[gender_col], df['No_show']).plot(kind='bar')
    plt.title("Gender vs No Show")
    plt.show()

# Graph 4: SMS Reminder vs No Show
if 'SMS_received' in df.columns:
    pd.crosstab(df['SMS_received'], df['No_show']).plot(kind='bar')
    plt.title("SMS Reminder vs No Show")
    plt.show()