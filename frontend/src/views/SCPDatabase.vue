<template>
  <div class="scp-page">
    <div class="site-background">
      <div class="grid-overlay"></div>
    </div>

    <div class="page-header">
      <h1 class="page-title">SCP DATABASE</h1>
      <div class="page-subtitle">SECURE · CONTAIN · PROTECT</div>
      <div class="access-banner" v-if="accessLevels.length">
        NIVEL DE ACREDITACIÓN: <span class="level-chip">{{ accessLevels[accessLevels.length - 1] }}</span>
      </div>
    </div>

    <main class="page-content">
      <!-- Listado -->
      <div v-if="!selectedScp" class="scp-list-panel">
        <div class="toolbar">
          <input
            v-model="search"
            class="search-input"
            placeholder="Buscar por ID o título..."
          />
          <button v-if="canCreate" class="btn btn-primary" @click="showCreateModal = true">
            + NUEVO ARCHIVO
          </button>
        </div>

        <div v-if="loading" class="loading-text">ACCEDIENDO A LA BASE DE DATOS...</div>
        <div v-else-if="filteredScps.length === 0" class="empty-text">
          No hay archivos SCP registrados.
        </div>

        <div class="scp-grid">
          <div
            v-for="scp in filteredScps"
            :key="scp.id"
            class="scp-card"
            @click="openScp(scp.id)"
          >
            <div class="scp-card-header">
              <span class="scp-id">{{ scp.scp_id }}</span>
              <span class="object-class" :class="'oc-' + scp.object_class">
                {{ scp.object_class.toUpperCase() }}
              </span>
            </div>
            <div class="scp-title">{{ scp.title }}</div>
          </div>
        </div>
      </div>

      <!-- Detalle -->
      <div v-else class="scp-detail-panel">
        <button class="btn btn-ghost" @click="selectedScp = null">← VOLVER AL ÍNDICE</button>

        <div class="detail-header">
          <h2 class="detail-id">{{ selectedScp.scp_id }}</h2>
          <span class="object-class" :class="'oc-' + selectedScp.object_class">
            CLASE: {{ selectedScp.object_class.toUpperCase() }}
          </span>
        </div>
        <h3 class="detail-title">{{ selectedScp.title }}</h3>

        <div
          v-for="level in ['L1', 'L2', 'L3', 'L4', 'L5', 'L6']"
          :key="level"
          class="section-block"
        >
          <template v-if="selectedScp['content_' + level.toLowerCase()] !== undefined">
            <div class="section-header">
              <span class="section-level">[{{ level }}]</span>
              <button
                v-if="selectedScp.can_edit"
                class="btn btn-tiny"
                @click="startEdit(level)"
              >
                EDITAR
              </button>
            </div>
            <pre
              v-if="editingSection !== level"
              class="section-content"
            >{{ selectedScp['content_' + level.toLowerCase()] || '[Sin contenido registrado]' }}</pre>
            <div v-else class="edit-area">
              <textarea v-model="editContent" rows="8"></textarea>
              <div class="edit-actions">
                <button class="btn btn-primary" @click="saveSection(level)">GUARDAR</button>
                <button class="btn btn-ghost" @click="editingSection = null">CANCELAR</button>
              </div>
            </div>
          </template>
          <div v-else class="section-redacted">
            <span class="section-level">[{{ level }}]</span>
            <span class="redacted-label">■■■■■■■■ ACCESO DENEGADO ■■■■■■■■</span>
          </div>
        </div>

        <!-- Apéndices -->
        <div class="appendix-section">
          <div class="section-header">
            <span class="section-level">APÉNDICES</span>
            <button
              v-if="selectedScp.can_add_appendix"
              class="btn btn-tiny"
              @click="showAppendixForm = !showAppendixForm"
            >
              + AGREGAR
            </button>
          </div>
          <div v-if="showAppendixForm" class="edit-area">
            <input v-model="appendixForm.title" placeholder="Título del apéndice" />
            <select v-model="appendixForm.level">
              <option v-for="l in accessLevels" :key="l" :value="l">Nivel {{ l }}</option>
            </select>
            <textarea v-model="appendixForm.content" rows="4" placeholder="Contenido (Markdown)"></textarea>
            <div class="edit-actions">
              <button class="btn btn-primary" @click="addAppendix">GUARDAR APÉNDICE</button>
            </div>
          </div>
          <div
            v-for="(app, i) in selectedScp.appendices"
            :key="i"
            class="appendix-item"
          >
            <div class="appendix-header">
              <span class="section-level">[{{ app.level }}]</span>
              <strong>{{ app.title }}</strong>
              <span class="appendix-author" v-if="app.author">— {{ app.author }}</span>
            </div>
            <pre class="section-content">{{ app.content }}</pre>
          </div>
          <div v-if="!selectedScp.appendices?.length && !showAppendixForm" class="empty-text">
            Sin apéndices registrados.
          </div>
        </div>
      </div>

      <!-- Modal crear SCP -->
      <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
        <div class="modal">
          <h3>NUEVO ARCHIVO SCP</h3>
          <input v-model="createForm.scp_id" placeholder="ID (ej: SCP-2995)" />
          <input v-model="createForm.title" placeholder="Título" />
          <select v-model="createForm.object_class">
            <option value="safe">Safe</option>
            <option value="euclid">Euclid</option>
            <option value="keter">Keter</option>
            <option value="thaumiel">Thaumiel</option>
            <option value="neutralized">Neutralized</option>
            <option value="apollyon">Apollyon</option>
            <option value="archon">Archon</option>
          </select>
          <textarea v-model="createForm.content_l1" rows="5" placeholder="Contenido L1 (Markdown)"></textarea>
          <div class="edit-actions">
            <button class="btn btn-primary" @click="createScp">CREAR</button>
            <button class="btn btn-ghost" @click="showCreateModal = false">CANCELAR</button>
          </div>
          <div v-if="error" class="error-text">{{ error }}</div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const scps = ref([])
const selectedScp = ref(null)
const search = ref('')
const loading = ref(true)
const error = ref('')
const accessLevels = ref([])
const canCreate = ref(false)

const editingSection = ref(null)
const editContent = ref('')
const showAppendixForm = ref(false)
const appendixForm = ref({ title: '', content: '', level: 'L1' })
const showCreateModal = ref(false)
const createForm = ref({ scp_id: '', title: '', object_class: 'euclid', content_l1: '' })

const getCsrf = () => {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1] || ''
}

const filteredScps = computed(() => {
  const q = search.value.toLowerCase()
  if (!q) return scps.value
  return scps.value.filter(
    s => s.scp_id.toLowerCase().includes(q) || s.title.toLowerCase().includes(q)
  )
})

const fetchScps = async () => {
  loading.value = true
  try {
    const res = await fetch('/api/scps/')
    if (res.ok) {
      const data = await res.json()
      scps.value = data.scps || []
    }
  } finally {
    loading.value = false
  }
}

const fetchUserAccess = async () => {
  try {
    const res = await fetch('/api/auth/user/')
    const user = await res.json()
    canCreate.value = !!user.is_superuser
  } catch { /* noop */ }
}

const openScp = async (id) => {
  const res = await fetch(`/api/scps/${id}/`)
  if (res.ok) {
    selectedScp.value = await res.json()
    accessLevels.value = selectedScp.value.accessible_levels || ['L1']
    editingSection.value = null
    showAppendixForm.value = false
  }
}

const startEdit = (level) => {
  editingSection.value = level
  editContent.value = selectedScp.value['content_' + level.toLowerCase()] || ''
}

const saveSection = async (level) => {
  const res = await fetch(`/api/scps/${selectedScp.value.id}/edit/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    body: JSON.stringify({ section: level, content: editContent.value })
  })
  const data = await res.json()
  if (res.ok) {
    await openScp(selectedScp.value.id)
  } else {
    error.value = data.error || 'Error al guardar'
  }
}

const addAppendix = async () => {
  const res = await fetch(`/api/scps/${selectedScp.value.id}/appendix/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    body: JSON.stringify(appendixForm.value)
  })
  if (res.ok) {
    appendixForm.value = { title: '', content: '', level: 'L1' }
    showAppendixForm.value = false
    await openScp(selectedScp.value.id)
  }
}

const createScp = async () => {
  error.value = ''
  const res = await fetch('/api/scps/create/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
    body: JSON.stringify(createForm.value)
  })
  const data = await res.json()
  if (res.ok) {
    showCreateModal.value = false
    createForm.value = { scp_id: '', title: '', object_class: 'euclid', content_l1: '' }
    await fetchScps()
  } else {
    error.value = data.error || 'Error al crear'
  }
}

onMounted(() => {
  fetchScps()
  fetchUserAccess()
})
</script>

<style scoped>
.scp-page {
  min-height: 100vh;
  background: #0a0a0f;
  color: #d8d8e0;
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  position: relative;
}
.site-background {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}
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
  z-index: 1;
  text-align: center;
  padding: 100px 20px 20px;
  border-bottom: 1px solid #2a2a35;
}
.page-title {
  font-size: 2rem;
  letter-spacing: 6px;
  color: #e8e8f0;
  margin: 0;
}
.page-subtitle {
  color: #aa2222;
  letter-spacing: 3px;
  font-size: 0.8rem;
  margin-top: 6px;
}
.access-banner {
  margin-top: 12px;
  font-size: 0.75rem;
  color: #888;
}
.level-chip {
  color: #ffb300;
  border: 1px solid #ffb300;
  padding: 1px 8px;
  border-radius: 3px;
}
.page-content {
  position: relative;
  z-index: 1;
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px 20px 80px;
}
.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}
.search-input,
input,
select,
textarea {
  background: #12121a;
  border: 1px solid #2a2a35;
  color: #d8d8e0;
  padding: 10px 12px;
  border-radius: 4px;
  font-family: inherit;
  width: 100%;
  box-sizing: border-box;
}
.search-input {
  flex: 1;
}
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
.btn:hover {
  background: rgba(170, 34, 34, 0.2);
}
.btn-primary {
  background: #aa2222;
}
.btn-ghost {
  border-color: #444;
  color: #999;
}
.btn-tiny {
  padding: 3px 10px;
  font-size: 0.7rem;
}
.scp-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}
.scp-card {
  background: #12121a;
  border: 1px solid #2a2a35;
  border-left: 3px solid #aa2222;
  padding: 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: border-color 0.2s, transform 0.15s;
}
.scp-card:hover {
  border-color: #aa2222;
  transform: translateY(-2px);
}
.scp-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.scp-id {
  font-weight: bold;
  color: #e8e8f0;
  letter-spacing: 1px;
}
.object-class {
  font-size: 0.65rem;
  padding: 2px 8px;
  border-radius: 3px;
  border: 1px solid #555;
  letter-spacing: 1px;
}
.oc-safe { color: #2ecc71; border-color: #2ecc71; }
.oc-euclid { color: #f1c40f; border-color: #f1c40f; }
.oc-keter { color: #e74c3c; border-color: #e74c3c; }
.oc-thaumiel { color: #3498db; border-color: #3498db; }
.oc-apollyon { color: #9b59b6; border-color: #9b59b6; }
.oc-neutralized { color: #7f8c8d; border-color: #7f8c8d; }
.oc-archon { color: #1abc9c; border-color: #1abc9c; }
.scp-title {
  color: #999;
  font-size: 0.85rem;
}
.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
}
.detail-id {
  font-size: 1.6rem;
  letter-spacing: 3px;
  margin: 0;
  color: #e8e8f0;
}
.detail-title {
  color: #aaa;
  font-weight: normal;
  margin: 8px 0 24px;
}
.section-block,
.appendix-section {
  margin-bottom: 22px;
}
.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}
.section-level {
  color: #ffb300;
  font-size: 0.8rem;
  letter-spacing: 1px;
}
.section-content {
  background: #12121a;
  border: 1px solid #2a2a35;
  padding: 14px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: inherit;
  font-size: 0.85rem;
  color: #c8c8d0;
  margin: 0;
}
.section-redacted {
  display: flex;
  gap: 12px;
  align-items: center;
  background: rgba(170, 34, 34, 0.06);
  border: 1px dashed #442222;
  padding: 12px 14px;
  border-radius: 4px;
}
.redacted-label {
  color: #663333;
  font-size: 0.8rem;
  letter-spacing: 2px;
}
.edit-area {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 12px;
}
.edit-actions {
  display: flex;
  gap: 10px;
}
.appendix-item {
  margin-bottom: 14px;
}
.appendix-header {
  display: flex;
  gap: 10px;
  align-items: baseline;
  margin-bottom: 4px;
}
.appendix-author {
  color: #666;
  font-size: 0.75rem;
}
.loading-text,
.empty-text {
  color: #666;
  text-align: center;
  padding: 30px;
  letter-spacing: 2px;
  font-size: 0.85rem;
}
.error-text {
  color: #e74c3c;
  font-size: 0.8rem;
}
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
  width: min(520px, 92vw);
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.modal h3 {
  margin: 0 0 6px;
  letter-spacing: 2px;
  color: #e8e8f0;
}

</style>
