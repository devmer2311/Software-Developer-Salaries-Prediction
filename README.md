# Software Developer Salaries Prediction

## Overview

This project aims to predict the salaries of software developers based on various features such as experience, skills, education, and location. The application uses a machine learning model trained on a dataset of software developer salaries.

## Features

- **Salary Prediction:** Predict the salary of a software developer based on input features.
- **Dynamic Skill Selection:** Users can dynamically add new skills to the prediction model.
- **Country and Age Filtering:** Filters available based on the predefined dataset.
- **Educational Qualification Handling:** Includes various education levels for predictions.

## Technologies Used

- **Streamlit:** For creating interactive web applications.
- **Python:** Programming language for the machine learning model and application logic.
- **Machine Learning Libraries:** Libraries like `scikit-learn` for training and using the prediction model.
- **Git LFS:** For handling large model files.

## Live Demo

Check out the live demo of the application at [`nextgen.streamlit.app`](https://nextgen.streamlit.app).

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repository**

   Open your terminal or command prompt and clone the repository using:

   ```git clone https://github.com/devmer2311/Software-Developer-Salaries-Prediction.git ```
   
2. **Navigate to the Project Directory**

   Change into the project directory:

   ```cd Software-Developer-Salaries-Prediction```

3. **Install Dependencies**

   Ensure you have Python and pip installed. Install the required Python libraries using:

   ``` pip install -r requirements.txt ```

4. **Run the Application**

   Start the Streamlit application using:

   ``` streamlit run app.py ```

   This command will open the application in your default web browser.

## Project Structure

- **predictnew.py**: The main Streamlit application file.
- **model/**: Directory containing the machine learning model and encoders.
- **requirements.txt**: File listing Python package dependencies.
- **.gitattributes**: Git LFS configuration file for tracking large files.


## Contributing
If you would like to contribute to this project, follow these steps:

Fork the Repository: Click the "Fork" button at the top-right of this page.

Clone Your Fork: Clone your fork to your local machine.

Create a New Branch: Create a new branch for your changes.

```git checkout -b my-feature-branch```

Make Your Changes: Make your modifications to the code or documentation.

```git add . ```

```git commit -m "Description of the changes" ```

Push Your Changes:

``` git push origin my-feature-branch ```

Create a Pull Request: Go to the original repository and create a pull request from your branch.

