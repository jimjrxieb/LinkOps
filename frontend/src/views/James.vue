<template>
  <div class="james-page">
    <div class="page-header">
      <h1 class="page-title">🤖 James - AI Assistant</h1>
      <p class="page-subtitle">Task Submission & AI-Powered Solutions</p>
    </div>

    <!-- Floating AI Avatar -->
    <div class="ai-avatar" :class="{ 'speaking': isSpeaking }">
      <div class="avatar-container">
        <div class="avatar-image">🤖</div>
        <div class="speech-bubble" v-if="isSpeaking">
          <p>{{ currentMessage }}</p>
        </div>
      </div>
    </div>

    <div class="content-grid">
      <!-- Task Submission Tool -->
      <div class="card task-submission">
        <h3 class="card-title">📝 Task Submission</h3>
        <form @submit.prevent="submitTask" class="form">
          <div class="form-group">
            <label>Task Description</label>
            <textarea 
              v-model="taskForm.description" 
              placeholder="Describe the task you need help with..."
              rows="4"
              class="form-input"
            ></textarea>
          </div>
          <div class="form-group">
            <label>Priority</label>
            <select v-model="taskForm.priority" class="form-input">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>
          <button type="submit" class="btn-primary">Submit Task</button>
        </form>
      </div>

      <!-- Q&A Input Form -->
      <div class="card qa-form">
        <h3 class="card-title">❓ Q&A Input</h3>
        <form @submit.prevent="submitQuestion" class="form">
          <div class="form-group">
            <label>Question</label>
            <textarea 
              v-model="qaForm.question" 
              placeholder="Ask James anything..."
              rows="3"
              class="form-input"
            ></textarea>
          </div>
          <button type="submit" class="btn-secondary">Ask Question</button>
        </form>
        <div v-if="qaResponse" class="response">
          <h4>Response:</h4>
          <p>{{ qaResponse }}</p>
        </div>
      </div>

      <!-- Info Dump Input -->
      <div class="card info-dump">
        <h3 class="card-title">📄 Info Dump</h3>
        <form @submit.prevent="submitInfoDump" class="form">
          <div class="form-group">
            <label>Information</label>
            <textarea 
              v-model="infoDumpForm.content" 
              placeholder="Paste or type information to be processed..."
              rows="5"
              class="form-input"
            ></textarea>
          </div>
          <div class="form-group">
            <label>Processing Type</label>
            <select v-model="infoDumpForm.type" class="form-input">
              <option value="text">Text Analysis</option>
              <option value="code">Code Review</option>
              <option value="log">Log Analysis</option>
              <option value="data">Data Processing</option>
            </select>
          </div>
          <button type="submit" class="btn-secondary">Process Info</button>
        </form>
      </div>

      <!-- Image Extractor -->
      <div class="card image-extractor">
        <h3 class="card-title">🖼️ Image Extractor</h3>
        <form @submit.prevent="extractFromImage" class="form">
          <div class="form-group">
            <label>Image URL or Upload</label>
            <input 
              v-model="imageForm.url" 
              type="url" 
              placeholder="Enter image URL..."
              class="form-input"
            />
            <div class="file-upload">
              <input 
                type="file" 
                @change="handleImageUpload" 
                accept="image/*"
                class="file-input"
              />
              <label class="file-label">Choose File</label>
            </div>
          </div>
          <div class="form-group">
            <label>Extraction Type</label>
            <select v-model="imageForm.extractionType" class="form-input">
              <option value="text">Text (OCR)</option>
              <option value="objects">Objects</option>
              <option value="faces">Faces</option>
              <option value="code">Code/Text</option>
            </select>
          </div>
          <button type="submit" class="btn-secondary">Extract</button>
        </form>
        <div v-if="imageResult" class="result">
          <h4>Extraction Result:</h4>
          <pre>{{ imageResult }}</pre>
        </div>
      </div>

      <!-- ChatGPT-Assisted Solution Path -->
      <div class="card solution-path">
        <h3 class="card-title">🧠 AI Solution Path</h3>
        <form @submit.prevent="generateSolutionPath" class="form">
          <div class="form-group">
            <label>Problem Description</label>
            <textarea 
              v-model="solutionForm.problem" 
              placeholder="Describe the problem you're facing..."
              rows="4"
              class="form-input"
            ></textarea>
          </div>
          <div class="form-group">
            <label>Context</label>
            <textarea 
              v-model="solutionForm.context" 
              placeholder="Additional context, constraints, or requirements..."
              rows="3"
              class="form-input"
            ></textarea>
          </div>
          <button type="submit" class="btn-primary">Generate Solution</button>
        </form>
        <div v-if="solutionPath" class="solution-result">
          <h4>AI-Generated Solution:</h4>
          <div class="solution-steps">
            <div v-for="(step, index) in solutionPath.steps" :key="index" class="step">
              <span class="step-number">{{ index + 1 }}</span>
              <p>{{ step }}</p>
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
  name: 'James',
  setup() {
    const isSpeaking = ref(false)
    const currentMessage = ref('')
    const qaResponse = ref('')
    const imageResult = ref('')
    const solutionPath = ref(null)

    const taskForm = ref({
      description: '',
      priority: 'medium'
    })

    const qaForm = ref({
      question: ''
    })

    const infoDumpForm = ref({
      content: '',
      type: 'text'
    })

    const imageForm = ref({
      url: '',
      extractionType: 'text'
    })

    const solutionForm = ref({
      problem: '',
      context: ''
    })

    const speak = (message) => {
      currentMessage.value = message
      isSpeaking.value = true
      setTimeout(() => {
        isSpeaking.value = false
      }, 3000)
    }

    const submitTask = async () => {
      try {
        speak("Task received. Processing your request...")
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        speak("Task submitted successfully to the queue.")
        taskForm.value.description = ''
      } catch (error) {
        console.error('Error submitting task:', error)
        speak("Error submitting task. Please try again.")
      }
    }

    const submitQuestion = async () => {
      try {
        speak("Analyzing your question...")
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 1500))
        qaResponse.value = "Based on my analysis, here's what I found: [Mock response]"
        speak("Question processed. Check the response below.")
      } catch (error) {
        console.error('Error submitting question:', error)
        speak("Error processing question. Please try again.")
      }
    }

    const submitInfoDump = async () => {
      try {
        speak("Processing information dump...")
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 2000))
        speak("Information processed and stored.")
        infoDumpForm.value.content = ''
      } catch (error) {
        console.error('Error submitting info dump:', error)
        speak("Error processing information. Please try again.")
      }
    }

    const handleImageUpload = (event) => {
      const file = event.target.files[0]
      if (file) {
        imageForm.value.url = URL.createObjectURL(file)
      }
    }

    const extractFromImage = async () => {
      try {
        speak("Extracting information from image...")
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 2500))
        imageResult.value = "Extracted text: [Mock OCR result]"
        speak("Image extraction complete.")
      } catch (error) {
        console.error('Error extracting from image:', error)
        speak("Error extracting from image. Please try again.")
      }
    }

    const generateSolutionPath = async () => {
      try {
        speak("Generating AI solution path...")
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 3000))
        solutionPath.value = {
          steps: [
            "Analyze the problem and identify root causes",
            "Research similar solutions and best practices",
            "Design a step-by-step approach",
            "Implement the solution with proper testing",
            "Monitor and validate the results"
          ]
        }
        speak("Solution path generated successfully.")
      } catch (error) {
        console.error('Error generating solution:', error)
        speak("Error generating solution. Please try again.")
      }
    }

    onMounted(() => {
      speak("Hello! I'm James, your AI assistant. How can I help you today?")
    })

    return {
      isSpeaking,
      currentMessage,
      taskForm,
      qaForm,
      qaResponse,
      infoDumpForm,
      imageForm,
      imageResult,
      solutionForm,
      solutionPath,
      submitTask,
      submitQuestion,
      submitInfoDump,
      handleImageUpload,
      extractFromImage,
      generateSolutionPath
    }
  }
}
</script>

<style scoped>
.james-page {
  position: relative;
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

.ai-avatar {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 100;
}

.avatar-container {
  position: relative;
}

.avatar-image {
  font-size: 4rem;
  filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.5));
  animation: float 3s ease-in-out infinite;
}

.speaking .avatar-image {
  animation: pulse 0.5s ease-in-out infinite;
}

.speech-bubble {
  position: absolute;
  top: -60px;
  right: 0;
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid #00ffff;
  border-radius: 15px;
  padding: 1rem;
  max-width: 300px;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

.speech-bubble::after {
  content: '';
  position: absolute;
  bottom: -10px;
  right: 20px;
  width: 0;
  height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-top: 10px solid #00ffff;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
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

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: #ccc;
  font-weight: 500;
}

.form-input {
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  color: #fff;
  font-family: 'Courier New', monospace;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #00ffff;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

.file-upload {
  position: relative;
  display: inline-block;
}

.file-input {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.file-label {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 6px;
  color: #00ffff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-label:hover {
  background: rgba(0, 255, 255, 0.2);
  border-color: #00ffff;
}

.btn-primary, .btn-secondary {
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

.btn-primary:hover, .btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.response, .result, .solution-result {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(0, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.2);
  border-radius: 8px;
}

.solution-steps {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.step-number {
  background: #00ffff;
  color: #000;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .ai-avatar {
    position: static;
    margin-bottom: 2rem;
    text-align: center;
  }
  
  .speech-bubble {
    position: static;
    margin-top: 1rem;
  }
}
</style> 