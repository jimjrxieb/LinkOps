<template>
  <div class="app holo-bg">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2 class="neon-text glitch" data-text="LinkOps Core">LinkOps Core</h2>
        <p class="text-xs text-gray-400">AI Command Center</p>
      </div>
      <nav>
        <ul>
          <li><router-link to="/dashboard" class="holo-hover">📊 Dashboard</router-link></li>
          <li><router-link to="/james" class="holo-hover">🤖 James</router-link></li>
          <li><router-link to="/whis" class="holo-hover">🧠 Whis</router-link></li>
          <li><router-link to="/agents" class="holo-hover">🧑‍💻 Agents</router-link></li>
          <li><router-link to="/about" class="holo-hover">ℹ️ About</router-link></li>
          <li><router-link to="/audit-dashboard" class="holo-hover">🛡️ Audit</router-link></li>
          <li><router-link to="/data-collection" class="holo-hover">📥 Data Collection</router-link></li>
          <li><router-link to="/digest" class="holo-hover">📒 Digest</router-link></li>
        </ul>
      </nav>
      <div class="sidebar-footer">
        <div class="status-indicator">
          <span class="text-xs text-green-400">● System Online</span>
        </div>
        <div class="user-section">
          <router-link to="/login" class="login-link">🔐 Login</router-link>
        </div>
      </div>
    </aside>
    <main class="content">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
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
  width: 280px;
  background: rgba(17, 17, 17, 0.95);
  color: #fff;
  padding: 1.5rem;
  border-right: 2px solid #00ffff;
  box-shadow: 0 0 30px rgba(0, 255, 255, 0.15);
  backdrop-filter: blur(15px);
  position: relative;
  overflow-y: auto;
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, 
    rgba(0, 255, 255, 0.05) 0%, 
    transparent 50%, 
    rgba(255, 0, 255, 0.05) 100%);
  pointer-events: none;
}

.sidebar-header {
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(0, 255, 255, 0.3);
  margin-bottom: 1.5rem;
  position: relative;
}

.sidebar-header h2 {
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  margin: 0.75rem 0;
}

.sidebar a {
  color: #0ff;
  text-decoration: none;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  display: block;
  border: 1px solid transparent;
  position: relative;
  overflow: hidden;
}

.sidebar a::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.sidebar a:hover::before {
  left: 100%;
}

.sidebar a:hover,
.sidebar a.router-link-active {
  background: rgba(0, 255, 255, 0.15);
  border-color: #00ffff;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
  transform: translateX(8px) scale(1.02);
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.8);
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(0, 255, 255, 0.3);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.login-link {
  color: #ff6b6b;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 107, 107, 0.3);
  transition: all 0.3s ease;
  text-align: center;
}

.login-link:hover {
  background: rgba(255, 107, 107, 0.1);
  border-color: #ff6b6b;
  box-shadow: 0 0 15px rgba(255, 107, 107, 0.3);
}

.content {
  flex-grow: 1;
  padding: 2rem;
  background: rgba(26, 26, 26, 0.8);
  color: #eee;
  overflow-y: auto;
  backdrop-filter: blur(10px);
  position: relative;
}

/* Page transitions */
.page-enter-active,
.page-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Holographic background effects */
.app::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 255, 255, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 0, 255, 0.08) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(0, 255, 0, 0.08) 0%, transparent 50%);
  pointer-events: none;
  z-index: -1;
  animation: holo-shift 15s ease-in-out infinite;
}

@keyframes holo-shift {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
}

/* Responsive design */
@media (max-width: 768px) {
  .sidebar {
    width: 240px;
    padding: 1rem;
  }
  
  .content {
    padding: 1rem;
  }
  
  .sidebar a:hover,
  .sidebar a.router-link-active {
    transform: translateX(5px) scale(1.01);
  }
}
</style>

<script>
export default {
  name: 'App',
  mounted() {
    // Initialize GSAP animations
    this.$nextTick(() => {
      this.initializeAnimations();
    });
  },
  methods: {
    initializeAnimations() {
      // Add subtle floating animation to sidebar
      gsap.to('.sidebar', {
        y: -5,
        duration: 2,
        repeat: -1,
        yoyo: true,
        ease: "power2.inOut"
      });
    }
  }
}
</script> 