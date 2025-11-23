# 🌾 KisanAI - Smart Farming Assistant

> An AI-powered farming assistant providing weather forecasts, market prices, soil health monitoring, expense tracking, and intelligent crop management.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Optimized-success.svg)](SYSTEM_STATUS.md)

---

## ✅ System Status

**Latest Review:** Completed ✅  
**Dependencies:** Up-to-date ✅  
**Code Quality:** Linted & Formatted with Ruff ✅

- ✅ All security vulnerabilities addressed.
- ✅ Frontend and backend dependencies updated to latest stable versions.
- ✅ Codebase linted and formatted for consistency.
- ✅ Project startup and setup scripts have been fixed and simplified.

---

## 📑 Table of Contents

- [System Status](#-system-status)
- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Environment Setup](#-environment-setup)
- [Development](#-development)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [Documentation](#-documentation)

---

## 🎯 Overview

KisanAI is a full-stack web application designed to help farmers make data-driven decisions. It combines real-time weather data, market price tracking, soil health monitoring, and AI-powered insights to optimize farming operations.

**Key Highlights:**
- 🌦️ Real-time weather forecasts with 5-day predictions
- 💰 Live market price tracking across multiple states
- 🌱 Soil health analysis with NPK levels and pH monitoring
- 📊 Financial tracking with income/expense analytics
- 🌾 Crop management with growth stage tracking
- 🤖 AI-powered chatbot for farming advice
- 📱 Responsive design - works on all devices
- 🔐 Secure authentication with JWT tokens

---

## ✨ Features

### 🌦️ Weather Forecasts
- Current weather conditions (temperature, humidity, wind speed)
- 5-day weather forecast with daily predictions
- City-based weather search
- Intelligent caching (6-hour TTL)

### 💰 Market Prices
- Real-time crop prices from government APIs
- State-wise price comparison
- Price history visualization (7-day trend)
- Modal, minimum, and maximum price tracking

### 🌱 Soil Health Monitoring
- NPK (Nitrogen, Phosphorus, Potassium) level tracking
- pH level monitoring with status indicators
- Moisture percentage tracking
- Historical soil reports

### 📊 Financial Management
- Income and expense tracking
- Category-based expense organization
- Crop-linked transactions
- Visual analytics with charts:
  - Timeline chart (income vs expenses)
  - Category breakdown (pie/bar chart)
- Profit/loss calculation

### 🌾 Crop Management
- Add and track multiple crops
- Plot/field assignment
- Growth stage tracking (Sown → Germination → Vegetative → Flowering → Fruiting → Harvest Ready → Harvested)
- Sowing date recording
- Quick crop status overview

### 🤖 AI-Powered Features
- **Smart Dashboard Insights**: AI-generated recommendations based on weather and crop data
- **Chatbot Assistant**: Ask farming questions and get AI-powered answers
- Intent detection for context-aware responses
- LLM integration via OpenRouter (Llama 3.1)

### 🔐 Authentication & Security
- User registration and login
- JWT token-based authentication
- Password hashing with bcrypt
- Protected API routes
- Session persistence

---

## 🛠️ Tech Stack

### Frontend
- **React 19** - UI library
- **React Router DOM 7** - Client-side routing
- **TanStack React Query 5** - Server state management & caching
- **TailwindCSS 3** - Utility-first CSS framework
- **Framer Motion 12** - Animation library
- **Axios** - HTTP client
- **Lucide React** - Icon library
- **Recharts** - Chart visualization
- **Vite 7** - Build tool and dev server

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy 2.0+** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **Uvicorn** - ASGI server
- **Pydantic 2.0+** - Data validation
- **python-jose** - JWT token handling
- **passlib[bcrypt]** - Password hashing
- **httpx** - Async HTTP client for external APIs

### External APIs
- **OpenWeatherMap** - Weather data
- **India Government Open Data** - Market prices
- **OpenRouter** - LLM integration (Llama 3.1)

### Development Tools
- **Git** - Version control
- **Docker** - Containerization
- **Ruff** - Python Linter and Formatter
- **ESLint** - JavaScript Linter

---

## 📁 Project Structure

```
kisan-ai/
│
├── backend/                    # Python FastAPI Backend
│   ├── main.py                # FastAPI app entry point
│   ├── config.py              # Settings & configuration
│   ├── requirements.txt       # Python dependencies
│   ├── seed.py                # Database seeding script
│   │
│   ├── routes/                # API endpoints
│   ├── services/              # Business logic
│   ├── models/                # Data models
│   ├── middleware/            # Custom middleware
│   ├── utils/                 # Helper functions
│   │
│   ├── data/                  # Runtime data (gitignored)
│   │   └── kisanai.db        # SQLite database
│   │
│   └── logs/                  # Application logs (gitignored)
│
├── frontend/                   # React Frontend
│   ├── index.html             # HTML entry point
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   │
│   └── src/
│       ├── main.jsx           # React entry point
│       ├── App.jsx            # Router configuration
│       │
│       ├── pages/             # Route components
│       ├── components/        # Reusable components
│       ├── context/           # React Context
│       ├── hooks/             # Custom hooks
│       ├── services/          # API services
│       └── lib/               # Libraries
│
├── docs/                       # Extended documentation
│
├── setup.bat                   # Windows setup script
├── start.bat                   # Start services (Windows)
└── stop.bat                    # Stop services (Windows)
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Node.js 16+** and npm
- **Git**

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/kisan-ai.git
cd kisan-ai
```

### 2. Run Setup Script
This script will create a Python virtual environment, install all backend and frontend dependencies, and seed the database with demo data.

```bash
setup.bat
```

### 3. Environment Configuration
Create a `backend/.env` file by copying `backend/.env.example`. Then, add your API keys.

```bash
# Required API Keys in backend/.env
OPENWEATHER_API_KEY=your-openweather-api-key
OPENROUTER_API_KEY=your-openrouter-api-key
```

### 4. Start Application
```bash
start.bat
```
This will start the backend on `http://localhost:8000` and the frontend on `http://localhost:3000`, and open the application in your browser.

**Demo Credentials:**
- Username: `demo`
- Password: `demo123`

---

## 💻 Development

### Backend Development

**Run in development mode:**
```bash
# From project root
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000
```

**Linting and Formatting:**
```bash
# Check for issues
.\.venv\Scripts\ruff.exe check backend

# Format code
.\.venv\Scripts\ruff.exe format backend
```

### Frontend Development

**Run development server:**
```bash
cd frontend
npm run dev
```

**Lint code:**
```bash
cd frontend
npm run lint
```

---

## 🐳 Deployment

See [docs/DEPLOYMENT_CHECKLIST.md](docs/DEPLOYMENT_CHECKLIST.md) for the complete deployment guide.

---

## 📡 API Documentation

**API docs are available at http://localhost:8000/docs** after starting the backend server.

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📚 Documentation

- **[UI/UX Guide](docs/UI_UX_GUIDE.md)**
- **[Backend Guide](docs/BACKEND_GUIDE.md)**
- **[React Query Guide](docs/REACT_QUERY_GUIDE.md)**
- **[Deployment Checklist](docs/DEPLOYMENT_CHECKLIST.md)**
