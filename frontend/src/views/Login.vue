<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <div class="logo-container">
            <div class="logo">🤖</div>
            <div class="logo-glow"></div>
          </div>
          <h1 class="login-title">LinkOps Core</h1>
          <p class="login-subtitle">AI Command Center Access</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label class="form-label">Username</label>
            <div class="input-container">
              <input 
                v-model="loginForm.username" 
                type="text" 
                class="form-input"
                placeholder="Enter your username"
                required
              />
              <div class="input-glow"></div>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Password</label>
            <div class="input-container">
              <input 
                v-model="loginForm.password" 
                type="password" 
                class="form-input"
                placeholder="Enter your password"
                required
              />
              <div class="input-glow"></div>
            </div>
          </div>

          <div class="form-options">
            <label class="checkbox-container">
              <input type="checkbox" v-model="loginForm.remember" />
              <span class="checkmark"></span>
              Remember me
            </label>
            <a href="#" class="forgot-password">Forgot Password?</a>
          </div>

          <button type="submit" class="login-btn" :disabled="isLoading">
            <span v-if="!isLoading">Access System</span>
            <span v-else class="loading-spinner">Authenticating...</span>
          </button>
        </form>

        <div class="login-footer">
          <p class="footer-text">New to LinkOps?</p>
          <button @click="showRegistration = true" class="register-btn">Create Account</button>
        </div>
      </div>

      <!-- Background Effects -->
      <div class="background-effects">
        <div class="floating-particles">
          <div v-for="i in 20" :key="i" class="particle" :style="getParticleStyle(i)"></div>
        </div>
        <div class="grid-overlay"></div>
      </div>
    </div>

    <!-- Registration Modal -->
    <div v-if="showRegistration" class="modal-overlay" @click="showRegistration = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Create Account</h2>
          <button @click="showRegistration = false" class="modal-close">×</button>
        </div>
        <form @submit.prevent="handleRegistration" class="registration-form">
          <div class="form-group">
            <label>Full Name</label>
            <input v-model="registrationForm.fullName" type="text" required />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="registrationForm.email" type="email" required />
          </div>
          <div class="form-group">
            <label>Username</label>
            <input v-model="registrationForm.username" type="text" required />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input v-model="registrationForm.password" type="password" required />
          </div>
          <button type="submit" class="btn-primary">Create Account</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const isLoading = ref(false)
    const showRegistration = ref(false)

    const loginForm = ref({
      username: '',
      password: '',
      remember: false
    })

    const registrationForm = ref({
      fullName: '',
      email: '',
      username: '',
      password: ''
    })

    const handleLogin = async () => {
      isLoading.value = true
      
      try {
        // Mock authentication
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        // Simulate successful login
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('user', JSON.stringify({
          username: loginForm.value.username,
          role: 'admin'
        }))
        
        // Redirect to dashboard
        router.push('/dashboard')
      } catch (error) {
        console.error('Login failed:', error)
      } finally {
        isLoading.value = false
      }
    }

    const handleRegistration = async () => {
      try {
        // Mock registration
        await new Promise(resolve => setTimeout(resolve, 1500))
        showRegistration.value = false
        // Show success message or auto-login
      } catch (error) {
        console.error('Registration failed:', error)
      }
    }

    const getParticleStyle = (index) => {
      const delay = Math.random() * 10
      const duration = 10 + Math.random() * 20
      const x = Math.random() * 100
      const y = Math.random() * 100
      
      return {
        '--delay': `${delay}s`,
        '--duration': `${duration}s`,
        '--x': `${x}%`,
        '--y': `${y}%`
      }
    }

    onMounted(() => {
      // Initialize particle animations
      const particles = document.querySelectorAll('.particle')
      particles.forEach((particle, index) => {
        particle.style.animationDelay = `${Math.random() * 10}s`
      })
    })

    return {
      loginForm,
      registrationForm,
      isLoading,
      showRegistration,
      handleLogin,
      handleRegistration,
      getParticleStyle
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
  position: relative;
  overflow: hidden;
}

.login-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 450px;
  padding: 2rem;
}

.login-card {
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 20px;
  padding: 3rem 2rem;
  backdrop-filter: blur(20px);
  box-shadow: 0 0 50px rgba(0, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.login-card::before {
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

.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo-container {
  position: relative;
  display: inline-block;
  margin-bottom: 1rem;
}

.logo {
  font-size: 4rem;
  filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.5));
  animation: logo-float 3s ease-in-out infinite;
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(0, 255, 255, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  animation: logo-glow 2s ease-in-out infinite alternate;
}

.login-title {
  color: #00ffff;
  font-size: 2rem;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}

.login-subtitle {
  color: #888;
  font-size: 1rem;
}

.login-form {
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  color: #ccc;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.input-container {
  position: relative;
}

.form-input {
  width: 100%;
  background: rgba(0, 0, 0, 0.5);
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 10px;
  padding: 1rem;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.form-input:focus {
  outline: none;
  border-color: #00ffff;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
}

.input-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 10px;
  background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.form-input:focus + .input-glow {
  opacity: 1;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ccc;
  cursor: pointer;
  font-size: 0.9rem;
}

.checkbox-container input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 4px;
  position: relative;
  transition: all 0.3s ease;
}

.checkbox-container input[type="checkbox"]:checked + .checkmark {
  background: #00ffff;
  border-color: #00ffff;
}

.checkbox-container input[type="checkbox"]:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #000;
  font-size: 12px;
  font-weight: bold;
}

.forgot-password {
  color: #00ffff;
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.forgot-password:hover {
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.login-btn {
  width: 100%;
  background: linear-gradient(45deg, #00ffff, #0080ff);
  border: none;
  border-radius: 10px;
  padding: 1rem;
  color: #000;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

.login-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.login-btn:hover::before {
  left: 100%;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 255, 255, 0.3);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}

.login-footer {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

.footer-text {
  color: #888;
  margin-bottom: 1rem;
}

.register-btn {
  background: none;
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  color: #00ffff;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.register-btn:hover {
  background: rgba(0, 255, 255, 0.1);
  border-color: #00ffff;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

/* Background Effects */
.background-effects {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.floating-particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #00ffff;
  border-radius: 50%;
  animation: particle-float 20s linear infinite;
  opacity: 0.6;
}

.particle:nth-child(even) {
  background: #ff00ff;
  animation-duration: 25s;
}

.particle:nth-child(3n) {
  background: #00ff00;
  animation-duration: 30s;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: grid-move 20s linear infinite;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.modal-content {
  background: rgba(0, 0, 0, 0.9);
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 15px;
  padding: 2rem;
  max-width: 400px;
  width: 90%;
  backdrop-filter: blur(20px);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h2 {
  color: #00ffff;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  color: #888;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: rgba(255, 0, 0, 0.2);
  color: #ff0000;
}

.registration-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.registration-form .form-group {
  margin-bottom: 0;
}

.registration-form input {
  width: 100%;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  color: #fff;
}

.btn-primary {
  background: linear-gradient(45deg, #00ffff, #0080ff);
  border: none;
  border-radius: 8px;
  padding: 0.75rem;
  color: #000;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
}

/* Animations */
@keyframes logo-float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

@keyframes logo-glow {
  0% { opacity: 0.5; transform: translate(-50%, -50%) scale(1); }
  100% { opacity: 0.8; transform: translate(-50%, -50%) scale(1.2); }
}

@keyframes particle-float {
  0% {
    transform: translate(var(--x), 100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.6;
  }
  100% {
    transform: translate(var(--x), -100px) rotate(360deg);
    opacity: 0;
  }
}

@keyframes grid-move {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .login-container {
    padding: 1rem;
  }
  
  .login-card {
    padding: 2rem 1.5rem;
  }
  
  .form-options {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style> 