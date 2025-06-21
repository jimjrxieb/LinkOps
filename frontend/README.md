# 🧠 LinkOps HoloCore - Elite AI Command Center

Vue 3 holographic interface for the LinkOps Core AI Training & Learning System.

## 🚀 Features

- **👑 James Tab**: Task evaluation, routing, and conversation history
- **🧠 Whis Tab**: Training queue, approval queue, and daily digest
- **🎨 Holographic UI**: Cyberpunk-inspired design with glass effects and neon colors
- **📊 Real-time Updates**: Live data from the backend API
- **🔄 State Management**: Pinia store for centralized state
- **📱 Responsive**: Works perfectly on all devices

## 🛠 Tech Stack

- **Vue 3** with Composition API
- **Vue Router** for navigation
- **Pinia** for state management
- **Tailwind CSS** with custom holographic theme
- **Axios** for API communication
- **Vite** for fast development

## 🎨 Design System

### Colors
- **Holo Cyan**: `#00ffff` - Primary accent
- **Holo Green**: `#00ff80` - Success states
- **Holo Blue**: `#0080ff` - Info states
- **Holo Yellow**: `#ffff00` - Warning states
- **Holo Red**: `#ff0000` - Error states

### Components
- **Holo Cards**: Glassy panels with backdrop blur
- **Holo Buttons**: Neon-styled interactive elements
- **Holo Inputs**: Cyber-styled form controls
- **Status Badges**: Color-coded status indicators

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn
- Backend running on localhost:8000

### Development Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Access the app:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Production Build

```bash
npm run build
npm run preview
```

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── agents/
│   │   ├── JamesTab.vue        # James task interface
│   │   └── WhisTab.vue         # Whis training interface
│   ├── stores/
│   │   └── agents.js           # Pinia store
│   ├── assets/
│   │   └── tailwind.css        # Custom styles
│   ├── App.vue                 # Main app component
│   ├── main.js                 # Vue entry point
│   └── router.js               # Vue Router config
├── package.json                # Dependencies
├── vite.config.js              # Vite configuration
├── tailwind.config.js          # Tailwind theme
└── postcss.config.js           # PostCSS config
```

## 🧠 Agent Tabs

### 👑 James Tab
- **Task Input**: Submit new tasks for evaluation
- **Evaluation Results**: View detected category and options
- **Action Buttons**: Complete with James or send to agents
- **Conversation History**: Real-time log of all interactions

### 🧠 Whis Tab
- **Training Queue**: Monitor pending, trained, matches, and fallbacks
- **Approval Queue**: Review and approve flagged runes
- **Daily Digest**: View daily statistics and metrics
- **Night Training**: Trigger AI training processes

## 🔧 Configuration

### Environment Variables
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

### API Proxy
The development server automatically proxies `/api/*` requests to the backend.

## 🎯 API Integration

The frontend integrates with these backend endpoints:

### James Endpoints
- `POST /api/james/evaluate` - Task evaluation
- `POST /api/tasks/complete-with-james` - Complete task
- `POST /api/tasks/send-to-agent` - Route to agent

### Whis Endpoints
- `GET /api/whis/queue` - Training queue status
- `GET /api/whis/approvals` - Pending approvals
- `POST /api/whis/approve-rune` - Approve rune
- `POST /api/whis/train-nightly` - Trigger training
- `GET /api/whis/digest` - Daily summary

## 🎨 Customization

### Adding New Colors
Edit `tailwind.config.js`:
```js
colors: {
  'holo': {
    'new-color': '#your-hex-code'
  }
}
```

### Adding New Components
Create reusable components in `src/components/`:
```vue
<template>
  <div class="holo-card">
    <!-- Your component content -->
  </div>
</template>
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build the image
docker build -t linkops-holocore .

# Run the container
docker run -p 3000:3000 linkops-holocore
```

### Static Deployment
```bash
# Build for production
npm run build

# Deploy dist/ folder to your hosting service
```

## 🔗 Integration

The frontend seamlessly integrates with the LinkOps Core backend:

1. **Real-time Updates**: Automatic refresh of data
2. **Error Handling**: Graceful error display and recovery
3. **Loading States**: Visual feedback during operations
4. **State Management**: Centralized state with Pinia

## 📱 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of LinkOps Core and follows the same license terms.

---

**Ready to command your AI army with elite precision!** 🚀 