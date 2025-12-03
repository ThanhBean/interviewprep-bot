# interviewprep-bot

# 🤖 AI Interview Coach Chatbot (Hugging Face API)

## Project Overview
This Python-based chatbot simulates a job interview coach. It asks behavioral questions and uses the **Mistral-7B-Instruct** large language model (LLM), accessed via the Hugging Face Serverless Inference API, to provide real-time, constructive feedback on the user's answers. The bot analyzes the structure and content of the user's response, acting as a supportive but strict mentor.

### Prerequisites
1.  **A Hugging Face Account:** Create a free account to generate an Access Token.
2.  **Access Token:** Generate a token with **Inference** permissions (either "Write" or "Fine-grained: Inference").

### Installations
1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Securely Configure API Key:**
    * Create a file named **`.env`** in the root directory.
    * Paste your token inside, ensuring the variable name is correct:
        ```env
        HUGGINGFACEHUB_API_TOKEN=hf_XXXXXXXXXXXXXXXXXXXXXXXXXXX
        ```
Execute the main script from your terminal:
```bash
python chatbot.py
