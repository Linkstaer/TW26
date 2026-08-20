<template>
  <div class="moderacion-global-page">
    <!-- Fondo SCP -->
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
    </div>

    <!-- Header -->
    <header class="moderacion-global-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-logo">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                <circle cx="12" cy="5" r="2"></circle>
              </svg>
            </div>
            <div class="header-title">
              <span class="header-main">GLOBAL MODERATION CONTROL</span>
              <span class="header-sub">SISTEMA DE GESTIÓN DE ADVERTENCIAS Y BANEOS</span>
            </div>
          </div>
        </div>
        
        <div class="header-right">
          <div class="session-status">
            <div class="session-indicator active"></div>
            <span class="session-text">MODERACIÓN GLOBAL ACTIVA</span>
          </div>
          <div class="current-time">
            {{ currentTime }}
          </div>
          <div class="header-actions">
            <button class="back-button" @click="goToModerationPanel">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 12H5"></path>
                <path d="M12 19l-7-7 7-7"></path>
              </svg>
              <span>VOLVER AL PANEL</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Navegación -->
    <nav class="moderacion-global-nav">
      <div class="nav-controls">
        <button 
          class="nav-button" 
          :class="{ 'active': activeTab === 'warns' }"
          @click="setActiveTab('warns')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
          </div>
          <span class="nav-text">ADVERTENCIAS</span>
        </button>
        
        <button 
          class="nav-button" 
          :class="{ 'active': activeTab === 'bans' }"
          @click="setActiveTab('bans')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <span class="nav-text">BANEOS</span>
        </button>
        
        <button 
          class="nav-button" 
          :class="{ 'active': activeTab === 'appeals' }"
          @click="setActiveTab('appeals')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
              <path d="M13 8H7"></path>
              <path d="M17 12H7"></path>
            </svg>
          </div>
          <span class="nav-text">APELACIONES</span>
        </button>
        
        <button 
          class="nav-button" 
          :class="{ 'active': activeTab === 'users' }"
          @click="setActiveTab('users')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <span class="nav-text">BUSCAR USUARIO</span>
        </button>
      </div>
      
      <div class="nav-info">
        <div class="info-item">
          <span class="info-label">MODERADOR:</span>
          <span class="info-value">{{ currentUser?.roblox_username || 'INVITADO' }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">NIVEL:</span>
          <span class="info-value" :class="{
            'junior-mod': getUserPermissionLevel() === 'MOD_JUNIOR',
            'official-mod': getUserPermissionLevel() === 'MOD_OFFICIAL',
            'qualified-mod': getUserPermissionLevel() === 'MOD_QUALIFIED',
            'senior-mod': getUserPermissionLevel() === 'MOD_SENIOR',
            'admin': getUserPermissionLevel() === 'ADMIN',
            'staff': getUserPermissionLevel() === 'STAFF',
            'observador': getUserPermissionLevel() === 'OBSERVADOR'
          }">
            {{ getUserPermissionLevel() }}
          </span>
        </div>
        <div class="info-item">
          <span class="info-label">SISTEMA:</span>
          <span class="info-value operational">OPERATIVO</span>
        </div>
      </div>
    </nav>

    <!-- Contenido Principal -->
    <main class="moderacion-global-main">
      <!-- Overlay de autenticación -->
      <div v-if="!currentUser?.is_authenticated || !hasModerationPermission()" class="auth-modal-overlay">
        <Login_Required 
          :redirect-path="'/moderation/global/'"
          :user="currentUser"
          :required-permission="'access_moderation_dashboard'"
        />
      </div>
      
      <!-- Contenido autenticado -->
      <div v-else class="authenticated-content">
        <!-- Pestaña: Warns -->
        <div v-if="activeTab === 'warns'" class="warns-tab">
          <div class="tab-header">
            <h2 class="tab-title">GESTIÓN DE ADVERTENCIAS</h2>
            <div class="tab-subtitle">
              Emitir y gestionar advertencias a usuarios
              <span v-if="paginationWarns.total > 0" class="pagination-info">
                | Página {{ paginationWarns.currentPage }} de {{ paginationWarns.totalPages }} ({{ paginationWarns.total }} advertencias)
              </span>
            </div>
          </div>

          <!-- Barra de búsqueda y acciones -->
          <div class="action-bar">
            <div class="search-container">
              <div class="search-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
              <input
                v-model="searchQueryWarns"
                @input="handleSearchWarns"
                type="text"
                placeholder="Buscar por nombre de usuario, ID de Roblox, moderador o razón..."
                class="search-input"
              />
              
              <button 
                v-if="searchQueryWarns" 
                @click="clearSearchWarns"
                class="search-clear"
                title="Limpiar búsqueda"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
              
              <div class="search-info">
                <div class="search-count" v-if="totalWarns > 0">
                  {{ totalWarns }} {{ totalWarns === 1 ? 'advertencia' : 'advertencias' }} encontradas
                </div>
              </div>
            </div>
            
            <div class="action-buttons">
              <button 
                class="action-button primary"
                @click="openCreateWarnModal"
                :disabled="!canCreateWarn()"
                :title="!canCreateWarn() ? 'Requiere al menos nivel MOD_JUNIOR' : ''"
              >
                <div class="action-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                  </svg>
                </div>
                <span>NUEVA ADVERTENCIA</span>
              </button>
              
              <button 
                class="action-button secondary"
                @click="refreshWarns"
              >
                <div class="action-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 4v6h-6"></path>
                    <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
                  </svg>
                </div>
                <span>ACTUALIZAR</span>
              </button>
            </div>
          </div>

          <!-- Filtros -->
          <div class="filters-container">
            <div class="filter-group">
              <label class="filter-label">Estado:</label>
              <select v-model="warnFilter.status" class="filter-select" @change="applyFiltersWarns">
                <option value="all">Todos los estados</option>
                <option value="active">Activas</option>
                <option value="appealed">Apeladas</option>
                <option value="expired">Expiradas</option>
                <option value="removed">Eliminadas</option>
              </select>
            </div>
            
            <div class="filter-group">
              <label class="filter-label">Gravedad:</label>
              <select v-model="warnFilter.severity" class="filter-select" @change="applyFiltersWarns">
                <option value="all">Todas las gravedades</option>
                <option value="1">Baja</option>
                <option value="2">Media</option>
                <option value="3">Alta</option>
              </select>
            </div>
            
            <div class="filter-group">
              <label class="filter-label">Ordenar por:</label>
              <select v-model="warnFilter.sort" class="filter-select" @change="applyFiltersWarns">
                <option value="-created_at">Más recientes primero</option>
                <option value="created_at">Más antiguas primero</option>
                <option value="severity">Gravedad (Alta a Baja)</option>
                <option value="-severity">Gravedad (Baja a Alta)</option>
                <option value="expires_at">Expiración (próximas)</option>
              </select>
            </div>
            
            <div class="filter-group">
              <label class="filter-label">Rango de fecha:</label>
              <input 
                type="date" 
                v-model="warnFilter.startDate" 
                class="filter-date"
                @change="applyFiltersWarns"
              />
              <span class="date-separator">a</span>
              <input 
                type="date" 
                v-model="warnFilter.endDate" 
                class="filter-date"
                @change="applyFiltersWarns"
              />
            </div>
          </div>

          <!-- Tabla de Warns -->
          <div class="table-container">
            <div v-if="loadingWarns" class="loading-state">
              <div class="loading-spinner"></div>
              <p class="loading-text">Cargando advertencias...</p>
            </div>
            
            <div v-else-if="displayedWarns.length > 0" class="warns-table">
              <table class="scp-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>USUARIO</th>
                    <th>MODERADOR</th>
                    <th>RAZÓN</th>
                    <th>GRAVEDAD</th>
                    <th>ESTADO</th>
                    <th>CREADA</th>
                    <th>EXPIRA</th>
                    <th>ACCIONES</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="warn in displayedWarns" :key="warn.id" class="table-row">
                    <td class="id-cell">
                      <span class="id-badge">#{{ warn.id }}</span>
                    </td>
                    <td class="user-cell">
                      <div class="user-info">
                        <span class="username">{{ warn.target.roblox_username }}</span>
                        <span class="user-id">ID: {{ warn.target.roblox_id }}</span>
                      </div>
                    </td>
                    <td class="moderator-cell">
                      <span v-if="warn.created_by">{{ warn.created_by.roblox_username }}</span>
                      <span v-else class="unknown">Sistema</span>
                    </td>
                    <td class="reason-cell">
                      <div class="reason-text" :title="warn.reason">
                        {{ truncateText(warn.reason, 50) }}
                      </div>
                      <div v-if="warn.evidence" class="evidence-badge" title="Tiene evidencia">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                          <polyline points="14 2 14 8 20 8"></polyline>
                          <line x1="16" y1="13" x2="8" y2="13"></line>
                          <line x1="16" y1="17" x2="8" y2="17"></line>
                          <polyline points="10 9 9 9 8 9"></polyline>
                        </svg>
                      </div>
                    </td>
                    <td class="severity-cell">
                      <span class="severity-badge" :class="`severity-${warn.severity}`">
                        {{ getSeverityText(warn.severity) }}
                      </span>
                    </td>
                    <td class="status-cell">
                      <span class="status-badge" :class="`status-${warn.status}`">
                        {{ getStatusText(warn.status) }}
                      </span>
                      <div v-if="warn.appealed" class="appealed-indicator" title="Apelada">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                        </svg>
                      </div>
                    </td>
                    <td class="date-cell">
                      {{ formatDateShort(warn.created_at) }}
                    </td>
                    <td class="date-cell">
                      <span v-if="warn.expires_at" :class="{ 'expiring-soon': isExpiringSoon(warn.expires_at) }">
                        {{ formatDateShort(warn.expires_at) }}
                      </span>
                      <span v-else class="no-expiry">Nunca</span>
                    </td>
                    <td class="actions-cell">
                      <button class="table-action view" @click="viewWarnDetails(warn)" title="Ver Detalles">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                          <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                      </button>
                      <button 
                        v-if="canManageWarns() && warn.status === 'active'"
                        class="table-action edit" 
                        @click="editWarn(warn)"
                        title="Editar Advertencia"
                        :disabled="!canManageWarns()"
                        :title="!canManageWarns() ? 'Requiere nivel MOD_QUALIFIED o superior' : ''"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                      </button>
                      <button 
                        v-if="canManageWarns() && warn.status === 'active' && !warn.appealed"
                        class="table-action remove" 
                        @click="removeWarn(warn)"
                        title="Eliminar Advertencia"
                        :disabled="!canManageWarns()"
                        :title="!canManageWarns() ? 'Requiere nivel MOD_QUALIFIED o superior' : ''"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <polyline points="3 6 5 6 21 6"></polyline>
                          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div v-else class="empty-state">
              <div class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
              </div>
              <h3 class="empty-title">No se encontraron advertencias</h3>
              <p class="empty-text" v-if="searchQueryWarns">
                No hay advertencias que coincidan con tu búsqueda
              </p>
              <p class="empty-text" v-else>
                No se han emitido advertencias aún
              </p>
            </div>

            <!-- Paginación -->
            <div v-if="paginationWarns.totalPages > 1" class="pagination-controls">
              <button 
                class="pagination-button" 
                :disabled="paginationWarns.currentPage === 1"
                @click="changePageWarns(paginationWarns.currentPage - 1)"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
                <span>ANTERIOR</span>
              </button>
              
              <div class="page-numbers">
                <span class="page-info">Página {{ paginationWarns.currentPage }} de {{ paginationWarns.totalPages }}</span>
              </div>
              
              <button 
                class="pagination-button" 
                :disabled="paginationWarns.currentPage === paginationWarns.totalPages"
                @click="changePageWarns(paginationWarns.currentPage + 1)"
              >
                <span>SIGUIENTE</span>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Pestaña: Bans -->
        <div v-else-if="activeTab === 'bans'" class="bans-tab">
          <div class="tab-header">
            <h2 class="tab-title">GESTIÓN DE BANEOS</h2>
            <div class="tab-subtitle">
              Gestionar baneos y suspensiones de usuarios
              <span v-if="paginationBans.total > 0" class="pagination-info">
                | Página {{ paginationBans.currentPage }} de {{ paginationBans.totalPages }} ({{ paginationBans.total }} baneos)
              </span>
            </div>
          </div>

          <!-- Barra de búsqueda y acciones -->
          <div class="action-bar">
            <div class="search-container">
              <div class="search-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
              <input
                v-model="searchQueryBans"
                @input="handleSearchBans"
                type="text"
                placeholder="Buscar usuarios baneados..."
                class="search-input"
              />
              
              <button 
                v-if="searchQueryBans" 
                @click="clearSearchBans"
                class="search-clear"
                title="Limpiar búsqueda"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
              
              <div class="search-info">
                <div class="search-count" v-if="totalBans > 0">
                  {{ totalBans }} {{ totalBans === 1 ? 'baneo' : 'baneos' }} encontrados
                </div>
              </div>
            </div>
            
            <div class="action-buttons">
              <button 
                class="action-button primary"
                @click="openCreateBanModal"
                :disabled="!canCreateBan()"
                :title="!canCreateBan() ? 'Requiere al menos nivel MOD_OFFICIAL' : ''"
              >
                <div class="action-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                  </svg>
                </div>
                <span>NUEVO BANEO</span>
              </button>
              
              <button 
                class="action-button secondary"
                @click="refreshBans"
              >
                <div class="action-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 4v6h-6"></path>
                    <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
                  </svg>
                </div>
                <span>ACTUALIZAR</span>
              </button>
            </div>
          </div>

          <!-- Filtros -->
          <div class="filters-container">
            <div class="filter-group">
              <label class="filter-label">Estado:</label>
              <select v-model="banFilter.status" class="filter-select" @change="applyFiltersBans">
                <option value="all">Todos los estados</option>
                <option value="active">Activos</option>
                <option value="revoked">Revocados</option>
                <option value="expired">Expirados</option>
              </select>
            </div>
            
            <div class="filter-group">
              <label class="filter-label">Tipo de Baneo:</label>
              <select v-model="banFilter.type" class="filter-select" @change="applyFiltersBans">
                <option value="all">Todos los tipos</option>
                <option value="temporary">Temporal</option>
                <option value="permanent">Permanente</option>
              </select>
            </div>
            
            <div class="filter-group">
              <label class="filter-label">Ordenar por:</label>
              <select v-model="banFilter.sort" class="filter-select" @change="applyFiltersBans">
                <option value="-created_at">Más recientes primero</option>
                <option value="created_at">Más antiguos primero</option>
                <option value="-ends_at">Expiración (próximos)</option>
                <option value="ends_at">Expiración (más lejanos)</option>
              </select>
            </div>
            
            <div class="filter-group">
              <label class="filter-label">Apelaciones:</label>
              <select v-model="banFilter.appealed" class="filter-select" @change="applyFiltersBans">
                <option value="all">Todos</option>
                <option value="true">Apelados</option>
                <option value="false">No Apelados</option>
              </select>
            </div>
          </div>

          <!-- Tabla de Bans -->
          <div class="table-container">
            <div v-if="loadingBans" class="loading-state">
              <div class="loading-spinner"></div>
              <p class="loading-text">Cargando baneos...</p>
            </div>
            
            <div v-else-if="displayedBans.length > 0" class="bans-table">
              <table class="scp-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>USUARIO</th>
                    <th>MODERADOR</th>
                    <th>RAZÓN</th>
                    <th>TIPO</th>
                    <th>DURACIÓN</th>
                    <th>ESTADO</th>
                    <th>CREADO</th>
                    <th>TERMINA</th>
                    <th>ACCIONES</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="ban in displayedBans" :key="ban.id" class="table-row">
                    <td class="id-cell">
                      <span class="id-badge">#{{ ban.id }}</span>
                    </td>
                    <td class="user-cell">
                      <div class="user-info">
                        <span class="username">{{ ban.target.roblox_username }}</span>
                        <span class="user-id">ID: {{ ban.target.roblox_id }}</span>
                      </div>
                    </td>
                    <td class="moderator-cell">
                      <span v-if="ban.created_by">{{ ban.created_by.roblox_username }}</span>
                      <span v-else class="unknown">Sistema</span>
                    </td>
                    <td class="reason-cell">
                      <div class="reason-text" :title="ban.reason">
                        {{ truncateText(ban.reason, 50) }}
                      </div>
                    </td>
                    <td class="type-cell">
                      <span class="type-badge" :class="`type-${ban.ban_type}`">
                        {{ ban.ban_type === 'temporary' ? 'Temporal' : 'Permanente' }}
                      </span>
                    </td>
                    <td class="duration-cell">
                      <span v-if="ban.ban_type === 'temporary' && ban.duration_days">
                        {{ ban.duration_days }} días
                      </span>
                      <span v-else class="permanent">Permanente</span>
                    </td>
                    <td class="status-cell">
                      <span class="status-badge" :class="`status-${ban.is_active ? 'active' : 'revoked'}`">
                        {{ ban.is_active ? 'Activo' : 'Revocado' }}
                      </span>
                      <div v-if="ban.appealed" class="appealed-indicator" title="Apelado">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                        </svg>
                      </div>
                    </td>
                    <td class="date-cell">
                      {{ formatDateShort(ban.created_at) }}
                    </td>
                    <td class="date-cell">
                      <span v-if="ban.ends_at" :class="{ 'expiring-soon': isExpiringSoon(ban.ends_at) }">
                        {{ formatDateShort(ban.ends_at) }}
                      </span>
                      <span v-else class="permanent">Nunca</span>
                    </td>
                    <td class="actions-cell">
                      <button class="table-action view" @click="viewBanDetails(ban)" title="Ver Detalles">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                          <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                      </button>
                      <button 
                        v-if="canCreateBan() && ban.is_active"
                        class="table-action revoke" 
                        @click="revokeBan(ban)"
                        title="Revocar Baneo"
                        :disabled="!canCreateBan()"
                        :title="!canCreateBan() ? 'Requiere nivel MOD_OFFICIAL o superior' : ''"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M18 6L6 18"></path>
                          <path d="M6 6l12 12"></path>
                        </svg>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div v-else class="empty-state">
              <div class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </div>
              <h3 class="empty-title">No se encontraron baneos</h3>
              <p class="empty-text" v-if="searchQueryBans">
                No hay baneos que coincidan con tu búsqueda
              </p>
              <p class="empty-text" v-else>
                No se han emitido baneos aún
              </p>
            </div>

            <!-- Paginación -->
            <div v-if="paginationBans.totalPages > 1" class="pagination-controls">
              <button 
                class="pagination-button" 
                :disabled="paginationBans.currentPage === 1"
                @click="changePageBans(paginationBans.currentPage - 1)"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="15 18 9 12 15 6"></polyline>
                </svg>
                <span>ANTERIOR</span>
              </button>
              
              <div class="page-numbers">
                <span class="page-info">Página {{ paginationBans.currentPage }} de {{ paginationBans.totalPages }}</span>
              </div>
              
              <button 
                class="pagination-button" 
                :disabled="paginationBans.currentPage === paginationBans.totalPages"
                @click="changePageBans(paginationBans.currentPage + 1)"
              >
                <span>SIGUIENTE</span>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Pestaña: Appeals -->
        <div v-else-if="activeTab === 'appeals'" class="appeals-tab">
          <div class="tab-header">
            <h2 class="tab-title">GESTIÓN DE APELACIONES</h2>
            <div class="tab-subtitle">
              Revisar y responder a apelaciones de usuarios
              <span v-if="pendingAppeals.length > 0" class="pending-count">
                | {{ pendingAppeals.length }} Apelaciones Pendientes
              </span>
            </div>
          </div>

          <!-- Lista de Apelaciones Pendientes -->
          <div class="appeals-container">
            <div v-if="loadingAppeals" class="loading-state">
              <div class="loading-spinner"></div>
              <p class="loading-text">Cargando apelaciones...</p>
            </div>
            
            <div v-else-if="pendingAppeals.length > 0" class="appeals-list">
              <div 
                v-for="appeal in pendingAppeals" 
                :key="appeal.id"
                class="appeal-card"
                :class="{ 'expiring-soon': isAppealUrgent(appeal) }"
              >
                <div class="appeal-header">
                  <div class="appeal-info">
                    <h4 class="appeal-title">
                      Apelación para Advertencia #{{ appeal.id }}
                      <span v-if="isAppealUrgent(appeal)" class="urgent-badge">URGENTE</span>
                    </h4>
                    <div class="appeal-meta">
                      <span class="meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                          <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                        {{ appeal.target.roblox_username }}
                      </span>
                      <span class="meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"></circle>
                          <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        {{ formatRelativeTime(appeal.appealed_at) }}
                      </span>
                      <span class="meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"></circle>
                          <line x1="12" y1="8" x2="12" y2="12"></line>
                          <line x1="12" y1="16" x2="12.01" y2="16"></line>
                        </svg>
                        Gravedad: {{ getSeverityText(appeal.severity) }}
                      </span>
                    </div>
                  </div>
                  <div class="appeal-actions">
                    <button class="appeal-action view" @click="viewAppealDetails(appeal)">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                    <span>REVISAR</span>
                    </button>
                  </div>
                </div>
                
                <div class="appeal-content">
                  <div class="appeal-reason">
                    <h5>Razón Original:</h5>
                    <p>{{ appeal.reason }}</p>
                  </div>
                  
                  <div v-if="appeal.evidence" class="appeal-evidence">
                    <h5>Evidencia:</h5>
                    <p class="evidence-text">{{ appeal.evidence }}</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else class="empty-state">
              <div class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <path d="M22 4 12 14.01l-3-3"></path>
                </svg>
              </div>
              <h3 class="empty-title">No hay apelaciones pendientes</h3>
              <p class="empty-text">Todas las apelaciones han sido revisadas</p>
            </div>
          </div>
        </div>

        <!-- Pestaña: User Search -->
        <div v-else-if="activeTab === 'users'" class="users-tab">
          <div class="tab-header">
            <h2 class="tab-title">BUSCAR USUARIO</h2>
            <div class="tab-subtitle">Buscar usuarios por ID de Roblox o nombre de usuario</div>
          </div>

          <!-- Búsqueda de Usuario -->
          <div class="user-search-container">
            <div class="search-panel">
              <div class="search-input-group">
                <div class="search-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                  </svg>
                </div>
                <input
                  v-model="userSearchQuery"
                  @keyup.enter="searchUser"
                  type="text"
                  placeholder="Ingresa ID de Roblox o nombre de usuario"
                  class="user-search-input"
                />
                <button class="search-button" @click="searchUser">
                  <span>BUSCAR</span>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </button>
              </div>
              
              <div class="search-hint">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="16" x2="12" y2="12"></line>
                  <line x1="12" y1="8" x2="12.01" y2="8"></line>
                </svg>
                <span>Buscar por ID de Roblox (ej: 123456789) o nombre de usuario</span>
              </div>
            </div>

            <!-- Resultados de Búsqueda -->
            <div v-if="loadingUser" class="loading-state">
            <div class="loading-spinner"></div>
            <p class="loading-text">Buscando usuario...</p>
            </div>

            <div v-else-if="searchedUser" class="user-profile">
            <div class="profile-header">
                <div class="profile-avatar">
                <div class="avatar-placeholder">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </div>
                </div>
                <div class="profile-info">
                <h3 class="profile-username">{{ searchedUser.roblox_username }}</h3>
                <div class="profile-id">ID de Roblox: {{ searchedUser.roblox_id }}</div>
                <div class="profile-stats">
                    <span class="stat-item">
                    <span class="stat-label">Advertencias:</span>
                    <span class="stat-value" :class="{ 'has-warns': searchedUser.warning_count > 0 }">
                        {{ searchedUser.warning_count }}
                    </span>
                    </span>
                    <span class="stat-item">
                    <span class="stat-label">Estado:</span>
                    <span class="stat-value" :class="{ 'banned': searchedUser.is_banned }">
                        {{ searchedUser.is_banned ? 'BANEADO' : 'ACTIVO' }}
                    </span>
                    </span>
                    <span v-if="searchedUser.first_login" class="stat-item">
                    <span class="stat-label">Primer Login:</span>
                    <span class="stat-value">{{ formatDateShort(searchedUser.first_login) }}</span>
                    </span>
                </div>
                </div>
                <div class="profile-actions">
                <button 
                    class="profile-action warn"
                    @click="warnSearchedUser"
                    :disabled="!canCreateWarn()"
                    :title="!canCreateWarn() ? 'Requiere al menos nivel MOD_JUNIOR' : ''"
                >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    <span>EMITIR ADVERTENCIA</span>
                </button>
                <button 
                    class="profile-action ban"
                    @click="banSearchedUser"
                    :disabled="!canCreateBan()"
                    :title="!canCreateBan() ? 'Requiere al menos nivel MOD_OFFICIAL' : ''"
                >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                    <span>EMITIR BANEO</span>
                </button>
                <button class="profile-action view" @click="viewUserHistory">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                    </svg>
                    <span>VER HISTORIAL</span>
                </button>
                </div>
            </div>
            
            <!-- Historial del Usuario -->
            <div v-if="userHistory" class="user-history">
                <h4 class="history-title">HISTORIAL DE MODERACIÓN</h4>
                
                <!-- Warns del Usuario -->
                <div v-if="userHistory.active_warns && userHistory.active_warns.length > 0" class="history-section">
                <h5 class="section-title">Advertencias Activas ({{ userHistory.active_warns.length }})</h5>
                <div class="warns-list">
                    <div 
                    v-for="warn in userHistory.active_warns" 
                    :key="warn.id"
                    class="history-item warn"
                    >
                    <div class="item-header">
                        <span class="item-id">Advertencia #{{ warn.id }}</span>
                        <span class="item-severity" :class="`severity-${warn.severity}`">
                        {{ getSeverityText(warn.severity) }}
                        </span>
                        <span class="item-date">{{ formatDateShort(warn.created_at) }}</span>
                    </div>
                    <div class="item-content">
                        <p class="item-reason">{{ warn.reason }}</p>
                        <div class="item-meta">
                        <span v-if="warn.expires_at" class="item-expiry">
                            Expira: {{ formatDateShort(warn.expires_at) }}
                        </span>
                        </div>
                    </div>
                    </div>
                </div>
                </div>
                
                <!-- Bans del Usuario -->
                <div v-if="userHistory.active_bans && userHistory.active_bans.length > 0" class="history-section">
                <h5 class="section-title">Baneos Activos ({{ userHistory.active_bans.length }})</h5>
                <div class="bans-list">
                    <div 
                    v-for="ban in userHistory.active_bans" 
                    :key="ban.id"
                    class="history-item ban"
                    >
                    <div class="item-header">
                        <span class="item-id">Baneo #{{ ban.id }}</span>
                        <span class="item-type" :class="`type-${ban.ban_type}`">
                        {{ ban.ban_type === 'temporary' ? 'Temporal' : 'Permanente' }}
                        </span>
                        <span class="item-date">{{ formatDateShort(ban.created_at) }}</span>
                    </div>
                    <div class="item-content">
                        <p class="item-reason">{{ ban.reason }}</p>
                        <div class="item-meta">
                        <span v-if="ban.ends_at" class="item-expiry">
                            Termina: {{ formatDateShort(ban.ends_at) }}
                        </span>
                        </div>
                    </div>
                    </div>
                </div>
                </div>
                
                <!-- Sin historial -->
                <div v-if="(!userHistory.active_warns || userHistory.active_warns.length === 0) && (!userHistory.active_bans || userHistory.active_bans.length === 0)" class="no-history">
                <div class="no-history-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <path d="M22 4 12 14.01l-3-3"></path>
                    </svg>
                </div>
                <p class="no-history-text">No se encontró historial de moderación para este usuario</p>
                </div>
            </div>
            </div>

            <div v-else-if="userSearchQuery && !loadingUser" class="no-results">
            <div class="no-results-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
            </div>
            <h4 class="no-results-title">Usuario no encontrado</h4>
            <p class="no-results-text">No se encontró usuario con ese ID de Roblox o nombre de usuario</p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modales -->
    <!-- Modal: Crear Warn -->
    <div v-if="showCreateWarnModal" class="modal-overlay" @click.self="closeCreateWarnModal">
      <div class="modal-content create-warn-modal">
        <div class="modal-header">
          <h3 class="modal-title">EMITIR NUEVA ADVERTENCIA</h3>
          <button class="modal-close" @click="closeCreateWarnModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="submitNewWarn">
            <div class="form-group">
              <label class="form-label">Usuario Objetivo *</label>
              <input
                v-model="newWarn.target_id"
                type="text"
                class="form-input"
                placeholder="ID de Roblox"
                required
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Razón *</label>
              <textarea
                v-model="newWarn.reason"
                class="form-textarea"
                placeholder="Razón detallada para la advertencia..."
                rows="3"
                required
              ></textarea>
            </div>
            
            <div class="form-group">
              <label class="form-label">Evidencia (Opcional)</label>
              <textarea
                v-model="newWarn.evidence"
                class="form-textarea"
                placeholder="Enlaces a evidencia (Discord, videos, etc.)..."
                rows="2"
              ></textarea>
            </div>
            
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Gravedad *</label>
                <select v-model="newWarn.severity" class="form-select" required>
                  <option value="1">Baja - Infracción menor</option>
                  <option value="2">Media - Infracción moderada</option>
                  <option value="3">Alta - Infracción grave</option>
                </select>
              </div>
              
              <div class="form-group">
                <label class="form-label">Expiración *</label>
                <select v-model="newWarn.expires_after_days" class="form-select" required>
                  <option value="7">7 días</option>
                  <option value="14">14 días</option>
                  <option value="30">30 días (por defecto)</option>
                  <option value="60">60 días</option>
                  <option value="90">90 días</option>
                  <option value="0">Nunca (permanente)</option>
                </select>
              </div>
            </div>
            
            <div class="form-actions">
              <button type="button" class="cancel-button" @click="closeCreateWarnModal">
                CANCELAR
              </button>
              <button type="submit" class="submit-button" :disabled="submittingWarn">
                <span v-if="submittingWarn">EMITIENDO...</span>
                <span v-else>EMITIR ADVERTENCIA</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal: Crear Ban -->
    <div v-if="showCreateBanModal" class="modal-overlay" @click.self="closeCreateBanModal">
      <div class="modal-content create-ban-modal">
        <div class="modal-header">
          <h3 class="modal-title">EMITIR NUEVO BANEO</h3>
          <button class="modal-close" @click="closeCreateBanModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="submitNewBan">
            <div class="form-group">
              <label class="form-label">Usuario Objetivo *</label>
              <input
                v-model="newBan.target_id"
                type="text"
                class="form-input"
                placeholder="ID de Roblox"
                required
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Razón *</label>
              <textarea
                v-model="newBan.reason"
                class="form-textarea"
                placeholder="Razón detallada para el baneo..."
                rows="3"
                required
              ></textarea>
            </div>
            
            <div class="form-group">
              <label class="form-label">Evidencia (Opcional)</label>
              <textarea
                v-model="newBan.evidence"
                class="form-textarea"
                placeholder="Enlaces a evidencia (Discord, videos, etc.)..."
                rows="2"
              ></textarea>
            </div>
            
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Tipo de Baneo *</label>
                <select v-model="newBan.ban_type" class="form-select" required @change="updateBanType">
                  <option value="temporary">Temporal</option>
                  <option value="permanent">Permanente</option>
                </select>
              </div>
              
              <div class="form-group" v-if="newBan.ban_type === 'temporary'">
                <label class="form-label">Duración *</label>
                <select v-model="newBan.duration_days" class="form-select" required>
                  <option value="1">1 día</option>
                  <option value="3">3 días</option>
                  <option value="7">7 días</option>
                  <option value="14">14 días</option>
                  <option value="30">30 días</option>
                  <option value="60">60 días</option>
                  <option value="90">90 días</option>
                </select>
              </div>
              
              <div class="form-group">
                <label class="form-label">¿Permitir Apelación?</label>
                <select v-model="newBan.can_appeal" class="form-select">
                  <option :value="true">Sí</option>
                  <option :value="false">No</option>
                </select>
              </div>
            </div>
            
            <div class="form-actions">
              <button type="button" class="cancel-button" @click="closeCreateBanModal">
                CANCELAR
              </button>
              <button type="submit" class="submit-button" :disabled="submittingBan">
                <span v-if="submittingBan">EMITIENDO...</span>
                <span v-else>EMITIR BANEO</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal: Detalles de Warn -->
    <div v-if="selectedWarn" class="modal-overlay" @click.self="selectedWarn = null">
      <div class="modal-content warn-details-modal">
        <div class="modal-header">
          <h3 class="modal-title">DETALLES DE ADVERTENCIA</h3>
          <button class="modal-close" @click="selectedWarn = null">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="details-grid">
            <div class="detail-item">
              <span class="detail-label">ID de Advertencia:</span>
              <span class="detail-value">#{{ selectedWarn.id }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Usuario Objetivo:</span>
              <span class="detail-value">{{ selectedWarn.target.roblox_username }} (ID: {{ selectedWarn.target.roblox_id }})</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Emitida Por:</span>
              <span class="detail-value">{{ selectedWarn.created_by?.roblox_username || 'Sistema' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Creada:</span>
              <span class="detail-value">{{ formatDateFull(selectedWarn.created_at) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Gravedad:</span>
              <span class="detail-value severity-badge" :class="`severity-${selectedWarn.severity}`">
                {{ getSeverityText(selectedWarn.severity) }}
              </span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Estado:</span>
              <span class="detail-value status-badge" :class="`status-${selectedWarn.status}`">
                {{ getStatusText(selectedWarn.status) }}
              </span>
            </div>
            <div class="detail-item" v-if="selectedWarn.expires_at">
              <span class="detail-label">Expira:</span>
              <span class="detail-value" :class="{ 'expiring-soon': isExpiringSoon(selectedWarn.expires_at) }">
                {{ formatDateFull(selectedWarn.expires_at) }}
              </span>
            </div>
            <div class="detail-item" v-if="selectedWarn.appealed">
              <span class="detail-label">Apelada:</span>
              <span class="detail-value">{{ formatDateFull(selectedWarn.appealed_at) }} por {{ selectedWarn.appealed_by?.roblox_username || 'Usuario' }}</span>
            </div>
            <div class="detail-item" v-if="selectedWarn.appeal_response">
              <span class="detail-label">Respuesta a Apelación:</span>
              <span class="detail-value">{{ selectedWarn.appeal_response }}</span>
            </div>
          </div>
          
          <div class="details-section">
            <h4 class="section-title">Razón</h4>
            <div class="section-content">
              <p>{{ selectedWarn.reason }}</p>
            </div>
          </div>
          
          <div v-if="selectedWarn.evidence" class="details-section">
            <h4 class="section-title">Evidencia</h4>
            <div class="section-content">
              <p class="evidence-text">{{ selectedWarn.evidence }}</p>
            </div>
          </div>
          
          <div class="modal-actions" v-if="hasPermission('manage_warns') || canManageWarns()">
            <button 
              v-if="selectedWarn.appealed && !selectedWarn.appeal_response"
              class="action-button primary"
              @click="respondToAppeal(selectedWarn)"
              :disabled="!canRespondAppeals()"
              :title="!canRespondAppeals() ? 'Requiere nivel MOD_QUALIFIED o superior' : ''"
            >
              RESPONDER A APELACIÓN
            </button>
            <button 
              v-if="selectedWarn.status === 'active'"
              class="action-button secondary"
              @click="removeSelectedWarn"
              :disabled="!canManageWarns()"
              :title="!canManageWarns() ? 'Requiere nivel MOD_QUALIFIED o superior' : ''"
            >
              ELIMINAR ADVERTENCIA
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Sistema de notificaciones -->
    <div class="scp-notifications">
      <transition-group name="notification-slide">
        <div 
          v-for="notification in notifications" 
          :key="notification.id"
          class="scp-notification"
          :class="`type-${notification.type}`"
          @click="removeNotification(notification.id)"
        >
          <div class="notification-header">
            <div class="notification-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path v-if="notification.type === 'success'" d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <path v-if="notification.type === 'success'" d="M22 4 12 14.01l-3-3"></path>
                <path v-if="notification.type === 'error'" d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line v-if="notification.type === 'error'" x1="12" y1="9" x2="12" y2="13"></line>
                <line v-if="notification.type === 'error'" x1="12" y1="17" x2="12.01" y2="17"></line>
                <circle v-if="notification.type === 'info'" cx="12" cy="12" r="10"></circle>
                <line v-if="notification.type === 'info'" x1="12" y1="16" x2="12" y2="12"></line>
                <line v-if="notification.type === 'info'" x1="12" y1="8" x2="12.01" y2="8"></line>
              </svg>
            </div>
            <div class="notification-title">
              {{ notification.title }}
            </div>
            <button class="notification-close">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="notification-content">
            {{ notification.message }}
          </div>
          <div class="notification-progress" :style="{ 
            animationDuration: `${notification.duration}ms`,
            animationPlayState: notification.paused ? 'paused' : 'running' 
          }"></div>
        </div>
      </transition-group>
    </div>
    <div v-if="showAppealResponseModal && selectedAppeal" class="modal-overlay" @click.self="closeAppealResponseModal">
        <div class="modal-content appeal-response-modal">
            <div class="modal-header">
            <h3 class="modal-title">RESPONDER A APELACIÓN</h3>
            <button class="modal-close" @click="closeAppealResponseModal">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
            </div>
            
            <div class="modal-body">
            <!-- Información de la apelación -->
            <div class="appeal-info">
                <div class="info-row">
                <span class="info-label">Advertencia ID:</span>
                <span class="info-value">#{{ selectedAppeal.id }}</span>
                </div>
                <div class="info-row">
                <span class="info-label">Usuario:</span>
                <span class="info-value">{{ selectedAppeal.target.roblox_username }} (ID: {{ selectedAppeal.target.roblox_id }})</span>
                </div>
                <div class="info-row">
                <span class="info-label">Gravedad:</span>
                <span class="info-value severity-badge" :class="`severity-${selectedAppeal.severity}`">
                    {{ getSeverityText(selectedAppeal.severity) }}
                </span>
                </div>
                <div class="info-row">
                <span class="info-label">Fecha de Creación:</span>
                <span class="info-value">{{ formatDateFull(selectedAppeal.created_at) }}</span>
                </div>
                <div class="info-row">
                <span class="info-label">Fecha de Apelación:</span>
                <span class="info-value">{{ formatDateFull(selectedAppeal.appealed_at) }}</span>
                </div>
            </div>
            
            <!-- Razón original -->
            <div class="section">
                <h4 class="section-title">Razón Original de la Advertencia</h4>
                <div class="section-content">
                <p>{{ selectedAppeal.reason }}</p>
                </div>
            </div>
            
            <!-- Evidencia -->
            <div v-if="selectedAppeal.evidence" class="section">
                <h4 class="section-title">Evidencia Presentada</h4>
                <div class="section-content">
                <p class="evidence-text">{{ selectedAppeal.evidence }}</p>
                </div>
            </div>
            
            <!-- Formulario de respuesta -->
            <div class="response-form">
                <div class="form-group">
                <label class="form-label">Tu Respuesta *</label>
                <p class="form-hint">
                    Escribe tu respuesta a la apelación. Si aceptas la apelación, la advertencia será eliminada automáticamente.
                </p>
                <textarea
                    v-model="appealResponse"
                    class="form-textarea"
                    placeholder="Escribe tu respuesta aquí... 
        Ejemplo: 'Apelación aceptada. La advertencia ha sido eliminada.'
        Ejemplo: 'Apelación rechazada. La evidencia presentada confirma la infracción.'"
                    rows="6"
                    required
                ></textarea>
                </div>
                
                <div class="response-tips">
                <h4>Consejos para responder:</h4>
                <ul>
                    <li>Sé claro y profesional en tu respuesta</li>
                    <li>Si aceptas la apelación, incluye la palabra "aceptado" o "aceptada"</li>
                    <li>Proporciona una breve explicación de tu decisión</li>
                    <li>Mantén un tono respetuoso</li>
                </ul>
                </div>
                
                <div class="form-actions">
                <button type="button" class="cancel-button" @click="closeAppealResponseModal">
                    CANCELAR
                </button>
                <button type="button" class="submit-button" @click="respondToAppeal" :disabled="!canRespondAppeals()" :title="!canRespondAppeals() ? 'Requiere nivel MOD_QUALIFIED o superior' : ''">
                    ENVIAR RESPUESTA
                </button>
                </div>
            </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { debounce } from 'lodash'
import Login_Required from '@/components/Login_Required.vue'

const router = useRouter()

// Estado principal
const activeTab = ref('warns')
const currentUser = ref(null)
const userPermissions = ref([])
const currentTime = ref('')
const loadingWarns = ref(false)
const loadingBans = ref(false)
const loadingAppeals = ref(false)
const loadingUser = ref(false)
const showCreateWarnModal = ref(false)
const showCreateBanModal = ref(false)
const selectedWarn = ref(null)
const selectedBan = ref(null)
const submittingWarn = ref(false)
const submittingBan = ref(false)
const showAppealResponseModal = ref(false)
const selectedAppeal = ref(null)
const appealResponse = ref('')

// Búsqueda y filtros
const searchQueryWarns = ref('')
const searchQueryBans = ref('')
const userSearchQuery = ref('')
const searchedUser = ref(null)
const userHistory = ref(null)

const warnFilter = reactive({
  status: 'all',
  severity: 'all',
  sort: '-created_at',
  startDate: '',
  endDate: ''
})

const banFilter = reactive({
  status: 'all',
  type: 'all',
  sort: '-created_at',
  appealed: 'all'
})

// Paginación
const paginationWarns = reactive({
  currentPage: 1,
  pageSize: 20,
  total: 0,
  totalPages: 0
})

const paginationBans = reactive({
  currentPage: 1,
  pageSize: 20,
  total: 0,
  totalPages: 0
})

// Datos
const warns = ref([])
const bans = ref([])
const pendingAppeals = ref([])

// Nuevo warn/ban
const newWarn = reactive({
  target_id: '',
  reason: '',
  evidence: '',
  severity: '2',
  expires_after_days: '30'
})

const newBan = reactive({
  target_id: '',
  reason: '',
  evidence: '',
  ban_type: 'temporary',
  duration_days: '7',
  can_appeal: true
})

// Notificaciones
const notifications = ref([])
let notificationId = 0

// Computed
const displayedWarns = computed(() => {
  if (searchQueryWarns.value) {
    const searchLower = searchQueryWarns.value.toLowerCase()
    return warns.value.filter(warn => 
      warn.target.roblox_username.toLowerCase().includes(searchLower) ||
      warn.target.roblox_id.toString().includes(searchLower) ||
      warn.reason.toLowerCase().includes(searchLower) ||
      (warn.created_by?.roblox_username?.toLowerCase().includes(searchLower) || false)
    )
  }
  return warns.value
})

const displayedBans = computed(() => {
  if (searchQueryBans.value) {
    const searchLower = searchQueryBans.value.toLowerCase()
    return bans.value.filter(ban => 
      ban.target.roblox_username.toLowerCase().includes(searchLower) ||
      ban.target.roblox_id.toString().includes(searchLower) ||
      ban.reason.toLowerCase().includes(searchLower)
    )
  }
  return bans.value
})

const totalWarns = computed(() => displayedWarns.value.length)
const totalBans = computed(() => displayedBans.value.length)

// ========== MÉTODOS DE PERMISOS ==========
// Método para cargar permisos del usuario
const fetchUserPermissions = async () => {
  try {
    const response = await fetch('/api/auth/user/permissions/')
    if (response.ok) {
      const data = await response.json()
      userPermissions.value = data.permissions || []
      
      // También guardar en currentUser para compatibilidad
      if (currentUser.value) {
        currentUser.value.permissions = data.permissions || []
      }
      
      showNotification('INFO', 'Permisos cargados correctamente', 'info', 3000)
    }
  } catch (error) {
    console.error('Error cargando permisos:', error)
    showNotification('ERROR', 'Error al cargar permisos', 'error', 4000)
  }
}

// Método para verificar acceso al panel de moderación
const hasModerationPermission = () => {
  if (!currentUser.value || !currentUser.value.is_authenticated) return false
  
  // Superusuarios y staff siempre tienen acceso
  if (currentUser.value.is_superuser || currentUser.value.is_staff) {
    return true
  }
  
  // Verificar si tiene permisos de moderación
  const hasModerationAccess = userPermissions.value.some(permission => 
    permission.includes('moderation') || 
    permission.includes('warn') || 
    permission.includes('ban') ||
    permission === 'access_moderation_dashboard'
  )
  
  return hasModerationAccess
}

// Método para verificar permisos específicos
const hasPermission = (permissionKey) => {
  if (!currentUser.value) return false
  
  // Superuser tiene todos los permisos
  if (currentUser.value.is_superuser) return true
  
  // Verificar en los permisos del usuario
  return userPermissions.value.includes(permissionKey)
}

// Método para obtener nivel de permiso con los 4 niveles de mod
const getUserPermissionLevel = () => {
  if (!currentUser.value) return 'INVITADO'
  
  // Superusuarios siempre son admin
  if (currentUser.value.is_superuser) return 'ADMIN'
  
  // Si es staff pero no tiene permisos específicos
  if (currentUser.value.is_staff && userPermissions.value.length === 0) {
    return 'STAFF'
  }
  
  // Verificar nivel basado en permisos jerárquicos
  const permissions = userPermissions.value || []
  
  // Nivel 4: Senior - Permisos avanzados y liderazgo
  if (permissions.includes('full_moderation_control') || 
      permissions.includes('full_discord_moderation')) {
    return 'MOD_SENIOR'
  }
  
  // Nivel 3: Qualified - Gestiona warns y puede responder apelaciones
  if (permissions.includes('manage_warns')) {
    return 'MOD_QUALIFIED'
  }
  
  // Nivel 2: Official - Puede crear warns y bans
  if (permissions.includes('register_ban')) {
    return 'MOD_OFFICIAL'
  }
  
  // Nivel 1: Junior - Solo puede crear warns básicos
  if (permissions.includes('create_warn')) {
    return 'MOD_JUNIOR'
  }
  
  // Tiene acceso al dashboard pero no a acciones específicas
  if (permissions.includes('access_moderation_dashboard')) {
    return 'OBSERVADOR'
  }
  
  // Staff sin permisos específicos
  if (currentUser.value.is_staff) {
    return 'STAFF'
  }
  
  return 'INVITADO'
}

// Método para obtener el nivel numérico de moderación
const getModerationLevel = () => {
  const permissionLevel = getUserPermissionLevel()
  
  switch(permissionLevel) {
    case 'MOD_SENIOR': return 4
    case 'MOD_QUALIFIED': return 3
    case 'MOD_OFFICIAL': return 2
    case 'MOD_JUNIOR': return 1
    case 'ADMIN': return 5 // Admin es nivel superior
    default: return 0 // No es moderador
  }
}

// Método para verificar si tiene al menos un nivel específico
const hasMinModLevel = (requiredLevel) => {
  const userLevel = getModerationLevel()
  return userLevel >= requiredLevel
}

// Métodos específicos por nivel
const isJuniorMod = () => hasMinModLevel(1)
const isOfficialMod = () => hasMinModLevel(2)
const isQualifiedMod = () => hasMinModLevel(3)
const isSeniorMod = () => hasMinModLevel(4)
const isAdmin = () => getUserPermissionLevel() === 'ADMIN'

// Método para verificar si puede responder apelaciones (Qualified+ o Senior)
const canRespondAppeals = () => {
  if (!currentUser.value) return false
  
  // Superuser y Admin siempre pueden
  if (currentUser.value.is_superuser || isAdmin()) return true
  
  // Qualified Mods (nivel 3+) y Senior Mods (nivel 4) pueden responder
  return isQualifiedMod() || isSeniorMod()
}

// Verificar acciones según nivel de permiso
const canCreateWarn = () => hasPermission('create_warn') || isJuniorMod() || isOfficialMod() || isQualifiedMod() || isSeniorMod()
const canCreateBan = () => hasPermission('register_ban') || isOfficialMod() || isQualifiedMod() || isSeniorMod()
const canManageWarns = () => hasPermission('manage_warns') || isQualifiedMod() || isSeniorMod()
const canAccessDashboard = () => hasPermission('access_moderation_dashboard') || isJuniorMod() || isOfficialMod() || isQualifiedMod() || isSeniorMod()

// ========== FIN MÉTODOS DE PERMISOS ==========

// Navegación
const setActiveTab = (tab) => {
  activeTab.value = tab
  switch(tab) {
    case 'warns':
      loadWarns()
      break
    case 'bans':
      loadBans()
      break
    case 'appeals':
      loadAppeals()
      break
  }
}

// Carga de datos
const loadWarns = async () => {
  if (!hasModerationPermission()) {
    showNotification('ACCESO DENEGADO', 'No tienes acceso al panel de moderación', 'error', 4000)
    return
  }
  
  loadingWarns.value = true
  try {
    const response = await fetch('/api/moderation/warns/')
    if (response.ok) {
      const data = await response.json()
      warns.value = data.warns || []
      updatePaginationWarns(warns.value.length)
    } else if (response.status === 403) {
      showNotification('ACCESO DENEGADO', 'No tienes permisos para ver advertencias', 'error', 4000)
    }
  } catch (error) {
    console.error('Error cargando advertencias:', error)
    showNotification('ERROR', 'Error al cargar advertencias', 'error', 4000)
  } finally {
    loadingWarns.value = false
  }
}

const loadBans = async () => {
  if (!hasModerationPermission()) {
    showNotification('ACCESO DENEGADO', 'No tienes acceso al panel de moderación', 'error', 4000)
    return
  }
  
  loadingBans.value = true
  try {
    const response = await fetch('/api/moderation/bans/')
    if (response.ok) {
      const data = await response.json()
      bans.value = data.bans || []
      updatePaginationBans(bans.value.length)
    } else if (response.status === 403) {
      showNotification('ACCESO DENEGADO', 'No tienes permisos para ver baneos', 'error', 4000)
    }
  } catch (error) {
    console.error('Error cargando baneos:', error)
    showNotification('ERROR', 'Error al cargar baneos', 'error', 4000)
  } finally {
    loadingBans.value = false
  }
}

const loadAppeals = async () => {
  if (!hasModerationPermission()) {
    showNotification('ACCESO DENEGADO', 'No tienes acceso al panel de moderación', 'error', 4000)
    return
  }
  
  loadingAppeals.value = true
  try {
    const response = await fetch('/api/moderation/warns/')
    if (response.ok) {
      const data = await response.json()
      // Filtrar warns apelados sin respuesta
      pendingAppeals.value = (data.warns || []).filter(w => 
        w.appealed && !w.appeal_response
      )
    } else if (response.status === 403) {
      showNotification('ACCESO DENEGADO', 'No tienes permisos para ver apelaciones', 'error', 4000)
    }
  } catch (error) {
    console.error('Error cargando apelaciones:', error)
    showNotification('ERROR', 'Error al cargar apelaciones', 'error', 4000)
  } finally {
    loadingAppeals.value = false
  }
}

const updatePaginationWarns = (total) => {
  paginationWarns.total = total
  paginationWarns.totalPages = Math.ceil(total / paginationWarns.pageSize)
}

const updatePaginationBans = (total) => {
  paginationBans.total = total
  paginationBans.totalPages = Math.ceil(total / paginationBans.pageSize)
}

// Búsqueda
const handleSearchWarns = debounce(() => {
  paginationWarns.currentPage = 1
  updatePaginationWarns(displayedWarns.value.length)
}, 300)

const handleSearchBans = debounce(() => {
  paginationBans.currentPage = 1
  updatePaginationBans(displayedBans.value.length)
}, 300)

const clearSearchWarns = () => {
  searchQueryWarns.value = ''
  paginationWarns.currentPage = 1
  updatePaginationWarns(warns.value.length)
}

const clearSearchBans = () => {
  searchQueryBans.value = ''
  paginationBans.currentPage = 1
  updatePaginationBans(bans.value.length)
}

// Filtros
const applyFiltersWarns = () => {
  // Implementar lógica de filtrado
  loadWarns()
}

const applyFiltersBans = () => {
  // Implementar lógica de filtrado
  loadBans()
}

// Paginación
const changePageWarns = (page) => {
  if (page < 1 || page > paginationWarns.totalPages) return
  paginationWarns.currentPage = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const changePageBans = (page) => {
  if (page < 1 || page > paginationBans.totalPages) return
  paginationBans.currentPage = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const goToModerationPanel = () => {
  router.push('/moderation')
}

// Acciones de Warn
const openCreateWarnModal = () => { 
  if (!canCreateWarn()) {
    showNotification('ACCESO DENEGADO', 'Necesitas al menos nivel MOD_JUNIOR para crear advertencias', 'error', 4000)
    return
  }
  showCreateWarnModal.value = true
}

const closeCreateWarnModal = () => {
  showCreateWarnModal.value = false
  Object.assign(newWarn, {
    target_id: '',
    reason: '',
    evidence: '',
    severity: '2',
    expires_after_days: '30'
  })
}

const submitNewWarn = async () => {
  if (!canCreateWarn()) {
    showNotification('ACCESO DENEGADO', 'No tienes permiso para crear advertencias', 'error', 4000)
    return
  }
  
  submittingWarn.value = true
  try {
    const csrfToken = getCSRFToken()
    const response = await fetch('/api/moderation/warns/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      credentials: 'include',
      body: JSON.stringify(newWarn)
    })
    
    if (response.ok) {
      const data = await response.json()
      showNotification('ÉXITO', 'Advertencia emitida exitosamente', 'success', 4000)
      closeCreateWarnModal()
      loadWarns()
    } else {
      const error = await response.json()
      showNotification('ERROR', error.error || 'Error al emitir advertencia', 'error', 5000)
    }
  } catch (error) {
    console.error('Error emitiendo advertencia:', error)
    showNotification('ERROR', 'Error al emitir advertencia', 'error', 5000)
  } finally {
    submittingWarn.value = false
  }
}

const viewWarnDetails = (warn) => {
  selectedWarn.value = warn
}

const editWarn = (warn) => {
  // Implementar edición de warn
  showNotification('INFO', 'Función de edición próximamente', 'info', 3000)
}

const removeWarn = async (warn) => {
  if (!canManageWarns() || !confirm(`¿Eliminar advertencia #${warn.id}?`)) {
    if (!canManageWarns()) {
      showNotification('ACCESO DENEGADO', 'Requieres nivel MOD_QUALIFIED o superior para eliminar advertencias', 'error', 4000)
    }
    return
  }
  
  try {
    const csrfToken = getCSRFToken()
    const response = await fetch(`/api/moderation/warns/${warn.id}/remove/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken
      },
      credentials: 'include'
    })
    
    if (response.ok) {
      showNotification('ÉXITO', 'Advertencia eliminada exitosamente', 'success', 4000)
      loadWarns()
    } else {
      showNotification('ERROR', 'Error al eliminar advertencia', 'error', 5000)
    }
  } catch (error) {
    console.error('Error eliminando advertencia:', error)
    showNotification('ERROR', 'Error al eliminar advertencia', 'error', 5000)
  }
}

const removeSelectedWarn = () => {
  if (selectedWarn.value) {
    removeWarn(selectedWarn.value)
    selectedWarn.value = null
  }
}

const viewAppealDetails = (appeal) => {
  // Guardar la apelación seleccionada
  selectedAppeal.value = appeal
  
  // Abrir modal de respuesta a apelación
  showAppealResponseModal.value = true
  
  // Resetear el formulario de respuesta
  appealResponse.value = ''
}


const closeAppealResponseModal = () => {
  showAppealResponseModal.value = false
  selectedAppeal.value = null
  appealResponse.value = ''
}

const respondToAppeal = async () => {
  if (!canRespondAppeals()) {
    showNotification('ACCESO DENEGADO', 'Requieres nivel MOD_QUALIFIED o superior para responder apelaciones', 'error', 4000)
    return
  }
  
  if (!selectedAppeal.value || !appealResponse.value.trim()) {
    showNotification('ERROR', 'Debes escribir una respuesta', 'error', 4000)
    return
  }
  
  try {
    const csrfToken = getCSRFToken()
    const response = await fetch(`/api/moderation/warns/${selectedAppeal.value.id}/respond-appeal/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      credentials: 'include',
      body: JSON.stringify({
        response: appealResponse.value
      })
    })
    
    if (response.ok) {
      showNotification('ÉXITO', 'Respuesta enviada correctamente', 'success', 5000)
      closeAppealResponseModal()
      loadAppeals() // Recargar la lista de apelaciones
      loadWarns()   // Recargar también la lista de warns
    } else {
      const error = await response.json()
      showNotification('ERROR', error.error || 'Error al enviar respuesta', 'error', 5000)
    }
  } catch (error) {
    console.error('Error respondiendo a apelación:', error)
    showNotification('ERROR', 'Error al enviar respuesta', 'error', 5000)
  }
}

// Acciones de Ban 
const openCreateBanModal = () => { 
  if (!canCreateBan()) {
    showNotification('ACCESO DENEGADO', 'Necesitas al menos nivel MOD_OFFICIAL para crear baneos', 'error', 4000)
    return
  }
  showCreateBanModal.value = true
}

const closeCreateBanModal = () => {
  showCreateBanModal.value = false
  Object.assign(newBan, {
    target_id: '',
    reason: '',
    evidence: '',
    ban_type: 'temporary',
    duration_days: '7',
    can_appeal: true
  })
}

const submitNewBan = async () => {
  if (!canCreateBan()) {
    showNotification('ACCESO DENEGADO', 'No tienes permiso para crear baneos', 'error', 4000)
    return
  }
  
  submittingBan.value = true
  try {
    const csrfToken = getCSRFToken()
    const response = await fetch('/api/moderation/bans/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      credentials: 'include',
      body: JSON.stringify(newBan)
    })
    
    if (response.ok) {
      const data = await response.json()
      showNotification('ÉXITO', 'Baneo emitido exitosamente', 'success', 4000)
      closeCreateBanModal()
      loadBans()
    } else {
      const error = await response.json()
      showNotification('ERROR', error.error || 'Error al emitir baneo', 'error', 5000)
    }
  } catch (error) {
    console.error('Error emitiendo baneo:', error)
    showNotification('ERROR', 'Error al emitir baneo', 'error', 5000)
  } finally {
    submittingBan.value = false
  }
}

const updateBanType = () => {
  if (newBan.ban_type === 'permanent') {
    newBan.duration_days = null
  } else {
    newBan.duration_days = '7'
  }
}

const viewBanDetails = (ban) => {
  selectedBan.value = ban
}

const revokeBan = async (ban) => {
  if (!canCreateBan() || !confirm(`¿Revocar baneo #${ban.id}?`)) {
    if (!canCreateBan()) {
      showNotification('ACCESO DENEGADO', 'Requieres nivel MOD_OFFICIAL o superior para revocar baneos', 'error', 4000)
    }
    return
  }
  
  try {
    const csrfToken = getCSRFToken()
    const response = await fetch(`/api/moderation/bans/${ban.id}/revoke/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      credentials: 'include',
      body: JSON.stringify({ reason: 'Revocado por moderador' })
    })
    
    if (response.ok) {
      showNotification('ÉXITO', 'Baneo revocado exitosamente', 'success', 4000)
      loadBans()
    } else {
      showNotification('ERROR', 'Error al revocar baneo', 'error', 5000)
    }
  } catch (error) {
    console.error('Error revocando baneo:', error)
    showNotification('ERROR', 'Error al revocar baneo', 'error', 5000)
  }
}

// Búsqueda de usuario
const searchUser = async () => {
  if (!userSearchQuery.value.trim()) {
    showNotification('INFO', 'Ingresa un ID de Roblox o nombre de usuario', 'info', 3000)
    return
  }
  
  loadingUser.value = true
  searchedUser.value = null
  userHistory.value = null
  
  try {
    // Usar la ruta correcta para búsqueda de usuarios
    const response = await fetch(`/api/moderation/users/search/${encodeURIComponent(userSearchQuery.value)}/`)
    if (response.ok) {
      const data = await response.json()
      
      if (data.results && data.results.length > 0) {
        // Tomar el primer resultado
        searchedUser.value = data.results[0]
        
        // Cargar historial del usuario
        try {
          const historyResponse = await fetch(`/api/moderation/user/${searchedUser.value.roblox_id}/`)
          if (historyResponse.ok) {
            userHistory.value = await historyResponse.json()
          } else {
            // Si no hay historial específico, crear uno vacío
            userHistory.value = { active_warns: [], active_bans: [] }
          }
        } catch (historyError) {
          console.error('Error cargando historial:', historyError)
          userHistory.value = { active_warns: [], active_bans: [] }
        }
      } else {
        showNotification('INFO', 'No se encontraron usuarios', 'info', 3000)
      }
    } else if (response.status === 404) {
      showNotification('INFO', 'Usuario no encontrado', 'info', 3000)
    } else {
      showNotification('ERROR', 'Error en la búsqueda', 'error', 4000)
    }
  } catch (error) {
    console.error('Error buscando usuario:', error)
    showNotification('ERROR', 'Error al buscar usuario', 'error', 4000)
  } finally {
    loadingUser.value = false
  }
}

const warnSearchedUser = () => {
  if (searchedUser.value && canCreateWarn()) {
    newWarn.target_id = searchedUser.value.roblox_id.toString() 
    openCreateWarnModal()
  } else if (!canCreateWarn()) {
    showNotification('ACCESO DENEGADO', 'Requieres nivel MOD_JUNIOR o superior para crear advertencias', 'error', 4000)
  }
}

const banSearchedUser = () => {
  if (searchedUser.value && canCreateBan()) {
    newBan.target_id = searchedUser.value.roblox_id.toString() 
    openCreateBanModal()
  } else if (!canCreateBan()) {
    showNotification('ACCESO DENEGADO', 'Requieres nivel MOD_OFFICIAL o superior para crear baneos', 'error', 4000)
  }
}

const viewUserHistory = () => {
  if (userHistory.value) {
    const historySection = document.querySelector('.user-history')
    if (historySection) {
      historySection.scrollIntoView({ behavior: 'smooth' })
    }
  }
}

// Utilidades
const getSeverityText = (severity) => {
  switch(severity) {
    case 1: return 'BAJA'
    case 2: return 'MEDIA'
    case 3: return 'ALTA'
    default: return 'DESCONOCIDA'
  }
}

const getStatusText = (status) => {
  const statusMap = {
    'active': 'Activa',
    'appealed': 'Apelada',
    'expired': 'Expirada',
    'removed': 'Eliminada',
    'revoked': 'Revocada'
  }
  return statusMap[status] || status
}

const truncateText = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

const formatDateShort = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES')
}

const formatDateFull = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('es-ES', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatRelativeTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  
  if (diffMins < 60) return `hace ${diffMins} min`
  if (diffHours < 24) return `hace ${diffHours} horas`
  return `hace ${diffDays} días`
}

const isExpiringSoon = (dateString) => {
  if (!dateString) return false
  const date = new Date(dateString)
  const now = new Date()
  const diffDays = (date - now) / 86400000
  return diffDays > 0 && diffDays <= 7 // Expira en menos de 7 días
}

const isAppealUrgent = (appeal) => {
  if (!appeal.appealed_at) return false
  const appealedDate = new Date(appeal.appealed_at)
  const now = new Date()
  const diffDays = (now - appealedDate) / 86400000
  return diffDays >= 3 // Apelación pendiente por más de 3 días
}

const refreshWarns = () => {
  loadWarns()
  showNotification('INFO', 'Advertencias actualizadas', 'info', 2000)
}

const refreshBans = () => {
  loadBans()
  showNotification('INFO', 'Baneos actualizados', 'info', 2000)
}

// Notificaciones
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

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
  }
}

// CSRF Token
const getCSRFToken = () => {
  // Try to get from cookies first
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
  
  if (cookieValue) return cookieValue;
  
  // Try meta tag
  const metaTag = document.querySelector('meta[name="csrf-token"]');
  if (metaTag) return metaTag.content;
  
  // Try X-CSRFToken header
  const csrfInput = document.querySelector('[name="csrfmiddlewaretoken"]');
  if (csrfInput) return csrfInput.value;
  
  console.warn('CSRF token not found. Using fallback.');
  return 'fallback-csrf-token-for-debug'; // Only for debugging
}

// Tiempo
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('es-ES', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  }).replace(/(\d+)\/(\d+)\/(\d+),/, '$3-$1-$2')
}

// Usuario actual
const fetchCurrentUser = async () => {
  try {
    const response = await fetch('/api/auth/user/')
    if (response.ok) {
      const data = await response.json()
      currentUser.value = data
      
      // Después de cargar el usuario, cargar sus permisos
      if (data.is_authenticated) {
        fetchUserPermissions()
      }
    }
  } catch (error) {
    console.error('Error obteniendo usuario:', error)
  }
}

// Lifecycle
onMounted(() => {
  updateTime()
  const timeInterval = setInterval(updateTime, 1000)
  
  fetchCurrentUser()
  
  return () => {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
/* Estilos base similares a los otros componentes SCP */
.moderacion-global-page {
  position: relative;
  min-height: 100vh;
  color: #d8d8d8;
  background: #0a0a0a;
  font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.5;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
}

/* Fondo SCP */
.site-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: 
    linear-gradient(135deg, #0a0a0a 0%, #121212 25%, #0a0a0a 50%, #121212 75%, #0a0a0a 100%),
    radial-gradient(circle at 20% 30%, rgba(30, 30, 30, 0.8) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(40, 40, 40, 0.6) 0%, transparent 50%);
  z-index: 0;
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(60, 60, 60, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(60, 60, 60, 0.1) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: gridMove 20s linear infinite;
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 10% 20%, rgba(100, 100, 100, 0.05) 1px, transparent 1px),
    radial-gradient(circle at 90% 80%, rgba(100, 100, 100, 0.05) 1px, transparent 1px);
  background-size: 30px 30px;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(80, 80, 80, 0.8) 10%, 
    rgba(120, 120, 120, 0.9) 50%, 
    rgba(80, 80, 80, 0.8) 90%, 
    transparent 100%);
  animation: scan 6s linear infinite;
  z-index: 1;
  opacity: 0.3;
}

@keyframes scan {
  0% { top: 0%; }
  100% { top: 100%; }
}

@keyframes gridMove {
  0% { transform: translateY(0); }
  100% { transform: translateY(40px); }
}

/* Header */
.moderacion-global-header {
  position: relative;
  z-index: 2;
  background: rgba(15, 15, 15, 0.98);
  border-bottom: 1px solid #333;
  padding: 2rem 2rem 1rem 2rem;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.5);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1600px;
  margin: 0 auto;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.header-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  border-radius: 2px;
}

.header-icon svg {
  width: 28px;
  height: 28px;
  color: #ff3333;
}

.header-title {
  display: flex;
  flex-direction: column;
}

.header-main {
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: #ff3333;
  text-transform: uppercase;
  line-height: 1.2;
}

.header-sub {
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  color: #888;
  text-transform: uppercase;
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
  border-radius: 0px;
  background: #4CAF50;
  box-shadow: 0 0 6px #4CAF50;
  animation: pulse 2s infinite;
}

.session-text {
  font-size: 11px;
  color: #4CAF50;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  font-weight: 600;
}

.current-time {
  font-size: 11px;
  color: #888;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.3px;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.back-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  color: #aaa;
  font-family: 'Consolas', monospace;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  min-width: 160px;
}

.back-button:hover {
  background: rgba(50, 50, 50, 0.7);
  border-color: #555;
  color: #fff;
}

.back-button svg {
  width: 16px;
  height: 16px;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

/* Navegación */
.moderacion-global-nav {
  position: relative;
  z-index: 2;
  background: rgba(20, 20, 20, 0.95);
  border-bottom: 1px solid #333;
  padding: 1rem 2rem;
  backdrop-filter: blur(10px);
}

.nav-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.nav-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  padding: 0.8rem 1.5rem;
  background: rgba(30, 30, 30, 0.9);
  border: 1px solid #444;
  color: #aaa;
  font-family: inherit;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  flex-shrink: 0;
}

.nav-button:hover:not(:disabled) {
  background: rgba(40, 40, 40, 0.95);
  border-color: #666;
  color: #ddd;
}

.nav-button.active {
  background: rgba(255, 51, 51, 0.1);
  border-color: #ff3333;
  color: #ff3333;
}

.nav-icon {
  width: 18px;
  height: 18px;
  color: currentColor;
}

.nav-text {
  font-weight: 600;
  font-family: 'Consolas', monospace;
}

.nav-info {
  display: flex;
  gap: 2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-label {
  font-size: 11px;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.info-value {
  font-size: 12px;
  color: #ddd;
  font-weight: 600;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

/* Estilos para diferentes niveles de permiso */
.junior-mod {
  color: #4CAF50;
  font-weight: bold;
  text-shadow: 0 0 3px rgba(76, 175, 80, 0.3);
}

.official-mod {
  color: #2196F3;
  font-weight: bold;
  text-shadow: 0 0 3px rgba(33, 150, 243, 0.3);
}

.qualified-mod {
  color: #FF9800;
  font-weight: bold;
  text-shadow: 0 0 3px rgba(255, 152, 0, 0.3);
}

.senior-mod {
  color: #9C27B0;
  font-weight: bold;
  text-shadow: 0 0 3px rgba(156, 39, 176, 0.3);
}

.admin {
  color: #ff3333;
  font-weight: bold;
  text-shadow: 0 0 5px rgba(255, 51, 51, 0.3);
}

.staff {
  color: #607D8B;
  font-weight: bold;
}

.observador {
  color: #9E9E9E;
  font-style: italic;
}

.info-value.operational {
  color: #4CAF50;
}

/* Contenido Principal */
.moderacion-global-main {
  position: relative;
  z-index: 2;
  flex: 1;
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

/* Overlay de autenticación */
.auth-modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.95);
  backdrop-filter: blur(10px);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

/* Pestañas de contenido */
.tab-header {
  padding: 2rem 0;
  border-bottom: 1px solid #333;
  margin-bottom: 2rem;
}

.tab-title {
  font-size: 2rem;
  font-weight: 700;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 0.5rem 0;
  font-family: 'Consolas', 'Courier New', monospace;
}

.tab-subtitle {
  font-size: 1rem;
  color: #aaa;
  letter-spacing: 0.3px;
}

.pagination-info,
.pending-count {
  color: #888;
  font-size: 0.9rem;
  margin-left: 1rem;
}

/* Barra de acciones */
.action-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.search-container {
  flex: 1;
  position: relative;
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  padding: 0.8rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  min-width: 300px;
}

.search-container:focus-within {
  border-color: #ff3333;
  box-shadow: 0 0 0 2px rgba(255, 51, 51, 0.1);
}

.search-icon {
  width: 18px;
  height: 18px;
  color: #888;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 0.9rem;
  font-family: inherit;
  outline: none;
}

.search-input::placeholder {
  color: #666;
}

.search-clear {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  padding: 0.3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.search-clear:hover {
  color: #ff3333;
}

.search-clear svg {
  width: 16px;
  height: 16px;
}

.search-info {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.search-count {
  font-size: 0.8rem;
  color: #888;
  font-family: 'Consolas', monospace;
  white-space: nowrap;
}

.action-buttons {
  display: flex;
  gap: 0.8rem;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-family: 'Consolas', monospace;
}

.action-button.primary {
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  color: #ff3333;
}

.action-button.primary:hover:not(:disabled) {
  background: rgba(255, 51, 51, 0.2);
  border-color: rgba(255, 51, 51, 0.5);
}

.action-button.secondary {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  color: #aaa;
}

.action-button.secondary:hover:not(:disabled) {
  background: rgba(50, 50, 50, 0.7);
  border-color: #555;
  color: #fff;
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-icon {
  width: 16px;
  height: 16px;
  color: currentColor;
}

/* Filtros */
.filters-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  padding: 1rem;
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.filter-select,
.filter-date {
  background: rgba(40, 40, 40, 0.8);
  border: 1px solid #444;
  color: #fff;
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
  font-family: inherit;
  outline: none;
  transition: border-color 0.3s ease;
}

.filter-select:hover,
.filter-date:hover {
  border-color: #555;
}

.filter-select:focus,
.filter-date:focus {
  border-color: #ff3333;
}

.filter-date {
  min-width: 120px;
}

.date-separator {
  color: #666;
  margin: 0 0.5rem;
}

/* Modal de respuesta a apelación */
.appeal-response-modal {
  max-width: 800px;
}

.appeal-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #444;
}

.info-row {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.info-label {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.info-value {
  font-size: 0.9rem;
  color: #ddd;
  font-weight: 500;
  word-break: break-word;
}

.section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.section-title {
  font-size: 0.9rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 1rem 0;
  font-family: 'Consolas', monospace;
}

.section-content {
  color: #ccc;
  line-height: 1.5;
}

.evidence-text {
  white-space: pre-wrap;
  word-break: break-word;
  padding: 1rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 2px;
}

.response-form {
  margin-top: 2rem;
}

.form-group {
  margin-bottom: 2rem;
}

.form-label {
  display: block;
  font-size: 0.9rem;
  color: #ccc;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin-bottom: 0.5rem;
  font-family: 'Consolas', monospace;
}

.form-hint {
  font-size: 0.85rem;
  color: #888;
  margin: 0 0 1rem 0;
  line-height: 1.4;
}

.form-textarea {
  width: 100%;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  padding: 1rem;
  color: #fff;
  font-size: 0.9rem;
  font-family: inherit;
  transition: all 0.3s ease;
  resize: vertical;
  min-height: 150px;
}

.form-textarea:focus {
  outline: none;
  border-color: #ff3333;
  box-shadow: 0 0 0 2px rgba(255, 51, 51, 0.1);
}

.response-tips {
  padding: 1.5rem;
  background: rgba(255, 152, 0, 0.05);
  border: 1px solid rgba(255, 152, 0, 0.2);
  border-radius: 2px;
  margin-bottom: 2rem;
}

.response-tips h4 {
  color: #FF9800;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 1rem 0;
  font-family: 'Consolas', monospace;
  font-size: 0.9rem;
}

.response-tips ul {
  margin: 0;
  padding-left: 1.5rem;
  color: #ccc;
  font-size: 0.85rem;
  line-height: 1.5;
}

.response-tips li {
  margin-bottom: 0.5rem;
}

.response-tips li:last-child {
  margin-bottom: 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 2rem;
  border-top: 1px solid #444;
}

/* Contenedor de tabla */
.table-container {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  min-height: 400px;
  display: flex;
  flex-direction: column;
}

.loading-state,
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 51, 51, 0.3);
  border-top: 3px solid #ff3333;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 1rem;
  color: #aaa;
  margin: 0;
}

.empty-icon {
  width: 60px;
  height: 60px;
  color: #ff3333;
  opacity: 0.8;
  margin-bottom: 1.5rem;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1rem 0;
}

.empty-text {
  font-size: 1rem;
  color: #aaa;
  margin: 0 0 2rem 0;
  max-width: 400px;
}

/* Tablas SCP */
.scp-table {
  width: 100%;
  border-collapse: collapse;
}

.scp-table thead {
  background: rgba(30, 30, 30, 0.9);
  border-bottom: 2px solid #444;
}

.scp-table th {
  padding: 1rem;
  text-align: left;
  font-size: 0.85rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-weight: 600;
  font-family: 'Consolas', monospace;
}

.scp-table tbody tr {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: background-color 0.3s ease;
}

.scp-table tbody tr:hover {
  background: rgba(255, 51, 51, 0.05);
}

.scp-table td {
  padding: 1rem;
  vertical-align: middle;
}

/* Celdas específicas */
.id-cell .id-badge {
  background: rgba(255, 51, 51, 0.1);
  color: #ff3333;
  padding: 0.3rem 0.6rem;
  border-radius: 2px;
  font-family: 'Consolas', monospace;
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-block;
}

.user-cell .user-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.username {
  font-weight: 600;
  color: #fff;
}

.user-id {
  font-size: 0.75rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.moderator-cell .unknown {
  color: #888;
  font-style: italic;
}

.reason-cell {
  max-width: 250px;
}

.reason-text {
  color: #ccc;
  line-height: 1.4;
  margin-bottom: 0.3rem;
}

.evidence-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
  padding: 0.2rem 0.4rem;
  border-radius: 2px;
  font-size: 0.7rem;
  cursor: help;
}

.evidence-badge svg {
  width: 12px;
  height: 12px;
}

/* Badges de severidad */
.severity-badge {
  padding: 0.3rem 0.6rem;
  border-radius: 2px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
  display: inline-block;
}

.severity-1 {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.severity-2 {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

.severity-3 {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

/* Badges de estado */
.status-badge {
  padding: 0.3rem 0.6rem;
  border-radius: 2px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
  display: inline-block;
}

.status-active {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.status-appealed {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
  border: 1px solid rgba(33, 150, 243, 0.3);
}

.status-expired {
  background: rgba(158, 158, 158, 0.1);
  color: #9E9E9E;
  border: 1px solid rgba(158, 158, 158, 0.3);
}

.status-removed {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.status-revoked {
  background: rgba(158, 158, 158, 0.1);
  color: #9E9E9E;
  border: 1px solid rgba(158, 158, 158, 0.3);
}

/* Badges de tipo */
.type-badge {
  padding: 0.3rem 0.6rem;
  border-radius: 2px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
  display: inline-block;
}

.type-temporary {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

.type-permanent {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.status-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.appealed-indicator {
  width: 16px;
  height: 16px;
  color: #2196F3;
  cursor: help;
}

.date-cell {
  font-family: 'Consolas', monospace;
  font-size: 0.85rem;
  color: #ccc;
}

.expiring-soon {
  color: #ff3333;
  font-weight: 700;
}

.no-expiry,
.permanent {
  color: #888;
  font-style: italic;
}

/* Acciones de tabla */
.actions-cell {
  display: flex;
  gap: 0.5rem;
}

.table-action {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  color: #aaa;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.table-action:hover:not(:disabled) {
  background: rgba(50, 50, 50, 0.8);
  border-color: #555;
}

.table-action.view:hover:not(:disabled) {
  color: #2196F3;
}

.table-action.edit:hover:not(:disabled) {
  color: #FF9800;
}

.table-action.remove:hover:not(:disabled),
.table-action.revoke:hover:not(:disabled) {
  color: #f44336;
}

.table-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.table-action svg {
  width: 16px;
  height: 16px;
}

/* Paginación */
.pagination-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(25, 25, 25, 0.8);
}

.pagination-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: rgba(30, 30, 30, 0.9);
  border: 1px solid #444;
  color: #aaa;
  font-family: 'Consolas', monospace;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 140px;
}

.pagination-button:hover:not(:disabled) {
  background: rgba(40, 40, 40, 0.95);
  border-color: #666;
  color: #ddd;
}

.pagination-button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.pagination-button svg {
  width: 16px;
  height: 16px;
}

.page-numbers {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-info {
  font-family: 'Consolas', monospace;
  font-size: 0.9rem;
  color: #888;
  letter-spacing: 0.3px;
}

/* Apelaciones */
.appeals-container {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  min-height: 400px;
}

.appeals-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1.5rem;
}

.appeal-card {
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.appeal-card:hover {
  border-color: #555;
  background: rgba(35, 35, 35, 0.9);
}

.appeal-card.expiring-soon {
  border-color: #ff3333;
  background: rgba(255, 51, 51, 0.05);
}

.appeal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.appeal-info {
  flex: 1;
}

.appeal-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.urgent-badge {
  background: rgba(255, 51, 51, 0.1);
  color: #ff3333;
  padding: 0.2rem 0.5rem;
  border-radius: 2px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.appeal-meta {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #aaa;
}

.meta-item svg {
  width: 14px;
  height: 14px;
}

.appeal-actions {
  display: flex;
  gap: 0.5rem;
}

.appeal-action {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  color: #ff3333;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Consolas', monospace;
}

.appeal-action:hover {
  background: rgba(255, 51, 51, 0.2);
  border-color: rgba(255, 51, 51, 0.5);
}

.appeal-action svg {
  width: 16px;
  height: 16px;
}

.appeal-content {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 1rem;
}

.appeal-reason,
.appeal-evidence {
  margin-bottom: 1rem;
}

.appeal-reason h5,
.appeal-evidence h5 {
  font-size: 0.9rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 0.5rem 0;
  font-family: 'Consolas', monospace;
}

.appeal-reason p,
.evidence-text {
  color: #ccc;
  line-height: 1.5;
  margin: 0;
}

/* Búsqueda de usuario */
.user-search-container {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  min-height: 400px;
}

.search-panel {
  padding: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.search-input-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.user-search-input {
  flex: 1;
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  padding: 0.8rem 1rem;
  color: #fff;
  font-size: 1rem;
  font-family: inherit;
  outline: none;
  transition: border-color 0.3s ease;
}

.user-search-input:focus {
  border-color: #ff3333;
  box-shadow: 0 0 0 2px rgba(255, 51, 51, 0.1);
}

.search-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  color: #ff3333;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Consolas', monospace;
}

.search-button:hover {
  background: rgba(255, 51, 51, 0.2);
  border-color: rgba(255, 51, 51, 0.5);
}

.search-button svg {
  width: 16px;
  height: 16px;
}

.search-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #666;
  font-size: 0.85rem;
}

.search-hint svg {
  width: 16px;
  height: 16px;
}

/* Perfil de usuario */
.user-profile {
  padding: 2rem;
}

.profile-header {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.profile-avatar {
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  background: rgba(255, 51, 51, 0.1);
  border: 2px solid rgba(255, 51, 51, 0.3);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-placeholder svg {
  width: 40px;
  height: 40px;
  color: #ff3333;
}

.profile-info {
  flex: 1;
}

.profile-username {
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 0.5rem 0;
}

.profile-id {
  font-size: 1rem;
  color: #888;
  font-family: 'Consolas', monospace;
  margin-bottom: 1rem;
}

.profile-stats {
  display: flex;
  gap: 2rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.stat-label {
  font-size: 0.8rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  font-family: 'Consolas', monospace;
}

.stat-value.has-warns {
  color: #ff3333;
}

.stat-value.banned {
  color: #f44336;
}

.profile-actions {
  display: flex;
  gap: 0.8rem;
  align-self: flex-start;
}

.profile-action {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-family: 'Consolas', monospace;
}

.profile-action.warn {
  background: rgba(255, 152, 0, 0.1);
  border: 1px solid rgba(255, 152, 0, 0.3);
  color: #FF9800;
}

.profile-action.warn:hover:not(:disabled) {
  background: rgba(255, 152, 0, 0.2);
  border-color: rgba(255, 152, 0, 0.5);
}

.profile-action.ban {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  color: #f44336;
}

.profile-action.ban:hover:not(:disabled) {
  background: rgba(244, 67, 54, 0.2);
  border-color: rgba(244, 67, 54, 0.5);
}

.profile-action.view {
  background: rgba(33, 150, 243, 0.1);
  border: 1px solid rgba(33, 150, 243, 0.3);
  color: #2196F3;
}

.profile-action.view:hover {
  background: rgba(33, 150, 243, 0.2);
  border-color: rgba(33, 150, 243, 0.5);
}

.profile-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.profile-action svg {
  width: 16px;
  height: 16px;
}

/* Historial del usuario */
.user-history {
  padding: 1.5rem;
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
}

.history-title {
  font-size: 1.2rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1.5rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255, 51, 51, 0.3);
}

.history-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1rem;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 1rem 0;
  font-family: 'Consolas', monospace;
}

.warns-list,
.bans-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.history-item {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  padding: 1rem;
}

.history-item.warn {
  border-left: 3px solid #FF9800;
}

.history-item.ban {
  border-left: 3px solid #f44336;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.item-id {
  font-weight: 600;
  color: #fff;
  font-family: 'Consolas', monospace;
}

.item-severity,
.item-type {
  padding: 0.2rem 0.5rem;
  border-radius: 2px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.item-date {
  font-size: 0.8rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.item-content {
  margin-top: 0.5rem;
}

.item-reason {
  color: #ccc;
  line-height: 1.5;
  margin: 0 0 0.5rem 0;
}

.item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: #888;
}

.no-history,
.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.no-history-icon,
.no-results-icon {
  width: 60px;
  height: 60px;
  margin-bottom: 1.5rem;
}

.no-results-icon {
  color: #ff3333;
}

.no-history-text,
.no-results-text {
  font-size: 1rem;
  color: #aaa;
  margin: 0;
}

.no-results-title {
  font-size: 1.5rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1rem 0;
}

/* Modales */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: rgba(25, 25, 25, 0.95);
  border: 1px solid #333;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: slideIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  padding: 1.5rem 2rem;
  background: rgba(30, 30, 30, 0.9);
  border-bottom: 1px solid #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0;
  font-family: 'Consolas', 'Courier New', monospace;
}

.modal-close {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s ease;
}

.modal-close:hover {
  color: #fff;
}

.modal-close svg {
  width: 20px;
  height: 20px;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

/* Modal de crear warn */
.create-warn-modal {
  max-width: 600px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-size: 0.9rem;
  color: #ccc;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin-bottom: 0.5rem;
  font-family: 'Consolas', monospace;
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  padding: 0.8rem;
  color: #fff;
  font-size: 0.9rem;
  font-family: inherit;
  transition: all 0.3s ease;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #ff3333;
  box-shadow: 0 0 0 2px rgba(255, 51, 51, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #444;
}

.cancel-button,
.submit-button {
  padding: 0.8rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-family: 'Consolas', monospace;
}

.cancel-button {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  color: #aaa;
}

.cancel-button:hover {
  background: rgba(50, 50, 50, 0.7);
  border-color: #555;
  color: #fff;
}

.submit-button {
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  color: #ff3333;
}

.submit-button:hover:not(:disabled) {
  background: rgba(255, 51, 51, 0.2);
  border-color: rgba(255, 51, 51, 0.5);
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal de detalles de warn */
.warn-details-modal {
  max-width: 700px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.detail-label {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.detail-value {
  font-size: 0.9rem;
  color: #ddd;
  font-weight: 500;
  word-break: break-word;
}

.details-section {
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.details-section:last-child {
  border-bottom: none;
}

.section-title {
  font-size: 0.9rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 0.8rem 0;
  font-family: 'Consolas', monospace;
}

.section-content {
  color: #ccc;
  line-height: 1.5;
}

.evidence-text {
  white-space: pre-wrap;
  word-break: break-word;
  padding: 1rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 2px;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.modal-actions .action-button {
  flex: 1;
  padding: 0.8rem;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-family: 'Consolas', monospace;
}

.modal-actions .action-button.primary {
  background: rgba(33, 150, 243, 0.1);
  border: 1px solid rgba(33, 150, 243, 0.3);
  color: #2196F3;
}

.modal-actions .action-button.primary:hover:not(:disabled) {
  background: rgba(33, 150, 243, 0.2);
  border-color: rgba(33, 150, 243, 0.5);
}

.modal-actions .action-button.secondary {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  color: #f44336;
}

.modal-actions .action-button.secondary:hover:not(:disabled) {
  background: rgba(244, 67, 54, 0.2);
  border-color: rgba(244, 67, 54, 0.5);
}

.modal-actions .action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Sistema de notificaciones SCP */
.scp-notifications {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 400px;
  pointer-events: none;
}

.scp-notification {
  background: linear-gradient(135deg, 
    rgba(20, 20, 20, 0.95) 0%, 
    rgba(30, 30, 30, 0.95) 100%);
  border: 1px solid #333;
  border-left: 4px solid #ff3333;
  padding: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  position: relative;
  overflow: hidden;
  pointer-events: auto;
  cursor: pointer;
  transition: all 0.3s ease;
  animation: slideInRight 0.3s ease;
}

.scp-notification:hover {
  transform: translateX(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6);
}

.scp-notification.type-success {
  border-left-color: #4CAF50;
}

.scp-notification.type-error {
  border-left-color: #ff3333;
}

.scp-notification.type-info {
  border-left-color: #2196F3;
}

.notification-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 0.8rem;
}

.notification-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.scp-notification.type-success .notification-icon {
  color: #4CAF50;
}

.scp-notification.type-error .notification-icon {
  color: #ff3333;
}

.scp-notification.type-info .notification-icon {
  color: #2196F3;
}

.notification-title {
  flex: 1;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #fff;
  font-family: 'Consolas', monospace;
}

.notification-close {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  padding: 0.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s ease;
}

.notification-close:hover {
  color: #fff;
}

.notification-close svg {
  width: 16px;
  height: 16px;
}

.notification-content {
  font-size: 0.9rem;
  color: #ccc;
  line-height: 1.4;
  margin-bottom: 0.5rem;
}

.notification-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    #ff3333 50%, 
    transparent 100%);
  animation: progressBar linear forwards;
}

.scp-notification.type-success .notification-progress {
  background: linear-gradient(90deg, 
    transparent 0%, 
    #4CAF50 50%, 
    transparent 100%);
}

.scp-notification.type-error .notification-progress {
  background: linear-gradient(90deg, 
    transparent 0%, 
    #ff3333 50%, 
    transparent 100%);
}

.scp-notification.type-info .notification-progress {
  background: linear-gradient(90deg, 
    transparent 0%, 
    #2196F3 50%, 
    transparent 100%);
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes progressBar {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(100%);
  }
}

.notification-slide-enter-active,
.notification-slide-leave-active {
  transition: all 0.3s ease;
}

.notification-slide-enter-from,
.notification-slide-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

/* Responsive */
@media (max-width: 768px) {
  .moderacion-global-header,
  .moderacion-global-nav,
  .moderacion-global-main {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .header-right {
    align-items: center;
  }
  
  .nav-controls {
    justify-content: center;
  }
  
  .action-bar {
    flex-direction: column;
  }
  
  .search-container {
    min-width: 100%;
  }
  
  .filters-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-group {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-date {
    width: 100%;
  }
  
  .scp-table {
    display: block;
    overflow-x: auto;
  }
  
  .scp-table th,
  .scp-table td {
    white-space: nowrap;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .profile-actions {
    justify-content: center;
    flex-wrap: wrap;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    max-height: 95vh;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .moderacion-global-main {
    padding: 1.5rem;
  }
}
</style>