
import sqlite3
import streamlit as st
import time
import pandas as pd
conn = sqlite3.connect('KnowledgeBase.db')
cursor = conn.cursor()

st.set_page_config(page_title="Foodstuff Inventory Management Consultant",page_icon="🧊",layout="wide" )


def read_question():
    cursor.execute("""
            SELECT *
            FROM Questions
            WHERE isSelected = 0
            ORDER BY ID ASC
            LIMIT 1
            """ )
    return cursor.fetchone()

with st.sidebar:
    st.header("Foodstuff Inventory Management Menu")
    menu_selection = st.radio("Menu:", ("Foodstuff Inventory Management", "Knowledge Base"))


if menu_selection == "Knowledge Base":
    # Create a form
    st.title("Insert Data Collection ")
    with st.form(key="my_form"):
        # Text inputs with labels
        Question = st.text_input(label="Question:")
        Answer = st.text_input(label="Reply:")
        
        Right = st.text_input(label="Right reply:")
        st.write("use sign :red[-] for many Right reply ex: Yes-no")
        Conclusion = st.text_input(label="Inference:")

        # Submit button
        submitted = st.form_submit_button(label="Store")

    # Process form submission
    if submitted:
        st.write("Submitted Data")
        Questions = [
            (Question,Answer,Right,Conclusion,0),
        ]
        cursor.executemany("""INSERT INTO Questions (Question,Reply,Rightreply,Inference,isSelected) 
                           VALUES  (?, ?, ?, ?, ?)""", Questions)

        conn.commit()
    cursor.execute("SELECT * FROM Questions")

    # Fetch all rows and column names
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # Create a pandas DataFrame
    df = pd.DataFrame(data, columns=columns)
    df

if menu_selection == "Foodstuff Inventory Management":

    st.title(":blue[Foodstuff Inventory Management Consultant]")
    st.subheader("Type :red['relode'] to relode the session :balloon:")
    messages = st.container(height=500)
    data = read_question()

    if 'my_list' not in st.session_state:
        st.session_state['my_list'] = []
    for item in st.session_state['my_list']:
        messages.chat_message("user").write(f"Consultant: {item}")
    if data:

        messages.chat_message("user").write(f":green[Consultant]: {str(data[1])} ex: {str(data[2])}")

    else :
        Conclusion = cursor.execute("SELECT * FROM AnswersX").fetchall()
        if Conclusion:
            
            messages.chat_message("user").write(f":green[Consultant]: Conclusion :")
            for items in Conclusion:
                messages.chat_message("user").write(f":green[Consultant]: {items[0]}.")
        else:
            messages.chat_message("user").write(f":green[Consultant]: can not get answer or tell you advise.")

    col1, col2 = st.columns([7, 1])
    with col1:
        
        user_input = st.text_input("Say something")
    with col2:
        st.write("")
        st.write("")
        submit_button = st.button("Send")

    if submit_button :  # Button clicked
        if  user_input in "relode":
            cursor.execute("""
                UPDATE Questions
                SET isSelected = 0
            
                """)
            cursor.execute("DELETE FROM AnswersX")
            # Commit the changes to the database
            conn.commit()
            st.session_state.clear()
            progress_bar = st.progress(0)
            for i in range(50):
                progress_bar.progress(i)
                time.sleep(0.01) 
            st.experimental_rerun()
        elif user_input not in str(data[2]):
            
            messages.chat_message("user").write(f"Sorry, that's not quite right. Try again. The answer should be related to: {str(data[1])}")

        else:
            messages.chat_message("assistant").write(user_input)
            st.session_state['my_list'].append(f"{str(data[1])} :- {user_input}")
            # Get further user input after answering correctly

            cursor.execute("""
                UPDATE Questions
                SET isSelected = 1
                WHERE ID = ?
                """, (data[0],))

            # Commit the changes to the database
            conn.commit()
            print(data[3].split('-'))
            if user_input in data[3].split('-') :
                sql = "INSERT INTO AnswersX (Answers) VALUES (?)"
                cursor.execute(sql, (data[4],))
                conn.commit()

            next_prompt = st.text("Inference")
            progress_bar = st.progress(0)
            for i in range(50):
                progress_bar.progress(i)
                time.sleep(0.01) 
            st.experimental_rerun()
        





