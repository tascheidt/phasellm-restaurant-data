"""
Welcome to a PhaseLLM demo app where we build a spreadsheet of restaurant recommendations for you!

There are three parts to this process, separated into three separate files:
1. step1.py -- uses PhaseLLM's WebSearchAgent to get a list of URLs to crawl and crawls those URLs
2. step2.py -- use an LLM to extract and aggregate restaurant information
3. step3.py -- saves the outputs into an Excel file

This file is step2.py

Questions? Please reach out: w --at-- phaseai --dot-- com
"""

import json
import time
import pandas as pd
from phasellm.llms import *
from collections import defaultdict
from apikeys import *

###
# Your API keys and settings.

# OpenAI API Key
openai_key = openai_key

# Google API Key for using its web search components + a search ID
# Our search ID has a global web context; i.e., we simply use the base Google search offering
google_api_key = google_api_key
search_id = search_id


###
# Message prompts used by the LLM to extract information

# Prompt #1: will be used for the system prompt (i.e., general instructions)
message_prompt_1 = """You are a culinary researcher putting together a food tour. This food tour needs to include the best restaurants from a broader list that has been provided to you. You are going to follow these steps in generating your list:
1. You will be given content to review.
2. Please review the content and simply make a list of all the restaurants mentioned.
3. Each element in the list should ONLY include the (a) restaurant name, and (b) a 5-10 word description of the food they serve. Do not duplicate any restaurants in the list. 

Please provide the output in the following format for each restauran:
NAME: <restaurant name>
DESCRIPTION: <5-10 words describing the food>
<exactly one line break between each restaurant>
"""

# Prompt #2: sends the specific site content
message_prompt_2 = """Here is the information to review.
------------------------------------------
{title}

{content} 
"""

###
# Helper functions


def parse_lines(content, results=None):
    """
    This function parses the output above into a set of dictionary objects and appends it back into the results object.
    """
    if results is None:
        results = {}

    lines = content.split("\n")
    for i in range(len(lines)):
        line = lines[i].strip()
        if line and line.startswith("NAME"):
            restaurant_name = line[6:].strip()
            
            if restaurant_name not in results:
                results[restaurant_name] = {
                    "name": restaurant_name,
                    "description": "",
                    "count": 1,
                }
            else:
                results[restaurant_name]["count"] += 1
            
            if i + 1 < len(lines):
                desc = lines[i + 1][13:].strip()
            else:
                # Handle the case where i + 1 is out of range
                desc = ""

            if desc:
                results[restaurant_name]["description"] += f"- {desc}\n"

    return results



###
# Set up the ChatBot flow with the prompts above.

cp = ChatPrompt(
    [
        {"role": "system", "content": message_prompt_1},
        {"role": "user", "content": message_prompt_2},
    ]
)
llm = OpenAIGPTWrapper(openai_key, model="gpt-3.5-turbo-16k")
cb = ChatBot(llm)

# Load results from step1.py
results = []
with open("search_minca.json", "r") as reader:
    results_ = reader.read()
    results = json.loads(results_)["results"]

# Parse the results from step1.py

parsed = {}
ctr_r = 1

for r in results:
    # Helper print() statements to show where we're at.
    print(ctr_r)
    ctr_r += 1
    print(r["title"])

    # Use the PhaseLLM ChatBot object to fill in our prompt with the specific content we crawled.
    cb.messages = cp.fill(content=r["content"], title=r["title"])

    # Send and process the content using the ChatBot approach above.
    try:
        response = cb.resend()
    except:
        # Sometimes we have a very long amount of text, so we might get an error above. In this case, we simply limit the content to the first 10,000 characters. You can get a lot more fancy here!
        print("Error, likely due to length of content. Trying shorter content.")
        cb.messages = cp.fill(content=r["content"][0:10000], title=r["title"])
        response = cb.resend()

    parsed = parse_lines(response, parsed)

    # We sleep for 30 seconds to avoid overloading the ChatGPT API.
    print("Complete. Waiting for next piece of content...")
    time.sleep(30)

# Save results to JSON.
with open("parsed_minca.json", "w") as writer:
    writer.write(json.dumps(parsed))
