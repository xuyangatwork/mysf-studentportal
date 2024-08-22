import streamlit as st
import streamlit_antd_components as sac
import page
import welcome
import sqlit_db


# Define the pages
def page1():
    st.title("ECG Proof-Of-Concept (POC)")

    page.poc_page()

def page2():
    st.title("Prompt Engineering")

    page.prompt_page()
    
def page0():
    st.title("Welcome to ECG Tool POC (v0.1)")

    if page.check_password():
        welcome.welcome_page()

def main():

    # Create DB
    conn = sqlit_db.connect_db()
    sqlit_db.create_table(conn)
    conn.close()

    # Create the menu
    with st.sidebar: #options for sidebar
        st.image("ECG.png")
        selected_menu = sac.menu([
            sac.MenuItem('Welcome'),
            sac.MenuItem('Prototype'),
            sac.MenuItem('Prompt Engineering')
            ], index=0, format_func='title', open_all=True)

    # Display the selected page
    if selected_menu == "Prototype":
        if page.check_password():
            page1()
    elif selected_menu == "Prompt Engineering":
        if page.check_password():
            page2()
    elif selected_menu == "Welcome":
        page0()

if __name__ == "__main__":
	main()
