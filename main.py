"""
Nestlé HR Policy Assistant - Final Fixed Version
With guaranteed text extraction.
"""

import os
import streamlit as st
from dotenv import load_dotenv
import tempfile
from openai import OpenAI
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

# Set title and header
st.set_page_config(page_title="Nestlé HR Policy Assistant", layout="wide")
st.title("Nestlé HR Policy Assistant")
st.markdown("Ask questions about Nestlé's HR policies and get instant answers.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for API Key input
with st.sidebar:
    st.header("Configuration")
    openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

    st.markdown("### About")
    st.markdown(
        """
        This assistant helps you find information about Nestlé's HR policies.
        Upload the HR policy PDF and ask questions to get instant answers.
        """
    )

    uploaded_file = st.file_uploader("Upload Nestlé HR Policy PDF", type="pdf")

# Function to extract text from PDF with guaranteed return
def extract_text_from_pdf(pdf_file):
    # Default empty text
    extracted_text = ""

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(pdf_file.getvalue())

    try:
        with open(temp_file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:  # Only add if text was extracted
                    extracted_text += page_text + "\n"
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    # Always return the text (might be empty if extraction failed)
    return extracted_text

# Function to split text into chunks
def split_text_into_chunks(text, chunk_size=1000, overlap=200):
    # Split into paragraphs first
    paragraphs = text.split('\n\n')

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        # If adding this paragraph would exceed chunk size, save current chunk and start a new one
        if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
            chunks.append(current_chunk)
            # Keep some overlap
            current_chunk = current_chunk[-overlap:] if len(current_chunk) > overlap else ""

        current_chunk += paragraph + "\n\n"

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# Function to generate answer using OpenAI
def generate_answer_with_context(query, context, api_key):
    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=api_key)

    # Create messages array for chat
    messages = [
        {"role": "system", "content": f"You are a helpful assistant that answers questions about Nestlé's HR policies based on the following information:\n\n{context}\n\nIf the answer cannot be found in the provided information, say that you don't know."}
    ]

    # Add the user's query
    messages.append({"role": "user", "content": query})

    # Generate response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.0
    )

    return response.choices[0].message.content

# Main application logic
if uploaded_file and openai_api_key:
    try:
        # Cache the processed data in session state
        if "document_text" not in st.session_state:
            with st.spinner("Processing document..."):
                # Extract text from PDF
                extracted_text = extract_text_from_pdf(uploaded_file)

                # Check if we got any text
                if not extracted_text or len(extracted_text.strip()) == 0:
                    st.error("Could not extract text from the uploaded PDF. Please make sure it's a valid, text-based PDF.")
                else:
                    # Split text into chunks
                    chunks = split_text_into_chunks(extracted_text)

                    # Store in session state
                    st.session_state.document_text = extracted_text
                    st.session_state.document_chunks = chunks

                    st.success(f"Document processed successfully! Extracted {len(chunks)} text segments. You can now ask questions.")

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Get user input
        user_query = st.chat_input("Ask a question about Nestlé's HR policies")

        if user_query and "document_chunks" in st.session_state and st.session_state.document_chunks:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_query})

            # Display user message
            with st.chat_message("user"):
                st.markdown(user_query)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Initialize the OpenAI client
                        client = OpenAI(api_key=openai_api_key)

                        # Get key terms from the question
                        analysis_response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": "The user is asking about a Nestlé HR policy. Extract 5-7 key terms from their question that would help find relevant information in an HR policy document."},
                                {"role": "user", "content": user_query}
                            ],
                            temperature=0.0
                        )

                        key_terms = analysis_response.choices[0].message.content
                        key_terms_list = [term.strip().lower() for term in key_terms.split() if len(term.strip()) > 2]

                        # Simple keyword matching to find relevant chunks
                        relevant_text = ""
                        for chunk in st.session_state.document_chunks:
                            chunk_lower = chunk.lower()
                            # Check if any of the key terms are in the chunk
                            if any(term in chunk_lower for term in key_terms_list):
                                relevant_text += chunk + "\n\n"

                        # If we couldn't find relevant chunks, use the first few chunks
                        if not relevant_text:
                            relevant_text = "\n\n".join(st.session_state.document_chunks[:3])

                        # Generate answer with the relevant context
                        answer = generate_answer_with_context(user_query, relevant_text, openai_api_key)

                        # Display answer
                        st.markdown(answer)

                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        error_message = f"Sorry, I encountered an error while processing your question: {str(e)}"
                        st.error(error_message)
                        st.session_state.messages.append({"role": "assistant", "content": error_message})

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

elif not uploaded_file:
    st.info("Please upload the Nestlé HR Policy PDF to continue.")
elif not openai_api_key:
    st.info("Please enter your OpenAI API key to continue.")