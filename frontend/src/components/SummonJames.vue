<template>
  <div class="summon-james">
    <!-- Floating Action Button -->
    <div 
      class="james-fab"
      :class="{ 'listening': isListening, 'speaking': isSpeaking }"
      @click="toggleJames"
      :title="fabTitle"
    >
      <div class="james-icon">
        <i class="fas fa-microphone" v-if="!isListening && !isSpeaking"></i>
        <i class="fas fa-volume-up" v-if="isSpeaking"></i>
        <div class="pulse-ring" v-if="isListening"></div>
      </div>
    </div>

    <!-- James Interface Modal -->
    <div v-if="showInterface" class="james-modal" @click.self="closeInterface">
      <div class="james-interface">
        <!-- Header -->
        <div class="james-header">
          <h2>James - LinkOps Assistant</h2>
          <button @click="closeInterface" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <!-- Voice Controls -->
        <div class="voice-controls">
          <div class="control-group">
            <button 
              @click="startListening"
              :disabled="isListening || isSpeaking"
              class="control-btn listen-btn"
              :class="{ 'active': isListening }"
            >
              <i class="fas fa-microphone"></i>
              {{ isListening ? 'Listening...' : 'Listen' }}
            </button>
            
            <button 
              @click="stopListening"
              :disabled="!isListening"
              class="control-btn stop-btn"
            >
              <i class="fas fa-stop"></i>
              Stop
            </button>
          </div>

          <div class="control-group">
            <button 
              @click="uploadImage"
              class="control-btn image-btn"
            >
              <i class="fas fa-image"></i>
              Upload Image
            </button>
            
            <input 
              ref="imageInput"
              type="file"
              accept="image/*"
              @change="handleImageUpload"
              style="display: none"
            >
          </div>
        </div>

        <!-- Conversation Area -->
        <div class="conversation-area">
          <div class="messages" ref="messagesContainer">
            <div 
              v-for="(message, index) in messages" 
              :key="index"
              class="message"
              :class="message.type"
            >
              <div class="message-content">
                <div class="message-text">{{ message.text }}</div>
                <div class="message-time">{{ formatTime(message.timestamp) }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div class="input-area">
          <div class="text-input-group">
            <input 
              v-model="textInput"
              @keyup.enter="sendTextMessage"
              placeholder="Type your message to James..."
              class="text-input"
              :disabled="isListening || isSpeaking"
            >
            <button 
              @click="sendTextMessage"
              :disabled="!textInput.trim() || isListening || isSpeaking"
              class="send-btn"
            >
              <i class="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>

        <!-- Status Bar -->
        <div class="status-bar">
          <div class="status-item">
            <i class="fas fa-circle" :class="statusColor"></i>
            {{ statusText }}
          </div>
          <div class="status-item" v-if="isListening">
            <i class="fas fa-waveform-lines"></i>
            {{ listeningDuration }}s
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="fas fa-cog fa-spin"></i>
        <p>James is processing...</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SummonJames',
  data() {
    return {
      showInterface: false,
      isListening: false,
      isSpeaking: false,
      isLoading: false,
      messages: [],
      textInput: '',
      listeningStartTime: null,
      listeningDuration: 0,
      mediaRecorder: null,
      audioChunks: [],
      jamesAPI: 'http://localhost:8000/api' // Update with actual James API URL
    }
  },
  computed: {
    fabTitle() {
      if (this.isListening) return 'James is listening...'
      if (this.isSpeaking) return 'James is speaking...'
      return 'Summon James'
    },
    statusText() {
      if (this.isListening) return 'Listening'
      if (this.isSpeaking) return 'Speaking'
      if (this.isLoading) return 'Processing'
      return 'Ready'
    },
    statusColor() {
      if (this.isListening) return 'text-blue-500'
      if (this.isSpeaking) return 'text-green-500'
      if (this.isLoading) return 'text-yellow-500'
      return 'text-gray-500'
    }
  },
  methods: {
    toggleJames() {
      this.showInterface = !this.showInterface
      if (this.showInterface) {
        this.addMessage('system', 'James is ready to assist you.')
      }
    },
    
    closeInterface() {
      this.showInterface = false
      if (this.isListening) {
        this.stopListening()
      }
    },

    async startListening() {
      try {
        this.isLoading = true
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        
        this.mediaRecorder = new MediaRecorder(stream)
        this.audioChunks = []
        
        this.mediaRecorder.ondataavailable = (event) => {
          this.audioChunks.push(event.data)
        }
        
        this.mediaRecorder.onstop = async () => {
          await this.processAudioRecording()
        }
        
        this.mediaRecorder.start()
        this.isListening = true
        this.listeningStartTime = Date.now()
        this.startListeningTimer()
        
        this.addMessage('user', 'Listening...')
        
      } catch (error) {
        console.error('Error starting listening:', error)
        this.addMessage('error', 'Could not access microphone.')
      } finally {
        this.isLoading = false
      }
    },

    stopListening() {
      if (this.mediaRecorder && this.isListening) {
        this.mediaRecorder.stop()
        this.isListening = false
        this.stopListeningTimer()
        
        // Stop all tracks
        this.mediaRecorder.stream.getTracks().forEach(track => track.stop())
      }
    },

    startListeningTimer() {
      this.listeningTimer = setInterval(() => {
        this.listeningDuration = Math.floor((Date.now() - this.listeningStartTime) / 1000)
      }, 1000)
    },

    stopListeningTimer() {
      if (this.listeningTimer) {
        clearInterval(this.listeningTimer)
        this.listeningDuration = 0
      }
    },

    async processAudioRecording() {
      try {
        this.isLoading = true
        const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' })
        
        const formData = new FormData()
        formData.append('audio', audioBlob, 'recording.wav')
        
        const response = await fetch(`${this.jamesAPI}/voice/conversation`, {
          method: 'POST',
          body: formData
        })
        
        if (response.ok) {
          const result = await response.json()
          this.addMessage('user', result.conversation.user_input)
          this.addMessage('james', result.conversation.james_response)
          
          // Play audio response
          await this.playAudioResponse(result.conversation.audio_response)
        } else {
          throw new Error('Voice processing failed')
        }
        
      } catch (error) {
        console.error('Error processing audio:', error)
        this.addMessage('error', 'Voice processing failed.')
      } finally {
        this.isLoading = false
      }
    },

    async playAudioResponse(audioUrl) {
      try {
        this.isSpeaking = true
        const audio = new Audio(audioUrl)
        await audio.play()
        
        audio.onended = () => {
          this.isSpeaking = false
        }
      } catch (error) {
        console.error('Error playing audio:', error)
        this.isSpeaking = false
      }
    },

    uploadImage() {
      this.$refs.imageInput.click()
    },

    async handleImageUpload(event) {
      const file = event.target.files[0]
      if (!file) return

      try {
        this.isLoading = true
        const formData = new FormData()
        formData.append('image', file)
        
        const response = await fetch(`${this.jamesAPI}/describe_image`, {
          method: 'POST',
          body: formData
        })
        
        if (response.ok) {
          const result = await response.json()
          this.addMessage('user', `Uploaded image: ${file.name}`)
          this.addMessage('james', result.description)
        } else {
          throw new Error('Image processing failed')
        }
        
      } catch (error) {
        console.error('Error processing image:', error)
        this.addMessage('error', 'Image processing failed.')
      } finally {
        this.isLoading = false
        event.target.value = '' // Reset input
      }
    },

    async sendTextMessage() {
      if (!this.textInput.trim()) return
      
      const message = this.textInput.trim()
      this.addMessage('user', message)
      this.textInput = ''
      
      try {
        this.isLoading = true
        
        // Send text message to James
        const response = await fetch(`${this.jamesAPI}/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: message,
            context: 'voice_interface'
          })
        })
        
        if (response.ok) {
          const result = await response.json()
          this.addMessage('james', result.response)
        } else {
          throw new Error('Text processing failed')
        }
        
      } catch (error) {
        console.error('Error sending text message:', error)
        this.addMessage('error', 'Message processing failed.')
      } finally {
        this.isLoading = false
      }
    },

    addMessage(type, text) {
      this.messages.push({
        type,
        text,
        timestamp: new Date()
      })
      
      this.$nextTick(() => {
        this.scrollToBottom()
      })
    },

    scrollToBottom() {
      const container = this.$refs.messagesContainer
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },

    formatTime(date) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  },

  beforeUnmount() {
    this.stopListening()
    this.stopListeningTimer()
  }
}
</script>

<style scoped>
.summon-james {
  position: relative;
}

.james-fab {
  position: fixed;
  bottom: 30px;
  right: 30px;
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.james-fab:hover {
  transform: scale(1.1);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4);
}

.james-fab.listening {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  animation: pulse 1.5s infinite;
}

.james-fab.speaking {
  background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
}

.james-icon {
  position: relative;
  color: white;
  font-size: 24px;
}

.pulse-ring {
  position: absolute;
  top: -10px;
  left: -10px;
  width: 50px;
  height: 50px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: pulse-ring 1.5s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@keyframes pulse-ring {
  0% { transform: scale(0.8); opacity: 1; }
  100% { transform: scale(1.2); opacity: 0; }
}

.james-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.james-interface {
  width: 90%;
  max-width: 600px;
  height: 80%;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.james-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.james-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 5px;
}

.voice-controls {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.control-group {
  display: flex;
  gap: 10px;
}

.control-btn {
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.listen-btn {
  background: #667eea;
  color: white;
}

.listen-btn:hover:not(:disabled) {
  background: #5a6fd8;
}

.listen-btn.active {
  background: #ff6b6b;
  animation: pulse 1.5s infinite;
}

.stop-btn {
  background: #ff6b6b;
  color: white;
}

.image-btn {
  background: #00b894;
  color: white;
}

.image-btn:hover {
  background: #00a085;
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.conversation-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.message.user {
  justify-content: flex-end;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 15px;
  position: relative;
}

.message.user .message-content {
  background: #667eea;
  color: white;
  border-bottom-right-radius: 5px;
}

.message.james .message-content {
  background: #f8f9fa;
  color: #333;
  border-bottom-left-radius: 5px;
}

.message.system .message-content {
  background: #e9ecef;
  color: #6c757d;
  font-style: italic;
}

.message.error .message-content {
  background: #f8d7da;
  color: #721c24;
}

.message-time {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 5px;
}

.input-area {
  padding: 20px;
  border-top: 1px solid #eee;
}

.text-input-group {
  display: flex;
  gap: 10px;
}

.text-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.text-input:focus {
  outline: none;
  border-color: #667eea;
}

.send-btn {
  padding: 12px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.send-btn:hover:not(:disabled) {
  background: #5a6fd8;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.status-bar {
  padding: 15px 20px;
  background: #f8f9fa;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
}

.loading-spinner {
  background: white;
  padding: 30px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.loading-spinner i {
  font-size: 32px;
  color: #667eea;
  margin-bottom: 15px;
}

.loading-spinner p {
  margin: 0;
  color: #666;
  font-weight: 500;
}
</style> 