<template>
  <div class="audit-logs-page">
    <!-- Fondo SCP -->
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
    </div>

    <!-- Header -->
    <header class="audit-logs-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-logo">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
            </div>
            <div class="header-title">
              <span class="header-main">AUDIT LOG SYSTEM</span>
              <span class="header-sub">REGISTRO COMPLETO DE ACTIVIDAD DEL SISTEMA</span>
            </div>
          </div>
        </div>
        
        <div class="header-right">
          <div class="session-status">
            <div class="session-indicator active"></div>
            <span class="session-text">SISTEMA DE AUDITORÍA ACTIVO</span>
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
    <nav class="audit-logs-nav">
      <div class="nav-controls">
        <button 
          class="nav-button" 
          :class="{ 'active': activeCategory === 'all' }"
          @click="setActiveCategory('all')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="8" y1="6" x2="21" y2="6"></line>
              <line x1="8" y1="12" x2="21" y2="12"></line>
              <line x1="8" y1="18" x2="21" y2="18"></line>
              <line x1="3" y1="6" x2="3.01" y2="6"></line>
              <line x1="3" y1="12" x2="3.01" y2="12"></line>
              <line x1="3" y1="18" x2="3.01" y2="18"></line>
            </svg>
          </div>
          <span class="nav-text">TODOS LOS LOGS</span>
        </button>
        
        <button 
          class="nav-button" 
          :class="{ 'active': activeCategory === 'moderation' }"
          @click="setActiveCategory('moderation')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
          </div>
          <span class="nav-text">MODERACIÓN</span>
        </button>
        
        <button 
          class="nav-button" 
          :class="{ 'active': activeCategory === 'permissions' }"
          @click="setActiveCategory('permissions')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <span class="nav-text">PERMISOS</span>
        </button>
        
        <button 
          class="nav-button" 
          :class="{ 'active': activeCategory === 'characters' }"
          @click="setActiveCategory('characters')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <span class="nav-text">PERSONAJES</span>
        </button>
        
        <button 
          class="nav-button" 
          :class="{ 'active': activeCategory === 'system' }"
          @click="setActiveCategory('system')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
              <line x1="8" y1="21" x2="16" y2="21"></line>
              <line x1="12" y1="17" x2="12" y2="21"></line>
            </svg>
          </div>
          <span class="nav-text">SISTEMA</span>
        </button>
      </div>
      
      <div class="nav-info">
        <div class="info-item">
          <span class="info-label">AUDITOR:</span>
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
          <span class="info-label">REGISTROS:</span>
          <span class="info-value" :class="{ 'warning': totalLogs > 10000 }">
            {{ totalLogs.toLocaleString() }}
          </span>
        </div>
        <div class="info-item">
          <span class="info-label">ACTIVIDAD:</span>
          <span class="info-value operational">{{ activityStatus }}</span>
        </div>
      </div>
    </nav>

    <!-- Contenido Principal -->
    <main class="audit-logs-main">
      <!-- Overlay de autenticación -->
      <div v-if="!currentUser?.is_authenticated || !hasAdminPermission()" class="auth-modal-overlay">
        <Login_Required 
          :redirect-path="'/audit-logs/'"
          :user="currentUser"
          :required-permission="'full_moderation_control'"
        />
      </div>
      
      <!-- Contenido autenticado -->
      <div v-else class="authenticated-content">
        <div class="tab-header">
          <h2 class="tab-title">REGISTRO DE AUDITORÍA DEL SISTEMA</h2>
          <div class="tab-subtitle">
            Registro completo de todas las acciones realizadas en el sistema
            <span v-if="pagination.total > 0" class="pagination-info">
              | Página {{ pagination.currentPage }} de {{ pagination.totalPages }} ({{ pagination.total }} registros)
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
              v-model="searchQuery"
              @input="handleSearch"
              type="text"
              placeholder="Buscar por usuario, acción, detalles..."
              class="search-input"
            />
            
            <button 
              v-if="searchQuery" 
              @click="clearSearch"
              class="search-clear"
              title="Limpiar búsqueda"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
            
            <div class="search-info">
              <div class="search-count" v-if="displayedLogs.length > 0">
                {{ displayedLogs.length }} {{ displayedLogs.length === 1 ? 'registro' : 'registros' }} encontrados
              </div>
            </div>
          </div>
          
          <div class="action-buttons">
            <button 
              class="action-button primary"
              @click="exportLogs"
              :disabled="loading"
              title="Exportar logs a CSV"
            >
              <div class="action-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
              </div>
              <span>EXPORTAR</span>
            </button>
            
            <button 
              class="action-button secondary"
              @click="refreshLogs"
              :disabled="loading"
            >
              <div class="action-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 4v6h-6"></path>
                  <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
                </svg>
              </div>
              <span>ACTUALIZAR</span>
            </button>
            
            <button 
              class="action-button danger"
              @click="cleanOldLogs"
              :disabled="loading"
              title="Eliminar logs antiguos (más de 30 días)"
            >
              <div class="action-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </div>
              <span>LIMPIAR</span>
            </button>
          </div>
        </div>

        <!-- Filtros avanzados -->
        <div class="filters-container">
          <div class="filter-group">
            <label class="filter-label">Tipo de Acción:</label>
            <select v-model="filters.actionType" class="filter-select" @change="applyFilters">
              <option value="all">Todos los tipos</option>
              <optgroup label="Usuarios y Permisos">
                <option value="user_login">Inicio de sesión</option>
                <option value="user_logout">Cierre de sesión</option>
                <option value="permissions_update">Actualización de permisos</option>
                <option value="role_assigned">Rol asignado</option>
                <option value="role_removed">Rol removido</option>
              </optgroup>
              <optgroup label="Moderación">
                <option value="warn_created">Advertencia creada</option>
                <option value="warn_updated">Advertencia actualizada</option>
                <option value="warn_removed">Advertencia eliminada</option>
                <option value="warn_appealed">Advertencia apelada</option>
                <option value="warn_appeal_responded">Respuesta a apelación</option>
                <option value="ban_created">Baneo creado</option>
                <option value="ban_revoked">Baneo revocado</option>
                <option value="ban_appealed">Baneo apelado</option>
                <option value="ban_appeal_responded">Respuesta a apelación de baneo</option>
              </optgroup>
              <optgroup label="Personajes">
                <option value="character_created">Personaje creado</option>
                <option value="character_updated">Personaje actualizado</option>
                <option value="character_deleted">Personaje eliminado</option>
              </optgroup>
              <optgroup label="Sistema">
                <option value="ssu_status_changed">Estado SSU cambiado</option>
                <option value="rp_file_edited">Archivo RP editado</option>
                <option value="faction_moderated">Facción moderada</option>
                <option value="actor_supervised">Actor supervisado</option>
              </optgroup>
            </select>
          </div>
          
          <div class="filter-group">
            <label class="filter-label">Usuario:</label>
            <select v-model="filters.userId" class="filter-select" @change="applyFilters">
              <option value="all">Todos los usuarios</option>
              <option v-for="user in availableUsers" :key="user.id" :value="user.id">
                {{ user.roblox_username }} ({{ user.roblox_id }})
              </option>
            </select>
          </div>
          
          <div class="filter-group">
            <label class="filter-label">Rango de fecha:</label>
            <input 
              type="date" 
              v-model="filters.startDate" 
              class="filter-date"
              @change="applyFilters"
            />
            <span class="date-separator">a</span>
            <input 
              type="date" 
              v-model="filters.endDate" 
              class="filter-date"
              @change="applyFilters"
            />
          </div>
          
          <div class="filter-group">
            <label class="filter-label">Ordenar por:</label>
            <select v-model="filters.sort" class="filter-select" @change="applyFilters">
              <option value="-created_at">Más recientes primero</option>
              <option value="created_at">Más antiguos primero</option>
              <option value="action_type">Tipo de acción (A-Z)</option>
              <option value="-action_type">Tipo de acción (Z-A)</option>
            </select>
          </div>
        </div>

        <!-- Tabla de Logs -->
        <div class="table-container">
          <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p class="loading-text">Cargando registros de auditoría...</p>
          </div>
          
          <div v-else-if="displayedLogs.length > 0" class="logs-table">
            <table class="scp-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>ACCIÓN</th>
                  <th>USUARIO</th>
                  <th>AFECTADO</th>
                  <th>DETALLES</th>
                  <th>FECHA</th>
                  <th>ACCIONES</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="log in paginatedLogs" 
                  :key="log.id" 
                  class="table-row"
                  :class="{ 'selected': selectedLog?.id === log.id }"
                  @click="selectLog(log)"
                >
                  <td class="id-cell">
                    <span class="id-badge">#{{ log.id }}</span>
                  </td>
                  <td class="action-cell">
                    <span class="action-badge" :class="getActionClass(log.action_type)">
                      {{ getActionDisplay(log.action_type) }}
                    </span>
                  </td>
                  <td class="user-cell">
                    <div class="user-info" v-if="log.action_user">
                      <span class="username">{{ log.action_user.roblox_username }}</span>
                      <span class="user-id">ID: {{ log.action_user.roblox_id }}</span>
                    </div>
                    <span v-else class="unknown">Sistema</span>
                  </td>
                  <td class="target-cell">
                    <div v-if="log.target_user" class="target-info">
                      <span class="username">{{ log.target_user.roblox_username }}</span>
                      <span class="user-id">ID: {{ log.target_user.roblox_id }}</span>
                    </div>
                    <span v-else class="no-target">N/A</span>
                  </td>
                  <td class="details-cell">
                    <div class="details-content">
                      <div class="details-preview" title="Ver detalles completos">
                        <span class="details-text">{{ getDetailsPreview(log) }}</span>
                        <svg class="details-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"></circle>
                          <line x1="12" y1="16" x2="12" y2="12"></line>
                          <line x1="12" y1="8" x2="12.01" y2="8"></line>
                        </svg>
                      </div>
                    </div>
                  </td>
                  <td class="date-cell">
                    <span class="date-full">{{ formatDateFull(log.created_at) }}</span>
                    <span class="date-relative">{{ formatRelativeTime(log.created_at) }}</span>
                  </td>
                  <td class="actions-cell">
                    <button class="table-action view" @click.stop="selectLog(log)" title="Ver Detalles">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </button>
                    <button 
                      v-if="hasAdminPermission()"
                      class="table-action delete" 
                      @click.stop="deleteLog(log)"
                      title="Eliminar Registro"
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
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
            </div>
            <h3 class="empty-title">No se encontraron registros</h3>
            <p class="empty-text" v-if="searchQuery">
              No hay registros que coincidan con tu búsqueda
            </p>
            <p class="empty-text" v-else>
              No hay registros de auditoría disponibles
            </p>
          </div>

          <!-- Paginación de la tabla -->
          <div v-if="displayedLogs.length > pagination.pageSize" class="table-pagination">
            <div class="pagination-info-row">
              <span class="pagination-stats">
                Mostrando {{ ((pagination.currentPage - 1) * pagination.pageSize) + 1 }} a 
                {{ Math.min(pagination.currentPage * pagination.pageSize, displayedLogs.length) }} 
                de {{ displayedLogs.length }} registros
              </span>
              <div class="pagination-controls-row">
                <button 
                  class="pagination-nav first"
                  :disabled="pagination.currentPage === 1"
                  @click="goToPage(1)"
                  title="Primera página"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="11 17 6 12 11 7"></polyline>
                    <polyline points="18 17 13 12 18 7"></polyline>
                  </svg>
                </button>
                <button 
                  class="pagination-nav prev"
                  :disabled="pagination.currentPage === 1"
                  @click="goToPage(pagination.currentPage - 1)"
                  title="Página anterior"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="15 18 9 12 15 6"></polyline>
                  </svg>
                </button>
                
                <div class="page-numbers">
                  <button 
                    v-for="page in visiblePages" 
                    :key="page"
                    class="page-number"
                    :class="{ 'active': page === pagination.currentPage }"
                    @click="goToPage(page)"
                  >
                    {{ page }}
                  </button>
                  <span v-if="hasEllipsis" class="page-ellipsis">...</span>
                </div>
                
                <button 
                  class="pagination-nav next"
                  :disabled="pagination.currentPage === pagination.totalPages"
                  @click="goToPage(pagination.currentPage + 1)"
                  title="Página siguiente"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </button>
                <button 
                  class="pagination-nav last"
                  :disabled="pagination.currentPage === pagination.totalPages"
                  @click="goToPage(pagination.totalPages)"
                  title="Última página"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="13 17 18 12 13 7"></polyline>
                    <polyline points="6 17 11 12 6 7"></polyline>
                  </svg>
                </button>
              </div>
            </div>
            
            <div class="page-size-selector">
              <span class="page-size-label">Registros por página:</span>
              <select v-model="pagination.pageSize" @change="updatePageSize" class="page-size-select">
                <option value="10">10</option>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Panel de detalles debajo de la tabla -->
        <div class="details-panel-container">
          <div class="details-panel">
            <div class="details-panel-header">
              <h3 class="details-title">
                📋 DETALLES DEL REGISTRO
                <span v-if="selectedLog" class="details-id">#{{ selectedLog.id }}</span>
                <span v-else class="details-placeholder">(Selecciona un registro)</span>
              </h3>
              <button 
                v-if="selectedLog" 
                class="close-details" 
                @click="selectedLog = null"
                title="Cerrar detalles"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
            
            <div class="details-panel-content">
              <!-- Estado vacío -->
              <div v-if="!selectedLog" class="no-selection">
                <div class="no-selection-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                  </svg>
                </div>
                <h4 class="no-selection-title">SELECCIONA UN REGISTRO</h4>
                <p class="no-selection-text">
                  Haz clic en cualquier registro de la tabla para ver sus detalles completos aquí.
                </p>
              </div>
              
              <!-- Contenido del log seleccionado -->
              <div v-else class="log-details-content">
                <div class="details-grid">
                  <div class="detail-item">
                    <span class="detail-label">ID del Registro:</span>
                    <span class="detail-value">#{{ selectedLog.id }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Acción:</span>
                    <span class="detail-value action-badge" :class="getActionClass(selectedLog.action_type)">
                      {{ getActionDisplay(selectedLog.action_type) }}
                      <span class="action-code">({{ selectedLog.action_type }})</span>
                    </span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Realizado por:</span>
                    <span class="detail-value" v-if="selectedLog.action_user">
                      <strong>{{ selectedLog.action_user.roblox_username }}</strong> (ID: {{ selectedLog.action_user.roblox_id }})
                    </span>
                    <span v-else class="unknown">Sistema</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Usuario afectado:</span>
                    <span class="detail-value" v-if="selectedLog.target_user">
                      <strong>{{ selectedLog.target_user.roblox_username }}</strong> (ID: {{ selectedLog.target_user.roblox_id }})
                    </span>
                    <span v-else class="no-target">Ninguno</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Fecha y Hora:</span>
                    <span class="detail-value">{{ formatDateFull(selectedLog.created_at) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">User Agent:</span>
                    <span class="detail-value user-agent">{{ selectedLog.user_agent || 'N/A' }}</span>
                  </div>
                </div>
                
                <!-- Sección de advertencias -->
                <div v-if="selectedLog.target_warn" class="details-section">
                  <h4 class="section-title">📝 ADVERTENCIA RELACIONADA</h4>
                  <div class="section-content warning-section">
                    <div class="related-item">
                      <span class="item-label">ID de Advertencia:</span>
                      <span class="item-value">#{{ selectedLog.target_warn.id }}</span>
                    </div>
                    <div class="related-item">
                      <span class="item-label">Razón:</span>
                      <span class="item-value reason-text">{{ selectedLog.target_warn.reason }}</span>
                    </div>
                    <div class="related-item">
                      <span class="item-label">Severidad:</span>
                      <span class="item-value severity-badge" :class="`severity-${selectedLog.target_warn.severity}`">
                        {{ getSeverityText(selectedLog.target_warn.severity) }}
                      </span>
                    </div>
                  </div>
                </div>
                
                <!-- Sección de baneos -->
                <div v-if="selectedLog.target_ban" class="details-section">
                  <h4 class="section-title">🔒 BANEO RELACIONADO</h4>
                  <div class="section-content ban-section">
                    <div class="related-item">
                      <span class="item-label">ID de Baneo:</span>
                      <span class="item-value">#{{ selectedLog.target_ban.id }}</span>
                    </div>
                    <div class="related-item">
                      <span class="item-label">Razón:</span>
                      <span class="item-value reason-text">{{ selectedLog.target_ban.reason }}</span>
                    </div>
                    <div class="related-item">
                      <span class="item-label">Tipo:</span>
                      <span class="item-value type-badge" :class="`type-${selectedLog.target_ban.ban_type}`">
                        {{ selectedLog.target_ban.ban_type === 'temporary' ? 'TEMPORAL' : 'PERMANENTE' }}
                      </span>
                    </div>
                  </div>
                </div>
                
                <!-- Sección de personajes -->
                <div v-if="selectedLog.target_character" class="details-section">
                  <h4 class="section-title">🎭 PERSONAJE RELACIONADO</h4>
                  <div class="section-content character-section">
                    <div class="related-item">
                      <span class="item-label">ID de Personaje:</span>
                      <span class="item-value">#{{ selectedLog.target_character.id }}</span>
                    </div>
                    <div class="related-item">
                      <span class="item-label">Nombre en clave:</span>
                      <span class="item-value codename">{{ selectedLog.target_character.codename }}</span>
                    </div>
                    <div class="related-item">
                      <span class="item-label">Facción:</span>
                      <span class="item-value faction">{{ selectedLog.target_character.faction || 'No especificada' }}</span>
                    </div>
                  </div>
                </div>
                
                <!-- Procesador de JSON con vistas mejoradas -->
                <div class="details-section">
                  <h4 class="section-title">📄 DETALLES ADICIONALES</h4>
                  <div class="json-processor">
                    <div class="json-view-selector">
                      <button 
                        class="json-view-btn" 
                        :class="{ 'active': jsonView === 'raw' }"
                        @click="jsonView = 'raw'"
                      >
                        📋 Vista JSON
                      </button>
                      <button 
                        class="json-view-btn" 
                        :class="{ 'active': jsonView === 'parsed' }"
                        @click="jsonView = 'parsed'"
                      >
                        👁️ Vista Legible
                      </button>
                      <button 
                        class="json-view-btn copy-btn"
                        @click="copyToClipboard(formatJsonDetails(selectedLog.details))"
                      >
                        📤 Copiar
                      </button>
                    </div>
                    
                    <div v-if="jsonView === 'raw'" class="json-container">
                      <pre class="json-details">{{ formatJsonDetails(selectedLog.details) }}</pre>
                    </div>
                    
                    <div v-else class="parsed-details">
                      <div v-if="hasParsedDetails" class="parsed-content">
                        <div v-for="(value, key) in parsedDetails" :key="key" class="parsed-item">
                          <span class="parsed-key">{{ formatKey(key) }}:</span>
                          <span class="parsed-value">{{ formatValue(value) }}</span>
                        </div>
                      </div>
                      <div v-else class="no-parsed-details">
                        <p>No hay detalles adicionales o no se pueden procesar.</p>
                        <button @click="jsonView = 'raw'" class="show-raw-btn">
                          Ver JSON original
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Acciones administrativas -->
                <div class="details-actions" v-if="hasAdminPermission()">
                  <button 
                    class="action-button danger full-width"
                    @click="deleteSelectedLog"
                  >
                    🗑️ ELIMINAR REGISTRO
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { debounce } from 'lodash'
import Login_Required from '@/components/Login_Required.vue'

const router = useRouter()

// Estado principal
const activeCategory = ref('all')
const currentUser = ref(null)
const userPermissions = ref([])
const currentTime = ref('')
const loading = ref(false)
const selectedLog = ref(null)
const availableUsers = ref([])
const activityStatus = ref('NORMAL')
const jsonView = ref('parsed') // 'raw' o 'parsed'

// Búsqueda y filtros
const searchQuery = ref('')
const filters = reactive({
  actionType: 'all',
  userId: 'all',
  startDate: '',
  endDate: '',
  sort: '-created_at'
})

// Paginación
const pagination = reactive({
  currentPage: 1,
  pageSize: 25,
  total: 0,
  totalPages: 0
})

// Datos
const logs = ref([])
const notifications = ref([])
let notificationId = 0

// Computed
const displayedLogs = computed(() => {
  let filtered = logs.value
  
  // Filtrar por categoría
  if (activeCategory.value !== 'all') {
    const categoryMap = {
      'moderation': [
        'warn_created', 'warn_updated', 'warn_removed', 'warn_appealed', 'warn_appeal_responded',
        'ban_created', 'ban_revoked', 'ban_appealed', 'ban_appeal_responded'
      ],
      'permissions': [
        'permissions_update', 'role_assigned', 'role_removed', 'user_login', 'user_logout'
      ],
      'characters': [
        'character_created', 'character_updated', 'character_deleted'
      ],
      'system': [
        'ssu_status_changed', 'rp_file_edited', 'faction_moderated', 'actor_supervised'
      ]
    }
    
    filtered = filtered.filter(log => 
      categoryMap[activeCategory.value]?.includes(log.action_type) || false
    )
  }
  
  // Filtrar por tipo de acción
  if (filters.actionType !== 'all') {
    filtered = filtered.filter(log => log.action_type === filters.actionType)
  }
  
  // Filtrar por usuario
  if (filters.userId !== 'all') {
    const userId = parseInt(filters.userId)
    filtered = filtered.filter(log => 
      (log.action_user && log.action_user.id === userId) ||
      (log.target_user && log.target_user.id === userId)
    )
  }
  
  // Filtrar por rango de fecha
  if (filters.startDate) {
    const startDate = new Date(filters.startDate)
    filtered = filtered.filter(log => new Date(log.created_at) >= startDate)
  }
  
  if (filters.endDate) {
    const endDate = new Date(filters.endDate)
    endDate.setHours(23, 59, 59, 999)
    filtered = filtered.filter(log => new Date(log.created_at) <= endDate)
  }
  
  // Búsqueda
  if (searchQuery.value) {
    const searchLower = searchQuery.value.toLowerCase()
    filtered = filtered.filter(log => {
      return (
        log.action_user?.roblox_username?.toLowerCase().includes(searchLower) ||
        log.action_user?.roblox_id?.toString().includes(searchLower) ||
        log.target_user?.roblox_username?.toLowerCase().includes(searchLower) ||
        log.target_user?.roblox_id?.toString().includes(searchLower) ||
        getActionDisplay(log.action_type).toLowerCase().includes(searchLower) ||
        (log.details && JSON.stringify(log.details).toLowerCase().includes(searchLower)) ||
        log.user_agent?.toLowerCase().includes(searchLower)
      )
    })
  }
  
  // Ordenar
  if (filters.sort === '-created_at') {
    filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  } else if (filters.sort === 'created_at') {
    filtered.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
  } else if (filters.sort === 'action_type') {
    filtered.sort((a, b) => getActionDisplay(a.action_type).localeCompare(getActionDisplay(b.action_type)))
  } else if (filters.sort === '-action_type') {
    filtered.sort((a, b) => getActionDisplay(b.action_type).localeCompare(getActionDisplay(a.action_type)))
  }
  
  // Actualizar paginación
  pagination.total = filtered.length
  pagination.totalPages = Math.ceil(filtered.length / pagination.pageSize)
  
  return filtered
})

const totalLogs = computed(() => logs.value.length)

const paginatedLogs = computed(() => {
  const start = (pagination.currentPage - 1) * pagination.pageSize
  const end = start + pagination.pageSize
  return displayedLogs.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, pagination.currentPage - Math.floor(maxVisible / 2))
  let end = Math.min(pagination.totalPages, start + maxVisible - 1)
  
  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1)
  }
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

const hasEllipsis = computed(() => {
  return pagination.totalPages > visiblePages.value.length && 
         visiblePages.value[visiblePages.value.length - 1] < pagination.totalPages
})

const parsedDetails = computed(() => {
  if (!selectedLog.value || !selectedLog.value.details) {
    return {}
  }
  
  try {
    const details = typeof selectedLog.value.details === 'string' 
      ? JSON.parse(selectedLog.value.details) 
      : selectedLog.value.details
    
    // Procesar detalles para hacerlos más legibles
    const processed = {}
    
    for (const [key, value] of Object.entries(details)) {
      // Formatear claves
      const formattedKey = key
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase())
      
      // Procesar valores
      let formattedValue = value
      
      if (typeof value === 'boolean') {
        formattedValue = value ? 'Sí' : 'No'
      } else if (typeof value === 'object' && value !== null) {
        formattedValue = JSON.stringify(value, null, 2)
      } else if (typeof value === 'string') {
        // Intentar parsear strings que podrían ser JSON
        if (value.startsWith('{') || value.startsWith('[')) {
          try {
            const parsed = JSON.parse(value)
            formattedValue = typeof parsed === 'object' ? JSON.stringify(parsed, null, 2) : value
          } catch {
            formattedValue = value
          }
        }
      }
      
      processed[formattedKey] = formattedValue
    }
    
    return processed
  } catch (error) {
    console.error('Error procesando detalles:', error)
    return {}
  }
})

const hasParsedDetails = computed(() => {
  return Object.keys(parsedDetails.value).length > 0
})

// Métodos de permisos
const fetchUserPermissions = async () => {
  try {
    const response = await fetch('/api/auth/user/permissions/')
    if (response.ok) {
      const data = await response.json()
      userPermissions.value = data.permissions || []
      
      if (currentUser.value) {
        currentUser.value.permissions = data.permissions || []
      }
    }
  } catch (error) {
    console.error('Error cargando permisos:', error)
  }
}

const hasAdminPermission = () => {
  if (!currentUser.value || !currentUser.value.is_authenticated) return false
  
  if (currentUser.value.is_superuser) return true
  
  return userPermissions.value.includes('full_moderation_control')
}

const getUserPermissionLevel = () => {
  if (!currentUser.value) return 'INVITADO'
  
  if (currentUser.value.is_superuser) return 'ADMIN'
  
  const permissions = userPermissions.value || []
  
  if (permissions.includes('full_moderation_control')) return 'MOD_SENIOR'
  if (permissions.includes('manage_warns')) return 'MOD_QUALIFIED'
  if (permissions.includes('register_ban')) return 'MOD_OFFICIAL'
  if (permissions.includes('create_warn')) return 'MOD_JUNIOR'
  if (permissions.includes('access_moderation_dashboard')) return 'OBSERVADOR'
  if (currentUser.value.is_staff) return 'STAFF'
  
  return 'INVITADO'
}

// Navegación
const setActiveCategory = (category) => {
  activeCategory.value = category
  pagination.currentPage = 1
}

const goToModerationPanel = () => {
  router.push('/moderation')
}

// Carga de datos
const loadLogs = async () => {
  if (!hasAdminPermission()) {
    showNotification('ACCESO DENEGADO', 'Solo administradores pueden ver los logs de auditoría', 'error', 4000)
    return
  }
  
  loading.value = true
  try {
    // Construir URL con parámetros de filtro
    const params = new URLSearchParams({
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      sort: filters.sort
    })
    
    if (filters.actionType !== 'all') {
      params.append('action_type', filters.actionType)
    }
    
    if (filters.userId !== 'all') {
      params.append('user_id', filters.userId)
    }
    
    if (filters.startDate) {
      params.append('start_date', filters.startDate)
    }
    
    if (filters.endDate) {
      params.append('end_date', filters.endDate)
    }
    
    // Cargar logs desde la API
    const logsResponse = await fetch(`/api/audit/logs/?${params.toString()}`)
    if (logsResponse.ok) {
      const data = await logsResponse.json()
      logs.value = data.logs || []
      
      // Actualizar paginación desde la respuesta del servidor
      if (data.pagination) {
        pagination.total = data.pagination.total
        pagination.totalPages = data.pagination.total_pages
        pagination.currentPage = data.pagination.page
      }
    }
    
    // Cargar usuarios para el filtro
    const usersResponse = await fetch('/api/audit/users/')
    if (usersResponse.ok) {
      const usersData = await usersResponse.json()
      availableUsers.value = usersData.users || []
    }
    
    // Actualizar estado de actividad
    updateActivityStatus()
    
  } catch (error) {
    console.error('Error cargando logs:', error)
    showNotification('ERROR', 'Error al cargar registros de auditoría', 'error', 4000)
  } finally {
    loading.value = false
  }
}

const loadAvailableUsers = async () => {
  try {
    const response = await fetch('/api/audit/users/')
    if (response.ok) {
      const data = await response.json()
      availableUsers.value = data.users || []
    }
  } catch (error) {
    console.error('Error cargando usuarios:', error)
  }
}

const updateActivityStatus = () => {
  const lastHour = new Date()
  lastHour.setHours(lastHour.getHours() - 1)
  
  const recentLogs = logs.value.filter(log => 
    new Date(log.created_at) > lastHour
  )
  
  if (recentLogs.length > 100) {
    activityStatus.value = 'ALTA'
  } else if (recentLogs.length > 50) {
    activityStatus.value = 'MEDIA'
  } else {
    activityStatus.value = 'NORMAL'
  }
}

// Búsqueda
const handleSearch = debounce(() => {
  pagination.currentPage = 1
}, 300)

const clearSearch = () => {
  searchQuery.value = ''
  pagination.currentPage = 1
}

// Filtros
const applyFilters = () => {
  pagination.currentPage = 1
  loadLogs() // Cargar logs con nuevos filtros
}

// Paginación
const goToPage = (page) => {
  if (page < 1 || page > pagination.totalPages) return
  pagination.currentPage = page
  loadLogs() // Cargar la página específica desde el servidor
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const updatePageSize = () => {
  pagination.currentPage = 1
  pagination.totalPages = Math.ceil(displayedLogs.value.length / pagination.pageSize)
}

// Acciones
const refreshLogs = () => {
  loadLogs()
  showNotification('INFO', 'Registros de auditoría actualizados', 'info', 2000)
}

const exportLogs = async () => {
  try {
    const response = await fetch('/api/audit/logs/export/')
    if (response.ok) {
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `audit-logs-${new Date().toISOString().split('T')[0]}.csv`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      
      showNotification('ÉXITO', 'Logs exportados exitosamente', 'success', 4000)
    }
  } catch (error) {
    console.error('Error exportando logs:', error)
    showNotification('ERROR', 'Error al exportar logs', 'error', 4000)
  }
}

const getSeverityText = (severity) => {
  switch(severity) {
    case 1: return 'BAJA'
    case 2: return 'MEDIA'
    case 3: return 'ALTA'
    case 4: return 'CRÍTICA'
    default: return 'DESCONOCIDA'
  }
}

const formatJsonDetails = (details) => {
  if (!details || Object.keys(details).length === 0) {
    return '{}'
  }
  
  // Si los detalles son una cadena, intentar formatearlos como JSON
  if (typeof details === 'string') {
    try {
      const parsedDetails = JSON.parse(details)
      return JSON.stringify(parsedDetails, null, 2)
    } catch {
      return details
    }
  }
  
  // Si ya es un objeto, formatearlo
  return JSON.stringify(details, null, 2)
}

const getActionClass = (actionType) => {
  if (actionType.includes('warn') || actionType.includes('ban')) {
    return 'action-moderation'
  } else if (actionType.includes('permission') || actionType.includes('role') || actionType.includes('user_')) {
    return 'action-permission'
  } else if (actionType.includes('character')) {
    return 'action-character'
  } else {
    return 'action-system'
  }
}

const cleanOldLogs = async () => {
  if (!confirm('¿Eliminar registros de auditoría antiguos (más de 30 días)? Esta acción no se puede deshacer.')) {
    return
  }
  
  loading.value = true
  try {
    const response = await fetch('/api/audit/logs/clean/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCSRFToken()
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      showNotification('ÉXITO', `Se eliminaron ${data.deleted_count} registros antiguos`, 'success', 4000)
      loadLogs()
    } else {
      showNotification('ERROR', 'Error al limpiar logs antiguos', 'error', 4000)
    }
  } catch (error) {
    console.error('Error limpiando logs:', error)
    showNotification('ERROR', 'Error al limpiar logs', 'error', 4000)
  } finally {
    loading.value = false
  }
}

const selectLog = (log) => {
  selectedLog.value = log
  jsonView.value = 'parsed' // Resetear a vista legible por defecto
}

const deleteLog = async (log) => {
  if (!hasAdminPermission() || !confirm(`¿Eliminar registro #${log.id}? Esta acción no se puede deshacer.`)) {
    if (!hasAdminPermission()) {
      showNotification('ACCESO DENEGADO', 'Solo administradores pueden eliminar registros', 'error', 4000)
    }
    return
  }
  
  try {
    const response = await fetch(`/api/audit/logs/${log.id}/delete/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': getCSRFToken()
      }
    })
    
    if (response.ok) {
      showNotification('ÉXITO', 'Registro eliminado exitosamente', 'success', 4000)
      loadLogs()
      if (selectedLog.value?.id === log.id) {
        selectedLog.value = null
      }
    } else {
      showNotification('ERROR', 'Error al eliminar registro', 'error', 4000)
    }
  } catch (error) {
    console.error('Error eliminando registro:', error)
    showNotification('ERROR', 'Error al eliminar registro', 'error', 4000)
  }
}

const deleteSelectedLog = () => {
  if (selectedLog.value) {
    deleteLog(selectedLog.value)
  }
}

// Utilidades
const getActionDisplay = (actionType) => {
  const actionMap = {
    'user_login': 'Inicio de sesión',
    'user_logout': 'Cierre de sesión',
    'permissions_update': 'Actualización de permisos',
    'role_assigned': 'Rol asignado',
    'role_removed': 'Rol removido',
    'warn_created': 'Advertencia creada',
    'warn_updated': 'Advertencia actualizada',
    'warn_removed': 'Advertencia eliminada',
    'warn_appealed': 'Advertencia apelada',
    'warn_appeal_responded': 'Respuesta a apelación',
    'ban_created': 'Baneo creado',
    'ban_revoked': 'Baneo revocado',
    'ban_appealed': 'Baneo apelado',
    'ban_appeal_responded': 'Respuesta a apelación de baneo',
    'character_created': 'Personaje creado',
    'character_updated': 'Personaje actualizado',
    'character_deleted': 'Personaje eliminado',
    'ssu_status_changed': 'Estado SSU cambiado',
    'rp_file_edited': 'Archivo RP editado',
    'faction_moderated': 'Facción moderada',
    'actor_supervised': 'Actor supervisado'
  }
  return actionMap[actionType] || actionType
}

const getDetailsPreview = (log) => {
  if (!log.details || Object.keys(log.details).length === 0) {
    return 'Sin detalles adicionales'
  }
  
  const details = log.details
  
  // Intentar extraer información útil
  if (typeof details === 'string') {
    try {
      const parsedDetails = JSON.parse(details)
      if (parsedDetails.reason) return `Razón: ${parsedDetails.reason.substring(0, 50)}...`
      if (parsedDetails.message) return `Mensaje: ${parsedDetails.message.substring(0, 50)}...`
      if (parsedDetails.scope) return `Ámbito: ${parsedDetails.scope}`
      if (parsedDetails.status) return `Estado: ${parsedDetails.status}`
      return 'Ver detalles...'
    } catch {
      return details.substring(0, 60) + (details.length > 60 ? '...' : '')
    }
  } else if (typeof details === 'object') {
    if (details.reason) return `Razón: ${details.reason.substring(0, 50)}...`
    if (details.message) return `Mensaje: ${details.message.substring(0, 50)}...`
    if (details.scope) return `Ámbito: ${details.scope} - Nivel: ${details.level}`
    if (details.status) return `Estado: ${details.status}`
  }
  
  return 'Ver detalles...'
}

const formatKey = (key) => {
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase())
}

const formatValue = (value) => {
  if (typeof value === 'boolean') {
    return value ? '✅ Sí' : '❌ No'
  } else if (value === null || value === undefined) {
    return 'N/A'
  } else if (typeof value === 'object') {
    return JSON.stringify(value, null, 2)
  }
  return value
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    showNotification('ÉXITO', 'Texto copiado al portapapeles', 'success', 2000)
  } catch (err) {
    console.error('Error al copiar:', err)
    // Fallback para navegadores antiguos
    const textArea = document.createElement('textarea')
    textArea.value = text
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    showNotification('ÉXITO', 'Texto copiado al portapapeles', 'success', 2000)
  }
}

const formatDateFull = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('es-ES', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
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
  
  if (diffMins < 1) return 'justo ahora'
  if (diffMins < 60) return `hace ${diffMins} min`
  if (diffHours < 24) return `hace ${diffHours} horas`
  if (diffDays === 1) return 'ayer'
  if (diffDays < 7) return `hace ${diffDays} días`
  return `hace ${Math.floor(diffDays / 7)} semanas`
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
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
  
  if (cookieValue) return cookieValue;
  
  const metaTag = document.querySelector('meta[name="csrf-token"]');
  if (metaTag) return metaTag.content;
  
  const csrfInput = document.querySelector('[name="csrfmiddlewaretoken"]');
  if (csrfInput) return csrfInput.value;
  
  return 'fallback-csrf-token-for-debug';
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

// Watch para cambios en usuario
watch(currentUser, (newUser) => {
  if (newUser?.is_authenticated) {
    loadLogs()
    loadAvailableUsers()
  }
})
</script>

<style scoped>
/* Estilos base similares a Moderacion_Global.vue */
.audit-logs-page {
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

/* Fondo SCP - reutilizado de Moderacion_Global */
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

/* Header específico para Audit Logs */
.audit-logs-header {
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
.audit-logs-nav {
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

.info-value.warning {
  color: #FF9800;
  font-weight: bold;
}

.info-value.operational {
  color: #4CAF50;
}

/* Contenido Principal */
.audit-logs-main {
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

.pagination-info {
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

.action-button.danger {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  color: #f44336;
}

.action-button.danger:hover:not(:disabled) {
  background: rgba(244, 67, 54, 0.2);
  border-color: rgba(244, 67, 54, 0.5);
}

.action-button.full-width {
  width: 100%;
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
  min-height: 32px;
}

.filter-select:hover,
.filter-date:hover {
  border-color: #555;
}

.filter-select:focus,
.filter-date:focus {
  border-color: #ff3333;
}

.filter-select {
  min-width: 180px;
}

.filter-date {
  min-width: 140px;
}

.date-separator {
  color: #666;
  margin: 0 0.5rem;
}

/* Badges de acción */
.action-badge {
  padding: 0.3rem 0.6rem;
  border-radius: 2px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
  display: inline-block;
}

.action-moderation {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

.action-permission {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
  border: 1px solid rgba(33, 150, 243, 0.3);
}

.action-character {
  background: rgba(156, 39, 176, 0.1);
  color: #9C27B0;
  border: 1px solid rgba(156, 39, 176, 0.3);
}

.action-system {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
  border: 1px solid rgba(76, 175, 80, 0.3);
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

/* Paginación de la tabla */
.table-pagination {
  padding: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(25, 25, 25, 0.8);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.pagination-info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.pagination-stats {
  font-size: 0.9rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.pagination-controls-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pagination-nav {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(30, 30, 30, 0.9);
  border: 1px solid #444;
  color: #aaa;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.pagination-nav:hover:not(:disabled) {
  background: rgba(40, 40, 40, 0.95);
  border-color: #666;
  color: #ddd;
}

.pagination-nav:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.pagination-nav svg {
  width: 16px;
  height: 16px;
}

.page-numbers {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-number {
  min-width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(30, 30, 30, 0.9);
  border: 1px solid #444;
  color: #aaa;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-number:hover:not(.active) {
  background: rgba(40, 40, 40, 0.95);
  border-color: #666;
  color: #ddd;
}

.page-number.active {
  background: rgba(255, 51, 51, 0.1);
  border-color: #ff3333;
  color: #ff3333;
}

.page-ellipsis {
  color: #666;
  padding: 0 0.5rem;
  font-size: 0.9rem;
}

.page-size-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: flex-end;
}

.page-size-label {
  font-size: 0.85rem;
  color: #888;
}

.page-size-select {
  background: rgba(40, 40, 40, 0.8);
  border: 1px solid #444;
  color: #fff;
  padding: 0.3rem 0.6rem;
  font-size: 0.85rem;
  font-family: inherit;
  outline: none;
  transition: border-color 0.3s ease;
}

.page-size-select:hover {
  border-color: #555;
}

.page-size-select:focus {
  border-color: #ff3333;
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
  cursor: pointer;
}

.scp-table tbody tr:hover {
  background: rgba(255, 51, 51, 0.05);
}

.scp-table tbody tr.selected {
  background: rgba(255, 51, 51, 0.1);
  border-left: 3px solid #ff3333;
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

.action-cell {
  min-width: 150px;
}

.user-cell .user-info,
.target-cell .target-info {
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

.unknown,
.no-target {
  color: #888;
  font-style: italic;
  font-size: 0.85rem;
}

.details-cell {
  max-width: 300px;
  min-width: 200px;
}

.details-content {
  cursor: pointer;
}

.details-preview {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.details-preview:hover {
  background: rgba(50, 50, 50, 0.8);
  border-color: #555;
}

.details-text {
  flex: 1;
  color: #ccc;
  font-size: 0.85rem;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.details-icon {
  width: 14px;
  height: 14px;
  color: #888;
  flex-shrink: 0;
}

.date-cell {
  min-width: 180px;
}

.date-full {
  display: block;
  font-family: 'Consolas', monospace;
  font-size: 0.85rem;
  color: #ccc;
  margin-bottom: 0.2rem;
}

.date-relative {
  display: block;
  font-size: 0.75rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

/* Acciones de tabla */
.actions-cell {
  display: flex;
  gap: 0.5rem;
  min-width: 80px;
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

.table-action.delete:hover:not(:disabled) {
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

/* Panel de detalles debajo de la tabla */
.details-panel-container {
  margin-top: 2rem;
}

.details-panel {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  display: flex;
  flex-direction: column;
}

.details-panel-header {
  padding: 1.5rem;
  border-bottom: 1px solid #333;
  background: rgba(30, 30, 30, 0.9);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.details-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.details-id {
  background: rgba(255, 51, 51, 0.1);
  color: #ff3333;
  padding: 0.2rem 0.6rem;
  border-radius: 2px;
  font-size: 0.9rem;
  font-family: 'Consolas', monospace;
}

.details-placeholder {
  color: #888;
  font-style: italic;
  font-weight: normal;
  font-size: 1rem;
}

.close-details {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  border-radius: 2px;
}

.close-details:hover {
  background: rgba(255, 51, 51, 0.1);
  color: #ff3333;
}

.close-details svg {
  width: 18px;
  height: 18px;
}

.details-panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

/* Estado sin selección */
.no-selection {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  height: 100%;
  padding: 3rem 1rem;
  color: #666;
}

.no-selection-icon {
  width: 80px;
  height: 80px;
  color: #ff3333;
  opacity: 0.5;
  margin-bottom: 1.5rem;
}

.no-selection-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1rem 0;
}

.no-selection-text {
  font-size: 0.95rem;
  color: #888;
  line-height: 1.5;
  max-width: 300px;
}

/* Contenido de detalles del log */
.log-details-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Grid de detalles */
.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #444;
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

.detail-value.user-agent {
  font-size: 0.8rem;
  font-family: 'Consolas', monospace;
  color: #aaa;
  max-height: 60px;
  overflow-y: auto;
  padding: 0.5rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 2px;
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

.related-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  margin-bottom: 0.8rem;
}

.related-item:last-child {
  margin-bottom: 0;
}

.item-label {
  font-size: 0.8rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.item-value {
  font-size: 0.9rem;
  color: #ddd;
  word-break: break-word;
}

/* Estilos adicionales para el panel de detalles */
.action-code {
  font-size: 0.8rem;
  opacity: 0.7;
  margin-left: 0.5rem;
  font-weight: normal;
}

.warning-section {
  border-left: 3px solid #FF9800;
  padding-left: 1rem;
  background: rgba(255, 152, 0, 0.05);
}

.ban-section {
  border-left: 3px solid #f44336;
  padding-left: 1rem;
  background: rgba(244, 67, 54, 0.05);
}

.character-section {
  border-left: 3px solid #9C27B0;
  padding-left: 1rem;
  background: rgba(156, 39, 176, 0.05);
}

.reason-text {
  color: #ddd;
  background: rgba(255, 255, 255, 0.05);
  padding: 0.5rem;
  border-radius: 2px;
  display: block;
  margin-top: 0.3rem;
}

.codename {
  color: #ffcc00;
  font-weight: bold;
  font-family: 'Consolas', monospace;
}

.faction {
  color: #4CAF50;
  font-weight: 500;
}

/* Procesador de JSON */
.json-processor {
  margin-top: 0.5rem;
}

.json-view-selector {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.json-view-btn {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  color: #aaa;
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  border-radius: 2px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Consolas', monospace;
}

.json-view-btn:hover {
  background: rgba(50, 50, 50, 0.8);
  border-color: #555;
  color: #ddd;
}

.json-view-btn.active {
  background: rgba(255, 51, 51, 0.1);
  border-color: #ff3333;
  color: #ff3333;
}

.json-view-btn.copy-btn {
  background: rgba(33, 150, 243, 0.2);
  border: 1px solid rgba(33, 150, 243, 0.3);
  color: #2196F3;
}

.json-view-btn.copy-btn:hover {
  background: rgba(33, 150, 243, 0.3);
  border-color: rgba(33, 150, 243, 0.5);
}

.json-container {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 2px;
  overflow: hidden;
}

.json-details {
  white-space: pre-wrap;
  word-break: break-word;
  padding: 1rem;
  font-family: 'Consolas', monospace;
  font-size: 0.85rem;
  color: #ccc;
  max-height: 300px;
  overflow-y: auto;
  margin: 0;
  background: rgba(30, 30, 30, 0.8);
}

.parsed-details {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 2px;
  padding: 1rem;
  max-height: 300px;
  overflow-y: auto;
}

.parsed-content {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.parsed-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.parsed-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.parsed-key {
  font-size: 0.85rem;
  color: #888;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.parsed-value {
  font-size: 0.9rem;
  color: #ddd;
  word-break: break-word;
  line-height: 1.4;
}

.no-parsed-details {
  text-align: center;
  padding: 2rem 1rem;
  color: #888;
}

.no-parsed-details p {
  margin-bottom: 1rem;
}

.show-raw-btn {
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  color: #ff3333;
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  border-radius: 2px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Consolas', monospace;
}

.show-raw-btn:hover {
  background: rgba(255, 51, 51, 0.2);
  border-color: rgba(255, 51, 51, 0.5);
}

.details-actions {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #444;
}

.severity-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 2px;
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.severity-1 { background: rgba(76, 175, 80, 0.2); color: #4CAF50; border: 1px solid rgba(76, 175, 80, 0.3); }
.severity-2 { background: rgba(255, 152, 0, 0.2); color: #FF9800; border: 1px solid rgba(255, 152, 0, 0.3); }
.severity-3 { background: rgba(244, 67, 54, 0.2); color: #f44336; border: 1px solid rgba(244, 67, 54, 0.3); }
.severity-4 { background: rgba(156, 39, 176, 0.2); color: #9C27B0; border: 1px solid rgba(156, 39, 176, 0.3); }

.type-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 2px;
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.type-temporary { background: rgba(255, 152, 0, 0.2); color: #FF9800; border: 1px solid rgba(255, 152, 0, 0.3); }
.type-permanent { background: rgba(244, 67, 54, 0.2); color: #f44336; border: 1px solid rgba(244, 67, 54, 0.3); }

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
  .audit-logs-header,
  .audit-logs-nav,
  .audit-logs-main {
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
  
  .filter-select,
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
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .pagination-info-row {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .pagination-controls-row {
    justify-content: center;
  }
  
  .page-size-selector {
    justify-content: center;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .audit-logs-main {
    padding: 1.5rem;
  }
}
</style>