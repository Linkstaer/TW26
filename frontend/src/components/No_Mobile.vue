<template>
  <!-- Overlay que cubre toda la página -->
  <div v-if="isMobile" class="mobile-block-overlay">
    <div class="scp-mobile-block">
      <!-- Encabezado SCP -->
      <div class="block-header">
        <div class="block-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <!-- Círculo exterior con corte (estilo candado) -->
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z" stroke="#ff3333" stroke-width="2"/>
            <!-- Cuerpo del candado -->
            <rect x="8" y="10" width="8" height="6" rx="1" stroke="#ff3333" stroke-width="1.5"/>
            <!-- Arco del candado -->
            <path d="M12 6C10.5 6 9 7.5 9 9v1h6V9c0-1.5-1.5-3-3-3z" stroke="#ff3333" stroke-width="1.5"/>
            <!-- SCP en el interior -->
            <text x="12" y="14" text-anchor="middle" font-family="'Courier New', monospace" font-size="3.5" font-weight="bold" fill="#ff3333">
                SCP
            </text>
            <!-- Líneas de restricción -->
            <line x1="6" y1="6" x2="10" y2="10" stroke="#ff3333" stroke-width="1"/>
            <line x1="18" y1="6" x2="14" y2="10" stroke="#ff3333" stroke-width="1"/>
            <line x1="6" y1="18" x2="10" y2="14" stroke="#ff3333" stroke-width="1"/>
            <line x1="18" y1="18" x2="14" y2="14" stroke="#ff3333" stroke-width="1"/>
            </svg>
        </div>
        <div class="block-title-section">
          <h2 class="block-title">ACCESO RESTRINGIDO</h2>
          <div class="block-subtitle">INTERFAZ MÓVIL NO SOPORTADA</div>
        </div>
        <div class="block-status">
          <div class="status-indicator mobile-denied"></div>
          <span class="status-text">COMPATIBILITY ERROR</span>
        </div>
      </div>

      <!-- Contenido principal -->
      <div class="block-content">
        <!-- Advertencia del sistema -->
        <div class="system-warning">
          <div class="warning-header">
            <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <h3>LIMITACIÓN DE PLATAFORMA DETECTADA</h3>
          </div>
          <div class="warning-content">
            <p>El <strong>Sistema de Gestión v2.4</strong> requiere capacidades de pantalla completa y herramientas de administración avanzadas que no están disponibles en dispositivos móviles.</p>
            
            <div class="requirement-list">
              <div class="requirement-item">
                <div class="req-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="#fc6f03" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                    <line x1="8" y1="21" x2="16" y2="21"></line>
                    <line x1="12" y1="17" x2="12" y2="21"></line>
                  </svg>
                </div>
                <div class="req-text">
                  <strong>Requisito Mínimo:</strong> Pantalla de 1024px o superior
                </div>
              </div>
              
              <div class="requirement-item">
                <div class="req-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="#fc6f03" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 7V4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3"></path>
                    <path d="M5 20h14"></path>
                    <path d="M8 10v11"></path>
                    <path d="M16 10v11"></path>
                    <path d="M12 4v16"></path>
                  </svg>
                </div>
                <div class="req-text">
                  <strong>Recomendado:</strong> Escritorio con navegador moderno
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Información técnica -->
        <div class="tech-info">
          <div class="info-grid">
            <div class="info-item">
              <span class="info-label">RESOLUCIÓN DETECTADA:</span>
              <span class="info-value">{{ screenWidth }} × {{ screenHeight }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">ESTADO DEL SISTEMA:</span>
              <span class="info-value status-error">INCOMPATIBLE</span>
            </div>
            <div class="info-item">
              <span class="info-label">PLATAFORMA:</span>
              <span class="info-value">{{ platform }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">REQUERIMIENTO:</span>
              <span class="info-value">ESCRITORIO</span>
            </div>
          </div>
        </div>

        <!-- Instrucciones -->
        <div class="instructions">
          <div class="instructions-header">
            <svg viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
            <h4>PROCEDIMIENTO DE ACCESO</h4>
          </div>
          <div class="instructions-content">
            <p>Para acceder al Sistema de Gestión de Agentes:</p>
            <ol>
              <li>Utilice una computadora de escritorio o laptop</li>
              <li>Asegúrese de tener una resolución mínima de 1024×768</li>
              <li>Utilice Chrome, Firefox o Edge actualizado</li>
              <li>Active JavaScript en su navegador</li>
              <li>Acceda desde una red segura y autorizada</li>
            </ol>
          </div>
        </div>

        <!-- Botón Volver a Inicio -->
        <div class="home-button-container">
          <button @click="goToHome" class="home-button">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
            <span>VOLVER A INICIO</span>
          </button>
        </div>
      </div>

      <!-- Footer -->
      <div class="block-footer">
        <div class="footer-grid">
          <div class="footer-item">
            <span class="footer-label">REFERENCIA:</span>
            <span class="footer-value">AMS-MOB-01</span>
          </div>
          <div class="footer-item">
            <span class="footer-label">ÚLTIMO INTENTO:</span>
            <span class="footer-value">{{ currentTime }}</span>
          </div>
          <div class="footer-item">
            <span class="footer-label">ESTATUS:</span>
            <span class="footer-value">BLOQUEADO</span>
          </div>
        </div>
      </div>

      <!-- Elementos decorativos SCP -->
      <div class="scan-line"></div>
      <div class="grid-overlay"></div>
    </div>
  </div>
  
  <!-- Slot para contenido normal (solo en escritorio) -->
  <slot v-else></slot>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Estado reactivo
const isMobile = ref(false)
const screenWidth = ref(0)
const screenHeight = ref(0)
const platform = ref('')
const currentTime = ref('')

// Detectar si es móvil
// Detectar si es móvil (recomendada)
const checkIsMobile = () => {
  screenWidth.value = window.innerWidth
  screenHeight.value = window.innerHeight
  
  const userAgent = navigator.userAgent.toLowerCase()
  
  // Detectar plataforma
  if (/android/i.test(userAgent)) platform.value = 'Android'
  else if (/iphone|ipad|ipod/i.test(userAgent)) platform.value = 'iOS'
  else if (/windows phone/i.test(userAgent)) platform.value = 'Windows Mobile'
  else if (/blackberry/i.test(userAgent)) platform.value = 'BlackBerry'
  else platform.value = 'Escritorio'
  
  // Parámetros ajustables
  const MOBILE_MAX_WIDTH = 768
  const TABLET_MAX_WIDTH = 1024
  const MIN_ASPECT_RATIO = 1.3 // Para diferenciar móviles (más altos que anchos)
  
  // Calcular aspect ratio
  const aspectRatio = screenWidth.value / screenHeight.value
  
  // Lógica mejorada:
  const isMobileUserAgent = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini|mobile/i.test(userAgent)
  const isTabletUserAgent = /ipad|tablet/i.test(userAgent) && !/mobile/i.test(userAgent)
  
  // Detectar dispositivo real:
  if (screenWidth.value >= 1024) {
    // Pantallas grandes = siempre escritorio
    isMobile.value = false
  } else if (screenWidth.value <= MOBILE_MAX_WIDTH && aspectRatio < MIN_ASPECT_RATIO) {
    // Pantalla pequeña con aspecto de móvil
    isMobile.value = isMobileUserAgent && !isTabletUserAgent
  } else if (screenWidth.value <= TABLET_MAX_WIDTH) {
    // Tablet o pantalla mediana
    isMobile.value = false // Tratar como escritorio
  } else {
    // Cualquier otro caso = escritorio
    isMobile.value = false
  }
  
  // Sobreescribir si claramente es escritorio por user agent
  if (/windows|macintosh|linux/i.test(userAgent) && !/mobile|android|iphone/i.test(userAgent)) {
    isMobile.value = false
  }
}

// Actualizar hora actual
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

// Función para ir al inicio
const goToHome = () => {
  // Redirigir a la página de inicio
  // Puedes cambiar '/' por la ruta de tu página de inicio
  router.push('/')
}

// Controlar el scroll del body
const toggleBodyScroll = (disable) => {
  if (disable) {
    document.body.style.overflow = 'hidden'
    document.body.style.position = 'fixed'
    document.body.style.width = '100%'
    document.body.style.height = '100%'
  } else {
    document.body.style.overflow = ''
    document.body.style.position = ''
    document.body.style.width = ''
    document.body.style.height = ''
  }
}

// Listener para resize
const handleResize = () => {
  checkIsMobile()
}

// Watch para controlar el scroll cuando cambia isMobile
watch(isMobile, (newValue) => {
  toggleBodyScroll(newValue)
})

// Ciclo de vida
onMounted(() => {
  checkIsMobile()
  updateTime()
  
  // Aplicar scroll bloqueado si es móvil
  if (isMobile.value) {
    toggleBodyScroll(true)
  }
  
  // Actualizar hora cada segundo
  const timeInterval = setInterval(updateTime, 1000)
  
  // Escuchar cambios de tamaño
  window.addEventListener('resize', handleResize)
  
  // Limpiar intervalos al desmontar
  onBeforeUnmount(() => {
    clearInterval(timeInterval)
    window.removeEventListener('resize', handleResize)
    toggleBodyScroll(false) // Restaurar scroll al desmontar
  })
})
</script>

<style scoped>
/* Estilos para deshabilitar scroll en toda la página */
body {
  margin: 0;
  padding: 0;
}

.mobile-block-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.98);
  backdrop-filter: blur(10px);
  z-index: 99999; /* Z-index muy alto para estar sobre todo */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  animation: fadeIn 0.5s ease;
  overflow-y: auto; /* Permitir scroll solo dentro del overlay si es necesario */
  -webkit-overflow-scrolling: touch;
}

.scp-mobile-block {
  background: linear-gradient(135deg, 
    rgba(15, 15, 15, 0.95) 0%, 
    rgba(20, 20, 20, 0.95) 50%, 
    rgba(15, 15, 15, 0.95) 100%);
  border: 2px solid #333;
  width: 100%;
  max-width: 800px;
  max-height: calc(100vh - 2rem); /* Asegura que no exceda la altura visible */
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
  position: relative;
  z-index: 2;
}

.scp-mobile-block::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, 
    #ff3333 0%, 
    #fc6f03 50%, 
    #ff3333 100%);
  z-index: 3;
}

/* Header */
.block-header {
  padding: 1.5rem;
  background: rgba(25, 25, 25, 0.95);
  border-bottom: 1px solid #333;
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
  flex-wrap: wrap;
}

.block-icon {
  width: 50px;
  height: 50px;
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.block-icon svg {
  width: 28px;
  height: 28px;
  color: #ff3333;
}

.block-title-section {
  flex: 1;
  min-width: 200px;
}

.block-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0 0 0.3rem 0;
  font-family: 'Consolas', 'Courier New', monospace;
  text-shadow: 0 2px 4px rgba(255, 51, 51, 0.3);
  line-height: 1.2;
}

.block-subtitle {
  font-size: 0.8rem;
  color: #888;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  font-weight: 600;
  line-height: 1.2;
}

.block-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  padding: 0.5rem 1rem;
  flex-shrink: 0;
}

.status-indicator.mobile-denied {
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

/* Contenido */
.block-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Botón Volver a Inicio */
.home-button-container {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.home-button {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: linear-gradient(135deg, #ff3333 0%, #fc6f03 100%);
  border: none;
  color: white;
  padding: 0.8rem 2rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(255, 51, 51, 0.3);
  font-family: 'Consolas', 'Courier New', monospace;
}

.home-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 51, 51, 0.4);
  background: linear-gradient(135deg, #ff4444 0%, #fd7f1a 100%);
}

.home-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(255, 51, 51, 0.3);
}

.home-button svg {
  width: 20px;
  height: 20px;
}

/* Advertencia del sistema */
.system-warning {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  padding: 1.2rem;
  border-radius: 2px;
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
  width: 24px;
  height: 24px;
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
}

.warning-content p {
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
}

.warning-content strong {
  color: #fc6f03;
}

.requirement-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin-top: 1rem;
}

.requirement-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  padding: 0.8rem;
  border-radius: 2px;
}

.req-icon {
  width: 32px;
  height: 32px;
  background: rgba(252, 111, 3, 0.1);
  border: 1px solid rgba(252, 111, 3, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.req-icon svg {
  width: 18px;
  height: 18px;
  color: #fc6f03;
}

.req-text {
  flex: 1;
  font-size: 0.9rem;
  color: #ccc;
}

.req-text strong {
  color: #fc6f03;
}

/* Información técnica */
.tech-info {
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  padding: 1.2rem;
  border-radius: 2px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.8rem;
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

.info-value.status-error {
  color: #ff3333;
  background: rgba(255, 51, 51, 0.1);
  padding: 0.2rem 0.5rem;
  display: inline-block;
  border-radius: 2px;
}

/* Instrucciones */
.instructions {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  padding: 1.2rem;
  border-radius: 2px;
}

.instructions-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 1rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid rgba(76, 175, 80, 0.3);
}

.instructions-header svg {
  width: 24px;
  height: 24px;
  color: #4CAF50;
  flex-shrink: 0;
}

.instructions-header h4 {
  font-size: 1rem;
  color: #4CAF50;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0;
  font-family: 'Consolas', monospace;
  line-height: 1.2;
}

.instructions-content {
  color: #ddd;
  line-height: 1.5;
}

.instructions-content p {
  margin: 0 0 0.8rem 0;
  font-size: 0.95rem;
}

.instructions-content ol {
  margin: 0;
  padding-left: 1.5rem;
}

.instructions-content li {
  margin: 0.5rem 0;
  color: #ccc;
  font-size: 0.9rem;
}

/* Footer */
.block-footer {
  padding: 1.2rem 1.5rem;
  background: rgba(25, 25, 25, 0.95);
  border-top: 1px solid #333;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.footer-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.footer-label {
  font-size: 0.65rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
  line-height: 1.2;
}

.footer-value {
  font-size: 0.8rem;
  color: #aaa;
  font-weight: 600;
  letter-spacing: 0.3px;
  line-height: 1.2;
}

/* Elementos decorativos SCP */
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
  pointer-events: none;
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
  pointer-events: none;
  opacity: 0.5;
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

@keyframes scan {
  0% { top: 0%; }
  100% { top: 100%; }
}

@keyframes gridMove {
  0% { transform: translateY(0); }
  100% { transform: translateY(40px); }
}

/* Responsive para el propio bloque en móviles */
@media (max-width: 768px) {
  .mobile-block-overlay {
    padding: 0.5rem;
  }
  
  .scp-mobile-block {
    max-height: 95vh;
  }
  
  .block-header {
    padding: 1rem;
    flex-direction: column;
    text-align: center;
    gap: 0.8rem;
  }
  
  .block-title {
    font-size: 1.3rem;
  }
  
  .block-status {
    width: 100%;
    justify-content: center;
  }
  
  .block-content {
    padding: 1rem;
    gap: 1rem;
  }
  
  .system-warning,
  .tech-info,
  .instructions {
    padding: 1rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .footer-grid {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .instructions-content ol {
    padding-left: 1.2rem;
  }
  
  .home-button {
    padding: 0.7rem 1.5rem;
    font-size: 0.8rem;
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .block-title {
    font-size: 1.1rem;
  }
  
  .warning-header h3,
  .instructions-header h4 {
    font-size: 0.9rem;
  }
  
  .warning-content p,
  .instructions-content li {
    font-size: 0.85rem;
  }
  
  .info-label,
  .footer-label {
    font-size: 0.6rem;
  }
  
  .info-value,
  .footer-value {
    font-size: 0.75rem;
  }
}
</style>