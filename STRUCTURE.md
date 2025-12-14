# 📁 KisanAI Project Structure

## Overview
This document describes the clean, organized structure of the KisanAI project after refactoring.

---

## 📂 Root Directory

```
kisan-ai/
├── backend/              # Python FastAPI Backend
├── frontend/             # React Frontend
├── docs/                 # Project documentation
├── scripts/              # Setup and utility scripts
├── .gitignore           # Git ignore rules
├── README.md            # Main documentation
├── CHANGELOG.md         # Version history
├── STRUCTURE.md         # This file
└── MANUAL_TESTING_INSTRUCTIONS.md
```

---

## 🐍 Backend Structure

```
backend/
├── main.py               # FastAPI application entry point
├── config.py             # Configuration and settings
├── requirements.txt      # Python dependencies
├── ruff.toml            # Linting configuration
├── seed.py              # Database seeding script
│
├── routes/              # API endpoint definitions
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── chatbot.py       # AI chatbot routes
│   ├── crops.py         # Crop management routes
│   ├── dashboard.py     # Dashboard data routes
│   ├── expenses.py      # Financial tracking routes
│   ├── prices.py        # Market price routes
│   ├── soil.py          # Soil health routes
│   └── weather.py       # Weather data routes
│
├── services/            # Business logic layer
│   ├── __init__.py
│   ├── ai_service.py    # LLM integration
│   ├── crop_service.py  # Crop management logic
│   ├── expense_service.py
│   ├── price_service.py # Market price fetching
│   ├── soil_service.py  # Soil data processing
│   └── weather_service.py
│
├── models/              # Data models
│   ├── __init__.py
│   ├── database.py      # SQLAlchemy models
│   └── schemas.py       # Pydantic schemas
│
├── middleware/          # Custom middleware
│   ├── __init__.py
│   └── performance.py   # Performance monitoring
│
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── helpers.py       # General helpers & auth
│   ├── validators.py    # Input validation
│   └── response.py      # Standardized responses
│
├── data/                # Runtime data (gitignored)
│   └── kisanai.db       # SQLite database
│
└── logs/                # Application logs (gitignored)
    └── app.log
```

### Backend Architecture

**Layered Design:**
- **Routes:** Handle HTTP requests, input validation
- **Services:** Business logic, external API calls
- **Models:** Database schema and data validation
- **Utils:** Reusable helper functions

---

## ⚛️ Frontend Structure

```
frontend/
├── index.html           # HTML entry point
├── package.json         # Node.js dependencies
├── vite.config.js       # Vite build configuration
├── tailwind.config.js   # TailwindCSS configuration
├── postcss.config.js    # PostCSS configuration
├── .eslintrc.json       # ESLint rules
│
├── src/
│   ├── main.jsx         # React entry point
│   ├── App.jsx          # Main app component & routing
│   ├── index.css        # Global styles
│   │
│   ├── pages/           # Page components (routes)
│   │   ├── Dashboard.jsx
│   │   ├── Crops.jsx
│   │   ├── Finances.jsx
│   │   ├── Weather.jsx
│   │   ├── Prices.jsx
│   │   ├── Soil.jsx
│   │   ├── Chat.jsx
│   │   ├── Login.jsx
│   │   └── Register.jsx
│   │
│   ├── components/      # Reusable UI components
│   │   ├── Layout.jsx
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   ├── Select.jsx
│   │   ├── Modal.jsx
│   │   ├── EmptyState.jsx
│   │   ├── InsightReport.jsx
│   │   ├── PageTransition.jsx
│   │   ├── ProtectedRoute.jsx
│   │   ├── SkeletonLoader.jsx
│   │   └── ErrorBoundary.jsx
│   │
│   ├── hooks/           # Custom React hooks
│   │   ├── useApi.js    # React Query hooks
│   │   ├── useAuth.js   # Authentication hook
│   │   └── useMediaQuery.js
│   │
│   ├── context/         # React Context providers
│   │   └── AuthContext.jsx
│   │
│   ├── services/        # API service layer
│   │   └── api.js       # Axios instance & API calls
│   │
│   ├── lib/             # Third-party library configs
│   │   └── queryClient.js  # React Query configuration
│   │
│   ├── config/          # Application configuration
│   │   ├── api.config.js    # API endpoints
│   │   └── query.config.js  # React Query settings
│   │
│   ├── constants/       # App-wide constants
│   │   └── index.js     # States, crops, stages, defaults
│   │
│   └── utils/           # Utility functions
│       └── dateUtils.js # Date formatting helpers
│
└── public/              # Static assets
    └── vite.svg
```

### Frontend Architecture

**Component-Based Design:**
- **Pages:** Full-page views mapped to routes
- **Components:** Reusable UI building blocks
- **Hooks:** Custom React Query hooks for data fetching
- **Config:** Centralized configuration management
- **Services:** API communication layer

---

## 📚 Documentation Structure

```
docs/
├── BACKEND_GUIDE.md          # Backend best practices
├── REACT_QUERY_GUIDE.md      # React Query patterns
├── UI_UX_GUIDE.md            # UI/UX standardization
└── DEPLOYMENT_CHECKLIST.md  # Production deployment guide
```

---

## 🛠️ Scripts Structure

```
scripts/
├── setup.bat     # Initial project setup (Windows)
├── start.bat     # Start both services (Windows)
└── stop.bat      # Stop all services (Windows)
```

**Usage:**
```bash
# First time setup
scripts\setup.bat

# Start development servers
scripts\start.bat

# Stop all servers
scripts\stop.bat
```

---

## 🔑 Key Design Principles

### Backend
1. **Layered Architecture:** Routes → Services → Models
2. **Separation of Concerns:** Business logic in services, not routes
3. **Type Safety:** Type hints on all functions
4. **Error Handling:** Consistent error responses
5. **Validation:** Input validation in utils/validators.py

### Frontend
1. **Component Reusability:** Shared UI components
2. **State Management:** React Query for server state
3. **Configuration:** Centralized in config/ folder
4. **Code Splitting:** Lazy-loaded pages
5. **Performance:** Memoization, optimized queries

---

## 🚀 Getting Started

1. **Setup:** Run `scripts\setup.bat`
2. **Configure:** Copy `.env.example` files and add API keys
3. **Start:** Run `scripts\start.bat`
4. **Access:** 
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

---

## 📦 Key Files

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI app initialization |
| `backend/config.py` | Environment config & logging |
| `frontend/src/App.jsx` | React router setup |
| `frontend/src/services/api.js` | Axios instance & API calls |
| `frontend/src/hooks/useApi.js` | React Query hooks |
| `frontend/src/config/api.config.js` | API endpoints config |
| `frontend/src/config/query.config.js` | React Query settings |

---

## 🔄 Data Flow

### Frontend Request Flow
```
User Action → Component → Hook (useApi.js) → Service (api.js) → Backend API
                    ↓
              React Query Cache
                    ↓
              Component Re-render
```

### Backend Request Flow
```
HTTP Request → Route → Service → External API / Database → Response
                ↓
         Middleware (Auth, Performance)
```

---

## 🧪 Testing Structure (Future)

```
backend/tests/           # Backend tests
  ├── test_routes/
  ├── test_services/
  └── test_models/

frontend/tests/          # Frontend tests
  ├── components/
  ├── hooks/
  └── pages/
```

---

## 🔐 Environment Variables

### Backend (.env)
```
OPENWEATHER_KEY=your_key
INDIA_GOV_API_KEY=your_key
OPENROUTER_API_KEY=your_key
SECRET_KEY=your_secret
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
VITE_DEFAULT_CITY=Pune
VITE_DEFAULT_STATE=Maharashtra
VITE_DEFAULT_CROP=Wheat
```

---

## 📊 Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend Framework | React 19 | UI library |
| State Management | TanStack Query 5 | Server state |
| Styling | TailwindCSS 3 | Utility CSS |
| Build Tool | Vite 7 | Fast bundler |
| Backend Framework | FastAPI 0.121+ | Web API |
| Database | SQLite/PostgreSQL | Data storage |
| ORM | SQLAlchemy 2.0+ | Database abstraction |
| Authentication | JWT | Secure auth |
| External APIs | OpenWeather, India Gov, OpenRouter | Data sources |

---

## 🎯 Code Quality Standards

✅ **Python:** Follow PEP 8, use type hints  
✅ **JavaScript:** ESLint rules enforced  
✅ **Components:** PropTypes for type checking  
✅ **Naming:** Descriptive, consistent conventions  
✅ **Comments:** Document complex logic  
✅ **Error Handling:** Graceful degradation  

---

## 📈 Performance Optimizations

- **Frontend:** React Query caching, lazy loading
- **Backend:** Response caching, async operations
- **Database:** Indexed queries, connection pooling
- **Network:** Request deduplication, stale-while-revalidate

---

**Last Updated:** November 30, 2025  
**Version:** 2.0 (Post-Refactor)  
**Status:** Production Ready ✅
