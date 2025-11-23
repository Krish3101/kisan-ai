# 🚀 KisanAI - Deployment & Production Checklist

> **Purpose:** Pre-deployment checklist, production optimizations, and monitoring setup.

---

## 📋 Pre-Deployment Checklist

### ✅ Code Quality

- [x] All features tested and working
- [x] No console.log statements in production code
- [ ] Remove all debugger statements
- [ ] Code follows style guidelines (UI_UX_GUIDE.md, BACKEND_GUIDE.md)
- [ ] All imports are used (no unused imports)
- [x] React imports removed where unnecessary (JSX transform)
- [ ] Type hints on all backend functions
- [ ] Docstrings on all service functions

### ✅ Security

- [ ] **CRITICAL:** Change SECRET_KEY in backend/config.py
- [ ] **CRITICAL:** Use environment variables for all secrets
- [ ] Add JWT token expiration (currently permanent)
- [ ] Implement refresh tokens
- [ ] Add rate limiting on API endpoints
- [ ] Enable HTTPS in production
- [ ] Configure CORS properly (restrict origins)
- [ ] Validate all user inputs (Pydantic schemas)
- [ ] SQL injection protection (using SQLAlchemy ORM ✅)
- [ ] Password requirements enforced
- [ ] Remove demo user creation script from production

### ✅ Environment Variables

Create `.env` file (NEVER commit to git):

```bash
# Backend (.env in root or backend/)
SECRET_KEY=your-super-secret-key-change-this-in-production
OPENWEATHER_API_KEY=your-openweathermap-api-key
OPENROUTER_API_KEY=your-openrouter-api-key
INDIA_GOV_API_KEY=your-india-gov-api-key
DATABASE_URL=sqlite:///./backend/data/kisan.db  # Or PostgreSQL URL

# Production settings
CORS_ORIGINS=https://your-domain.com
DEBUG=false
LOG_LEVEL=INFO

# Optional: Email settings (for future features)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

Create `.env.local` for frontend (if needed):

```bash
VITE_API_URL=http://localhost:8000
# In production: https://api.your-domain.com
```

### ✅ Database

- [x] SQLAlchemy models properly defined
- [x] Relationships configured correctly
- [x] Indexes on frequently queried columns
- [ ] Database migration strategy planned
- [ ] Backup strategy in place
- [ ] Consider PostgreSQL for production (instead of SQLite)

**Migration from SQLite to PostgreSQL:**

1. Install psycopg2:
   ```bash
   pip install psycopg2-binary
   ```

2. Update config.py:
   ```python
   DATABASE_URL = os.getenv(
       "DATABASE_URL", 
       "postgresql://user:password@localhost/kisanai"
   )
   ```

3. Use Alembic for migrations:
   ```bash
   pip install alembic
   alembic init alembic
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

### ✅ API Configuration

- [x] All routes properly documented
- [x] Proper HTTP status codes used
- [x] Error responses standardized
- [ ] Add request validation
- [ ] Add response models
- [ ] API versioning (e.g., /api/v1/)
- [ ] Rate limiting configured
- [ ] Add API documentation (FastAPI auto-docs at /docs)

### ✅ Frontend Build

- [ ] Optimize bundle size
- [ ] Remove unused dependencies
- [ ] Tree-shake unused code
- [ ] Minify CSS/JS
- [ ] Optimize images
- [ ] Add service worker for PWA (optional)
- [ ] Configure proper caching headers

**Build optimization (vite.config.js):**

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          charts: ['recharts'],
          query: ['@tanstack/react-query'],
          motion: ['framer-motion'],
        },
      },
    },
    chunkSizeWarningLimit: 1000, // KB
    sourcemap: false, // Disable source maps in production
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

---

## 🔧 Production Optimizations

### Backend Optimizations

1. **Use Uvicorn with workers:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

2. **Add production ASGI server (gunicorn + uvicorn):**
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

3. **Enable Gzip compression:**
   ```python
   # main.py
   from fastapi.middleware.gzip import GZipMiddleware
   
   app.add_middleware(GZipMiddleware, minimum_size=1000)
   ```

4. **Add database connection pooling:**
   ```python
   # config.py
   from sqlalchemy import create_engine
   from sqlalchemy.pool import QueuePool
   
   engine = create_engine(
       DATABASE_URL,
       poolclass=QueuePool,
       pool_size=10,
       max_overflow=20,
       pool_pre_ping=True,  # Verify connections before use
   )
   ```

5. **Cache static responses:**
   ```python
   from fastapi.responses import Response
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def get_crop_types():
       return ["Wheat", "Rice", "Corn", "Cotton", "Sugarcane"]
   
   @app.get("/crop-types")
   async def crop_types():
       types = get_crop_types()
       return Response(
           content=json.dumps(types),
           media_type="application/json",
           headers={"Cache-Control": "public, max-age=3600"}
       )
   ```

### Frontend Optimizations

1. **Lazy load routes:**
   ```javascript
   import { lazy, Suspense } from 'react';
   import SkeletonLoader from './components/SkeletonLoader';
   
   const Dashboard = lazy(() => import('./pages/Dashboard'));
   const Crops = lazy(() => import('./pages/Crops'));
   const Finances = lazy(() => import('./pages/Finances'));
   
   // In App.jsx
   <Suspense fallback={<SkeletonLoader />}>
     <Routes>
       <Route path="/" element={<Dashboard />} />
       <Route path="/crops" element={<Crops />} />
       <Route path="/finances" element={<Finances />} />
     </Routes>
   </Suspense>
   ```

2. **Optimize images:**
   ```bash
   # Install image optimizer
   npm install vite-plugin-imagemin -D
   ```
   
   ```javascript
   // vite.config.js
   import viteImagemin from 'vite-plugin-imagemin';
   
   export default defineConfig({
     plugins: [
       react(),
       viteImagemin({
         gifsicle: { optimizationLevel: 7 },
         optipng: { optimizationLevel: 7 },
         mozjpeg: { quality: 80 },
         pngquant: { quality: [0.8, 0.9] },
         svgo: { plugins: [{ removeViewBox: false }] },
       }),
     ],
   });
   ```

3. **Add service worker (PWA):**
   ```bash
   npm install vite-plugin-pwa -D
   ```
   
   ```javascript
   // vite.config.js
   import { VitePWA } from 'vite-plugin-pwa';
   
   export default defineConfig({
     plugins: [
       react(),
       VitePWA({
         registerType: 'autoUpdate',
         manifest: {
           name: 'KisanAI',
           short_name: 'KisanAI',
           description: 'Smart farming assistant',
           theme_color: '#16a34a',
           icons: [
             {
               src: '/icon-192.png',
               sizes: '192x192',
               type: 'image/png',
             },
             {
               src: '/icon-512.png',
               sizes: '512x512',
               type: 'image/png',
             },
           ],
         },
       }),
     ],
   });
   ```

---

## 📦 Docker Deployment

### Dockerfile (Backend)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ .

# Create data directory
RUN mkdir -p data logs

# Expose port
EXPOSE 8000

# Run with gunicorn
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### Dockerfile (Frontend)

```dockerfile
FROM node:20-alpine as build

WORKDIR /app

# Install dependencies
COPY frontend/package*.json ./
RUN npm ci

# Copy source and build
COPY frontend/ .
RUN npm run build

# Production image with nginx
FROM nginx:alpine

# Copy built files
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### docker-compose.yml (Production)

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://user:password@db:5432/kisanai
      - OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY}
      - GROQ_API_KEY=${GROQ_API_KEY}
    ports:
      - "8000:8000"
    volumes:
      - ./backend/data:/app/data
      - ./backend/logs:/app/logs
    depends_on:
      - db
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=kisanai
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=kisanai
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  postgres_data:
```

### nginx.conf

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Frontend routes (SPA)
    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache";
    }

    # API proxy
    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 📊 Monitoring & Logging

### Backend Logging

```python
# backend/main.py
import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'logs/app.log',
            maxBytes=10485760,  # 10MB
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

### Error Tracking (Sentry)

```bash
# Backend
pip install sentry-sdk[fastapi]

# Frontend
npm install @sentry/react
```

```python
# backend/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
    environment="production",
)
```

```javascript
// frontend/main.jsx
import * as Sentry from '@sentry/react';

Sentry.init({
  dsn: 'your-sentry-dsn',
  environment: 'production',
  integrations: [new Sentry.BrowserTracing()],
  tracesSampleRate: 0.1,
});
```

### Health Check Endpoints

```python
# backend/main.py
from datetime import datetime
from sqlalchemy import text

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint for monitoring"""
    try:
        # Check database
        db.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected",
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return Response(
            content=json.dumps({
                "status": "unhealthy",
                "error": str(e)
            }),
            status_code=503
        )
```

---

## 🧪 Testing Before Deployment

### Backend Tests

```python
# tests/test_crops.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_crops():
    response = client.get("/crops")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_crop():
    data = {
        "name": "Test Wheat",
        "type": "Cereal",
        "plot": "Plot A",
        "sowing_date": "2024-01-01"
    }
    response = client.post("/crops/add", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Wheat"
```

Run tests:
```bash
pip install pytest pytest-cov
pytest --cov=backend tests/
```

### Frontend Tests

```javascript
// tests/Crops.test.jsx
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Crops from '../src/pages/Crops';

test('renders crops page', () => {
  const queryClient = new QueryClient();
  render(
    <QueryClientProvider client={queryClient}>
      <Crops />
    </QueryClientProvider>
  );
  expect(screen.getByText(/crops/i)).toBeInTheDocument();
});
```

Run tests:
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom
npm test
```

---

## 🚀 Deployment Steps

### 1. Prepare Environment

```bash
# Update dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# Build frontend
npm run build

# Test backend
cd ../backend && pytest

# Check linting
ruff check backend
```

### 2. Deploy with Docker

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose logs -f
```

### 3. Deploy to Cloud (Example: Railway/Render)

**Backend (Railway):**
1. Connect GitHub repo
2. Set environment variables
3. Deploy from main branch
4. Set start command: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`

**Frontend (Vercel/Netlify):**
1. Connect GitHub repo
2. Build command: `npm run build`
3. Output directory: `dist`
4. Environment: `VITE_API_URL=https://your-backend-url.railway.app`

### 4. Post-Deployment

```bash
# Verify health check
curl https://your-api-domain.com/health

# Test critical endpoints
curl https://your-api-domain.com/crops
curl https://your-api-domain.com/weather

# Monitor logs
tail -f logs/app.log

# Check database
sqlite3 backend/data/kisan.db "SELECT COUNT(*) FROM users;"
```

---

## 📈 Performance Monitoring

### Key Metrics to Track

1. **Response Times:**
   - `/crops` < 100ms
   - `/weather` < 200ms (external API)
   - `/dashboard` < 150ms

2. **Error Rates:**
   - Target: < 1% error rate
   - Monitor 4xx and 5xx responses

3. **Database:**
   - Query execution time
   - Connection pool usage
   - Slow query logs

4. **Frontend:**
   - Time to Interactive (TTI)
   - First Contentful Paint (FCP)
   - Largest Contentful Paint (LCP)
   - Bundle size < 500KB

### Tools:

- **Backend:** Prometheus + Grafana
- **Frontend:** Lighthouse, Web Vitals
- **Errors:** Sentry
- **Logs:** ELK Stack or Cloudwatch
- **Uptime:** UptimeRobot, Pingdom

---

## ✅ Final Checklist

Before going live:

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] SECRET_KEY changed
- [ ] CORS origins restricted
- [ ] HTTPS enabled
- [ ] Database backed up
- [ ] Monitoring set up
- [ ] Error tracking active
- [ ] Health check working
- [ ] Documentation updated
- [ ] Demo credentials removed
- [ ] Rate limiting active
- [ ] JWT expiration set
- [ ] Logging configured
- [ ] Performance tested
- [ ] Security audit passed

---

**Version:** 1.0  
**Last Updated:** November 20, 2025  
**Status:** Ready for Production 🎉
