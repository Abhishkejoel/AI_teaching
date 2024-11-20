# AI-Powered Teaching Assistant

Welcome to the **AI-Powered Teaching Assistant** project! This application integrates multiple AI-driven tools to enhance the learning experience for students. It features four main bots:

1. **Summary Bot**: Summarizes content from YouTube videos, audio files, or PDF documents.
2. **Doubt Solving Bot**: Answers questions based on the provided content.
3. **Quiz Generation Bot**: Creates quizzes to test comprehension.
4. **Notes Generation Bot**: Generates comprehensive lecture notes and PowerPoint presentations.

Access the live application [here](https://studyscribe.framer.ai/).

## Table of Contents
- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Usage Guide](#usage-guide)
- [Technologies Used](#technologies-used)
- [Contact](#contact)

## Features

- **Summary Bot**: Quickly generate concise summaries from various input types.
- **Doubt Solving Bot**: Get instant answers to specific questions related to the content.
- **Quiz Generation Bot**: Test your understanding with automatically generated quizzes.
- **Notes Generation Bot**: Create detailed lecture notes and downloadable PowerPoint presentations.

## Setup and Installation

To run this project locally, follow these steps:

1. **Clone the Repository**
    ```sh
    git clone https://github.com/AbhishekTadepalli/AI-powered-teaching-assistant.git
    cd AI-powered-teaching-assistant
    ```

2. **Create and Activate a Virtual Environment**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3. **Install Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**
    - Create a `.env` file in the root directory.
    - Add your OpenAI API key:
        ```env
        OPENAI_API_KEY=your_openai_api_key
        ```

5. **Run the Application**
    ```sh
    streamlit run app.py
    ```

## Usage Guide

### Summary Bot
1. Select **YouTube URL**, **Audio File**, or **PDF Document**.
2. Provide the input.
3. Click **Generate Summary** to view the summarized content.

### Doubt Solving Bot
1. Use the Summary Bot to generate a transcript.
2. Enter your question related to the content.
3. Click **Get Answer** to receive an AI-generated response.

### Quiz Generation Bot
1. Generate a transcript using the Summary Bot.
2. Click **Generate Quiz** to receive multiple-choice questions.
3. Complete the quiz and view your results with explanations.

### Notes Generation Bot
1. Select your input type and provide the content.
2. Click **Generate Notes** to create detailed lecture notes.
3. Download the generated PowerPoint presentation for offline use.

## Technologies Used

- **Streamlit**: Interactive web application framework.
- **OpenAI API**: Natural language processing for summarization, Q&A, and more.
- **YouTube Transcript API**: Extracting transcripts from YouTube videos.
- **Pydub**: Audio file manipulation.
- **PyPDF2**: PDF text extraction.
- **python-pptx**: PowerPoint presentation generation.

## Contact

For any questions or support, feel free to reach out:

- **GitHub**: [Abhishek Tadepalli](https://github.com/AbhishekTadepalli)
- **Email**: abhishekjoel58@gmail.com

---

*Enhance your learning experience with AI-powered tools!*

