# Nestlé HR Policy Assistant

This is an AI-powered HR Assistant that can answer questions about Nestlé's HR policies using the OpenAI GPT model and Streamlit.

## Features

- Upload and process Nestlé HR policy PDF documents
- Convert document text into vector representations
- Answer user queries using OpenAI's GPT model
- User-friendly chat interface built with Streamlit

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd nestle-hr-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`
   - Alternatively, you can enter your API key directly in the Streamlit interface

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL displayed in the terminal (usually http://localhost:8501)

3. Upload the Nestlé HR policy PDF document using the file uploader in the sidebar

4. Start asking questions about Nestlé's HR policies in the chat interface

## How It Works

1. **Document Processing**: The application uses PyPDFLoader to extract text from the uploaded PDF.

2. **Text Chunking**: The document is split into smaller chunks for efficient processing using CharacterTextSplitter.

3. **Vector Representation**: Text chunks are converted into vector embeddings using OpenAI's embedding model.

4. **Question Answering**: When a user asks a question, the system:
   - Finds the most relevant document chunks using vector similarity
   - Passes these chunks and the question to OpenAI's GPT model
   - Returns the generated answer to the user

## Technical Details

- **Document Loader**: PyPDFLoader from LangChain
- **Text Splitter**: CharacterTextSplitter from LangChain
- **Embeddings**: OpenAIEmbeddings from LangChain
- **Vector Store**: Chroma from LangChain
- **LLM**: ChatOpenAI (GPT-3.5-Turbo) from LangChain
- **UI Framework**: Streamlit

## Requirements

- Python 3.7+
- OpenAI API key

## License

[Include license information here]