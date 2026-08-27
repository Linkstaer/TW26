<template>
  <div class="docs-page">
    <div class="site-background"><div class="grid-overlay"></div></div>

    <div class="page-header">
      <h1 class="page-title">DOCUMENTACIÓN</h1>
      <div class="page-subtitle">ARCHIVO INTERNO DEL SITIO</div>
    </div>

    <main class="page-content">
      <!-- Detalle -->
      <div v-if="selectedDoc" class="doc-detail">
        <div class="detail-toolbar">
          <button class="btn btn-ghost" @click="closeDoc">← VOLVER</button>
          <div class="detail-actions" v-if="selectedDoc.can_edit">
            <button v-if="!editing" class="btn btn-tiny" @click="startEdit">EDITAR</button>
            <button class="btn btn-tiny" @click="toggleHistory">
              {{ showHistory ? 'OCULTAR HISTORIAL' : 'HISTORIAL' }}
            </button>
          </div>
        </div>

        <div class="doc-meta">
          <span class="level-chip">{{ selectedDoc.min_access_level }}</span>
          <span class="doc-type">{{ typeLabel(selectedDoc.doc_type) }}</span>
          <span class="doc-author" v-if="selectedDoc.author">
            Autor: {{ selectedDoc.author }}
            <template v-if="selectedDoc.author_faction"> ({{ selectedDoc.author_faction }})</template>
          </span>
          <span class="doc-date" v-if="selectedDoc.updated_at">
            Última edición: {{ formatDateTime(selectedDoc.updated_at) }}
          </span>
        </div>
        <h2 class="doc-title">{{ selectedDoc.title }}</h2>

        <pre v-if="!editing" class="doc-content">{{ selectedDoc.content }}</pre>
        <div v-else class="edit-area">
          <textarea v-model="editContent" rows="18"></textarea>
          <input v-model="editSummary" placeholder="Resumen del cambio (opcional)" />
          <div class="edit-actions">
            <button class="btn btn-primary" @click="saveDoc">GUARDAR CAMBIOS</button>
            <button class="btn btn-ghost" @click="cancelEdit">CANCELAR</button>
          </div>
          <div v-if="error" class="error-text">{{ error }}</div>
        </div>

        <!-- Versionado del documento -->
        <div v-if="showHistory" class="history-section">
          <div class="history-title">HISTORIAL DE EDICIONES</div>
          <div v-if="historyLoading" class="loading-text">RECUPERANDO REGISTROS...</div>
          <div v-else-if="!history.length" class="empty-text">Sin ediciones registradas.</div>
          <div v-for="entry in history" :key="entry.id" class="history-item">
            <span class="doc-date">{{ formatDateTime(entry.created_at) }}</span>
            <span class="doc-author">{{ entry.edited_by || 'desconocido' }}</span>
            <span class="history-summary" v-if="entry.edit_summary">
              {{ entry.edit_summary }}
            </span>
          </div>
        </div>
      </div>

      <!-- Listado -->
      <div v-else>
        <div class="toolbar">
          <input v-model="search" class="search-input" placeholder="Buscar documento..." />
          <button v-if="showCreate === null || showCreate" class="btn btn-primary" @click="createOpen = true">
            + NUEVO DOCUMENTO
          </button>
        </div>

        <div v-if="loading" class="loading-text">CARGANDO ARCHIVO...</div>
        <div v-else-if="filteredDocs.length === 0" class="empty-text">
          No hay documentos visibles para su nivel de acceso.
        </div>

        <div class="doc-list">
          <div v-for="doc in filteredDocs" :key="doc.id" class="doc-row" @click="openDoc(doc.slug)">
            <span class="level-chip">{{ doc.min_access_level }}</span>
            <span class="doc-row-title">{{ doc.title }}</span>
            <span class="doc-type">{{ typeLabel(doc.doc_type) }}</span>
            <span class="doc-date">{{ formatDate(doc.created_at) }}</span>
          </div>
        </div>
      </div>

      <!-- Modal crear -->
      <div v-if="createOpen" class="modal-overlay" @click.self="createOpen = false">
        <div class="modal">
          <h3>NUEVO DOCUMENTO</h3>
          <input v-model="form.title" placeholder="Título" />
          <select v-model="form.doc_type">
            <option value="procedure">Procedimiento</option>
            <option value="memo">Memo</option>
            <option value="briefing">Briefing</option>
            <option value="regulation">Reglamento</option>
            <option value="other">Otro</option>
          </select>
          <select v-model="form.min_access_level">
            <option v-for="l in ['L1','L2','L3','L4','L5','L6']" :key="l" :value="l">
              Nivel mínimo: {{ l }}
            </option>
          </select>
          <textarea v-model="form.content" rows="10" placeholder="Contenido (Markdown)"></textarea>
          <div class="edit-actions">
            <button class="btn btn-primary" @click="createDoc">PUBLICAR</button>
            <button class="btn btn-ghost" @click="createOpen = false">CANCELAR</button>
          </div>
          <div v-if="error" class="error-text">{{ error }}</div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const docs = ref([])
const selectedDoc = ref(null)
const search = ref('')
const loading = ref(true)
const error = ref('')
const createOpen = ref(false)
const showCreate = ref(true) // el backend valida los permisos reales
const form = ref({ title: '', doc_type: 'other', min_access_level: 'L1', content: '' })

// Edición e historial (spec §5.2 / §5.3)
const editing = ref(false)
const editContent = ref('')
const editSummary = ref('')
const showHistory = ref(false)
const history = ref([])
const historyLoading = ref(false)

const TYPE_LABELS = {
  procedure: 'Procedimiento',
  memo: 'Memo',
  briefing: 'Briefing',
  regulation: 'Reglamento',
  other: 'Otro',
}
const typeLabel = (t) => TYPE_LABELS[t] || t

const getCsrf = () => {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1] || ''
}

const formatDate = (iso) => (iso ? new Date(iso).toLocaleDateString('es-ES') : '')
const formatDateTime = (iso) =>
  iso
    ? new Date(iso).toLocaleString('es-ES', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
      })
    : ''

const filteredDocs = computed(() => {
  const q = search.value.toLowerCase()
  if (!q) return docs.value
  return docs.value.filter(d => d.title.toLowerCase().includes(q))
})

const fetchDocs = async () => {
  loading.value = true
  try {
    const res = await fetch('/api/documents/')
    if (res.ok) {
      const data = await res.json()
      docs.value = data.documents || []
    }
  } finally {
    loading.value = false
  }
}

const openDoc = async (slug) => {
  const res = await fetch(`/api/documents/${slug}/`)
  if (res.ok) {
    selectedDoc.value = await res.json()
    editing.value = false
    showHistory.value = false
    history.value = []
    error.value = ''
  }
}

const closeDoc = () => {
  selectedDoc.value = null
  editing.value = false
  showHistory.value = false
}

const startEdit = () => {
  editContent.value = selectedDoc.value.content
  editSummary.value = ''
  error.value = ''
  editing.value = true
}

const cancelEdit = () => {
  editing.value = false
  error.value = ''
}

const saveDoc = async () => {
  error.value = ''
  const res = await fetch(`/api/documents/${selectedDoc.value.slug}/edit/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    body: JSON.stringify({ content: editContent.value, summary: editSummary.value })
  })
  const data = await res.json()
  if (res.ok) {
    // Recargar en vez de parchear en memoria: así el updated_at y el
    // historial quedan alineados con lo que guardó el backend.
    await openDoc(selectedDoc.value.slug)
    await fetchDocs()
  } else {
    error.value = data.error || 'Error al guardar'
  }
}

const toggleHistory = async () => {
  showHistory.value = !showHistory.value
  if (!showHistory.value || history.value.length) return

  historyLoading.value = true
  try {
    const res = await fetch(`/api/documents/${selectedDoc.value.slug}/history/`)
    if (res.ok) history.value = (await res.json()).history || []
  } finally {
    historyLoading.value = false
  }
}

const createDoc = async () => {
  error.value = ''
  const res = await fetch('/api/documents/create/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    body: JSON.stringify(form.value)
  })
  const data = await res.json()
  if (res.ok) {
    createOpen.value = false
    form.value = { title: '', doc_type: 'other', min_access_level: 'L1', content: '' }
    await fetchDocs()
  } else {
    error.value = data.error || 'Error al publicar'
  }
}

onMounted(fetchDocs)
</script>

<style scoped>
.docs-page {
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
  max-width: 900px;
  margin: 0 auto;
  padding: 24px 20px 80px;
}
.toolbar { display: flex; gap: 12px; margin-bottom: 20px; }
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
.search-input { flex: 1; }
.btn {
  border: 1px solid #aa2222;
  background: transparent;
  color: #e8e8f0;
  padding: 10px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-family: inherit;
  letter-spacing: 1px;
  font-size: 0.8rem;
}
.btn:hover { background: rgba(170, 34, 34, 0.2); }
.btn-primary { background: #aa2222; }
.btn-ghost { border-color: #444; color: #999; }
.doc-list { display: flex; flex-direction: column; gap: 8px; }
.doc-row {
  display: flex;
  align-items: center;
  gap: 14px;
  background: #12121a;
  border: 1px solid #2a2a35;
  border-radius: 4px;
  padding: 12px 16px;
  cursor: pointer;
  transition: border-color 0.2s;
}
.doc-row:hover { border-color: #aa2222; }
.doc-row-title { flex: 1; color: #e8e8f0; }
.level-chip {
  color: #ffb300;
  border: 1px solid #ffb300;
  padding: 1px 8px;
  border-radius: 3px;
  font-size: 0.7rem;
}
.doc-type { color: #888; font-size: 0.75rem; letter-spacing: 1px; }
.doc-date { color: #555; font-size: 0.75rem; }
.doc-meta {
  display: flex;
  gap: 14px;
  align-items: center;
  margin: 20px 0 10px;
}
.doc-author { color: #888; font-size: 0.8rem; }
.doc-title { color: #e8e8f0; letter-spacing: 1px; }
.doc-content {
  background: #12121a;
  border: 1px solid #2a2a35;
  padding: 20px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: inherit;
  font-size: 0.9rem;
  color: #c8c8d0;
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
}
.modal h3 { margin: 0 0 6px; letter-spacing: 2px; color: #e8e8f0; }
.edit-actions { display: flex; gap: 10px; }

.detail-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.detail-actions { display: flex; gap: 8px; }
.btn-tiny {
  padding: 5px 12px;
  font-size: 0.7rem;
  letter-spacing: 1px;
}
.edit-area {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 12px;
}
.history-section {
  margin-top: 28px;
  padding-top: 14px;
  border-top: 1px solid #2a2a35;
}
.history-title {
  color: #aa2222;
  letter-spacing: 2px;
  font-size: 0.75rem;
  margin-bottom: 10px;
}
.history-item {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: baseline;
  padding: 8px 4px;
  border-bottom: 1px solid #16161e;
  font-size: 0.82rem;
}
.history-summary { color: #c8c8d0; flex: 1 1 220px; }

</style>
