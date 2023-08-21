import step1
import step2
import step3
import streamlit as st

def run_step1(location, place_type, queries):
    result1 = step1.process(location, place_type, queries)
    return result1

#create a function to run step2
def run_step2(message_prompt):
    result2 = step2.process(message_prompt)
    return result2

#create a function to run step3
def run_step3(filename):
    result3 = step3.process(filename)
    return result3

st.title("PhaseLLM Demo")
st.title("Preferences form for your tour location and type of tour")

with st.form('Inputs'):
    location = st.text_input("Location", "Tokyo, Japan")
    place_type = st.text_input("Place type", "Restaurants")
    queries = st.text_area("Search queries", "best japanese restaurants in ginza part of tokyo\n"
                                        "ginza restaurants that only locals know\n"
                                        "tokyo ginza restaurants that are holes in the wall but AMAZING\n"
                                        "unique tokyo ginza restaurants\n"
                                        "tokyo ginza best food\n"
                                        "most unique tokyo (ginza) restaurants\n"
                                        "best tokyo ginza restaurants you can't miss", height=300)
    message_prompt_text = """You are a culinary researcher putting together a food tour. This food tour needs to include the best restaurants from a broader list that has been provided to you. You are going to follow these steps in generating your list:
1. You will be given content to review.
2. Please review the content and simply make a list of all the restaurants mentioned.
3. Each element in the list should ONLY include the (a) restaurant name, and (b) a 5-10 word description of the food they serve.
Please provide the output in the following format for each restauran:
NAME: <restaurant name>
DESCRIPTION: <5-10 words describing the food>
<exactly one line break between each restaurant>"""

    message_prompt = st.text_area("Message Prompt for ChatGPT", value=message_prompt_text, height=300)
    filename = st.text_input("Filename", "restaurants-in-ginza")

    submit = st.form_submit_button('Submit')

if submit:
    result1 = run_step1(location, place_type, queries)
    st.title("Results from step 1")
    st.write(result1)

    result2 = run_step2(message_prompt)  # Add appropriate arguments if needed
    st.title("Results from step 2")
    st.write(result2)

    result3 = run_step3(filename)  # Add appropriate arguments if needed
    st.title("Results from step 3")
    st.write(result3)
