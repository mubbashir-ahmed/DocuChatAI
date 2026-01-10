# DocuChatAI

An advanced document-based AI chatbot API that integrates **AWS Kendra** for enterprise search and **OpenAI's ChatGPT** for consensus generation and natural language synthesis. Built with **FastAPI** for high performance and scalability.

## 🚀 Features

*   **Hybrid Intelligence**: Combines AWS Kendra's document search with ChatGPT's reasoning.
*   **FastAPI Framework**: High-performance, easy-to-use API with automatic interactive documentation.
*   **Robust Logging**: Centralized daily CSV logging for auditing and debugging.
*   **Rate Limiting**: Built-in protection against abuse (default: 10 requests/minute per IP).
*   **Enterprise Ready**: Singleton service patterns, comprehensive configuration management, and type safety.
*   **Open Source**: MIT Licensed.

## 🛠️ Architecture

*   **`src/api.py`**: FastAPI application entry point.
*   **`src/main.py`**: Core orchestration logic connecting Kendra and OpenAI's ChatGPT.
*   **`src/services/`**: Integration modules for AWS Kendra (`aws_kendra.py`) and OpenAI's ChatGPT (`openai.py`).
*   **`src/configs/`**: Configuration management using `.env` files.
*   **`tests/`**: Unit tests for logic and endpoints.

## 📋 Prerequisites

*   Python 3.9+
*   AWS Account (with Kendra Index set up)
*   OpenAI API Key

## ⚙️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/AIChatbot.git
    cd DocuChatAI
    ```

2.  **Create a virtual environment**:
    ```bash
    py -m venv .venv
    .venv\Scripts\activate  # Windows
    # source .venv/bin/activate  # Linux/Mac
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Copy `.env.example` to `.env` and fill in your credentials.
    ```bash
    cp .env.example .env
    ```
    
    Update the following variables in `.env`:
    *   `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY`
    *   `AWS_KENDRA_INDEX_ID`
    *   `OPENAI_API_KEY`

## ▶️ Usage

Start the server using Uvicorn:

```bash
uvicorn src.api:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### API Documentation
Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

### Example Request

**POST** `/chatbot`

```json
{
  "query": "What are the safety protocols?"
}
```

## 🧪 Testing

Run unit tests using `pytest`:

```bash
pytest tests/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Mubbashir Ahmed
