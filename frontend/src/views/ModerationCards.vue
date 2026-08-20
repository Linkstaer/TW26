<template>
  <div class="moderacion-page">
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
    </div>

    <!-- Notifications -->
    <div class="notifications-container">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="notification"
        :class="notification.type"
      >
        <div class="notification-header">
          <span class="notification-title">{{ notification.title }}</span>
          <button class="notification-close" @click="removeNotification(notification.id)">&times;</button>
        </div>
        <div class="notification-message">{{ notification.message }}</div>
      </div>
    </div>

    <div class="moderacion-header">
      <div class="header-left">
        <div class="header-logo">
          <div class="header-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#aa2222" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <div class="header-title">
            <span class="header-main">TARJETAS DE ACCESO</span>
            <span class="header-sub">SISTEMA DE CLEARANCE</span>
          </div>
        </div>
      </div>
      
      <div class="header-right">
        <div class="session-status">
          <div class="session-indicator active"></div>
          <span class="session-text">ADMIN ACTIVE</span>
        </div>
        <div class="current-time">{{ currentTime }}</div>
      </div>
    </div>

    <main class="moderacion-main">
      <div class="content-header">
        <h2>GESTIÓN DE TARJETAS</h2>
        <button class="create-btn" @click="showCreateModal = true">
          + CREAR TARJETA
        </button>
      </div>

      <div class="cards-grid">
        <div v-for="card in cards" :key="card.id" class="access-card">
          <div class="card-header">
            <span class="card-level">{{ card.name }}</span>
            <span v-if="card.is_classified" class="classified-badge">CLASIFICADO</span>
          </div>
          <div class="card-body">
            <h3>{{ card.name }}</h3>
            <p>{{ card.description || 'Sin descripción' }}</p>
          </div>
          <div class="card-footer">
            <button class="edit-btn" @click="editCard(card)">EDITAR</button>
          </div>
        </div>
      </div>
    </main>

    <div v-if="editingCard" class="modal-overlay" @click="editingCard = null">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>EDITAR TARJETA</h2>
          <button class="close-btn" @click="editingCard = null">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Nombre:</label>
            <input v-model="editingCard.name" />
          </div>
          <div class="form-group">
            <label>Descripción:</label>
            <textarea v-model="editingCard.description" rows="4"></textarea>
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="editingCard.is_classified" />
              Clasificada
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="editingCard = null">CANCELAR</button>
          <button class="save-btn" @click="saveCard">GUARDAR</button>
        </div>
      </div>
    </div>

    <!-- Modal Crear Tarjeta -->
    <div v-if="showCreateModal" class="modal-overlay" @click="closeCreateModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>CREAR TARJETA</h2>
          <button class="close-btn" @click="closeCreateModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Nombre:</label>
            <input v-model="cardForm.name" placeholder="Ej: Gamma 1, Gamma 2, O5" />
          </div>
          <div class="form-group">
            <label>Descripción:</label>
            <textarea v-model="cardForm.description" rows="4" placeholder="Descripción de la tarjeta..."></textarea>
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="cardForm.is_classified" />
              Clasificada
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="closeCreateModal">CANCELAR</button>
          <button class="save-btn" @click="createCard">CREAR</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

const cards = ref([])
const editingCard = ref(null)
const showCreateModal = ref(false)
const currentTime = ref('')
const notifications = ref([])
let notificationId = 0

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
  }
}

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

const cardForm = ref({
  name: '',
  description: '',
  is_classified: false
})

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('en-US', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
  }).replace(/(\d+)\/(\d+)\/(\d+),/, '$3-$1-$2')
}

const fetchCards = async () => {
  try {
    const response = await fetch('/api/cards/')
    if (response.ok) {
      const data = await response.json()
      cards.value = data.cards || []
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const editCard = (card) => {
  editingCard.value = { ...card }
}

const closeCreateModal = () => {
  showCreateModal.value = false
  cardForm.value = {
    name: '',
    description: '',
    is_classified: false
  }
}

const createCard = async () => {
  try {
    const response = await fetch('/api/cards/create/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cardForm.value)
    })
    if (response.ok) {
      await fetchCards()
      closeCreateModal()
      showNotification('ÉXITO', 'Tarjeta creada correctamente', 'success', 4000)
    } else {
      const data = await response.json()
      showNotification('ERROR', data.error || 'Error al crear', 'error', 5000)
    }
  } catch (err) {
    showNotification('ERROR', 'Error al crear', 'error', 5000)
  }
}

const saveCard = async () => {
  try {
    const response = await fetch(`/api/cards/${editingCard.value.id}/update/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingCard.value)
    })
    if (response.ok) {
      await fetchCards()
      editingCard.value = null
      showNotification('ÉXITO', 'Tarjeta actualizada correctamente', 'success', 4000)
    } else {
      showNotification('ERROR', 'Error al guardar', 'error', 5000)
    }
  } catch (err) {
    showNotification('ERROR', 'Error al guardar', 'error', 5000)
  }
}

onMounted(() => {
  updateTime()
  setInterval(updateTime, 1000)
  fetchCards()
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
  margin-top: 50px;
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
}

.header-sub {
  font-size: 0.7rem;
  color: #888;
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
  background: #4CAF50;
}

.session-text {
  font-size: 0.7rem;
  color: #4CAF50;
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

.create-btn {
  padding: 10px 20px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  cursor: pointer;
  font-size: 0.8rem;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.access-card {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
}

.card-header {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  background: rgba(30, 30, 30, 0.8);
  border-bottom: 1px solid #333;
}

.card-level {
  font-size: 1.2rem;
  font-weight: 700;
  color: #aa2222;
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
}

.classified-badge {
  padding: 3px 8px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  font-size: 0.7rem;
}

.card-footer {
  padding: 15px;
  border-top: 1px solid #333;
}

.edit-btn {
  width: 100%;
  padding: 8px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  cursor: pointer;
}

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
  padding: 20px;
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
  margin-bottom: 5px;
  color: #888;
  font-size: 0.8rem;
}

.form-group input, .form-group select, .form-group textarea {
  width: 100%;
  padding: 10px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  color: #fff;
  box-sizing: border-box;
}

.checkbox-label {
  display: flex !important;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.perms-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.perms-grid label {
  color: #aaa;
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

.notifications-container {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.notification {
  background: rgba(30, 30, 30, 0.98);
  border: 1px solid #444;
  border-left: 4px solid #666;
  padding: 15px 20px;
  min-width: 300px;
  max-width: 400px;
  animation: slideIn 0.3s ease-out;
}

.notification.success {
  border-left-color: #4CAF50;
}

.notification.error {
  border-left-color: #f44336;
}

.notification.info {
  border-left-color: #2196F3;
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

.notification.error .notification-title {
  color: #f44336;
}

.notification.success .notification-title {
  color: #4CAF50;
}

.notification-close {
  background: none;
  border: none;
  color: #888;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.notification-message {
  color: #aaa;
  font-size: 0.85rem;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>
