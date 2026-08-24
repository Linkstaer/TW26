<template>
  <div class="terminal-page">
    <div class="terminal-window">
      <div class="terminal-titlebar">
        <span class="titlebar-text">RAISA QUERY TERMINAL v3.1 — SITE-81 "TWILIGHT"</span>
        <div class="mode-switch" v-if="canTechnical">
          <button class="mode-btn" :class="{ active: mode === 'rp' }" @click="mode = 'rp'">RP</button>
          <button class="mode-btn" :class="{ active: mode === 'technical' }" @click="mode = 'technical'">TÉCNICO</button>
        </div>
      </div>

      <div class="terminal-body" ref="terminalBody">
        <div class="boot-text">
          <p>&gt; INICIALIZANDO TERMINAL DE CONSULTA...</p>
          <p>&gt; CONEXIÓN SEGURA ESTABLECIDA.</p>
          <p>&gt; ACREDITACIÓN VERIFICADA: <span class="highlight">{{ cardDisplay || 'VERIFICANDO...' }}</span></p>
          <p>&gt; Las consultas quedan registradas conforme al protocolo RAISA-7.</p>
          <p>&gt; Escriba su consulta y presione ENTER.</p>
          <p class="separator">═══════════════════════════════════════════</p>
        </div>

        <div v-for="(entry, i) in history" :key="i" class="terminal-entry">
          <div class="query-line">
            <span class="prompt">&gt;&gt;</span> {{ entry.query }}
          </div>
          <pre class="response-line">{{ entry.response }}</pre>
        </div>

        <div v-if="waiting" class="terminal-entry">
          <div class="query-line"><span class="prompt">&gt;&gt;</span> {{ pendingQuery }}</div>
          <div class="response-line blink">PROCESANDO CONSULTA{{ dots }}</div>
        </div>
      </div>

      <div class="terminal-input-row">
        <span class="prompt">&gt;&gt;</span>
        <input
          v-model="query"
          class="terminal-input"
          :disabled="waiting"
          placeholder="Consulta a la base de datos..."
          @keydown.enter="submit"
          autofocus
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onUnmounted } from 'vue'

const query = ref('')
const pendingQuery = ref('')
const history = ref([])
const waiting = ref(false)
const mode = ref('rp')
const canTechnical = ref(false)
const cardDisplay = ref('')
const terminalBody = ref(null)
const dots = ref('')
let dotsTimer = null

const getCsrf = () => {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1] || ''
}

const scrollToBottom = async () => {
  await nextTick()
  if (terminalBody.value) {
    terminalBody.value.scrollTop = terminalBody.value.scrollHeight
  }
}

const submit = async () => {
  const q = query.value.trim()
  if (!q || waiting.value) return

  pendingQuery.value = q
  query.value = ''
  waiting.value = true
  dotsTimer = setInterval(() => {
    dots.value = dots.value.length >= 3 ? '' : dots.value + '.'
  }, 400)
  await scrollToBottom()

  try {
    const res = await fetch('/api/ai/query/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
      body: JSON.stringify({ query: q, mode: mode.value })
    })
    const data = await res.json()
    history.value.push({
      query: q,
      response: res.ok ? data.response : `[ERROR] ${data.error || 'Fallo de conexión con el núcleo.'}`
    })
    if (res.ok && data.card) cardDisplay.value = data.card
  } catch {
    history.value.push({ query: q, response: '[ERROR] Terminal fuera de línea.' })
  } finally {
    waiting.value = false
    clearInterval(dotsTimer)
    dots.value = ''
    await scrollToBottom()
  }
}

const loadInitial = async () => {
  try {
    const [userRes, histRes] = await Promise.all([
      fetch('/api/auth/user/'),
      fetch('/api/ai/history/')
    ])
    const user = await userRes.json()
    canTechnical.value = !!(user.is_staff || user.is_superuser)
    if (histRes.ok) {
      const data = await histRes.json()
      history.value = (data.history || []).map(h => ({ query: h.query, response: h.response }))
    }
  } catch { /* noop */ }
  await scrollToBottom()
}

onMounted(loadInitial)
onUnmounted(() => clearInterval(dotsTimer))
</script>

<style scoped>
.terminal-page {
  min-height: 100vh;
  background: #050508;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 100px 20px 40px;
  box-sizing: border-box;
}
.terminal-window {
  width: min(900px, 100%);
  height: 75vh;
  background: #020204;
  border: 1px solid #1a3a1a;
  border-radius: 6px;
  box-shadow: 0 0 40px rgba(30, 255, 100, 0.06), inset 0 0 80px rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: 'Consolas', monospace;
}
.terminal-titlebar {
  background: #0a140a;
  border-bottom: 1px solid #1a3a1a;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.titlebar-text {
  color: #3aff6e;
  font-size: 0.7rem;
  letter-spacing: 2px;
}
.mode-switch { display: flex; gap: 6px; }
.mode-btn {
  background: transparent;
  border: 1px solid #1a3a1a;
  color: #2a7a3a;
  font-family: inherit;
  font-size: 0.65rem;
  padding: 3px 10px;
  border-radius: 3px;
  cursor: pointer;
  letter-spacing: 1px;
}
.mode-btn.active { border-color: #3aff6e; color: #3aff6e; }
.terminal-body {
  flex: 1;
  overflow-y: auto;
  padding: 18px 20px;
  color: #35d060;
  font-size: 0.85rem;
  line-height: 1.55;
}
.boot-text p { margin: 2px 0; color: #2a9a4a; }
.separator { color: #1a3a1a !important; }
.highlight { color: #ffb300; }
.terminal-entry { margin-top: 14px; }
.query-line { color: #7adf9a; }
.prompt { color: #3aff6e; margin-right: 6px; }
.response-line {
  margin: 6px 0 0 18px;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: inherit;
  color: #35d060;
}
.blink { animation: blink 1.2s step-end infinite; }
@keyframes blink { 50% { opacity: 0.4; } }
.terminal-input-row {
  display: flex;
  align-items: center;
  gap: 4px;
  border-top: 1px solid #1a3a1a;
  padding: 12px 20px;
  background: #030306;
}
.terminal-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #7adf9a;
  font-family: inherit;
  font-size: 0.9rem;
  caret-color: #3aff6e;
}
.terminal-body::-webkit-scrollbar { width: 8px; }
.terminal-body::-webkit-scrollbar-thumb { background: #1a3a1a; border-radius: 4px; }
</style>
