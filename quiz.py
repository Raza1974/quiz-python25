import streamlit as st
import time
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from io import BytesIO
import random

# Page config
st.set_page_config(page_title="Python Quiz App", page_icon="🧠")
st.title("🧠 Python MCQ Quiz App")
st.markdown("Answer all questions, and click **Submit Quiz** to see your score.")

# Author & social info
st.sidebar.markdown("### 👨‍💻 Author")
st.sidebar.write("**Syed Mohammad Raza Rizvi**")
st.sidebar.write("Governor Sindh IT Initiative Student")
st.sidebar.write("[📧 Email](mailto:asimr6573@gmail.com)")
st.sidebar.write("[🔗 LinkedIn](https://www.linkedin.com/in/rizviraza74)")

# Username input
name = st.text_input("👤 Enter your name:", key="username")

# Timer (40 minutes)
with st.expander("⏱ Timer (40 min)", expanded=True):
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, 2400 - int(elapsed))  # 2400 seconds = 40 minutes
    mins, secs = divmod(remaining, 60)
    st.info(f"⏳ Time Remaining: {mins:02d}:{secs:02d}")
    if remaining == 0:
        st.error("⏰ Time's up! Please submit your quiz now.")

# Questions (shuffled every refresh)
questions = [
    {"question": "What is the output of print(type([]))?", "options": ["<class 'list'>", "<class 'tuple'>", "<class 'dictionary'>", "<class 'set'>"], "answer": "<class 'list'>"},
    {"question": "Which of the following is a mutable data type in Python?", "options": ["String", "Tuple", "List", "Integer"], "answer": "List"},
    {"question": "What will be the output of a = [1, 2, 3]; print(a * 2)?", "options": ["[1, 2, 3, 1, 2, 3]", "[2, 4, 6]", "Error", "[1, 2, 3, 2]"], "answer": "[1, 2, 3, 1, 2, 3]"},
    {"question": "Which keyword is used to define a function in Python?", "options": ["func", "define", "def", "function"], "answer": "def"},
    {"question": "What is the output of bool(0) in Python?", "options": ["True", "False", "0", "None"], "answer": "False"},
    {"question": "Which of the following is used to handle exceptions in Python?", "options": ["do-catch", "try-except", "try-catch", "catch-except"], "answer": "try-except"},
    {"question": "What is the result of len('Hello World')?", "options": ["10", "11", "12", "Error"], "answer": "11"},
    {"question": "Which of the following is NOT a valid Python keyword?", "options": ["assert", "pass", "eval", "then"], "answer": "then"},
    {"question": "Which data type is used to store key-value pairs?", "options": ["List", "Tuple", "Dictionary", "Set"], "answer": "Dictionary"},
    {"question": "What will be the output of x = 'Python'; print(x[0])?", "options": ["P", "y", "n", "x"], "answer": "P"},
    {"question": "What does the __init__() function do in a class?", "options": ["Initializes the class attributes", "Is used for inheritance", "Is used to create a new object", "Is used to delete an object"], "answer": "Initializes the class attributes"},
    {"question": "Which of the following functions is used to get the remainder of a division in Python?", "options": ["divmod()", "remainder()", "mod()", "div()"], "answer": "divmod()"},
    {"question": "How can you create a set in Python?", "options": ["set = {1, 2, 3}", "set = (1, 2, 3)", "set = [1, 2, 3]", "set = (1:2, 2:3)"], "answer": "set = {1, 2, 3}"},
    {"question": "What is the output of print(3 ** 2) in Python?", "options": ["6", "9", "3", "None"], "answer": "9"},
    {"question": "Which method can be used to remove an element from a set in Python?", "options": ["remove()", "del()", "pop()", "discard()"], "answer": "remove()"},
    {"question": "What is the purpose of the lambda function in Python?", "options": ["To create a named function", "To create an anonymous function", "To create a class", "To define a loop"], "answer": "To create an anonymous function"},
    {"question": "Which of the following is the correct syntax for a dictionary in Python?", "options": ["dict = (1: 'apple', 2: 'banana')", "dict = [1: 'apple', 2: 'banana']", "dict = {1: 'apple', 2: 'banana'}", "dict = <1: 'apple', 2: 'banana'>"], "answer": "dict = {1: 'apple', 2: 'banana'}"},
    {"question": "What is the result of 5 // 2 in Python?", "options": ["2", "2.5", "3", "5"], "answer": "2"},
    {"question": "What is the use of the 'break' statement in Python?", "options": ["To exit the loop", "To skip the loop", "To continue the loop", "To define a function"], "answer": "To exit the loop"},
    {"question": "Which of the following is the correct way to create a tuple in Python?", "options": ["tuple = (1, 2, 3)", "tuple = [1, 2, 3]", "tuple = {1, 2, 3}", "tuple = <1, 2, 3>"], "answer": "tuple = (1, 2, 3)"}
]

# Shuffle
random.shuffle(questions)

# Quiz Form
score = 0
user_answers = {}
submitted = False

with st.form("quiz_form"):
    for idx, q in enumerate(questions):
        st.subheader(f"Q{idx+1}. {q['question']}")
        selected = st.radio(f"Choose your answer for Q{idx+1}", q["options"], key=f"q_{idx}", index=None)
        user_answers[q["question"]] = selected

    submitted = st.form_submit_button("Submit Quiz")

# After submission
if submitted:
    if not name:
        st.warning("⚠️ Please enter your name before submitting.")
    else:
        st.write("---")
        st.header("📊 Results")
        for idx, q in enumerate(questions):
            user_choice = user_answers[q["question"]]
            if user_choice == q["answer"]:
                st.success(f"✅ Q{idx+1}. {q['question']} — Correct!")
                score += 1
            else:
                st.error(f"❌ Q{idx+1}. {q['question']} — Incorrect. You chose: {user_choice}")
                st.info(f"✔️ Correct answer: {q['answer']}")

        st.markdown(f"## 🏁 Final Score for **{name}**: **{score} / {len(questions)}**")

        if score == len(questions):
            st.balloons()
            st.success("🏆 Perfect score! You’re a Python Pro!")
        elif score >= 14:
            st.info("🎉 Great job! Keep going!")
        elif score >= 10:
            st.warning("🙂 Good effort. Some revision will help.")
        else:
            st.error("📚 Don't worry! Review and try again.")

        # Save result
        result = {
            "Name": name,
            "Score": score,
            "Total": len(questions),
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        df = pd.DataFrame([result])
        try:
            df.to_csv("quiz_results.csv", mode='a', index=False, header=not pd.io.common.file_exists("quiz_results.csv"))
            st.success("✅ Your result has been saved.")
        except Exception as e:
            st.error(f"Error saving result: {e}")

        # PDF Export
        def create_pdf(result_data):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, txt="Python MCQ Quiz Result", ln=True, align='C')
            pdf.ln(10)

            for key, value in result_data.items():
                pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

            pdf.ln(10)
            pdf.set_font("Arial", "I", size=12)
            pdf.cell(200, 10, txt="Prepared by: Syed Mohammad Raza Rizvi", ln=True)
            pdf.cell(200, 10, txt="Governor Sindh IT Initiative Student", ln=True)

            return BytesIO(pdf.output(dest="S").encode("latin1"))

        pdf_data = create_pdf(result)
        st.download_button("Download Result as PDF", data=pdf_data, file_name="quiz_result.pdf", mime="application/pdf")

        if st.button("Refresh Quiz"):
            st.session_state.clear()
            st.experimental_rerun()
