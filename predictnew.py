import streamlit as st
import base64
import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder
from typing import List

# Function to read and encode the SVG image
def get_svg_image_as_base64(file_path):
    with open(file_path, "rb") as svg_file:
        encoded_svg = base64.b64encode(svg_file.read()).decode()
    return encoded_svg

# Read and encode the local SVG image
encoded_svg_image = get_svg_image_as_base64("images/th2.svg")

# Load the model and encoders
model_filename = 'model/salary_prediction_model.pkl'
encoder_filename = 'model/encoders_and_skills.pkl'

try:
    with open(model_filename, 'rb') as file:
        model = pickle.load(file)

    with open(encoder_filename, 'rb') as file:
        encoders_and_skills = pickle.load(file)

    country_encoder = encoders_and_skills['country_encoder']
    edlevel_encoder = encoders_and_skills['edlevel_encoder']
    age_mapping = encoders_and_skills['age_mapping']
    all_skills = encoders_and_skills['all_skills']
except KeyError as e:
    st.error(f"Missing key: {e}")
    st.stop()
except FileNotFoundError as e:
    st.error(f"File not found: {e}")
    st.stop()
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.stop()

# List of countries according to the dataset
countries_list = [
    'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 
    'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 
    'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bolivia', 'Bosnia and Herzegovina', 
    'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 
    'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Chile', 'China', 'Colombia', 
    'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', "Côte d'Ivoire", 
    'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 
    'El Salvador', 'Estonia', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 
    'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Guinea', 'Guinea-Bissau', 
    'Guyana', 'Honduras', 'Hong Kong (S.A.R.)', 'Hungary', 'Iceland', 'India', 
    'Indonesia', 'Iran, Islamic Republic of...', 'Iraq', 'Ireland', 'Isle of Man', 
    'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 
    'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Lao People\'s Democratic Republic', 'Latvia', 
    'Lebanon', 'Lesotho', 'Libyan Arab Jamahiriya', 'Liechtenstein', 'Lithuania', 
    'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 
    'Mauritania', 'Mauritius', 'Mexico', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 
    'Mozambique', 'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 
    'Nicaragua', 'Niger', 'Nigeria', 'Nomadic', 'Norway', 'Oman', 'Pakistan', 
    'Palau', 'Palestine', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland', 
    'Portugal', 'Qatar', 'Republic of Korea', 'Republic of Moldova', 'Romania', 
    'Russian Federation', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 
    'Saint Vincent and the Grenadines', 'Saudi Arabia', 'Senegal', 'Serbia', 
    'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 
    'South Korea', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 
    'Switzerland', 'Syrian Arab Republic', 'Taiwan', 'Tajikistan', 'Thailand', 
    'The former Yugoslav Republic of Macedonia', 'Togo', 'Trinidad and Tobago', 
    'Tunisia', 'Turkey', 'Turkmenistan', 'Uganda', 'Ukraine', 'United Arab Emirates', 
    'United Kingdom of Great Britain and Northern Ireland', 'United Republic of Tanzania', 
    'United States of America', 'Uruguay', 'Uzbekistan', 'Venezuela, Bolivarian Republic of...', 
    'Viet Nam', 'Yemen', 'Zambia', 'Zimbabwe'
]

# Helper function to get user input and format it for prediction
def get_user_input(user_age, user_edlevel, user_country, user_workexp, user_skills):
    # Encode categorical user input
    user_age_encoded = age_mapping.get(user_age, 0)
    user_country_encoded = country_encoder.transform([user_country])[0]
    user_edlevel_encoded = edlevel_encoder.transform([user_edlevel])[0]

    # Create a feature vector for the user input
    user_features = {
        'Age': user_age_encoded,
        'EdLevel': user_edlevel_encoded,
        'Country': user_country_encoded,
        'WorkExp': user_workexp
    }

    # Initialize skill columns with 0
    for skill in all_skills:
        user_features[skill] = 0

    # Set the skills the user has to 1
    for skill in user_skills:
        user_features[skill] = 1

    user_df = pd.DataFrame([user_features])
    return user_df

if 'show_about' not in st.session_state:
    st.session_state.show_about = False

# Header with logo and navbar using HTML and CSS
header_html = """
    <style>
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background-color:#108eda;
        color: white;
    }
    .logo {
        width: 116px; /* Adjust size as needed */
        height: auto;
    }
    .navbar {
        display: flex;
        gap: 20px;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        font-weight: bold;
        padding: 5px 10px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .navbar a:hover {
        background-color: #003db5;
    }
    </style>
    <div class="header">
        <img src="https://www.norteccommunications.com/wp-content/uploads/2020/06/nextgen_logo.png" alt="Logo" class="logo">
        <div class="navbar">
            <a href="#predict-software-developer-salaries-with-accuracy">Home</a>
            <a href="#about-us">About</a>
            <a href="#salary-predictor">Salary Predictor</a>
            <a href="#contact-us">Contact</a>
        </div>
    </div>
"""

# Render the header
st.markdown(header_html, unsafe_allow_html=True)

# Homepage with background image and text
st.markdown(f"""
    <style>
    .homepage {{
        background-image: url('data:image/svg+xml;base64,{encoded_svg_image}');
        background-size: cover;
        background-position: center;
        height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding-left: 24px;
        color: white;
        font-size: 36px;
        opacity: 0.9;
    }}
    .stars {{
        display: flex;
        align-items: center;
        margin-top: 10px;
    }}
    .star {{
        width: 24px;
        height: 24px;
        margin-right: 5px;
        filter: invert(89%) sepia(7%) saturate(1666%) hue-rotate(58deg) brightness(97%) contrast(93%);
    }}
    .predict-salary-button {{
        background-color: #003db5;
        color: white;
        padding: 10px 5px;
        width: 150px; /* Set width of the button */
        border: none;
        border-radius: 5px;
        font-size: 18px;
        cursor: pointer;
        margin-bottom: 10px;
        transition: background-color 0.3s;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}
    .predict-salary-button:hover {{
        background-color: #108eda;
    }}
    </style>
    <div class="homepage">
        <h1 style="color:white;font-weight:bolder;font-size:49px">Predict<br> Software Developer Salaries <br>with Accuracy</h1>
        <p>Utilize machine learning to predict software developer salaries accurately with NexGenSalary.</p>
        <button class="predict-salary-button" onclick="window.location.href='#salary-predictor'">Predict Salary</button>
        <div class="stars">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/49/Star_empty.svg" alt="Star" class="star">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/49/Star_empty.svg" alt="Star" class="star">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/49/Star_empty.svg" alt="Star" class="star">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/49/Star_empty.svg" alt="Star" class="star">
            <img src="https://upload.wikimedia.org/wikipedia/commons/4/49/Star_empty.svg" alt="Star" class="star">
        </div>
    </div>
""", unsafe_allow_html=True)

# Display About Us section
if st.session_state.show_about:
    st.markdown("<h2 id='about' style='text-align:center;font-weight:bolder;background-color:#192533;color:white'>About Us</h2>", unsafe_allow_html=True)
    about_us_html = """
        <div style="display: flex; align-items: center; background-color:#192533; color:white; padding:20px;">
            <div style="flex: 1; padding: 20px;">
                Welcome to <b style='color:#108eda'>NexGenSalary Predictor</b>! We are dedicated to helping you estimate your salary based on various factors such as experience, education, and skills.
                <br>Our project aims to use machine learning to accurately predict how much software developers should earn. We'll analyze things like their experience, where they work, 
                and their job title to give HR departments, recruiters, and job seekers helpful information for making decisions about hiring and compensation.
            </div>
            <div style="flex: 1; text-align: center;">
                <img src="https://assets.entrepreneur.com/content/3x2/2000/20191202130611-salarypicture.jpeg" alt="About Us Image" style="max-width: 100%; height: auto; border: 2px solid black; border-radius: 10px;">
            </div>
        </div>
    """
    st.markdown(about_us_html, unsafe_allow_html=True)

# Section for Salary Predictor inputs in a form with reduced width
st.markdown("<h2 id='predictor' style='text-align:center;font-weight:bolder;background-color:#192533;color:white'>Salary Predictor</h2>", unsafe_allow_html=True)

# Inputs for the user with optimization
with st.spinner('Loading options...'):
    # Exclude 'Under 18 years old' from the age options
    age_options = ["-Select-"] + [age for age in age_mapping.keys() if age != 'Under 18 years old']
    user_age = st.selectbox('Age', options=age_options, index=0)

    # Exclude '-Select-' from education level options
    edlevel_options = list(edlevel_encoder.classes_)
    user_edlevel = st.selectbox('Education Level', options=edlevel_options, index=0)

    # Include countries list without '-Select-' option
    country_options = countries_list
    user_country = st.selectbox('Country', options=country_options, index=0)

    user_workexp = st.slider('Years of Work Experience', min_value=0, max_value=50, value=0)

# Skill selection with dynamic addition
combined_skills = list(set(all_skills + st.session_state.get('temporary_skills', [])))
selected_skills = st.multiselect('Skills', options=combined_skills, default=[])

if st.button('Predict Salary'):
    if user_age == "-Select-" or user_edlevel == "-Select-" or user_country == "-Select-":
        st.warning('Please fill in all mandatory fields: Age, Education Level And Country.')
    else:
        user_df = get_user_input(user_age, user_edlevel, user_country, user_workexp, selected_skills)
        
        # Predict salary
        try:
            prediction = model.predict(user_df)[0]
            st.success(f'Predicted Salary: ${prediction:,.2f}')
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

# List of developers with their images and names
# List of developers with their images and names
developers = [
    {"name": "Dev Mer", "image_url": "https://tweakyourbiz.com/wp-content/uploads/2022/05/React-Native-App-Developer-India.jpg"},
    {"name": "Sanket Prajapati", "image_url": "https://www.springboard.com/blog/wp-content/uploads/2021/03/how-to-become-a-financial-analyst.jpg"},
    {"name": "Vivek Mali", "image_url": "https://tse4.mm.bing.net/th?id=OIP.VOT-9gDBRzUPC2DLIZJYnQAAAA&pid=Api&P=0&h=180"},
    {"name": "Saloni Rana", "image_url": "https://static.economist.com/sites/default/files/images/print-edition/20230624_ima003.jpg"},
    {"name": "Nivedita Parmar", "image_url": "https://wallpapercave.com/wp/wp5799138.jpg"},
]

# Display all developers in a single row using Streamlit columns
col1, col2, col3, col4, col5 = st.columns(5)

for idx, developer in enumerate(developers):
    with col1 if idx == 0 else col2 if idx == 1 else col3 if idx == 2 else col4 if idx == 3 else col5:
        st.markdown(f"""
            <div style="border: 2px solid #ccc; border-radius: 10px; padding: 10px; text-align: center; height: 190px;">
                <img src="{developer['image_url']}" alt="{developer['name']}'s Image" style="width: 100px; height: 100px; border-radius: 50%; border: 2px solid black;">
                <h3 style='text-align:center;font-size:22px'>{developer['name']}</h3>
            </div>
        """, unsafe_allow_html=True)

# Display Contact section
st.markdown("<h2 id='contact-us' style='text-align:center;font-weight:bolder;background-color:#192533;color:white'>Connect With Us</h2>", unsafe_allow_html=True)

with st.container():
    st.markdown("""
        <style>
        .contact-form-container {
            max-width: 500px;
            margin: 0 auto;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="contact-form-container">', unsafe_allow_html=True)
    
    with st.form(key='contact_form_1'):
        st.text_input('Your Name', key='contact_name')
        st.text_input('Email Address', key='contact_email')
        st.text_area('Message', key='contact_message', height=150)
        
        st.write('<style>div.row-widget.stButton {justify-content: center;}</style>', unsafe_allow_html=True)
        submit_contact_button = st.form_submit_button(label='Send Message')

    if submit_contact_button:
        # Placeholder for actual backend logic
        st.success('Your message has been sent successfully!')
        st.write("""
            <script>
            setTimeout(function() {
                document.querySelector(".css-1ceggqc-StreamlitSuccess").style.opacity = '0';
                document.querySelector(".css-1ceggqc-StreamlitSuccess").style.transition = 'opacity 2s ease-out';
                setTimeout(function() {
                    document.querySelector(".css-1ceggqc-StreamlitSuccess").style.display = 'none';
                }, 1500);
            }, 1500);
            </script>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Footer with styling
footer_html = """
    <style>
    .footer {
        font-size: 20px;
        text-align: center;
        color: white;
        padding: 10px;
        background-color: #108eda;
        bottom: 0;
        width: 100%;
    }
    </style>
    <div class="footer">
        Made with ❤️ by TenchTrendSetters<br> © 2024 NextGenSalary. All rights reserved.
    </div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
