<template>
  <div class="perfil-page">
    <!-- Fondo SCP - más oscuro -->
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
      <div class="dark-overlay"></div>
    </div>

    <!-- Header con padding-top de 2rem -->
    <header class="perfil-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-logo">
            <div class="profile-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="#fc6f03" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <div class="header-title">
              <span class="header-main">AGENT PROFILE</span>
              <span class="header-sub">PERSONNEL RECORDS</span>
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
    </header>

    <!-- Navegación Principal -->
    <nav class="perfil-nav">
      <div class="nav-controls">
        <button 
          class="nav-button" 
          @click="$router.push('/')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
          </div>
          <span class="nav-text">VOLVER AL INICIO</span>
        </button>
        
        <!-- Placeholders [REDACTED] -->
        <button class="nav-button redacted" v-for="n in 3" :key="n" disabled>
          <div class="nav-icon redacted">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <span class="nav-text redacted-text">[REDACTED]</span>
        </button>
      </div>
      
      <div class="nav-info">
        <div class="info-item">
          <span class="info-label">VIEWING:</span>
          <span class="info-value">USER PROFILE</span>
        </div>
        <div class="info-item">
          <span class="info-label">CLEARANCE:</span>
          <span class="info-value">{{ currentUser?.is_authenticated ? 'LEVEL 2' : 'GUEST' }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">SYSTEM:</span>
          <span class="info-value operational">OPERATIONAL</span>
        </div>
      </div>
    </nav>

    <!-- Contenido Principal -->
    <main class="perfil-main">
      <!-- Overlay de carga -->
      <div v-if="loading" class="loading-overlay">
        <div class="loading-spinner large"></div>
        <p class="loading-text">CARGANDO PERFIL...</p>
      </div>
      
      <!-- Contenido del perfil -->
      <div v-else-if="profileUser" class="profile-content">
        <!-- Información del usuario -->
        <div class="user-info-section">
          <div class="user-header">
            <div class="user-avatar">
              <div class="avatar-container">
                <svg viewBox="0 0 24 24" fill="none" stroke="#fc6f03" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </div>
            </div>
            
            <div class="user-details">
              <h1 class="user-name">{{ profileUser.roblox_username }}</h1>
              <div class="user-id">
                <span class="id-label">ROBLOX ID:</span>
                <span class="id-value">#{{ profileUser.roblox_id }}</span>
              </div>
              <div class="user-last-login">
                <span class="login-label">ÚLTIMO ACCESO:</span>
                <span class="login-value">{{ formatDateTime(profileUser.last_login) }}</span>
              </div>
            </div>
            
            <div class="user-stats">
              <div class="stat-item">
                <span class="stat-number">{{ characters.length }}</span>
                <span class="stat-label">AGENTES</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ formatDate(profileUser.first_login) }}</span>
                <span class="stat-label">REGISTRO</span>
              </div>
            </div>
          </div>
          
          <!-- Indicador de permisos -->
          <div class="permissions-indicator" v-if="profileUser.is_staff || profileUser.is_superuser">
            <div class="permissions-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
              </svg>
            </div>
            <div class="permissions-text">
              <span class="permissions-title">STAFF MEMBER</span>
              <span class="permissions-subtitle" v-if="profileUser.is_superuser">Administrador del Sistema</span>
              <span class="permissions-subtitle" v-else-if="profileUser.is_staff">Staff Member</span>
            </div>
          </div>
        </div>

        <!-- Lista de personajes -->
        <div class="characters-section">
          <div class="section-header">
            <h2 class="section-title">
              <span class="title-text">AGENTES REGISTRADOS</span>
              <span class="title-badge">{{ characters.length }}</span>
            </h2>
            <div class="section-subtitle">
              Agentes registrados por {{ profileUser.roblox_username }} en Site-81
            </div>
          </div>

          <!-- Barra de búsqueda -->
          <div class="search-bar">
            <div class="search-container">
              <div class="search-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
              <input
                v-model="searchQuery"
                @input="handleSearch"
                type="text"
                placeholder="Buscar agentes por codename, nombre, facción..."
                class="search-input"
              />
              
              <!-- Botón para limpiar búsqueda -->
              <button 
                v-if="searchQuery" 
                @click="clearSearch"
                class="search-clear"
                title="Limpiar búsqueda"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
              
              <div class="search-info">
                <div class="search-count" v-if="displayedCharacters.length > 0">
                  {{ displayedCharacters.length }} {{ displayedCharacters.length === 1 ? 'agente' : 'agentes' }}
                </div>
              </div>
            </div>
          </div>

          <!-- Grid de personajes -->
          <div class="characters-grid-container">
            <div v-if="charactersLoading" class="loading-state">
              <div class="loading-spinner"></div>
              <p class="loading-text">Cargando agentes...</p>
            </div>
            
            <div v-else-if="displayedCharacters.length > 0" class="enhanced-cards-grid">
              <div 
                v-for="character in displayedCharacters" 
                :key="character.id"
                class="enhanced-character-card"
                @click="viewCharacter(character)"
              >
                <!-- Header de la tarjeta con gradiente -->
                <div class="card-header">
                  <div class="header-gradient"></div>
                  <div class="codename-container">
                    <h3 class="character-codename">{{ character.codename }}</h3>
                    <div class="id-badge">ID: #{{ character.id.toString().padStart(6, '0') }}</div>
                  </div>
                </div>
                
                <!-- Contenido principal -->
                <div class="card-body">
                  <div class="name-row">
                    <div class="name-faction">
                      <h4 class="character-name">{{ character.first_name }} {{ character.last_name }}</h4>
                      <span class="character-faction">{{ character.faction }}</span>
                    </div>
                    <div class="right-info">
                      <div class="info-item">
                        <span class="info-label">EDAD</span>
                        <span class="info-value">{{ calculateAge(character.birth_date) || 'N/A' }} años</span>
                      </div>
                      <div class="info-item">
                        <span class="info-label">REGISTRADO</span>
                        <span class="info-value">{{ formatDateShort(character.created_at) }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div class="owner-id-section">
                    <div class="owner-label">OWNER</div>
                    <div class="owner-name">{{ character.owner_username }} | ID: #{{ character.id.toString().padStart(6, '0') }}</div>
                  </div>
                </div>
                
                <!-- Footer de la tarjeta con acciones -->
                <div class="card-footer">
                  <div class="status-indicator">
                    <div class="status-dot active"></div>
                    <span class="status-text">ACTIVO</span>
                  </div>
                  <div class="view-indicator">
                    <span>VER DETALLES</span>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M5 12h14"></path>
                      <path d="m12 5 7 7-7 7"></path>
                    </svg>
                  </div>
                </div>
                
                <!-- Elemento decorativo de esquina -->
                <div class="corner-decoration"></div>
              </div>
            </div>
            
            <div v-else class="empty-state">
              <div class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#fc6f03" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </div>
              <h3 class="empty-title">
                {{ searchQuery ? 'No se encontraron agentes' : 'Sin agentes registrados' }}
              </h3>
              <p class="empty-text" v-if="searchQuery">
                No hay agentes que coincidan con "{{ searchQuery }}"
              </p>
              <p class="empty-text" v-else>
                Este usuario aún no ha registrado agentes en el sistema.
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Error state -->
      <div v-else-if="error" class="error-state">
        <div class="error-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="#aa2222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
        </div>
        <h3 class="error-title">ERROR DE CARGA</h3>
        <p class="error-text">{{ error }}</p>
        <button class="retry-button" @click="loadProfile">
          <span class="button-text">REINTENTAR</span>
          <div class="button-indicator">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M23 4v6h-6"></path>
              <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
            </svg>
          </div>
        </button>
      </div>

      <!-- Modal de detalles del personaje -->
      <div v-if="selectedCharacter" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content character-modal" @click.stop>
          <div class="modal-header">
            <button class="modal-close" @click="closeModal">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
            <h3 class="modal-title">{{ selectedCharacter.codename }}</h3>
            <div class="modal-subtitle">DETALLES DEL AGENTE</div>
          </div>
          
          <div class="modal-body">
            <div class="detail-section">
              <h4 class="section-title">INFORMACIÓN DE IDENTIDAD</h4>
              <div class="detail-grid">
                <div class="detail-item">
                  <span class="detail-label">Nombre:</span>
                  <span class="detail-value">{{ selectedCharacter.first_name }} {{ selectedCharacter.last_name }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">País:</span>
                  <span class="detail-value">{{ selectedCharacter.country }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Edad:</span>
                  <span class="detail-value">{{ calculateAge(selectedCharacter.birth_date) || 'N/A' }} años</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Facción:</span>
                  <span class="detail-value faction">{{ selectedCharacter.faction }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Codename:</span>
                  <span class="detail-value highlight">{{ selectedCharacter.codename }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Registrado:</span>
                  <span class="detail-value">{{ formatDateDDMMYYYY(selectedCharacter.created_at) }}</span>
                </div>
              </div>
            </div>
            
            <div class="detail-section" v-if="selectedCharacter.lore">
              <h4 class="section-title">LORE Y BIOGRAFÍA</h4>
              <div class="lore-container">
                <div class="lore-content" v-html="renderMarkdown(selectedCharacter.lore)"></div>
              </div>
            </div>
            
            <div class="detail-section" v-if="hasMorphData(selectedCharacter)">
              <h4 class="section-title">DATOS MORPH</h4>
              <div class="morph-preview">
                <div class="morph-command-container">
                  <div class="command-preview">
                    <code class="command-text">{{ selectedCharacter.morph_command }}</code>
                  </div>
                  <button class="copy-button small" @click="copyMorphCommand(selectedCharacter)">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                    <span>COPIAR</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="perfil-footer">
      <div class="footer-info">
        <span class="info-label">SYSTEM:</span>
        <span class="info-value">PROFILE-VIEW v1.0</span>
      </div>
      <div class="footer-info">
        <span class="info-label">PROFILE ID:</span>
        <span class="info-value">{{ profileUser?.roblox_id ? `#${profileUser.roblox_id}` : 'N/A' }}</span>
      </div>
      <div class="footer-info">
        <span class="info-label">ACCESS LEVEL:</span>
        <span class="info-value">{{ currentUser?.is_authenticated ? 'AUTHORIZED' : 'GUEST' }}</span>
      </div>
    </footer>

    <!-- Sistema de notificaciones -->
    <div class="scp-notifications">
      <transition-group name="notification-slide">
        <div 
          v-for="notification in notifications" 
          :key="notification.id"
          class="scp-notification"
          :class="`type-${notification.type}`"
          @click="removeNotification(notification.id)"
        >
          <div class="notification-header">
            <div class="notification-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path v-if="notification.type === 'success'" d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <path v-if="notification.type === 'success'" d="M22 4 12 14.01l-3-3"></path>
                <path v-if="notification.type === 'error'" d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line v-if="notification.type === 'error'" x1="12" y1="9" x2="12" y2="13"></line>
                <line v-if="notification.type === 'error'" x1="12" y1="17" x2="12.01" y2="17"></line>
                <circle v-if="notification.type === 'info'" cx="12" cy="12" r="10"></circle>
                <line v-if="notification.type === 'info'" x1="12" y1="16" x2="12" y2="12"></line>
                <line v-if="notification.type === 'info'" x1="12" y1="8" x2="12.01" y2="8"></line>
              </svg>
            </div>
            <div class="notification-title">
              {{ notification.title }}
            </div>
            <button class="notification-close">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="notification-content">
            {{ notification.message }}
          </div>
          <div class="notification-progress" :style="{ 
            animationDuration: `${notification.duration}ms`,
            animationPlayState: notification.paused ? 'paused' : 'running' 
          }"></div>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { debounce } from 'lodash'

const route = useRoute()
const router = useRouter()

// Estado principal
const loading = ref(true)
const charactersLoading = ref(false)
const profileUser = ref(null)
const characters = ref([])
const selectedCharacter = ref(null)
const searchQuery = ref('')
const currentUser = ref(null)
const currentTime = ref('')
const error = ref(null)

// Notificaciones
const notifications = ref([])
let notificationId = 0

// Variable para almacenar la posición del scroll
let scrollPosition = 0

// Métodos para controlar el scroll del modal
const disableBodyScroll = () => {
  // Guardar posición actual del scroll
  scrollPosition = window.scrollY
  
  // Agregar clase al body y estilos
  document.body.style.overflow = 'hidden'
  document.body.style.position = 'fixed'
  document.body.style.width = '100%'
  document.body.style.top = `-${scrollPosition}px`
  document.body.style.left = '0'
  document.body.style.right = '0'
}

const enableBodyScroll = () => {
  // Remover estilos del body
  document.body.style.overflow = ''
  document.body.style.position = ''
  document.body.style.width = ''
  document.body.style.top = ''
  document.body.style.left = ''
  document.body.style.right = ''
  
  // Restaurar posición de scroll
  window.scrollTo(0, scrollPosition)
  scrollPosition = 0
}

// Computed
const displayedCharacters = computed(() => {
  if (!searchQuery.value.trim()) {
    return characters.value
  }
  
  const query = searchQuery.value.toLowerCase()
  return characters.value.filter(character => {
    return (
      character.codename?.toLowerCase().includes(query) ||
      character.first_name?.toLowerCase().includes(query) ||
      character.last_name?.toLowerCase().includes(query) ||
      character.faction?.toLowerCase().includes(query)
    )
  })
})

// Método para cerrar el modal
const closeModal = () => {
  selectedCharacter.value = null
}

// Método para ver detalles del personaje
const viewCharacter = (character) => {
  selectedCharacter.value = character
}

// Watcher para selectedCharacter
watch(selectedCharacter, (newVal) => {
  if (newVal) {
    disableBodyScroll()
  } else {
    enableBodyScroll()
  }
})

// Manejar tecla ESC para cerrar modal
const handleKeydown = (e) => {
  if (e.key === 'Escape' && selectedCharacter.value) {
    closeModal()
  }
}

// Métodos de utilidad
const showNotification = (title, message, type = 'info', duration = 5000) => {
  const id = ++notificationId
  notifications.value.push({
    id,
    title,
    message,
    type,
    duration,
    paused: false
  })
  
  setTimeout(() => {
    removeNotification(id)
  }, duration)
}

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
  }
}

const loadProfile = async () => {
  const robloxId = route.params.id
  if (!robloxId) {
    error.value = 'ID de usuario no proporcionado'
    loading.value = false
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    // Cargar información del usuario usando la ruta correcta
    const userResponse = await fetch(`/api/users/${robloxId}/`)
    if (!userResponse.ok) {
      throw new Error('Usuario no encontrado')
    }
    
    const userData = await userResponse.json()
    profileUser.value = userData
    
    // Cargar personajes del usuario
    await loadUserCharacters(robloxId)
    
  } catch (err) {
    console.error('Error loading profile:', err)
    error.value = err.message || 'Error al cargar el perfil'
    showNotification('ERROR', 'No se pudo cargar el perfil', 'error', 4000)
  } finally {
    loading.value = false
  }
}

const loadUserCharacters = async (robloxId) => {
  charactersLoading.value = true
  try {
    const response = await fetch(`/api/users/${robloxId}/characters/`)
    if (!response.ok) {
      throw new Error('Error al cargar personajes')
    }
    
    const data = await response.json()
    characters.value = data.results || data || []
    
    // Asegúrate de que cada personaje tenga owner_username
    characters.value.forEach(character => {
      if (!character.owner_username && profileUser.value) {
        character.owner_username = profileUser.value.roblox_username
      }
    })
    
  } catch (err) {
    console.error('Error loading characters:', err)
    showNotification(
      'ERROR',
      'No se pudieron cargar los agentes',
      'error',
      4000
    )
  } finally {
    charactersLoading.value = false
  }
}

const fetchCurrentUser = async () => {
  try {
    const response = await fetch('/api/auth/user/')
    if (response.ok) {
      const data = await response.json()
      currentUser.value = data
    }
  } catch (error) {
    console.error('Error fetching current user:', error)
  }
}

const handleSearch = debounce(() => {
  // Búsqueda ya está implementada en computed
}, 300)

const clearSearch = () => {
  searchQuery.value = ''
}

const calculateAge = (birthDate) => {
  if (!birthDate) return null
  
  const today = new Date()
  const birth = new Date(birthDate)
  let age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--
  }
  
  return age
}

const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  
  const day = date.getDate().toString().padStart(2, '0')
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const year = date.getFullYear()
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  
  return `${day}/${month}/${year} ${hours}:${minutes}`
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  const day = date.getDate().toString().padStart(2, '0')
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const year = date.getFullYear()
  return `${day}/${month}/${year}`
}

const formatDateShort = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const day = date.getDate().toString().padStart(2, '0')
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const year = date.getFullYear().toString().slice(-2)
  return `${day}/${month}/${year}`
}

const formatDateDDMMYYYY = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const day = date.getDate().toString().padStart(2, '0')
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const year = date.getFullYear()
  return `${day}/${month}/${year}`
}

const renderMarkdown = (text) => {
  if (!text) return ''
  
  let html = text
    .replace(/^##### (.*$)/gm, '<h5>$1</h5>')
    .replace(/^#### (.*$)/gm, '<h4>$1</h4>')
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
  
  html = html
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
  
  html = html.replace(/^- (.*$)/gm, '<li>$1</li>')
  html = html.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
  
  html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
  
  html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
  
  html = html.replace(/`(.*?)`/g, '<code>$1</code>')
  
  html = html.replace(/^> (.*$)/gm, '<blockquote>$1</blockquote>')
  
  const parts = html.split(/(<pre>[\s\S]*?<\/pre>)/)
  html = parts.map(part => {
    if (part.startsWith('<pre>') && part.endsWith('</pre>')) {
      return part
    }
    return part.replace(/\n/g, '<br>')
  }).join('')
  
  return html
}

const hasMorphData = (character) => {
  return (
    character.morph ||
    character.hat ||
    character.nvg_color ||
    character.shirt ||
    character.pants ||
    character.ntag ||
    character.rtag
  )
}

const copyMorphCommand = async (character) => {
  if (character?.morph_command) {
    try {
      await navigator.clipboard.writeText(character.morph_command)
      showNotification(
        'COMANDO COPIADO',
        'El comando morph ha sido copiado al portapapeles',
        'success',
        3000
      )
    } catch (error) {
      console.error('Error copying to clipboard:', error)
      showNotification(
        'ERROR',
        'No se pudo copiar el comando',
        'error',
        4000
      )
    }
  }
}

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

// Watchers
watch(() => route.params.id, (newId) => {
  if (newId) {
    loadProfile()
  }
})

// Lifecycle
onMounted(() => {
  updateTime()
  const timeInterval = setInterval(updateTime, 1000)
  
  // Agregar event listener para tecla ESC
  window.addEventListener('keydown', handleKeydown)
  
  fetchCurrentUser()
  loadProfile()
  
  onUnmounted(() => {
    clearInterval(timeInterval)
    window.removeEventListener('keydown', handleKeydown)
    enableBodyScroll() // Asegurar que el scroll se restaure al desmontar
  })
})
</script>

<style scoped>
/* Estilos principales - Página completa */
.perfil-page {
  position: relative;
  min-height: 100vh;
  color: #d8d8d8;
  background: #0a0a0a;
  font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.5;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
}

/* Fondo SCP - Más oscuro */
.site-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: 
    linear-gradient(135deg, #080808 0%, #0a0a0a 25%, #080808 50%, #0a0a0a 75%, #080808 100%),
    radial-gradient(circle at 20% 30%, rgba(20, 20, 20, 0.8) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(30, 30, 30, 0.6) 0%, transparent 50%);
  z-index: 0;
}

.dark-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  z-index: 1;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(50, 50, 50, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(50, 50, 50, 0.08) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: gridMove 20s linear infinite;
  z-index: 1;
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 10% 20%, rgba(80, 80, 80, 0.04) 1px, transparent 1px),
    radial-gradient(circle at 90% 80%, rgba(80, 80, 80, 0.04) 1px, transparent 1px);
  background-size: 30px 30px;
  z-index: 1;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(60, 60, 60, 0.8) 10%, 
    rgba(100, 100, 100, 0.9) 50%, 
    rgba(60, 60, 60, 0.8) 90%, 
    transparent 100%);
  animation: scan 6s linear infinite;
  z-index: 1;
  opacity: 0.2;
}

@keyframes scan {
  0% { top: 0%; }
  100% { top: 100%; }
}

@keyframes gridMove {
  0% { transform: translateY(0); }
  100% { transform: translateY(40px); }
}

/* Header con 2rem de padding top */
.perfil-header {
  position: relative;
  z-index: 2;
  background: rgba(10, 10, 10, 0.98);
  border-bottom: 1px solid #222;
  padding: 2rem 2rem 1rem 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.7);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1600px;
  margin: 0 auto;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.header-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.profile-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(252, 111, 3, 0.08);
  border: 1px solid rgba(252, 111, 3, 0.2);
  border-radius: 2px;
}

.profile-icon svg {
  width: 28px;
  height: 28px;
}

.header-title {
  display: flex;
  flex-direction: column;
}

.header-main {
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: #fff;
  text-transform: uppercase;
  line-height: 1.2;
}

.header-sub {
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  color: #777;
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
  color: #777;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.3px;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

/* Navegación */
.perfil-nav {
  position: relative;
  z-index: 2;
  background: rgba(15, 15, 15, 0.95);
  border-bottom: 1px solid #222;
  padding: 1rem 2rem;
  backdrop-filter: blur(10px);
}

.nav-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.nav-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  padding: 0.8rem 1.5rem;
  background: rgba(25, 25, 25, 0.9);
  border: 1px solid #333;
  color: #999;
  font-family: inherit;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  flex-shrink: 0;
}

.nav-button:hover:not(:disabled) {
  background: rgba(35, 35, 35, 0.95);
  border-color: #444;
  color: #ccc;
}

.nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-button.redacted {
  border-color: #aa2222;
  background: rgba(170, 34, 34, 0.08);
}

.nav-icon {
  width: 18px;
  height: 18px;
  color: currentColor;
}

.nav-icon.redacted {
  color: #aa2222;
}

.nav-text {
  font-weight: 600;
  font-family: 'Consolas', monospace;
}

.nav-text.redacted-text {
  color: #aa2222;
}

.nav-info {
  display: flex;
  gap: 2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-label {
  font-size: 11px;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.info-value {
  font-size: 12px;
  color: #ccc;
  font-weight: 600;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.info-value.operational {
  color: #4CAF50;
}

/* Contenido Principal */
.perfil-main {
  position: relative;
  z-index: 2;
  flex: 1;
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

/* Overlay de carga */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
}

.loading-spinner.large {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(252, 111, 3, 0.3);
  border-top: 4px solid #fc6f03;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  font-size: 1.2rem;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
  margin: 0;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Contenido del perfil */
.profile-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Información del usuario */
.user-info-section {
  background: rgba(15, 15, 15, 0.9);
  border: 1px solid #222;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.user-header {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 2rem;
  align-items: center;
  margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
  .user-header {
    grid-template-columns: 1fr;
    text-align: center;
  }
}

.user-avatar {
  position: relative;
}

.avatar-container {
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(252, 111, 3, 0.1);
  border: 2px solid rgba(252, 111, 3, 0.3);
  border-radius: 2px;
  position: relative;
  overflow: hidden;
}

.avatar-container svg {
  width: 50px;
  height: 50px;
  color: #fc6f03;
}

.avatar-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(to bottom, rgba(252, 111, 3, 0.2), transparent);
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 2.2rem;
  font-weight: 800;
  color: #fff;
  margin: 0 0 0.5rem 0;
  letter-spacing: 0.5px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
  font-family: 'Consolas', 'Courier New', monospace;
}

.user-id {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 0.5rem;
}

.id-label {
  font-size: 0.9rem;
  color: #777;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
}

.id-value {
  font-size: 1.1rem;
  color: #fc6f03;
  font-weight: 700;
  font-family: 'Consolas', monospace;
  background: rgba(252, 111, 3, 0.1);
  padding: 0.3rem 0.8rem;
  border: 1px solid rgba(252, 111, 3, 0.3);
}

.user-last-login {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.login-label {
  font-size: 0.9rem;
  color: #777;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
}

.login-value {
  font-size: 1rem;
  color: #aaa;
  font-weight: 500;
  font-family: 'Consolas', monospace;
}

.user-stats {
  display: flex;
  gap: 2rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
}

.stat-number {
  font-size: 2rem;
  font-weight: 800;
  color: #fc6f03;
  margin-bottom: 0.3rem;
  font-family: 'Consolas', monospace;
  text-shadow: 0 0 10px rgba(252, 111, 3, 0.3);
}

.stat-label {
  font-size: 0.8rem;
  color: #777;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
}

/* Indicador de permisos */
.permissions-indicator {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(90deg, rgba(252, 111, 3, 0.1) 0%, transparent 100%);
  border: 1px solid rgba(252, 111, 3, 0.2);
  border-left: 4px solid #fc6f03;
}

.permissions-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(252, 111, 3, 0.2);
  border: 1px solid rgba(252, 111, 3, 0.3);
  border-radius: 2px;
  flex-shrink: 0;
}

.permissions-icon svg {
  width: 24px;
  height: 24px;
  color: #fc6f03;
}

.permissions-text {
  flex: 1;
}

.permissions-title {
  display: block;
  font-size: 1.1rem;
  font-weight: 700;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.2rem;
  font-family: 'Consolas', monospace;
}

.permissions-subtitle {
  display: block;
  font-size: 0.9rem;
  color: #aaa;
  letter-spacing: 0.3px;
}

/* Sección de personajes */
.characters-section {
  background: rgba(15, 15, 15, 0.9);
  border: 1px solid #222;
  padding: 2rem;
}

.section-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.8rem;
  font-weight: 700;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 0.5rem 0;
  font-family: 'Consolas', 'Courier New', monospace;
}

.title-badge {
  font-size: 1rem;
  background: rgba(252, 111, 3, 0.2);
  color: #fc6f03;
  padding: 0.3rem 0.8rem;
  border: 1px solid rgba(252, 111, 3, 0.3);
  border-radius: 2px;
  font-family: 'Consolas', monospace;
}

.section-subtitle {
  font-size: 1rem;
  color: #aaa;
  letter-spacing: 0.3px;
}

/* Barra de búsqueda */
.search-bar {
  margin-bottom: 2rem;
}

.search-container {
  position: relative;
  background: rgba(25, 25, 25, 0.6);
  border: 1px solid #333;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.search-container:focus-within {
  border-color: #fc6f03;
  box-shadow: 0 0 0 2px rgba(252, 111, 3, 0.1);
}

.search-icon {
  width: 20px;
  height: 20px;
  color: #888;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 1rem;
  font-family: inherit;
  outline: none;
}

.search-input::placeholder {
  color: #666;
}

.search-clear {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.search-clear:hover {
  color: #fc6f03;
}

.search-clear svg {
  width: 16px;
  height: 16px;
}

.search-info {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.search-count {
  font-size: 0.9rem;
  color: #888;
  font-family: 'Consolas', monospace;
  white-space: nowrap;
  background: rgba(255, 255, 255, 0.05);
  padding: 0.2rem 0.5rem;
  border-radius: 2px;
}

/* Contenedor del grid de personajes */
.characters-grid-container {
  min-height: 200px;
}

.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(252, 111, 3, 0.3);
  border-top: 3px solid #fc6f03;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.loading-text {
  font-size: 1rem;
  color: #aaa;
  margin: 0;
}

.empty-icon {
  width: 60px;
  height: 60px;
  color: #fc6f03;
  opacity: 0.8;
  margin-bottom: 1.5rem;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1rem 0;
}

.empty-text {
  font-size: 1rem;
  color: #aaa;
  margin: 0 0 2rem 0;
  max-width: 400px;
}

/* Grid de tarjetas mejoradas - 3 por línea */
.enhanced-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.enhanced-character-card {
  background: linear-gradient(145deg, rgba(20, 20, 20, 0.95) 0%, rgba(30, 30, 30, 0.95) 100%);
  border: 1px solid #333;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
  height: 300px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.enhanced-character-card:hover {
  transform: translateY(-6px);
  border-color: #fc6f03;
  box-shadow: 0 12px 30px rgba(252, 111, 3, 0.25);
}

.enhanced-character-card:hover .card-header .header-gradient {
  opacity: 1;
  transform: scale(1.05);
}

.enhanced-character-card:hover .view-indicator {
  color: #fc6f03;
}

.enhanced-character-card:hover .view-indicator svg {
  transform: translateX(4px);
}

/* Header con gradiente */
.card-header {
  position: relative;
  padding: 1.2rem 1.2rem 0.8rem 1.2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  min-height: 70px;
  flex-shrink: 0;
}

.header-gradient {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: linear-gradient(90deg, rgba(252, 111, 3, 0.1) 0%, rgba(252, 111, 3, 0.05) 50%, transparent 100%);
  opacity: 0.7;
  transition: all 0.4s ease;
  z-index: 1;
}

.codename-container {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.character-codename {
  font-size: min(1.4rem, max(0.9rem, 3.5vw));
  font-weight: 800;
  color: #fff;
  margin: 0;
  font-family: 'Consolas', 'Courier New', monospace;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  line-height: 1.2;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  max-height: 2.8em;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  text-overflow: ellipsis;
}

.id-badge {
  font-size: 0.7rem;
  color: #888;
  background: rgba(255, 255, 255, 0.05);
  padding: 0.2rem 0.5rem;
  border-radius: 2px;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.3px;
}

/* Cuerpo de la tarjeta */
.card-body {
  flex: 1;
  padding: 0.8rem 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  position: relative;
  z-index: 2;
  min-height: 0;
  overflow: hidden;
}

.name-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.8rem;
  gap: 0.5rem;
  min-height: 70px;
}

.name-faction {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.character-name {
  font-size: min(1.1rem, max(0.8rem, 2.5vw));
  font-weight: 600;
  color: #ddd;
  margin: 0 0 0.3rem 0;
  line-height: 1.2;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  max-height: 2.4em;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  text-overflow: ellipsis;
}

.character-faction {
  font-size: min(0.8rem, max(0.65rem, 1.8vw));
  color: #fc6f03;
  background: rgba(252, 111, 3, 0.1);
  padding: 0.2rem 0.5rem;
  border: 1px solid rgba(252, 111, 3, 0.3);
  display: inline-block;
  margin-top: 0.3rem;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.3px;
  max-width: 100%;
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.right-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  margin-left: 0.5rem;
  flex-shrink: 0;
  min-width: 110px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.info-label {
  font-size: 0.65rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
  font-weight: 600;
}

.info-value {
  font-size: min(0.9rem, max(0.75rem, 2vw));
  color: #ddd;
  font-weight: 500;
  text-align: right;
  line-height: 1.2;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.owner-id-section {
  margin-top: auto;
  padding-top: 0.8rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.owner-label {
  font-size: 0.65rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
  margin-bottom: 0.2rem;
}

.owner-name {
  font-size: min(0.85rem, max(0.75rem, 1.8vw));
  color: #aaa;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  word-wrap: break-word;
  overflow-wrap: break-word;
  max-height: 1.8em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Footer de la tarjeta */
.card-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(0, 0, 0, 0.2);
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4CAF50;
  box-shadow: 0 0 8px #4CAF50;
  animation: pulse 2s infinite;
}

.status-text {
  font-size: 0.75rem;
  color: #4CAF50;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
  font-weight: 700;
}

.view-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
  font-weight: 600;
  transition: all 0.3s ease;
}

.view-indicator svg {
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

/* Decoración de esquina */
.corner-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 20px;
  height: 20px;
  border-top: 2px solid #fc6f03;
  border-right: 2px solid #fc6f03;
  border-top-right-radius: 4px;
  opacity: 0.5;
}

/* Error state */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.error-icon {
  width: 60px;
  height: 60px;
  color: #aa2222;
  margin-bottom: 1.5rem;
}

.error-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #aa2222;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1rem 0;
}

.error-text {
  font-size: 1rem;
  color: #aaa;
  margin: 0 0 2rem 0;
  max-width: 400px;
}

.retry-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  padding: 1rem 2rem;
  background: rgba(252, 111, 3, 0.1);
  border: 1px solid rgba(252, 111, 3, 0.3);
  color: #fc6f03;
  font-size: 1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  background: rgba(252, 111, 3, 0.2);
  border-color: rgba(252, 111, 3, 0.5);
}

.button-text {
  font-family: 'Consolas', monospace;
}

.button-indicator {
  width: 16px;
  height: 16px;
  color: currentColor;
}

/* Modal de detalles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  animation: fadeIn 0.3s ease;
  overflow-y: auto;
}

body:has(.modal-overlay) {
  overflow: hidden !important;
  position: fixed !important;
  width: 100% !important;
  height: 100% !important;
}

.character-modal {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  max-width: 800px;
  width: 100%;
  max-height: calc(90vh - 4rem);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  padding: 1.5rem 2rem;
  background: rgba(25, 25, 25, 0.9);
  border-bottom: 1px solid #333;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex-shrink: 0;
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 10;
}

.modal-close:hover {
  color: #fff;
}

.modal-close svg {
  width: 20px;
  height: 20px;
}

.modal-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0;
  font-family: 'Consolas', 'Courier New', monospace;
}

.modal-subtitle {
  font-size: 0.9rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Para navegadores que no soportan :has() */
body.modal-open {
  overflow: hidden !important;
  position: fixed !important;
  width: 100% !important;
  height: 100% !important;
}


.detail-section {
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  padding: 1.5rem;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1rem 0;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid rgba(252, 111, 3, 0.3);
  font-family: 'Consolas', 'Courier New', monospace;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-label {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.detail-value {
  font-size: 1rem;
  color: #ddd;
  font-weight: 500;
}

.detail-value.highlight {
  color: #fc6f03;
  font-weight: 700;
}

.detail-value.faction {
  color: #fc6f03;
  background: rgba(252, 111, 3, 0.1);
  padding: 0.25rem 0.5rem;
  border: 1px solid rgba(252, 111, 3, 0.3);
  display: inline-block;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.3px;
}

.lore-container {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  padding: 1.5rem;
  margin-top: 1rem;
}

.lore-content {
  color: #ddd;
  line-height: 1.6;
}

.lore-content h1,
.lore-content h2,
.lore-content h3,
.lore-content h4,
.lore-content h5,
.lore-content h6 {
  color: #fc6f03;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}

.lore-content p {
  margin: 1em 0;
}

.lore-content ul,
.lore-content ol {
  margin: 1em 0;
  padding-left: 2em;
}

.lore-content li {
  margin: 0.5em 0;
}

.morph-preview {
  margin-top: 1rem;
}

.morph-command-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.command-preview {
  background: rgba(20, 20, 20, 0.8);
  border: 1px solid #444;
  padding: 1rem;
  overflow-x: auto;
}

.command-text {
  font-family: 'Consolas', monospace;
  font-size: 0.9rem;
  color: #4CAF50;
  white-space: nowrap;
}

/* Botón de copiar más pequeño */
.copy-button.small {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.4rem 0.8rem;
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  color: #4CAF50;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: flex-start;
  min-width: auto;
  height: 32px;
}

.copy-button.small:hover {
  background: rgba(76, 175, 80, 0.2);
  border-color: rgba(76, 175, 80, 0.5);
}

.copy-button.small svg {
  width: 14px;
  height: 14px;
}

.copy-button.small span {
  font-size: 0.7rem;
}

/* Footer */
.perfil-footer {
  position: relative;
  z-index: 2;
  background: rgba(10, 10, 10, 0.98);
  border-top: 1px solid #222;
  padding: 1rem 2rem;
  backdrop-filter: blur(10px);
  margin-top: auto;
}

.footer-info {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

/* Sistema de notificaciones SCP */
.scp-notifications {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 400px;
  pointer-events: none;
}

.scp-notification {
  background: linear-gradient(135deg, 
    rgba(20, 20, 20, 0.95) 0%, 
    rgba(30, 30, 30, 0.95) 100%);
  border: 1px solid #333;
  border-left: 4px solid #fc6f03;
  padding: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  position: relative;
  overflow: hidden;
  pointer-events: auto;
  cursor: pointer;
  transition: all 0.3s ease;
  animation: slideInRight 0.3s ease;
}

.scp-notification:hover {
  transform: translateX(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6);
}

.scp-notification.type-success {
  border-left-color: #4CAF50;
}

.scp-notification.type-error {
  border-left-color: #ff3333;
}

.scp-notification.type-info {
  border-left-color: #2196F3;
}

.notification-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 0.8rem;
}

.notification-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.scp-notification.type-success .notification-icon {
  color: #4CAF50;
}

.scp-notification.type-error .notification-icon {
  color: #ff3333;
}

.scp-notification.type-info .notification-icon {
  color: #2196F3;
}

.notification-title {
  flex: 1;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #fff;
  font-family: 'Consolas', monospace;
}

.notification-close {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  padding: 0.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s ease;
}

.notification-close:hover {
  color: #fff;
}

.notification-close svg {
  width: 16px;
  height: 16px;
}

.notification-content {
  font-size: 0.9rem;
  color: #ccc;
  line-height: 1.4;
  margin-bottom: 0.5rem;
}

.notification-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    #fc6f03 50%, 
    transparent 100%);
  animation: progressBar linear forwards;
}

.scp-notification.type-success .notification-progress {
  background: linear-gradient(90deg, 
    transparent 0%, 
    #4CAF50 50%, 
    transparent 100%);
}

.scp-notification.type-error .notification-progress {
  background: linear-gradient(90deg, 
    transparent 0%, 
    #ff3333 50%, 
    transparent 100%);
}

.scp-notification.type-info .notification-progress {
  background: linear-gradient(90deg, 
    transparent 0%, 
    #2196F3 50%, 
    transparent 100%);
}

/* Animaciones */
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes progressBar {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(100%);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.notification-slide-enter-active,
.notification-slide-leave-active {
  transition: all 0.3s ease;
}

.notification-slide-enter-from,
.notification-slide-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

/* Responsive */
@media (max-width: 1200px) {
  .enhanced-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .perfil-header,
  .perfil-nav,
  .perfil-footer {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .header-right {
    align-items: center;
  }
  
  .nav-controls {
    justify-content: center;
  }
  
  .nav-info {
    justify-content: center;
  }
  
  .perfil-main {
    padding: 1rem;
  }
  
  .user-info-section,
  .characters-section {
    padding: 1.5rem;
  }
  
  .user-header {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 1.5rem;
  }
  
  .user-stats {
    justify-content: center;
  }
  
  .stat-item {
    min-width: 100px;
  }
  
  .enhanced-cards-grid {
    grid-template-columns: 1fr;
  }
  
  .enhanced-character-card {
    height: 260px;
  }
  
  .modal-overlay {
    padding: 0.5rem;
  }
  
  .character-modal {
    max-height: 95vh;
    max-width: 95vw;
  }
  
  .modal-header,
  .modal-body {
    padding: 1rem;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .enhanced-cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1025px) {
  .enhanced-cards-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* ESTILOS GLOBALES - Necesarios para controlar el scroll del body */
body.modal-open {
  overflow: hidden !important;
  position: fixed !important;
  width: 100% !important;
  height: 100% !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
}

/* Para navegadores móviles iOS */
@supports (-webkit-touch-callout: none) {
  body.modal-open {
    position: fixed !important;
    width: 100% !important;
    height: 100% !important;
    overflow: hidden !important;
  }
}

/* Prevenir scroll táctil cuando el modal está abierto */
body.modal-open .perfil-page {
  overflow: hidden;
  height: 100vh;
}

</style>