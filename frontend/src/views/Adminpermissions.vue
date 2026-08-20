<template>
  <div class="admin-permissions-page">
    <!-- Fondo SCP -->
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
    </div>

    <!-- Header -->
    <header class="admin-permissions-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-logo">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                <path d="M12 8v4"></path>
                <path d="M12 16h.01"></path>
              </svg>
            </div>
            <div class="header-title">
              <span class="header-main">PANEL DE GESTIÓN DE STAFF</span>
              <span class="header-sub">ADMINISTRACIÓN DE ROLES Y PERMISOS DE MODERACIÓN</span>
            </div>
          </div>
        </div>
        
        <div class="header-right">
          <div class="session-status">
            <div class="session-indicator active"></div>
            <span class="session-text">CONTROL ADMINISTRATIVO ACTIVO</span>
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
              <span>VOLVER A MODERACIÓN</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Navegación -->
    <nav class="admin-permissions-nav">
      <div class="nav-controls">
        <button 
          class="nav-button" 
          :class="{ 'active': activeTab === 'current' }"
          @click="setActiveTab('current')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <span class="nav-text">STAFF ACTUAL</span>
        </button>
        
        <button 
          class="nav-button" 
          :class="{ 'active': activeTab === 'add' }"
          @click="setActiveTab('add')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="8.5" cy="7" r="4"></circle>
              <line x1="20" y1="8" x2="20" y2="14"></line>
              <line x1="23" y1="11" x2="17" y2="11"></line>
            </svg>
          </div>
          <span class="nav-text">AGREGAR STAFF</span>
        </button>
        
        <button 
          class="nav-button" 
          :class="{ 'active': activeTab === 'roles' }"
          @click="setActiveTab('roles')"
        >
          <div class="nav-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="3" y1="9" x2="21" y2="9"></line>
              <line x1="9" y1="21" x2="9" y2="9"></line>
            </svg>
          </div>
          <span class="nav-text">CONFIGURACIÓN</span>
        </button>
      </div>
      
      <div class="nav-info">
        <div class="info-item">
          <span class="info-label">ADMIN:</span>
          <span class="info-value">{{ currentUser?.roblox_username || 'INVITADO' }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">TOTAL STAFF:</span>
          <span class="info-value">{{ staffUsers.length }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">SISTEMA:</span>
          <span class="info-value operational">OPERATIVO</span>
        </div>
      </div>
    </nav>

    <!-- Contenido Principal -->
    <main class="admin-permissions-main">
      <!-- Verificación de permisos -->
      <div v-if="!hasAdminPermissions()" class="access-denied">
        <div class="denied-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M4.93 4.93l14.14 14.14"></path>
          </svg>
        </div>
        <h3>ACCESO ADMINISTRATIVO REQUERIDO</h3>
        <p>Necesitas permiso de control_moderacion_total para acceder a este panel</p>
      </div>

      <div v-else class="admin-content">
        <!-- Pestaña: Staff Actual -->
        <div v-if="activeTab === 'current'" class="current-staff-tab">
          <div class="tab-header">
            <h2 class="tab-title">MIEMBROS DEL STAFF ACTUALES</h2>
            <div class="tab-subtitle">
              Gestionar roles y permisos de los miembros del staff actuales
              <span v-if="staffUsers.length > 0" class="count-info">
                | {{ staffUsers.length }} miembros del staff
              </span>
            </div>
          </div>

          <!-- Barra de búsqueda -->
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
                placeholder="Buscar miembros del staff por nombre de usuario..."
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
                <div class="search-count" v-if="filteredStaff.length > 0">
                  {{ filteredStaff.length }} {{ filteredStaff.length === 1 ? 'miembro encontrado' : 'miembros encontrados' }}
                </div>
              </div>
            </div>
            
            <div class="action-buttons">
              <button 
                class="action-button secondary"
                @click="refreshStaffList"
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

          <!-- Lista de Staff -->
          <div class="staff-list-container">
            <div v-if="loadingStaff" class="loading-state">
              <div class="loading-spinner"></div>
              <p class="loading-text">Cargando miembros del staff...</p>
            </div>
            
            <div v-else-if="filteredStaff.length > 0" class="staff-grid">
              <div 
                v-for="staff in filteredStaff" 
                :key="staff.id"
                class="staff-card"
                :class="{ 'selected': selectedStaff?.id === staff.id }"
                @click="selectStaff(staff)"
              >
                <div class="staff-card-header">
                  <div class="staff-avatar">
                    {{ getInitials(staff.roblox_username) }}
                  </div>
                  <div class="staff-info">
                    <h4 class="staff-name">{{ staff.roblox_username }}</h4>
                    <div class="staff-id">ID: {{ staff.roblox_id }}</div>
                    <div class="staff-meta">
                      <span class="meta-item" v-if="staff.is_superuser">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                          <path d="M22 4 12 14.01l-3-3"></path>
                        </svg>
                        SUPERUSUARIO
                      </span>
                      <span class="meta-item" v-if="staff.warning_count > 0">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"></circle>
                          <line x1="12" y1="8" x2="12" y2="12"></line>
                          <line x1="12" y1="16" x2="12.01" y2="16"></line>
                        </svg>
                        {{ staff.warning_count }} warns
                      </span>
                      <span class="meta-item" v-if="staff.is_banned">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                        </svg>
                        BANEADO
                      </span>
                    </div>
                  </div>
                </div>
                
                <div class="staff-roles">
                  <div class="roles-label">ROLES:</div>
                  <div class="roles-tags">
                    <span 
                      v-for="role in staff.roles" 
                      :key="`${staff.id}-${role.scope}-${role.level}`"
                      class="role-tag"
                      :class="getScopeClass(role.scope)"
                    >
                      {{ role.scope_display }} {{ role.level_display }}
                    </span>
                    <span v-if="staff.roles.length === 0" class="no-roles">
                      Sin roles asignados
                    </span>
                  </div>
                </div>
                
                <div class="staff-permissions">
                  <div class="permissions-count">
                    {{ staff.permissions_count }} permisos
                  </div>
                </div>
                
                <div class="staff-actions">
                  <button class="staff-action edit" @click.stop="editStaff(staff)" title="Editar Roles">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </button>
                  <button 
                    v-if="!staff.is_superuser"
                    class="staff-action remove" 
                    @click.stop="removeStaff(staff)"
                    title="Remover del Staff"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            
            <div v-else class="empty-state">
              <div class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
              </div>
              <h3 class="empty-title">No se encontraron miembros del staff</h3>
              <p class="empty-text" v-if="searchQuery">
                No hay miembros del staff que coincidan con tu búsqueda
              </p>
              <p class="empty-text" v-else>
                No se han asignado roles a ningún usuario aún
              </p>
              <button class="empty-action" @click="setActiveTab('add')">
                AGREGAR NUEVO MIEMBRO DEL STAFF
              </button>
            </div>
          </div>

          <!-- Panel de edición de staff -->
          <div v-if="selectedStaff && editingStaff" class="staff-edit-panel" ref="editPanelRef">
            <div class="edit-panel-header">
              <h3 class="edit-title">
                Editar Staff: {{ selectedStaff.roblox_username }}
                <span class="edit-subtitle">ID: {{ selectedStaff.roblox_id }}</span>
              </h3>
              <button class="edit-close" @click="cancelEdit">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
            
            <div class="edit-panel-content">
              <!-- Roles asignados -->
              <div class="edit-section">
                <h4 class="section-title">ROLES ASIGNADOS</h4>
                <div class="assigned-roles">
                  <div 
                    v-for="(role, index) in staffRoles"
                    :key="index"
                    class="assigned-role"
                    :class="getScopeClass(role.scope)"
                  >
                    <div class="role-info">
                      <span class="role-name">{{ getScopeDisplay(role.scope) }}</span>
                      <span class="role-level">{{ getLevelDisplay(role.scope, role.level) }}</span>
                    </div>
                    <div class="role-permissions">
                      <span class="perms-count">
                        {{ getScopePermissionsCount(role.scope, role.level) }} permisos
                      </span>
                    </div>
                    <button class="role-remove" @click="removeRole(index)" title="Eliminar Rol">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                    </button>
                  </div>
                  
                  <div v-if="staffRoles.length === 0" class="no-roles-message">
                    Sin roles asignados. El usuario perderá estado de staff.
                  </div>
                </div>
              </div>
              
              <!-- Agregar nuevo rol -->
              <div class="edit-section">
                <h4 class="section-title">AGREGAR NUEVO ROL</h4>
                <div class="add-role-form">
                  <div class="form-row">
                    <div class="form-group">
                      <label class="form-label">Ámbito</label>
                      <select v-model="newRole.scope" class="form-select">
                        <option value="">Seleccionar ámbito...</option>
                        <option 
                          v-for="scope in availableScopes" 
                          :key="scope.value"
                          :value="scope.value"
                          :disabled="hasRoleScope(scope.value)"
                        >
                          {{ scope.display }}
                        </option>
                      </select>
                    </div>
                    
                    <div class="form-group">
                      <label class="form-label">Nivel</label>
                      <select v-model="newRole.level" class="form-select" :disabled="!newRole.scope">
                        <option value="">Seleccionar nivel...</option>
                        <option 
                          v-for="level in getAvailableLevels(newRole.scope)" 
                          :key="level"
                          :value="level"
                        >
                          {{ getLevelDisplay(newRole.scope, level) }}
                        </option>
                      </select>
                    </div>
                    
                    <div class="form-group">
                      <label class="form-label">Vista Previa de Permisos</label>
                      <div class="permissions-preview">
                        <div v-if="newRole.scope && newRole.level" class="preview-list">
                          <span 
                            v-for="permission in getScopePermissions(newRole.scope, newRole.level)" 
                            :key="permission"
                            class="preview-permission"
                          >
                            {{ permission }}
                          </span>
                        </div>
                        <div v-else class="preview-empty">
                          Selecciona ámbito y nivel para ver los permisos
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <button 
                    class="add-role-button"
                    @click="addRole"
                    :disabled="!newRole.scope || !newRole.level"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="12" y1="5" x2="12" y2="19"></line>
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                    <span>AGREGAR ROL</span>
                  </button>
                </div>
              </div>
              
              <!-- Permisos individuales (extra) -->
              <div class="edit-section">
                <h4 class="section-title">PERMISOS INDIVIDUALES</h4>
                <div class="individual-permissions">
                  <p class="permissions-note">
                    Los permisos individuales pueden sobrescribir los permisos de los roles. Usar con precaución.
                  </p>
                  <div class="permissions-grid">
                    <div 
                      v-for="permission in allPermissions" 
                      :key="permission"
                      class="permission-checkbox"
                    >
                      <input 
                        type="checkbox" 
                        :id="`perm-${permission}`"
                        :value="permission"
                        v-model="individualPermissions"
                      />
                      <label :for="`perm-${permission}`">
                        {{ permission }}
                      </label>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Acciones -->
              <div class="edit-actions">
                <button class="edit-action cancel" @click="cancelEdit">
                  CANCELAR
                </button>
                <button class="edit-action save" @click="saveStaffRoles" :disabled="!rolesChanged">
                  GUARDAR CAMBIOS
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pestaña: Agregar Staff -->
        <div v-else-if="activeTab === 'add'" class="add-staff-tab">
          <div class="tab-header">
            <h2 class="tab-title">AGREGAR NUEVO MIEMBRO DEL STAFF</h2>
            <div class="tab-subtitle">Asignar roles a un nuevo miembro del staff por ID de Roblox</div>
          </div>

          <div class="add-staff-container">
            <!-- Búsqueda de usuario -->
            <div class="user-search-section">
              <h3 class="section-title">BUSCAR USUARIO</h3>
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
                    placeholder="Ingresa ID de Roblox o nombre de usuario..."
                    class="user-search-input"
                  />
                  <button class="search-button" @click="searchUser">
                    <span>BUSCAR</span>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Resultados de búsqueda -->
            <div v-if="loadingUserSearch" class="loading-state">
              <div class="loading-spinner"></div>
              <p class="loading-text">Buscando usuario...</p>
            </div>

            <div v-else-if="searchResults.length > 0" class="search-results-section">
              <h3 class="section-title">SELECCIONAR USUARIO</h3>
              <div class="search-results">
                <div 
                  v-for="user in searchResults" 
                  :key="user.id"
                  class="user-result"
                  :class="{ 'selected': selectedUser?.id === user.id }"
                  @click="selectUserForStaff(user)"
                >
                  <div class="user-avatar">
                    {{ getInitials(user.roblox_username) }}
                  </div>
                  <div class="user-info">
                    <span class="username">{{ user.roblox_username }}</span>
                    <span class="user-id">ID: {{ user.roblox_id }}</span>
                  </div>
                  <div class="user-stats">
                    <span class="stat warns" v-if="user.warning_count > 0">
                      {{ user.warning_count }} warns
                    </span>
                    <span class="stat banned" v-if="user.is_banned">
                      BANEADO
                    </span>
                    <span class="stat staff" v-if="user.is_staff">
                      STAFF
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Configuración de roles -->
            <div v-if="selectedUser" class="roles-config-section">
              <h3 class="section-title">CONFIGURAR ROLES PARA {{ selectedUser.roblox_username }}</h3>
              
              <div class="current-roles">
                <h4 class="subsection-title">ROLES ASIGNADOS</h4>
                <div class="roles-list">
                  <div 
                    v-for="(role, index) in newStaffRoles"
                    :key="index"
                    class="role-item"
                    :class="getScopeClass(role.scope)"
                  >
                    <div class="role-content">
                      <span class="role-name">{{ getScopeDisplay(role.scope) }}</span>
                      <span class="role-level">{{ getLevelDisplay(role.scope, role.level) }}</span>
                    </div>
                    <button class="role-remove" @click="removeNewRole(index)">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                    </button>
                  </div>
                  
                  <div v-if="newStaffRoles.length === 0" class="no-roles-message">
                    Sin roles asignados aún
                  </div>
                </div>
              </div>
              
              <div class="add-role-section">
                <h4 class="subsection-title">AGREGAR ROL</h4>
                <div class="add-role-form">
                  <div class="form-row">
                    <select v-model="newStaffRole.scope" class="form-select">
                      <option value="">Seleccionar ámbito...</option>
                      <option 
                        v-for="scope in availableScopes" 
                        :key="scope.value"
                        :value="scope.value"
                      >
                        {{ scope.display }}
                      </option>
                    </select>
                    
                    <select v-model="newStaffRole.level" class="form-select" :disabled="!newStaffRole.scope">
                      <option value="">Seleccionar nivel...</option>
                      <option 
                        v-for="level in getAvailableLevels(newStaffRole.scope)" 
                        :key="level"
                        :value="level"
                      >
                        {{ getLevelDisplay(newStaffRole.scope, level) }}
                      </option>
                    </select>
                    
                    <button 
                      class="add-button"
                      @click="addNewStaffRole"
                      :disabled="!newStaffRole.scope || !newStaffRole.level"
                    >
                      AGREGAR
                    </button>
                  </div>
                </div>
              </div>
              
              <div class="permissions-summary">
                <h4 class="subsection-title">RESUMEN DE PERMISOS</h4>
                <div class="permissions-list">
                  <div 
                    v-for="permission in getAllNewStaffPermissions()" 
                    :key="permission"
                    class="permission-summary-item"
                  >
                    {{ permission }}
                  </div>
                  <div v-if="getAllNewStaffPermissions().length === 0" class="no-permissions">
                    Sin permisos de los roles asignados
                  </div>
                </div>
              </div>
              
              <div class="add-staff-actions">
                <button class="action-button cancel" @click="cancelAddStaff">
                  CANCELAR
                </button>
                <button 
                  class="action-button save" 
                  @click="saveNewStaff"
                  :disabled="newStaffRoles.length === 0"
                >
                  AGREGAR MIEMBRO DEL STAFF
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pestaña: Configuración de Roles -->
        <div v-else-if="activeTab === 'roles'" class="roles-config-tab">
          <div class="tab-header">
            <h2 class="tab-title">CONFIGURACIÓN DE ROLES</h2>
            <div class="tab-subtitle">Ver y gestionar la estructura de permisos de los roles</div>
          </div>

          <div class="roles-structure">
            <div v-for="(scopeData, scope) in permissionsStructure" :key="scope" class="scope-section">
              <h3 class="scope-title">
                {{ getScopeDisplay(scope) }}
                <span class="scope-key">{{ scope }}</span>
              </h3>
              
              <div class="levels-container">
                <div 
                  v-for="(levelData, levelKey) in scopeData" 
                  :key="levelKey"
                  class="level-card"
                >
                  <div class="level-header">
                    <span class="level-name">{{ levelData.level_display }}</span>
                    <span class="permissions-count">
                      {{ levelData.permissions.length }} permisos
                    </span>
                  </div>
                  
                  <div class="permissions-list">
                    <div 
                      v-for="permission in levelData.permissions" 
                      :key="permission"
                      class="permission-item"
                    >
                      {{ permission }}
                    </div>
                  </div>
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

const router = useRouter()

// Estado principal
const activeTab = ref('current')
const currentUser = ref(null)
const currentTime = ref('')
const loadingStaff = ref(false)
const loadingUserSearch = ref(false)

// Staff actual
const staffUsers = ref([])
const searchQuery = ref('')
const selectedStaff = ref(null)
const editingStaff = ref(false)
const staffRoles = ref([])
const originalRoles = ref([])
const individualPermissions = ref([])
const editPanelRef = ref(null)

// Agregar staff
const userSearchQuery = ref('')
const searchResults = ref([])
const selectedUser = ref(null)
const newStaffRoles = ref([])
const newStaffRole = reactive({
  scope: '',
  level: ''
})

// Configuración de roles
const permissionsStructure = ref({})
const availableScopes = ref([])
const allPermissions = ref([])

// Nuevo rol para edición
const newRole = reactive({
  scope: '',
  level: ''
})

// Notificaciones
const notifications = ref([])
let notificationId = 0

// Computed
const filteredStaff = computed(() => {
  if (!searchQuery.value) return staffUsers.value
  
  const query = searchQuery.value.toLowerCase()
  return staffUsers.value.filter(staff => 
    staff.roblox_username.toLowerCase().includes(query) ||
    staff.roblox_id.toString().includes(query)
  )
})

const rolesChanged = computed(() => {
  return JSON.stringify(staffRoles.value) !== JSON.stringify(originalRoles.value)
})

const hasRoleScope = (scope) => {
  return staffRoles.value.some(role => role.scope === scope)
}

// Métodos
const hasAdminPermissions = () => {
  // En producción, verificar del backend
  return true // Temporalmente true para desarrollo
}

const getInitials = (username) => {
  if (!username) return '?'
  return username.substring(0, 2).toUpperCase()
}

const getScopeClass = (scope) => {
  const scopeClasses = {
    'global': 'scope-global',
    'moderation': 'scope-moderation',
    'ingame': 'scope-ingame',
    'discord': 'scope-discord',
    'rp_roleplay': 'scope-roleplay',
    'rp_faction': 'scope-faction',
    'rp_actors': 'scope-actors'
  }
  return scopeClasses[scope] || ''
}

const getScopeDisplay = (scope) => {
  const scopeDisplays = {
    'global': 'Administración Global',
    'moderation': 'Moderación General',
    'ingame': 'Moderación In-Game',
    'discord': 'Moderación Discord',
    'rp_roleplay': 'Equipo Roleplay',
    'rp_faction': 'Moderación Facciones',
    'rp_actors': 'Supervisión Actores'
  }
  return scopeDisplays[scope] || scope
}

const getLevelDisplay = (scope, level) => {
  const levelNames = {
    'global': {
      1: 'SSU Host',
      2: 'Admin+'
    },
    'moderation': {
      1: 'Junior',
      2: 'Official',
      3: 'Qualified',
      4: 'Senior'
    },
    'ingame': {
      1: 'Junior',
      2: 'Official',
      3: 'Qualified+'
    },
    'discord': {
      1: 'Junior',
      2: 'Official',
      3: 'Qualified',
      4: 'Senior'
    },
    'rp_roleplay': {
      1: 'Equipo RP',
      2: 'Líder RP'
    },
    'rp_faction': {
      1: 'Equipo RP',
      2: 'Líder RP'
    },
    'rp_actors': {
      1: 'Equipo RP',
      2: 'Líder RP'
    }
  }
  
  const scopeLevels = levelNames[scope] || {}
  return scopeLevels[level] || `Nivel ${level}`
}

const getScopePermissionsCount = (scope, level) => {
  if (!permissionsStructure.value[scope]) return 0
  let count = 0
  for (let lvl = 1; lvl <= level; lvl++) {
    const levelKey = `level_${lvl}`
    if (permissionsStructure.value[scope][levelKey]) {
      count += permissionsStructure.value[scope][levelKey].permissions.length
    }
  }
  return count
}

const getScopePermissions = (scope, level) => {
  const permissions = []
  if (!permissionsStructure.value[scope]) return permissions
  
  for (let lvl = 1; lvl <= level; lvl++) {
    const levelKey = `level_${lvl}`
    if (permissionsStructure.value[scope][levelKey]) {
      permissions.push(...permissionsStructure.value[scope][levelKey].permissions)
    }
  }
  return [...new Set(permissions)]
}

const getAvailableLevels = (scope) => {
  if (!scope || !permissionsStructure.value[scope]) return []
  const levels = Object.keys(permissionsStructure.value[scope])
    .map(key => parseInt(key.replace('level_', '')))
    .sort((a, b) => a - b)
  return levels
}

// Carga de datos
const loadStaffUsers = async () => {
  if (!hasAdminPermissions()) return
  
  loadingStaff.value = true
  try {
    const response = await fetch('/api/staff/users/')
    
    if (response.ok) {
      const data = await response.json()
      staffUsers.value = data.staff_users || []
    }
  } catch (error) {
    console.error('Error cargando miembros del staff:', error)
    showNotification('ERROR', 'Error al cargar miembros del staff', 'error', 4000)
  } finally {
    loadingStaff.value = false
  }
}

const loadPermissionsStructure = async () => {
  try {
    const response = await fetch('/api/staff/permissions/structure/')
    
    if (response.ok) {
      const data = await response.json()
      permissionsStructure.value = data.permissions_structure || {}
      availableScopes.value = Object.entries(data.scope_choices || {}).map(([value, display]) => ({
        value,
        display
      }))
      allPermissions.value = data.all_permissions || []
    }
  } catch (error) {
    console.error('Error cargando estructura de permisos:', error)
  }
}

// Staff management
const selectStaff = (staff) => {
  selectedStaff.value = staff
  editingStaff.value = true
  
  // Load staff roles
  loadStaffRoles(staff.id)
  
  // Scroll to edit panel after a short delay (para asegurar que el DOM esté actualizado)
  nextTick(() => {
    scrollToEditPanel()
  })
}

const scrollToEditPanel = () => {
  if (editPanelRef.value) {
    editPanelRef.value.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    })
  }
}

const loadStaffRoles = async (userId) => {
  try {
    const response = await fetch(`/api/auth/user/${userId}/permissions/view/`)
    
    if (response.ok) {
      const data = await response.json()
      staffRoles.value = data.roles || []
      originalRoles.value = JSON.parse(JSON.stringify(data.roles))
      individualPermissions.value = []
    }
  } catch (error) {
    console.error('Error cargando roles del staff:', error)
  }
}

const editStaff = (staff) => {
  selectedStaff.value = staff
  editingStaff.value = true
  loadStaffRoles(staff.id)
  
  // Scroll to edit panel
  nextTick(() => {
    scrollToEditPanel()
  })
}

const cancelEdit = () => {
  editingStaff.value = false
  selectedStaff.value = null
  staffRoles.value = []
  originalRoles.value = []
  individualPermissions.value = []
  newRole.scope = ''
  newRole.level = ''
}

const addRole = () => {
  if (!newRole.scope || !newRole.level) return
  
  // Verificar si ya existe un role con este scope
  const existingIndex = staffRoles.value.findIndex(r => r.scope === newRole.scope)
  
  if (existingIndex !== -1) {
    // Actualizar el nivel del role existente
    staffRoles.value[existingIndex].level = newRole.level
  } else {
    // Agregar nuevo role
    staffRoles.value.push({
      scope: newRole.scope,
      level: newRole.level
    })
  }
  
  newRole.scope = ''
  newRole.level = ''
}

const removeRole = (index) => {
  staffRoles.value.splice(index, 1)
}

const saveStaffRoles = async () => {
  if (!selectedStaff.value) return
  
  try {
    const csrfToken = getCSRFToken()
    const response = await fetch(`/api/auth/user/${selectedStaff.value.id}/permissions/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        roles: staffRoles.value,
        individual_permissions: individualPermissions.value
      })
    })
    
    if (response.ok) {
      showNotification('ÉXITO', 'Roles del staff actualizados exitosamente', 'success', 4000)
      originalRoles.value = JSON.parse(JSON.stringify(staffRoles.value))
      loadStaffUsers() // Refresh the list
    } else {
      const error = await response.json()
      showNotification('ERROR', error.error || 'Error al actualizar roles', 'error', 5000)
    }
  } catch (error) {
    console.error('Error guardando roles del staff:', error)
    showNotification('ERROR', 'Error al actualizar roles', 'error', 5000)
  }
}

const removeStaff = async (staff) => {
  if (!confirm(`¿Remover a ${staff.roblox_username} del staff?`)) return
  
  try {
    const csrfToken = getCSRFToken()
    const response = await fetch(`/api/auth/user/${staff.id}/permissions/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        roles: [],
        individual_permissions: []
      })
    })
    
    if (response.ok) {
      showNotification('ÉXITO', 'Miembro removido del staff', 'success', 4000)
      loadStaffUsers()
    } else {
      showNotification('ERROR', 'Error al remover miembro del staff', 'error', 5000)
    }
  } catch (error) {
    console.error('Error removiendo del staff:', error)
    showNotification('ERROR', 'Error al remover miembro del staff', 'error', 5000)
  }
}

// Add staff
const searchUser = async () => {
  if (!userSearchQuery.value.trim()) {
    showNotification('INFO', 'Por favor ingresa un ID de Roblox o nombre de usuario', 'info', 3000)
    return
  }
  
  loadingUserSearch.value = true
  searchResults.value = []
  
  try {
    const response = await fetch(`/api/moderation/users/search/${encodeURIComponent(userSearchQuery.value)}/`)
    if (response.ok) {
      const data = await response.json()
      searchResults.value = data.results || []
      
      if (searchResults.value.length === 0) {
        showNotification('INFO', 'No se encontraron usuarios', 'info', 3000)
      }
    }
  } catch (error) {
    console.error('Error buscando usuarios:', error)
    showNotification('ERROR', 'Error buscando usuarios', 'error', 5000)
  } finally {
    loadingUserSearch.value = false
  }
}

const selectUserForStaff = (user) => {
  selectedUser.value = user
  newStaffRoles.value = []
  newStaffRole.scope = ''
  newStaffRole.level = ''
}

const addNewStaffRole = () => {
  if (!newStaffRole.scope || !newStaffRole.level) return
  
  // Verificar si ya existe un role con este scope
  const existingIndex = newStaffRoles.value.findIndex(r => r.scope === newStaffRole.scope)
  
  if (existingIndex !== -1) {
    // Actualizar el nivel del role existente
    newStaffRoles.value[existingIndex].level = newStaffRole.level
  } else {
    // Agregar nuevo role
    newStaffRoles.value.push({
      scope: newStaffRole.scope,
      level: newStaffRole.level
    })
  }
  
  newStaffRole.scope = ''
  newStaffRole.level = ''
}

const removeNewRole = (index) => {
  newStaffRoles.value.splice(index, 1)
}

const getAllNewStaffPermissions = () => {
  const allPerms = new Set()
  
  newStaffRoles.value.forEach(role => {
    const perms = getScopePermissions(role.scope, role.level)
    perms.forEach(perm => allPerms.add(perm))
  })
  
  return Array.from(allPerms)
}

const saveNewStaff = async () => {
  if (!selectedUser.value || newStaffRoles.value.length === 0) return
  
  try {
    const csrfToken = getCSRFToken()
    const response = await fetch(`/api/auth/user/${selectedUser.value.id}/permissions/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        roles: newStaffRoles.value,
        individual_permissions: []
      })
    })
    
    if (response.ok) {
      showNotification('ÉXITO', 'Miembro del staff agregado exitosamente', 'success', 4000)
      cancelAddStaff()
      setActiveTab('current')
      loadStaffUsers()
    } else {
      const error = await response.json()
      showNotification('ERROR', error.error || 'Error al agregar miembro del staff', 'error', 5000)
    }
  } catch (error) {
    console.error('Error agregando al staff:', error)
    showNotification('ERROR', 'Error al agregar miembro del staff', 'error', 5000)
  }
}

const cancelAddStaff = () => {
  selectedUser.value = null
  searchResults.value = []
  newStaffRoles.value = []
  newStaffRole.scope = ''
  newStaffRole.level = ''
  userSearchQuery.value = ''
}

// Utilidades
const setActiveTab = (tab) => {
  activeTab.value = tab
  
  switch(tab) {
    case 'current':
      loadStaffUsers()
      break
    case 'roles':
      loadPermissionsStructure()
      break
  }
}

const handleSearch = debounce(() => {
  // Búsqueda en tiempo real
}, 300)

const clearSearch = () => {
  searchQuery.value = ''
}

const refreshStaffList = () => {
  loadStaffUsers()
  showNotification('INFO', 'Lista de staff actualizada', 'info', 2000)
}

const goToModerationPanel = () => {
  router.push('/moderation')
}

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

const fetchCurrentUser = async () => {
  try {
    const response = await fetch('/api/auth/user/')
    if (response.ok) {
      const data = await response.json()
      currentUser.value = data
    }
  } catch (error) {
    console.error('Error obteniendo usuario actual:', error)
  }
}

const getCSRFToken = () => {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1]
  
  if (cookieValue) return cookieValue
  
  const metaTag = document.querySelector('meta[name="csrf-token"]')
  if (metaTag) return metaTag.content
  
  const csrfInput = document.querySelector('[name="csrfmiddlewaretoken"]')
  if (csrfInput) return csrfInput.value
  
  console.warn('CSRF token no encontrado')
  return 'fallback-csrf-token'
}

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

// Lifecycle
onMounted(() => {
  updateTime()
  const timeInterval = setInterval(updateTime, 1000)
  
  fetchCurrentUser()
  loadStaffUsers()
  loadPermissionsStructure()
  
  return () => {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
/* Estilos base - similar a Moderacion_Global.vue */
.admin-permissions-page {
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
.admin-permissions-header {
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
.admin-permissions-nav {
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

.info-value.operational {
  color: #4CAF50;
}

/* Contenido Principal */
.admin-permissions-main {
  position: relative;
  z-index: 2;
  flex: 1;
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

.access-denied {
  text-align: center;
  padding: 4rem 2rem;
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  margin: 2rem 0;
}

.denied-icon {
  width: 80px;
  height: 80px;
  color: #ff3333;
  margin: 0 auto 2rem;
}

.access-denied h3 {
  font-size: 1.5rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 1rem;
}

.access-denied p {
  color: #aaa;
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

.count-info {
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

/* Lista de Staff */
.staff-list-container {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  min-height: 400px;
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

.empty-action {
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

.empty-action:hover {
  background: rgba(255, 51, 51, 0.2);
  border-color: rgba(255, 51, 51, 0.5);
}

.staff-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
}

.staff-card {
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  padding: 1.5rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.staff-card:hover {
  border-color: #555;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.staff-card.selected {
  border-color: #ff3333;
  background: rgba(255, 51, 51, 0.05);
}

.staff-card-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.staff-avatar {
  width: 60px;
  height: 60px;
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #ff3333;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.staff-info {
  flex: 1;
}

.staff-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 0.3rem 0;
}

.staff-id {
  font-size: 0.8rem;
  color: #888;
  font-family: 'Consolas', monospace;
  margin-bottom: 0.5rem;
}

.staff-meta {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  color: #aaa;
  border-radius: 2px;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.meta-item svg {
  width: 10px;
  height: 10px;
}

.staff-roles {
  margin-bottom: 1rem;
}

.roles-label {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin-bottom: 0.5rem;
  font-family: 'Consolas', monospace;
}

.roles-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.role-tag {
  padding: 0.3rem 0.6rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  border-radius: 2px;
  font-family: 'Consolas', monospace;
}

/* Colores para diferentes scopes */
.scope-global {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.scope-moderation {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
  border: 1px solid rgba(33, 150, 243, 0.3);
}

.scope-ingame {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

.scope-discord {
  background: rgba(156, 39, 176, 0.1);
  color: #9C27B0;
  border: 1px solid rgba(156, 39, 176, 0.3);
}

.scope-roleplay {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.scope-faction {
  background: rgba(255, 87, 34, 0.1);
  color: #FF5722;
  border: 1px solid rgba(255, 87, 34, 0.3);
}

.scope-actors {
  background: rgba(0, 188, 212, 0.1);
  color: #00BCD4;
  border: 1px solid rgba(0, 188, 212, 0.3);
}

.no-roles {
  color: #666;
  font-style: italic;
  font-size: 0.8rem;
}

.staff-permissions {
  margin-bottom: 1rem;
}

.permissions-count {
  font-size: 0.8rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.staff-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.staff-action {
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

.staff-action:hover {
  background: rgba(50, 50, 50, 0.8);
  border-color: #555;
}

.staff-action.edit:hover {
  color: #2196F3;
}

.staff-action.remove:hover {
  color: #f44336;
}

.staff-action svg {
  width: 16px;
  height: 16px;
}

/* Panel de edición */
.staff-edit-panel {
  background: rgba(25, 25, 25, 0.95);
  border: 1px solid #333;
  margin-top: 2rem;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.edit-panel-header {
  padding: 1.5rem;
  background: rgba(30, 30, 30, 0.9);
  border-bottom: 1px solid #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.edit-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #fff;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.edit-subtitle {
  font-size: 0.9rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.edit-close {
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

.edit-close:hover {
  color: #fff;
}

.edit-close svg {
  width: 20px;
  height: 20px;
}

.edit-panel-content {
  padding: 1.5rem;
}

.edit-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.edit-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.section-title {
  font-size: 1rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 1rem 0;
  font-family: 'Consolas', monospace;
}

.assigned-roles {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.assigned-role {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 2px;
}

.role-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.role-name {
  font-weight: 600;
  color: #fff;
}

.role-level {
  font-size: 0.8rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.role-permissions {
  font-size: 0.8rem;
  color: #aaa;
}

.role-remove {
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

.role-remove:hover {
  color: #f44336;
}

.role-remove svg {
  width: 16px;
  height: 16px;
}

.no-roles-message {
  padding: 2rem;
  text-align: center;
  color: #666;
  font-style: italic;
  background: rgba(40, 40, 40, 0.3);
  border: 1px dashed #444;
  border-radius: 2px;
}

/* Formulario de agregar rol */
.add-role-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.form-label {
  display: block;
  font-size: 0.8rem;
  color: #ccc;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin-bottom: 0.5rem;
  font-family: 'Consolas', monospace;
}

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

.form-select:focus {
  outline: none;
  border-color: #ff3333;
  box-shadow: 0 0 0 2px rgba(255, 51, 51, 0.1);
}

.permissions-preview {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  padding: 1rem;
  min-height: 60px;
  max-height: 150px;
  overflow-y: auto;
}

.preview-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.preview-permission {
  font-size: 0.75rem;
  padding: 0.2rem 0.5rem;
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 2px;
  font-family: 'Consolas', monospace;
}

.preview-empty {
  color: #666;
  font-style: italic;
  text-align: center;
  padding: 1rem;
}

.add-role-button {
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
  align-self: flex-start;
}

.add-role-button:hover:not(:disabled) {
  background: rgba(255, 51, 51, 0.2);
  border-color: rgba(255, 51, 51, 0.5);
}

.add-role-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.add-role-button svg {
  width: 16px;
  height: 16px;
}

/* Permisos individuales */
.individual-permissions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.permissions-note {
  font-size: 0.9rem;
  color: #888;
  margin: 0 0 1rem 0;
}

.permissions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 0.8rem;
  max-height: 300px;
  overflow-y: auto;
  padding: 1rem;
  background: rgba(40, 40, 40, 0.3);
  border: 1px solid #444;
  border-radius: 2px;
}

.permission-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.permission-checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #ff3333;
}

.permission-checkbox label {
  font-size: 0.85rem;
  color: #ccc;
  cursor: pointer;
  user-select: none;
}

/* Acciones de edición */
.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #444;
}

.edit-action {
  padding: 0.8rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-family: 'Consolas', monospace;
  min-width: 150px;
}

.edit-action.cancel {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  color: #aaa;
}

.edit-action.cancel:hover {
  background: rgba(50, 50, 50, 0.7);
  border-color: #555;
  color: #fff;
}

.edit-action.save {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  color: #4CAF50;
}

.edit-action.save:hover:not(:disabled) {
  background: rgba(76, 175, 80, 0.2);
  border-color: rgba(76, 175, 80, 0.5);
}

.edit-action.save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Pestaña de agregar staff */
.add-staff-container {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  padding: 2rem;
}

.user-search-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.2rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1rem 0;
  font-family: 'Consolas', monospace;
}

.search-panel {
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  padding: 1.5rem;
}

.search-input-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.user-search-input {
  flex: 1;
  background: rgba(40, 40, 40, 0.8);
  border: 1px solid #444;
  padding: 0.8rem 1rem;
  color: #fff;
  font-size: 1rem;
  font-family: inherit;
  outline: none;
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

/* Resultados de búsqueda */
.search-results-section {
  margin-bottom: 2rem;
}

.search-results {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.user-result {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-result:hover {
  border-color: #555;
  background: rgba(40, 40, 40, 0.8);
}

.user-result.selected {
  border-color: #ff3333;
  background: rgba(255, 51, 51, 0.1);
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #ff3333;
  font-size: 0.9rem;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.username {
  font-weight: 600;
  color: #fff;
}

.user-id {
  font-size: 0.8rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.user-stats {
  display: flex;
  gap: 0.5rem;
}

.stat {
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 2px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.stat.warns {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

.stat.banned {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.stat.staff {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
  border: 1px solid rgba(33, 150, 243, 0.3);
}

/* Configuración de roles para nuevo staff */
.roles-config-section {
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  padding: 1.5rem;
  margin-top: 2rem;
}

.subsection-title {
  font-size: 1rem;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 1rem 0;
  font-family: 'Consolas', monospace;
}

.current-roles {
  margin-bottom: 1.5rem;
}

.roles-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.role-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.8rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 2px;
}

.role-content {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.role-name {
  font-weight: 600;
  color: #fff;
}

.role-level {
  font-size: 0.8rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.add-role-section {
  margin-bottom: 1.5rem;
}

.add-role-form .form-row {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
}

.add-button {
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
  min-width: 100px;
}

.add-button:hover:not(:disabled) {
  background: rgba(255, 51, 51, 0.2);
  border-color: rgba(255, 51, 51, 0.5);
}

.add-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.permissions-summary {
  margin-bottom: 1.5rem;
}

.permissions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  max-height: 200px;
  overflow-y: auto;
  padding: 1rem;
  background: rgba(40, 40, 40, 0.3);
  border: 1px solid #444;
  border-radius: 2px;
}

.permission-summary-item {
  font-size: 0.75rem;
  padding: 0.2rem 0.5rem;
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 2px;
  font-family: 'Consolas', monospace;
}

.no-permissions {
  color: #666;
  font-style: italic;
  font-size: 0.9rem;
}

.add-staff-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid #444;
}

.add-staff-actions .action-button {
  padding: 0.8rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-family: 'Consolas', monospace;
  min-width: 180px;
}

.add-staff-actions .action-button.cancel {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  color: #aaa;
}

.add-staff-actions .action-button.cancel:hover {
  background: rgba(50, 50, 50, 0.7);
  border-color: #555;
  color: #fff;
}

.add-staff-actions .action-button.save {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  color: #4CAF50;
}

.add-staff-actions .action-button.save:hover:not(:disabled) {
  background: rgba(76, 175, 80, 0.2);
  border-color: rgba(76, 175, 80, 0.5);
}

.add-staff-actions .action-button.save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Pestaña de configuración de roles */
.roles-structure {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  padding: 2rem;
}

.scope-section {
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.scope-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.scope-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ff3333;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.scope-key {
  font-size: 0.9rem;
  color: #888;
  font-family: 'Consolas', monospace;
  background: rgba(40, 40, 40, 0.6);
  padding: 0.2rem 0.5rem;
  border-radius: 2px;
}

.levels-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.level-card {
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  padding: 1.5rem;
}

.level-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.level-name {
  font-weight: 600;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.permissions-count {
  font-size: 0.8rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.permissions-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.permission-item {
  font-size: 0.85rem;
  padding: 0.5rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  color: #ccc;
  font-family: 'Consolas', monospace;
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
  .admin-permissions-header,
  .admin-permissions-nav,
  .admin-permissions-main {
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
  
  .staff-grid {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    flex-direction: column;
  }
  
  .form-group {
    min-width: 100%;
  }
  
  .permissions-grid {
    grid-template-columns: 1fr;
  }
  
  .levels-container {
    grid-template-columns: 1fr;
  }
  
  .add-staff-actions {
    flex-direction: column;
  }
  
  .add-staff-actions .action-button {
    min-width: 100%;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .admin-permissions-main {
    padding: 1.5rem;
  }
  
  .staff-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>