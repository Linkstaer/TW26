[file name]: SSUManagement.vue
<template>
  <div class="ssu-page">
    <!-- Fondo SCP -->
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
    </div>

    <!-- Header -->
    <div class="ssu-header">
      <div class="header-left">
        <div class="header-logo">
          <div class="header-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <div class="header-title">
            <span class="header-main">SSU MANAGEMENT</span>
            <span class="header-sub">SYSTEM SERVER UNIT CONTROL</span>
          </div>
        </div>
      </div>
      
      <div class="header-right">
        <div class="session-status">
          <div class="session-indicator active"></div>
          <span class="session-text">{{ userRole?.toUpperCase() || 'NO AUTORIZADO' }}</span>
        </div>
        <div class="current-time">
          {{ currentTime }}
        </div>
        <button class="back-button" @click="$router.push('/moderation')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"></path>
          </svg>
          VOLVER
        </button>
      </div>
    </div>

    <!-- Contenido Principal -->
    <main class="ssu-main">
      <div class="ssu-container">
        <!-- Título y Subtítulo -->
        <div class="ssu-header-section">
          <h1 class="ssu-title">SYSTEM SERVER UNIT</h1>
          <div class="ssu-subtitle">CONTROL DEl SERVIDOR DEL SITIO</div>
          
          <!-- Estado Actual -->
          <div class="current-status" :class="{'on': ssuStatus, 'off': !ssuStatus}">
            <div class="status-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="status-info">
              <span class="status-label">ESTADO ACTUAL</span>
              <span class="status-value" :class="{'on': ssuStatus, 'off': !ssuStatus}">
                {{ ssuStatus ? 'SERVIDOR ACTIVO' : 'SERVIDOR INACTIVO' }}
              </span>
              <div class="status-indicator" :class="{'active': ssuStatus}"></div>
            </div>
          </div>
        </div>

        <!-- Interruptor Cómicamente Grande -->
        <div class="comic-switch-container" v-if="hasPermission">
          <div class="switch-label">CONTROL MAESTRO DEL SERVIDOR</div>
          
          <div class="comic-switch" @click="toggleSSU">
            <!-- Marco exterior con efecto de metal -->
            <div class="switch-frame">
              <!-- Base del interruptor -->
              <div class="switch-base">
                <!-- Parte superior - deslizante -->
                <div class="switch-slider" :class="{'on': ssuStatus, 'off': !ssuStatus}">
                  <!-- Indicador de posición -->
                  <div class="position-indicator">
                    <span class="position-text">{{ ssuStatus ? 'ON' : 'OFF' }}</span>
                  </div>
                  
                  <!-- Botón de agarre -->
                  <div class="grip-handle">
                    <div class="grip-line"></div>
                    <div class="grip-line"></div>
                    <div class="grip-line"></div>
                  </div>
                </div>
                
                <!-- Pista de deslizamiento -->
                <div class="switch-track">
                  <div class="track-end off">OFF</div>
                  <div class="track-middle">
                    <div class="track-line"></div>
                    <div class="track-line"></div>
                    <div class="track-line"></div>
                  </div>
                  <div class="track-end on">ON</div>
                </div>
              </div>
              
              <!-- Panel de estado con luces LED -->
              <div class="status-panel">
                <div class="led-indicator" :class="{'active': !ssuStatus}"></div>
                <div class="led-indicator" :class="{'active': ssuStatus}"></div>
                <span class="panel-text">SERVER STATUS</span>
              </div>
            </div>
            
            <!-- Etiquetas de acción -->
            <div class="action-labels">
              <div class="action-label off">DESACTIVAR SERVIDOR</div>
              <div class="action-label on">ACTIVAR SERVIDOR</div>
            </div>
          </div>
          
          <!-- Instrucciones -->
          <div class="switch-instructions">
            <div class="instruction-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
              </svg>
            </div>
            <span class="instruction-text">Haz clic en el interruptor para {{ ssuStatus ? 'DESACTIVAR' : 'ACTIVAR' }} el SERVIDOR</span>
          </div>
        </div>

        <!-- Panel de Información -->
        <div class="info-panel">
          <div class="info-header">
            <h3 class="info-title">INFORMACIÓN DEL SERVIDOR</h3>
            <div class="info-subtitle">ESTADO DEL SERVIDOR</div>
          </div>
          
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">ÚLTIMO CAMBIO:</span>
              <span class="info-value">{{ lastChange || 'NUNCA' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">DURACIÓN ACTUAL:</span>
              <span class="info-value">{{ currentDuration }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">CAMBIOS HOY:</span>
              <span class="info-value">{{ changesToday || 0 }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">OPERADOR ACTUAL:</span>
              <span class="info-value">{{ currentOperator || 'NINGUNO' }}</span>
            </div>
          </div>
          
          <!-- Logs de Actividad -->
          <div class="activity-logs" v-if="activityLogs.length > 0">
            <h4 class="logs-title">REGISTRO DE ACTIVIDAD</h4>
            <div class="logs-container">
              <div v-for="(log, index) in activityLogs" :key="index" class="log-item">
                <div class="log-time">{{ log.time }}</div>
                <div class="log-action" :class="{'on': log.action === 'ACTIVATED', 'off': log.action === 'DEACTIVATED'}">
                  {{ log.action === 'ACTIVATED' ? 'SERVIDOR ACTIVADO' : 'SERVIDOR DESACTIVADO' }}
                </div>
                <div class="log-operator">{{ log.operator }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sin Permisos -->
        <div class="no-permission" v-if="!hasPermission">
          <div class="permission-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#aa2222" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line>
            </svg>
          </div>
          <h3 class="permission-title">ACCESO RESTRINGIDO</h3>
          <p class="permission-text">No tienes los permisos necesarios para acceder al control del SSU.</p>
          <div class="permission-requirements">
            <div class="requirement-item">
              <span class="requirement-label">REQUISITO:</span>
              <span class="requirement-value">SSU Host+</span>
            </div>
            <div class="requirement-item">
              <span class="requirement-label">PERMISO:</span>
              <span class="requirement-value">change_ssu_status</span>
            </div>
          </div>
          <button class="back-button" @click="goBack">
            <span class="button-text">VOLVER AL PANEL</span>
          </button>
        </div>
      </div>
    </main>

    <!-- Modal de Confirmación -->
    <div v-if="showConfirmationModal" class="confirmation-modal">
      <div class="modal-overlay" @click="cancelToggle"></div>
      <div class="modal-content">
        <div class="modal-header">
          <div class="modal-icon" :class="{'on': !ssuStatus, 'off': ssuStatus}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 16v-4"></path>
              <path d="M12 8h.01"></path>
            </svg>
          </div>
          <h3 class="modal-title">CONFIRMAR CAMBIO DE ESTADO</h3>
        </div>
        <div class="modal-body">
          <p class="modal-text">
            Estás a punto de {{ ssuStatus ? 'DESACTIVAR' : 'ACTIVAR' }} el Servidor.
            <br><br>
            <strong>{{ ssuStatus ? 'La desactivación' : 'La activación' }} del SSU afectará:</strong>
          </p>
          <div class="effects-list">
            <div class="effect-item">
              <div class="effect-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </div>
              <span class="effect-text">Restricciones de acceso al sitio</span>
            </div>
            <div class="effect-item">
              <div class="effect-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                  <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                </svg>
              </div>
              <span class="effect-text">Protocolos de seguridad activos</span>
            </div>
            <div class="effect-item">
              <div class="effect-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
              </div>
              <span class="effect-text">Monitoreo y registro de actividad</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-button cancel" @click="cancelToggle">
            <span class="button-text">CANCELAR</span>
          </button>
          <button class="modal-button confirm" @click="confirmToggle">
            <span class="button-text">{{ ssuStatus ? 'DESACTIVAR SERVIDOR' : 'ACTIVAR SERVIDOR' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Estado
const ssuStatus = ref(false)
const hasPermission = ref(false)
const currentTime = ref('')
const lastChange = ref('')
const currentDuration = ref('00:00:00')
const changesToday = ref(0)
const currentOperator = ref('')
const activityLogs = ref([])
const showConfirmationModal = ref(false)
const toggleInProgress = ref(false)
const user = ref(null)

// Computed
const userRole = computed(() => {
  if (!user.value) return null
  if (user.value.is_superuser) return 'ADMINISTRADOR'
  if (user.value.is_staff) return 'MODERADOR'
  return 'INVITADO'
})

// Métodos
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('es-ES', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  }).replace(/(\d+)\/(\d+)\/(\d+),/, '$3-$1-$2')
}

const fetchCurrentUser = async () => {
  try {
    const response = await fetch('/api/auth/user/')
    if (response.ok) {
      const data = await response.json()
      user.value = data
      
      if (data.is_authenticated) {
        await checkPermissions()
        await fetchSSUStatus()
        await fetchSSUInfo()
      }
    }
  } catch (error) {
    console.error('Error obteniendo usuario:', error)
  }
}

const checkPermissions = async () => {
  try {
    const response = await fetch('/api/auth/user/permissions/')
    if (response.ok) {
      const data = await response.json()
      const permissions = data.permissions || []
      const scopes = data.scopes || []
      
      // Verificar permisos: superuser o global level 1+
      if (user.value.is_superuser) {
        hasPermission.value = true
      } else {
        // Buscar scope global con nivel 1 o superior
        const globalScope = scopes.find(s => s.scope === 'global' && s.level >= 1)
        hasPermission.value = globalScope !== undefined || permissions.includes('change_ssu_status')
      }
    }
  } catch (error) {
    console.error('Error obteniendo permisos:', error)
  }
}

const fetchSSUStatus = async () => {
  try {
    const response = await fetch('/api/ssu/')
    if (response.ok) {
      const data = await response.json()
      ssuStatus.value = data.ssu_status
    }
  } catch (error) {
    console.error('Error obteniendo estado SSU:', error)
  }
}

const fetchSSUInfo = async () => {
  try {
    const response = await fetch('/api/ssu/info/')
    if (response.ok) {
      const data = await response.json()
      lastChange.value = data.last_change
      currentDuration.value = data.current_duration
      changesToday.value = data.changes_today
      currentOperator.value = data.current_operator || user.value?.roblox_username
      activityLogs.value = data.activity_logs || []
    }
  } catch (error) {
    console.error('Error obteniendo información SSU:', error)
  }
}

const toggleSSU = () => {
  if (!hasPermission.value || toggleInProgress.value) return
  showConfirmationModal.value = true
}

const confirmToggle = async () => {
  toggleInProgress.value = true
  showConfirmationModal.value = false
  
  try {
    const response = await fetch('/api/ssu/toggle/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      ssuStatus.value = data.ssu_status
      
      // Actualizar información
      await fetchSSUInfo()
      
      // Agregar al log local
      addToActivityLog()
      
      // Pequeño delay para feedback visual
      setTimeout(() => {
        toggleInProgress.value = false
      }, 500)
    } else {
      console.error('Error al cambiar estado SSU')
      toggleInProgress.value = false
    }
  } catch (error) {
    console.error('Error al cambiar estado SSU:', error)
    toggleInProgress.value = false
  }
}

const cancelToggle = () => {
  showConfirmationModal.value = false
}

const addToActivityLog = () => {
  const now = new Date()
  const timeString = now.toLocaleTimeString('es-ES', { 
    hour: '2-digit', 
    minute: '2-digit',
    second: '2-digit' 
  })
  
  const newLog = {
    time: timeString,
    action: ssuStatus.value ? 'DEACTIVATED' : 'ACTIVATED',
    operator: user.value?.roblox_username || 'DESCONOCIDO'
  }
  
  activityLogs.value.unshift(newLog)
  
  // Mantener solo los últimos 10 registros
  if (activityLogs.value.length > 10) {
    activityLogs.value = activityLogs.value.slice(0, 10)
  }
}

const getCSRFToken = () => {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1]
  return cookieValue || ''
}

const goBack = () => {
  router.push('/moderation')
}

// Lifecycle
onMounted(() => {
  updateTime()
  const timeInterval = setInterval(updateTime, 1000)
  
  fetchCurrentUser()
  
  return () => {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
/* Estilos base */
.ssu-page {
  position: relative;
  min-height: 100vh;
  color: #d8d8d8;
  background: #0a0a0a;
  font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.5;
  overflow-x: hidden;
  padding: 20px;
  box-sizing: border-box;
}

/* Fondo SCP (mismo que otros componentes) */
.site-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: 
    linear-gradient(135deg, #0a0a0a 0%, #121212 25%, #0a0a0a 50%, #121212 75%, #0a0a0a 100%),
    radial-gradient(circle at 20% 30%, rgba(30, 30, 30, 0.8) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(40, 40, 40, 0.6) 0%, transparent 50%);
  z-index: 0;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(60, 60, 60, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(60, 60, 60, 0.1) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: gridMove 20s linear infinite;
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 10% 20%, rgba(100, 100, 100, 0.05) 1px, transparent 1px),
    radial-gradient(circle at 90% 80%, rgba(100, 100, 100, 0.05) 1px, transparent 1px);
  background-size: 30px 30px;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(80, 80, 80, 0.8) 10%, 
    rgba(120, 120, 120, 0.9) 50%, 
    rgba(80, 80, 80, 0.8) 90%, 
    transparent 100%);
  animation: scan 6s linear infinite;
  z-index: 1;
  opacity: 0.3;
}

@keyframes scan {
  0% { top: 0%; }
  100% { top: 100%; }
}

@keyframes gridMove {
  0% { transform: translateY(0); }
  100% { transform: translateY(40px); }
}

/* Header */
.ssu-header {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: rgba(15, 15, 15, 0.95);
  border: 1px solid #333;
  border-radius: 0px;
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  border-radius: 2px;
}

.header-icon svg {
  width: 24px;
  height: 24px;
  color: #ff3333;
}

.header-title {
  display: flex;
  flex-direction: column;
}

.header-main {
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: #ff3333;
  text-transform: uppercase;
  line-height: 1.2;
}

.header-sub {
  font-size: 0.7rem;
  letter-spacing: 0.5px;
  color: #888;
  text-transform: uppercase;
}

.header-right {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 16px;
}

.back-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  color: #aaa;
  font-family: 'Consolas', monospace;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.back-button:hover {
  background: rgba(50, 50, 50, 0.7);
  border-color: #555;
  color: #fff;
}

.back-button svg {
  width: 16px;
  height: 16px;
}

.session-status {
  display: flex;
  align-items: center;
  gap: 6px;
}

.session-indicator {
  width: 6px;
  height: 6px;
  border-radius: 0px;
  background: #4CAF50;
  box-shadow: 0 0 6px #4CAF50;
  animation: pulse 2s infinite;
}

.session-text {
  font-size: 11px;
  color: #4CAF50;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  font-weight: 600;
}

.current-time {
  font-size: 11px;
  color: #888;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.3px;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

/* Contenido Principal */
.ssu-main {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
}

.ssu-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

/* Sección de Encabezado */
.ssu-header-section {
  text-align: center;
  padding: 30px;
  background: rgba(20, 20, 20, 0.9);
  border: 1px solid #333;
  border-radius: 0px;
}

.ssu-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin: 0 0 10px 0;
  text-shadow: 0 0 15px rgba(255, 51, 51, 0.4);
}

.ssu-subtitle {
  font-size: 1rem;
  color: #aaa;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 30px;
}

/* Estado Actual */
.current-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 20px;
  background: rgba(30, 30, 30, 0.8);
  border: 2px solid #444;
  border-radius: 0px;
  max-width: 500px;
  margin: 0 auto;
  transition: all 0.3s ease;
}

.current-status.on {
  border-color: #00aa00;
  background: rgba(0, 40, 0, 0.3);
}

.current-status.off {
  border-color: #aa0000;
  background: rgba(40, 0, 0, 0.3);
}

.status-icon {
  width: 50px;
  height: 50px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.status-icon svg {
  width: 30px;
  height: 30px;
  color: #ff3333;
}

.status-info {
  flex: 1;
  position: relative;
}

.status-label {
  display: block;
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
  margin-bottom: 5px;
}

.status-value {
  display: block;
  font-size: 1.8rem;
  font-weight: 900;
  font-family: 'Consolas', monospace;
  letter-spacing: 1px;
}

.status-value.on {
  color: #00ff00;
  text-shadow: 0 0 15px rgba(0, 255, 0, 0.4);
}

.status-value.off {
  color: #ff3333;
  text-shadow: 0 0 15px rgba(255, 51, 51, 0.4);
}

.status-indicator {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #333;
  transition: all 0.3s ease;
}

.status-indicator.active {
  background: #00ff00;
  box-shadow: 0 0 10px #00ff00;
  animation: pulse 2s infinite;
}

/* Interruptor Cómicamente Grande */
.comic-switch-container {
  text-align: center;
  padding: 40px;
  background: rgba(15, 15, 15, 0.95);
  border: 1px solid #444;
  border-radius: 0px;
}

.switch-label {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 30px;
  text-shadow: 0 0 10px rgba(255, 51, 51, 0.3);
}

.comic-switch {
  position: relative;
  display: inline-block;
  cursor: pointer;
  user-select: none;
  transition: all 0.3s ease;
}

.comic-switch:hover {
  transform: scale(1.02);
}

.switch-frame {
  position: relative;
  padding: 30px;
  background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
  border: 3px solid #555;
  border-radius: 10px;
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.switch-base {
  position: relative;
  width: 400px;
  height: 100px;
  background: #222;
  border: 2px solid #444;
  border-radius: 5px;
  overflow: hidden;
}

.switch-slider {
  position: absolute;
  top: 10px;
  width: 180px;
  height: 80px;
  background: linear-gradient(135deg, #333 0%, #444 100%);
  border: 2px solid #666;
  border-radius: 5px;
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  cursor: pointer;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.switch-slider.on {
  left: 210px;
  background: linear-gradient(135deg, #004400 0%, #006600 100%);
  border-color: #00aa00;
}

.switch-slider.off {
  left: 10px;
  background: linear-gradient(135deg, #440000 0%, #660000 100%);
  border-color: #aa0000;
}

.position-indicator {
  background: rgba(0, 0, 0, 0.7);
  padding: 5px 15px;
  border-radius: 3px;
}

.position-text {
  font-size: 1.2rem;
  font-weight: 900;
  color: #fff;
  font-family: 'Consolas', monospace;
  letter-spacing: 2px;
}

.grip-handle {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.grip-line {
  width: 30px;
  height: 3px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 1.5px;
}

.switch-track {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.track-end {
  font-size: 1.5rem;
  font-weight: 900;
  font-family: 'Consolas', monospace;
  letter-spacing: 2px;
  padding: 10px 20px;
  border-radius: 3px;
  z-index: 1;
}

.track-end.on {
  color: #00ff00;
  background: rgba(0, 100, 0, 0.3);
  border: 1px solid rgba(0, 255, 0, 0.3);
}

.track-end.off {
  color: #ff3333;
  background: rgba(100, 0, 0, 0.3);
  border: 1px solid rgba(255, 51, 51, 0.3);
}

.track-middle {
  display: flex;
  flex-direction: column;
  gap: 5px;
  flex: 1;
  align-items: center;
}

.track-line {
  width: 100%;
  height: 2px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 1px;
}

.status-panel {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
  padding: 10px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid #444;
  border-radius: 3px;
}

.led-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #333;
  transition: all 0.3s ease;
}

.led-indicator.active.on {
  background: #00ff00;
  box-shadow: 0 0 10px #00ff00;
}

.led-indicator.active.off {
  background: #ff3333;
  box-shadow: 0 0 10px #ff3333;
}

.panel-text {
  font-size: 0.9rem;
  color: #aaa;
  font-family: 'Consolas', monospace;
  letter-spacing: 1px;
}

.action-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.action-label {
  font-size: 0.9rem;
  font-weight: 600;
  padding: 5px 15px;
  border-radius: 3px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.action-label.on {
  color: #00ff00;
  background: rgba(0, 100, 0, 0.2);
  border: 1px solid rgba(0, 255, 0, 0.2);
}

.action-label.off {
  color: #ff3333;
  background: rgba(100, 0, 0, 0.2);
  border: 1px solid rgba(255, 51, 51, 0.2);
}

.switch-instructions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 30px;
  padding: 15px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  border-radius: 3px;
}

.instruction-icon {
  width: 24px;
  height: 24px;
  color: #ff3333;
}

.instruction-text {
  font-size: 0.9rem;
  color: #aaa;
  font-weight: 500;
}

/* Panel de Información */
.info-panel {
  background: rgba(15, 15, 15, 0.95);
  border: 1px solid #333;
  border-radius: 0px;
  padding: 25px;
}

.info-header {
  text-align: center;
  margin-bottom: 25px;
}

.info-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 8px 0;
}

.info-subtitle {
  font-size: 0.8rem;
  color: #888;
  letter-spacing: 0.3px;
  text-transform: uppercase;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 0.75rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.info-value {
  font-size: 0.85rem;
  font-weight: 600;
  color: #ddd;
  font-family: 'Consolas', monospace;
}

/* Logs de Actividad */
.activity-logs {
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  padding: 20px;
  margin-top: 20px;
}

.logs-title {
  font-size: 0.9rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 51, 51, 0.3);
}

.logs-container {
  max-height: 300px;
  overflow-y: auto;
}

.log-item {
  display: grid;
  grid-template-columns: 80px 1fr 150px;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 0.8rem;
}

.log-item:last-child {
  border-bottom: none;
}

.log-time {
  color: #888;
  font-family: 'Consolas', monospace;
}

.log-action {
  font-weight: 600;
  font-family: 'Consolas', monospace;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.log-action.on {
  color: #00ff00;
}

.log-action.off {
  color: #ff3333;
}

.log-operator {
  color: #aaa;
  text-align: right;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Sin Permisos */
.no-permission {
  text-align: center;
  padding: 60px 30px;
  background: rgba(20, 20, 20, 0.9);
  border: 1px solid #aa2222;
  border-radius: 0px;
}

.permission-icon {
  width: 80px;
  height: 80px;
  color: #aa2222;
  margin: 0 auto 20px;
}

.permission-title {
  font-size: 1.8rem;
  font-weight: 900;
  color: #aa2222;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0 0 15px 0;
}

.permission-text {
  font-size: 1rem;
  color: #d8d8d8;
  line-height: 1.6;
  margin: 0 0 30px 0;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.permission-requirements {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
  background: rgba(40, 20, 20, 0.6);
  border: 1px solid rgba(170, 34, 34, 0.3);
  border-radius: 0px;
  max-width: 400px;
  margin: 0 auto 30px;
}

.requirement-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.requirement-item:last-child {
  border-bottom: none;
}

.requirement-label {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.requirement-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #aa2222;
  font-family: 'Consolas', monospace;
}

.back-button {
  padding: 12px 30px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  border-radius: 0px;
  color: #aa2222;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 200px;
}

.back-button:hover {
  background: rgba(170, 34, 34, 0.2);
  border-color: rgba(170, 34, 34, 0.5);
  transform: translateY(-1px);
}

/* Modal de Confirmación */
.confirmation-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
}

.modal-content {
  position: relative;
  background: rgba(15, 15, 15, 0.98);
  border: 2px solid #444;
  border-radius: 0px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
  animation: modalAppear 0.3s ease forwards;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  padding: 30px 30px 20px 30px;
  text-align: center;
  border-bottom: 1px solid #333;
}

.modal-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 15px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid currentColor;
}

.modal-icon.on {
  color: #00aa00;
  background: rgba(0, 40, 0, 0.3);
}

.modal-icon.off {
  color: #aa0000;
  background: rgba(40, 0, 0, 0.3);
}

.modal-icon svg {
  width: 30px;
  height: 30px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 900;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0;
}

.modal-body {
  padding: 30px;
}

.modal-text {
  font-size: 1rem;
  color: #d8d8d8;
  line-height: 1.6;
  margin: 0 0 30px 0;
}

.effects-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.effect-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #555;
  border-radius: 3px;
}

.effect-icon {
  width: 24px;
  height: 24px;
  color: #ff3333;
  flex-shrink: 0;
}

.effect-text {
  font-size: 0.9rem;
  color: #d8d8d8;
}

.modal-footer {
  padding: 20px 30px 30px 30px;
  text-align: center;
  border-top: 1px solid #333;
  display: flex;
  gap: 15px;
}

.modal-button {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 0px;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Consolas', monospace;
}

.modal-button.cancel {
  background: rgba(80, 80, 80, 0.6);
  border: 1px solid #666;
  color: #ddd;
}

.modal-button.cancel:hover {
  background: rgba(100, 100, 100, 0.8);
  border-color: #777;
}

.modal-button.confirm {
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  color: #ff3333;
}

.modal-button.confirm:hover {
  background: rgba(255, 51, 51, 0.2);
  border-color: rgba(255, 51, 51, 0.5);
}

/* Responsive */
@media (max-width: 768px) {
  .ssu-page {
    padding: 10px;
  }
  
  .ssu-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .header-left {
    flex-direction: column;
    text-align: center;
  }
  
  .header-right {
    align-items: center;
  }
  
  .ssu-title {
    font-size: 2rem;
  }
  
  .switch-base {
    width: 100%;
    max-width: 400px;
  }
  
  .switch-slider {
    width: 45%;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .log-item {
    grid-template-columns: 70px 1fr 100px;
    font-size: 0.7rem;
  }
  
  .modal-footer {
    flex-direction: column;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .switch-base {
    width: 350px;
  }
  
  .switch-slider {
    width: 160px;
  }
  
  .switch-slider.on {
    left: 180px;
  }
}
</style>