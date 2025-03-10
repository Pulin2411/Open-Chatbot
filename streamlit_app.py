import streamlit as st
import openai

# Initialize OpenAI client
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set the title of the chatbot
st.title("NOC Support ChatBot")

# Initialize chat history in session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get response from OpenAI
def get_response(user_input):
    system_message = {
        "role": "system",
        "content": (
            "You are a helpful and professional assistant. "
            "Do NOT discuss or respond to queries about sex, vulgarity, drugs, alcohol, gender bias, or caste. "
            "If asked about such topics, politely refuse and steer the conversation to positive, professional, and informative subjects."
        )
    }
    
    # Include chat history along with system message
    messages = [system_message] + st.session_state.messages + [{"role": "user", "content": user_input}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )

    return response["choices"][0]["message"]["content"]

# Display existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if user_input := st.chat_input("I am not suppose to annswer this type of question..."):
    # Display user message
    st.chat_message("user").markdown(user_input)

    # Get bot response
    bot_response = get_response(user_input)

    # Display bot message
    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # Store messages in session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
