<template>
  <div class="agents-page">
    <div class="page-header">
      <h1 class="page-title">🧑‍💻 AI Agents</h1>
      <p class="page-subtitle">Specialized AI Agents for Task Execution</p>
    </div>

    <div class="agents-grid">
      <!-- Katie Agent -->
      <div class="agent-card katie">
        <div class="agent-header">
          <div class="agent-avatar">👩‍💻</div>
          <div class="agent-info">
            <h3 class="agent-name">Katie</h3>
            <p class="agent-title">Data Processing Specialist</p>
            <div class="agent-status online">● Online</div>
          </div>
        </div>
        
        <div class="agent-stats">
          <div class="stat">
            <span class="stat-number">{{ katieStats.tasksCompleted }}</span>
            <span class="stat-label">Tasks Completed</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ katieStats.successRate }}%</span>
            <span class="stat-label">Success Rate</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ katieStats.uptime }}h</span>
            <span class="stat-label">Uptime</span>
          </div>
        </div>
        
        <div class="agent-description">
          <p>Specializes in data processing, analysis, and report generation. Handles complex data transformations and statistical analysis.</p>
        </div>
        
        <div class="agent-capabilities">
          <h4>Capabilities</h4>
          <div class="capability-tags">
            <span class="capability-tag">Data Analysis</span>
            <span class="capability-tag">Report Generation</span>
            <span class="capability-tag">Statistical Modeling</span>
            <span class="capability-tag">Data Visualization</span>
          </div>
        </div>
        
        <div class="agent-actions">
          <button @click="viewAgentDetails('katie')" class="btn-primary">View Details</button>
          <button @click="assignTask('katie')" class="btn-secondary">Assign Task</button>
        </div>
      </div>

      <!-- Igris Agent -->
      <div class="agent-card igris">
        <div class="agent-header">
          <div class="agent-avatar">🤖</div>
          <div class="agent-info">
            <h3 class="agent-name">Igris</h3>
            <p class="agent-title">System Integration Expert</p>
            <div class="agent-status online">● Online</div>
          </div>
        </div>
        
        <div class="agent-stats">
          <div class="stat">
            <span class="stat-number">{{ igrisStats.tasksCompleted }}</span>
            <span class="stat-label">Tasks Completed</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ igrisStats.successRate }}%</span>
            <span class="stat-label">Success Rate</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ igrisStats.uptime }}h</span>
            <span class="stat-label">Uptime</span>
          </div>
        </div>
        
        <div class="agent-description">
          <p>Expert in system integration, API management, and cross-platform communication. Handles complex integration scenarios.</p>
        </div>
        
        <div class="agent-capabilities">
          <h4>Capabilities</h4>
          <div class="capability-tags">
            <span class="capability-tag">API Integration</span>
            <span class="capability-tag">System Architecture</span>
            <span class="capability-tag">Protocol Management</span>
            <span class="capability-tag">Cross-Platform</span>
          </div>
        </div>
        
        <div class="agent-actions">
          <button @click="viewAgentDetails('igris')" class="btn-primary">View Details</button>
          <button @click="assignTask('igris')" class="btn-secondary">Assign Task</button>
        </div>
      </div>

      <!-- FickNury Agent -->
      <div class="agent-card ficknury">
        <div class="agent-header">
          <div class="agent-avatar">⚡</div>
          <div class="agent-info">
            <h3 class="agent-name">FickNury</h3>
            <p class="agent-title">Task Evaluation & Deployment</p>
            <div class="agent-status online">● Online</div>
          </div>
        </div>
        
        <div class="agent-stats">
          <div class="stat">
            <span class="stat-number">{{ ficknuryStats.tasksCompleted }}</span>
            <span class="stat-label">Tasks Completed</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ ficknuryStats.successRate }}%</span>
            <span class="stat-label">Success Rate</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ ficknuryStats.uptime }}h</span>
            <span class="stat-label">Uptime</span>
          </div>
        </div>
        
        <div class="agent-description">
          <p>Specializes in task evaluation, confidence scoring, and automated deployment decisions. Makes intelligent routing choices.</p>
        </div>
        
        <div class="agent-capabilities">
          <h4>Capabilities</h4>
          <div class="capability-tags">
            <span class="capability-tag">Task Evaluation</span>
            <span class="capability-tag">Confidence Scoring</span>
            <span class="capability-tag">Deployment Logic</span>
            <span class="capability-tag">Risk Assessment</span>
          </div>
        </div>
        
        <div class="agent-actions">
          <button @click="viewAgentDetails('ficknury')" class="btn-primary">View Details</button>
          <button @click="assignTask('ficknury')" class="btn-secondary">Assign Task</button>
        </div>
      </div>
    </div>

    <!-- Agent Performance Dashboard -->
    <div class="performance-dashboard">
      <h2 class="dashboard-title">📊 Agent Performance Dashboard</h2>
      
      <div class="dashboard-grid">
        <!-- Task Completion Trends -->
        <div class="dashboard-card">
          <h3>Task Completion Trends</h3>
          <div class="trend-chart">
            <div class="chart-bar" style="height: 80%">
              <span class="bar-label">Katie</span>
              <span class="bar-value">80%</span>
            </div>
            <div class="chart-bar" style="height: 65%">
              <span class="bar-label">Igris</span>
              <span class="bar-value">65%</span>
            </div>
            <div class="chart-bar" style="height: 90%">
              <span class="bar-label">FickNury</span>
              <span class="bar-value">90%</span>
            </div>
          </div>
        </div>

        <!-- Response Time Metrics -->
        <div class="dashboard-card">
          <h3>Average Response Time</h3>
          <div class="response-times">
            <div class="response-item">
              <span class="agent-name">Katie</span>
              <span class="response-time">{{ katieStats.avgResponseTime }}ms</span>
            </div>
            <div class="response-item">
              <span class="agent-name">Igris</span>
              <span class="response-time">{{ igrisStats.avgResponseTime }}ms</span>
            </div>
            <div class="response-item">
              <span class="agent-name">FickNury</span>
              <span class="response-time">{{ ficknuryStats.avgResponseTime }}ms</span>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="dashboard-card">
          <h3>Recent Activity</h3>
          <div class="activity-feed">
            <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
              <div class="activity-icon">{{ activity.icon }}</div>
              <div class="activity-content">
                <p class="activity-text">{{ activity.text }}</p>
                <span class="activity-time">{{ formatTime(activity.timestamp) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- System Health -->
        <div class="dashboard-card">
          <h3>System Health</h3>
          <div class="health-metrics">
            <div class="health-item">
              <span class="health-label">CPU Usage</span>
              <div class="health-bar">
                <div class="health-fill" :style="{ width: systemHealth.cpu + '%' }"></div>
              </div>
              <span class="health-value">{{ systemHealth.cpu }}%</span>
            </div>
            <div class="health-item">
              <span class="health-label">Memory Usage</span>
              <div class="health-bar">
                <div class="health-fill" :style="{ width: systemHealth.memory + '%' }"></div>
              </div>
              <span class="health-value">{{ systemHealth.memory }}%</span>
            </div>
            <div class="health-item">
              <span class="health-label">Network</span>
              <div class="health-bar">
                <div class="health-fill" :style="{ width: systemHealth.network + '%' }"></div>
              </div>
              <span class="health-value">{{ systemHealth.network }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'Agents',
  setup() {
    const katieStats = ref({
      tasksCompleted: 1247,
      successRate: 94,
      uptime: 168,
      avgResponseTime: 245
    })

    const igrisStats = ref({
      tasksCompleted: 892,
      successRate: 87,
      uptime: 156,
      avgResponseTime: 189
    })

    const ficknuryStats = ref({
      tasksCompleted: 2156,
      successRate: 96,
      uptime: 192,
      avgResponseTime: 156
    })

    const systemHealth = ref({
      cpu: 45,
      memory: 62,
      network: 78
    })

    const recentActivity = ref([
      {
        id: 1,
        icon: '👩‍💻',
        text: 'Katie completed data analysis task #1247',
        timestamp: new Date(Date.now() - 300000)
      },
      {
        id: 2,
        icon: '🤖',
        text: 'Igris integrated new API endpoint',
        timestamp: new Date(Date.now() - 600000)
      },
      {
        id: 3,
        icon: '⚡',
        text: 'FickNury evaluated deployment for task #2156',
        timestamp: new Date(Date.now() - 900000)
      },
      {
        id: 4,
        icon: '👩‍💻',
        text: 'Katie generated monthly report',
        timestamp: new Date(Date.now() - 1200000)
      }
    ])

    const viewAgentDetails = (agent) => {
      console.log(`Viewing details for ${agent}`)
      // Navigate to detailed agent view
    }

    const assignTask = (agent) => {
      console.log(`Assigning task to ${agent}`)
      // Open task assignment modal
    }

    const formatTime = (timestamp) => {
      const now = new Date()
      const diff = now - timestamp
      const minutes = Math.floor(diff / 60000)
      
      if (minutes < 1) return 'Just now'
      if (minutes < 60) return `${minutes}m ago`
      
      const hours = Math.floor(minutes / 60)
      if (hours < 24) return `${hours}h ago`
      
      const days = Math.floor(hours / 24)
      return `${days}d ago`
    }

    onMounted(() => {
      // Initialize real-time updates
      setInterval(() => {
        // Update stats periodically
        katieStats.value.tasksCompleted += Math.floor(Math.random() * 3)
        igrisStats.value.tasksCompleted += Math.floor(Math.random() * 2)
        ficknuryStats.value.tasksCompleted += Math.floor(Math.random() * 4)
      }, 30000)
    })

    return {
      katieStats,
      igrisStats,
      ficknuryStats,
      systemHealth,
      recentActivity,
      viewAgentDetails,
      assignTask,
      formatTime
    }
  }
}
</script>

<style scoped>
.agents-page {
  min-height: 100vh;
}

.page-header {
  margin-bottom: 2rem;
  text-align: center;
}

.page-title {
  font-size: 2.5rem;
  color: #00ffff;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  margin-bottom: 0.5rem;
}

.page-subtitle {
  color: #888;
  font-size: 1.1rem;
}

.agents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.agent-card {
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 15px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 0 30px rgba(0, 255, 255, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.agent-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, 
    rgba(0, 255, 255, 0.05) 0%, 
    transparent 50%, 
    rgba(255, 0, 255, 0.05) 100%);
  pointer-events: none;
}

.agent-card:hover {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 40px rgba(0, 255, 255, 0.2);
  transform: translateY(-5px);
}

.agent-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.agent-avatar {
  font-size: 3rem;
  filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.5));
}

.agent-info {
  flex: 1;
}

.agent-name {
  color: #00ffff;
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.agent-title {
  color: #888;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.agent-status {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  display: inline-block;
}

.agent-status.online {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
}

.agent-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(0, 255, 255, 0.05);
  border-radius: 10px;
}

.stat {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #00ffff;
}

.stat-label {
  font-size: 0.8rem;
  color: #888;
}

.agent-description {
  margin-bottom: 1.5rem;
}

.agent-description p {
  color: #ccc;
  line-height: 1.6;
}

.agent-capabilities h4 {
  color: #00ffff;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.capability-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.capability-tag {
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

.agent-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

/* Performance Dashboard */
.performance-dashboard {
  margin-top: 3rem;
}

.dashboard-title {
  color: #00ffff;
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.dashboard-card {
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 15px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
}

.dashboard-card h3 {
  color: #00ffff;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

/* Trend Chart */
.trend-chart {
  display: flex;
  align-items: end;
  gap: 1rem;
  height: 150px;
}

.chart-bar {
  flex: 1;
  background: linear-gradient(to top, #00ffff, #0080ff);
  border-radius: 4px 4px 0 0;
  position: relative;
  min-height: 20px;
}

.bar-label {
  position: absolute;
  bottom: -25px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.8rem;
  color: #888;
}

.bar-value {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.8rem;
  color: #00ffff;
  font-weight: bold;
}

/* Response Times */
.response-times {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.response-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: rgba(0, 255, 255, 0.05);
  border-radius: 8px;
}

.agent-name {
  color: #00ffff;
  font-weight: 500;
}

.response-time {
  color: #fff;
  font-weight: bold;
}

/* Activity Feed */
.activity-feed {
  max-height: 200px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  font-size: 1.2rem;
}

.activity-content {
  flex: 1;
}

.activity-text {
  color: #ccc;
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

.activity-time {
  color: #888;
  font-size: 0.8rem;
}

/* Health Metrics */
.health-metrics {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.health-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.health-label {
  color: #ccc;
  min-width: 100px;
  font-size: 0.9rem;
}

.health-bar {
  flex: 1;
  height: 8px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
  overflow: hidden;
}

.health-fill {
  height: 100%;
  background: linear-gradient(90deg, #00ffff, #0080ff);
  transition: width 0.3s ease;
}

.health-value {
  color: #00ffff;
  font-weight: bold;
  min-width: 50px;
  text-align: right;
}

/* Buttons */
.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  flex: 1;
}

.btn-primary {
  background: linear-gradient(45deg, #00ffff, #0080ff);
  color: #000;
}

.btn-secondary {
  background: linear-gradient(45deg, #ff6b6b, #ff8e53);
  color: #fff;
}

.btn-primary:hover, .btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .agents-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .agent-stats {
    flex-direction: column;
    gap: 1rem;
  }
  
  .agent-actions {
    flex-direction: column;
  }
  
  .trend-chart {
    height: 120px;
  }
}
</style> 