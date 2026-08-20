<template>
  <div class="error-page">
    <!-- Fondo SCP -->
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
    </div>

    <!-- Error Content Section -->
    <section class="content-section">
      <div class="section-content">
        <!-- Header Móvil Expandido -->
        <div class="mobile-header">
          <div class="mobile-error-code">
            <div class="error-code-large">404</div>
            <div class="error-type">ERROR DE LOCALIZACIÓN</div>
          </div>
          
          <div class="mobile-error-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
          </div>
        </div>

        <!-- Contenido Principal -->
        <div class="error-content">
          <!-- Mensaje de Error -->
          <div class="error-message">
            <h1 class="error-title">RECURSO NO ENCONTRADO</h1>
            <p class="error-description">
              El recurso solicitado no ha sido localizado dentro de los registros de la Fundación SCP. 
              La ruta especificada puede haber sido reasignada, clasificada o eliminada por protocolos de seguridad.
            </p>
          </div>

          <!-- Detalles del Error -->
          <div class="error-details">
            <div class="detail-row">
              <div class="detail-label">CÓDIGO DE ERROR:</div>
              <div class="detail-value">404-NF</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">TIPO DE FALLO:</div>
              <div class="detail-value">LOCALIZACIÓN</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">TIEMPO DEL INCIDENTE:</div>
              <div class="detail-value">{{ currentTime }}</div>
            </div>
          </div>

          <!-- Estado del Sistema -->
          <div class="system-status">
            <div class="status-row">
              <div class="status-indicator inactive"></div>
              <div class="status-text">CONEXIÓN: INTERRUMPIDA</div>
            </div>
            <div class="status-row">
              <div class="status-indicator active"></div>
              <div class="status-text">SEGURIDAD: ACTIVA</div>
            </div>
          </div>

          <!-- Advertencia -->
          <div class="warning-box">
            <div class="warning-header">
              <div class="warning-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                  <line x1="12" y1="9" x2="12" y2="13"></line>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
              </div>
              <div class="warning-title">ADVERTENCIA DE SEGURIDAD</div>
            </div>
            <p class="warning-text">
              Los intentos repetidos de acceder a recursos no autorizados pueden resultar 
              en la revocación de privilegios de acceso y acciones disciplinarias.
            </p>
          </div>

          <!-- Botones de Acción -->
          <div class="action-container">
            <button class="action-button primary" @click="goHome">
              <div class="button-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                  <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
              </div>
              <span class="button-label">VOLVER AL INICIO</span>
            </button>
            
            <button class="action-button secondary" @click="goBack">
              <div class="button-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 12H5"></path>
                  <path d="M12 19l-7-7 7-7"></path>
                </svg>
              </div>
              <span class="button-label">PÁGINA ANTERIOR</span>
            </button>
          </div>

          <!-- Protocolos de Acción -->
          <div class="protocol-container">
            <div class="protocol-header">
              <div class="protocol-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                  <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                </svg>
              </div>
              <div class="protocol-title">PROTOCOLO DE ACCIÓN RECOMENDADO</div>
            </div>
            <div class="protocol-steps">
              <div class="protocol-step">
                <div class="step-number">1</div>
                <div class="step-text">Verificar la dirección del recurso solicitado</div>
              </div>
              <div class="protocol-step">
                <div class="step-number">2</div>
                <div class="step-text">Contactar con administración si el error persiste</div>
              </div>
              <div class="protocol-step">
                <div class="step-number">3</div>
                <div class="step-text">Reportar anomalías de navegación al departamento técnico</div>
              </div>
              <div class="protocol-step">
                <div class="step-number">4</div>
                <div class="step-text">Mantener registro del incidente para auditoría</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer Móvil -->
    <div class="mobile-footer">
      <div class="footer-line"></div>
      <div class="footer-content">
        <div class="footer-item">DOCUMENTO DE ERROR 404 GENERADO AUTOMÁTICAMENTE</div>
        <div class="footer-item">CONFIDENCIAL - ACCESO NO AUTORIZADO PROHIBIDO</div>
        <div class="footer-item classification">
          <div class="classification-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
          </div>
          <div class="classification-text">CLASIFICADO - NIVEL 2</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const currentTime = ref('')

const updateTime = () => {
  const now = new Date()
  const options = { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    hour: '2-digit', 
    minute: '2-digit', 
    second: '2-digit',
    hour12: false
  }
  currentTime.value = now.toLocaleString('es-ES', options).replace(',', '')
}

const goHome = () => {
  router.push('/')
}

const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    goHome()
  }
}

onMounted(() => {
  updateTime()
  const timer = setInterval(updateTime, 1000)
  
  onUnmounted(() => {
    clearInterval(timer)
  })
})
</script>

<style scoped>
/* Reset y base - Mobile First */
.error-page {
  position: relative;
  min-height: 100vh;
  color: #d8d8d8;
  background: #0a0a0a;
  overflow-x: hidden;
  font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.5;
  width: 100%;
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

/* Fondo SCP */
.site-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
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
  right: 0;
  bottom: 0;
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
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 10% 20%, rgba(100, 100, 100, 0.05) 1px, transparent 1px),
    radial-gradient(circle at 90% 80%, rgba(100, 100, 100, 0.05) 1px, transparent 1px);
  background-size: 30px 30px;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(80, 80, 80, 0.8) 10%, 
    rgba(120, 120, 120, 0.9) 50%, 
    rgba(80, 80, 80, 0.8) 90%, 
    transparent 100%);
  animation: scan 6s linear infinite;
  z-index: 1;
  opacity: 0.4;
}

@keyframes scan {
  0% { top: 0%; }
  100% { top: 100%; }
}

@keyframes gridMove {
  0% { transform: translateY(0); }
  100% { transform: translateY(40px); }
}

/* Sección de Contenido */
.content-section {
  position: relative;
  z-index: 1;
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 0;
  margin: 0;
}

.section-content {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 20px 16px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

/* Header Móvil */
.mobile-header {
  width: 100%;
  background: rgba(25, 25, 25, 0.8);
  border: 1px solid #444;
  border-radius: 12px;
  padding: 20px 16px;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  box-sizing: border-box;
}

.mobile-error-code {
  text-align: center;
  width: 100%;
}

.error-code-large {
  font-size: 64px;
  font-weight: 900;
  color: #ff4444;
  font-family: 'Courier New', monospace;
  line-height: 1;
  margin-bottom: 8px;
  text-shadow: 0 0 10px rgba(255, 68, 68, 0.3);
}

.error-type {
  font-size: 16px;
  font-weight: 600;
  color: #ff6666;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.mobile-error-icon {
  width: 80px;
  height: 80px;
  color: #ff4444;
  animation: pulseError 2s infinite;
}

@keyframes pulseError {
  0% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.05); }
  100% { opacity: 0.6; transform: scale(1); }
}

/* Contenido de Error */
.error-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.error-message {
  width: 100%;
  background: rgba(25, 25, 25, 0.7);
  border: 1px solid #444;
  border-radius: 12px;
  padding: 20px 16px;
  box-sizing: border-box;
}

.error-title {
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 16px 0;
  text-align: center;
  line-height: 1.3;
}

.error-description {
  font-size: 15px;
  color: #ccc;
  line-height: 1.6;
  margin: 0;
  text-align: center;
}

/* Detalles del Error */
.error-details {
  width: 100%;
  background: rgba(30, 30, 30, 0.7);
  border: 1px solid #444;
  border-radius: 12px;
  padding: 16px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid rgba(68, 68, 68, 0.5);
  min-height: 48px;
  box-sizing: border-box;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 13px;
  color: #aaa;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  flex: 1;
  text-align: left;
}

.detail-value {
  font-size: 15px;
  color: #fff;
  font-family: 'Consolas', monospace;
  font-weight: 600;
  letter-spacing: 0.5px;
  flex: 1;
  text-align: right;
}

/* Estado del Sistema */
.system-status {
  width: 100%;
  background: rgba(25, 25, 25, 0.7);
  border: 1px solid #444;
  border-radius: 12px;
  padding: 16px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
  background: rgba(30, 30, 30, 0.5);
  border: 1px solid #444;
  border-radius: 8px;
  min-height: 56px;
  box-sizing: border-box;
  width: 100%;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-indicator.inactive {
  background: #ff4444;
  box-shadow: 0 0 8px #ff4444;
}

.status-indicator.active {
  background: #00ff00;
  box-shadow: 0 0 8px #00ff00;
  animation: pulse 2s infinite;
}

.status-text {
  font-size: 15px;
  color: #aaa;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.5px;
  flex: 1;
  font-weight: 500;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* Advertencia */
.warning-box {
  width: 100%;
  background: rgba(40, 30, 0, 0.3);
  border: 1px solid #aa8800;
  border-radius: 12px;
  padding: 20px 16px;
  box-sizing: border-box;
}

.warning-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.warning-icon {
  width: 24px;
  height: 24px;
  color: #ffcc00;
  flex-shrink: 0;
}

.warning-title {
  font-size: 16px;
  font-weight: 700;
  color: #ffcc00;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.warning-text {
  font-size: 14px;
  color: #ffdd88;
  line-height: 1.6;
  margin: 0;
}

/* Botones de Acción */
.action-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 18px 20px;
  border: none;
  border-radius: 10px;
  font-family: inherit;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  box-sizing: border-box;
  min-height: 60px;
  text-transform: uppercase;
}

.action-button.primary {
  background: rgba(114, 137, 218, 0.25);
  border: 1px solid rgba(114, 137, 218, 0.5);
  color: #d8d8d8;
}

.action-button.primary:hover {
  background: rgba(114, 137, 218, 0.35);
  border-color: rgba(114, 137, 218, 0.7);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(114, 137, 218, 0.2);
}

.action-button.secondary {
  background: rgba(60, 60, 60, 0.6);
  border: 1px solid #666;
  color: #d8d8d8;
}

.action-button.secondary:hover {
  background: rgba(80, 80, 80, 0.7);
  border-color: #777;
  transform: translateY(-2px);
}

.button-icon {
  width: 22px;
  height: 22px;
  color: currentColor;
  flex-shrink: 0;
}

.button-label {
  text-align: center;
  font-weight: 600;
}

/* Protocolos */
.protocol-container {
  width: 100%;
  background: rgba(20, 20, 20, 0.8);
  border: 1px solid #444;
  border-radius: 12px;
  padding: 20px 16px;
  box-sizing: border-box;
  margin-top: 8px;
}

.protocol-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #333;
}

.protocol-icon {
  width: 24px;
  height: 24px;
  color: #aaa;
  flex-shrink: 0;
}

.protocol-title {
  font-size: 16px;
  color: #ddd;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.protocol-steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.protocol-step {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.step-number {
  width: 28px;
  height: 28px;
  background: rgba(60, 60, 60, 0.8);
  border: 1px solid #555;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: #ddd;
  flex-shrink: 0;
  margin-top: 2px;
}

.step-text {
  font-size: 14px;
  color: #ccc;
  line-height: 1.5;
  flex: 1;
  padding-top: 4px;
}

/* Footer Móvil */
.mobile-footer {
  width: 100%;
  background: rgba(15, 15, 15, 0.9);
  border-top: 1px solid #333;
  padding: 20px 16px;
  box-sizing: border-box;
  margin-top: 24px;
}

.footer-line {
  height: 1px;
  background: linear-gradient(90deg, transparent, #666, transparent);
  margin-bottom: 20px;
  width: 100%;
}

.footer-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.footer-item {
  font-size: 12px;
  color: #777;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  text-align: center;
  line-height: 1.4;
}

.footer-item.classification {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  border-radius: 6px;
  margin-top: 8px;
}

.classification-icon {
  width: 16px;
  height: 16px;
  color: #aaa;
  flex-shrink: 0;
}

.classification-text {
  font-size: 12px;
  color: #aaa;
  font-weight: 600;
}

/* Tablet */
@media (min-width: 640px) {
  .section-content {
    padding: 30px 24px;
    max-width: 600px;
    margin: 0 auto;
  }
  
  .mobile-header {
    padding: 30px 24px;
  }
  
  .error-code-large {
    font-size: 72px;
  }
  
  .error-type {
    font-size: 18px;
  }
  
  .mobile-error-icon {
    width: 90px;
    height: 90px;
  }
  
  .error-title {
    font-size: 22px;
  }
  
  .error-description {
    font-size: 16px;
  }
  
  .detail-label {
    font-size: 14px;
  }
  
  .detail-value {
    font-size: 16px;
  }
  
  .status-text {
    font-size: 16px;
  }
  
  .warning-title {
    font-size: 17px;
  }
  
  .warning-text {
    font-size: 15px;
  }
  
  .action-button {
    padding: 20px 24px;
    font-size: 17px;
    min-height: 64px;
  }
  
  .protocol-title {
    font-size: 17px;
  }
  
  .step-text {
    font-size: 15px;
  }
  
  .footer-item {
    font-size: 13px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .section-content {
    max-width: 800px;
    padding: 40px;
    gap: 32px;
  }
  
  .mobile-header {
    padding: 40px;
    flex-direction: row;
    justify-content: space-between;
  }
  
  .mobile-error-code {
    text-align: left;
    flex: 1;
  }
  
  .error-code-large {
    font-size: 80px;
  }
  
  .error-type {
    font-size: 20px;
  }
  
  .mobile-error-icon {
    width: 100px;
    height: 100px;
  }
  
  .error-message,
  .error-details,
  .system-status,
  .warning-box,
  .protocol-container {
    padding: 24px 20px;
  }
  
  .error-title {
    font-size: 24px;
  }
  
  .error-description {
    font-size: 17px;
  }
  
  .detail-row {
    padding: 16px 0;
  }
  
  .detail-label {
    font-size: 15px;
  }
  
  .detail-value {
    font-size: 17px;
  }
  
  .status-row {
    padding: 16px 20px;
  }
  
  .action-container {
    flex-direction: row;
    gap: 20px;
  }
  
  .action-button {
    flex: 1;
  }
  
  .mobile-footer {
    padding: 30px 40px;
  }
  
  .footer-content {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
  }
  
  .footer-item {
    text-align: left;
    flex: 1;
    min-width: 200px;
  }
  
  .footer-item.classification {
    flex: none;
    width: auto;
  }
}

/* Pantallas grandes */
@media (min-width: 1400px) {
  .section-content {
    max-width: 900px;
  }
  
  .error-code-large {
    font-size: 90px;
  }
  
  .error-type {
    font-size: 22px;
  }
}
</style>