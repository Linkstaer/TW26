<template>
  <div class="feed-page">
    <div class="site-background"><div class="grid-overlay"></div></div>

    <div class="page-header">
      <h1 class="page-title">FEED DE ANUNCIOS</h1>
      <div class="page-subtitle">COMUNICADOS Y EVENTOS DEL SITIO</div>
    </div>

    <main class="page-content">
      <div class="tabs">
        <button class="tab" :class="{ active: tab === 'announcements' }" @click="tab = 'announcements'">
          ANUNCIOS
        </button>
        <button class="tab" :class="{ active: tab === 'events' }" @click="tab = 'events'">
          EVENTOS DEL SISTEMA
        </button>
        <button class="btn btn-primary create-btn" @click="createOpen = true">+ PUBLICAR</button>
      </div>

      <!-- Anuncios -->
      <div v-if="tab === 'announcements'">
        <div v-if="loading" class="loading-text">SINCRONIZANDO FEED...</div>
        <div v-else-if="announcements.length === 0" class="empty-text">
          No hay anuncios visibles para su nivel de acceso.
        </div>
        <div class="feed-list">
          <div
            v-for="ann in announcements"
            :key="ann.id"
            class="feed-item"
            :class="{ pinned: ann.is_pinned }"
            @click="openAnnouncement(ann.id)"
          >
            <div class="feed-item-header">
              <span class="type-chip" :class="'t-' + ann.announcement_type">
                {{ typeLabel(ann.announcement_type) }}
              </span>
              <span class="level-chip">{{ ann.min_access_level }}</span>
              <span v-if="ann.is_pinned" class="pin-chip">📌 FIJADO</span>
              <span class="feed-date">{{ formatDate(ann.created_at) }}</span>
            </div>
            <div class="feed-title">{{ ann.title }}</div>
            <div class="feed-author" v-if="ann.author">Publicado por {{ ann.author }}</div>
          </div>
        </div>
      </div>

      <!-- Eventos -->
      <div v-else>
        <div v-if="events.length === 0" class="empty-text">Sin eventos registrados.</div>
        <div class="feed-list">
          <div v-for="ev in events" :key="ev.id" class="feed-item event-item">
            <div class="feed-item-header">
              <span class="type-chip t-automatic">{{ eventLabel(ev.event_type) }}</span>
              <span class="feed-date">{{ formatDate(ev.created_at) }}</span>
            </div>
            <div class="feed-title">{{ ev.title }}</div>
            <div class="feed-body">{{ ev.description }}</div>
          </div>
        </div>
      </div>

      <!-- Detalle de anuncio -->
      <div v-if="selected" class="modal-overlay" @click.self="selected = null">
        <div class="modal">
          <div class="feed-item-header">
            <span class="type-chip" :class="'t-' + selected.announcement_type">
              {{ typeLabel(selected.announcement_type) }}
            </span>
            <span class="level-chip">{{ selected.min_access_level }}</span>
          </div>
          <h3>{{ selected.title }}</h3>
          <pre class="announcement-content">{{ selected.content }}</pre>
          <div class="feed-author" v-if="selected.author">
            Publicado por {{ selected.author }} — {{ formatDate(selected.created_at) }}
          </div>
          <div class="edit-actions">
            <button class="btn btn-ghost" @click="selected = null">CERRAR</button>
          </div>
        </div>
      </div>

      <!-- Publicar -->
      <div v-if="createOpen" class="modal-overlay" @click.self="createOpen = false">
        <div class="modal">
          <h3>PUBLICAR ANUNCIO</h3>
          <input v-model="form.title" placeholder="Título" />
          <select v-model="form.announcement_type">
            <option value="in_rp">In-RP</option>
            <option value="off_rp">Off-RP</option>
            <option value="critical">Crítico (solo administración)</option>
          </select>
          <select v-model="form.min_access_level">
            <option v-for="l in ['L1','L2','L3','L4','L5','L6']" :key="l" :value="l">
              Nivel mínimo: {{ l }}
            </option>
          </select>
          <textarea v-model="form.content" rows="6" placeholder="Contenido"></textarea>
          <div class="edit-actions">
            <button class="btn btn-primary" @click="createAnnouncement">PUBLICAR</button>
            <button class="btn btn-ghost" @click="createOpen = false">CANCELAR</button>
          </div>
          <div v-if="error" class="error-text">{{ error }}</div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const tab = ref('announcements')
const announcements = ref([])
const events = ref([])
const selected = ref(null)
const loading = ref(true)
const createOpen = ref(false)
const error = ref('')
const form = ref({ title: '', content: '', announcement_type: 'off_rp', min_access_level: 'L1' })

const TYPE_LABELS = { in_rp: 'IN-RP', off_rp: 'OFF-RP', automatic: 'AUTOMÁTICO', critical: 'CRÍTICO' }
const EVENT_LABELS = {
  scp_created: 'NUEVO SCP',
  scp_deleted: 'SCP ELIMINADO',
  faction_created: 'FACCIÓN CREADA',
  faction_dissolved: 'FACCIÓN DISUELTA',
  document_created: 'NUEVO DOCUMENTO',
  user_joined_faction: 'INGRESO A FACCIÓN',
  user_left_faction: 'SALIDA DE FACCIÓN',
}
const typeLabel = (t) => TYPE_LABELS[t] || t
const eventLabel = (t) => EVENT_LABELS[t] || t

const getCsrf = () => {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1] || ''
}

const formatDate = (iso) => (iso ? new Date(iso).toLocaleString('es-ES') : '')

const fetchAll = async () => {
  loading.value = true
  try {
    const [annRes, evRes] = await Promise.all([
      fetch('/api/announcements/'),
      fetch('/api/feed/events/')
    ])
    if (annRes.ok) announcements.value = (await annRes.json()).announcements || []
    if (evRes.ok) events.value = (await evRes.json()).events || []
  } finally {
    loading.value = false
  }
}

const openAnnouncement = async (id) => {
  const res = await fetch(`/api/announcements/${id}/`)
  if (res.ok) {
    selected.value = await res.json()
    // registrar vista
    fetch(`/api/announcements/${id}/view/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': getCsrf() }
    }).catch(() => {})
  }
}

const createAnnouncement = async () => {
  error.value = ''
  const res = await fetch('/api/announcements/create/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    body: JSON.stringify(form.value)
  })
  const data = await res.json()
  if (res.ok) {
    createOpen.value = false
    form.value = { title: '', content: '', announcement_type: 'off_rp', min_access_level: 'L1' }
    await fetchAll()
  } else {
    error.value = data.error || 'Error al publicar'
  }
}

onMounted(fetchAll)
</script>

<style scoped>
.feed-page {
  min-height: 100vh;
  background: #0a0a0f;
  color: #d8d8e0;
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  position: relative;
}
.site-background { position: fixed; inset: 0; pointer-events: none; }
.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(170, 34, 34, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(170, 34, 34, 0.05) 1px, transparent 1px);
  background-size: 40px 40px;
}
.page-header {
  position: relative;
  text-align: center;
  padding: 100px 20px 20px;
  border-bottom: 1px solid #2a2a35;
}
.page-title { font-size: 2rem; letter-spacing: 6px; margin: 0; color: #e8e8f0; }
.page-subtitle { color: #aa2222; letter-spacing: 3px; font-size: 0.8rem; margin-top: 6px; }
.page-content {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 20px 80px;
}
.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  align-items: center;
}
.tab {
  background: transparent;
  border: 1px solid #2a2a35;
  color: #888;
  padding: 8px 18px;
  border-radius: 4px;
  cursor: pointer;
  font-family: inherit;
  font-size: 0.75rem;
  letter-spacing: 1px;
}
.tab.active { border-color: #aa2222; color: #e8e8f0; background: rgba(170, 34, 34, 0.15); }
.create-btn { margin-left: auto; }
.btn {
  border: 1px solid #aa2222;
  background: transparent;
  color: #e8e8f0;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-family: inherit;
  letter-spacing: 1px;
  font-size: 0.75rem;
}
.btn:hover { background: rgba(170, 34, 34, 0.2); }
.btn-primary { background: #aa2222; }
.btn-ghost { border-color: #444; color: #999; }
.feed-list { display: flex; flex-direction: column; gap: 12px; }
.feed-item {
  background: #12121a;
  border: 1px solid #2a2a35;
  border-radius: 4px;
  padding: 14px 18px;
  cursor: pointer;
  transition: border-color 0.2s;
}
.feed-item:hover { border-color: #aa2222; }
.feed-item.pinned { border-left: 3px solid #ffb300; }
.event-item { cursor: default; border-left: 3px solid #3498db; }
.feed-item-header {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 6px;
}
.type-chip {
  font-size: 0.65rem;
  padding: 2px 8px;
  border-radius: 3px;
  border: 1px solid #555;
  letter-spacing: 1px;
}
.t-in_rp { color: #2ecc71; border-color: #2ecc71; }
.t-off_rp { color: #3498db; border-color: #3498db; }
.t-automatic { color: #95a5a6; border-color: #95a5a6; }
.t-critical { color: #e74c3c; border-color: #e74c3c; }
.level-chip {
  color: #ffb300;
  border: 1px solid #ffb300;
  padding: 1px 8px;
  border-radius: 3px;
  font-size: 0.65rem;
}
.pin-chip { font-size: 0.65rem; color: #ffb300; }
.feed-date { margin-left: auto; color: #555; font-size: 0.7rem; }
.feed-title { color: #e8e8f0; font-size: 0.95rem; }
.feed-author { color: #666; font-size: 0.75rem; margin-top: 4px; }
.feed-body { color: #999; font-size: 0.85rem; margin-top: 4px; }
.announcement-content {
  background: #0a0a0f;
  border: 1px solid #2a2a35;
  padding: 16px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: inherit;
  font-size: 0.85rem;
  color: #c8c8d0;
}
input, select, textarea {
  background: #12121a;
  border: 1px solid #2a2a35;
  color: #d8d8e0;
  padding: 10px 12px;
  border-radius: 4px;
  font-family: inherit;
  width: 100%;
  box-sizing: border-box;
}
.loading-text, .empty-text {
  color: #666;
  text-align: center;
  padding: 30px;
  letter-spacing: 2px;
  font-size: 0.85rem;
}
.error-text { color: #e74c3c; font-size: 0.8rem; }
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.modal {
  background: #12121a;
  border: 1px solid #aa2222;
  border-radius: 6px;
  padding: 24px;
  width: min(560px, 92vw);
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 85vh;
  overflow-y: auto;
}
.modal h3 { margin: 0; letter-spacing: 2px; color: #e8e8f0; }
.edit-actions { display: flex; gap: 10px; }

</style>
