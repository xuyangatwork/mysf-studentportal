import streamlit as st
import llm
import json
import sqlit_db

riasec_options = ["R", "I", "A", "S", "E", "C"]

riasec_industries = {
    "R": ["Aerospace", "Built Environment", "Environmental Services", "Energy and Chemicals", 
                  "Food Services", "Logistics", "Landscape", "Marine and Offshore Engineering", 
                  "Precision Engineering", "Public Transport", "Security"],
    "I": ["Architecture", "Healthcare", "Biopharmaceuticals Manufacturing", "Electronics", 
                      "Energy and Chemicals", "Energy and Power", "Information and Communications Technology", 
                      "Marine and Offshore Engineering", "Precision Engineering"],
    "A": ["Advertising", "Architecture", "Arts and Entertainment", "Beauty Services", "Design", 
                 "Landscape", "Media"],
    "S": ["Early Childhood care and education", "Healthcare", "Human Resource", 
               "Public Service (Education)", "Social Service", "Training and Adult Education"],
    "E": ["Advertising", "Air Transport", "Consultancy", "Design", "Finance", 
                     "Hotel and Accommodation Services", "Human Resource", "Legal", "Media", 
                     "Public Service (Education)", "Real Estate", "Retail", "Tourism"],
    "C": ["Aerospace", "Accountancy", "Air Transport", "Finance", "Food Manufacturing", 
                     "Information and Communications", "Insurance", "Legal", "Logistics", 
                     "Real Estate", "Sea Transport", "Wholesale Trade"]}

goal_options = ["Strengthen sustainable food production and security", 
                "Ensure sustainable management of water and sanitation", 
                "Ensure access to cleaner energy sources and address climate change challenges",
                "Promote lifelong learning and inclusive education", 
                "Leverage technology to foster an innovative economy",
                "Uplift society and enable social mobility", 
                "Provide quality and accessible healthcare", 
                "Uphold fairness and justice for all",
                "Promote inclusivity and support for individuals with disabilities"]

def get_prompt():

    if 'system_prompt_date' not in st.session_state:
        st.session_state.system_prompt_date = ""
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = ""

    # Read prompt from DB
    conn = sqlit_db.connect_db()
    system_prompt_db = sqlit_db.read_prompt(conn)
    if system_prompt_db:
        st.session_state.system_prompt_date = system_prompt_db[1]
        st.session_state.system_prompt = system_prompt_db[2]
    else:
        st.error("Please go Prompt Engineering and enter System Prompt first.")
    conn.close()


def poc_page():

    get_prompt()

    inputs = {}

    if 'job_json' not in st.session_state:
        st.session_state.job_json = ""

    # Select RIASEC
    st.subheader("A. Know Yourself")

    # Create a multi-select box for RIASEC categories
    selected_riasec = st.multiselect("Select Your RIASEC:", list(riasec_industries.keys()))
    if selected_riasec:
        selected_riasec_str = ", ".join(selected_riasec)
        inputs['riasec'] = selected_riasec_str

    # Collect industries related to selected RIASEC categories
    related_industries = []
    for category in selected_riasec:
        for industry in riasec_industries[category]:
            related_industries.append(f"{category} - {industry}")

    # Allow user to further select from the related industries
    selected_industry = st.selectbox("Select Related Industries:", related_industries)
    if selected_industry:
        inputs['industry'] = selected_industry.split(' - ', 1)[-1].strip()
    else:
        st.write("Select industries from the list above.")

    #with st.form(key='form_riasec'):
    #    selected_riasec = st.multiselect("Select Your RIASEC:", riasec_options)
    #    st.write("Realistic, Investigative, Artistic, Social, Enterprising, Conventional")
    #    selected_riasec_str = ""
    #    if selected_riasec:
    #        selected_riasec_str = ", ".join(selected_riasec)
    #        inputs['riasec'] = selected_riasec_str

    #    if st.form_submit_button(label='Show Matching Job Roles'):
    #        st.session_state.job_json = llm.get_riasec(selected_riasec_str)

    # Select Goal
    st.subheader("B. Discover Your Purpose & Make A Difference")

    with st.form(key='form_career'):

        if st.session_state.job_json != "":
            try:
                data = json.loads(st.session_state.job_json)
                job_titles = [job['job_title'] for job in data['jobs']]
                selected_job = st.selectbox("Select Your Interested Job:", job_titles)
                if selected_job:
                    inputs['job'] = selected_job
            except json.JSONDecodeError as e:
                st.error(f"Failed to decode JSON: {e}")
        
        selected_goal = st.selectbox("Select your purpose statement:", goal_options)
        if selected_goal:
            selected_goal_str = ", ".join(selected_goal)
            inputs['goal'] = selected_goal_str
        my_own_goal = st.text_input("I have my own purpose statement ... (optional)")
        if my_own_goal:
            inputs['ownGoal'] = my_own_goal
        else:
            inputs['ownGoal'] = ""

        if st.form_submit_button(label='Check Now'):
            llm.single_openai_call(inputs)

def prompt_page():

    get_prompt()

    with st.form(key='form_prompt'):
        text_input = st.text_area("Enter System Prompt", height=500, value=st.session_state.system_prompt)
        st.write(f"Last updated date: {st.session_state.system_prompt_date}")

        if st.form_submit_button(label='Submit'):
            st.session_state.system_prompt = text_input
            
            # Update prompt in DB
            conn = sqlit_db.connect_db()
            sqlit_db.upsert_prompt(conn, text_input)
            conn.close()

            st.success("Update successfully")

    st.subheader("Prompt Engineering CO-STAR Framework")
    st.write('''Context (C): Providing background information helps the LLM understand the specific scenario.''')
    st.write('''Objective (O): Clearly defining the task directs the LLM’s focus.''')
    st.write('''Style (S): Specifying the desired writing style aligns the LLM response.''')
    st.write('''Tone (T): Setting the tone ensures the response resonates with the required sentiment.''')
    st.write('''Audience (A): Identifying the intended audience tailors the LLM’s response to be targeted to an audience.''')
    st.write('''Response (R): Providing the response format, like text or json, ensures the LLM outputs, and help build pipelines.''')
    
    st.subheader('System Prompt (Google Doc)')
    st.write('https://docs.google.com/document/d/153foOpYYHNO_oYcR-RwY1-ceUEyZlkCPrTe2rQnONWU/edit?usp=sharing')

def check_password():
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True

    # Create a password input field
    password = st.text_input("Enter password", type="password")
    
    # Define the correct password (you can also retrieve this from a secure source)
    correct_password = st.secrets["PASSWORD"]

    # Check the entered password
    if password == correct_password:
        st.session_state.password_correct = True
        st.success("Password correct! You can now access other pages.")
        return True
    elif password:
        st.error("Incorrect password. Please try again.")
        return False
