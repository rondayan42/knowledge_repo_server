# Knowledge Repository - Backend Server

A Flask-based REST API for the Knowledge Repository application, featuring JWT authentication, article management, file uploads, and Prometheus monitoring.

---

## ✨ Features

- **RESTful API** - Full CRUD operations for articles, categories, departments, tags
- **JWT Authentication** - Secure login with token-based auth
- **Role-based Access** - Admin and user roles with permissions
- **File Uploads** - Support for attachments and images
- **Favorites & History** - Track favorite articles and recently viewed
- **Prometheus Monitoring** - Metrics endpoint for observability
- **Health Checks** - Kubernetes-ready health endpoints

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Framework** | Flask |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Authentication** | JWT (PyJWT) |
| **Server** | Gunicorn |
| **Monitoring** | Prometheus |

---

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL database
- pip

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd knowledge_repo_server
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/knowledge_repo
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
PORT=5000
DEBUG=true
```

### 5. Initialize Database

```bash
python seed_root_user.py
```

### 6. Run the Server

```bash
# Development
python app.py

# Production
gunicorn -c gunicorn.conf.py app:app
```

The API will be available at `http://localhost:5000`

---

## 📜 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get JWT token |
| GET | `/api/auth/me` | Get current user info |
| GET | `/api/auth/config` | Get auth configuration |

### Articles
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/articles` | List all articles |
| GET | `/api/articles/:id` | Get single article |
| POST | `/api/articles` | Create article (auth required) |
| PUT | `/api/articles/:id` | Update article (auth required) |
| DELETE | `/api/articles/:id` | Delete article (auth required) |
| GET | `/api/articles/search?q=` | Search articles |
| GET | `/api/articles/stats` | Get article statistics |

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories` | List all categories |
| POST | `/api/categories` | Create category (auth required) |
| PUT | `/api/categories/:id` | Update category |
| DELETE | `/api/categories/:id` | Delete category (auth required) |

### Departments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/departments` | List all departments |
| POST | `/api/departments` | Create department (auth required) |
| PUT | `/api/departments/:id` | Update department |
| DELETE | `/api/departments/:id` | Delete department (auth required) |

### Priorities
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/priorities` | List all priorities |
| POST | `/api/priorities` | Create priority (auth required) |
| PUT | `/api/priorities/:id` | Update priority |
| DELETE | `/api/priorities/:id` | Delete priority (auth required) |

### Tags
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tags` | List all tags |
| POST | `/api/tags` | Create tag (auth required) |
| DELETE | `/api/tags/:id` | Delete tag (auth required) |

### Favorites
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/favorites` | Get user's favorites (auth required) |
| POST | `/api/favorites/:articleId` | Add to favorites (auth required) |
| DELETE | `/api/favorites/:articleId` | Remove from favorites (auth required) |

### Recently Viewed
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/recently-viewed` | Get recently viewed (auth required) |
| POST | `/api/recently-viewed/:articleId` | Add to history (auth required) |
| DELETE | `/api/recently-viewed` | Clear history (auth required) |

### Users (Admin Only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | List all users |
| PUT | `/api/users/:id/role` | Update user role |
| PUT | `/api/users/:id/approve` | Approve/reject user |
| DELETE | `/api/users/:id` | Delete user |

### File Uploads
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/attachments` | Upload file attachment (auth required) |
| POST | `/api/images` | Upload inline image (auth required) |

### Health & Monitoring
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/ready` | Readiness check (tests DB) |
| GET | `/metrics` | Prometheus metrics |

---

## 📊 Monitoring

The server exposes Prometheus metrics at `/metrics`:

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total HTTP requests |
| `http_request_duration_seconds` | Histogram | Request latency |
| `app_auth_attempts_total` | Counter | Login attempts |
| `app_file_uploads_total` | Counter | File uploads |
| `app_exceptions_total` | Counter | Application errors |

---

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

---

## 🐳 Docker

### Build Image

```bash
docker build -t knowledge-repo-server .
```

### Run Container

```bash
docker run -d -p 5000:5000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=your-secret \
  -e JWT_SECRET=your-jwt-secret \
  knowledge-repo-server
```

---

## ☸️ Kubernetes Deployment

### Deploy with Kustomize

```bash
kubectl apply -k k8s/
```

### Deploy Individually

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml      # Edit with real credentials first!
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml
```

### K8s Files

| File | Purpose |
|------|---------|
| `deployment.yaml` | Flask app deployment (2 replicas) |
| `service.yaml` | ClusterIP service on port 5000 |
| `configmap.yaml` | Environment variables |
| `secrets.yaml` | Database credentials (edit this!) |
| `ingress.yaml` | External access |
| `hpa.yaml` | Auto-scaling (2-5 pods) |
| `pvc.yaml` | Storage for uploads |

---

## 📁 Project Structure

```
knowledge_repo_server/
├── models/              # SQLAlchemy models
├── routes/              # API route handlers
├── monitoring/          # Prometheus metrics
├── tests/               # Unit tests
├── k8s/                 # Kubernetes manifests
├── uploads/             # Uploaded files
├── app.py               # Main application
├── auth.py              # Authentication helpers
├── config.py            # Configuration
├── database.py          # Database connection
├── requirements.txt     # Dependencies
├── Dockerfile           # Docker build
└── gunicorn.conf.py     # Gunicorn config
```

---

## 🔐 Authentication

The API uses JWT tokens for authentication.

### Login Flow

1. POST to `/api/auth/login` with email/password
2. Receive JWT token in response
3. Include token in subsequent requests:
   ```
   Authorization: Bearer <token>
   ```

### Default Root User

After running `seed_root_user.py`:
- Email: `root@admin.local`
- Password: `root123`

⚠️ Change this in production!

---

## 📝 License

This project is private and proprietary.
