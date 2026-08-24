<template>
  <div class="dashboard-page">
    <!-- Fondo SCP -->
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
    </div>

    <!-- Header Dashboard -->
    <div class="dashboard-header">
      <div class="header-left">
        <div class="header-logo">
          <div class="header-title">
            <span class="header-main">DASHBOARD CONTROL</span>
            <span class="header-sub">SECURED FACILITY INTERFACE</span>
          </div>
        </div>
      </div>
      
      <div class="header-right">
        <div class="session-status">
          <div class="session-indicator active"></div>
          <span class="session-text">SESSION ACTIVE</span>
        </div>
        <div class="current-time">
          {{ currentTime }}
        </div>
      </div>
    </div>

    

    <!-- Contenido Principal - Tarjetas -->
    <main class="cards-container">
      <div v-if="!currentUser?.is_authenticated" class="auth-modal-overlay">
        <Login_Required 
          :redirect-path="'/dashboard/personnel/'"
          :user="currentUser"
        />        
      </div>
      <div v-else class="authenticated-content">
      <div class="cards-header">
        <h1 class="cards-title">CONTROL PANEL</h1>
        <div class="cards-subtitle">AUTHORIZED FUNCTIONS & TOOLS</div>
      </div>

      <!-- Grid de Tarjetas -->
      <div class="cards-grid">
        <!-- Tarjeta 1: Manejo de Personal (Activa) -->
        <div class="dashboard-card" :class="{ 'active': activeCard === 1 }" @click="activateCard(1)">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <div class="card-title">MANEJO DE PERSONAL</div>
            <div class="card-status" v-if="activeCard === 1">
              <span class="status-active">ACTIVE</span>
            </div>
          </div>
          <div class="card-content">
            <p class="card-description">Gestiona y visualiza los expedientes del personal autorizado, sus niveles de acceso y asignaciones.</p>
            <div class="card-meta">
              <span class="meta-label">ACCESS:</span>
              <span class="meta-value authorized">GRANTED</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button class="action-button" @click.stop="goToPersonnel">
                <span class="button-text">ACCESS SYSTEM</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 2: Apeloraciones -->
        <div class="dashboard-card" :class="{ 'active': activeCard === 2 }" @click="activateCard(2)">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <div class="card-title">APELACIONES</div>
            <div class="card-status" v-if="activeCard === 2">
              <span class="status-active">ACTIVE</span>
            </div>
          </div>
          <div class="card-content">
            <p class="card-description">Administra y revisa las apelaciones de sanciones disciplinarias.</p>
            <div class="card-meta">
              <span class="meta-label">ACCESS:</span>
              <span class="meta-value authorized">GRANTED</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button class="action-button" @click.stop="goToApeals">
                <span class="button-text">ACCESS SYSTEM</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 3: Facciones Públicas -->
        <div class="dashboard-card" :class="{ 'active': activeCard === 3 }" @click="activateCard(3)">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="card-title">FACCIONES</div>
            <div class="card-status" v-if="activeCard === 3">
              <span class="status-active">ACTIVE</span>
            </div>
          </div>
          <div class="card-content">
            <p class="card-description">Explora las facciones públicas disponibles y envía tu solicitud de ingreso.</p>
            <div class="card-meta">
              <span class="meta-label">ACCESS:</span>
              <span class="meta-value authorized">GRANTED</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button class="action-button" @click.stop="goToFactions">
                <span class="button-text">ACCESS SYSTEM</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 4: MOD DASHBOARD (Solo para moderadores) -->
        <div class="dashboard-card" 
            :class="{ 
              'active': activeCard === 4,
              'restricted-card': !hasModDashboardAccess()
            }" 
            @click="handleModDashboardClick && activateCard(4)">
          
          <div class="card-header" :class="{ 'restricted-header': !hasModDashboardAccess() }">
            <div class="card-icon" :class="{ 'restricted-icon': !hasModDashboardAccess() }">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                <template v-if="!hasModDashboardAccess()">
                  <line x1="4.93" y1="19.07" x2="19.07" y2="4.93"></line>
                </template>
              </svg>
            </div>
            <div class="card-title" :class="{ 'restricted-title': !hasModDashboardAccess() }">
              MOD DASHBOARD
            </div>
            <div class="card-status">
              <span v-if="hasModDashboardAccess()" class="status-active">ACTIVE</span>
              <span v-if="!hasModDashboardAccess()" class="status-red">RESTRICTED</span>
            </div>
          </div>
          
          <div class="card-content">
            <p class="card-description" :class="{ 'restricted-description': !hasModDashboardAccess() }">
              <template v-if="hasModDashboardAccess()">
                Access the moderation control panel for advanced administrative functions.
              </template>
              <template v-if="!hasModDashboardAccess()">
                This function requires moderator-level permissions and security clearance.
              </template>
            </p>
            <div class="card-meta">
              <span class="meta-label">ACCESS:</span>
              <span class="meta-value" :class="hasModDashboardAccess() ? 'authorized' : 'restricted-access'">
                <template v-if="hasModDashboardAccess()">MODERATORS ONLY</template>
                <template v-if="!hasModDashboardAccess()">RESTRICTED</template>
              </span>
            </div>
          </div>
          
          <div class="card-footer">
            <div class="card-action">
              <button 
                class="action-button" 
                :class="{ 
                  'disabled': !hasModDashboardAccess(),
                  'restricted-button': !hasModDashboardAccess()
                }" 
                @click.stop="goToModDashboard"
                :disabled="!hasModDashboardAccess()"
              >
                <span class="button-text">
                  <template v-if="hasModDashboardAccess()">ACCESS PANEL</template>
                  <template v-if="!hasModDashboardAccess()">ACCESS DENIED</template>
                </span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <template v-if="hasModDashboardAccess()">
                      <polyline points="9 18 15 12 9 6"></polyline>
                    </template>
                    <template v-if="!hasModDashboardAccess()">
                      <line x1="18" y1="6" x2="6" y2="18"></line>
                      <line x1="6" y1="6" x2="18" y2="18"></line>
                    </template>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>
        <!-- Tarjeta 5: SCP Database -->
        <div class="dashboard-card" @click="goToScps">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <circle cx="12" cy="12" r="4"></circle>
                <line x1="12" y1="2" x2="12" y2="8"></line>
                <line x1="12" y1="16" x2="12" y2="22"></line>
                <line x1="2" y1="12" x2="8" y2="12"></line>
                <line x1="16" y1="12" x2="22" y2="12"></line>
              </svg>
            </div>
            <div class="card-title">SCP DATABASE</div>
          </div>
          <div class="card-content">
            <p class="card-description">Consulta los archivos SCP del sitio. El contenido visible depende de tu tarjeta de acceso.</p>
            <div class="card-meta">
              <span class="meta-label">ACCESS:</span>
              <span class="meta-value authorized">BY CLEARANCE</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button class="action-button" @click.stop="goToScps">
                <span class="button-text">ACCESS SYSTEM</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 6: Documentación -->
        <div class="dashboard-card" @click="goToDocuments">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
              </svg>
            </div>
            <div class="card-title">DOCUMENTACIÓN</div>
          </div>
          <div class="card-content">
            <p class="card-description">Procedimientos, memos, reglamentos y briefings internos filtrados por nivel de acceso.</p>
            <div class="card-meta">
              <span class="meta-label">ACCESS:</span>
              <span class="meta-value authorized">BY CLEARANCE</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button class="action-button" @click.stop="goToDocuments">
                <span class="button-text">ACCESS SYSTEM</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 7: Anuncios -->
        <div class="dashboard-card" @click="goToAnnouncements">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 11l18-5v12L3 14v-3z"></path>
                <path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"></path>
              </svg>
            </div>
            <div class="card-title">ANUNCIOS</div>
          </div>
          <div class="card-content">
            <p class="card-description">Feed de comunicados In-RP, Off-RP y eventos automáticos del sistema.</p>
            <div class="card-meta">
              <span class="meta-label">ACCESS:</span>
              <span class="meta-value authorized">GRANTED</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button class="action-button" @click.stop="goToAnnouncements">
                <span class="button-text">ACCESS SYSTEM</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 8: Terminal de Consulta -->
        <div class="dashboard-card" @click="goToTerminal">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="4 17 10 11 4 5"></polyline>
                <line x1="12" y1="19" x2="20" y2="19"></line>
              </svg>
            </div>
            <div class="card-title">TERMINAL DE CONSULTA</div>
          </div>
          <div class="card-content">
            <p class="card-description">Asistente institucional RAISA. Consulta SCPs, documentos y facciones según tu acreditación.</p>
            <div class="card-meta">
              <span class="meta-label">ACCESS:</span>
              <span class="meta-value authorized">GRANTED</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button class="action-button" @click.stop="goToTerminal">
                <span class="button-text">ACCESS SYSTEM</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 9: Sugerencias de Lore -->
        <div class="dashboard-card" @click="goToLore">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 20h9"></path>
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
              </svg>
            </div>
            <div class="card-title">SUGERENCIAS DE LORE</div>
          </div>
          <div class="card-content">
            <p class="card-description">Programa exclusivo para Boosters: propone ideas de lore al equipo de roleplay.</p>
            <div class="card-meta">
              <span class="meta-label">ACCESS:</span>
              <span class="meta-value authorized">BOOSTERS</span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button class="action-button" @click.stop="goToLore">
                <span class="button-text">ACCESS SYSTEM</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

      </div>

      <!-- Información del Sistema -->
      <div class="system-info">
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">SYSTEM STATUS:</span>
            <span class="info-value operational">OPERATIONAL</span>
          </div>
          <div class="info-item">
            <span class="info-label">USER:</span>
            <span class="info-value">{{ currentUser?.roblox_username || 'GUEST' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">CLEARANCE LEVEL:</span>
            <span class="info-value">3</span>
          </div>
          <div class="info-item">
            <span class="info-label">ACCESS TYPE:</span>
            <span class="info-value">{{ currentUser?.is_authenticated ? 'AUTHORIZED' : 'GUEST' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">SYSTEM VERSION:</span>
            <span class="info-value">TWILIGHT-DASH v1.0.4</span>
          </div>
          <div class="info-item">
            <span class="info-label">LAST UPDATE:</span>
            <span class="info-value">{{ currentTime }}</span>
          </div>
        </div>
      </div>
      </div>

    </main>

    <!-- Modal de Acceso Denegado -->
    <div v-if="showDeniedModal" class="access-denied-modal">
      <div class="modal-overlay" @click="closeModal"></div>
      <div class="modal-content">
        <div class="modal-header">
          <div class="modal-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#aa2222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
          </div>
          <h3 class="modal-title">ACCESS DENIED</h3>
        </div>
        <div class="modal-body">
          <p class="modal-text">You do not have sufficient clearance to access this function.</p>
          <div class="clearance-info">
            <div class="clearance-item">
              <span class="clearance-label">CURRENT CLEARANCE:</span>
              <span class="clearance-value">LEVEL 3</span>
            </div>
            <div class="clearance-item">
              <span class="clearance-label">REQUIRED CLEARANCE:</span>
              <span class="clearance-value redacted">LEVEL 4+</span>
            </div>
            <div class="clearance-item">
              <span class="clearance-label">STATUS:</span>
              <span class="clearance-value denied">ACCESS DENIED</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-button" @click="closeModal">
            <span class="button-text">ACKNOWLEDGE</span>
          </button>
        </div>
      </div>
    </div>
  </div>
  <No_Mobile />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import No_Mobile from '@/components/No_Mobile.vue'
import Login_Required from '@/components/Login_Required.vue'

const router = useRouter()
const activeCard = ref(1)
const currentUser = ref(null)
const currentTime = ref('')
const showDeniedModal = ref(false)
const userPermissions = ref([])

const activateCard = (cardNumber) => {
  activeCard.value = cardNumber
}

const showAccessDenied = (cardNumber) => {
  activeCard.value = cardNumber
  showDeniedModal.value = true
}

const closeModal = () => {
  showDeniedModal.value = false
  activeCard.value = 1
}

const goToPersonnel = () => {
  router.push('/dashboard/personnel')
}

const goToApeals = () => {
  router.push("/dashboard/appeals")
}

const goToFactions = () => {
  router.push('/dashboard/factions')
}

const goToScps = () => {
  router.push('/dashboard/scps')
}

const goToDocuments = () => {
  router.push('/dashboard/documents')
}

const goToAnnouncements = () => {
  router.push('/dashboard/announcements')
}

const goToTerminal = () => {
  router.push('/dashboard/terminal')
}

const goToLore = () => {
  router.push('/dashboard/lore-suggestions')
}

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('en-US', {
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
      currentUser.value = data
    }
  } catch (error) {
    console.error('Error fetching user:', error)
  }
}

// En tu script setup
import { computed } from 'vue'

// Método para verificar acceso al Mod Dashboard
const hasModDashboardAccess = () => {
  // Verifica si el usuario está autenticado
  if (!currentUser.value || !currentUser.value.is_authenticated) return false
  
  // Superusuarios siempre tienen acceso
  if (currentUser.value.is_superuser) return true
  
  // Obtener permisos del usuario actual
  return userPermissions.value.includes('access_moderation_dashboard')
}

// Manejar clic en la tarjeta
const handleModDashboardClick = () => {
  if (hasModDashboardAccess()) {
    activateCard(4)
  } else {
    showAccessDenied(4)
  }
}

const fetchUserPermissions = async () => {
  try {
    const response = await fetch('/api/auth/user/permissions/')
    if (response.ok) {
      const data = await response.json()
      userPermissions.value = data.permissions || []
    }
  } catch (error) {
    console.error('Error fetching permissions:', error)
  }
}

// Navegar al Mod Dashboard
const goToModDashboard = () => {
  if (hasModDashboardAccess()) {
    router.push('/moderation')
  } else {
    showAccessDenied(4)
  }
}

onMounted(() => {
  updateTime()
  const timeInterval = setInterval(updateTime, 1000)
  fetchCurrentUser()
  fetchUserPermissions()
  
  return () => {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
/* Estilos principales */
.dashboard-page {
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

/* Fondo SCP */
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

/* Header Dashboard */
.dashboard-header {
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

.header-logo-img {
  height: 40px;
  width: 40px;
  object-fit: contain;
  filter: grayscale(0.3) brightness(1.2);
}

.header-title {
  display: flex;
  flex-direction: column;
}

.header-main {
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: #fff;
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
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
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

.session-indicator.active {
  background: #4CAF50;
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

/* Contenedor de Tarjetas */
.cards-container {
  position: relative;
  z-index: 2;
}

.cards-header {
  text-align: center;
  margin-bottom: 40px;
}

.cards-title {
  font-size: 2rem;
  font-weight: 900;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0 0 8px 0;
  text-shadow: 0 0 10px rgba(252, 111, 3, 0.3);
}

.cards-subtitle {
  font-size: 0.9rem;
  color: #aaa;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

/* Grid de Tarjetas */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.dashboard-card {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  border-radius: 0px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  backdrop-filter: blur(5px);
}

.dashboard-card:hover {
  transform: translateY(-2px);
  border-color: #444;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.dashboard-card.active {
  border-color: #fc6f03;
  background: rgba(30, 20, 15, 0.95);
  box-shadow: 0 0 20px rgba(252, 111, 3, 0.2);
}

.dashboard-card.redacted {
  cursor: not-allowed;
  opacity: 0.8;
}

.dashboard-card.redacted:hover {
  transform: none;
  border-color: #aa2222;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px;
  background: rgba(30, 30, 30, 0.8);
  border-bottom: 1px solid #333;
}

.card-header.redacted {
  background: rgba(40, 20, 20, 0.8);
  border-bottom-color: #aa2222;
}

.card-icon {
  width: 24px;
  height: 24px;
  color: #fc6f03;
  flex-shrink: 0;
}

.card-icon.redacted {
  color: #aa2222;
}

.card-title {
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex: 1;
}

.card-title.redacted-text {
  color: #aa2222;
  font-family: 'Consolas', monospace;
}

.card-status {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.3px;
}

.status-active {
  color: #4CAF50;
  text-transform: uppercase;
}

.status-redacted {
  color: #aa2222;
  text-transform: uppercase;
}

.card-content {
  padding: 20px;
}

.card-description {
  font-size: 0.9rem;
  color: #aaa;
  line-height: 1.6;
  margin: 0 0 16px 0;
}

.card-description.redacted-text {
  color: #884444;
  font-style: italic;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.meta-label {
  font-size: 0.7rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.meta-value {
  font-size: 0.8rem;
  font-weight: 600;
  font-family: 'Consolas', monospace;
}

.meta-value.authorized {
  color: #4CAF50;
}

.meta-value.redacted {
  color: #aa2222;
}

.card-footer {
  padding: 0 20px 20px 20px;
}

.card-action {
  display: flex;
  justify-content: flex-end;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(252, 111, 3, 0.1);
  border: 1px solid rgba(252, 111, 3, 0.3);
  border-radius: 0px;
  color: #fc6f03;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button:hover {
  background: rgba(252, 111, 3, 0.2);
  border-color: rgba(252, 111, 3, 0.5);
  transform: translateY(-1px);
}

.button-icon {
  width: 14px;
  height: 14px;
  color: currentColor;
}

.clearance-warning {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  border-radius: 0px;
}

.warning-icon {
  width: 16px;
  height: 16px;
  color: #aa2222;
}

.warning-text {
  font-size: 0.7rem;
  color: #aa2222;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

/* Información del Sistema */
.system-info {
  background: rgba(15, 15, 15, 0.95);
  border: 1px solid #333;
  border-radius: 0px;
  padding: 20px;
  backdrop-filter: blur(5px);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
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

.info-value.operational {
  color: #4CAF50;
}

/* Modal de Acceso Denegado */
.access-denied-modal {
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
  border: 1px solid #aa2222;
  border-radius: 0px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 10px 40px rgba(170, 34, 34, 0.3);
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
  width: 50px;
  height: 50px;
  color: #aa2222;
  margin: 0 auto 15px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 900;
  color: #aa2222;
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
  text-align: center;
  line-height: 1.6;
  margin: 0 0 30px 0;
}

.clearance-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
  background: rgba(40, 20, 20, 0.6);
  border: 1px solid rgba(170, 34, 34, 0.3);
  border-radius: 0px;
}

.clearance-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.clearance-item:last-child {
  border-bottom: none;
}

.clearance-label {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.clearance-value {
  font-size: 0.9rem;
  font-weight: 700;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.5px;
}

.clearance-value.redacted {
  color: #aa2222;
}

.clearance-value.denied {
  color: #ff4444;
}

.modal-footer {
  padding: 20px 30px 30px 30px;
  text-align: center;
  border-top: 1px solid #333;
}

.modal-button {
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

.modal-button:hover {
  background: rgba(170, 34, 34, 0.2);
  border-color: rgba(170, 34, 34, 0.5);
  transform: translateY(-1px);
}

.button-text {
  font-family: 'Consolas', monospace;
}

/* Responsive */
@media (max-width: 768px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-header {
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
  
  .cards-title {
    font-size: 1.5rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1025px) {
  .cards-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Estilos para tarjeta restringida */
.dashboard-card.restricted {
  cursor: not-allowed;
  opacity: 0.8;
  border-color: #aa2222;
  background: rgba(40, 20, 20, 0.7);
}

.dashboard-card.restricted:hover {
  transform: none;
  box-shadow: 0 0 15px rgba(170, 34, 34, 0.2);
}

.dashboard-card.accessible {
  border-color: #333;
  background: rgba(20, 20, 20, 0.95);
}

.dashboard-card.accessible:hover {
  border-color: #444;
  transform: translateY(-2px);
}

/* Header restringido */
.card-header.restricted {
  background: rgba(40, 20, 20, 0.8);
  border-bottom-color: #aa2222;
}

.card-icon.restricted {
  color: #aa2222;
}

.restricted-text {
  color: #aa2222 !important;
}

/* Estados */
.status-denied {
  color: #aa2222;
  text-transform: uppercase;
  font-weight: 600;
  font-size: 0.7rem;
}

/* Botón restringido */
.restricted-btn {
  background: rgba(170, 34, 34, 0.1) !important;
  border-color: rgba(170, 34, 34, 0.3) !important;
  color: #aa2222 !important;
  cursor: not-allowed !important;
}

.restricted-btn:hover {
  background: rgba(170, 34, 34, 0.1) !important;
  border-color: rgba(170, 34, 34, 0.3) !important;
  transform: none !important;
}

/* Texto en rojo para MOD DASHBOARD sin acceso */
.card-title.restricted-text {
  color: #aa2222;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.5px;
}

/* Meta value denegado */
.meta-value.denied {
  color: #aa2222;
  font-weight: 700;
}

/* Efecto de línea diagonal en icono cuando está restringido */
.card-icon.restricted svg line {
  animation: denyPulse 2s infinite;
}

@keyframes denyPulse {
  0%, 100% { stroke-opacity: 0.6; }
  50% { stroke-opacity: 1; }
}

/* Efecto de parpadeo para tarjeta restringida */
.dashboard-card.restricted {
  animation: restrictedGlow 3s infinite;
}

@keyframes restrictedGlow {
  0%, 100% { box-shadow: 0 0 5px rgba(170, 34, 34, 0.2); }
  50% { box-shadow: 0 0 15px rgba(170, 34, 34, 0.4); }
}
</style>