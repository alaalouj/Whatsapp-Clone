# WhatsApp Clone

_Note: Replace "WhatsApp Clone" with your preferred project name once defined._

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Infrastructure](#project-infrastructure)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Description

This project is an academic endeavor undertaken at **Galatasaray University** for the course **"Systèmes et Applications Répartis"** (Distributed Systems and Applications). The objective is to develop a **WhatsApp Clone**, a real-time chat application that emulates the core functionalities of WhatsApp. This application leverages modern technologies to facilitate seamless communication between users in real-time.

## Features

- **User Registration and Authentication**

  - Create a new user account with a unique username and email.
  - Secure login using JWT (JSON Web Tokens).

- **Real-Time Chat**

  - Send and receive messages instantly without page reloads.
  - Support for one-on-one conversations.

- **User Management**

  - View a list of registered users.
  - Select a user to start a conversation.

- **WebSocket Integration**

  - Real-time updates for incoming messages and new users.
  - Efficient handling of multiple concurrent connections.

- **Dockerized Deployment**
  - Simplified setup and deployment using Docker and Docker Compose.

## Technologies Used

- **Backend:**

  - **Python** with **FastAPI** for building the RESTful API and WebSocket endpoints.
  - **PostgreSQL** for the relational database.
  - **Kafka** for message streaming and real-time data handling.
  - **SQLAlchemy** for ORM (Object-Relational Mapping).

- **Frontend:**

  - **Flask** for rendering templates and handling client-side logic.
  - **JavaScript** for managing WebSocket connections and dynamic DOM updates.

- **DevOps:**
  - **Docker** for containerizing the application components.
  - **Docker Compose** for orchestrating multi-container deployments.

## Installation

Follow these steps to set up and run the project locally:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/alaalouj/Whatsapp-Clone.git
   cd whatsapp-clone
   ```

2. **Set Up Environment Variables**

   Create a `.env` file in the `backend` directory with the following variables:

   ```env
   POSTGRES_USER=your_postgres_username
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_DB=your_postgres_db
   KAFKA_BROKER=kafka:9092
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   BACKEND_URL=http://localhost:8000
   API_URL=http://backend:8000
   FLASK_SECRET_KEY=supersecretkey
   ```

3. **Build and Start the Containers**

   ```bash
   docker-compose up --build -d
   ```

4. **Access the Application**

   Open your browser and navigate to `http://localhost:8080` to access the frontend.

## Usage

1. **Register a New User**

   - Navigate to the registration page.
   - Provide a unique username, email, and password.
   - Submit the form to create a new account.

2. **Login**

   - Enter your registered username and password.
   - Upon successful authentication, you will be redirected to the conversations page.

3. **Start Chatting**
   - Select a contact from the sidebar.
   - Type your message in the input field and click "Send".
   - Messages will appear in the conversation window in real-time.

## Project Infrastructure

### Architecture Diagram

Below is a high-level overview of the project's architecture:
+---------------------+ +--------------------+ +----------------+
| Frontend | | Backend | | Database |
| (Flask + JS) | <-> | (FastAPI + Kafka) | <-> | (PostgreSQL) |
+---------------------+ +--------------------+ +----------------+

### Component Breakdown

- **Frontend (Flask + JavaScript):**

  - Handles user interactions, rendering templates, and managing WebSocket connections.
  - Communicates with the backend via RESTful APIs and WebSockets.

- **Backend (FastAPI + Kafka):**

  - Exposes RESTful API endpoints for user authentication, message handling, and user management.
  - Manages WebSocket connections for real-time communication.
  - Utilizes Kafka for message streaming and processing.

- **Database (PostgreSQL):**

  - Stores user information, messages, and other persistent data.

- **Docker & Docker Compose:**
  - Containerizes all components, ensuring consistency across different environments.
  - Orchestrates the multi-container setup, managing dependencies and networking.

## Project Structure

whatsapp-clone/
├── backend/
│ ├── app/
│ │ ├── routes/
│ │ │ ├── **init**.py
│ │ │ ├── auth.py
│ │ │ ├── messages.py
│ │ │ ├── users.py
│ │ │ └── websocket.py
│ │ ├── **init**.py
│ │ ├── config.py
│ │ ├── db.py
│ │ ├── dependencies.py
│ │ ├── kafka_utils.py
│ │ ├── main.py
│ │ ├── models.py
│ │ ├── schemas.py
│ │ ├── security.py
│ │ └── websocket_manager.py
│ ├── Dockerfile
│ ├── requirements.txt
│ └── wait-for-it.sh
├── frontend/
│ ├── app/
│ │ ├── templates/
│ │ │ ├── base.html
│ │ │ ├── conversations.html
│ │ │ ├── login.html
│ │ │ └── register.html
│ │ ├── **init**.py
│ │ └── main.py
│ ├── Dockerfile
│ └── requirements.txt
├── docker-compose.yml
├── .env
└──

### Directory and File Descriptions

- **backend/**: Contains all backend-related code and configurations.

  - **app/**: Main application package.
    - **models.py**: Defines the database models using SQLAlchemy.
    - **schemas.py**: Defines Pydantic schemas for request and response validation.
    - **routes/**: Contains all API route modules.
      - \***\*init**.py\*\*:
      - **auth.py**: Handles user registration, login, and authentication-related endpoints.
      - **messages.py**: Manages message sending and conversation retrieval.
      - **websocket.py**: Manages WebSocket connections and real-time communication.
      - **users.py**:
    - \***\*init**.py\*\*:
    - **config.py**:
    - **main.py**:
    - **websocket_manager.py**: Implements the `ConnectionManager` for handling WebSocket connections.
    - **db.py**: Sets up the database connection and session management.
    - **security.py**: Handles password hashing, token creation, and verification.
    - **kafka_utils.py**: Contains utilities for interacting with Kafka (producing messages).
    - **dependencies.py**: Defines common dependencies used across routes (e.g., getting current user ID).
  - **Dockerfile**: Docker configuration for building the backend container.
  - **requirements.txt**: Lists Python dependencies for the backend.
  - **wait-for-it.sh**:

- **frontend/**: Contains all frontend-related code and configurations.

  - **app/**: Main application package.
    - \***\*init**.py\*\*:
    - **main.py**: Flask application entry point, handling routes and rendering templates.
    - **templates/**: Contains HTML templates.
      - **base.html**: Base template with common HTML structure.
      - **login.html**: User login page.
      - **register.html**: User registration page.
      - **conversations.html**: Main chat interface.
  - **Dockerfile**: Docker configuration for building the frontend container.
  - **requirements.txt**: Lists Python dependencies for the frontend.

- **docker-compose.yml**: Defines and orchestrates multi-container Docker applications, including backend, frontend, PostgreSQL, Kafka, and Zookeeper.

- **.env**: Environment variables for configuring the application. Should include sensitive information like database credentials and secret keys.

- **README.md**: Project documentation (this file).

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**

   ```bash
   git clone https://github.com/alaalouj/Whatsapp-Clone.git
   cd whatsapp-clone
   ```

2. **Create a New Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**

4. **Commit Your Changes**

   ```bash
   git commit -m "Add your descriptive commit message"
   ```

5. **Push to the Branch**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software as per the terms of the license.

## Contact

For any inquiries or support, please contact us

---

_Thank you for using the WhatsApp Clone project! We hope it serves as a valuable learning tool for understanding distributed systems and real-time applications._
