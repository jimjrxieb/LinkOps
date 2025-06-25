<template>
  <div class="whis-page">
    <div class="page-header">
      <h1 class="page-title">🧠 Whis - AI Training System</h1>
      <p class="page-subtitle">Neural Network Training & Knowledge Management</p>
    </div>

    <div class="content-grid">
      <!-- AI Training Queue -->
      <div class="card training-queue">
        <h3 class="card-title">🔄 Training Queue</h3>
        <div class="queue-stats">
          <div class="stat">
            <span class="stat-number">{{ queueStats.pending }}</span>
            <span class="stat-label">Pending</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ queueStats.processing }}</span>
            <span class="stat-label">Processing</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ queueStats.completed }}</span>
            <span class="stat-label">Completed</span>
          </div>
        </div>
        
        <div class="queue-items">
          <div v-for="item in trainingQueue" :key="item.id" class="queue-item" :class="item.status">
            <div class="item-header">
              <span class="item-type">{{ item.type }}</span>
              <span class="item-status">{{ item.status }}</span>
            </div>
            <p class="item-description">{{ item.description }}</p>
            <div class="item-progress" v-if="item.status === 'processing'">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: item.progress + '%' }"></div>
              </div>
              <span class="progress-text">{{ item.progress }}%</span>
            </div>
            <div class="item-actions">
              <button v-if="item.status === 'pending'" @click="startTraining(item.id)" class="btn-small">Start</button>
              <button v-if="item.status === 'processing'" @click="pauseTraining(item.id)" class="btn-small">Pause</button>
              <button @click="removeFromQueue(item.id)" class="btn-small btn-danger">Remove</button>
            </div>
          </div>
        </div>
        
        <button @click="addToQueue" class="btn-primary">Add Training Item</button>
      </div>

      <!-- Daily Digest Viewer -->
      <div class="card digest-viewer">
        <h3 class="card-title">📊 Daily Digest</h3>
        <div class="digest-controls">
          <input v-model="digestDate" type="date" class="form-input" />
          <button @click="loadDigest" class="btn-secondary">Load Digest</button>
        </div>
        
        <div v-if="currentDigest" class="digest-content">
          <div class="digest-summary">
            <h4>Summary</h4>
            <p>{{ currentDigest.summary }}</p>
          </div>
          
          <div class="digest-stats">
            <div class="digest-stat">
              <span class="stat-number">{{ currentDigest.stats.trainingItems }}</span>
              <span class="stat-label">Training Items</span>
            </div>
            <div class="digest-stat">
              <span class="stat-number">{{ currentDigest.stats.newRunes }}</span>
              <span class="stat-label">New Runes</span>
            </div>
            <div class="digest-stat">
              <span class="stat-number">{{ currentDigest.stats.newOrbs }}</span>
              <span class="stat-label">New Orbs</span>
            </div>
          </div>
          
          <div class="digest-highlights">
            <h4>Key Highlights</h4>
            <ul>
              <li v-for="highlight in currentDigest.highlights" :key="highlight">{{ highlight }}</li>
            </ul>
          </div>
        </div>
        
        <div v-else class="no-digest">
          <p>Select a date to view the digest</p>
        </div>
      </div>

      <!-- Rune + Orb Approval Queue -->
      <div class="card approval-queue">
        <h3 class="card-title">⚡ Approval Queue</h3>
        <div class="queue-tabs">
          <button 
            @click="activeTab = 'runes'" 
            :class="{ active: activeTab === 'runes' }" 
            class="tab-btn"
          >
            Runes ({{ runeQueue.length }})
          </button>
          <button 
            @click="activeTab = 'orbs'" 
            :class="{ active: activeTab === 'orbs' }" 
            class="tab-btn"
          >
            Orbs ({{ orbQueue.length }})
          </button>
        </div>
        
        <div v-if="activeTab === 'runes'" class="queue-content">
          <div v-for="rune in runeQueue" :key="rune.id" class="approval-item">
            <div class="item-preview">
              <h4>{{ rune.name }}</h4>
              <p class="item-description">{{ rune.description }}</p>
              <div class="item-meta">
                <span class="meta-tag">Confidence: {{ rune.confidence }}%</span>
                <span class="meta-tag">Created: {{ formatDate(rune.createdAt) }}</span>
              </div>
            </div>
            <div class="item-actions">
              <button @click="approveItem('rune', rune.id)" class="btn-small btn-success">Approve</button>
              <button @click="rejectItem('rune', rune.id)" class="btn-small btn-danger">Reject</button>
              <button @click="viewDetails('rune', rune.id)" class="btn-small">View</button>
            </div>
          </div>
        </div>
        
        <div v-if="activeTab === 'orbs'" class="queue-content">
          <div v-for="orb in orbQueue" :key="orb.id" class="approval-item">
            <div class="item-preview">
              <h4>{{ orb.name }}</h4>
              <p class="item-description">{{ orb.description }}</p>
              <div class="item-meta">
                <span class="meta-tag">Confidence: {{ orb.confidence }}%</span>
                <span class="meta-tag">Created: {{ formatDate(orb.createdAt) }}</span>
              </div>
            </div>
            <div class="item-actions">
              <button @click="approveItem('orb', orb.id)" class="btn-small btn-success">Approve</button>
              <button @click="rejectItem('orb', orb.id)" class="btn-small btn-danger">Reject</button>
              <button @click="viewDetails('orb', orb.id)" class="btn-small">View</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Training Analytics -->
      <div class="card analytics">
        <h3 class="card-title">📈 Training Analytics</h3>
        <div class="analytics-grid">
          <div class="analytics-card">
            <h4>Training Success Rate</h4>
            <div class="analytics-value">{{ analytics.successRate }}%</div>
            <div class="analytics-chart">
              <div class="chart-bar" :style="{ width: analytics.successRate + '%' }"></div>
            </div>
          </div>
          
          <div class="analytics-card">
            <h4>Knowledge Growth</h4>
            <div class="analytics-value">{{ analytics.knowledgeGrowth }}</div>
            <div class="analytics-trend positive">+{{ analytics.growthRate }}%</div>
          </div>
          
          <div class="analytics-card">
            <h4>Active Runes</h4>
            <div class="analytics-value">{{ analytics.activeRunes }}</div>
            <div class="analytics-trend positive">+{{ analytics.runeGrowth }}%</div>
          </div>
          
          <div class="analytics-card">
            <h4>Active Orbs</h4>
            <div class="analytics-value">{{ analytics.activeOrbs }}</div>
            <div class="analytics-trend positive">+{{ analytics.orbGrowth }}%</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'Whis',
  setup() {
    const activeTab = ref('runes')
    const digestDate = ref(new Date().toISOString().split('T')[0])
    const currentDigest = ref(null)

    const queueStats = ref({
      pending: 5,
      processing: 2,
      completed: 23
    })

    const trainingQueue = ref([
      {
        id: 1,
        type: 'Text Analysis',
        status: 'processing',
        description: 'Analyzing system logs for patterns',
        progress: 65
      },
      {
        id: 2,
        type: 'Code Review',
        status: 'pending',
        description: 'Reviewing Kubernetes deployment scripts',
        progress: 0
      },
      {
        id: 3,
        type: 'Data Processing',
        status: 'completed',
        description: 'Processing user feedback data',
        progress: 100
      }
    ])

    const runeQueue = ref([
      {
        id: 1,
        name: 'Kubernetes Debug Pattern',
        description: 'Automated debugging for common K8s issues',
        confidence: 92,
        createdAt: new Date(Date.now() - 86400000)
      },
      {
        id: 2,
        name: 'Database Optimization',
        description: 'PostgreSQL query optimization patterns',
        confidence: 87,
        createdAt: new Date(Date.now() - 172800000)
      }
    ])

    const orbQueue = ref([
      {
        id: 1,
        name: 'System Monitoring Orb',
        description: 'Comprehensive system health monitoring',
        confidence: 94,
        createdAt: new Date(Date.now() - 43200000)
      },
      {
        id: 2,
        name: 'Security Scan Orb',
        description: 'Automated security vulnerability scanning',
        confidence: 89,
        createdAt: new Date(Date.now() - 129600000)
      }
    ])

    const analytics = ref({
      successRate: 87,
      knowledgeGrowth: '2.3TB',
      growthRate: 12,
      activeRunes: 156,
      runeGrowth: 8,
      activeOrbs: 89,
      orbGrowth: 15
    })

    const startTraining = (id) => {
      const item = trainingQueue.value.find(item => item.id === id)
      if (item) {
        item.status = 'processing'
        item.progress = 0
        // Simulate progress
        const interval = setInterval(() => {
          item.progress += Math.random() * 10
          if (item.progress >= 100) {
            item.progress = 100
            item.status = 'completed'
            clearInterval(interval)
          }
        }, 1000)
      }
    }

    const pauseTraining = (id) => {
      const item = trainingQueue.value.find(item => item.id === id)
      if (item) {
        item.status = 'pending'
      }
    }

    const removeFromQueue = (id) => {
      trainingQueue.value = trainingQueue.value.filter(item => item.id !== id)
    }

    const addToQueue = () => {
      const newItem = {
        id: Date.now(),
        type: 'Custom Training',
        status: 'pending',
        description: 'New training item added',
        progress: 0
      }
      trainingQueue.value.push(newItem)
    }

    const loadDigest = () => {
      // Mock digest data
      currentDigest.value = {
        summary: 'Today was a productive day for AI training. The system processed 45 new training items and generated 12 new runes and 8 new orbs.',
        stats: {
          trainingItems: 45,
          newRunes: 12,
          newOrbs: 8
        },
        highlights: [
          'Improved accuracy in Kubernetes debugging patterns',
          'New security scanning capabilities added',
          'Database optimization patterns refined',
          'System monitoring enhanced with new metrics'
        ]
      }
    }

    const approveItem = (type, id) => {
      if (type === 'rune') {
        runeQueue.value = runeQueue.value.filter(item => item.id !== id)
      } else {
        orbQueue.value = orbQueue.value.filter(item => item.id !== id)
      }
    }

    const rejectItem = (type, id) => {
      if (type === 'rune') {
        runeQueue.value = runeQueue.value.filter(item => item.id !== id)
      } else {
        orbQueue.value = orbQueue.value.filter(item => item.id !== id)
      }
    }

    const viewDetails = (type, id) => {
      console.log(`Viewing details for ${type} ${id}`)
    }

    const formatDate = (date) => {
      return new Intl.DateTimeFormat('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    }

    onMounted(() => {
      loadDigest()
    })

    return {
      activeTab,
      digestDate,
      currentDigest,
      queueStats,
      trainingQueue,
      runeQueue,
      orbQueue,
      analytics,
      startTraining,
      pauseTraining,
      removeFromQueue,
      addToQueue,
      loadDigest,
      approveItem,
      rejectItem,
      viewDetails,
      formatDate
    }
  }
}
</script>

<style scoped>
.whis-page {
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

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2rem;
}

.card {
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 15px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 0 30px rgba(0, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.card:hover {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 40px rgba(0, 255, 255, 0.2);
  transform: translateY(-5px);
}

.card-title {
  color: #00ffff;
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

/* Queue Stats */
.queue-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 2rem;
  padding: 1rem;
  background: rgba(0, 255, 255, 0.05);
  border-radius: 10px;
}

.stat {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: bold;
  color: #00ffff;
}

.stat-label {
  font-size: 0.9rem;
  color: #888;
}

/* Queue Items */
.queue-items {
  margin-bottom: 1.5rem;
}

.queue-item {
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.queue-item.processing {
  border-color: #ffaa00;
  box-shadow: 0 0 15px rgba(255, 170, 0, 0.3);
}

.queue-item.completed {
  border-color: #00ff00;
  box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.item-type {
  font-weight: bold;
  color: #00ffff;
}

.item-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  text-transform: uppercase;
}

.item-status.pending {
  background: rgba(255, 170, 0, 0.2);
  color: #ffaa00;
}

.item-status.processing {
  background: rgba(0, 255, 255, 0.2);
  color: #00ffff;
}

.item-status.completed {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
}

.item-description {
  color: #ccc;
  margin-bottom: 1rem;
}

.item-progress {
  margin-bottom: 1rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00ffff, #0080ff);
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.8rem;
  color: #888;
}

.item-actions {
  display: flex;
  gap: 0.5rem;
}

/* Digest Controls */
.digest-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-input {
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  color: #fff;
  flex: 1;
}

.digest-content {
  background: rgba(0, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 10px;
  padding: 1.5rem;
}

.digest-summary {
  margin-bottom: 1.5rem;
}

.digest-summary h4 {
  color: #00ffff;
  margin-bottom: 0.5rem;
}

.digest-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1.5rem;
}

.digest-stat {
  text-align: center;
}

.digest-highlights h4 {
  color: #00ffff;
  margin-bottom: 0.5rem;
}

.digest-highlights ul {
  list-style: none;
  padding: 0;
}

.digest-highlights li {
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(0, 255, 255, 0.1);
}

.digest-highlights li:last-child {
  border-bottom: none;
}

/* Approval Queue */
.queue-tabs {
  display: flex;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(0, 255, 255, 0.3);
}

.tab-btn {
  background: none;
  border: none;
  color: #888;
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 2px solid transparent;
}

.tab-btn.active {
  color: #00ffff;
  border-bottom-color: #00ffff;
}

.approval-item {
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-preview h4 {
  color: #00ffff;
  margin-bottom: 0.5rem;
}

.item-meta {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.meta-tag {
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

/* Analytics */
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.analytics-card {
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 10px;
  padding: 1rem;
  text-align: center;
}

.analytics-card h4 {
  color: #888;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.analytics-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #00ffff;
  margin-bottom: 0.5rem;
}

.analytics-trend {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.analytics-trend.positive {
  background: rgba(0, 255, 0, 0.2);
  color: #00ff00;
}

.analytics-chart {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
  overflow: hidden;
}

.chart-bar {
  height: 100%;
  background: linear-gradient(90deg, #00ffff, #0080ff);
  transition: width 0.3s ease;
}

/* Buttons */
.btn-primary, .btn-secondary, .btn-small {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-primary {
  background: linear-gradient(45deg, #00ffff, #0080ff);
  color: #000;
}

.btn-secondary {
  background: linear-gradient(45deg, #ff6b6b, #ff8e53);
  color: #fff;
}

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
}

.btn-success {
  background: linear-gradient(45deg, #00ff00, #00cc00);
  color: #000;
}

.btn-danger {
  background: linear-gradient(45deg, #ff0000, #cc0000);
  color: #fff;
}

.btn-primary:hover, .btn-secondary:hover, .btn-small:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .queue-stats, .digest-stats {
    flex-direction: column;
    gap: 1rem;
  }
  
  .approval-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .item-actions {
    width: 100%;
    justify-content: space-between;
  }
}
</style> 