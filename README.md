# Job Interview Preparation Intent-based Chatbot  

This project is a **Job Interview Preparation Chatbot** developed as part of the **Skill4Future Internship** by AICTE. The chatbot is designed to assist job seekers in preparing for interviews by simulating Q&A sessions tailored to specific job roles. It uses Python, Streamlit, and Natural Language Processing (NLP) techniques to provide an interactive and engaging user experience.  

## Features  
- Simulates mock interview sessions with commonly asked questions.  
- Offers personalized question banks for various job roles like Software Developer, Web Developer, Flutter Developer, and more.  
- Maintains a conversation history for users to review and learn.  
- Provides a user-friendly interface built with **Streamlit**.  

## How It Works  
1. Select a job role from the dropdown menu.  
2. Ask your questions related to the role in the text input field.  
3. The chatbot uses NLP to analyze the question and provides an appropriate response.  
4. Conversation history is stored for future reference.  

## Tech Stack  
- **Language:** Python  
- **Framework:** Streamlit  
- **Libraries Used:**  
  - `scikit-learn` for training and predicting responses.  
  - `TfidfVectorizer` for text vectorization.  
  - `LogisticRegression` for response classification.  

## Deployment  
The chatbot is designed to be deployed using **Streamlit Cloud** for easy access via a web browser.  

## Setup Instructions  
1. Clone the repository:  
   ```bash
   git clone https://github.com/ShivA-800/aicte_internship_chatbot.git
   cd job-interview-chatbot

2. Install the required packages:
   pip install -r requirements.txt

3. Run the chatbot locally:
   streamlit run chatbot.py

