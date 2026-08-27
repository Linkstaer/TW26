<template>
  <div class="mod-page">
    <div class="site-background"><div class="grid-overlay"></div></div>

    <div class="page-header">
      <h1 class="page-title">BÚSQUEDA DE PERSONAL</h1>
      <div class="page-subtitle">HERRAMIENTAS DE MODERACIÓN · SOLO LECTURA</div>
    </div>

    <main class="page-content">
      <div class="toolbar">
        <input
          v-model="search"
          class="search-input"
          placeholder="Roblox Username · Roblox User ID · Codename · Nombre del personaje"
          @input="debouncedSearch"
          @keyup.enter="runSearch"
        />
        <button class="btn btn-primary" @click="runSearch">BUSCAR</button>
      </div>

      <div class="notice">
        Moderación no puede editar personajes, tarjetas, rangos ni facciones.
        Todas las consultas quedan registradas.
      </div>

      <div v-if="denied" class="empty-text">
        No tenés permisos para consultar el registro de personal.
      </div>
      <div v-else-if="loading" class="loading-text">CONSULTANDO REGISTRO...</div>
      <div v-else-if="!results.length && searched" class="empty-text">
        Sin coincidencias para «{{ lastQuery }}».
      </div>

      <div class="result-list">
        <div
          v-for="row in results"
          :key="row.id"
          class="result-row"
          :class="{ active: detail?.id === row.id }"
          @click="openDetail(row.id)"
        >
          <div class="result-main">
            <span class="codename">{{ row.character.codename }}</span>
            <span class="real-name">{{ row.character.name }}</span>
          </div>
          <div class="result-meta">
            <span class="faction" v-if="row.character.faction">
              {{ row.character.faction.name }}
              <template v-if="row.character.faction.rank">
                · {{ row.character.faction.rank }}
              </template>
            </span>
            <span class="faction muted" v-else>Sin facción</span>
            <span class="level-chip" v-if="row.character.access_card">
              {{ row.character.access_card }}
            </span>
            <span class="actor-chip" v-if="row.character.scp_actor">
              ACTOR · {{ row.character.scp_actor.scp_id }}
            </span>
            <span class="status-chip" :class="'st-' + row.character.status">
              {{ row.character.status_display }}
            </span>
          </div>
          <div class="result-user">
            <span class="username">{{ row.user.username }}</span>
            <span class="roblox-id">#{{ row.user.id }}</span>
            <span class="warn-chip" v-if="row.user.warning_count">
              {{ row.user.warning_count }} warn(s)
            </span>
            <span class="ban-chip" v-if="row.user.is_banned">BANEADO</span>
          </div>
        </div>
      </div>

      <!-- Vista consolidada (spec §6) -->
      <div v-if="detail" class="detail-panel">
        <div class="detail-head">
          <h2>{{ detail.character.codename }}</h2>
          <button class="btn btn-ghost btn-tiny" @click="detail = null">CERRAR</button>
        </div>

        <div class="detail-grid">
          <div class="detail-field">
            <label>Nombre real</label>
            <span>{{ detail.character.name || '—' }}</span>
          </div>
          <div class="detail-field">
            <label>Estado</label>
            <span>{{ detail.character.status_display }}</span>
          </div>
          <div class="detail-field">
            <label>Facción</label>
            <span>{{ detail.character.faction?.name || 'Sin facción' }}</span>
          </div>
          <div class="detail-field">
            <label>Rango</label>
            <span>{{ detail.character.faction?.rank || '—' }}</span>
          </div>
          <div class="detail-field">
            <label>Tarjeta de acceso</label>
            <span>{{ detail.character.access_card || 'L1 — Básica' }}</span>
          </div>
          <div class="detail-field">
            <label>SCP asignado</label>
            <span v-if="detail.character.scp_actor">
              {{ detail.character.scp_actor.scp_id }} — {{ detail.character.scp_actor.title }}
            </span>
            <span v-else>—</span>
          </div>
        </div>

        <!-- Enlaces directos (spec §6) -->
        <div class="quick-links">
          <router-link class="btn btn-tiny" :to="`/users/${detail.user.id}`">
            PERFIL DE USUARIO
          </router-link>
          <router-link
            class="btn btn-tiny"
            :to="detail.character.profile_url"
          >
            FICHA DEL PERSONAJE
          </router-link>
          <router-link
            v-if="detail.character.scp_url"
            class="btn btn-tiny"
            :to="detail.character.scp_url"
          >
            ARCHIVO SCP
          </router-link>
        </div>

        <div class="detail-section">
          <h3>SOLICITUDES ACTIVAS</h3>
          <div v-if="!detail.pending_applications.length" class="empty-text small">
            Sin solicitudes pendientes.
          </div>
          <div v-for="app in detail.pending_applications" :key="app.id" class="log-item">
            <span class="log-date">{{ formatDate(app.created_at) }}</span>
            <span class="log-desc">{{ app.faction }}</span>
          </div>
        </div>

        <div class="detail-section">
          <h3>HISTORIAL DE ACCIONES</h3>
          <div v-if="!detail.history.length" class="empty-text small">
            Sin movimientos registrados.
          </div>
          <div v-for="(entry, i) in detail.history" :key="i" class="log-item">
            <span class="log-date">{{ formatDate(entry.created_at) }}</span>
            <span class="log-action">{{ entry.action_display }}</span>
            <span class="log-desc">{{ entry.faction }}</span>
            <span class="log-author" v-if="entry.performed_by">— {{ entry.performed_by }}</span>
          </div>
        </div>

        <div class="detail-section" v-if="detail.actor_logs.length">
          <h3>BITÁCORA DE ACTOR SCP</h3>
          <div v-for="(entry, i) in detail.actor_logs" :key="i" class="log-item">
            <span class="log-date">{{ formatDate(entry.created_at) }}</span>
            <span class="log-action">{{ entry.action }}</span>
            <span class="log-desc">{{ entry.description }}</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const search = ref('')
const lastQuery = ref('')
const results = ref([])
const detail = ref(null)
const loading = ref(false)
const searched = ref(false)
const denied = ref(false)
let timer = null

const formatDate = (iso) =>
  iso
    ? new Date(iso).toLocaleString('es-ES', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
      })
    : ''

const runSearch = async () => {
  const q = search.value.trim()
  if (!q) {
    results.value = []
    searched.value = false
    return
  }

  loading.value = true
  searched.value = true
  lastQuery.value = q
  detail.value = null

  try {
    const res = await fetch(`/api/moderation/characters/?search=${encodeURIComponent(q)}`)
    if (res.status === 403 || res.status === 401) {
      denied.value = true
      results.value = []
      return
    }
    denied.value = false
    if (res.ok) results.value = (await res.json()).characters || []
  } finally {
    loading.value = false
  }
}

const debouncedSearch = () => {
  // El buscador dispara en cada tecla; sin debounce son ~10 requests por palabra.
  clearTimeout(timer)
  timer = setTimeout(runSearch, 350)
}

const openDetail = async (characterId) => {
  const res = await fetch(`/api/moderation/characters/${characterId}/`)
  if (res.ok) detail.value = await res.json()
}
</script>

<style scoped>
.mod-page {
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
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px 20px 80px;
}
.toolbar { display: flex; gap: 12px; }
input {
  background: #12121a;
  border: 1px solid #2a2a35;
  color: #d8d8e0;
  padding: 10px 12px;
  border-radius: 4px;
  font-family: inherit;
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
  text-decoration: none;
  display: inline-block;
}
.btn:hover { background: rgba(170, 34, 34, 0.2); }
.btn-primary { background: #aa2222; }
.btn-ghost { border-color: #444; color: #999; }
.btn-tiny { padding: 5px 12px; font-size: 0.7rem; }
.notice {
  margin: 14px 0 20px;
  padding: 10px 14px;
  border-left: 3px solid #c9a227;
  background: rgba(201, 162, 39, 0.07);
  color: #b9b9c4;
  font-size: 0.78rem;
  line-height: 1.5;
}
.result-list { display: flex; flex-direction: column; gap: 8px; }
.result-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 18px;
  align-items: center;
  background: #12121a;
  border: 1px solid #2a2a35;
  border-radius: 4px;
  padding: 12px 16px;
  cursor: pointer;
  transition: border-color 0.2s;
}
.result-row:hover, .result-row.active { border-color: #aa2222; }
.result-main { display: flex; gap: 10px; align-items: baseline; min-width: 200px; }
.codename { color: #e8e8f0; font-weight: 600; letter-spacing: 1px; }
.real-name { color: #8a8a99; font-size: 0.82rem; }
.result-meta { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; flex: 1; }
.result-user {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-left: auto;
  font-size: 0.8rem;
}
.username { color: #c8c8d2; }
.roblox-id { color: #5a5a68; font-family: ui-monospace, Menlo, monospace; }
.faction { color: #b9b9c4; font-size: 0.82rem; }
.faction.muted { color: #5a5a68; font-style: italic; }
.level-chip {
  color: #ffb300;
  border: 1px solid #ffb300;
  padding: 1px 8px;
  border-radius: 3px;
  font-size: 0.7rem;
}
.actor-chip {
  color: #aa2222;
  border: 1px solid #aa2222;
  padding: 1px 8px;
  border-radius: 3px;
  font-size: 0.68rem;
  letter-spacing: 1px;
}
.status-chip {
  font-size: 0.68rem;
  letter-spacing: 1px;
  padding: 1px 8px;
  border-radius: 3px;
  border: 1px solid #444;
  color: #999;
}
.status-chip.st-classified { border-color: #c9a227; color: #c9a227; }
.status-chip.st-deleted { border-color: #666; color: #666; }
.warn-chip { color: #c9a227; font-size: 0.72rem; }
.ban-chip { color: #e74c3c; font-size: 0.72rem; letter-spacing: 1px; }
.detail-panel {
  margin-top: 28px;
  background: #12121a;
  border: 1px solid #aa2222;
  border-radius: 6px;
  padding: 20px 24px;
}
.detail-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.detail-head h2 { margin: 0; letter-spacing: 2px; color: #e8e8f0; }
.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
  margin: 18px 0;
}
.detail-field { display: flex; flex-direction: column; gap: 4px; }
.detail-field label {
  font-size: 0.68rem;
  letter-spacing: 1.5px;
  color: #6a6a78;
  text-transform: uppercase;
}
.detail-field span { color: #d8d8e0; font-size: 0.9rem; }
.quick-links { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.detail-section { margin-top: 20px; padding-top: 12px; border-top: 1px solid #1e1e28; }
.detail-section h3 {
  margin: 0 0 10px;
  font-size: 0.72rem;
  letter-spacing: 2px;
  color: #aa2222;
}
.log-item {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: baseline;
  padding: 7px 4px;
  border-bottom: 1px solid #16161e;
  font-size: 0.82rem;
}
.log-date {
  color: #6a6a78;
  font-family: ui-monospace, Menlo, monospace;
  font-size: 0.74rem;
  min-width: 130px;
}
.log-action { color: #aa2222; font-size: 0.74rem; letter-spacing: 1px; }
.log-desc { color: #c8c8d2; flex: 1 1 200px; }
.log-author { color: #8a8a99; font-size: 0.76rem; }
.loading-text, .empty-text {
  color: #666;
  text-align: center;
  padding: 30px;
  letter-spacing: 2px;
  font-size: 0.85rem;
}
.empty-text.small { padding: 12px; letter-spacing: 1px; font-size: 0.78rem; }
</style>
