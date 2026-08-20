<template>
  <div v-if="!currentUser?.is_authenticated" class="login-required-overlay">
    <div class="scp-login-modal">
      <!-- Encabezado del modal -->
      <div class="modal-header">
        <div class="modal-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="#fc6f03" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        </div>
        <div class="modal-title-section">
          <h2 class="modal-title">ACCESO RESTRINGIDO</h2>
          <div class="modal-subtitle">SISTEMA DE GESTIÓN DE AGENTES - CLEARANCE LEVEL 2 REQUERIDO</div>
        </div>
        <div class="modal-status">
          <div class="status-indicator denied"></div>
          <span class="status-text">ACCESO DENEGADO</span>
        </div>
      </div>

      <!-- Contenido del modal -->
      <div class="modal-content">
        <!-- Advertencia de seguridad -->
        <div class="security-warning">
          <div class="warning-header">
            <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            <h3>ADVERTENCIA DE SEGURIDAD NIVEL 4</h3>
          </div>
          <div class="warning-content">
            <p>Este sistema contiene información clasificada Nivel 2/SCP. El acceso está restringido a:</p>
            <ul>
              <li>Personal autorizado con nivel de autorización <strong>Level 2</strong> o superior</li>
              <li>Personal del Departamento de Seguridad de la Fundación</li>
              <li>Miembros del Consejo O5 con autorización explícita</li>
            </ul>
            <p class="warning-note">Cualquier intento de acceso no autorizado será registrado y reportado inmediatamente al Departamento de Seguridad Interna.</p>
          </div>
        </div>

        <!-- Información del sistema -->
        <div class="system-info">
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">SISTEMA:</span>
              <span class="info-value">AGENT-MANAGEMENT v2.4</span>
            </div>
            <div class="info-item">
              <span class="info-label">ESTADO:</span>
              <span class="info-value status-operational">OPERATIVO</span>
            </div>
            <div class="info-item">
              <span class="info-label">UBICACIÓN:</span>
              <span class="info-value">SITE-81</span>
            </div>
            <div class="info-item">
              <span class="info-label">CLASIFICACIÓN:</span>
              <span class="info-value status-classified">LEVEL 2/SCP</span>
            </div>
          </div>
        </div>

        <!-- Botón de acción -->
        <div class="action-section">
          <div class="action-required">
            <div class="required-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
            <div class="required-text">
              <h4>ACCIÓN REQUERIDA</h4>
              <p>Debe autenticarse para acceder al Sistema de Gestión de Agentes</p>
            </div>
          </div>
          
          <a :href="loginUrl" class="scp-login-button">
            <div class="button-glow"></div>
            <div class="button-content">
              <div class="button-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                  <polyline points="10 17 15 12 10 7"></polyline>
                  <line x1="15" y1="12" x2="3" y2="12"></line>
                </svg>
              </div>
              <div class="button-text">
                <span class="main-text">INICIAR SESIÓN CON ROBLOX</span>
                <span class="sub-text">Redirección automática habilitada</span>
              </div>
              <div class="button-indicator">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
              </div>
            </div>
          </a>

          <div class="login-info">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            <span>Será redirigido al portal de autenticación de Roblox. Al completar la autenticación, volverá automáticamente a esta página.</span>
          </div>
        </div>
      </div>

      <!-- Footer del modal -->
      <div class="modal-footer">
        <div class="footer-grid">
          <div class="footer-item">
            <span class="footer-label">REFERENCIA:</span>
            <span class="footer-value">AMS-81-02</span>
          </div>
          <div class="footer-item">
            <span class="footer-label">ÚLTIMO ACCESO:</span>
            <span class="footer-value">{{ currentTime }}</span>
          </div>
          <div class="footer-item">
            <span class="footer-label">AUDITORÍA:</span>
            <span class="footer-value">HABILITADA</span>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Slot para contenido normal (solo cuando el usuario está autenticado) -->
  <slot v-else></slot>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, computed } from 'vue'

// Props (opcional, para mayor flexibilidad)
const props = defineProps({
  redirectPath: {
    type: String,
    default: '/dashboard/personnel/'
  },
  user: {
    type: Object,
    default: null
  }
})

// Estado reactivo
const currentUser = ref(null)
const currentTime = ref('')

// Computed properties
const loginUrl = computed(() => {
  const nextUrl = encodeURIComponent(props.redirectPath)
  return `/accounts/login/roblox/?next=${nextUrl}`
})

// Métodos
const updateTime = () => {
  const now = new Date()
  const day = now.getDate().toString().padStart(2, '0')
  const month = (now.getMonth() + 1).toString().padStart(2, '0')
  const year = now.getFullYear()
  const hours = now.getHours().toString().padStart(2, '0')
  const minutes = now.getMinutes().toString().padStart(2, '0')
  const seconds = now.getSeconds().toString().padStart(2, '0')
  currentTime.value = `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`
}

const fetchCurrentUser = async () => {
  try {
    const response = await fetch('/api/auth/user/')
    if (response.ok) {
      currentUser.value = await response.json()
    }
  } catch (error) {
    console.error('Error fetching user:', error)
    currentUser.value = null
  }
}

// Control del scroll del body - MEJORADO
const controlBodyScroll = (needsLogin) => {
  if (needsLogin) {
    // Guardar la posición actual del scroll
    const scrollY = window.scrollY
    document.body.style.position = 'fixed'
    document.body.style.top = `-${scrollY}px`
    document.body.style.width = '100%'
    document.body.style.overflow = 'hidden'
    
    // Guardar la posición del scroll para restaurarla después
    document.body.dataset.savedScrollY = scrollY
  } else {
    // Restaurar la posición del scroll
    const savedScrollY = document.body.dataset.savedScrollY || '0'
    document.body.style.position = ''
    document.body.style.top = ''
    document.body.style.width = ''
    document.body.style.overflow = ''
    
    // Restaurar la posición del scroll
    window.scrollTo(0, parseInt(savedScrollY))
    delete document.body.dataset.savedScrollY
  }
}

// Watcher para controlar el scroll
watch(() => !currentUser.value?.is_authenticated, (needsLogin) => {
  controlBodyScroll(needsLogin)
}, { immediate: true })

// Ciclo de vida
onMounted(() => {
  updateTime()
  const timeInterval = setInterval(updateTime, 1000)
  
  // Obtener usuario actual
  fetchCurrentUser()
  
  // También puedes hacer polling periódico si es necesario
  const userInterval = setInterval(fetchCurrentUser, 30000) // Cada 30 segundos
  
  // Limpiar intervalos al desmontar
  onBeforeUnmount(() => {
    clearInterval(timeInterval)
    clearInterval(userInterval)
    
    // Asegurarse de restaurar el scroll
    controlBodyScroll(false)
  })
})

// Exponer métodos si es necesario
defineExpose({
  refreshUser: fetchCurrentUser
})
</script>

<style scoped>
/* Overlay de login required - MODIFICADO para ocupar toda la pantalla */
.login-required-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  min-height: 100vh;
  min-height: 100dvh; /* Soporte para dispositivos móviles */
  background: rgba(0, 0, 0, 0.98);
  backdrop-filter: blur(15px);
  z-index: 9998;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  animation: fadeIn 0.3s ease;
  overflow-y: auto;
  padding-top: 80px;
}

.scp-login-modal {
  background: linear-gradient(135deg, 
    rgba(15, 15, 15, 0.98) 0%, 
    rgba(20, 20, 20, 0.98) 50%, 
    rgba(15, 15, 15, 0.98) 100%);
  border: 2px solid #333;
  width: 100%;
  max-width: 700px;
  max-height: 90vh; /* Limitar altura máxima al 90% de la pantalla */
  min-height: min-content; /* Asegurar que crezca con el contenido */
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9);
  position: relative;
  z-index: 9999;
}

.scp-login-modal::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, 
    #fc6f03 0%, 
    #ff3333 50%, 
    #fc6f03 100%);
  z-index: 3;
}

/* Header del modal */
.modal-header {
  padding: 1.5rem 1.5rem 1rem 1.5rem;
  background: rgba(25, 25, 25, 0.95);
  border-bottom: 1px solid #333;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  flex-wrap: wrap;
  flex-shrink: 0; /* Evitar que el header se encoja */
}

.modal-icon {
  width: 45px;
  height: 45px;
  background: rgba(252, 111, 3, 0.1);
  border: 1px solid rgba(252, 111, 3, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.modal-icon svg {
  width: 24px;
  height: 24px;
  color: #fc6f03;
}

.modal-title-section {
  flex: 1;
  min-width: 200px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0 0 0.2rem 0;
  font-family: 'Consolas', 'Courier New', monospace;
  text-shadow: 0 2px 4px rgba(255, 51, 51, 0.3);
  line-height: 1.2;
}

.modal-subtitle {
  font-size: 0.75rem;
  color: #888;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  font-weight: 600;
  line-height: 1.2;
}

.modal-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  padding: 0.5rem 1rem;
  flex-shrink: 0;
}

.status-indicator.denied {
  width: 8px;
  height: 8px;
  background: #ff3333;
  box-shadow: 0 0 8px #ff3333;
  animation: pulse 1.5s infinite;
}

.status-text {
  font-size: 0.8rem;
  color: #ff3333;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

/* Contenido del modal */
.modal-content {
  flex: 1; /* Ocupar espacio restante */
  padding: 1.5rem;
  overflow-y: auto; /* Scroll interno si el contenido es muy largo */
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  min-height: 0; /* Importante para que el flex funcione correctamente con scroll */
}

/* Advertencia de seguridad */
.security-warning {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  padding: 1.2rem;
  border-radius: 2px;
  flex-shrink: 0;
}

.warning-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 1rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid rgba(255, 51, 51, 0.3);
}

.warning-header svg {
  width: 22px;
  height: 22px;
  color: #ff3333;
  flex-shrink: 0;
}

.warning-header h3 {
  font-size: 1rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0;
  font-family: 'Consolas', monospace;
  line-height: 1.2;
}

.warning-content {
  color: #ddd;
  line-height: 1.5;
  font-size: 0.9rem;
}

.warning-content p {
  margin: 0 0 0.8rem 0;
}

.warning-content ul {
  margin: 0.8rem 0;
  padding-left: 1.2rem;
}

.warning-content li {
  margin: 0.4rem 0;
  color: #ccc;
  font-size: 0.9rem;
}

.warning-content strong {
  color: #fc6f03;
}

.warning-note {
  font-style: italic;
  color: #ff6666;
  border-left: 3px solid #ff3333;
  padding-left: 1rem;
  margin-top: 1rem !important;
}

/* Información del sistema */
.system-info {
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  padding: 1.2rem;
  border-radius: 2px;
  flex-shrink: 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.info-label {
  font-size: 0.7rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
  line-height: 1.2;
}

.info-value {
  font-size: 0.9rem;
  color: #ddd;
  font-weight: 600;
  letter-spacing: 0.3px;
  line-height: 1.2;
}

.info-value.status-operational {
  color: #4CAF50;
}

.info-value.status-classified {
  color: #ff3333;
  background: rgba(255, 51, 51, 0.1);
  padding: 0.2rem 0.5rem;
  display: inline-block;
  border-radius: 2px;
}

/* Botón de acción */
.action-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  flex-shrink: 0; /* Evitar que se encoja */
  margin-bottom: auto; /* Empujar hacia arriba si hay espacio extra */
}

.action-required {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  padding: 0.8rem;
}

.required-icon {
  width: 36px;
  height: 36px;
  background: rgba(76, 175, 80, 0.2);
  border: 1px solid rgba(76, 175, 80, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.required-icon svg {
  width: 18px;
  height: 18px;
  color: #4CAF50;
}

.required-text {
  flex: 1;
}

.required-text h4 {
  font-size: 0.95rem;
  color: #4CAF50;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 0.3rem 0;
  font-family: 'Consolas', monospace;
  line-height: 1.2;
}

.required-text p {
  font-size: 0.85rem;
  color: #aaa;
  margin: 0;
  line-height: 1.2;
}

.scp-login-button {
  display: block;
  background: rgba(30, 30, 30, 0.9);
  border: 2px solid #4CAF50;
  color: #4CAF50;
  text-decoration: none;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  flex-shrink: 0;
}

.scp-login-button:hover {
  border-color: #66BB6A;
  background: rgba(76, 175, 80, 0.05);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(76, 175, 80, 0.3);
}

.button-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(76, 175, 80, 0.2) 50%, 
    transparent 100%);
  transition: left 0.5s ease;
}

.scp-login-button:hover .button-glow {
  left: 100%;
}

.button-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.2rem 1.5rem;
  position: relative;
  z-index: 1;
}

.button-icon {
  width: 28px;
  height: 28px;
  color: currentColor;
}

.button-text {
  flex: 1;
  margin: 0 1.5rem;
  text-align: center;
}

.main-text {
  display: block;
  font-size: 1.1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.2rem;
  font-family: 'Consolas', monospace;
  line-height: 1.2;
}

.sub-text {
  display: block;
  font-size: 0.8rem;
  color: #88cc88;
  letter-spacing: 0.3px;
  line-height: 1.2;
}

.button-indicator {
  width: 24px;
  height: 24px;
  color: currentColor;
}

.login-info {
  display: flex;
  align-items: flex-start;
  gap: 0.8rem;
  color: #888;
  font-size: 0.85rem;
  line-height: 1.4;
  flex-shrink: 0;
}

.login-info svg {
  width: 16px;
  height: 16px;
  color: #888;
  margin-top: 0.2rem;
  flex-shrink: 0;
}

/* Footer del modal */
.modal-footer {
  padding: 1.2rem 1.5rem;
  background: rgba(25, 25, 25, 0.95);
  border-top: 1px solid #333;
  flex-shrink: 0; /* Evitar que el footer se encoja */
}

.footer-grid {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.footer-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.footer-label {
  font-size: 0.6rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
  line-height: 1.2;
}

.footer-value {
  font-size: 0.75rem;
  color: #aaa;
  font-weight: 600;
  letter-spacing: 0.3px;
  line-height: 1.2;
}

/* Animaciones */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

/* Responsive */
@media (max-width: 768px) {
  .login-required-overlay {
    padding: 1rem;
    align-items: flex-start; /* Alinear al inicio en móviles */
  }
  
  .scp-login-modal {
    max-height: 95vh; /* Más alto en móviles */
    margin-top: 1rem;
    margin-bottom: 1rem;
  }
  
  .modal-header {
    padding: 1rem;
    flex-direction: column;
    text-align: center;
    gap: 0.8rem;
  }
  
  .modal-title {
    font-size: 1.3rem;
  }
  
  .modal-status {
    width: 100%;
    justify-content: center;
  }
  
  .modal-content {
    padding: 1rem;
    gap: 1rem;
  }
  
  .security-warning,
  .system-info,
  .action-section {
    padding: 1rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .footer-grid {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .button-content {
    padding: 1rem;
  }
  
  .button-text {
    margin: 0 1rem;
  }
  
  .main-text {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .login-required-overlay {
    padding: 0.5rem;
  }
  
  .scp-login-modal {
    max-height: 100vh; /* Usar toda la pantalla en móviles pequeños */
    margin: 0;
    border-width: 1px;
  }
  
  .modal-title {
    font-size: 1.1rem;
  }
  
  .warning-header h3 {
    font-size: 0.9rem;
  }
  
  .warning-content p,
  .warning-content li {
    font-size: 0.85rem;
  }
  
  .button-content {
    flex-direction: column;
    gap: 0.8rem;
  }
  
  .button-icon,
  .button-indicator {
    display: none;
  }
  
  .button-text {
    margin: 0;
  }
  
  .modal-content {
    padding: 0.75rem;
  }
}
</style>