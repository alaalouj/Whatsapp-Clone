# WhatsApp Clone


## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Description

The objective of this project is to develop a **WhatsApp Clone**, a real-time chat application that emulates the core functionalities of WhatsApp.

## Features

- **User Registration and Authentication**

- **Real-Time Chat**

- **Contact List**

- **Dockerized Deployment**

## Installation

Follow these steps to set up and run the project locally:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/alaalouj/Whatsapp-Clone.git
   cd whatsapp-clone
   ```

2. **Set Up Environment Variables**

   Create a `.env` file in the directory with the following variables:

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

3. **Build and Start**

   ```bash
   docker-compose up --build -d
   ```
  (It might take a little time)
  
4. **Access the application**

   Open your browser and navigate to `http://localhost:8080` to start to use the app.


## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software as per the terms of the license.

## Contact

For any requests or support, please contact us: https://github.com/Ouass77ck https://github.com/alaalouj

---
