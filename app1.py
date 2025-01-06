
# from groq import Groq

# client = Groq(api_key="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")

# query="using titanic.csv answer, what was the distribution of male and female survivors?"

# completion = client.chat.completions.create(
#     model="llama-3.3-70b-versatile",
#     messages=[
#         {
#             "role": "user",
#             "content": query 
#         },
       
#     ],
#     temperature=0,
#     max_tokens=1024,
#     top_p=0,
#     stream=True,
#     stop=None,
# )




# for chunk in completion:
#     print(chunk.choices[0].delta.content or "", end="")

import streamlit as st
import pandas as pd
from groq import Groq

# Initialize the Groq client with your API key
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Streamlit app
st.title("Titanic Dataset Query App")
st.write("Upload your Titanic dataset and ask questions about it!")

# File upload
uploaded_file = st.file_uploader("Upload Titanic CSV File", type=["csv"])

if uploaded_file is not None:
    # Display the uploaded file
    st.write("Dataset preview:")
    titanic_data = pd.read_csv(uploaded_file)
    st.dataframe(titanic_data)

    # Convert the dataset to CSV format as a string
    csv_context = titanic_data.to_csv(index=False)

    # Query input
    query = st.text_area(
        "Enter your query about the Titanic dataset:",
        placeholder="e.g., What was the distribution of male and female survivors?",
    )

    # Submit button
    if st.button("Ask AI"):
        if query.strip():
            with st.spinner("Generating response..."):
                # Prepare the messages for the model
                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant knowledgeable about analyzing CSV data.",
                    },
                    {
                        "role": "user",
                        "content": f"The following dataset is provided as context:\n\n{csv_context}\n\n{query}",
                    },
                ]

                # Generate the completion
                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages,
                        temperature=0,
                        max_tokens=1024,
                        top_p=0,
                        stream=True,
                        stop=None,
                    )

                    # Display the response
                    st.write("**AI Response:**")
                    response = ""
                    for chunk in completion:
                        content = chunk.choices[0].delta.content or ""
                        response += content
                        st.write(content, end="")

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a query before submitting.")
else:
    st.info("Please upload a CSV file to begin.")
