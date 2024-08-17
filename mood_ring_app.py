import streamlit as st
import openai
import os

# Streamlit app
st.title("Mood Ring App")

# User input for the thoughts
user_thoughts = st.text_area("Enter your thoughts:")
text_promt = 'Tell me about my mood if I think about ' + user_thoughts + 'Limit your answer to 900 characters.'


if st.button('Analyze Mood'):
    # Construct the OpenAI API client
    client = openai.OpenAI(
        api_key = os.getenv('OPENAI_API_KEY'),
        organization = os.getenv('OPENAI_ORG_ID'),
        project = os.getenv('OPENAI_PROJECT_ID')
)

    # Generate text response
    text_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a zen monk."
            },
            {
                "role": "user",
                "content": text_promt
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the response content
    text_reply = text_response.choices[0].message.content

    # Display the text response in the Streamlit app
    st.write("### You entered" ,)
    st.write(user_thoughts)
    st.write("### Mood Analysis")
    st.write(text_reply)

    # Generate an image based on the text reply
    image_response = client.images.generate(
        prompt=text_reply,
        n=1,  # Number of images to generate
        size="1024x1024"  # Size of the generated image
    )

    # Extract and display the generated image URL
    image_url = image_response.data[0].url
    st.image(image_url, caption="Generated Image")
    st.write(f"Generated image URL: {image_url}")
