import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# import OpenAI
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', "Key not found") # for local api key
client = OpenAI(
  api_key=OPENAI_API_KEY
)

# .pdf file
# I've try using library like PyPDF2 or PyMuPDF to convert pdf to text, but the symbols and format is hard to convert as I thought.
# So I do some correction manually and with ChatGPT, after convert pdf to text by PyMuPDF.
pdf_file = """
{
  "a": {
    "#1": {
      "wrong": "I hope you all have a enjoyable stay.",
      "correct": "I hope you all have an enjoyable stay.",
      "instruction": "Always use 'an' (NOT 'a') before a word beginning with a vowel sound: ‘an egg’, ‘an envelope’."
    },
    "#2": {
      "wrong": "My husband is doing a MSc in civil engineering.",
      "correct": "My husband is doing an MSc in civil engineering.",
      "instruction": "Use 'an' (NOT 'a') before an abbreviation that begins with a vowel sound: ‘an MSc’, ‘an MP’."
    },
    "#3": {
      "wrong": "Sometimes it is difficult to live a honest life.",
      "correct": "Sometimes it is difficult to live an honest life.",
      "instruction": "Use 'an' (NOT 'a') before words beginning with 'h' when the 'h' is not pronounced: ‘an honour’, ‘an hour’."
    }
  },
  "a/an": {
    "#1": {
      "wrong": "The child had been a deaf since birth.",
      "correct": "The child had been deaf since birth.",
      "instruction": "Do not use 'a/an' before an adjective (e.g., ‘deaf’, ‘British’) unless the adjective is followed by a noun."
    }
  },
  "abandon": {
    "#1": {
      "wrong": "Since capital punishment was abandoned, the crime rate has increased.",
      "correct": "Since capital punishment was abolished, the crime rate has increased.",
      "instruction": "Abandon = give up a plan, activity, or attempt to do something without being successful."
    },
    "#2": {
      "wrong": "It is difficult to reach abandoned places such as small country villages.",
      "correct": "It is difficult to reach remote places such as small country villages.",
      "instruction": "Abandoned = left forever by the owners or occupiers."
    }
  },
  "ability": {
    "#1": {
      "wrong": "These machines are destroying our ability of thinking.",
      "correct": "These machines are destroying our ability to think.",
      "instruction": "Use 'ability to do sth' (NOT 'of doing')."
    },
    "#2": {
      "wrong": "I want to improve my ability of reading.",
      "correct": "I want to improve my reading ability.",
      "instruction": "Use 'reading/writing/teaching/acting ability'."
    },
    "#3": {
      "wrong": "I want to improve my ability of English.",
      "correct": "I want to improve my ability in English.",
      "instruction": "Use 'ability in a language or subject'."
    }
  },
  "able": {
    "#1": {
      "wrong": "One man is able to destroy the whole world.",
      "correct": "One man is capable of destroying the whole world.",
      "instruction": "If someone is able to do something, they can do it and it is not unusual or surprising if they do it."
    },
    "#2": {
      "wrong": "There are so many places to visit in London that I'm not able to decide where to go.",
      "correct": "There are so many places to visit in London that I can’t decide where to go."
    },
    "#3": {
      "wrong": "In some countries you are not able to drink until you are 21.",
      "correct": "In some countries you can’t drink until you are 21."
    },
    "#4": {
      "wrong": "Technology has made them able to grow their own food.",
      "correct": "Technology has enabled them to grow their own food.",
      "instruction": "Enable = make someone able to do something."
    }
  },
  "about": {
    "#1": {
      "wrong": "I am always delighted when I receive a letter from you. About the party on December 26th, I shall be very pleased to attend.",
      "correct": "I am always delighted when I receive a letter from you. With regard to the party on December 26th, I shall be very pleased to attend."
    },
    "#2": {
      "wrong": "It all depends on how different the new country is from your own. About myself, I haven’t experienced any culture shock but then this is my second trip to the States.",
      "correct": "It all depends on how different the new country is from your own. In my own case, I haven’t experienced any culture shock but then this is my second trip to the States."
    },
    "#3": {
      "wrong": "I was about leaving when the telephone rang.",
      "correct": "I was about to leave when the telephone rang."
    }
  },
  "above": {
    "#1": {
      "wrong": "There were above a hundred people in the crowd.",
      "correct": "There were over a hundred people in the crowd.",
      "instruction": "Do not use 'above' with numbers (unless referring to points on a scale)."
    },
    "#2": {
      "wrong": "I like to stay at home on a Sunday, as I’ve said above.",
      "correct": "I like to stay at home on a Sunday, as I’ve already said.",
      "instruction": "Above is used in formal writing to refer to something that has been mentioned earlier."
    },
    "#3": {
      "wrong": "Taking all the above into account, one could say that tourism does more harm than good.",
      "correct": "Taking all the above arguments into account, one could say that tourism does more harm than good.",
      "instruction": "Instead of using 'the above' as a loose reference to something mentioned earlier, make the reference more precise by using 'the above + noun' or 'the + noun + above'."
    }
  },
  "above all": {
    "#1": {
      "wrong": "He likes reading, above all novels.",
      "correct": "He likes reading, especially novels.",
      "instruction": "'Above all' means ‘most importantly’."
    },
    "#2": {
      "wrong": "This year English is above all my most important subject.",
      "correct": "This year English is by far my most important subject.",
      "instruction": "With a superlative form ('the most important'), use 'by far'."
    },
    "#3": {
      "wrong": "Where would you like to go above all?",
      "correct": "Where would you like to go most of all?",
      "instruction": "When you mean ‘more than anywhere/anything/anyone else’, use 'most of all' or 'the most'."
    }
  },
  "abovementioned": {
    "#1": {
      "wrong": "I would be grateful if you would send it to the address abovementioned.",
      "correct": "I would be grateful if you would send it to the abovementioned address."
    },
    "instruction": "'Above-mentioned' comes before the noun."
  },
  "abroad": {
    "#1": {
      "wrong": "Since I was small, I’ve always wanted to go to abroad.",
      "correct": "Since I was small, I’ve always wanted to go abroad."
    },
    "#2": {
      "wrong": "I would like to continue my studies in abroad.",
      "correct": "I would like to continue my studies abroad."
    },
    "instruction": "Go/live/be abroad (WITHOUT 'to', 'at', 'in', etc.)."
  },
  "absent": {
    "#1": {
      "wrong": "It’s a pity that you were absent from the training session.",
      "correct": "It’s a pity that you missed the training session."
    },
    "#2": {
      "wrong": "It’s a pity that you were absent from the training session.",
      "correct": "It’s a pity that you weren’t at the training session."
    },
    "instruction": "'Be absent' = not be present at something that you are officially supposed to attend."
  },
  "absolutely": {
    "#1": {
      "wrong": "It is absolutely important that you see a doctor immediately.",
      "correct": "It is very important that you see a doctor immediately."
    },
    "#2": {
      "wrong": "It is absolutely important that you see a doctor immediately.",
      "correct": "It is absolutely essential that you see a doctor immediately."
    },
    "instruction": "See Note at VERY."
  },
  "accept": {
    "#1": {
      "wrong": "The company will not accept to buy new machines.",
      "correct": "The company will not agree to buy new machines.",
      "instruction": "You accept someone’s advice, opinion, or suggestion, BUT you agree to do something."
    },
    "#2": {
      "wrong": "The driver did not accept me to get on the bus.",
      "correct": "The driver did not allow me to get on the bus."
    },
    "#3": {
      "wrong": "We can’t accept a motorway to be built through our town.",
      "correct": "We can’t allow a motorway to be built through our town."
    },
    "instruction": "You allow/permit someone to do something, or let them do it."
  }
}
"""

# Initialize session_state
if "data" not in st.session_state:
    st.session_state.data = []

# full page
st.set_page_config(
    layout="wide",
)

# webpage title
st.title("Spellchecker")
st.header("Description")
st.markdown("""
            This is a APP create by streamlit and interact with openai api.  
            Type any words or sentences below, return correction of input!
            """)

# seperate input, output with columns
col1, col2 = st.columns([2, 3])

# get user input
with col1:
    st.subheader("Your input")
    with st.form(key="input", clear_on_submit=True):
        input = st.text_input("Type words or sentences")
        submit = st.form_submit_button("Submit")

# display output
with col2:
    st.subheader("Correction")
    tab1, tab2 = st.tabs(["Correction", "Correction history"]) # create tab for correction history
    
    # display correciton
    with tab1:
        if submit and input:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"""
                        You are a english teacher, correct words or sentences from user input.
                        Please related to {pdf_file}, and Longman dictionary of common errors to learn about how to response.
                        The input will only be words or sentences waiting for your correction, don't do any further.
                        Here is some output format you must do!:
                        If correct, return in format: "Correct; "input" is the correct spelling!" or "Correct; There is no misspelling!"
                        If uncorrect, return in format: "Wrong; The correction is: "output".
                        You should use ...
                        """
                    },
                    {"role": "user", "content": f"Here is the words/sentences: '{input}'"}
                ],
            )
            
            response = completion.choices[0].message.content.split(";") # seperate assistant response
            print(response)
            # display assistant response
            if response[0] == "Correct":
                st.success(response[1])
            else:
                st.error(response[1])
             
             # store data   
            new_data = {"input": input, "response": response[1]}
            st.session_state.data.append(new_data)
            
        elif submit:
          st.error("Please provide some words or sentences for correction.")
    
    # display correction history       
    with tab2:
        df = pd.DataFrame(st.session_state.data)
        st.write("History:")
        st.write(df)
