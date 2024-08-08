import streamlit as st
from openai import OpenAI

def metacog_feedback():
    placeholder = st.empty()

    with placeholder:
        inputs = {}
        inputs["question"] = ""
        inputs["text"] = ""

        with st.form("Metacognitive Feedback"):
            question = st.text_input("Question")
            text = st.text_area("Text for analysis")

            submitted = st.form_submit_button("Submit text for feedback")

            if submitted:
                inputs["question"] = question
                inputs["text"] = text
        
    if inputs is not None:
        if inputs["text"] != "" and inputs["question"] != "":
            chat_bot = "gpt-4o"
            #openai_API(inputs, chat_bot)
        else:
            st.warning("You will need to enter both question and text.")

def single_openai_call(inputs):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key = st.secrets["OPENAI_API_KEY"])

    prompt = "My RIASEC: " + inputs['riasec'] + "; My Career Aspirations: " + inputs['industry'] + "; My Goal: " + inputs['goal']
    if inputs['ownGoal'] != "":
        prompt = prompt + inputs['ownGoal']

    stream = client.chat.completions.create(
		model="gpt-4o",
		messages=[
			{"role": "system", "content":st.session_state.system_prompt},
			{"role": "user", "content": prompt},
		],
		temperature=0.5,
		stream=True
	)
    st.subheader("How to Broaden Your Career Aspirations")  
    st.write_stream(stream)

def get_riasec(inputs):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key = st.secrets["OPENAI_API_KEY"])

    system_prompt = prompt = """
        Generate a list including 15 job roles matched based on the RIASEC profile below. 
        Please respond in the following JSON format:
        {
        "jobs": [
            {"job_title": "Job Title 1"},
            {"job_title": "Job Title 2"},
            {"job_title": "Job Title 3"}
        ]
        }
        """
    prompt = "My RIASEC profile is: " + inputs

    completion = client.chat.completions.create(
		model="gpt-4o",
        response_format={ "type": "json_object" },
		messages=[
			{"role": "system", "content": system_prompt},
			{"role": "user", "content": prompt},
		],
		temperature=0.5, #settings option
		#presence_penalty=st.session_state.default_presence_penalty, #settings option
		#frequency_penalty=st.session_state.default_frequency_penalty, #settings option
        stream=False
	)
    return completion.choices[0].message.content
        