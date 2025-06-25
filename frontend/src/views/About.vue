<template>
  <div class="about-page">
    <div class="page-header">
      <h1 class="page-title">ℹ️ About LinkOps</h1>
      <p class="page-subtitle">AI Agent Profiles & System Information</p>
    </div>

    <div class="profiles-grid">
      <!-- Whis Profile -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="profile-avatar">🧠</div>
          <div class="profile-info">
            <h3 class="profile-name">Whis</h3>
            <p class="profile-title">AI Training System</p>
          </div>
          <button @click="editProfile('whis')" class="edit-btn">✏️</button>
        </div>
        
        <div class="profile-content">
          <div v-if="!editing.whis" class="profile-bio">
            <p>{{ profiles.whis.bio }}</p>
          </div>
          <div v-else class="profile-edit">
            <textarea 
              v-model="profiles.whis.bio" 
              class="bio-textarea"
              rows="4"
              placeholder="Enter Whis's bio..."
            ></textarea>
            <div class="edit-actions">
              <button @click="saveProfile('whis')" class="btn-save">Save</button>
              <button @click="cancelEdit('whis')" class="btn-cancel">Cancel</button>
            </div>
          </div>
          
          <div class="profile-avatar-section">
            <h4>Avatar</h4>
            <div class="avatar-upload">
              <img v-if="profiles.whis.avatar" :src="profiles.whis.avatar" alt="Whis Avatar" class="avatar-preview" />
              <div v-else class="avatar-placeholder">🧠</div>
              <input 
                type="file" 
                @change="handleAvatarUpload('whis', $event)" 
                accept="image/*"
                class="avatar-input"
              />
              <label class="avatar-label">Change Avatar</label>
            </div>
          </div>
        </div>
      </div>

      <!-- James Profile -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="profile-avatar">🤖</div>
          <div class="profile-info">
            <h3 class="profile-name">James</h3>
            <p class="profile-title">AI Assistant</p>
          </div>
          <button @click="editProfile('james')" class="edit-btn">✏️</button>
        </div>
        
        <div class="profile-content">
          <div v-if="!editing.james" class="profile-bio">
            <p>{{ profiles.james.bio }}</p>
          </div>
          <div v-else class="profile-edit">
            <textarea 
              v-model="profiles.james.bio" 
              class="bio-textarea"
              rows="4"
              placeholder="Enter James's bio..."
            ></textarea>
            <div class="edit-actions">
              <button @click="saveProfile('james')" class="btn-save">Save</button>
              <button @click="cancelEdit('james')" class="btn-cancel">Cancel</button>
            </div>
          </div>
          
          <div class="profile-avatar-section">
            <h4>Avatar</h4>
            <div class="avatar-upload">
              <img v-if="profiles.james.avatar" :src="profiles.james.avatar" alt="James Avatar" class="avatar-preview" />
              <div v-else class="avatar-placeholder">🤖</div>
              <input 
                type="file" 
                @change="handleAvatarUpload('james', $event)" 
                accept="image/*"
                class="avatar-input"
              />
              <label class="avatar-label">Change Avatar</label>
            </div>
          </div>
        </div>
      </div>

      <!-- Katie Profile -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="profile-avatar">👩‍💻</div>
          <div class="profile-info">
            <h3 class="profile-name">Katie</h3>
            <p class="profile-title">Data Processing Specialist</p>
          </div>
          <button @click="editProfile('katie')" class="edit-btn">✏️</button>
        </div>
        
        <div class="profile-content">
          <div v-if="!editing.katie" class="profile-bio">
            <p>{{ profiles.katie.bio }}</p>
          </div>
          <div v-else class="profile-edit">
            <textarea 
              v-model="profiles.katie.bio" 
              class="bio-textarea"
              rows="4"
              placeholder="Enter Katie's bio..."
            ></textarea>
            <div class="edit-actions">
              <button @click="saveProfile('katie')" class="btn-save">Save</button>
              <button @click="cancelEdit('katie')" class="btn-cancel">Cancel</button>
            </div>
          </div>
          
          <div class="profile-avatar-section">
            <h4>Avatar</h4>
            <div class="avatar-upload">
              <img v-if="profiles.katie.avatar" :src="profiles.katie.avatar" alt="Katie Avatar" class="avatar-preview" />
              <div v-else class="avatar-placeholder">👩‍💻</div>
              <input 
                type="file" 
                @change="handleAvatarUpload('katie', $event)" 
                accept="image/*"
                class="avatar-input"
              />
              <label class="avatar-label">Change Avatar</label>
            </div>
          </div>
        </div>
      </div>

      <!-- Igris Profile -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="profile-avatar">🔗</div>
          <div class="profile-info">
            <h3 class="profile-name">Igris</h3>
            <p class="profile-title">System Integration Expert</p>
          </div>
          <button @click="editProfile('igris')" class="edit-btn">✏️</button>
        </div>
        
        <div class="profile-content">
          <div v-if="!editing.igris" class="profile-bio">
            <p>{{ profiles.igris.bio }}</p>
          </div>
          <div v-else class="profile-edit">
            <textarea 
              v-model="profiles.igris.bio" 
              class="bio-textarea"
              rows="4"
              placeholder="Enter Igris's bio..."
            ></textarea>
            <div class="edit-actions">
              <button @click="saveProfile('igris')" class="btn-save">Save</button>
              <button @click="cancelEdit('igris')" class="btn-cancel">Cancel</button>
            </div>
          </div>
          
          <div class="profile-avatar-section">
            <h4>Avatar</h4>
            <div class="avatar-upload">
              <img v-if="profiles.igris.avatar" :src="profiles.igris.avatar" alt="Igris Avatar" class="avatar-preview" />
              <div v-else class="avatar-placeholder">🔗</div>
              <input 
                type="file" 
                @change="handleAvatarUpload('igris', $event)" 
                accept="image/*"
                class="avatar-input"
              />
              <label class="avatar-label">Change Avatar</label>
            </div>
          </div>
        </div>
      </div>

      <!-- FickNury Profile -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="profile-avatar">⚡</div>
          <div class="profile-info">
            <h3 class="profile-name">FickNury</h3>
            <p class="profile-title">Task Evaluation & Deployment</p>
          </div>
          <button @click="editProfile('ficknury')" class="edit-btn">✏️</button>
        </div>
        
        <div class="profile-content">
          <div v-if="!editing.ficknury" class="profile-bio">
            <p>{{ profiles.ficknury.bio }}</p>
          </div>
          <div v-else class="profile-edit">
            <textarea 
              v-model="profiles.ficknury.bio" 
              class="bio-textarea"
              rows="4"
              placeholder="Enter FickNury's bio..."
            ></textarea>
            <div class="edit-actions">
              <button @click="saveProfile('ficknury')" class="btn-save">Save</button>
              <button @click="cancelEdit('ficknury')" class="btn-cancel">Cancel</button>
            </div>
          </div>
          
          <div class="profile-avatar-section">
            <h4>Avatar</h4>
            <div class="avatar-upload">
              <img v-if="profiles.ficknury.avatar" :src="profiles.ficknury.avatar" alt="FickNury Avatar" class="avatar-preview" />
              <div v-else class="avatar-placeholder">⚡</div>
              <input 
                type="file" 
                @change="handleAvatarUpload('ficknury', $event)" 
                accept="image/*"
                class="avatar-input"
              />
              <label class="avatar-label">Change Avatar</label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- System Information -->
    <div class="system-info">
      <h2 class="section-title">🔧 System Information</h2>
      <div class="info-grid">
        <div class="info-card">
          <h3>Version</h3>
          <p>LinkOps Core v1.0.0</p>
        </div>
        <div class="info-card">
          <h3>Architecture</h3>
          <p>Microservices with Kubernetes</p>
        </div>
        <div class="info-card">
          <h3>Database</h3>
          <p>PostgreSQL with Redis Cache</p>
        </div>
        <div class="info-card">
          <h3>Frontend</h3>
          <p>Vue 3 + Tailwind CSS</p>
        </div>
        <div class="info-card">
          <h3>AI Framework</h3>
          <p>Custom Neural Networks</p>
        </div>
        <div class="info-card">
          <h3>Deployment</h3>
          <p>Docker + AKS</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'About',
  setup() {
    const editing = ref({
      whis: false,
      james: false,
      katie: false,
      igris: false,
      ficknury: false
    })

    const profiles = ref({
      whis: {
        bio: 'Whis is the core AI training system that processes and learns from various data inputs. It generates runes (knowledge patterns) and orbs (action templates) to improve system intelligence.',
        avatar: null
      },
      james: {
        bio: 'James is the primary AI assistant that handles task submission, Q&A, information processing, and provides ChatGPT-assisted solution paths for complex problems.',
        avatar: null
      },
      katie: {
        bio: 'Katie specializes in data processing, analysis, and report generation. She handles complex data transformations and statistical analysis with high accuracy.',
        avatar: null
      },
      igris: {
        bio: 'Igris is the system integration expert responsible for API management, cross-platform communication, and handling complex integration scenarios.',
        avatar: null
      },
      ficknury: {
        bio: 'FickNury evaluates tasks, assigns confidence scores, and makes intelligent deployment decisions. It routes tasks to appropriate agents based on complexity and requirements.',
        avatar: null
      }
    })

    const editProfile = (agent) => {
      editing.value[agent] = true
    }

    const saveProfile = (agent) => {
      localStorage.setItem(`profile_${agent}`, JSON.stringify(profiles.value[agent]))
      editing.value[agent] = false
    }

    const cancelEdit = (agent) => {
      const saved = localStorage.getItem(`profile_${agent}`)
      if (saved) {
        profiles.value[agent] = JSON.parse(saved)
      }
      editing.value[agent] = false
    }

    const handleAvatarUpload = (agent, event) => {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          profiles.value[agent].avatar = e.target.result
          localStorage.setItem(`profile_${agent}`, JSON.stringify(profiles.value[agent]))
        }
        reader.readAsDataURL(file)
      }
    }

    onMounted(() => {
      Object.keys(profiles.value).forEach(agent => {
        const saved = localStorage.getItem(`profile_${agent}`)
        if (saved) {
          profiles.value[agent] = JSON.parse(saved)
        }
      })
    })

    return {
      editing,
      profiles,
      editProfile,
      saveProfile,
      cancelEdit,
      handleAvatarUpload
    }
  }
}
</script>

<style scoped>
.about-page {
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

.profiles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.profile-card {
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

.profile-card::before {
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

.profile-card:hover {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 40px rgba(0, 255, 255, 0.2);
  transform: translateY(-5px);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  position: relative;
}

.profile-avatar {
  font-size: 3rem;
  filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.5));
}

.profile-info {
  flex: 1;
}

.profile-name {
  color: #00ffff;
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
}

.profile-title {
  color: #888;
  font-size: 0.9rem;
}

.edit-btn {
  background: none;
  border: none;
  color: #00ffff;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  background: rgba(0, 255, 255, 0.1);
  transform: scale(1.1);
}

.profile-content {
  position: relative;
  z-index: 2;
}

.profile-bio {
  margin-bottom: 1.5rem;
}

.profile-bio p {
  color: #ccc;
  line-height: 1.6;
}

.profile-edit {
  margin-bottom: 1.5rem;
}

.bio-textarea {
  width: 100%;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 8px;
  padding: 1rem;
  color: #fff;
  font-family: inherit;
  resize: vertical;
  min-height: 100px;
}

.bio-textarea:focus {
  outline: none;
  border-color: #00ffff;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

.edit-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-save, .btn-cancel {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn-save {
  background: linear-gradient(45deg, #00ff00, #00cc00);
  color: #000;
}

.btn-cancel {
  background: linear-gradient(45deg, #ff6b6b, #ff8e53);
  color: #fff;
}

.btn-save:hover, .btn-cancel:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.profile-avatar-section {
  border-top: 1px solid rgba(0, 255, 255, 0.2);
  padding-top: 1.5rem;
}

.profile-avatar-section h4 {
  color: #00ffff;
  margin-bottom: 1rem;
  font-size: 1rem;
}

.avatar-upload {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar-preview, .avatar-placeholder {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 2px solid rgba(0, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  background: rgba(0, 0, 0, 0.5);
}

.avatar-input {
  display: none;
}

.avatar-label {
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 255, 255, 0.3);
}

.avatar-label:hover {
  background: rgba(0, 255, 255, 0.2);
  border-color: #00ffff;
}

/* System Information */
.system-info {
  margin-top: 3rem;
}

.section-title {
  color: #00ffff;
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.info-card {
  background: rgba(0, 0, 0, 0.7);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 10px;
  padding: 1.5rem;
  text-align: center;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.info-card:hover {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
  transform: translateY(-3px);
}

.info-card h3 {
  color: #00ffff;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.info-card p {
  color: #ccc;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .profiles-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .edit-btn {
    position: absolute;
    top: 0;
    right: 0;
  }
  
  .avatar-upload {
    flex-direction: column;
    align-items: center;
  }
}
</style> 