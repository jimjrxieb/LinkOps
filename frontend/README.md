# LinkOps Frontend Microservice

A Vue 3-based frontend microservice for the LinkOps AI Command Center, featuring a holographic sci-fi interface.

## 🚀 Features

- **Holographic UI Design** - Sci-fi themed interface with glowing effects
- **Vue 3 + Composition API** - Modern reactive framework
- **Tailwind CSS** - Utility-first styling
- **GSAP Animations** - Smooth, professional animations
- **Microservice Architecture** - Independent deployment
- **Kubernetes Ready** - Full K8s deployment support
- **ArgoCD Compatible** - GitOps deployment workflow

## 📁 Project Structure

```
frontend/
├── Dockerfile              # Multi-stage production build
├── nginx.conf              # Nginx configuration for serving
├── vite.config.js          # Vite build configuration
├── package.json            # Dependencies and scripts
├── public/                 # Static assets
├── src/
│   ├── assets/             # Images, fonts, styles
│   ├── components/         # Reusable Vue components
│   ├── views/              # Page components
│   ├── router/             # Vue Router configuration
│   ├── stores/             # Pinia state management
│   ├── services/           # API service layer
│   └── App.vue             # Root component
└── README.md               # This file
```

## 🛠 Development

### Prerequisites

- Node.js 18+
- npm 8+

### Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint

# Run tests
npm run test
```

### Environment Variables

Create `.env.local` for local development:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WHIS_URL=http://localhost:8001
VITE_JAMES_URL=http://localhost:8002
VITE_SANITIZER_URL=http://localhost:8003
VITE_DATA_COLLECTOR_URL=http://localhost:8004
```

## 🐳 Docker Deployment

### Build Image

```bash
# Build production image
docker build -t linkopsacr.azurecr.io/frontend:latest .

# Run locally
docker run -p 80:80 linkopsacr.azurecr.io/frontend:latest
```

### Multi-stage Build

The Dockerfile uses a multi-stage build:
1. **Builder stage** - Compiles Vue.js application
2. **Production stage** - Nginx serves static files

## ☸️ Kubernetes Deployment

### Prerequisites

- AKS cluster with NGINX ingress controller
- Azure Container Registry (ACR)
- ArgoCD (optional)

### Deploy to Kubernetes

```bash
# Apply all resources
kubectl apply -k infrastructure/k8s/base/

# Check deployment status
kubectl get pods -n linkops
kubectl get services -n linkops
kubectl get ingress -n linkops
```

### Access the Application

After deployment, access via:
- **Primary**: `http://linkops.local`
- **Alternative**: `http://www.linkops.local`

## 🔧 Configuration

### Nginx Configuration

The `nginx.conf` includes:
- Gzip compression
- Security headers
- Static asset caching
- Vue Router history mode support
- Health check endpoint
- API proxy configuration

### Vite Configuration

Optimized for production:
- Code splitting
- Tree shaking
- Minification
- Source map generation (disabled in prod)
- Manual chunks for vendor libraries

## 📊 Monitoring & Health Checks

### Health Endpoints

- **Application Health**: `GET /health`
- **Readiness Probe**: `GET /`
- **Liveness Probe**: `GET /`

### Kubernetes Probes

```yaml
livenessProbe:
  httpGet:
    path: /
    port: 80
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /
    port: 80
  initialDelaySeconds: 5
  periodSeconds: 5
```

## 🔄 CI/CD Pipeline

### GitHub Actions

The `.github/workflows/frontend-build.yml` workflow:
1. Builds Docker image on push/PR
2. Pushes to Azure Container Registry
3. Deploys to AKS (main branch only)

### ArgoCD Integration

The frontend is included in the ArgoCD application:
- **Path**: `infrastructure/k8s/base/frontend/`
- **Auto-sync**: Enabled
- **Self-heal**: Enabled

## 🎨 UI Components

### Core Pages

- **Dashboard** - System overview and monitoring
- **James** - AI assistant interface
- **Whis** - Training system management
- **Agents** - Agent profiles and performance
- **Login** - Authentication interface
- **About** - System information and profiles

### Design System

- **Color Palette**: Cyberpunk theme with neon cyan (#00ffff)
- **Typography**: Futuristic fonts with glowing effects
- **Animations**: GSAP-powered smooth transitions
- **Layout**: Responsive grid system with glassmorphism

## 🔌 API Integration

### Service Layer

The `src/services/api.js` provides:
- Centralized API client configuration
- Service-specific API functions
- Error handling and retry logic
- Health check utilities

### Microservice Communication

- **Backend**: Core API endpoints
- **Whis**: Training and approval workflows
- **James**: Task submission and AI assistance
- **Sanitizer**: Data processing
- **Data Collector**: Data ingestion

## 🚀 Performance Optimization

### Build Optimizations

- **Code Splitting**: Automatic vendor chunk separation
- **Tree Shaking**: Unused code elimination
- **Minification**: Terser for JavaScript compression
- **Asset Optimization**: Image and font optimization

### Runtime Optimizations

- **Lazy Loading**: Route-based code splitting
- **Caching**: Static asset caching with nginx
- **Compression**: Gzip compression enabled
- **CDN Ready**: Static assets optimized for CDN

## 🔒 Security

### Security Headers

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

### Best Practices

- Non-root container execution
- Minimal attack surface
- Regular security updates
- Environment variable management

## 🧪 Testing

### Test Commands

```bash
# Unit tests
npm run test

# UI tests
npm run test:ui

# Coverage report
npm run test:coverage

# Type checking
npm run type-check
```

### Test Coverage

- Component unit tests
- API service tests
- Integration tests
- E2E tests (planned)

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale frontend deployment
kubectl scale deployment frontend --replicas=5 -n linkops

# Auto-scaling (HPA)
kubectl apply -f infrastructure/k8s/base/frontend/hpa.yaml
```

### Load Balancing

- Kubernetes Service load balancing
- NGINX ingress controller
- Session affinity support

## 🐛 Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Clear node_modules and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **Docker Build Issues**
   ```bash
   # Clear Docker cache
   docker system prune -a
   ```

3. **Kubernetes Deployment Issues**
   ```bash
   # Check pod logs
   kubectl logs deployment/frontend -n linkops
   
   # Check pod status
   kubectl describe pod -l app=frontend -n linkops
   ```

### Debug Mode

Enable debug mode in development:
```env
VITE_ENABLE_DEBUG=true
```

## 📚 Resources

- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [GSAP Documentation](https://greensock.com/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of the LinkOps platform and follows the same licensing terms. 