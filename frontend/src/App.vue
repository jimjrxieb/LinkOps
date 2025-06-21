<template>
  <div class="h-screen bg-gradient-to-br from-cyber-dark via-black to-cyber-dark text-holo-cyan font-mono relative overflow-hidden holo-bg">
    <!-- Matrix Rain Background -->
    <div class="matrix-rain"></div>
    
    <!-- Scan line effect -->
    <div class="scan-line"></div>
    
    <!-- Header -->
    <header class="p-4 text-xl font-bold backdrop-blur-sm border-b border-holo-cyan/30 bg-cyber-gray/20 relative z-10">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-holo-cyan/20 rounded-full flex items-center justify-center animate-pulse pulse-cyber">
            🧠
          </div>
          <h1 class="text-glow neon-text" data-text="LinkOps HoloCore">LinkOps HoloCore</h1>
        </div>
        <div class="text-sm text-holo-cyan/70">
          <span class="typewriter">Shadow Monarch Protocol v0.1</span>
        </div>
      </div>
    </header>

    <!-- Navigation -->
    <nav class="flex gap-4 p-4 bg-cyber-gray/10 text-holo-cyan border-b border-holo-cyan/20 relative z-10">
      <RouterLink 
        to="/james" 
        class="holo-nav-link holo-hover"
        :class="{ active: $route.path === '/james' }"
      >
        👑 James
      </RouterLink>
      <RouterLink 
        to="/whis" 
        class="holo-nav-link holo-hover"
        :class="{ active: $route.path === '/whis' }"
      >
        🧠 Whis
      </RouterLink>
      <RouterLink 
        to="/katie" 
        class="holo-nav-link opacity-50 cursor-not-allowed"
      >
        ☸️ Katie (Coming Soon)
      </RouterLink>
      <RouterLink 
        to="/igris" 
        class="holo-nav-link opacity-50 cursor-not-allowed"
      >
        🛡️ Igris (Coming Soon)
      </RouterLink>
    </nav>

    <!-- Main Content -->
    <main class="p-6 overflow-y-auto h-[calc(100vh-140px)] relative z-10">
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="text-xs text-center text-holo-cyan/60 py-2 border-t border-holo-cyan/20 bg-cyber-gray/10 relative z-10">
      <div class="flex items-center justify-center space-x-4">
        <span>Persistent AI Orchestration Engine</span>
        <div class="status-indicator"></div>
        <span>Elite Command Center</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
// Nothing yet - pure layout component with cyberpunk effects
</script>

<style scoped>
@import './assets/cyberpunk.css';
</style> 