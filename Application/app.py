import streamlit as st
import pandas as pd
import joblib

# Set page config
st.set_page_config(page_title='Loan Eligibility Prediction System', page_icon=':bank:', layout='wide')

# Load the model
model = joblib.load('final.pkl')  # Replace 'model.pkl' with your actual model filename

def preprocess_input(data):
    df = pd.DataFrame(data, index=[0])

    # Your preprocessing steps
    df['MaritalStatus'] = df['MaritalStatus'].replace({'Divorced': 0, 'Married': 1, 'Single': 2})
    df['EmploymentType'] = df['EmploymentType'].replace({'Employed': 1, 'Unemployed': 0})
    df['Education'] = df['Education'].replace({'Bachelor': 0, 'High School': 1, 'Masters': 2, 'PHD': 3})
    df['HasMortgage'] = df['HasMortgage'].replace({'Yes': 1, 'No': 0})
    df['HasDependents'] = df['HasDependents'].replace({'Yes': 1, 'No': 0})
    df['HasCoSigner'] = df['HasCoSigner'].replace({'Yes': 1, 'No': 0})
    df['LoanPurpose'] = df['LoanPurpose'].replace({'Auto': 0, 'Business': 1, 'Education': 2, 'Home': 3, 'Other': 4})

    return df

def predict_loan_status(data):
    # Preprocess input
    preprocessed_data = preprocess_input(data)

    # Debugging: Print preprocessed data
    print("Preprocessed data:", preprocessed_data)

    # Make prediction using loaded model
    prediction = model.predict(preprocessed_data)

    # Debugging: Print prediction result
    print("Prediction:", prediction)

    # Return prediction
    return prediction


def get_insight(age, marital_status, months_employed):
    # Provide insights based on inputs...
    if age <= 30:
        st.write("People with age less than 30 are 3% less likely to be eligible for the loan.")
    
    if months_employed <= 12:  
        st.write("People with less than 5 years of experience are 4% less likely to be eligible for the loan.")
    elif months_employed < 48:  
        st.write("People with less than 16 years of experience are 2% less likely to be eligible for the loan.")
    
    if marital_status == 'Single':
        st.write("People who are married are 3% more likely to be eligible for the loan.")

def app():
    st.title('Loan Eligibility Prediction System')
    st.image('logo.jpeg', width=200)  # Assuming you have a logo image

    # Explain the app
    st.markdown("""
    Welcome to your Loan Eligibility Prediction System. This system predicts...
    """)

    # Layout inputs using columns
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input('Enter your Age', min_value=0)
        marital_status = st.selectbox('MaritalStatus', ['Divorced', 'Married', 'Single'])
        employment_type = st.selectbox('Employment Type', ['Employed', 'Unemployed'])
        education = st.selectbox('Education Level', ['High School', 'Bachelor', 'Masters', 'PHD'])


    with col2:
        months_employed = st.number_input('Months Employed', min_value=0)
        has_dependents = st.selectbox('Has Dependents', ['Yes', 'No'])
        loan_term = st.number_input('How long do you plan to payup the loan(Months)')

    with col3:
        has_mortgage = st.selectbox('Has Mortgage', ['Yes', 'No'])
        has_cosigner = st.selectbox('Has CoSigner', ['Yes', 'No'])
        loan_purpose = st.selectbox('Loan Purpose', ['Auto', 'Business', 'Education', 'Home', 'Other'])
        income = st.number_input('Applicant Income', min_value=0)
        loan_amount = st.number_input('Loan Amount', min_value=500)


    submit_button = st.button('Click to check eligibility')

    if submit_button:
        inputs = {
            'Age': age,
            'MaritalStatus': marital_status,
            'EmploymentType': employment_type,
            'MonthsEmployed': months_employed,
            'HasDependents': has_dependents,
            'Education': education,
            'HasMortgage': has_mortgage,
            'HasCoSigner': has_cosigner,
            'LoanPurpose': loan_purpose,
            'LoanTerm': loan_term,
            'Income': income,
            'LoanAmount': loan_amount
        }

        prediction = predict_loan_status(inputs)

        if prediction == 0:
            st.error('Sorry, you do not qualify for this loan.')
            get_insight(age, marital_status, months_employed)
        else:
            st.success('Congratulations, you are eligible.')

if __name__ == '__main__':
    app()
