# Ask a PDF API

## Repository Structure
```
ask_a_pdf_api/
│── LICENSE
│── README.md
│── docker-compose.yml
│── agent/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── agent.py
│   ├── uploads/  
```

## Description
This project is a Flask-based API that allows users to upload PDFs, query stored PDFs, and utilize an open-source LLM (Mistral) for answering questions based on stored information.

## Setup and Installation
### Prerequisites
- Docker
- Docker Compose

### Running the Application
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/ask_a_pdf_api.git
   cd ask_a_pdf_api
   ```
2. Build and start the containers:
   ```sh
   docker-compose up --build
   ```
3. The API will be available at `http://localhost:5000`

## API Endpoints
### Upload a PDF
**POST** `/upload_pdf`
- Uploads a PDF file and extracts text.

### Ask a Question
**POST** `/ask`
- Sends a question to the LLM, retrieving a response.

### Query Database
**POST** `/query_db`
- Queries MongoDB for stored questions and answers.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Visal API Overview

![alt text](https://github.com/syntaxai-lab/ask_a_pdf_api/blob/main/Screenshot%202025-02-05%20at%207.27.02%E2%80%AFPM.png?raw=true)

	•	Resource: Describes the functionality of each endpoint.
	•	URI: The path to access the resource.
	•	Method: The HTTP method used (e.g., POST).
	•	Parameters: Input data required for the endpoint to function.
	•	Status Code: The response codes indicating success (200: OK) or failure (e.g., 301: No query provided).
