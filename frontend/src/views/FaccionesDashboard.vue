<template>
  <div class="page-container">
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
            <div class="notification-title">{{ notification.title }}</div>
            <button class="notification-close">&times;</button>
          </div>
          <div class="notification-content">{{ notification.message }}</div>
        </div>
      </transition-group>
    </div>

    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
    </div>

    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">DIRECTORIO DE FACCIONES</h1>
        <p class="page-subtitle">ORGANIZACIONES AUTORIZADAS DEL SITIO</p>
      </div>
      <div class="header-right">
        <button class="back-button" @click="$router.push('/dashboard')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"></path>
          </svg>
          VOLVER
        </button>
      </div>
    </div>

    <!-- Mis Facciones (si es miembro) -->
    <div v-if="myFactions.length > 0" class="my-factions-section">
      <h2 class="section-title">MIS FACCIONES</h2>
      <div class="my-factions-grid">
        <div 
          v-for="myFaction in myFactions" 
          :key="myFaction.faction_id" 
          class="my-faction-card"
          :style="{ borderColor: getFactionColor(myFaction.faction_id) }"
        >
          <div class="my-faction-header">
            <span class="faction-name">{{ myFaction.faction_name }}</span>
            <span class="faction-type-badge">{{ myFaction.faction_type }}</span>
          </div>
          <div class="my-faction-info">
            <div class="info-row">
              <span class="info-label">Rango:</span>
              <span class="info-value">{{ myFaction.rank }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Tarjeta:</span>
              <span class="info-value">{{ myFaction.access_card || 'Ninguna' }}</span>
            </div>
          </div>
          <div class="my-faction-actions">
            <!-- Botón gestionar para líderes -->
            <button 
              v-if="myFaction.is_leader" 
              class="action-btn manage-btn"
              @click="$router.push(`/dashboard/factions/manage/${myFaction.faction_id}`)"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M12 1v6m0 12v6M4.22 4.22l4.24 4.24m7.08 7.08l4.24 4.24M1 12h6m12 0h6M4.22 19.78l4.24-4.24m7.08-7.08l4.24-4.24"></path>
              </svg>
              GESTIONAR
            </button>
            <!-- Botón ver miembros para todos los miembros -->
            <button 
              class="action-btn view-btn"
              @click="viewFactionMembers(myFaction)"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87m-4-12a4 4 0 0 1 0 7.75"></path>
              </svg>
              VER MIEMBROS
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Facciones Disponibles -->
    <div class="available-factions-section">
      <h2 class="section-title">FACCIONES DISPONIBLES</h2>
      
      <div v-if="loading" class="loading-state">
        <div class="loader"></div>
        <p>CARGANDO FACCIONES...</p>
      </div>

      <div v-else-if="factions.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <p>NO HAY FACCIONES PÚBLICAS DISPONIBLES</p>
      </div>

      <div v-else class="factions-grid">
        <div 
          v-for="faction in factions" 
          :key="faction.id" 
          class="faction-card"
          :class="{ 'has-divisions': faction.has_divisions }"
          @click="selectFaction(faction)"
        >
          <div class="faction-header" :style="{ backgroundColor: faction.color + '20', borderColor: faction.color }">
            <div class="faction-icon" :style="{ backgroundColor: faction.color }">
              {{ faction.name.charAt(0) }}
            </div>
            <div class="faction-title">
              <h3>{{ faction.name }}</h3>
              <span class="faction-type">{{ faction.type }}</span>
            </div>
            <div v-if="faction.is_classified" class="classified-badge">CLASIFICADO</div>
          </div>
          
          <div class="faction-body">
            <p class="faction-description">{{ faction.description || 'Sin descripción disponible.' }}</p>
            
            <div class="faction-features">
              <span v-if="faction.has_divisions" class="feature-badge">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                  <line x1="9" y1="3" x2="9" y2="21"></line>
                </svg>
                DIVISIONES
              </span>
              <span class="feature-badge">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87m-4-12a4 4 0 0 1 0 7.75"></path>
                </svg>
                PÚBLICA
              </span>
            </div>
          </div>

          <div class="faction-footer">
            <div v-if="isFactionAdmin" class="admin-actions">
              <button
                class="apply-btn admin-manage-btn"
                @click.stop="$router.push(`/dashboard/factions/manage/${faction.id}`)"
              >
                GESTIONAR
              </button>
              <button
                class="apply-btn admin-view-btn"
                @click.stop="viewFactionMembers(faction)"
              >
                VER MIEMBROS
              </button>
            </div>
            <button
              v-else-if="!isMemberOf(faction.id) && faction.allow_applications"
              class="apply-btn"
              @click.stop="applyToFaction(faction)"
            >
              SOLICITAR INGRESO
            </button>
            <span v-else-if="isMemberOf(faction.id)" class="member-badge">
              YA ERES MIEMBRO
            </span>
            <span v-else class="closed-badge">
              NO APLICABLE
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Ver Miembros -->
    <div v-if="showMembersModal" class="modal-overlay" @click="showMembersModal = false">
      <div class="modal-content members-modal" @click.stop>
        <div class="modal-header">
          <h2>MIEMBROS DE {{ selectedFactionForMembers?.faction_name || selectedFactionForMembers?.name }}</h2>
          <button class="close-btn" @click="showMembersModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="loadingMembers" class="loading-state">
            <div class="loader"></div>
          </div>
          <div v-else-if="factionMembers.length === 0" class="empty-state">
            <p>NO HAY MIEMBROS EN ESTA FACCIÓN</p>
          </div>
          <div v-else class="members-list">
            <div v-for="member in factionMembers" :key="member.character_id" class="member-item">
              <div class="member-avatar">
                {{ (member.character_name || '?').charAt(0) }}
              </div>
              <div class="member-info">
                <span class="member-name">{{ member.character_name }}</span>
                <span class="member-rank">{{ member.rank || 'Sin rango' }}</span>
              </div>
              <div v-if="member.access_card" class="member-division">
                {{ member.access_card }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Detalles Facción -->
    <div v-if="selectedFaction" class="modal-overlay" @click="selectedFaction = null">
      <div class="modal-content faction-modal" @click.stop>
        <div class="modal-header" :style="{ borderColor: selectedFaction.color }">
          <h2>{{ selectedFaction.name }}</h2>
          <button class="close-btn" @click="selectedFaction = null">&times;</button>
        </div>
        <div class="modal-body">
          <div class="faction-detail-header">
            <div class="faction-detail-icon" :style="{ backgroundColor: selectedFaction.color }">
              {{ selectedFaction.name.charAt(0) }}
            </div>
            <div class="faction-detail-info">
              <span class="faction-detail-type">{{ selectedFaction.type }}</span>
              <span v-if="selectedFaction.is_classified" class="classified-badge">CLASIFICADO</span>
            </div>
          </div>
          
          <p class="faction-detail-description">{{ selectedFaction.description }}</p>
          
          <div class="faction-detail-actions">
            <button 
              v-if="!isMemberOf(selectedFaction.id) && selectedFaction.allow_applications"
              class="apply-btn-large"
              @click="applyToFaction(selectedFaction)"
            >
              SOLICITAR INGRESO
            </button>
            <span v-else-if="isMemberOf(selectedFaction.id)" class="member-badge-large">
              YA ERES MIEMBRO DE ESTA FACCIÓN
            </span>
            <span v-else class="closed-badge-large">
              ESTA FACCIÓN NO ACEPTA SOLICITUDES
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const loading = ref(true)
const factions = ref([])
const currentUser = ref(null)
const isFactionAdmin = ref(false)
const myFactions = ref([])
const myCharacters = ref([])
const selectedFaction = ref(null)
const showMembersModal = ref(false)
const selectedFactionForMembers = ref(null)
const factionMembers = ref([])
const loadingMembers = ref(false)

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

const fetchFactions = async () => {
  try {
    const response = await fetch('/api/factions/')
    if (response.ok) {
      const data = await response.json()
      factions.value = data.results || data || []
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const fetchMyFactions = async () => {
  try {
    const response = await fetch('/api/factions/my/')
    if (response.ok) {
      const data = await response.json()
      myFactions.value = data.factions || data.results || data || []
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const fetchMyCharacters = async () => {
  try {
    const response = await fetch('/api/characters/mine/')
    if (response.ok) {
      const data = await response.json()
      myCharacters.value = data.results || data || []
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const fetchFactionMembers = async (factionId) => {
  loadingMembers.value = true
  try {
    const response = await fetch(`/api/factions/${factionId}/members/`)
    if (response.ok) {
      const data = await response.json()
      factionMembers.value = data.members || data.results || []
    }
  } catch (err) {
    console.error('Error:', err)
    showNotification('ERROR', 'Error al cargar miembros', 'error', 5000)
  }
  loadingMembers.value = false
}

const isMemberOf = (factionId) => {
  return myFactions.value.some(f => f.faction_id === factionId)
}

const getFactionColor = (factionId) => {
  const faction = factions.value.find(f => f.id === factionId)
  return faction?.color || '#aa2222'
}

const selectFaction = (faction) => {
  selectedFaction.value = faction
}

const viewFactionMembers = async (faction) => {
  selectedFactionForMembers.value = faction
  showMembersModal.value = true
  await fetchFactionMembers(faction.faction_id || faction.id)
}

const applyToFaction = async (faction) => {
  if (!myCharacters.value || myCharacters.value.length === 0) {
    showNotification('ERROR', 'Necesitas tener un personaje para solicitar ingreso a una facción', 'error', 5000)
    return
  }
  
  const characterId = myCharacters.value[0].id
  
  try {
    const response = await fetch(`/api/factions/${faction.id}/apply/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ character_id: characterId, message: '' })
    })
    
    if (response.ok) {
      showNotification('ÉXITO', 'Solicitud enviada correctamente', 'success', 4000)
      selectedFaction.value = null
    } else {
      const data = await response.json()
      showNotification('ERROR', data.error || 'Error al aplicar', 'error', 5000)
    }
  } catch (err) {
    showNotification('ERROR', 'Error al aplicar a la facción', 'error', 5000)
  }
}

const fetchCurrentUser = async () => {
  try {
    const res = await fetch('/api/auth/user/')
    currentUser.value = await res.json()
    if (currentUser.value?.is_superuser || currentUser.value?.is_staff) {
      isFactionAdmin.value = true
      return
    }
    // Moderación de facciones también gestiona sin ser miembro
    const permRes = await fetch('/api/auth/user/permissions/')
    if (permRes.ok) {
      const permData = await permRes.json()
      isFactionAdmin.value = (permData.permissions || []).includes('moderate_factions_full')
    }
  } catch { /* noop */ }
}

onMounted(async () => {
  await Promise.all([fetchFactions(), fetchMyFactions(), fetchMyCharacters(), fetchCurrentUser()])
  loading.value = false
})
</script>

<style scoped>
.admin-actions {
  display: flex;
  gap: 8px;
  width: 100%;
}
.admin-actions .apply-btn {
  flex: 1;
}
.admin-manage-btn {
  border-color: #2ecc71 !important;
  color: #2ecc71 !important;
}
.admin-manage-btn:hover {
  background: rgba(46, 204, 113, 0.15) !important;
}
.page-container {
  min-height: 100vh;
  color: #d8d8d8;
  background: #0a0a0a;
  padding: 20px;
  position: relative;
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

.page-header {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header-left {
  display: flex;
  flex-direction: column;
}

.page-title {
  font-size: 1.8rem;
  color: #fff;
  margin: 0;
  letter-spacing: 2px;
}

.page-subtitle {
  color: #666;
  margin: 5px 0 0 0;
  font-size: 0.8rem;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  cursor: pointer;
  font-size: 0.8rem;
}

.back-button svg {
  width: 16px;
  height: 16px;
}

.section-title {
  font-size: 1rem;
  color: #fff;
  margin: 0 0 20px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #333;
}

/* Mis Facciones */
.my-factions-section {
  position: relative;
  z-index: 1;
  margin-bottom: 40px;
}

.my-factions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.my-faction-card {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  border-left: 4px solid;
  padding: 20px;
}

.my-faction-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.my-faction-header .faction-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
}

.faction-type-badge {
  padding: 4px 8px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  font-size: 0.7rem;
}

.my-faction-info {
  margin-bottom: 15px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  border-bottom: 1px solid #222;
}

.info-label {
  color: #666;
  font-size: 0.8rem;
}

.info-value {
  color: #fff;
  font-size: 0.8rem;
}

.my-faction-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  border: 1px solid;
  background: transparent;
  color: #fff;
  cursor: pointer;
  font-size: 0.75rem;
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

.manage-btn {
  border-color: rgba(76, 175, 80, 0.5);
  color: #4CAF50;
}

.manage-btn:hover {
  background: rgba(76, 175, 80, 0.1);
}

.view-btn {
  border-color: rgba(170, 34, 34, 0.5);
  color: #aa2222;
}

.view-btn:hover {
  background: rgba(170, 34, 34, 0.1);
}

/* Available Factions */
.available-factions-section {
  position: relative;
  z-index: 1;
}

.factions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.faction-card {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.faction-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
}

.faction-header {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  border-bottom: 1px solid;
  background: rgba(30, 30, 30, 0.5);
}

.faction-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
}

.faction-title {
  flex: 1;
}

.faction-title h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #fff;
}

.faction-type {
  color: #666;
  font-size: 0.75rem;
}

.classified-badge {
  padding: 4px 8px;
  background: rgba(170, 34, 34, 0.2);
  border: 1px solid #aa2222;
  color: #aa2222;
  font-size: 0.65rem;
}

.faction-body {
  padding: 20px;
}

.faction-description {
  color: #aaa;
  font-size: 0.85rem;
  margin: 0 0 15px 0;
  line-height: 1.5;
}

.faction-features {
  display: flex;
  gap: 10px;
}

.feature-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 4px 8px;
  background: rgba(60, 60, 60, 0.3);
  border: 1px solid #444;
  color: #888;
  font-size: 0.7rem;
}

.feature-badge svg {
  width: 12px;
  height: 12px;
}

.faction-footer {
  padding: 15px 20px;
  border-top: 1px solid #333;
}

.apply-btn {
  width: 100%;
  padding: 12px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background 0.2s;
}

.apply-btn:hover {
  background: rgba(170, 34, 34, 0.2);
}

.member-badge, .closed-badge {
  display: block;
  text-align: center;
  padding: 12px;
  font-size: 0.8rem;
}

.member-badge {
  color: #4CAF50;
}

.closed-badge {
  color: #666;
}

/* Modals */
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
  color: #fff;
  font-size: 1rem;
}

.close-btn {
  background: none;
  border: none;
  color: #888;
  font-size: 2rem;
  cursor: pointer;
}

.modal-body {
  padding: 20px;
}

/* Members Modal */
.members-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px;
  background: rgba(30, 30, 30, 0.5);
  border: 1px solid #333;
}

.member-avatar {
  width: 40px;
  height: 40px;
  background: rgba(170, 34, 34, 0.2);
  border: 1px solid #aa2222;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #aa2222;
  font-weight: 700;
}

.member-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.member-name {
  color: #fff;
  font-size: 0.9rem;
}

.member-rank {
  color: #666;
  font-size: 0.75rem;
}

.member-division {
  padding: 4px 8px;
  background: rgba(60, 60, 60, 0.3);
  border: 1px solid #444;
  color: #888;
  font-size: 0.7rem;
}

/* Faction Detail Modal */
.faction-modal .modal-header {
  border-left: 4px solid;
}

.faction-detail-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.faction-detail-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
}

.faction-detail-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.faction-detail-type {
  color: #666;
  font-size: 0.9rem;
}

.faction-detail-description {
  color: #aaa;
  line-height: 1.6;
  margin-bottom: 20px;
}

.faction-detail-actions {
  text-align: center;
}

.apply-btn-large {
  width: 100%;
  padding: 15px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  cursor: pointer;
  font-size: 0.9rem;
}

.member-badge-large, .closed-badge-large {
  display: block;
  padding: 15px;
  font-size: 0.9rem;
}

.member-badge-large {
  color: #4CAF50;
}

.closed-badge-large {
  color: #666;
}

/* Loading & Empty States */
.loading-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.loader {
  width: 40px;
  height: 40px;
  border: 3px solid #333;
  border-top-color: #aa2222;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state svg {
  width: 60px;
  height: 60px;
  margin-bottom: 20px;
  opacity: 0.5;
}

/* Notifications */
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
}

.scp-notification.type-success {
  border-left-color: #4CAF50;
}

.scp-notification.type-error {
  border-left-color: #f44336;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.notification-title {
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
}

.notification-content {
  color: #aaa;
  font-size: 0.85rem;
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
