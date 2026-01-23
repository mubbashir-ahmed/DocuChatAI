# DocuChatAI

An advanced document-based AI chatbot API that integrates **AWS Kendra** for enterprise search and **OpenAI's ChatGPT** for consensus generation and natural language synthesis. Built with **FastAPI** for high performance and scalability.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Kendra-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-ChatGPT-412991?style=for-the-badge&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

## 📋 Features

- **Hybrid Intelligence** - Combines AWS Kendra's document search with ChatGPT's reasoning.
- **Consensus Generation** - Aggregates multiple source documents into a single coherent answer.
- **FastAPI Framework** - High-performance API with automatic interactive documentation (Swagger).
- **Robust Logging** - Centralized daily CSV logging for auditing and debugging.
- **Rate Limiting** - Built-in protection against abuse (default: 10 requests/minute per IP).
- **Enterprise Ready** - Singleton service patterns and comprehensive configuration management.

## 🛠️ Architecture

1. **AWS Kendra Search**
   - Deep search across enterprise document repositories.
   - Confidence-weighted result extraction.

2. **OpenAI Synthesis**
   - Intelligent consensus building from multiple text snippets.
   - Natural language generation for user-friendly responses.

## 📁 Project Structure

```
DocuChatAI/
├── src/
│   ├── api.py           # FastAPI application entry point
│   ├── main.py          # Core orchestration logic
│   ├── services/        # AWS and OpenAI integration modules
│   ├── models/          # Pydantic models for request/response
│   ├── configs/         # Environment configuration
│   └── utils/           # Shared utilities (logging, etc.)
├── tests/               # Unit and integration tests
├── .env.example         # Template for environment variables
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- AWS Account (with Kendra Index set up)
- OpenAI API Key

### Installation & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/mubbashir-ahmed/DocuChatAI.git
   cd DocuChatAI
   ```

2. **Configure Environment**
   - Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the API**
   ```bash
   uvicorn src.api:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

## 🛠️ Technologies Used

- **Python / FastAPI** - Core application framework
- **AWS Kendra** - Enterprise search and document retrieval
- **OpenAI API** - Consensus generation and synthesis
- **Boto3** - AWS SDK for Python
- **SlowAPI** - Rate limiting for FastAPI
- **Pandas** - Efficient CSV logging management

## 📸 Preview

### API Documentation (Swagger UI)
Visit `http://127.0.0.1:8000/docs` to interact with the API directly.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Contributors

- **Mubbashir Ahmed** (Author & Maintainer)
  GitHub: [@mubbashir-ahmed](https://github.com/mubbashir-ahmed)

- **Mohammed2372**
  Github: [@Mohammed2372](https://github.com/Mohammed2372)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request. Please [read the contributing guidelines](CONTRIBUTING.md).

## ⭐ Show Your Support

⭐ If you find this project helpful, please consider giving it a star!
