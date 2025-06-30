<template>
  <div class="whis-smithing-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">🔨 Whis Smithing</h1>
      <p class="text-gray-300">AI Forge - Learning Artifacts Factory</p>
    </div>

    <!-- Approval Queue -->
    <div class="glass-panel p-8 mb-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">⚖️ Approval Queue</h2>
      
      <div v-if="approvalQueue.length === 0" class="text-center py-8">
        <div class="text-4xl mb-4">🎉</div>
        <p class="text-gray-300">No pending smithing outputs to approve</p>
      </div>

      <div v-else class="space-y-6">
        <div 
          v-for="item in approvalQueue" 
          :key="item.id"
          class="approval-item glass-panel p-6 rounded-lg border border-gray-600"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <h3 class="text-lg font-medium mb-2">{{ item.task_title }}</h3>
              <div class="flex items-center space-x-4 text-sm text-gray-400 mb-3">
                <span>Confidence: {{ item.confidence_score }}%</span>
                <span>Source: {{ item.source }}</span>
                <span>{{ item.timestamp }}</span>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <span 
                class="px-3 py-1 rounded-full text-xs font-medium"
                :class="{
                  'bg-green-500 text-white': item.confidence_score >= 80,
                  'bg-yellow-500 text-black': item.confidence_score >= 60 && item.confidence_score < 80,
                  'bg-red-500 text-white': item.confidence_score < 60
                }"
              >
                {{ item.confidence_score >= 80 ? 'High' : item.confidence_score >= 60 ? 'Medium' : 'Low' }}
              </span>
            </div>
          </div>

          <!-- Original Task -->
          <div class="mb-4">
            <h4 class="text-sm font-medium text-blue-400 mb-2">📝 Original Task</h4>
            <div class="bg-gray-800 p-3 rounded text-sm">
              {{ item.original_task }}
            </div>
          </div>

          <!-- Proposed Rune -->
          <div class="mb-4">
            <h4 class="text-sm font-medium text-green-400 mb-2">🧾 Proposed Rune</h4>
            <div class="bg-gray-800 p-3 rounded">
              <pre class="text-sm text-gray-300">{{ item.proposed_rune }}</pre>
            </div>
          </div>

          <!-- Proposed Orb -->
          <div class="mb-4">
            <h4 class="text-sm font-medium text-purple-400 mb-2">💡 Proposed Orb</h4>
            <div class="bg-gray-800 p-3 rounded">
              <p class="text-sm text-gray-300">{{ item.proposed_orb }}</p>
              <div class="flex flex-wrap gap-2 mt-2">
                <span 
                  v-for="tag in item.orb_tags" 
                  :key="tag"
                  class="px-2 py-1 bg-purple-600 text-white text-xs rounded"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center space-x-3">
            <button 
              @click="approveItem(item.id)"
              class="bg-green-500 hover:bg-green-600 px-4 py-2 rounded font-medium transition-colors"
            >
              ✅ Approve
            </button>
            <button 
              @click="denyItem(item.id)"
              class="bg-red-500 hover:bg-red-600 px-4 py-2 rounded font-medium transition-colors"
            >
              ❌ Deny
            </button>
            <button 
              @click="editItem(item)"
              class="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded font-medium transition-colors"
            >
              ✏️ Edit
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Dashboard -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-blue-400 mb-2">{{ stats.pending }}</div>
        <div class="text-sm text-gray-300">Pending Approval</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-green-400 mb-2">{{ stats.approved }}</div>
        <div class="text-sm text-gray-300">Approved Today</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-purple-400 mb-2">{{ stats.runes }}</div>
        <div class="text-sm text-gray-300">Total Runes</div>
      </div>
      <div class="glass-panel p-6 text-center">
        <div class="text-3xl font-bold text-yellow-400 mb-2">{{ stats.orbs }}</div>
        <div class="text-sm text-gray-300">Total Orbs</div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="glass-panel p-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">📊 Recent Activity</h2>
      <div class="space-y-3">
        <div 
          v-for="activity in recentActivity" 
          :key="activity.id"
          class="activity-item p-3 rounded-lg border border-gray-600"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="text-2xl">{{ activity.icon }}</div>
              <div>
                <p class="text-sm font-medium">{{ activity.action }}</p>
                <p class="text-xs text-gray-400">{{ activity.description }}</p>
              </div>
            </div>
            <div class="text-xs text-gray-400">{{ activity.timestamp }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="glass-panel p-8 rounded-lg max-w-2xl w-full mx-4">
        <h3 class="text-xl font-medium mb-4">✏️ Edit Smithing Output</h3>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2">Rune</label>
            <textarea 
              v-model="editForm.rune" 
              class="w-full h-32 bg-gray-800 p-3 rounded text-sm"
              placeholder="Edit the proposed rune..."
            ></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-2">Orb</label>
            <textarea 
              v-model="editForm.orb" 
              class="w-full h-24 bg-gray-800 p-3 rounded text-sm"
              placeholder="Edit the proposed orb..."
            ></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-2">Tags</label>
            <input 
              v-model="editForm.tags" 
              class="w-full bg-gray-800 p-3 rounded text-sm"
              placeholder="Comma-separated tags..."
            />
          </div>
        </div>
        
        <div class="flex items-center space-x-3 mt-6">
          <button 
            @click="saveEdit"
            class="bg-green-500 hover:bg-green-600 px-4 py-2 rounded font-medium"
          >
            💾 Save & Approve
          </button>
          <button 
            @click="cancelEdit"
            class="bg-gray-500 hover:bg-gray-600 px-4 py-2 rounded font-medium"
          >
            ❌ Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { whisService } from '@/services/api'

export default {
  name: 'WhisSmithing',
  setup() {
    const approvalQueue = ref([])
    const stats = ref({
      pending: 0,
      approved: 0,
      runes: 0,
      orbs: 0
    })
    const recentActivity = ref([])
    const showEditModal = ref(false)
    const editForm = ref({
      id: null,
      rune: '',
      orb: '',
      tags: ''
    })

    // Mock data for demonstration
    const loadMockData = () => {
      approvalQueue.value = [
        {
          id: 1,
          task_title: "Deploy Kubernetes Cluster",
          original_task: "Set up a production-ready Kubernetes cluster with proper security configurations",
          proposed_rune: `#!/bin/bash
# Deploy Kubernetes cluster with security best practices
kubectl create namespace production
kubectl apply -f security-policies/
kubectl apply -f monitoring/
kubectl apply -f ingress-controller/`,
          proposed_orb: "Always implement security policies and monitoring before deploying production workloads. Use namespace isolation and proper RBAC configurations.",
          orb_tags: ["kubernetes", "security", "production"],
          confidence_score: 85,
          source: "task_input",
          timestamp: "2 minutes ago"
        },
        {
          id: 2,
          task_title: "Database Migration Script",
          original_task: "Create a script to safely migrate data from MySQL to PostgreSQL",
          proposed_rune: `#!/bin/bash
# Database migration script
pg_dump mysql_db > backup.sql
psql postgresql_db < backup.sql
python3 validate_migration.py`,
          proposed_orb: "Always backup data before migration and validate the results. Use transaction logs for rollback capability.",
          orb_tags: ["database", "migration", "backup"],
          confidence_score: 72,
          source: "youtube_transcript",
          timestamp: "15 minutes ago"
        }
      ]

      stats.value = {
        pending: 2,
        approved: 12,
        runes: 156,
        orbs: 89
      }

      recentActivity.value = [
        {
          id: 1,
          icon: "✅",
          action: "Approved Rune",
          description: "Kubernetes deployment script approved",
          timestamp: "5 minutes ago"
        },
        {
          id: 2,
          icon: "💡",
          action: "New Orb Created",
          description: "Security best practices for container deployments",
          timestamp: "12 minutes ago"
        },
        {
          id: 3,
          icon: "❌",
          action: "Denied Output",
          description: "Incomplete Terraform configuration rejected",
          timestamp: "1 hour ago"
        }
      ]
    }

    const approveItem = async (id) => {
      try {
        await whisService.approveSmithingOutput(id)
        approvalQueue.value = approvalQueue.value.filter(item => item.id !== id)
        stats.value.pending--
        stats.value.approved++
        // Add to recent activity
        recentActivity.value.unshift({
          id: Date.now(),
          icon: "✅",
          action: "Approved Rune/Orb",
          description: "Smithing output approved and sent to enhancement",
          timestamp: "Just now"
        })
      } catch (error) {
        console.error('Failed to approve item:', error)
      }
    }

    const denyItem = async (id) => {
      try {
        await whisService.denySmithingOutput(id)
        approvalQueue.value = approvalQueue.value.filter(item => item.id !== id)
        stats.value.pending--
        // Add to recent activity
        recentActivity.value.unshift({
          id: Date.now(),
          icon: "❌",
          action: "Denied Output",
          description: "Smithing output rejected",
          timestamp: "Just now"
        })
      } catch (error) {
        console.error('Failed to deny item:', error)
      }
    }

    const editItem = (item) => {
      editForm.value = {
        id: item.id,
        rune: item.proposed_rune,
        orb: item.proposed_orb,
        tags: item.orb_tags.join(', ')
      }
      showEditModal.value = true
    }

    const saveEdit = async () => {
      try {
        await whisService.updateSmithingOutput(editForm.value.id, {
          rune: editForm.value.rune,
          orb: editForm.value.orb,
          tags: editForm.value.tags.split(',').map(tag => tag.trim())
        })
        
        // Update the item in the queue
        const item = approvalQueue.value.find(i => i.id === editForm.value.id)
        if (item) {
          item.proposed_rune = editForm.value.rune
          item.proposed_orb = editForm.value.orb
          item.orb_tags = editForm.value.tags.split(',').map(tag => tag.trim())
        }
        
        showEditModal.value = false
        // Add to recent activity
        recentActivity.value.unshift({
          id: Date.now(),
          icon: "✏️",
          action: "Updated Output",
          description: "Smithing output edited and approved",
          timestamp: "Just now"
        })
      } catch (error) {
        console.error('Failed to save edit:', error)
      }
    }

    const cancelEdit = () => {
      showEditModal.value = false
      editForm.value = { id: null, rune: '', orb: '', tags: '' }
    }

    onMounted(() => {
      loadMockData()
      // In production, load real data:
      // whisService.getApprovalQueue()
      // whisService.getSmithingStats()
      // whisService.getRecentActivity()
    })

    return {
      approvalQueue,
      stats,
      recentActivity,
      showEditModal,
      editForm,
      approveItem,
      denyItem,
      editItem,
      saveEdit,
      cancelEdit
    }
  }
}
</script>

<style scoped>
.whis-smithing-container {
  max-width: 1400px;
  margin: 0 auto;
}

.approval-item, .activity-item {
  transition: all 0.3s ease;
}

.approval-item:hover, .activity-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
</style> 