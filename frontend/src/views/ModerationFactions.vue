<template>
  <div class="moderacion-page">
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

    <!-- Fondo SCP -->
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
    </div>

    <!-- Header -->
    <div class="moderacion-header">
      <div class="header-left">
        <div class="header-logo">
          <div class="header-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#aa2222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <div class="header-title">
            <span class="header-main">ADMINISTRACIÓN DE FACCIONES</span>
            <span class="header-sub">GESTIÓN DE ORGANIZACIONES</span>
          </div>
        </div>
      </div>
      
      <div class="header-right">
        <div class="session-status">
          <div class="session-indicator active"></div>
          <span class="session-text">ADMIN ACTIVE</span>
        </div>
        <div class="current-time">
          {{ currentTime }}
        </div>
        <button class="back-button" @click="$router.push('/moderation')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5"></path>
            <path d="M12 19l-7-7 7-7"></path>
          </svg>
          VOLVER
        </button>
      </div>
    </div>

    <!-- Contenido Principal -->
    <main class="moderacion-main">
      <div class="tabs-container">
        <button class="tab-btn" :class="{ active: activeTab === 'factions' }" @click="activeTab = 'factions'">
          FACCIONES
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'types' }" @click="activeTab = 'types'">
          TIPOS DE FACCIÓN
        </button>
      </div>

      <div class="tab-content">
        <!-- Factions Tab -->
        <div v-if="activeTab === 'factions'" class="tab-panel">
          <div class="content-header">
            <h2>LISTADO DE FACCIONES</h2>
            <button class="create-btn" @click="showCreateModal = true">
              + CREAR FACCIÓN
            </button>
          </div>

          <div v-if="loading" class="loading-state">
            <div class="loader"></div>
          </div>

          <div v-else class="factions-table">
            <div class="table-header">
              <span class="col-name">NOMBRE</span>
              <span class="col-type">TIPO</span>
              <span class="col-status">ESTADO</span>
              <span class="col-members">MIEMBROS</span>
              <span class="col-actions">ACCIONES</span>
            </div>
            <div v-for="faction in factions" :key="faction.id" class="table-row">
              <span class="col-name">{{ faction.display_name || faction.name }}</span>
              <span class="col-type">{{ faction.faction_type }}</span>
              <span class="col-status">
                <span class="status-badge" :class="faction.is_public ? 'public' : 'private'">
                  {{ faction.is_public ? 'PÚBLICA' : 'PRIVADA' }}
                </span>
              </span>
              <span class="col-members">{{ faction.member_count || 0 }}</span>
              <span class="col-actions">
                <button class="action-btn edit" @click="editFaction(faction)">EDITAR</button>
              </span>
            </div>
          </div>
        </div>

        <!-- Faction Types Tab -->
        <div v-if="activeTab === 'types'" class="tab-panel">
          <div class="content-header">
            <h2>TIPOS DE FACCIÓN</h2>
            <button class="create-btn" @click="showCreateTypeModal = true">
              + CREAR TIPO
            </button>
          </div>

          <div class="faction-types-grid">
            <div v-for="type in factionTypes" :key="type.key" class="faction-type-card" :style="{ borderColor: type.color }">
              <div class="type-color" :style="{ backgroundColor: type.color }"></div>
              <div class="type-info">
                <span class="type-name">{{ type.display_name }}</span>
                <span class="type-key">{{ type.key }}</span>
                <span v-if="type.is_default" class="type-badge">Por defecto</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </main>

    <!-- Modal Crear/Editar Facción -->
    <div v-if="showCreateModal || editingFaction" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ editingFaction ? 'EDITAR FACCIÓN' : 'CREAR FACCIÓN' }}</h2>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Nombre interno:</label>
            <input v-model="factionForm.name" placeholder="Nombre interno" />
          </div>
          <div class="form-group">
            <label>Nombre a mostrar:</label>
            <input v-model="factionForm.display_name" placeholder="Nombre visible" />
          </div>
          <div class="form-group">
            <label>Tipo:</label>
            <select v-model="factionForm.faction_type">
              <option v-for="type in factionTypes" :key="type.key" :value="type.key">
                {{ type.display_name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Descripción:</label>
            <textarea v-model="factionForm.description" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>Color:</label>
            <input type="color" v-model="factionForm.color" />
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="factionForm.is_public" />
              Facción pública
            </label>
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="factionForm.allow_applications" />
              Permitir aplicaciones
            </label>
          </div>
          <div class="form-group">
            <label>Líder de la facción:</label>
            <div class="leader-search">
              <input 
                v-model="leaderSearch" 
                @input="searchLeaders"
                placeholder="Buscar usuario..."
                class="search-input"
              />
              <div v-if="leaderResults.length > 0" class="search-results">
                <div 
                  v-for="user in leaderResults" 
                  :key="user.id" 
                  class="search-result"
                  @click="selectLeader(user)"
                >
                  {{ user.roblox_username }} ({{ user.roblox_id }})
                </div>
              </div>
              <div v-if="selectedLeader" class="selected-leader">
                <span>{{ selectedLeader.roblox_username }}</span>
                <button type="button" class="clear-btn" @click="clearLeader">&times;</button>
              </div>
            </div>
          </div>

          <!-- Rank Brackets Card Assignment -->
          <div v-if="editingFaction" class="bracket-section">
            <h3 class="section-title">TARJETAS POR BRACKET</h3>
            <div class="bracket-cards">
              <div class="bracket-card">
                <span class="bracket-label low">LOW RANK (1-25)</span>
                <select v-model="editingBracketCards.low">
                  <option value="">-- Sin tarjeta --</option>
                  <option v-for="card in accessCards" :key="card.id" :value="String(card.id)">
                    {{ card.name }}
                  </option>
                </select>
              </div>
              <div class="bracket-card">
                <span class="bracket-label mid">MID RANK (26-50)</span>
                <select v-model="editingBracketCards.mid">
                  <option value="">-- Sin tarjeta --</option>
                  <option v-for="card in accessCards" :key="card.id" :value="String(card.id)">
                    {{ card.name }}
                  </option>
                </select>
              </div>
              <div class="bracket-card">
                <span class="bracket-label high">HIGH RANK (51-75)</span>
                <select v-model="editingBracketCards.high">
                  <option value="">-- Sin tarjeta --</option>
                  <option v-for="card in accessCards" :key="card.id" :value="String(card.id)">
                    {{ card.name }}
                  </option>
                </select>
              </div>
              <div class="bracket-card">
                <span class="bracket-label command">HIGH COMMAND (76-100)</span>
                <select v-model="editingBracketCards.command">
                  <option value="">-- Sin tarjeta --</option>
                  <option v-for="card in accessCards" :key="card.id" :value="String(card.id)">
                    {{ card.name }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Divisions Card Assignment -->
          <div v-if="editingFaction" class="divisions-section">
            <div class="divisions-header">
              <h3 class="section-title">DIVISIONES</h3>
              <button type="button" class="add-division-btn" @click="addNewDivision">+ Añadir</button>
            </div>
            <div v-if="editingDivisionsCards.length > 0" class="divisions-list">
              <div v-for="(div, index) in editingDivisionsCards" :key="div.id || index" class="division-item">
                <div class="division-info">
                  <input v-model="div.name" placeholder="Nombre de división" class="division-name-input" />
                  <select v-model="div.access_card_id" class="division-card-select">
                    <option value="">-- Sin tarjeta --</option>
                    <option v-for="card in accessCards" :key="card.id" :value="String(card.id)">
                      {{ card.name }}
                    </option>
                  </select>
                </div>
                <button type="button" class="remove-division-btn" @click="removeDivision(index)">&times;</button>
              </div>
            </div>
            <div v-else class="no-divisions">
              <p>No hay divisiones. Añade una para asignar tarjeta.</p>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="closeModal">CANCELAR</button>
          <button class="save-btn" @click="saveFaction">
            {{ editingFaction ? 'GUARDAR' : 'CREAR' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Crear Tipo de Facción -->
    <div v-if="showCreateTypeModal" class="modal-overlay" @click="showCreateTypeModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>CREAR TIPO DE FACCIÓN</h2>
          <button class="close-btn" @click="showCreateTypeModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Key (identificador único):</label>
            <input v-model="newFactionType.key" placeholder="Ej: mtf, research, security" />
          </div>
          <div class="form-group">
            <label>Nombre a mostrar:</label>
            <input v-model="newFactionType.display_name" placeholder="Ej: Mobile Task Force" />
          </div>
          <div class="form-group">
            <label>Color:</label>
            <input type="color" v-model="newFactionType.color" />
          </div>
          <div class="form-group">
            <label>Descripción:</label>
            <textarea v-model="newFactionType.description" rows="2"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showCreateTypeModal = false">CANCELAR</button>
          <button class="save-btn" @click="createFactionType">CREAR</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const loading = ref(true)
const factions = ref([])
const accessCards = ref([])
const showCreateModal = ref(false)
const editingFaction = ref(null)
const currentTime = ref('')
const leaderSearch = ref('')
const leaderResults = ref([])
const selectedLeader = ref(null)
const editingRank = ref(null)
const showRankModal = ref(false)
const editingDivision = ref(null)
const showDivisionModal = ref(false)
const activeTab = ref('factions')
const factionTypes = ref([])
const showCreateTypeModal = ref(false)
const editingBracketCards = ref({ low: '', mid: '', high: '', command: '' })
const editingDivisionsCards = ref([])

const notifications = ref([])
let notificationId = 0

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
    const index = notifications.value.findIndex(n => n.id === id)
    if (index !== -1) {
      notifications.value.splice(index, 1)
    }
  }, duration)
}

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
  }
}

const newFactionType = ref({
  key: '',
  display_name: '',
  color: '#aa2222',
  description: ''
})

const factionForm = ref({
  name: '',
  display_name: '',
  faction_type: 'MTF',
  description: '',
  color: '#aa2222',
  is_public: true,
  allow_applications: true,
  leader_id: ''
})

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('en-US', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
  }).replace(/(\d+)\/(\d+)\/(\d+),/, '$3-$1-$2')
}

const fetchFactions = async () => {
  try {
    const response = await fetch('/api/factions/all/')
    if (response.ok) {
      const data = await response.json()
      factions.value = data.factions || []
    }
  } catch (err) {
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}

const fetchAccessCards = async () => {
  try {
    const response = await fetch('/api/cards/')
    if (response.ok) {
      const data = await response.json()
      accessCards.value = data.cards || []
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const searchLeaders = () => {
  if (leaderSearch.value.length < 2) {
    leaderResults.value = []
    return
  }
  fetch(`/api/moderation/users/search/${leaderSearch.value}/`)
    .then(res => res.json())
    .then(data => {
      leaderResults.value = data.results || []
    })
    .catch(err => console.error('Error:', err))
}

const selectLeader = (user) => {
  selectedLeader.value = user
  factionForm.value.leader_id = user.id
  leaderSearch.value = ''
  leaderResults.value = []
}

const clearLeader = () => {
  selectedLeader.value = null
  factionForm.value.leader_id = ''
}

const editFaction = async (faction) => {
  editingFaction.value = { ...faction, divisions: [] }
  editingBracketCards.value = { low: '', mid: '', high: '', command: '' }
  factionForm.value = {
    name: faction.name,
    display_name: faction.display_name || faction.name,
    faction_type: faction.faction_type,
    description: faction.description || '',
    color: faction.color || '#aa2222',
    is_public: faction.is_public,
    allow_applications: faction.allow_applications,
    leader_id: faction.leader_id || ''
  }
  // Set current leader if exists
  if (faction.leaders && faction.leaders.length > 0) {
    selectedLeader.value = faction.leaders[0]
    factionForm.value.leader_id = faction.leaders[0].id
  } else {
    selectedLeader.value = null
  }
  leaderSearch.value = ''
  leaderResults.value = []
  // Fetch ranks and divisions for this faction
  try {
    const [ranksRes, divisionsRes] = await Promise.all([
      fetch(`/api/factions/${faction.id}/ranks/`),
      fetch(`/api/faction-dashboard/${faction.id}/divisions/`)
    ])
    
    if (ranksRes.ok) {
      const ranksData = await ranksRes.json()
      // Assign cards to brackets based on rank levels
      const ranks = ranksData.ranks || []
      const bracketCards = { low: '', mid: '', high: '', command: '' }
      ranks.forEach(rank => {
        if (rank.level <= 25 && rank.access_card) bracketCards.low = String(rank.access_card.id)
        else if (rank.level <= 50 && rank.access_card) bracketCards.mid = String(rank.access_card.id)
        else if (rank.level <= 75 && rank.access_card) bracketCards.high = String(rank.access_card.id)
        else if (rank.level > 75 && rank.access_card) bracketCards.command = String(rank.access_card.id)
      })
      editingBracketCards.value = bracketCards
    }
    if (divisionsRes.ok) {
      const divisionsData = await divisionsRes.json()
      // Add access_card_id to divisions if not present
      const divisions = divisionsData.divisions || []
      const divisionsCards = []
      divisions.forEach(div => {
        const cardId = div.access_card_id ? String(div.access_card_id) : ''
        divisionsCards.push({ id: div.id, name: div.name, access_card_id: cardId })
      })
      editingDivisionsCards.value = divisionsCards
      editingFaction.value.divisions = divisions
    }
  } catch (err) {
    console.error('Error loading faction data:', err)
  }
}

const addNewDivision = () => {
  editingDivisionsCards.value.push({ name: '', access_card_id: '', is_new: true })
}

const removeDivision = (index) => {
  editingDivisionsCards.value.splice(index, 1)
}

const closeModal = () => {
  showCreateModal.value = false
  editingFaction.value = null
  leaderSearch.value = ''
  leaderResults.value = []
  selectedLeader.value = null
  factionForm.value = {
    name: '', display_name: '', faction_type: 'MTF', description: '',
    color: '#aa2222', is_public: true, allow_applications: true, leader_id: ''
  }
}

const saveFaction = async () => {
  try {
    const url = editingFaction.value 
      ? `/api/factions/${editingFaction.value.id}/update/`
      : '/api/factions/create/'
    const method = 'POST'
    
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(factionForm.value)
    })
    
    if (response.ok) {
      await fetchFactions()
      closeModal()
      showNotification('ÉXITO', editingFaction.value ? 'Facción actualizada correctamente' : 'Facción creada correctamente', 'success', 4000)
    } else {
      const data = await response.json()
      showNotification('ERROR', data.error || 'Error al guardar', 'error', 5000)
    }
  } catch (err) {
    showNotification('ERROR', 'Error al guardar', 'error', 5000)
  }
}

const fetchFactionTypes = async () => {
  try {
    const response = await fetch('/api/factions/types/')
    if (response.ok) {
      const data = await response.json()
      factionTypes.value = data.types || []
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const createFactionType = async () => {
  try {
    const response = await fetch('/api/factions/types/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newFactionType.value)
    })
    if (response.ok) {
      await fetchFactionTypes()
      showCreateTypeModal.value = false
      newFactionType.value = { key: '', display_name: '', color: '#aa2222', description: '' }
      showNotification('ÉXITO', 'Tipo de facción creado correctamente', 'success', 4000)
    } else {
      const data = await response.json()
      showNotification('ERROR', data.error || 'Error al crear tipo', 'error', 5000)
    }
  } catch (err) {
    console.error('Error:', err)
    showNotification('ERROR', 'Error al crear tipo', 'error', 5000)
  }
}

onMounted(() => {
  updateTime()
  setInterval(updateTime, 1000)
  fetchFactions()
  fetchAccessCards()
  fetchFactionTypes()
})
</script>

<style scoped>
.moderacion-page {
  min-height: 100vh;
  color: #d8d8d8;
  background: #0a0a0a;
  padding-bottom: 40px;
}

.site-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #0a0a0a 0%, #121212 50%, #0a0a0a 100%);
  z-index: 0;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: linear-gradient(rgba(60, 60, 60, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(60, 60, 60, 0.1) 1px, transparent 1px);
  background-size: 40px 40px;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(80, 80, 80, 0.8), rgba(120, 120, 120, 0.9) 50%, rgba(80, 80, 80, 0.8) 90%, transparent 100%);
  animation: scan 6s linear infinite;
}

@keyframes scan {
  0% { top: 0%; }
  100% { top: 100%; }
}

.moderacion-header {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: rgba(15, 15, 15, 0.95);
  border-bottom: 1px solid #333;
  backdrop-filter: blur(10px);
}

.header-left {
  display: flex;
  align-items: center;
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
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
}

.header-icon svg {
  width: 24px;
  height: 24px;
}

.header-title {
  display: flex;
  flex-direction: column;
}

.header-main {
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: 1px;
}

.header-sub {
  font-size: 0.7rem;
  color: #888;
  letter-spacing: 0.5px;
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
  background: #4CAF50;
  box-shadow: 0 0 6px #4CAF50;
}

.session-text {
  font-size: 0.7rem;
  color: #4CAF50;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.current-time {
  font-size: 0.7rem;
  color: #666;
  font-family: 'Consolas', monospace;
}

.moderacion-main {
  position: relative;
  z-index: 2;
  padding: 2rem;
}

.tabs-container {
  display: flex;
  gap: 5px;
  margin-bottom: 20px;
  margin-top: 40px;
  border-bottom: 1px solid #333;
}

.tab-btn {
  padding: 12px 24px;
  background: transparent;
  border: none;
  color: #888;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tab-btn.active {
  color: #aa2222;
  border-bottom-color: #aa2222;
}

.tab-content {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  padding: 20px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.content-header h2 {
  font-size: 1rem;
  color: #fff;
  margin: 0;
}

.faction-types-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.faction-type-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(30, 30, 30, 0.5);
  border: 1px solid #333;
  border-left-width: 4px;
  border-radius: 4px;
}

.type-color {
  width: 24px;
  height: 24px;
  border-radius: 4px;
}

.type-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.type-name {
  font-weight: 600;
  color: #fff;
  font-size: 0.9rem;
}

.type-key {
  font-size: 0.7rem;
  color: #666;
}

.type-badge {
  font-size: 0.65rem;
  color: #4a9;
  background: rgba(68, 170, 153, 0.1);
  padding: 2px 6px;
  border-radius: 2px;
  width: fit-content;
}

.create-btn {
  padding: 10px 20px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  cursor: pointer;
  font-size: 0.8rem;
}

.loading-state {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.loader {
  width: 40px;
  height: 40px;
  border: 3px solid #333;
  border-top-color: #aa2222;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.factions-table {
  display: flex;
  flex-direction: column;
}

.table-header, .table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
  gap: 10px;
  padding: 12px;
  align-items: center;
}

.table-header {
  background: rgba(30, 30, 30, 0.8);
  border-bottom: 1px solid #444;
  font-size: 0.75rem;
  color: #888;
  text-transform: uppercase;
}

.table-row {
  border-bottom: 1px solid #333;
}

.table-row:hover {
  background: rgba(40, 40, 40, 0.5);
}

.col-name {
  font-weight: 600;
  color: #fff;
}

.col-type {
  color: #aaa;
  font-size: 0.85rem;
}

.status-badge {
  padding: 3px 8px;
  font-size: 0.7rem;
  font-weight: 600;
}

.status-badge.public {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  color: #4CAF50;
}

.status-badge.private {
  background: rgba(255, 152, 0, 0.1);
  border: 1px solid rgba(255, 152, 0, 0.3);
  color: #ff9800;
}

.col-members {
  color: #aaa;
}

.action-btn {
  padding: 5px 12px;
  background: transparent;
  border: 1px solid #444;
  color: #aaa;
  cursor: pointer;
  font-size: 0.7rem;
}

.action-btn:hover {
  background: rgba(170, 34, 34, 0.1);
  border-color: #aa2222;
  color: #aa2222;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.access-card {
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
}

.card-header {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  background: rgba(40, 40, 40, 0.8);
  border-bottom: 1px solid #444;
}

.card-level {
  font-size: 1.2rem;
  font-weight: 700;
  color: #aa2222;
}

.card-type {
  font-size: 0.75rem;
  color: #888;
  text-transform: uppercase;
}

.card-body {
  padding: 15px;
}

.card-body h3 {
  margin: 0 0 10px 0;
  color: #fff;
}

.card-body p {
  font-size: 0.85rem;
  color: #aaa;
  margin: 0 0 15px 0;
}

.card-perms {
  display: flex;
  gap: 5px;
  margin-bottom: 10px;
}

.perm {
  padding: 2px 6px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  font-size: 0.7rem;
  font-weight: 600;
}

.classified-badge {
  display: inline-block;
  padding: 3px 8px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  font-size: 0.7rem;
  font-weight: 600;
}

.card-footer {
  padding: 15px;
  border-top: 1px solid #444;
}

.edit-btn {
  width: 100%;
  padding: 8px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  cursor: pointer;
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
}

.modal-content {
  background: rgba(20, 20, 20, 0.98);
  border: 1px solid #333;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #333;
}

.modal-header h2 {
  margin: 0;
  color: #aa2222;
  font-size: 1.1rem;
}

.close-btn {
  background: none;
  border: none;
  color: #888;
  font-size: 2rem;
  cursor: pointer;
}

.modal-body {
  padding: 24px;
  background: linear-gradient(180deg, rgba(20, 20, 20, 0.95) 0%, rgba(15, 15, 15, 0.98) 100%);
}

.modal-body .form-group {
  margin-bottom: 20px;
  background: rgba(30, 30, 30, 0.5);
  padding: 16px;
  border-radius: 6px;
  border: 1px solid rgba(50, 50, 50, 0.5);
}

.modal-body .form-group:hover {
  border-color: rgba(100, 100, 100, 0.5);
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #333;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #aaa;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.form-group input[type="text"],
.form-group input[type="color"],
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px;
  background: rgba(10, 10, 10, 0.8);
  border: 1px solid #333;
  color: #fff;
  box-sizing: border-box;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input[type="text"]:focus,
.form-group input[type="color"]:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #aa2222;
  box-shadow: 0 0 0 2px rgba(170, 34, 34, 0.2);
}

.checkbox-label {
  display: flex !important;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  color: #ccc !important;
}

.checkbox-label input[type="checkbox"] {
  width: 18px !important;
  height: 18px;
  accent-color: #aa2222;
  cursor: pointer;
}

.perms-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.perms-grid label {
  color: #aaa;
  cursor: pointer;
}

.leader-search {
  position: relative;
}

.leader-search .search-input {
  width: 100%;
  padding: 10px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  color: #fff;
  box-sizing: border-box;
}

.leader-search .search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: rgba(30, 30, 30, 0.98);
  border: 1px solid #444;
  border-top: none;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

.leader-search .search-result {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #333;
}

.leader-search .search-result:hover {
  background: rgba(170, 34, 34, 0.2);
}

.leader-search .selected-leader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  margin-top: 8px;
  color: #fff;
}

.leader-search .clear-btn {
  background: none;
  border: none;
  color: #aaa;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 5px;
}

.leader-search .clear-btn:hover {
  color: #aa2222;
}

.cancel-btn {
  padding: 10px 20px;
  background: transparent;
  border: 1px solid #444;
  color: #aaa;
  cursor: pointer;
}

.save-btn {
  padding: 10px 20px;
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  color: #4CAF50;
  cursor: pointer;
}

.bracket-section, .divisions-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #333;
}

.section-title {
  font-size: 0.9rem;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 15px;
}

.bracket-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.bracket-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bracket-label {
  font-size: 0.75rem;
  font-weight: 600;
}

.bracket-label.low { color: #888; }
.bracket-label.mid { color: #fc6f03; }
.bracket-label.high { color: #aa2222; }
.bracket-label.command { color: #ff4444; }

.bracket-card select, .division-card-select {
  padding: 8px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  color: #fff;
}

.divisions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.add-division-btn {
  padding: 6px 12px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  cursor: pointer;
  font-size: 0.75rem;
}

.divisions-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.division-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #333;
}

.division-info {
  display: flex;
  gap: 10px;
  flex: 1;
}

.division-name-input {
  flex: 1;
  padding: 8px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  color: #fff;
}

.division-card-select {
  width: 200px;
}

.remove-division-btn {
  background: none;
  border: none;
  color: #aa2222;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0 10px;
}

.no-divisions {
  padding: 20px;
  text-align: center;
  color: #666;
}

.scp-notifications {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.scp-notification {
  background: rgba(30, 30, 30, 0.98);
  border: 1px solid #444;
  border-left: 4px solid #666;
  padding: 15px 20px;
  min-width: 300px;
  max-width: 400px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.scp-notification.type-success {
  border-left-color: #4CAF50;
}

.scp-notification.type-error {
  border-left-color: #f44336;
}

.scp-notification.type-info {
  border-left-color: #2196F3;
}

.notification-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.notification-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.notification-icon svg {
  width: 100%;
  height: 100%;
}

.type-success .notification-icon {
  color: #4CAF50;
}

.type-error .notification-icon {
  color: #f44336;
}

.type-info .notification-icon {
  color: #2196F3;
}

.notification-title {
  flex: 1;
  font-weight: 700;
  color: #fff;
  font-size: 0.9rem;
}

.notification-close {
  background: none;
  border: none;
  color: #888;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  width: 20px;
  height: 20px;
}

.notification-close svg {
  width: 100%;
  height: 100%;
}

.notification-content {
  color: #aaa;
  font-size: 0.85rem;
  padding-left: 30px;
}

.notification-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: rgba(170, 34, 34, 0.8);
  animation: progress linear forwards;
}

.type-success .notification-progress {
  background: rgba(76, 175, 80, 0.8);
}

.type-error .notification-progress {
  background: rgba(244, 67, 54, 0.8);
}

@keyframes progress {
  from { width: 100%; }
  to { width: 0%; }
}

.notification-slide-enter-active,
.notification-slide-leave-active {
  transition: all 0.3s ease;
}

.notification-slide-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.notification-slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
