# Async Notification Service

An asynchronous, production-style notification system built using **FastAPI**, **RabbitMQ**, and **SQLite**. This service supports email, SMS, and push notifications with retry handling, dead-letter queue (DLQ), and notification tracking via REST API.

---

## 🚀 Features

- 📬 **Send Notifications** (Email, SMS, Push)
- 🐇 **Queue-based Processing** with RabbitMQ
- 🔁 **Retry Mechanism** for transient failures
- 📦 **Dead Letter Queue** for failed notifications
- 🧾 **SQLite Logging** of all notification attempts
- 🔍 **Traceable UUIDs** for each notification
- 🧪 **Test Coverage** with `pytest`
- 💌 **Real Email Delivery** using Mailtrap
- 🌐 **REST API** to fetch notification logs

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (async), SQLModel (SQLite)
- **Queue**: RabbitMQ, aio-pika
- **SMTP**: Mailtrap (via aiosmtplib)
- **Testing**: Pytest, HTTPX (async client)
- **Deployment**: Docker-ready (coming soon)

---

## 📦 Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/py-async-notification-service.git
cd py-async-notification-service
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
Copy `.env.example` and fill with your RabbitMQ and SMTP (Mailtrap) credentials:
```bash
cp .env.example .env
```

### 5. Run the app
Start the FastAPI app:
```bash
uvicorn app.main:app --reload
```

Start the worker (in another terminal):
```bash
python -m app.workers.worker
```

---

## 🔁 Testing Notifications

### Send Notification
Open Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

Use the `/notify/` endpoint:
```json
{
  "type": "email",
  "to": "test@example.com",
  "subject": "Hello",
  "body": "This is a test notification."
}
```

### View Notification Log
Use `/logs/{id}` to fetch the status of a notification by its UUID.

---

## 🧪 Run Tests
```bash
pytest tests/
```

---

## 🐳 Docker Support
- Production-ready Dockerfile for the FastAPI API
- Dedicated Dockerfile for the background worker
- docker-compose.yml to run the full stack locally (API + Worker + RabbitMQ)
