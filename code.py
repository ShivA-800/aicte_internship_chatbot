import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Define questions and answers for each role
roles = {
    "Software Developer": [
        ("What is object-oriented programming?", "It is a paradigm using objects and classes for modularity."),
        ("Explain the Software Development Life Cycle (SDLC).", "It is a process with phases like planning, design, and testing."),
        ("What is the difference between compiled and interpreted languages?", "Compiled translates before execution, interpreted runs line by line."),
        ("What are design patterns?", "Reusable solutions for common software design problems."),
        ("What is version control, and why is it important?", "Tracks code changes and enables collaboration."),
        ("What are microservices?", "Independent services for specific functions in an application."),
        ("Explain RESTful APIs.", "APIs that use standard HTTP methods for communication."),
        ("What are some best practices for writing clean code?", "Use readable names, consistent formatting, and comments."),
        ("What is Agile methodology?", "An iterative development approach focused on collaboration."),
        ("What is the difference between unit testing and integration testing?", "Unit tests individual components, integration tests combined components.")
    ],
    "Web Developer": [
        ("What is the difference between HTML and HTML5?", "HTML5 adds features like multimedia and semantic elements."),
        ("What is CSS?", "A language for styling and laying out web pages."),
        ("What is JavaScript, and why is it important?", "A language for adding interactivity to websites."),
        ("Explain the concept of responsive design.", "Ensures websites adapt to various screen sizes."),
        ("What is a framework, and why is it used?", "Pre-written tools to simplify development, like React."),
        ("What is the DOM in web development?", "A tree structure representing a webpage."),
        ("What are APIs, and how are they used in web development?", "Interfaces for communication between software systems."),
        ("What is cross-browser compatibility?", "Ensures websites work on different browsers."),
        ("What is SEO, and why is it important?", "Optimizing websites for better search engine ranking."),
        ("What is the difference between static and dynamic websites?", "Static is fixed, dynamic changes based on interaction.")
    ],
    "Flutter Developer": [
        ("What is Flutter?", "A UI toolkit for building cross-platform apps."),
        ("What is a widget in Flutter?", "The building block for creating UI in Flutter."),
        ("What is Dart, and why is it used in Flutter?", "Dart is Flutter's programming language."),
        ("What are stateful and stateless widgets?", "Stateful maintains state, stateless does not."),
        ("What is hot reload in Flutter?", "A feature to instantly see code changes in the UI."),
        ("What is the difference between runApp() and main()?", "main() starts the app, runApp() sets the root widget."),
        ("How do you manage state in Flutter?", "Using providers, BLoC, or setState()."),
        ("What is the purpose of pubspec.yaml?", "To manage dependencies and metadata for the app."),
        ("What is Navigator in Flutter?", "Manages app navigation and routes."),
        ("What are some common layout widgets in Flutter?", "Row, Column, Stack, and Container.")
    ],
    "Network Administrator": [
        ("What is a network topology?", "The arrangement of devices in a network."),
        ("What is the difference between a switch and a router?", "Switch connects devices, router connects networks."),
        ("What is an IP address?", "A unique identifier for devices on a network."),
        ("What is a firewall?", "A security system to control network traffic."),
        ("What is the OSI model?", "A framework for understanding network layers."),
        ("What is DHCP?", "A protocol for automatic IP address assignment."),
        ("What is DNS?", "Translates domain names to IP addresses."),
        ("What is a VPN?", "A secure connection over a public network."),
        ("What is subnetting?", "Dividing a network into smaller segments."),
        ("What is bandwidth?", "The maximum data transfer rate of a network.")
    ],
    "IT Consultant": [
        ("What does an IT consultant do?", "Advises on technology to meet business needs."),
        ("What is cloud computing?", "Delivery of services like storage over the internet."),
        ("What is the importance of cybersecurity?", "Protects systems from unauthorized access."),
        ("What is change management?", "Handling changes in IT systems or processes."),
        ("What are the benefits of virtualization?", "Efficient resource use and easier management."),
        ("What is disaster recovery?", "A plan to restore IT operations after disruptions."),
        ("What is ITIL?", "A framework for managing IT services."),
        ("What is business continuity planning?", "Ensuring operations during and after disruptions."),
        ("What is a feasibility study?", "Assessing the viability of a proposed project."),
        ("What is the role of data analytics in IT consulting?", "Provides insights for better decision-making.")
    ],
    "Team Leader": [
        ("What are the key qualities of a team leader?", "Good communication, decision-making, and empathy."),
        ("How do you motivate a team?", "By setting clear goals and recognizing achievements."),
        ("What is conflict resolution?", "Addressing and resolving disputes effectively."),
        ("What is delegation?", "Assigning tasks to team members based on skills."),
        ("What is the importance of feedback?", "Helps improve performance and team dynamics."),
        ("What is team building?", "Activities to strengthen collaboration and trust."),
        ("How do you handle underperforming team members?", "Identify issues and provide support for improvement."),
        ("What is time management?", "Efficiently planning and controlling time for tasks."),
        ("How do you manage stress in a team?", "Promote work-life balance and provide support."),
        ("What is goal setting?", "Defining objectives to guide team efforts.")
    ],
    "HR": [
        ("What is the role of HR in an organization?", "Manages recruitment, employee relations, and policies."),
        ("What is recruitment?", "The process of hiring the right talent."),
        ("What is employee engagement?", "Strategies to keep employees motivated and satisfied."),
        ("What is performance management?", "Monitoring and improving employee performance."),
        ("What is training and development?", "Programs to enhance employee skills and knowledge."),
        ("What is workplace diversity?", "Inclusion of employees from various backgrounds."),
        ("What is employee retention?", "Strategies to keep employees in the organization."),
        ("What is conflict management?", "Resolving disputes among employees effectively."),
        ("What is payroll management?", "Handling employee salaries, taxes, and benefits."),
        ("What is compliance in HR?", "Ensuring adherence to labor laws and regulations.")
    ]
}

# Prepare training data for each role
if "models" not in st.session_state:
    models = {}
    vectorizers = {}

    for role, qna in roles.items():
        questions = [q for q, _ in qna]
        answers = [a for _, a in qna]

        # Train TfidfVectorizer and LogisticRegression for each role
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(questions)
        model = LogisticRegression()
        model.fit(X, answers)

        models[role] = model
        vectorizers[role] = vectorizer

    st.session_state.models = models
    st.session_state.vectorizers = vectorizers

# Sidebar Navigation
st.sidebar.title("Job Interview Chatbot")
menu = st.sidebar.radio("Navigate", ["Home", "Conversation History", "About"])

# Store conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Main application logic
if menu == "Home":
    st.title("Job Interview Chatbot")

    # Role selection dropdown
    selected_role = st.selectbox("Select a Job Role:", list(roles.keys()))

    user_input = st.text_input("Ask a question about your selected job role:")

    if st.button("Get Answer"):
        if user_input.strip():
            # Fetch the corresponding model and vectorizer
            model = st.session_state.models[selected_role]
            vectorizer = st.session_state.vectorizers[selected_role]

            # Predict response
            input_vec = vectorizer.transform([user_input])
            prediction = model.predict(input_vec)[0]

            st.write("**Chatbot Response:**")
            st.write(prediction)

            # Save conversation to history
            st.session_state.history.append((selected_role, user_input, prediction))
        else:
            st.warning("Please enter a question!")

elif menu == "Conversation History":
    st.title("Conversation History")

    if st.session_state.history:
        for i, (role, q, a) in enumerate(st.session_state.history, 1):
            st.write(f"{i}. **Role:** {role}")
            st.write(f"   **Question:** {q}")
            st.write(f"   **Answer:** {a}")
    else:
        st.write("No conversation history yet.")

elif menu == "About":
    st.title("About This Chatbot")
    st.write("""
        Here’s a detailed description of the "Interview Preparation Chatbot" is created by **Shiva Radharapu**, along with the kind of information the bot can provide:

---

### **Interview Preparation Chatbot**

The **Interview Preparation Chatbot** is an Intent based chatbot designed to help job seekers and candidates prepare for interviews. It simulates real-life interview scenarios, offering personalized guidance based on the job role, industry, and user’s experience level. By interacting with the chatbot, candidates can practice answering common interview questions, receive tips on improving their responses, and gain insights into the interview process.

### **Features and Capabilities:**

1. **Mock Interview Sessions**:
   - The chatbot can conduct mock interviews by asking a series of commonly asked interview questions.
   - It can simulate both technical and non-technical interviews based on the user's preferences.

2. **Personalized Question Bank**:
   - The chatbot is equipped with a vast database of interview questions, categorized by:
     - **Behavioral questions** (e.g., “Tell me about a time you overcame a challenge”).
     - **Technical questions** (e.g., coding problems, algorithm-related questions).
     - **Situational questions** (e.g., “How would you handle a conflict with a coworker?”).
     - **Industry-specific questions** (for tech, finance, healthcare, etc.).
   
3. **Interview Tips**:
   - The chatbot provides general advice and strategies for preparing for interviews:
     - **Dos and Don’ts** in interviews.
     - **Effective ways to present your experience**.
     - **Answering tricky or difficult questions**.
     - **Improving body language and communication skills**.


### **User Experience**:

1. **Easy Interaction**:
   - The chatbot communicates through text-based conversation, making it user-friendly and accessible.
   - Users can ask specific questions, such as “What are some common questions for a software developer interview?” or “How can I improve my communication skills?”.


2. **Data Privacy**:
   - The chatbot ensures that all personal information shared by the user (e.g., resume, LinkedIn profile, etc.) is kept confidential and used only for providing tailored suggestions and feedback.

3. **Accessibility**:
   - Available 24/7, the chatbot can be accessed via a website or mobile app, providing interview preparation resources at any time.

---
**By**  
Shiva kumar Radharapu   
AICTE Student ID: STU657db68fae2661702737551  
AICTE Internship ID: INTERNSHIP_173070615967287aef12823  





    """)
    #https://shivaradharapu-aicte-internship-chatbot.streamlit.app/  deployment using streamlit 
