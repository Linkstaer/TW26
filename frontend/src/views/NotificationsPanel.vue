<template>
  <div class="notifications-panel">
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">NOTIFICACIONES</h1>
        <p class="page-subtitle">CENTRO DE COMUNICACIONES</p>
      </div>
      <button class="mark-all-btn" @click="markAllRead" :disabled="unreadCount === 0">
        MARCAR TODO LEÍDO
      </button>
    </div>

    <div class="unread-badge" v-if="unreadCount > 0">
      <span>{{ unreadCount }} notificación{{ unreadCount > 1 ? 's' : '' }} sin leer</span>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="loader"></div>
      <p>CARGANDO NOTIFICACIONES...</p>
    </div>

    <div v-else-if="notifications.length === 0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
        <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
      </svg>
      <p>NO TIENES NOTIFICACIONES</p>
    </div>

    <div v-else class="notifications-list">
      <div 
        v-for="notif in notifications" 
        :key="notif.id" 
        class="notification-item"
        :class="{ 'unread': !notif.is_read, 'invitation': notif.type === 'faction_invitation' }"
        @click="handleNotificationClick(notif)"
      >
        <div class="notif-icon">
          <svg v-if="notif.type === 'faction_invitation'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
        </div>
        <div class="notif-content">
          <div class="notif-header">
            <span class="notif-title">{{ notif.title }}</span>
            <span class="notif-time">{{ formatDate(notif.created_at) }}</span>
          </div>
          <p class="notif-message">{{ notif.message }}</p>
        </div>
        <div class="notif-actions">
          <button v-if="notif.type === 'faction_invitation' && !notif.is_read" class="respond-btn" @click.stop="respondToInvitation(notif)">
            RESPONDER
          </button>
          <button v-if="notif.type === 'faction_application' && notif.faction_id" class="respond-btn" @click.stop="goToApplications(notif)">
            GESTIONAR
          </button>
          <button v-if="!notif.is_read" class="read-btn" @click.stop="markAsRead(notif.id)">
            ✓
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Invitación -->
    <div v-if="respondingInvitation" class="modal" @click="respondingInvitation = null">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>INVITACIÓN DE FACCIÓN</h2>
          <button class="close-btn" @click="respondingInvitation = null">&times;</button>
        </div>
        <div class="modal-body">
          <p>{{ respondingInvitation.message }}</p>
        </div>
        <div class="modal-footer">
          <button class="decline-btn" @click="respondInvitation(respondingInvitation.id, 'decline')">RECHAZAR</button>
          <button class="accept-btn" @click="respondInvitation(respondingInvitation.id, 'accept')">ACEPTAR</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const loading = ref(true)
const notifications = ref([])
const unreadCount = ref(0)
const router = useRouter()

const goToApplications = (notif) => {
  if (!notif.is_read) markAsRead(notif.id)
  router.push(`/dashboard/factions/manage/${notif.faction_id}`)
}

// Mantener sincronizado el badge del Header (misma SPA, sin recarga)
const broadcastUnread = () => {
  window.dispatchEvent(
    new CustomEvent('notifications-updated', { detail: { count: unreadCount.value } })
  )
}
const respondingInvitation = ref(null)

const fetchNotifications = async () => {
  try {
    const response = await fetch('/api/notifications/')
    if (response.ok) {
      const data = await response.json()
      notifications.value = data.notifications || []
    }
  } catch (err) {
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}

const fetchUnreadCount = async () => {
  try {
    const response = await fetch('/api/notifications/unread-count/')
    if (response.ok) {
      const data = await response.json()
      unreadCount.value = data.unread_count || 0
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const markAsRead = async (id) => {
  try {
    const response = await fetch(`/api/notifications/${id}/read/`, { method: 'POST' })
    if (response.ok) {
      const notif = notifications.value.find(n => n.id === id)
      if (notif) notif.is_read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
      broadcastUnread()
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const markAllRead = async () => {
  try {
    const response = await fetch('/api/notifications/read-all/', { method: 'POST' })
    if (response.ok) {
      notifications.value.forEach(n => n.is_read = true)
      unreadCount.value = 0
      broadcastUnread()
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const handleNotificationClick = async (notif) => {
  if (!notif.is_read) {
    await markAsRead(notif.id)
  }
  if (notif.type === 'faction_invitation') {
    respondingInvitation.value = notif
  }
}

const respondToInvitation = (notif) => {
  respondingInvitation.value = notif
}

const respondInvitation = async (invitationId, action) => {
  try {
    const response = await fetch(`/api/invitations/${invitationId}/respond/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action })
    })
    if (response.ok) {
      const data = await response.json()
      alert(data.message)
      respondingInvitation.value = null
      await fetchNotifications()
      await fetchUnreadCount()
    } else {
      const data = await response.json()
      alert(data.error || 'Error al responder')
    }
  } catch (err) {
    alert('Error al responder invitación')
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 60) return `Hace ${minutes} min`
  if (hours < 24) return `Hace ${hours} h`
  if (days < 7) return `Hace ${days} días`
  return date.toLocaleDateString()
}

onMounted(() => {
  fetchNotifications()
  fetchUnreadCount()
})
</script>

<style scoped>
.notifications-panel {
  padding: 20px;
  min-height: 100vh;
  color: #d8d8d8;
  background: #0a0a0a;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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

.mark-all-btn {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid #333;
  color: #aaa;
  cursor: pointer;
}

.mark-all-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.unread-badge {
  padding: 10px 15px;
  background: rgba(252, 111, 3, 0.1);
  border: 1px solid rgba(252, 111, 3, 0.3);
  margin-bottom: 20px;
  color: #fc6f03;
  font-size: 0.85rem;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #888;
}

.loader {
  width: 40px;
  height: 40px;
  border: 3px solid #333;
  border-top-color: #fc6f03;
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

.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.notification-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  cursor: pointer;
  transition: all 0.2s;
}

.notification-item:hover {
  border-color: #444;
}

.notification-item.unread {
  background: rgba(30, 25, 20, 0.95);
  border-left: 3px solid #fc6f03;
}

.notification-item.invitation {
  border-left: 3px solid #4CAF50;
}

.notif-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(40, 40, 40, 0.8);
  flex-shrink: 0;
}

.notif-icon svg {
  width: 20px;
  height: 20px;
  color: #888;
}

.unread .notif-icon svg {
  color: #fc6f03;
}

.notif-content {
  flex: 1;
}

.notif-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.notif-title {
  font-weight: 600;
  color: #fff;
}

.unread .notif-title {
  color: #fc6f03;
}

.notif-time {
  font-size: 0.75rem;
  color: #666;
}

.notif-message {
  font-size: 0.85rem;
  color: #aaa;
  margin: 0;
  line-height: 1.4;
}

.notif-actions {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.respond-btn {
  padding: 5px 10px;
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  color: #4CAF50;
  font-size: 0.7rem;
  cursor: pointer;
}

.read-btn {
  width: 30px;
  height: 30px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid #333;
  color: #4CAF50;
  cursor: pointer;
  font-size: 14px;
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
  max-width: 400px;
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
  color: #fc6f03;
  font-size: 1.2rem;
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

.modal-body p {
  color: #aaa;
  line-height: 1.6;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #333;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.accept-btn {
  padding: 10px 20px;
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  color: #4CAF50;
  cursor: pointer;
}

.decline-btn {
  padding: 10px 20px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  cursor: pointer;
}
</style>
