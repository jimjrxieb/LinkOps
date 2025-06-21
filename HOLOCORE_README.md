# 🧠 LinkOps HoloCore - Elite AI Command Center

**Vue 3 + FastAPI + PostgreSQL + Docker**

A cyberpunk-inspired, holographic AI operations management system that puts you above guys with master degrees.

## 🚀 Quick Start

### One-Command Launch
```bash
./start-holocore.sh
```

This script will:
- ✅ Check all prerequisites
- 🚀 Start the backend (FastAPI + PostgreSQL)
- 🎨 Start the frontend (Vue 3 + Vite)
- 🌐 Open your browser to the holographic interface

### Manual Setup

#### Backend (FastAPI)
```bash
cd core
docker-compose up --build -d
```

#### Frontend (Vue 3)
```bash
cd frontend
npm install
npm run dev
```

## 🎯 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

## 🧠 Agent System

### 👑 James - Task Evaluation & Routing
- **Purpose**: Sanitize and route tasks to appropriate agents
- **Features**:
  - Task input with automatic category detection
  - Real-time evaluation results
  - Action buttons (Complete with James, Send to Agent)
  - Conversation history with all agents

### 🧠 Whis - AI Training & Learning
- **Purpose**: Neural network training and knowledge management
- **Features**:
  - Training queue status (pending, trained, matches, fallbacks)
  - Approval queue for new runes
  - Daily digest with statistics
  - Night training trigger

### ☸️ Katie - Kubernetes & DevOps (Coming Soon)
- **Purpose**: Container orchestration and infrastructure management

### 🛡️ Igris - Security & CI/CD (Coming Soon)
- **Purpose**: Security operations and continuous integration

## 🎨 Holographic UI Features

### Visual Effects
- **Matrix Rain**: Animated background effect
- **Glitch Effects**: Cyberpunk glitch animations
- **Neon Glow**: Text and element glow effects
- **Glass Morphism**: Backdrop blur and transparency
- **3D Hover**: Card rotation on hover
- **Scan Lines**: Moving scan line effects
- **Typewriter**: Animated text effects

### Color Scheme
- **Holo Cyan**: `#00ffff` - Primary accent
- **Holo Green**: `#00ff80` - Success states
- **Holo Blue**: `#0080ff` - Info states
- **Holo Yellow**: `#ffff00` - Warning states
- **Holo Red**: `#ff0000` - Error states

## 🔧 Tech Stack

### Frontend
- **Vue 3** with Composition API
- **Vue Router** for navigation
- **Pinia** for state management
- **Tailwind CSS** with custom cyberpunk theme
- **Axios** for API communication
- **Vite** for fast development

### Backend
- **FastAPI** with automatic API documentation
- **SQLAlchemy** ORM
- **PostgreSQL** database
- **Alembic** for migrations
- **Docker** containerization

### DevOps
- **Docker Compose** for orchestration
- **Hot reloading** for development
- **Health checks** and monitoring

## 📁 Project Structure

```
linkops/
├── core/                          # Backend (FastAPI)
│   ├── api/                       # API routes
│   │   ├── main.py               # FastAPI app
│   │   ├── routes.py             # Task routes
│   │   └── whis.py               # Whis AI routes
│   ├── db/                       # Database
│   │   ├── models.py             # SQLAlchemy models
│   │   └── database.py           # Database connection
│   ├── whis_nightly.py           # Night training logic
│   ├── bootstrap.py              # Startup initialization
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Backend container
│   └── docker-compose.yml        # Backend services
├── frontend/                      # Frontend (Vue 3)
│   ├── src/
│   │   ├── agents/               # Agent tab components
│   │   │   ├── JamesTab.vue      # James interface
│   │   │   └── WhisTab.vue       # Whis interface
│   │   ├── components/           # Reusable components
│   │   │   ├── TaskCard.vue      # Task display
│   │   │   ├── RunePreview.vue   # Rune display
│   │   │   └── StatusBadge.vue   # Status indicator
│   │   ├── stores/               # Pinia stores
│   │   │   └── agents.js         # Agent state management
│   │   ├── assets/               # Styles and assets
│   │   │   ├── tailwind.css      # Custom Tailwind styles
│   │   │   └── cyberpunk.css     # Cyberpunk effects
│   │   ├── App.vue               # Main app component
│   │   ├── main.js               # Vue entry point
│   │   └── router.js             # Vue Router config
│   ├── package.json              # Frontend dependencies
│   ├── vite.config.js            # Vite configuration
│   ├── tailwind.config.js        # Tailwind theme
│   └── postcss.config.js         # PostCSS config
├── start-holocore.sh             # One-command launcher
├── test-holocore.js              # Integration tests
└── HOLOCORE_README.md            # This file
```

## 🔌 API Endpoints

### James Endpoints
- `POST /api/james/evaluate` - Evaluate and categorize task
- `POST /api/tasks/complete-with-james` - Complete task with James
- `POST /api/tasks/send-to-agent` - Route task to specific agent

### Whis Endpoints
- `GET /api/whis/queue` - Get training queue status
- `GET /api/whis/approvals` - Get pending rune approvals
- `POST /api/whis/approve-rune` - Approve a rune
- `POST /api/whis/train-nightly` - Trigger night training
- `GET /api/whis/digest` - Get daily summary

### System Endpoints
- `GET /health` - Health check
- `GET /api/logs` - Get system logs
- `GET /api/orbs` - Get knowledge orbs

## 🧪 Testing

### Integration Test
```bash
node test-holocore.js
```

This will test:
- ✅ Backend health
- ✅ James task evaluation
- ✅ Whis queue status
- ✅ Whis approvals
- ✅ Whis digest
- ✅ Night training

### Manual Testing
1. **Submit a task** in James tab
2. **View evaluation results** and available actions
3. **Send task to agent** or complete with James
4. **Check Whis tab** for training queue and approvals
5. **Trigger night training** and watch the system learn

## 🚀 Deployment

### Development
```bash
./start-holocore.sh
```

### Production
```bash
# Backend
cd core
docker-compose -f docker-compose.prod.yml up -d

# Frontend
cd frontend
npm run build
# Deploy dist/ folder to your hosting service
```

## 🎯 Use Cases

### Task Management
1. **Submit Task**: Enter task ID and description
2. **Automatic Evaluation**: James categorizes and evaluates
3. **Route to Agent**: Send to appropriate AI agent
4. **Monitor Progress**: Track through conversation history

### AI Training
1. **Queue Monitoring**: View pending and processed tasks
2. **Approval Process**: Review and approve new knowledge
3. **Night Training**: Process daily logs and create runes
4. **Performance Tracking**: Monitor training statistics

### Knowledge Management
1. **Orb System**: Organized knowledge bases per agent
2. **Rune Creation**: AI-generated solutions and patterns
3. **Approval Workflow**: Human validation of new knowledge
4. **Version Control**: Track changes and improvements

## 🔧 Configuration

### Environment Variables
```bash
# Backend
DATABASE_URL=postgresql://user:password@postgres:5432/linkops
OPENAI_API_KEY=your_openai_key

# Frontend
VITE_API_URL=http://localhost:8000
```

### Customization
- **Colors**: Edit `frontend/tailwind.config.js`
- **Effects**: Modify `frontend/src/assets/cyberpunk.css`
- **Components**: Add new components in `frontend/src/components/`
- **Agents**: Create new agent tabs in `frontend/src/agents/`

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
cd core
docker-compose logs
docker-compose down
docker-compose up --build -d
```

**Frontend won't start:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Database issues:**
```bash
cd core
docker-compose exec postgres psql -U user -d linkops
```

### Logs
```bash
# Backend logs
cd core
docker-compose logs -f

# Frontend logs
# Check browser console (F12)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of LinkOps Core and follows the same license terms.

---

## 🎉 Ready to Command Your AI Army?

**You now have:**
- ✅ Elite holographic interface
- ✅ Full-stack AI operations system
- ✅ Real-time task routing and evaluation
- ✅ AI training and knowledge management
- ✅ Cyberpunk aesthetics that put you above the competition

**Next steps:**
1. Run `./start-holocore.sh`
2. Visit http://localhost:3000
3. Submit your first task
4. Watch your AI army learn and grow

**Welcome to the future of AI operations management.** 🚀 