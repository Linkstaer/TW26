<template>
  <div class="leader-panel">
    <!-- Site Background -->
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
    </div>

    <!-- Header -->
    <div class="panel-header">
      <div class="header-left">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="#aa2222" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            <path d="M12 8v4M12 16h.01"></path>
          </svg>
        </div>
        <div class="header-title">
          <span class="title-main">PANEL DE CONTROL FACCIONARIO</span>
          <span class="title-sub">GESTIÓN DE FACCIÓN</span>
        </div>
      </div>
      <div class="header-right">
        <div class="session-status">
          <div class="session-indicator active"></div>
          <span class="session-text">ADMIN ACTIVE</span>
        </div>
        <div class="current-time">{{ currentTime }}</div>
        <button class="back-floating-btn" @click="$router.push('/dashboard/factions')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"></path>
          </svg>
          VOLVER
        </button>
      </div>
    </div>

    <!-- Navegación -->
    <nav class="panel-nav">
      <button class="nav-btn" :class="{ active: activeTab === 'members' }" @click="activeTab = 'members'">
        MIEMBROS
      </button>
      <button 
        v-if="selectedFaction?.allow_applications" 
        class="nav-btn" 
        :class="{ active: activeTab === 'applications' }" 
        @click="activeTab = 'applications'"
      >
        SOLICITUDES
      </button>
      <button class="nav-btn" :class="{ active: activeTab === 'ranks' }" @click="activeTab = 'ranks'">
        RANGOS
      </button>
      <button class="nav-btn" :class="{ active: activeTab === 'divisions' }" @click="activeTab = 'divisions'">
        DIVISIONES
      </button>
      <button class="nav-btn" :class="{ active: activeTab === 'invite' }" @click="activeTab = 'invite'">
        INVITAR
      </button>
    </nav>

    <!-- Main Panel Content -->
    <div class="panel-content">
      <!-- Members Tab -->
      <div v-if="activeTab === 'members'" class="tab-panel">
        <div class="panel-toolbar">
          <input v-model="memberSearch" placeholder="Buscar miembro..." class="search-input" />
          <span class="member-count">{{ filteredMembers.length }} MIEMBROS</span>
        </div>

        <div v-if="loading" class="loading-state">
          <div class="loader"></div>
        </div>

        <div v-else-if="filteredMembers.length === 0" class="empty-panel">
          <p>NO HAY MIEMBROS REGISTRADOS</p>
        </div>

        <div v-else class="members-by-bracket">
          <!-- Low Rank (1-25) -->
          <div v-if="membersByBracket.low.length > 0" class="bracket-section">
            <div class="bracket-header">
              <span class="bracket-title">BAJO RANGO (1-25)</span>
              <span class="bracket-count">{{ membersByBracket.low.length }} MIEMBROS</span>
            </div>
            <div class="members-table">
              <div class="table-header">
                <span class="col-name">NOMBRE</span>
                <span class="col-rank">RANGO</span>
                <span class="col-card">TARJETA</span>
                <span class="col-actions">ACCIONES</span>
              </div>
              <div v-for="member in membersByBracket.low" :key="member.id" class="table-row">
                <span class="col-name">{{ member.character_name }}</span>
                <span class="col-rank">
                  <select v-model="member.rank_id" @change="updateMemberRank(member)" class="rank-select">
                    <option v-for="rank in ranks" :key="rank.id" :value="rank.id">
                      {{ rank.name }} (Nvl {{ rank.level }})
                    </option>
                  </select>
                </span>
                <span class="col-card">{{ member.access_card || 'L1' }}</span>
                <span class="col-actions">
                  <button class="action-btn expel" @click="expelMember(member)">EXPULSAR</button>
                </span>
              </div>
            </div>
          </div>

          <!-- Mid Rank (26-50) -->
          <div v-if="membersByBracket.mid.length > 0" class="bracket-section">
            <div class="bracket-header">
              <span class="bracket-title">MEDIO RANGO (26-50)</span>
              <span class="bracket-count">{{ membersByBracket.mid.length }} MIEMBROS</span>
            </div>
            <div class="members-table">
              <div class="table-header">
                <span class="col-name">NOMBRE</span>
                <span class="col-rank">RANGO</span>
                <span class="col-card">TARJETA</span>
                <span class="col-actions">ACCIONES</span>
              </div>
              <div v-for="member in membersByBracket.mid" :key="member.id" class="table-row">
                <span class="col-name">{{ member.character_name }}</span>
                <span class="col-rank">
                  <select v-model="member.rank_id" @change="updateMemberRank(member)" class="rank-select">
                    <option v-for="rank in ranks" :key="rank.id" :value="rank.id">
                      {{ rank.name }} (Nvl {{ rank.level }})
                    </option>
                  </select>
                </span>
                <span class="col-card">{{ member.access_card || 'L1' }}</span>
                <span class="col-actions">
                  <button class="action-btn expel" @click="expelMember(member)">EXPULSAR</button>
                </span>
              </div>
            </div>
          </div>

          <!-- High Rank (51-75) -->
          <div v-if="membersByBracket.high.length > 0" class="bracket-section">
            <div class="bracket-header">
              <span class="bracket-title">ALTO RANGO (51-75)</span>
              <span class="bracket-count">{{ membersByBracket.high.length }} MIEMBROS</span>
            </div>
            <div class="members-table">
              <div class="table-header">
                <span class="col-name">NOMBRE</span>
                <span class="col-rank">RANGO</span>
                <span class="col-card">TARJETA</span>
                <span class="col-actions">ACCIONES</span>
              </div>
              <div v-for="member in membersByBracket.high" :key="member.id" class="table-row">
                <span class="col-name">{{ member.character_name }}</span>
                <span class="col-rank">
                  <select v-model="member.rank_id" @change="updateMemberRank(member)" class="rank-select">
                    <option v-for="rank in ranks" :key="rank.id" :value="rank.id">
                      {{ rank.name }} (Nvl {{ rank.level }})
                    </option>
                  </select>
                </span>
                <span class="col-card">{{ member.access_card || 'L1' }}</span>
                <span class="col-actions">
                  <button class="action-btn expel" @click="expelMember(member)">EXPULSAR</button>
                </span>
              </div>
            </div>
          </div>

          <!-- High Command (76-100) -->
          <div v-if="membersByBracket.command.length > 0" class="bracket-section">
            <div class="bracket-header">
              <span class="bracket-title">ALTO MANDO (76-100)</span>
              <span class="bracket-count">{{ membersByBracket.command.length }} MIEMBROS</span>
            </div>
            <div class="members-table">
              <div class="table-header">
                <span class="col-name">NOMBRE</span>
                <span class="col-rank">RANGO</span>
                <span class="col-card">TARJETA</span>
                <span class="col-actions">ACCIONES</span>
              </div>
              <div v-for="member in membersByBracket.command" :key="member.id" class="table-row">
                <span class="col-name">{{ member.character_name }}</span>
                <span class="col-rank">
                  <select v-model="member.rank_id" @change="updateMemberRank(member)" class="rank-select">
                    <option v-for="rank in ranks" :key="rank.id" :value="rank.id">
                      {{ rank.name }} (Nvl {{ rank.level }})
                    </option>
                  </select>
                </span>
                <span class="col-card">{{ member.access_card || 'L1' }}</span>
                <span class="col-actions">
                  <button class="action-btn expel" @click="expelMember(member)">EXPULSAR</button>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Applications Tab -->
      <div v-if="activeTab === 'applications'" class="tab-panel">
        <div v-if="applications.length === 0" class="empty-panel">
          <p>NO HAY SOLICITUDES PENDIENTES</p>
        </div>

        <div v-else class="applications-list">
          <div v-for="app in applications" :key="app.id" class="application-card">
            <div class="app-header">
              <span class="app-character">{{ app.character_name }}</span>
              <span class="app-date">{{ app.created_at }}</span>
            </div>
            <div class="app-body">
              <p class="app-message">{{ app.message || 'Sin mensaje' }}</p>
            </div>
            <div class="app-actions">
              <button class="action-btn accept" @click="acceptApplication(app.id)">ACEPTAR</button>
              <button class="action-btn reject" @click="rejectApplication(app.id)">RECHAZAR</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Ranks Tab -->
      <div v-if="activeTab === 'ranks'" class="tab-panel">
        <div class="panel-toolbar">
          <button class="create-btn" @click="showCreateRankModal = true">+ CREAR RANGO</button>
        </div>

        <div class="ranks-hierarchy">
          <div v-for="rank in sortedRanks" :key="rank.id" class="rank-card">
            <div class="rank-header">
              <span class="rank-name">{{ rank.name }}</span>
              <span class="rank-level" :class="getBracketClass(rank.level)">NIVEL {{ rank.level }} - {{ getBracketDisplay(rank.level) }}</span>
            </div>
            <div class="rank-perms">
              <span v-if="rank.can_manage_members" class="perm-tag">GESTOR</span>
              <span v-if="rank.can_review_applications" class="perm-tag">REVISOR</span>
              <span v-if="rank.can_assign_ranks" class="perm-tag">ASIGNADOR</span>
              <span v-if="rank.access_card" class="perm-card">{{ rank.access_card.level }}</span>
            </div>
            <div class="rank-actions">
              <button class="action-btn edit" @click="editRank(rank)">EDITAR</button>
              <button v-if="rank.name !== 'Líder' && rank.name !== 'Recluta'" class="action-btn delete" @click="deleteRank(rank)">ELIMINAR</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Divisions Tab -->
      <div v-if="activeTab === 'divisions'" class="tab-panel">
        <div class="panel-toolbar">
          <button class="create-btn" @click="showCreateDivisionModal = true" :disabled="divisions.length >= 5">
            + CREAR DIVISIÓN ({{ divisions.length }}/5)
          </button>
        </div>

        <div v-if="divisions.length === 0" class="empty-panel">
          <p>NO HAY DIVISIONES CREADAS</p>
        </div>

        <div v-else class="divisions-list">
          <div v-for="div in divisions" :key="div.id" class="division-card">
            <div class="division-header">
              <span class="division-name">{{ div.name }}</span>
              <span class="division-badge" :class="div.is_public ? 'public' : 'private'">
                {{ div.is_public ? 'PÚBLICA' : 'PRIVADA' }}
              </span>
            </div>
            <p v-if="div.description" class="division-desc">{{ div.description }}</p>
            
            <div class="division-members">
              <span class="members-title">MIEMBROS ({{ div.members.length }}):</span>
              <div v-if="div.members.length > 0" class="member-tags">
                <span v-for="member in div.members" :key="member.id" class="member-tag">
                  {{ member.character_name }}
                  <button class="remove-member" @click="removeFromDivision(div, member)">&times;</button>
                </span>
              </div>
              <button class="add-member-btn" @click="showAddMemberToDivision(div)">
                + AGREGAR MIEMBRO
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Invite Tab -->
      <div v-if="activeTab === 'invite'" class="tab-panel">
        <div class="invite-section">
          <div class="form-group">
            <label>BUSCAR USUARIO:</label>
            <input v-model="inviteSearch" @input="searchUsers" placeholder="Escribe username o ID..." class="search-input" />
          </div>

          <div v-if="inviteResults.length > 0" class="search-results">
            <div v-for="user in inviteResults" :key="user.id" class="result-item" @click="selectUserToInvite(user)">
              <span class="result-name">{{ user.roblox_username }}</span>
              <span class="result-id">ID: {{ user.roblox_id }}</span>
            </div>
          </div>

          <div v-if="selectedInviteUser" class="invite-confirm">
            <p>Invitar a: <strong>{{ selectedInviteUser.roblox_username }}</strong></p>
            <button class="action-btn send" @click="sendInvitation">ENVIAR INVITACIÓN</button>
          </div>
        </div>

        <div class="pending-invites">
          <h3>INVITACIONES PENDIENTES</h3>
          <div v-for="inv in invitations" :key="inv.id" class="invite-card">
            <span class="inv-user">{{ inv.user_name }}</span>
            <span class="inv-status">{{ inv.status }}</span>
            <span class="inv-date">{{ inv.created_at }}</span>
            <button class="action-btn cancel" @click="cancelInvitation(inv.id)">CANCELAR</button>
          </div>
          <div v-if="invitations.length === 0" class="empty-panel">
            <p>NO HAY INVITACIONES PENDIENTES</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Rank Modal -->
    <div v-if="showCreateRankModal" class="modal-overlay" @click="showCreateRankModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>CREAR RANGO</h2>
          <button class="close-btn" @click="showCreateRankModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Nombre del rango:</label>
            <input v-model="newRank.name" placeholder="Ej: Cabo, Sargento, etc." />
          </div>
          <div class="form-group">
            <label>Nivel jerárquico:</label>
            <input type="number" v-model="newRank.level" min="1" max="99" />
            <small class="form-help">1 = más bajo, 100 = más alto</small>
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="newRank.can_manage_members" />
              Puede gestionar miembros
            </label>
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="newRank.can_review_applications" />
              Puede revisar solicitudes
            </label>
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="newRank.can_assign_ranks" />
              Puede asignar rangos
            </label>
          </div>
          <div class="form-info">
            <p>Las tarjetas de acceso son gestionadas exclusivamente por administradores desde el panel de moderación.</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showCreateRankModal = false">CANCELAR</button>
          <button class="save-btn" @click="createRank">CREAR</button>
        </div>
      </div>
    </div>

    <!-- Create Division Modal -->
    <div v-if="showCreateDivisionModal" class="modal-overlay" @click="showCreateDivisionModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>CREAR DIVISIÓN</h2>
          <button class="close-btn" @click="showCreateDivisionModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Nombre de la división:</label>
            <input v-model="newDivision.name" placeholder="Ej: Alpha, Bravo, Charlie..." />
          </div>
          <div class="form-group">
            <label>Descripción:</label>
            <textarea v-model="newDivision.description" rows="2" placeholder="Descripción opcional..."></textarea>
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="newDivision.is_public" />
              División pública (visible para todos los miembros)
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showCreateDivisionModal = false">CANCELAR</button>
          <button class="save-btn" @click="createDivision">CREAR</button>
        </div>
      </div>
    </div>

    <!-- Add Member to Division Modal -->
    <div v-if="showAddMemberModal" class="modal-overlay" @click="showAddMemberModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>AGREGAR A {{ selectedDivisionForMember?.name }}</h2>
          <button class="close-btn" @click="showAddMemberModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <p class="modal-info">Selecciona un personaje para agregar a la división:</p>
          <div class="member-select-list">
            <div v-for="member in membersNotInDivision" :key="member.id" class="member-select-item" @click="addMemberToDivision(member.character_id)">
              {{ member.character_name }}
            </div>
            <div v-if="membersNotInDivision.length === 0" class="empty-panel">
              <p>No hay miembros disponibles</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Back Button -->
    <button class="back-floating-btn" @click="$router.push('/dashboard/factions')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M19 12H5M12 19l-7-7 7-7"></path>
      </svg>
      VOLVER
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const selectedFactionId = ref('')
const selectedFaction = ref(null)
const activeTab = ref('members')
const loading = ref(false)
const currentTime = ref('')

const members = ref([])
const applications = ref([])
const ranks = ref([])
const accessCards = ref([])
const availableCharacters = ref([])

const memberSearch = ref('')
const showCreateRankModal = ref(false)

const inviteSearch = ref('')
const inviteResults = ref([])
const selectedInviteUser = ref(null)
const invitations = ref([])

const divisions = ref([])
const showCreateDivisionModal = ref(false)
const selectedDivisionForMember = ref(null)
const showAddMemberModal = ref(false)

const newDivision = ref({
  name: '',
  description: '',
  is_public: true
})

const getBracketDisplay = (level) => {
  if (level <= 25) return 'LOW RANK'
  if (level <= 50) return 'MID RANK'
  if (level <= 75) return 'HIGH RANK'
  return 'HIGH COMMAND'
}

const getBracketClass = (level) => {
  if (level <= 25) return 'low'
  if (level <= 50) return 'mid'
  if (level <= 75) return 'high'
  return 'command'
}

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('en-US', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
  }).replace(/(\d+)\/(\d+)\/(\d+),/, '$3-$1-$2')
}

const sortedRanks = computed(() => {
  return [...ranks.value].sort((a, b) => b.level - a.level)
})

const filteredMembers = computed(() => {
  if (!memberSearch.value) return members.value
  const search = memberSearch.value.toLowerCase()
  return members.value.filter(m => m.character_name.toLowerCase().includes(search))
})

const membersNotInDivision = computed(() => {
  if (!selectedDivisionForMember.value) return members.value
  const memberIdsInDivision = selectedDivisionForMember.value.members?.map(m => m.character_id) || []
  return members.value.filter(m => !memberIdsInDivision.includes(m.character_id))
})

const membersByBracket = computed(() => {
  const getBracket = (level) => {
    if (level <= 25) return 'low'
    if (level <= 50) return 'mid'
    if (level <= 75) return 'high'
    return 'command'
  }
  
  const brackets = { low: [], mid: [], high: [], command: [] }
  filteredMembers.value.forEach(m => {
    const level = m.rank_level || 1
    brackets[getBracket(level)].push(m)
  })
  return brackets
})

const fetchAccessCards = async () => {
  try {
    const response = await fetch('/api/cards/')
    if (response.ok) {
      const data = await response.json()
      accessCards.value = data.cards || []
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const loadFactionData = async () => {
  if (!selectedFactionId.value) return
  loading.value = true
  try {
    // Obtener detalles de la facción
    const factionRes = await fetch(`/api/factions/${selectedFactionId.value}/`)
    if (factionRes.ok) {
      selectedFaction.value = await factionRes.json()
    }

    const [membersRes, appsRes, ranksRes, divisionsRes, invitesRes] = await Promise.all([
      fetch(`/api/factions/${selectedFactionId.value}/members/`),
      fetch(`/api/faction-dashboard/${selectedFactionId.value}/applications/`),
      fetch(`/api/factions/${selectedFactionId.value}/ranks/`),
      fetch(`/api/faction-dashboard/${selectedFactionId.value}/divisions/`),
      fetch(`/api/factions/${selectedFactionId.value}/invitations/`)
    ])

    if (membersRes.ok) {
      const data = await membersRes.json()
      members.value = data.members || []
    }
    if (appsRes.ok) {
      const data = await appsRes.json()
      applications.value = data.applications || []
    }
    if (ranksRes.ok) {
      const data = await ranksRes.json()
      ranks.value = data.ranks || []
    }
    if (divisionsRes.ok) {
      const data = await divisionsRes.json()
      divisions.value = data.divisions || []
    }
    if (invitesRes.ok) {
      const data = await invitesRes.json()
      invitations.value = data.invitations || []
    }
  } catch (err) {
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}

const updateMemberRank = async (member) => {
  try {
    const response = await fetch(`/api/faction-dashboard/${selectedFactionId.value}/members/${member.id}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rank_id: member.rank_id })
    })
    if (response.ok) {
      alert('Rango actualizado')
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const expelMember = async (member) => {
  if (!confirm(`¿Expulsar a ${member.character_name}?`)) return
  try {
    const response = await fetch(`/api/faction-dashboard/${selectedFactionId.value}/members/${member.id}/`, {
      method: 'DELETE'
    })
    if (response.ok) {
      await loadFactionData()
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const acceptApplication = async (appId) => {
  try {
    const response = await fetch(`/api/faction-dashboard/${selectedFactionId.value}/applications/${appId}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'accept' })
    })
    if (response.ok) {
      await loadFactionData()
      alert('Solicitud aceptada')
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const rejectApplication = async (appId) => {
  try {
    const response = await fetch(`/api/faction-dashboard/${selectedFactionId.value}/applications/${appId}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'reject' })
    })
    if (response.ok) {
      await loadFactionData()
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const createRank = async () => {
  try {
    const response = await fetch(`/api/factions/${selectedFactionId.value}/ranks/create/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newRank.value)
    })
    if (response.ok) {
      showCreateRankModal.value = false
      await loadFactionData()
      newRank.value = { name: '', level: 10, access_card_id: '', can_manage_members: false, can_review_applications: false, can_assign_ranks: false }
      alert('Rango creado')
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const editRank = (rank) => {
  alert('Edición de rangos en desarrollo')
}

const deleteRank = async (rank) => {
  if (!confirm(`¿Eliminar rango ${rank.name}?`)) return
  alert('Eliminación de rangos en desarrollo')
}

let searchTimeout = null
const searchUsers = () => {
  clearTimeout(searchTimeout)
  if (inviteSearch.value.length < 2) {
    inviteResults.value = []
    return
  }
  searchTimeout = setTimeout(async () => {
    try {
      const response = await fetch(`/api/moderation/users/search/${inviteSearch.value}/`)
      if (response.ok) {
        const data = await response.json()
        inviteResults.value = data.results || []
      }
    } catch (err) {
      console.error('Error:', err)
    }
  }, 300)
}

const selectUserToInvite = (user) => {
  selectedInviteUser.value = user
  inviteSearch.value = ''
  inviteResults.value = []
}

const sendInvitation = async () => {
  if (!selectedInviteUser.value) return
  try {
    const response = await fetch(`/api/factions/${selectedFactionId.value}/invite/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: selectedInviteUser.value.id })
    })
    if (response.ok) {
      selectedInviteUser.value = null
      alert('Invitación enviada')
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const cancelInvitation = async (invId) => {
  if (!confirm('¿Cancelar esta invitación?')) return
  try {
    const response = await fetch(`/api/factions/invitations/${invId}/cancel/`, {
      method: 'POST'
    })
    if (response.ok) {
      await loadFactionData()
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const createDivision = async () => {
  if (divisions.value.length >= 5) {
    alert('Máximo de 5 divisiones permitidas')
    return
  }
  try {
    const response = await fetch(`/api/faction-dashboard/${selectedFactionId.value}/divisions/create/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newDivision.value)
    })
    if (response.ok) {
      showCreateDivisionModal.value = false
      newDivision.value = { name: '', description: '', is_public: true }
      await loadFactionData()
      alert('División creada')
    } else {
      const data = await response.json()
      alert(data.error || 'Error al crear')
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const showAddMemberToDivision = (div) => {
  selectedDivisionForMember.value = div
  showAddMemberModal.value = true
}

const addMemberToDivision = async (characterId) => {
  try {
    const response = await fetch(`/api/faction-dashboard/${selectedFactionId.value}/divisions/${selectedDivisionForMember.value.id}/add-member/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ character_id: characterId })
    })
    if (response.ok) {
      showAddMemberModal.value = false
      await loadFactionData()
      alert('Miembro agregado')
    } else {
      const data = await response.json()
      alert(data.error || 'Error al agregar')
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

const removeFromDivision = async (div, member) => {
  alert('Funcionalidad en desarrollo')
}

onMounted(async () => {
  updateTime()
  setInterval(updateTime, 1000)
  await fetchAccessCards()

  const factionId = route.params.id
  if (factionId) {
    selectedFactionId.value = factionId
    await loadFactionData()
  }
})
</script>

<style scoped>
.leader-panel {
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
  background: linear-gradient(90deg, transparent, rgba(170, 34, 34, 0.8), rgba(170, 34, 34, 0.9) 50%, rgba(170, 34, 34, 0.8) 90%, transparent 100%);
  animation: scan 6s linear infinite;
}

@keyframes scan {
  0% { top: 0%; }
  100% { top: 100%; }
}

.panel-header {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: rgba(15, 15, 15, 0.95);
  border-bottom: 1px solid #333;
  margin-bottom: 0;
}

.panel-nav {
  display: flex;
  gap: 5px;
  padding: 0 1.5rem;
  background: rgba(20, 20, 20, 0.95);
  border-bottom: 1px solid #333;
  margin-bottom: 20px;
}

.nav-btn {
  padding: 14px 20px;
  background: transparent;
  border: none;
  color: #888;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.2s;
}

.nav-btn:hover {
  color: #aaa;
  background: rgba(40, 40, 40, 0.5);
}

.nav-btn.active {
  color: #aa2222;
  border-bottom-color: #aa2222;
  background: rgba(170, 34, 34, 0.1);
}

.header-left {
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

.title-main {
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: 1px;
}

.title-sub {
  font-size: 0.7rem;
  color: #888;
  letter-spacing: 0.5px;
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
  box-shadow: 0 0 6px #4CAF50;
}

.session-indicator.active {
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

.faction-selector-section {
  position: relative;
  z-index: 2;
  margin-bottom: 30px;
}

.selector-header {
  margin-bottom: 10px;
}

.selector-label {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.faction-select {
  width: 100%;
  max-width: 400px;
  padding: 12px 16px;
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  color: #fff;
  font-size: 0.9rem;
  cursor: pointer;
}

.faction-select:focus {
  border-color: #aa2222;
  outline: none;
}

.empty-state {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
}

.empty-icon svg {
  width: 100%;
  height: 100%;
}

.empty-text {
  font-size: 1rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.panel-content {
  position: relative;
  z-index: 2;
}

.tabs-container {
  display: flex;
  gap: 5px;
  margin-bottom: 20px;
  border-bottom: 1px solid #333;
}

.tab-btn {
  padding: 12px 24px;
  background: transparent;
  border: none;
  color: #888;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tab-btn.active {
  color: #aa2222;
  border-bottom-color: #aa2222;
}

.tab-panel {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  padding: 20px;
}

.panel-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-input {
  padding: 10px 16px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  color: #fff;
  width: 250px;
}

.member-count {
  font-size: 0.8rem;
  color: #888;
}

.loading-state {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.loader {
  width: 40px;
  height: 40px;
  border: 3px solid #333;
  border-top-color: #aa2222;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-panel {
  text-align: center;
  padding: 40px;
  color: #666;
}

.members-table {
  display: flex;
  flex-direction: column;
}

.members-by-bracket {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.bracket-section {
  background: rgba(20, 20, 20, 0.5);
  border: 1px solid #333;
  border-radius: 4px;
  overflow: hidden;
}

.bracket-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: rgba(40, 40, 40, 0.8);
  border-bottom: 1px solid #333;
}

.bracket-title {
  font-size: 0.8rem;
  font-weight: 700;
  color: #aaa;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.bracket-count {
  font-size: 0.7rem;
  color: #666;
}

.bracket-section:first-child .bracket-header {
  border-left: 3px solid #4a9;
}

.bracket-section:nth-child(2) .bracket-header {
  border-left: 3px solid #49a;
}

.bracket-section:nth-child(3) .bracket-header {
  border-left: 3px solid #a49;
}

.bracket-section:nth-child(4) .bracket-header {
  border-left: 3px solid #a44;
}

.table-header, .table-row {
  display: grid;
  grid-template-columns: 2fr 1.5fr 1fr 1fr;
  gap: 10px;
  padding: 12px;
  align-items: center;
}

.table-header {
  background: rgba(30, 30, 30, 0.8);
  border-bottom: 1px solid #444;
  font-size: 0.75rem;
  color: #888;
  text-transform: uppercase;
}

.table-row {
  border-bottom: 1px solid #333;
}

.table-row:hover {
  background: rgba(40, 40, 40, 0.5);
}

.col-name {
  font-weight: 600;
  color: #fff;
}

.rank-select {
  padding: 6px 10px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  color: #fff;
  font-size: 0.8rem;
}

.col-card {
  color: #fc6f03;
  font-size: 0.85rem;
}

.action-btn {
  padding: 6px 12px;
  background: transparent;
  border: 1px solid #444;
  color: #aaa;
  cursor: pointer;
  font-size: 0.7rem;
  text-transform: uppercase;
}

.action-btn:hover {
  background: rgba(170, 34, 34, 0.1);
  border-color: #aa2222;
  color: #aa2222;
}

.action-btn.expel:hover {
  background: rgba(170, 34, 34, 0.2);
  border-color: #aa2222;
  color: #aa2222;
}

.action-btn.accept {
  background: rgba(76, 175, 80, 0.1);
  border-color: rgba(76, 175, 80, 0.3);
  color: #4CAF50;
}

.action-btn.reject {
  background: rgba(170, 34, 34, 0.1);
  border-color: rgba(170, 34, 34, 0.3);
  color: #aa2222;
}

.action-btn.send {
  background: rgba(170, 34, 34, 0.1);
  border-color: rgba(170, 34, 34, 0.3);
  color: #aa2222;
}

.action-btn.cancel {
  background: rgba(170, 34, 34, 0.1);
  border-color: rgba(170, 34, 34, 0.3);
  color: #aa2222;
}

.action-btn.delete {
  border-color: rgba(170, 34, 34, 0.5);
  color: #aa2222;
}

.applications-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.application-card {
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #333;
  padding: 15px;
}

.app-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.app-character {
  font-weight: 600;
  color: #fff;
}

.app-date {
  color: #666;
  font-size: 0.8rem;
}

.app-message {
  color: #aaa;
  margin: 10px 0;
}

.app-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.create-btn {
  padding: 10px 20px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  cursor: pointer;
  font-size: 0.8rem;
}

.ranks-hierarchy {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.rank-card {
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #333;
  padding: 15px;
}

.rank-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.rank-name {
  font-weight: 600;
  color: #fff;
}

.rank-level {
  color: #aa2222;
  font-size: 0.85rem;
}

.rank-level.low {
  color: #888;
}

.rank-level.mid {
  color: #fc6f03;
}

.rank-level.high {
  color: #aa2222;
}

.rank-level.command {
  color: #ff4444;
}

.rank-perms {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.perm-tag {
  padding: 3px 8px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
  font-size: 0.7rem;
}

.perm-card {
  padding: 3px 8px;
  background: rgba(252, 111, 3, 0.1);
  border: 1px solid rgba(252, 111, 3, 0.3);
  color: #fc6f03;
  font-size: 0.7rem;
}

.rank-actions {
  display: flex;
  gap: 10px;
}

.invite-section {
  margin-bottom: 30px;
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

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  color: #fff;
  box-sizing: border-box;
}

.form-help {
  display: block;
  margin-top: 5px;
  color: #666;
  font-size: 0.7rem;
}

.form-info {
  margin-top: 15px;
  padding: 12px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
}

.form-info p {
  margin: 0;
  color: #888;
  font-size: 0.75rem;
}

.checkbox-label {
  display: flex !important;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.search-results {
  margin-top: 10px;
  background: rgba(30, 30, 30, 0.98);
  border: 1px solid #444;
}

.result-item {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #333;
}

.result-item:hover {
  background: rgba(170, 34, 34, 0.2);
}

.result-name {
  display: block;
  color: #fff;
}

.result-id {
  font-size: 0.75rem;
  color: #666;
}

.invite-confirm {
  margin-top: 15px;
  padding: 15px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
}

.pending-invites h3 {
  font-size: 0.9rem;
  color: #fff;
  margin-bottom: 15px;
}

.invite-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #333;
  margin-bottom: 10px;
}

.inv-user {
  color: #fff;
}

.inv-date {
  color: #666;
  font-size: 0.8rem;
}

/* Modal */
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

/* Divisions Tab */
.divisions-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.division-card {
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #333;
  padding: 15px;
}

.division-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.division-name {
  font-weight: 700;
  color: #fff;
  font-size: 1rem;
}

.division-badge {
  padding: 3px 10px;
  font-size: 0.7rem;
  text-transform: uppercase;
}

.division-badge.public {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  color: #4CAF50;
}

.division-badge.private {
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  color: #aa2222;
}

.division-desc {
  color: #888;
  font-size: 0.85rem;
  margin: 10px 0;
}

.division-members {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #333;
}

.members-title {
  display: block;
  font-size: 0.75rem;
  color: #666;
  margin-bottom: 10px;
}

.member-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.member-tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 10px;
  background: rgba(100, 100, 100, 0.1);
  border: 1px solid rgba(100, 100, 100, 0.3);
  color: #fff;
  font-size: 0.75rem;
}

.remove-member {
  background: none;
  border: none;
  color: #aa2222;
  cursor: pointer;
  padding: 0 2px;
  font-size: 1rem;
}

.add-member-btn {
  padding: 8px 16px;
  background: rgba(252, 111, 3, 0.1);
  border: 1px solid rgba(252, 111, 3, 0.3);
  color: #fc6f03;
  cursor: pointer;
  font-size: 0.75rem;
}

.add-member-btn:hover {
  background: rgba(252, 111, 3, 0.2);
}

.modal-info {
  color: #888;
  margin-bottom: 15px;
}

.member-select-list {
  max-height: 300px;
  overflow-y: auto;
}

.member-select-item {
  padding: 12px;
  cursor: pointer;
  border-bottom: 1px solid #333;
}

.member-select-item:hover {
  background: rgba(170, 34, 34, 0.2);
}

/* Back Button */
.back-floating-btn {
  position: fixed;
  bottom: 30px;
  left: 30px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  color: #aaa;
  cursor: pointer;
  font-size: 0.8rem;
  z-index: 100;
}

.back-floating-btn svg {
  width: 16px;
  height: 16px;
}

.back-floating-btn:hover {
  border-color: #aa2222;
  color: #aa2222;
}
</style>
