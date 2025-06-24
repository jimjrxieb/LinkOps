<template>
  <div class="app holo-bg">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2 class="neon-text glitch" data-text="LinkOps Core">LinkOps Core</h2>
        <p class="text-xs text-gray-400">AI Agent Platform</p>
      </div>
      <nav>
        <ul>
          <li><router-link to="/dashboard" class="holo-hover">📊 Dashboard</router-link></li>
          <li><router-link to="/audit-dashboard" class="holo-hover">🛡️ Audit</router-link></li>
          <li><router-link to="/data-collection" class="holo-hover">📥 Data Collection</router-link></li>
          <li><router-link to="/whis" class="holo-hover">🧠 Whis</router-link></li>
          <li><router-link to="/agents" class="holo-hover">🧑‍💻 Agents</router-link></li>
          <li><router-link to="/digest" class="holo-hover">📒 Digest</router-link></li>
        </ul>
      </nav>
      <div class="sidebar-footer">
        <div class="status-indicator">
          <span class="text-xs text-green-400">● System Online</span>
        </div>
      </div>
    </aside>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style>
@import './assets/cyberpunk.css';

.app {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
}

.sidebar {
  width: 250px;
  background: rgba(17, 17, 17, 0.95);
  color: #fff;
  padding: 1rem;
  border-right: 2px solid #00ffff;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.sidebar-header {
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  margin-bottom: 1rem;
}

.sidebar-header h2 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin: 0.5rem 0;
}

.sidebar a {
  color: #0ff;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s ease;
  display: block;
  border: 1px solid transparent;
}

.sidebar a:hover,
.sidebar a.router-link-active {
  background: rgba(0, 255, 255, 0.1);
  border-color: #00ffff;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
  transform: translateX(5px);
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

.content {
  flex-grow: 1;
  padding: 2rem;
  background: rgba(26, 26, 26, 0.8);
  color: #eee;
  overflow-y: auto;
  backdrop-filter: blur(5px);
}

/* Matrix rain effect for background */
.app::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 0, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(0, 255, 0, 0.1) 0%, transparent 50%);
  pointer-events: none;
  z-index: -1;
  animation: holo-shift 10s ease-in-out infinite;
}

/* Responsive design */
@media (max-width: 768px) {
  .sidebar {
    width: 200px;
  }
  
  .content {
    padding: 1rem;
  }
}
</style>

<script>
import PwCDashboard from './components/PwCDashboard.vue'

export default {
  components: {
    PwCDashboard
  }
}
</script> 