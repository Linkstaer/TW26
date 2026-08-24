<template>
  <div class="lore-page">
    <div class="site-background"><div class="grid-overlay"></div></div>

    <div class="page-header">
      <h1 class="page-title">SUGERENCIAS DE LORE</h1>
      <div class="page-subtitle">PROGRAMA EXCLUSIVO PARA BOOSTERS</div>
    </div>

    <main class="page-content">
      <div v-if="loading" class="loading-text">CARGANDO...</div>

      <template v-else>
        <div v-if="!isBooster && !isReviewer" class="locked-panel">
          <div class="locked-icon">🔒</div>
          <p>Este programa está reservado para Boosters del servidor.</p>
          <p class="locked-sub">Conviértete en Booster para proponer ideas de lore al equipo de roleplay.</p>
        </div>

        <template v-else>
          <div class="toolbar" v-if="isBooster">
            <button class="btn btn-primary" @click="createOpen = true">+ NUEVA SUGERENCIA</button>
          </div>

          <div v-if="suggestions.length === 0" class="empty-text">
            {{ isReviewer ? 'No hay sugerencias enviadas.' : 'Aún no enviaste sugerencias.' }}
          </div>

          <div class="suggestion-list">
            <div v-for="sg in suggestions" :key="sg.id" class="suggestion-card">
              <div class="suggestion-header">
                <span class="status-chip" :class="'s-' + sg.status">{{ statusLabel(sg.status) }}</span>
                <strong class="suggestion-title">{{ sg.title }}</strong>
                <span class="suggestion-author" v-if="isReviewer">por {{ sg.author }}</span>
                <span class="suggestion-date">{{ formatDate(sg.created_at) }}</span>
              </div>
              <pre class="suggestion-content">{{ sg.content }}</pre>
              <div v-if="sg.review_notes" class="review-notes">
                <strong>Respuesta del equipo{{ sg.reviewed_by ? ` (${sg.reviewed_by})` : '' }}:</strong>
                {{ sg.review_notes }}
              </div>
              <div v-if="isReviewer && sg.status === 'pending'" class="review-actions">
                <input v-model="reviewNotes[sg.id]" placeholder="Notas de revisión (opcional)" />
                <button class="btn btn-approve" @click="review(sg.id, 'approve')">APROBAR</button>
                <button class="btn btn-reject" @click="review(sg.id, 'reject')">RECHAZAR</button>
              </div>
            </div>
          </div>
        </template>
      </template>

      <!-- Modal crear -->
      <div v-if="createOpen" class="modal-overlay" @click.self="createOpen = false">
        <div class="modal">
          <h3>NUEVA SUGERENCIA DE LORE</h3>
          <input v-model="form.title" placeholder="Título de la propuesta" />
          <textarea v-model="form.content" rows="8" placeholder="Describe tu idea de lore..."></textarea>
          <div class="edit-actions">
            <button class="btn btn-primary" @click="create">ENVIAR</button>
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

const suggestions = ref([])
const isBooster = ref(false)
const isReviewer = ref(false)
const loading = ref(true)
const createOpen = ref(false)
const error = ref('')
const form = ref({ title: '', content: '' })
const reviewNotes = ref({})

const STATUS_LABELS = { pending: 'PENDIENTE', approved: 'APROBADA', rejected: 'RECHAZADA' }
const statusLabel = (s) => STATUS_LABELS[s] || s

const getCsrf = () => {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1] || ''
}

const formatDate = (iso) => (iso ? new Date(iso).toLocaleDateString('es-ES') : '')

const fetchSuggestions = async () => {
  loading.value = true
  try {
    const res = await fetch('/api/lore/suggestions/')
    if (res.ok) {
      const data = await res.json()
      suggestions.value = data.suggestions || []
      isBooster.value = !!data.is_booster
      isReviewer.value = !!data.is_reviewer
    }
  } finally {
    loading.value = false
  }
}

const create = async () => {
  error.value = ''
  const res = await fetch('/api/lore/suggestions/create/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    body: JSON.stringify(form.value)
  })
  const data = await res.json()
  if (res.ok) {
    createOpen.value = false
    form.value = { title: '', content: '' }
    await fetchSuggestions()
  } else {
    error.value = data.error || 'Error al enviar'
  }
}

const review = async (id, action) => {
  const res = await fetch(`/api/lore/suggestions/${id}/review/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    body: JSON.stringify({ action, notes: reviewNotes.value[id] || '' })
  })
  if (res.ok) await fetchSuggestions()
}

onMounted(fetchSuggestions)
</script>

<style scoped>
.lore-page {
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
.page-subtitle { color: #9b59b6; letter-spacing: 3px; font-size: 0.8rem; margin-top: 6px; }
.page-content {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 20px 80px;
}
.toolbar { display: flex; justify-content: flex-end; margin-bottom: 20px; }
.locked-panel {
  text-align: center;
  padding: 60px 20px;
  border: 1px dashed #2a2a35;
  border-radius: 6px;
  color: #888;
}
.locked-icon { font-size: 2.4rem; margin-bottom: 12px; }
.locked-sub { color: #555; font-size: 0.85rem; }
.suggestion-list { display: flex; flex-direction: column; gap: 14px; }
.suggestion-card {
  background: #12121a;
  border: 1px solid #2a2a35;
  border-radius: 4px;
  padding: 16px 18px;
}
.suggestion-header {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
}
.suggestion-title { color: #e8e8f0; }
.suggestion-author { color: #888; font-size: 0.75rem; }
.suggestion-date { margin-left: auto; color: #555; font-size: 0.7rem; }
.status-chip {
  font-size: 0.65rem;
  padding: 2px 8px;
  border-radius: 3px;
  border: 1px solid;
  letter-spacing: 1px;
}
.s-pending { color: #f1c40f; border-color: #f1c40f; }
.s-approved { color: #2ecc71; border-color: #2ecc71; }
.s-rejected { color: #e74c3c; border-color: #e74c3c; }
.suggestion-content {
  white-space: pre-wrap;
  word-break: break-word;
  font-family: inherit;
  font-size: 0.85rem;
  color: #b8b8c0;
  margin: 0;
}
.review-notes {
  margin-top: 10px;
  padding: 10px 12px;
  background: rgba(155, 89, 182, 0.08);
  border-left: 3px solid #9b59b6;
  font-size: 0.8rem;
  color: #aaa;
}
.review-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}
.review-actions input { flex: 1; }
input, textarea {
  background: #0a0a0f;
  border: 1px solid #2a2a35;
  color: #d8d8e0;
  padding: 9px 12px;
  border-radius: 4px;
  font-family: inherit;
  box-sizing: border-box;
  width: 100%;
}
.btn {
  border: 1px solid #aa2222;
  background: transparent;
  color: #e8e8f0;
  padding: 9px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-family: inherit;
  letter-spacing: 1px;
  font-size: 0.75rem;
  white-space: nowrap;
}
.btn:hover { background: rgba(170, 34, 34, 0.2); }
.btn-primary { background: #aa2222; }
.btn-ghost { border-color: #444; color: #999; }
.btn-approve { border-color: #2ecc71; color: #2ecc71; }
.btn-approve:hover { background: rgba(46, 204, 113, 0.15); }
.btn-reject { border-color: #e74c3c; color: #e74c3c; }
.btn-reject:hover { background: rgba(231, 76, 60, 0.15); }
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
  border: 1px solid #9b59b6;
  border-radius: 6px;
  padding: 24px;
  width: min(560px, 92vw);
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.modal h3 { margin: 0; letter-spacing: 2px; color: #e8e8f0; }
.edit-actions { display: flex; gap: 10px; }

</style>
