<template>
  <div class="admin-panel">
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

    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">ADMINISTRACIÓN DE FACCIONES</h1>
        <p class="page-subtitle">GESTIÓN DE TARJETAS DE ACCESO</p>
      </div>
      <button class="back-btn" @click="$router.push('/dashboard/factions')">
        VOLVER
      </button>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'cards' }" 
        @click="activeTab = 'cards'"
      >
        TARJETAS
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'create' }" 
        @click="activeTab = 'create'"
      >
        CREAR FACCIÓN
      </button>
    </div>

    <!-- Tarjetas de Acceso -->
    <div v-if="activeTab === 'cards'" class="tab-content">
      <div class="cards-grid">
        <div v-for="card in cards" :key="card.id" class="card-item">
          <div class="card-header">
            <span class="card-level">{{ card.name }}</span>
          </div>
          <div class="card-body">
            <h3>{{ card.name }}</h3>
            <p>{{ card.description }}</p>
            <div class="card-permissions">
              <span v-if="card.can_edit_scp">SCP</span>
              <span v-if="card.can_edit_scd">SCD</span>
              <span v-if="card.can_edit_o5">O5</span>
              <span v-if="card.can_edit_any">ANY</span>
            </div>
          </div>
          <div class="card-footer">
            <button class="edit-btn" @click="editCard(card)">EDITAR</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Crear Facción -->
    <div v-if="activeTab === 'create'" class="tab-content">
      <form @submit.prevent="createFaction" class="faction-form">
        <div class="form-group">
          <label>Nombre interno:</label>
          <input v-model="newFaction.name" required />
        </div>
        <div class="form-group">
          <label>Nombre a mostrar:</label>
          <input v-model="newFaction.display_name" required />
        </div>
        <div class="form-group">
          <label>Tipo de facción:</label>
          <select v-model="newFaction.faction_type" required>
            <option value="MTF">MTF</option>
            <option value="RESEARCH">Research</option>
            <option value="SECURITY">Security</option>
            <option value="ADMIN">Admin</option>
            <option value="ETHICS">Ethics</option>
            <option value="OTHER">Other</option>
          </select>
        </div>
        <div class="form-group">
          <label>Descripción:</label>
          <textarea v-model="newFaction.description" rows="4"></textarea>
        </div>
        <div class="form-group">
          <label>Color:</label>
          <input type="color" v-model="newFaction.color" />
        </div>
        <div class="form-group">
          <label>
            <input type="checkbox" v-model="newFaction.is_public" />
            Facción pública
          </label>
        </div>
        <div class="form-group">
          <label>
            <input type="checkbox" v-model="newFaction.allow_applications" />
            Permitir aplicaciones
          </label>
        </div>
        <button type="submit" class="submit-btn">CREAR FACCIÓN</button>
      </form>
    </div>

    <!-- Modal Editar Tarjeta -->
    <div v-if="editingCard" class="modal" @click="editingCard = null">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Editar Tarjeta</h2>
          <button class="close-btn" @click="editingCard = null">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Nombre:</label>
            <input v-model="editingCard.name" />
          </div>
          <div class="form-group">
            <label>Descripción:</label>
            <textarea v-model="editingCard.description" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>Clasificada:</label>
            <input type="checkbox" v-model="editingCard.is_classified" />
          </div>
          <h4>Permisos de edición:</h4>
          <div class="permissions-grid">
            <label><input type="checkbox" v-model="editingCard.can_edit_scp" /> SCP</label>
            <label><input type="checkbox" v-model="editingCard.can_edit_scd" /> SCD</label>
            <label><input type="checkbox" v-model="editingCard.can_edit_o5" /> O5</label>
            <label><input type="checkbox" v-model="editingCard.can_edit_any" /> ANY</label>
          </div>
        </div>
        <div class="modal-footer">
          <button class="save-btn" @click="saveCard">GUARDAR</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const activeTab = ref('cards')
const cards = ref([])
const editingCard = ref(null)
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

const newFaction = ref({
  name: '',
  display_name: '',
  faction_type: 'MTF',
  description: '',
  color: '#fc6f03',
  is_public: true,
  allow_applications: true
})

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
      showNotification('ÉXITO', 'Tarjeta guardada correctamente', 'success', 4000)
    } else {
      showNotification('ERROR', 'Error al guardar', 'error', 5000)
    }
  } catch (err) {
    showNotification('ERROR', 'Error al guardar', 'error', 5000)
  }
}

const createFaction = async () => {
  try {
    const response = await fetch('/api/factions/create/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newFaction.value)
    })
    if (response.ok) {
      showNotification('ÉXITO', 'Facción creada correctamente', 'success', 4000)
      newFaction.value = {
        name: '',
        display_name: '',
        faction_type: 'MTF',
        description: '',
        color: '#fc6f03',
        is_public: true,
        allow_applications: true
      }
    } else {
      const data = await response.json()
      showNotification('ERROR', data.error || 'Error al crear facción', 'error', 5000)
    }
  } catch (err) {
    showNotification('ERROR', 'Error al crear facción', 'error', 5000)
  }
}

onMounted(() => {
  fetchCards()
})
</script>

<style scoped>
.admin-panel {
  padding: 20px;
  min-height: 100vh;
  color: #d8d8d8;
  background: #0a0a0a;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-title {
  font-size: 2rem;
  font-weight: 900;
  color: #fc6f03;
  margin: 0;
}

.page-subtitle {
  font-size: 0.8rem;
  color: #888;
  margin: 5px 0 0 0;
}

.back-btn {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid #333;
  color: #aaa;
  cursor: pointer;
}

.tabs {
  display: flex;
  gap: 5px;
  margin-bottom: 20px;
  border-bottom: 1px solid #333;
}

.tab-btn {
  padding: 12px 20px;
  background: transparent;
  border: none;
  color: #888;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.tab-btn.active {
  color: #fc6f03;
  border-bottom-color: #fc6f03;
}

.tab-content {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  padding: 20px;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.card-item {
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
  color: #fc6f03;
}

.card-type {
  font-size: 0.8rem;
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

.card-permissions {
  display: flex;
  gap: 5px;
}

.card-permissions span {
  padding: 3px 8px;
  background: rgba(252, 111, 3, 0.1);
  border: 1px solid rgba(252, 111, 3, 0.3);
  color: #fc6f03;
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
  background: rgba(252, 111, 3, 0.1);
  border: 1px solid rgba(252, 111, 3, 0.3);
  color: #fc6f03;
  cursor: pointer;
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

.form-group input[type="text"],
.form-group input[type="color"],
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  color: #fff;
}

.faction-form {
  max-width: 600px;
}

.submit-btn {
  padding: 12px 24px;
  background: rgba(252, 111, 3, 0.1);
  border: 1px solid rgba(252, 111, 3, 0.3);
  color: #fc6f03;
  font-weight: 600;
  cursor: pointer;
}

/* Modal */
.modal {
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
  color: #fc6f03;
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
  justify-content: center;
}

.save-btn {
  padding: 10px 30px;
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  color: #4CAF50;
  cursor: pointer;
}

.permissions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.permissions-grid label {
  color: #aaa;
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
