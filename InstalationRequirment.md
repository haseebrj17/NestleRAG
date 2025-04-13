# Nestlé HR Policy Assistant - Final Instructions

I've fixed the errors in the code:

1. Updated the OpenAI API usage to match the newer SDK version
2. Fixed the text extraction return value issue
3. Added more error checking

## Installation Instructions

1. **Create your requirements.txt file**:

```
streamlit==1.26.0
openai>=1.2.0
python-dotenv==1.0.0
PyPDF2==3.0.1
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Save the app code as app.py**

4. **Run the application**:

```bash
streamlit run app.py
```

## Using the Application

1. **Enter your OpenAI API key** in the sidebar input field

2. **Upload your Nestlé HR policy PDF document** using the file uploader

3. **Ask questions** about the HR policies in the chat input at the bottom

## How the Application Works

1. **Document Processing**:
   - The PDF is loaded and text is extracted
   - Text is split into manageable chunks
   - Chunks are stored in the session state

2. **Question Answering**:
   - OpenAI extracts key terms from the user's question
   - The app finds document chunks containing those key terms
   - Relevant chunks are sent to OpenAI along with the question
   - OpenAI generates an answer based on the relevant context

## Troubleshooting

- If you see "Could not extract text from the uploaded PDF", your PDF might be scanned or image-based. Try a different PDF.

- If you get API errors, check that your API key is correct and has sufficient credits.

- If the application seems slow, it may be because it's processing a large PDF. Be patient during the initial processing.

## Notes for Your Project Submission

This application satisfies all the requirements for your Nestlé HR Policy Assistant project:

1. ✅ PDF document processing
2. ✅ Text extraction and chunking
3. ✅ Context retrieval using keyword extraction
4. ✅ Integration with OpenAI's GPT model
5. ✅ Clean user interface with Streamlit
6. ✅ Chat-based interaction
7. ✅ Proper error handling

The code is also well-documented and easy to understand, making it suitable for your course submission.