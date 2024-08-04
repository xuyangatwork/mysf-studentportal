import streamlit as st
import llm
import json
import sqlit_db

riasec_options = ["R", "I", "A", "S", "E", "C"]
goal_options = ["Strengthen sustainable food production and security", 
                "Ensure sustainable management of water and sanitation", 
                "Ensure access to cleaner energy sources and address climate change challenges",
                "Promote lifelong learning and inclusive education", 
                "Leverage technology to foster an innovative economy",
                "Uplift society and enable social mobility", 
                "Provide quality and accessible healthcare", 
                "Uphold fairness and justice for all",
                "Promote inclusivity and support for individuals with disabilities"]

def poc_page():

    inputs = {}

    if 'job_json' not in st.session_state:
        st.session_state.job_json = ""

    # Select RIASEC
    st.subheader("A. Know Yourself")
    with st.form(key='form_riasec'):
        selected_riasec = st.multiselect("Select Your RIASEC:", riasec_options)
        st.write("Realistic, Investigative, Artistic, Social, Enterprising, Conventional")
        selected_riasec_str = ""
        if selected_riasec:
            selected_riasec_str = ", ".join(selected_riasec)
            inputs['riasec'] = selected_riasec_str

        if st.form_submit_button(label='Show Matching Job Roles'):
            st.session_state.job_json = llm.get_riasec(selected_riasec_str)
    

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
        
        selected_goal = st.selectbox("Select you goal:", goal_options)
        if selected_goal:
            selected_goal_str = ", ".join(selected_goal)
            inputs['goal'] = selected_goal_str
        my_own_goal = st.text_input("I have my own goal ... (optional)")
        if my_own_goal:
            inputs['ownGoal'] = my_own_goal
        else:
            inputs['ownGoal'] = ""

        if st.form_submit_button(label='Check Now'):
            llm.single_openai_call(inputs)

def prompt_page():

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
    conn.close()

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