<template>
  <div class="appeals-page">
    <!-- Fondo SCP -->
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
    </div>

    <!-- Header -->
    <header class="appeals-header">
      <div class="header-content">
        <div class="header-left">
          <div class="header-logo">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                <path d="M13 8H7"></path>
                <path d="M17 12H7"></path>
              </svg>
            </div>
            <div class="header-title">
              <span class="header-main">SISTEMA DE APELACIONES</span>
              <span class="header-sub">APELA TUS ADVERTENCIAS Y BANEOS</span>
            </div>
          </div>
        </div>
        
        <div class="header-right">
          <div class="session-status">
            <div class="session-indicator active"></div>
            <span class="session-text">SISTEMA DE APELACIONES ACTIVO</span>
          </div>
          <div class="current-time">
            {{ currentTime }}
          </div>
          <div class="header-actions">
            <button class="back-button" @click="goToDashboard">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 12H5"></path>
                <path d="M12 19l-7-7 7-7"></path>
              </svg>
              <span>VOLVER AL DASHBOARD</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Contenido Principal -->
    <main class="appeals-main">
      <!-- Overlay de autenticación -->
      <div v-if="!currentUser?.is_authenticated" class="auth-modal-overlay">
        <div class="login-required">
          <div class="login-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <h3 class="login-title">ACCESO RESTRINGIDO</h3>
          <p class="login-text">Debes iniciar sesión para acceder al sistema de apelaciones</p>
          <button class="login-button" @click="redirectToLogin">
            INICIAR SESIÓN
          </button>
        </div>
      </div>
      
      <!-- Contenido autenticado -->
      <div v-else class="authenticated-content">
        <!-- Información del Usuario -->
        <div class="user-info-panel">
          <div class="user-avatar">
            <div class="avatar-placeholder">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
          </div>
          <div class="user-details">
            <h2 class="user-name">{{ currentUser?.roblox_username || 'Usuario' }}</h2>
            <div class="user-stats">
              <div class="stat-item">
                <span class="stat-label">ID Roblox:</span>
                <span class="stat-value">{{ currentUser?.roblox_id || 'N/A' }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Advertencias:</span>
                <span class="stat-value" :class="{ 'has-warns': currentUser?.warning_count > 0 }">
                  {{ currentUser?.warning_count || 0 }}
                </span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Estado:</span>
                <span class="stat-value" :class="{ 'banned': currentUser?.is_banned }">
                  {{ currentUser?.is_banned ? 'BANEADO' : 'ACTIVO' }}
                </span>
              </div>
            </div>
          </div>
          <div class="user-status">
            <div class="status-indicator" :class="{ 'active': !currentUser?.is_banned, 'banned': currentUser?.is_banned }"></div>
            <span class="status-text">
              {{ currentUser?.is_banned ? 'CUENTA SUSPENDIDA' : 'CUENTA ACTIVA' }}
            </span>
          </div>
        </div>

        <!-- Navegación -->
        <nav class="appeals-nav">
          <button 
            class="nav-button" 
            :class="{ 'active': activeTab === 'warnings' }"
            @click="setActiveTab('warnings')"
          >
            <div class="nav-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
            </div>
            <span class="nav-text">ADVERTENCIAS APELABLES</span>
            <span v-if="appealableWarnings.length > 0" class="nav-badge">
              {{ appealableWarnings.length }}
            </span>
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
            <span class="nav-text">BANEOS APELABLES</span>
            <span v-if="appealableBans.length > 0" class="nav-badge">
              {{ appealableBans.length }}
            </span>
          </button>
          
          <button 
            class="nav-button" 
            :class="{ 'active': activeTab === 'history' }"
            @click="setActiveTab('history')"
          >
            <div class="nav-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
              </svg>
            </div>
            <span class="nav-text">HISTORIAL DE APELACIONES</span>
          </button>
        </nav>

        <!-- Contenido de las pestañas -->
        <div class="appeals-content">
          <!-- Pestaña: Advertencias Apelables -->
          <div v-if="activeTab === 'warnings'" class="warnings-tab">
            <div class="tab-header">
              <h3 class="tab-title">ADVERTENCIAS APELABLES</h3>
              <p class="tab-description">
                Aquí puedes apelar las advertencias que hayas recibido. Cada advertencia debe ser apelada individualmente.
              </p>
            </div>
            <div v-if="appealCooldown && !appealCooldown.can_appeal" class="cooldown-warning">
              <div class="cooldown-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"></circle>
                      <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
              </div>
              <div class="cooldown-content">
                  <h4 class="cooldown-title">APELACIÓN EN ENFRIAMIENTO</h4>
                  
                  <!-- Solo mostrar UN mensaje, no dos -->
                  <div class="cooldown-message">
                      <!-- Opción 1: Si el backend envía un mensaje formateado -->
                      <p v-if="appealCooldown.message" class="cooldown-text">
                          {{ appealCooldown.message }}
                      </p>
                      <!-- Opción 2: Si tenemos fecha de cooldown -->
                      <p v-else-if="appealCooldown.cooldown_ends" class="cooldown-text">
                          Podrás apelar nuevamente: {{ formatDateInUserTimeZone(appealCooldown.cooldown_ends) }}
                      </p>
                      
                      <!-- Opción 3: Mensaje genérico -->
                      <p v-else class="cooldown-text">
                          Debes esperar para poder apelar nuevamente
                      </p>
                  </div>
              </div>
          </div>
            <div v-if="loadingWarnings" class="loading-state">
              <div class="loading-spinner"></div>
              <p class="loading-text">Cargando advertencias...</p>
            </div>
            
            <div v-else-if="appealableWarnings.length > 0" class="warnings-list">
              <div 
                v-for="warning in appealableWarnings" 
                :key="warning.id"
                class="warning-card"
                :class="{
                  'appealed': warning.appealed,
                  'expiring-soon': isExpiringSoon(warning.expires_at)
                }"
              >
                <div class="warning-header">
                  <div class="warning-info">
                    <h4 class="warning-title">
                      Advertencia #{{ warning.id }}
                      <span v-if="warning.appealed" class="appealed-badge">APELADA</span>
                      <span v-if="isExpiringSoon(warning.expires_at)" class="expiring-badge">PRÓXIMO A EXPIRAR</span>
                    </h4>
                    <div class="warning-meta">
                      <span class="meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"></circle>
                          <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        {{ formatDate(warning.created_at) }}
                      </span>
                      <span class="meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"></circle>
                          <line x1="12" y1="8" x2="12" y2="12"></line>
                          <line x1="12" y1="16" x2="12.01" y2="16"></line>
                        </svg>
                        Gravedad: 
                        <span class="severity" :class="`severity-${warning.severity}`">
                          {{ getSeverityText(warning.severity) }}
                        </span>
                      </span>
                      <span v-if="warning.expires_at" class="meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"></circle>
                          <line x1="12" y1="6" x2="12" y2="12"></line>
                          <line x1="12" y1="12" x2="16" y2="12"></line>
                        </svg>
                        Expira: {{ formatDateShort(warning.expires_at) }}
                      </span>
                    </div>
                  </div>
                  
                  <div class="warning-actions">
                    <button 
                      v-if="!warning.appealed"
                      class="action-button appeal"
                      @click="openAppealModal(warning, 'warning')"
                      :disabled="submittingAppeal"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                      </svg>
                      <span>APELAR</span>
                    </button>
                    
                    <button 
                      v-else
                      class="action-button viewed"
                      @click="viewAppealResponse(warning)"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                      <span>VER RESPUESTA</span>
                    </button>
                  </div>
                </div>
                
                <div class="warning-content">
                  <div class="reason-section">
                    <h5>Razón de la Advertencia:</h5>
                    <p>{{ warning.reason }}</p>
                  </div>
                  
                  <div v-if="warning.evidence" class="evidence-section">
                    <h5>Evidencia Presentada:</h5>
                    <p class="evidence-text">{{ truncateText(warning.evidence, 100) }}</p>
                    <button v-if="warning.evidence.length > 100" class="view-evidence-link" @click="viewEvidence(warning)">
                      Ver evidencia completa
                    </button>
                  </div>
                  
                  <div v-if="warning.appealed" class="appeal-section">
                    <h5>Tu Apelación:</h5>
                    <p class="appeal-message">{{ warning.appeal_message || 'Apelación presentada' }}</p>
                    <div v-if="warning.appeal_response" class="response-section">
                      <h6>Respuesta del Moderador:</h6>
                      <p class="response-text">{{ warning.appeal_response }}</p>
                      <span class="response-date">
                        Respondido: {{ formatDateShort(warning.appeal_responded_at) }}
                      </span>
                    </div>
                    <div v-else class="pending-response">
                      <span class="pending-badge">EN REVISIÓN</span>
                      <p class="pending-text">Tu apelación está siendo revisada por los moderadores</p>
                    </div>
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
              <h4 class="empty-title">No tienes advertencias apelables</h4>
              <p class="empty-text">
                No se encontraron advertencias activas que puedas apelar en este momento.
              </p>
            </div>
          </div>

          <!-- Pestaña: Baneos Apelables -->
          <div v-else-if="activeTab === 'bans'" class="bans-tab">
            <div class="tab-header">
              <h3 class="tab-title">BANEOS APELABLES</h3>
              <p class="tab-description">
                Aquí puedes apelar los baneos que hayas recibido. Solo los baneos que permiten apelación aparecerán aquí.
              </p>
            </div>

            <div v-if="loadingBans" class="loading-state">
              <div class="loading-spinner"></div>
              <p class="loading-text">Cargando baneos...</p>
            </div>
            
            <div v-else-if="appealableBans.length > 0" class="bans-list">
              <div 
                v-for="ban in appealableBans" 
                :key="ban.id"
                class="ban-card"
                :class="{
                  'appealed': ban.appealed,
                  'permanent': ban.ban_type === 'permanent'
                }"
              >
                <div class="ban-header">
                  <div class="ban-info">
                    <h4 class="ban-title">
                      Baneo #{{ ban.id }}
                      <span v-if="ban.appealed" class="appealed-badge">APELADO</span>
                      <span v-if="ban.ban_type === 'permanent'" class="permanent-badge">PERMANENTE</span>
                      <span v-else class="temporary-badge">TEMPORAL</span>
                    </h4>
                    <div class="ban-meta">
                      <span class="meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"></circle>
                          <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        {{ formatDate(ban.created_at) }}
                      </span>
                      <span class="meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="12" cy="12" r="10"></circle>
                          <line x1="12" y1="6" x2="12" y2="12"></line>
                          <line x1="12" y1="12" x2="16" y2="12"></line>
                        </svg>
                        {{ ban.ban_type === 'temporary' && ban.ends_at ? `Termina: ${formatDateShort(ban.ends_at)}` : 'Sin fecha de término' }}
                      </span>
                      <span class="meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                          <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                        Moderador: {{ ban.created_by?.roblox_username || 'Sistema' }}
                      </span>
                    </div>
                  </div>

                  
                  <div class="ban-actions">
                    <button 
                      v-if="!ban.appealed && ban.can_appeal"
                      class="action-button appeal"
                      @click="openAppealModal(ban, 'ban')"
                      :disabled="submittingAppeal"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                      </svg>
                      <span>APELAR BANEO</span>
                    </button>
                    
                    <button 
                      v-else-if="ban.appealed"
                      class="action-button viewed"
                      @click="viewAppealResponse(ban)"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                      <span>VER RESPUESTA</span>
                    </button>
                    
                    <button 
                      v-else
                      class="action-button disabled"
                      disabled
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line>
                      </svg>
                      <span>NO APELABLE</span>
                    </button>
                  </div>
                </div>
                
                <div class="ban-content">
                  <div class="reason-section">
                    <h5>Razón del Baneo:</h5>
                    <p>{{ ban.reason }}</p>
                  </div>
                  
                  <div v-if="ban.evidence" class="evidence-section">
                    <h5>Evidencia Presentada:</h5>
                    <p class="evidence-text">{{ truncateText(ban.evidence, 100) }}</p>
                    <button v-if="ban.evidence.length > 100" class="view-evidence-link" @click="viewEvidence(ban)">
                      Ver evidencia completa
                    </button>
                  </div>
                  
                  <div v-if="ban.appealed" class="appeal-section">
                    <h5>Tu Apelación:</h5>
                    <p class="appeal-message">{{ ban.appeal_message || 'Apelación presentada' }}</p>
                    <div v-if="ban.appeal_response" class="response-section">
                      <h6>Respuesta del Moderador:</h6>
                      <p class="response-text">{{ ban.appeal_response }}</p>
                      <span class="response-date">
                        Respondido: {{ formatDateShort(ban.appeal_responded_at) }}
                      </span>
                    </div>
                    <div v-else class="pending-response">
                      <span class="pending-badge">EN REVISIÓN</span>
                      <p class="pending-text">Tu apelación está siendo revisada por los moderadores</p>
                    </div>
                  </div>
                  
                  <div class="ban-details">
                    <div class="detail-item">
                      <span class="detail-label">Tipo:</span>
                      <span class="detail-value">{{ ban.ban_type === 'temporary' ? 'Temporal' : 'Permanente' }}</span>
                    </div>
                    <div v-if="ban.duration_days" class="detail-item">
                      <span class="detail-label">Duración:</span>
                      <span class="detail-value">{{ ban.duration_days }} días</span>
                    </div>
                    <div v-if="ban.ends_at" class="detail-item">
                      <span class="detail-label">Fecha de Término:</span>
                      <span class="detail-value">{{ formatDateFull(ban.ends_at) }}</span>
                    </div>
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
              <h4 class="empty-title">No tienes baneos apelables</h4>
              <p class="empty-text">
                No se encontraron baneos que puedas apelar en este momento, o no tienes baneos activos.
              </p>
            </div>
          </div>

          <!-- Pestaña: Historial de Apelaciones -->
          <div v-else-if="activeTab === 'history'" class="history-tab">
            <div class="tab-header">
              <h3 class="tab-title">HISTORIAL DE APELACIONES</h3>
              <p class="tab-description">
                Historial completo de todas tus apelaciones, incluyendo las ya resueltas.
              </p>
            </div>

            <div v-if="loadingHistory" class="loading-state">
              <div class="loading-spinner"></div>
              <p class="loading-text">Cargando historial...</p>
            </div>
            
            <div v-else-if="appealHistory.length > 0" class="history-list">
              <div 
              v-for="item in appealHistory" 
              :key="item.id"
              class="history-card"
              :class="{
                  'warning': item.type === 'warning',
                  'ban': item.type === 'ban',
                  'resolved': item.is_resolved,
                  'pending': !item.is_resolved
              }"
              >
                <div class="history-header">
                    <div class="history-type">
                        <span class="type-badge" :class="item.type">
                            {{ item.type === 'warning' ? 'ADVERTENCIA' : 'BANEO' }}
                        </span>
                        <span class="history-id">#{{ item.id }}</span>
                    </div>
                    
                    <div class="history-status">
                        <span class="status-badge" :class="getAppealStatus(item).class">
                            {{ getAppealStatus(item).text }}
                        </span>
                    </div>
                </div>
                
                <div class="history-content">
                    <div class="history-reason">
                    <h5>Razón Original:</h5>
                    <p>{{ item.reason }}</p>
                    </div>
                    
                    <div class="history-appeal">
                    <h5>Tu Apelación:</h5>
                    <p>{{ item.appeal_message || 'Apelación presentada' }}</p>
                    <span class="appeal-date">
                        Apelado: {{ formatDateShort(item.appealed_at || item.created_at) }}
                    </span>
                    </div>
                    
                    <div v-if="item.is_resolved" class="history-response">
                    <h5>Respuesta del Moderador:</h5>
                    <p>{{ item.appeal_response }}</p>
                    <div class="response-meta">
                        <span class="response-date">
                        Respondido: {{ formatDateShort(item.resolved_at) }}
                        </span>
                        <span v-if="item.appeal_responded_by" class="response-moderator">
                        por {{ item.appeal_responded_by }}
                        </span>
                    </div>
                    </div>
                    
                    <div v-else class="pending-notice">
                    <div class="pending-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                    </div>
                    <div class="pending-text">
                        <strong>EN REVISIÓN</strong>
                        <p>Tu apelación está siendo revisada por los moderadores</p>
                    </div>
                    </div>
                </div>
                
                <div class="history-footer">
                    <span class="history-date">
                    {{ formatDate(item.created_at) }}
                    </span>
                    <div class="history-actions">
                    <button 
                        v-if="item.evidence"
                        class="view-evidence-button"
                        @click="viewEvidence(item)"
                    >
                        VER EVIDENCIA
                    </button>
                    <button 
                        v-if="item.type === 'warning' && item.expires_at"
                        class="view-expiry-button"
                        @click="viewExpiry(item)"
                    >
                        VER EXPIRACIÓN
                    </button>
                    </div>
                </div>
              </div>
            </div>
            
            <div v-else class="empty-state">
              <div class="empty-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
              </div>
              <h4 class="empty-title">No hay historial de apelaciones</h4>
              <p class="empty-text">
                Aún no has realizado ninguna apelación. Las apelaciones que realices aparecerán aquí.
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal: Apelar -->
    <div v-if="showAppealModal" class="modal-overlay" @click.self="closeAppealModal">
      <div class="modal-content appeal-modal">
        <div class="modal-header">
          <h3 class="modal-title">
            {{ appealModal.type === 'warning' ? 'APELAR ADVERTENCIA' : 'APELAR BANEO' }}
          </h3>
          <button class="modal-close" @click="closeAppealModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="appeal-info">
            <div class="info-item">
              <span class="info-label">ID:</span>
              <span class="info-value">#{{ appealModal.id }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Tipo:</span>
              <span class="info-value">{{ appealModal.type === 'warning' ? 'Advertencia' : 'Baneo' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Razón Original:</span>
              <span class="info-value">{{ appealModal.reason }}</span>
            </div>
          </div>
          
          <form @submit.prevent="submitAppeal" class="appeal-form">
            <div class="form-group">
              <label class="form-label">Mensaje de Apelación *</label>
              <p class="form-hint">
                Explica por qué crees que esta {{ appealModal.type === 'warning' ? 'advertencia' : 'baneo' }} 
                debería ser revisada. Sé claro y conciso en tus argumentos.
              </p>
              <textarea
                v-model="appealMessage"
                class="form-textarea"
                placeholder="Describe tu situación y por qué mereces una reconsideración..."
                rows="6"
                required
                :maxlength="1000"
              ></textarea>
              <div class="char-counter">
                {{ appealMessage.length }}/1000 caracteres
              </div>
            </div>
            
            <div class="form-group">
              <label class="form-label">Evidencia Adicional (Opcional)</label>
              <p class="form-hint">
                Si tienes evidencia adicional que respalde tu apelación (capturas de pantalla, videos, etc.), 
                incluye los enlaces aquí.
              </p>
              <textarea
                v-model="additionalEvidence"
                class="form-textarea"
                placeholder="Enlaces a evidencia adicional..."
                rows="3"
                :maxlength="500"
              ></textarea>
              <div class="char-counter">
                {{ additionalEvidence.length }}/500 caracteres
              </div>
            </div>
            
            <div class="appeal-notice">
              <div class="notice-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
              </div>
              <div class="notice-content">
                <h4>IMPORTANTE</h4>
                <p>
                  • Las apelaciones se revisan por orden de llegada<br>
                  • Proporciona toda la información relevante<br>
                  • Sé respetuoso en tu mensaje<br>
                  • El proceso puede tardar varios días<br>
                  • Recibirás una notificación cuando haya una respuesta
                </p>
              </div>
            </div>
            
            <div class="form-actions">
              <button type="button" class="cancel-button" @click="closeAppealModal">
                CANCELAR
              </button>
              <button type="submit" class="submit-button" :disabled="submittingAppeal">
                <span v-if="submittingAppeal">ENVIANDO APELACIÓN...</span>
                <span v-else>ENVIAR APELACIÓN</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal: Ver Respuesta -->
    <div v-if="showResponseModal" class="modal-overlay" @click.self="closeResponseModal">
      <div class="modal-content response-modal">
        <div class="modal-header">
          <h3 class="modal-title">RESPUESTA A TU APELACIÓN</h3>
          <button class="modal-close" @click="closeResponseModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="response-info">
            <div class="info-item">
              <span class="info-label">ID:</span>
              <span class="info-value">#{{ responseModal.id }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Tipo:</span>
              <span class="info-value">{{ responseModal.type === 'warning' ? 'Advertencia' : 'Baneo' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">Estado:</span>
              <span class="info-value status-badge" :class="responseModal.status">
                {{ getStatusText(responseModal.status) }}
              </span>
            </div>
            <div class="info-item">
              <span class="info-label">Fecha de Respuesta:</span>
              <span class="info-value">{{ formatDateFull(responseModal.responded_at) }}</span>
            </div>
          </div>
          
          <div class="response-sections">
            <div class="section">
              <h4>Tu Apelación Original</h4>
              <div class="section-content">
                <p>{{ responseModal.appeal_message }}</p>
              </div>
            </div>
            
            <div class="section">
              <h4>Respuesta del Moderador</h4>
              <div class="section-content">
                <p>{{ responseModal.response }}</p>
              </div>
              <div v-if="responseModal.moderator" class="moderator-info">
                <span class="moderator-label">Respondido por:</span>
                <span class="moderator-name">{{ responseModal.moderator }}</span>
              </div>
            </div>
            
            <div v-if="responseModal.notes" class="section">
              <h4>Notas Adicionales</h4>
              <div class="section-content">
                <p>{{ responseModal.notes }}</p>
              </div>
            </div>
          </div>
          
          <div class="modal-actions">
            <button class="close-button" @click="closeResponseModal">
              CERRAR
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal: Ver Evidencia -->
    <div v-if="showEvidenceModal" class="modal-overlay" @click.self="closeEvidenceModal">
      <div class="modal-content evidence-modal">
        <div class="modal-header">
          <h3 class="modal-title">EVIDENCIA PRESENTADA</h3>
          <button class="modal-close" @click="closeEvidenceModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="evidence-content">
            <div class="evidence-header">
              <div class="evidence-type">
                <span class="type-badge">{{ evidenceModal.type === 'warning' ? 'ADVERTENCIA' : 'BANEO' }}</span>
                <span class="evidence-id">#{{ evidenceModal.id }}</span>
              </div>
              <div class="evidence-meta">
                <span class="meta-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                  {{ formatDate(evidenceModal.created_at) }}
                </span>
              </div>
            </div>
            
            <div class="evidence-text">
              <pre>{{ evidenceModal.evidence }}</pre>
            </div>
            
            <div v-if="hasValidLinks" class="evidence-actions">
              <button 
                class="copy-button"
                @click="copyEvidenceLinks"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
                <span>COPIAR ENLACES</span>
              </button>
              
              <button 
                class="open-button"
                @click="openEvidenceLinks"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
                <span>ABRIR ENLACES</span>
              </button>
            </div>
          </div>
          
          <div class="evidence-notice">
            <div class="notice-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
            </div>
            <div class="notice-content">
              <h4>INFORMACIÓN IMPORTANTE</h4>
              <p>
                • Esta es la evidencia presentada por el moderador<br>
                • Los enlaces pueden llevar a Discord, YouTube, Imgur, etc.<br>
                • Solo copia o abre enlaces de fuentes confiables<br>
                • Para más detalles, contacta al equipo de moderación
              </p>
            </div>
          </div>
          
          <div class="modal-actions">
            <button class="close-button" @click="closeEvidenceModal">
              CERRAR
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Estado principal
const currentUser = ref(null)
const currentTime = ref('')
const activeTab = ref('warnings')
const loadingWarnings = ref(false)
const loadingBans = ref(false)
const loadingHistory = ref(false)
const submittingAppeal = ref(false)
const appealCooldown = ref(null)

// Modales
const showAppealModal = ref(false)
const showResponseModal = ref(false)
const showEvidenceModal = ref(false)

// Datos
const warnings = ref([])
const bans = ref([])
const appealHistory = ref([])

// Modal data
const appealModal = reactive({
  id: null,
  type: null, // 'warning' or 'ban'
  reason: ''
})

const responseModal = reactive({
  id: null,
  type: null,
  status: '',
  appeal_message: '',
  response: '',
  moderator: '',
  responded_at: null,
  notes: ''
})

const evidenceModal = reactive({
  id: null,
  type: null,
  evidence: '',
  created_at: null
})

// Formulario
const appealMessage = ref('')
const additionalEvidence = ref('')

// Notificaciones
const notifications = ref([])
let notificationId = 0

// Computed
const appealableWarnings = computed(() => {
  return warnings.value.filter(w => 
    w.status === 'active' && 
    !w.appealed
  )
})

const appealableBans = computed(() => {
  return bans.value.filter(b => 
    b.is_active && 
    b.can_appeal && 
    !b.appealed
  )
})

const hasValidLinks = computed(() => {
  if (!evidenceModal.evidence) return false
  const urlPattern = /https?:\/\/[^\s]+/g
  return urlPattern.test(evidenceModal.evidence)
})

// Métodos
const setActiveTab = (tab) => {
  activeTab.value = tab
  switch(tab) {
    case 'warnings':
      loadWarnings()
      break
    case 'bans':
      loadBans()
      break
    case 'history':
      loadAppealHistory()
      break
  }
}

const loadWarnings = async () => {
  if (!currentUser.value) return
  
  loadingWarnings.value = true
  try {
    const response = await fetch('/api/moderation/user/appeals/', {
      credentials: 'include'
    })
    if (response.ok) {
      const data = await response.json()
      console.log('Warnings data:', data)  // Debug
      
      // Para la pestaña de advertencias, mostrar solo las APELABLES
      warnings.value = data.appealable_warnings || []
      
      // Verificar cooldown
      if (data.appeal_cooldown) {
        appealCooldown.value = data.appeal_cooldown
      }
    }
  } catch (error) {
    console.error('Error cargando advertencias:', error)
    showNotification('ERROR', 'Error al cargar advertencias', 'error', 4000)
  } finally {
    loadingWarnings.value = false
  }
}

const loadBans = async () => {
  if (!currentUser.value) return
  
  loadingBans.value = true
  try {
    const response = await fetch('/api/moderation/user/appeals/', {
      credentials: 'include'
    })
    if (response.ok) {
      const data = await response.json()
      console.log('Bans data:', data)  // Debug
      
      // Para la pestaña de baneos, mostrar solo los APELABLES
      bans.value = data.appealable_bans || []
    }
  } catch (error) {
    console.error('Error cargando baneos:', error)
    showNotification('ERROR', 'Error al cargar baneos', 'error', 4000)
  } finally {
    loadingBans.value = false
  }
}

const loadAppealHistory = async () => {
  if (!currentUser.value) return
  
  loadingHistory.value = true
  try {
    const response = await fetch('/api/moderation/user/appeals/', {
      credentials: 'include'
    })
    if (response.ok) {
      const data = await response.json()
      console.log('History data:', data)  // Debug
      
      // Combinar TODAS las apelaciones (warns y bans) para historial
      const allAppeals = [
        ...(data.appealed_warnings || []),
        ...(data.appealed_bans || [])
      ]
      
      // Ordenar por fecha de apelación (más reciente primero)
      appealHistory.value = allAppeals.sort((a, b) => {
        const dateA = a.appealed_at ? new Date(a.appealed_at) : new Date(a.created_at)
        const dateB = b.appealed_at ? new Date(b.appealed_at) : new Date(b.created_at)
        return dateB - dateA
      })
      
      console.log('Sorted history:', appealHistory.value)  // Debug
    }
  } catch (error) {
    console.error('Error cargando historial:', error)
    showNotification('ERROR', 'Error al cargar historial de apelaciones', 'error', 4000)
  } finally {
    loadingHistory.value = false
  }
}

const getAppealStatus = (appeal) => {
  if (!appeal.is_resolved) {
    return {
      status: 'pending',
      text: 'PENDIENTE',
      class: 'pending'
    }
  }
  
  const response = appeal.appeal_response?.toLowerCase() || ''
  
  // Buscar múltiples variantes de "aceptado"
  const acceptedKeywords = ['aceptado', 'aceptada', 'aprobado', 'aprobada', 'acepto', 'acepta']
  const isAccepted = acceptedKeywords.some(keyword => response.includes(keyword))
  
  // Buscar variantes de "rechazado"
  const rejectedKeywords = ['rechazado', 'rechazada', 'denegado', 'denegada', 'rechazo', 'rechaza']
  const isRejected = rejectedKeywords.some(keyword => response.includes(keyword))
  
  // Si no está claro, revisar el estado del warn/ban
  if (appeal.type === 'warning' && appeal.status === 'removed') {
    return {
      status: 'approved',
      text: 'APROBADA',
      class: 'approved'
    }
  }
  
  if (appeal.type === 'ban' && appeal.status === 'revoked') {
    return {
      status: 'approved',
      text: 'APROBADA',
      class: 'approved'
    }
  }
  
  // Por defecto, decidir basado en palabras clave
  if (isAccepted) {
    return {
      status: 'approved',
      text: 'APROBADA',
      class: 'approved'
    }
  } else if (isRejected) {
    return {
      status: 'rejected',
      text: 'RECHAZADA',
      class: 'rejected'
    }
  } else {
    // Si no se puede determinar, marcar como respondida pero sin decisión clara
    return {
      status: 'responded',
      text: 'RESPONDIDA',
      class: 'pending'
    }
  }
}

const truncateText = (text, maxLength) => {
  if (!text || text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const viewEvidence = (item) => {
  evidenceModal.id = item.id
  evidenceModal.type = 'warning' in item ? 'warning' : 'ban'
  evidenceModal.evidence = item.evidence || ''
  evidenceModal.created_at = item.created_at
  showEvidenceModal.value = true
}

const closeEvidenceModal = () => {
  showEvidenceModal.value = false
  evidenceModal.id = null
  evidenceModal.type = null
  evidenceModal.evidence = ''
  evidenceModal.created_at = null
}

const extractLinks = () => {
  if (!evidenceModal.evidence) return []
  const urlPattern = /https?:\/\/[^\s]+/g
  return evidenceModal.evidence.match(urlPattern) || []
}

const copyEvidenceLinks = async () => {
  const links = extractLinks()
  if (links.length === 0) {
    showNotification('INFO', 'No se encontraron enlaces', 'info', 3000)
    return
  }
  
  const textToCopy = links.join('\n')
  try {
    await navigator.clipboard.writeText(textToCopy)
    showNotification('ÉXITO', 'Enlaces copiados al portapapeles', 'success', 3000)
  } catch (error) {
    console.error('Error copiando enlaces:', error)
    showNotification('ERROR', 'Error al copiar enlaces', 'error', 3000)
  }
}

const openEvidenceLinks = () => {
  const links = extractLinks()
  if (links.length === 0) {
    showNotification('INFO', 'No se encontraron enlaces', 'info', 3000)
    return
  }
  
  links.forEach(link => {
    window.open(link, '_blank', 'noopener,noreferrer')
  })
  
  showNotification('INFO', `Abriendo ${links.length} enlace(s)`, 'info', 3000)
}

const openAppealModal = (item, type) => {
  // Verificar cooldown primero
  if (appealCooldown.value && !appealCooldown.value.can_appeal) {
    showNotification('ERROR', appealCooldown.value.reason, 'error', 5000)
    return
  }
  
  // Verificar si ya está apelado
  if (item.appealed) {
    viewAppealResponse(item)
    return
  }
  
  appealModal.id = item.id
  appealModal.type = type
  appealModal.reason = item.reason
  appealMessage.value = ''
  additionalEvidence.value = ''
  showAppealModal.value = true
}

const closeAppealModal = () => {
  showAppealModal.value = false
  appealModal.id = null
  appealModal.type = null
  appealModal.reason = ''
}

const submitAppeal = async () => {
  if (!appealMessage.value.trim()) {
    showNotification('ERROR', 'Debes escribir un mensaje de apelación', 'error', 4000)
    return
  }
  
  submittingAppeal.value = true
  
  try {
    const csrfToken = getCSRFToken()
    const endpoint = appealModal.type === 'warning' 
      ? `/api/moderation/warns/${appealModal.id}/appeal/`
      : `/api/moderation/bans/${appealModal.id}/appeal/` // Necesitarías crear este endpoint
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      credentials: 'include',
      body: JSON.stringify({
        message: appealMessage.value,
        additional_evidence: additionalEvidence.value
      })
    })
    
    if (response.ok) {
      showNotification('ÉXITO', 'Apelación enviada correctamente', 'success', 5000)
      closeAppealModal()
      
      // Recargar datos
      if (appealModal.type === 'warning') {
        loadWarnings()
      } else {
        loadBans()
      }
      loadAppealHistory()
      
    } else {
      const error = await response.json()
      showNotification('ERROR', error.error || 'Error al enviar apelación', 'error', 5000)
    }
  } catch (error) {
    console.error('Error enviando apelación:', error)
    showNotification('ERROR', 'Error al enviar apelación', 'error', 5000)
  } finally {
    submittingAppeal.value = false
  }
}

const viewAppealResponse = (item) => {
  responseModal.id = item.id
  responseModal.type = 'warning' in item ? 'warning' : 'ban'
  responseModal.appeal_message = item.appeal_message || 'Apelación presentada'
  responseModal.response = item.appeal_response || ''
  responseModal.status = item.appeal_response ? 
    (item.appeal_response.toLowerCase().includes('aceptado') ? 'approved' : 'rejected') : 
    'pending'
  responseModal.moderator = item.appeal_responded_by?.roblox_username
  responseModal.responded_at = item.appeal_responded_at
  responseModal.notes = item.additional_notes || ''
  
  showResponseModal.value = true
}

const closeResponseModal = () => {
  showResponseModal.value = false
  Object.keys(responseModal).forEach(key => {
    responseModal[key] = null
  })
}

const viewHistoryDetails = (item) => {
  viewAppealResponse(item)
}

const viewExpiry = (item) => {
  showNotification('INFO', `Expira: ${formatDateFull(item.expires_at)}`, 'info', 5000)
}

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
    'approved': 'APROBADA',
    'rejected': 'RECHAZADA',
    'pending': 'PENDIENTE',
    'active': 'ACTIVA',
    'inactive': 'INACTIVA'
  }
  return statusMap[status] || status
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  })
}

const formatDateShort = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES')
}

const formatDateFull = (dateString) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  
  // Usar la zona horaria local del usuario automáticamente
  return date.toLocaleString('es-ES', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}

const getUserTimeZone = () => {
  return Intl.DateTimeFormat().resolvedOptions().timeZone
}

// Función para formatear fecha en la zona horaria del usuario
const formatDateInUserTimeZone = (dateString, format = 'full') => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  const userTimeZone = getUserTimeZone()
  
  const options = {
    timeZone: userTimeZone,
    day: '2-digit',
    month: format === 'short' ? '2-digit' : 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  }
  
  if (format === 'short') {
    // Para formato corto: DD/MM/YYYY HH:mm
    return date.toLocaleString('es-ES', {
      ...options,
      month: '2-digit'
    }).replace(',', '')
  }
  
  // Formato completo: DD de Mes de YYYY, HH:mm
  return date.toLocaleString('es-ES', options)
}

const isExpiringSoon = (dateString) => {
  if (!dateString) return false
  const date = new Date(dateString)
  const now = new Date()
  const diffDays = (date - now) / 86400000
  return diffDays > 0 && diffDays <= 7
}

const goToDashboard = () => {
  router.push('/dashboard')
}

const redirectToLogin = () => {
  router.push('/login')
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
    const response = await fetch('/api/auth/user/', {
      credentials: 'include'
    })
    if (response.ok) {
      const data = await response.json()
      currentUser.value = data
      if (data.is_authenticated) {
        loadWarnings()
      }
    }
  } catch (error) {
    console.error('Error obteniendo usuario:', error)
  }
}

// CSRF Token
const getCSRFToken = () => {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1]
  
  if (cookieValue) return cookieValue
  
  const metaTag = document.querySelector('meta[name="csrf-token"]')
  if (metaTag) return metaTag.content
  
  return ''
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
/* Estilos base - similares a Moderacion_Global.vue */
.appeals-page {
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

/* Fondo SCP - igual que en Moderacion_Global */
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
.appeals-header {
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

/* Contenido Principal */
.appeals-main {
  position: relative;
  z-index: 2;
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
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

.login-required {
  text-align: center;
  background: rgba(30, 30, 30, 0.9);
  border: 1px solid #333;
  padding: 3rem;
  max-width: 400px;
  width: 100%;
}

.login-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 2rem;
  background: rgba(255, 51, 51, 0.1);
  border: 2px solid rgba(255, 51, 51, 0.3);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-icon svg {
  width: 40px;
  height: 40px;
  color: #ff3333;
}

.login-title {
  font-size: 1.5rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1rem 0;
  font-family: 'Consolas', 'Courier New', monospace;
}

.login-text {
  color: #aaa;
  margin: 0 0 2rem 0;
  line-height: 1.5;
}

.login-button {
  padding: 0.8rem 2rem;
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  color: #ff3333;
  font-family: 'Consolas', monospace;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-button:hover {
  background: rgba(255, 51, 51, 0.2);
  border-color: rgba(255, 51, 51, 0.5);
}

/* Información del Usuario */
.user-info-panel {
  display: flex;
  align-items: center;
  gap: 2rem;
  background: rgba(30, 30, 30, 0.9);
  border: 1px solid #444;
  padding: 1.5rem 2rem;
  margin-bottom: 2rem;
}

.user-avatar {
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 60px;
  height: 60px;
  background: rgba(255, 51, 51, 0.1);
  border: 2px solid rgba(255, 51, 51, 0.3);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-placeholder svg {
  width: 30px;
  height: 30px;
  color: #ff3333;
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 0.5rem 0;
}

.user-stats {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
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
  font-size: 1rem;
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

.user-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 0px;
}

.status-indicator.active {
  background: #4CAF50;
  box-shadow: 0 0 6px #4CAF50;
}

.status-indicator.banned {
  background: #f44336;
  box-shadow: 0 0 6px #f44336;
}

.status-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: #ccc;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

/* Navegación */
.appeals-nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #333;
  padding-bottom: 1rem;
}

.nav-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  padding: 0.8rem 1.5rem;
  background: rgba(30, 30, 30, 0.9);
  border: 1px solid #444;
  border-bottom: none;
  color: #aaa;
  font-family: inherit;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  position: relative;
  margin-bottom: -1px;
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
  border-bottom: 1px solid rgba(15, 15, 15, 0.98);
  margin-bottom: -2px;
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

.nav-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #ff3333;
  color: #fff;
  font-size: 0.7rem;
  font-weight: 700;
  min-width: 20px;
  height: 20px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 0.3rem;
  font-family: 'Consolas', monospace;
}

/* Contenido de las pestañas */
.appeals-content {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  min-height: 400px;
}

.tab-header {
  padding: 2rem 2rem 1rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tab-title {
  font-size: 1.5rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 0.5rem 0;
  font-family: 'Consolas', 'Courier New', monospace;
}

.tab-description {
  color: #aaa;
  line-height: 1.5;
  margin: 0;
}

/* Estados de carga y vacío */
.loading-state,
.empty-state {
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
  margin-bottom: 1.5rem;
}

.empty-icon svg {
  width: 100%;
  height: 100%;
}

.empty-title {
  font-size: 1.2rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1rem 0;
}

.empty-text {
  font-size: 1rem;
  color: #aaa;
  margin: 0;
  max-width: 400px;
}

/* Listas de advertencias y baneos */
.warnings-list,
.bans-list,
.history-list {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.warning-card,
.ban-card,
.history-card {
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  transition: all 0.3s ease;
}

.warning-card:hover,
.ban-card:hover,
.history-card:hover {
  border-color: #555;
  background: rgba(35, 35, 35, 0.9);
}

.warning-card.appealed {
  border-color: #2196F3;
  background: rgba(33, 150, 243, 0.05);
}

.warning-card.expiring-soon {
  border-color: #ff3333;
  background: rgba(255, 51, 51, 0.05);
}

.ban-card.permanent {
  border-color: #f44336;
}

/* Headers de tarjetas */
.warning-header,
.ban-header,
.history-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.warning-info,
.ban-info,
.history-info {
  flex: 1;
}

.warning-title,
.ban-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.appealed-badge,
.expiring-badge,
.permanent-badge,
.temporary-badge {
  padding: 0.2rem 0.5rem;
  border-radius: 2px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.appealed-badge {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
  border: 1px solid rgba(33, 150, 243, 0.3);
}

.expiring-badge {
  background: rgba(255, 51, 51, 0.1);
  color: #ff3333;
  border: 1px solid rgba(255, 51, 51, 0.3);
}

.permanent-badge {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.temporary-badge {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

.warning-meta,
.ban-meta {
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

.severity {
  padding: 0.2rem 0.5rem;
  border-radius: 2px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
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

.warning-actions,
.ban-actions {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-family: 'Consolas', monospace;
  white-space: nowrap;
}

.action-button.appeal {
  background: rgba(33, 150, 243, 0.1);
  border: 1px solid rgba(33, 150, 243, 0.3);
  color: #2196F3;
}

.action-button.appeal:hover:not(:disabled) {
  background: rgba(33, 150, 243, 0.2);
  border-color: rgba(33, 150, 243, 0.5);
}

.action-button.viewed {
  background: rgba(158, 158, 158, 0.1);
  border: 1px solid rgba(158, 158, 158, 0.3);
  color: #9E9E9E;
}

.action-button.viewed:hover {
  background: rgba(158, 158, 158, 0.2);
  border-color: rgba(158, 158, 158, 0.5);
}

.action-button.disabled {
  background: rgba(97, 97, 97, 0.1);
  border: 1px solid rgba(97, 97, 97, 0.3);
  color: #616161;
  cursor: not-allowed;
}

.action-button svg {
  width: 16px;
  height: 16px;
}

/* Contenido de tarjetas */
.warning-content,
.ban-content,
.history-content {
  padding: 1.5rem;
}

.reason-section,
.evidence-section,
.appeal-section,
.response-section,
.history-appeal,
.history-response {
  margin-bottom: 1.5rem;
}

.reason-section:last-child,
.evidence-section:last-child,
.appeal-section:last-child {
  margin-bottom: 0;
}

.reason-section h5,
.evidence-section h5,
.appeal-section h5,
.response-section h6,
.history-appeal h5,
.history-response h5 {
  font-size: 0.9rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 0.5rem 0;
  font-family: 'Consolas', monospace;
}

.reason-section p,
.evidence-text,
.appeal-message,
.response-text,
.history-appeal p,
.history-response p {
  color: #ccc;
  line-height: 1.5;
  margin: 0;
}

.evidence-text {
  white-space: pre-wrap;
  word-break: break-word;
  padding: 1rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 2px;
  margin-bottom: 0.5rem;
}

.view-evidence-link {
  background: none;
  border: none;
  color: #2196F3;
  font-size: 0.85rem;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
  font-family: 'Consolas', monospace;
  transition: color 0.3s ease;
}

.view-evidence-link:hover {
  color: #64B5F6;
}

.response-section {
  padding: 1rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 2px;
  margin-top: 1rem;
}

.response-date {
  display: block;
  font-size: 0.8rem;
  color: #888;
  margin-top: 0.5rem;
  font-family: 'Consolas', monospace;
}

.pending-response {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 152, 0, 0.1);
  border: 1px solid rgba(255, 152, 0, 0.3);
  border-radius: 2px;
  margin-top: 1rem;
}

.pending-badge {
  padding: 0.2rem 0.5rem;
  background: rgba(255, 152, 0, 0.2);
  border: 1px solid rgba(255, 152, 0, 0.4);
  color: #FF9800;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.pending-text {
  color: #FF9800;
  font-size: 0.9rem;
  margin: 0;
}

/* Detalles de baneos */
.ban-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
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
}

/* Historial */
.history-header {
  padding: 1rem 1.5rem;
}

.history-type {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.type-badge {
  padding: 0.3rem 0.6rem;
  border-radius: 2px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.type-badge.warning {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

.type-badge.ban {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.history-id {
  font-size: 0.9rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.history-status {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 0.3rem 0.6rem;
  border-radius: 2px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
}

.status-badge.approved {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.status-badge.rejected {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.status-badge.pending {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

.history-content {
  padding: 1.5rem;
}

.history-reason,
.history-appeal,
.history-response {
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.history-response:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.appeal-date {
  display: block;
  font-size: 0.8rem;
  color: #888;
  margin-top: 0.5rem;
  font-family: 'Consolas', monospace;
}

.response-meta {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #888;
}

.response-moderator {
  color: #2196F3;
  font-weight: 500;
}

.pending-notice {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 152, 0, 0.1);
  border: 1px solid rgba(255, 152, 0, 0.3);
  border-radius: 2px;
  margin-top: 1rem;
}

.pending-icon {
  width: 24px;
  height: 24px;
  color: #FF9800;
  flex-shrink: 0;
}

.pending-text {
  flex: 1;
}

.pending-text strong {
  color: #FF9800;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
  font-size: 0.9rem;
  display: block;
  margin-bottom: 0.3rem;
}

.pending-text p {
  color: #ccc;
  font-size: 0.85rem;
  margin: 0;
  line-height: 1.4;
}

.history-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-date {
  font-size: 0.85rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.history-actions {
  display: flex;
  gap: 0.5rem;
}

.view-evidence-button,
.view-expiry-button {
  padding: 0.3rem 0.6rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  font-family: 'Consolas', monospace;
}

.view-evidence-button {
  background: rgba(33, 150, 243, 0.1);
  border: 1px solid rgba(33, 150, 243, 0.3);
  color: #2196F3;
}

.view-evidence-button:hover {
  background: rgba(33, 150, 243, 0.2);
  border-color: rgba(33, 150, 243, 0.5);
}

.view-expiry-button {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  color: #4CAF50;
}

.view-expiry-button:hover {
  background: rgba(76, 175, 80, 0.2);
  border-color: rgba(76, 175, 80, 0.5);
}

/* Modales - similares a Moderacion_Global */
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
  max-width: 700px;
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

/* Modal de apelación */
.appeal-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #444;
}

.info-item {
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

.appeal-form {
  margin-top: 1rem;
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
  min-height: 120px;
}

.form-textarea:focus {
  outline: none;
  border-color: #ff3333;
  box-shadow: 0 0 0 2px rgba(255, 51, 51, 0.1);
}

.char-counter {
  text-align: right;
  font-size: 0.8rem;
  color: #888;
  margin-top: 0.5rem;
  font-family: 'Consolas', monospace;
}

.appeal-notice {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(255, 51, 51, 0.05);
  border: 1px solid rgba(255, 51, 51, 0.2);
  border-radius: 2px;
  margin-bottom: 2rem;
}

.notice-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  color: #ff3333;
}

.notice-content h4 {
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 0.5rem 0;
  font-family: 'Consolas', monospace;
  font-size: 0.9rem;
}

.notice-content p {
  color: #ccc;
  font-size: 0.85rem;
  line-height: 1.5;
  margin: 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
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
  background: rgba(33, 150, 243, 0.1);
  border: 1px solid rgba(33, 150, 243, 0.3);
  color: #2196F3;
}

.submit-button:hover:not(:disabled) {
  background: rgba(33, 150, 243, 0.2);
  border-color: rgba(33, 150, 243, 0.5);
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal de respuesta */
.response-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #444;
}

.response-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section {
  padding: 1.5rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 2px;
}

.section h4 {
  font-size: 0.9rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 1rem 0;
  font-family: 'Consolas', monospace;
}

.section-content p {
  color: #ccc;
  line-height: 1.5;
  margin: 0;
}

.moderator-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}

.close-button {
  padding: 0.8rem 1.5rem;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  color: #aaa;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Consolas', monospace;
}

.close-button:hover {
  background: rgba(50, 50, 50, 0.7);
  border-color: #555;
  color: #fff;
}

/* Modal de evidencia */
.evidence-modal {
  max-width: 800px;
}

.evidence-content {
  margin-bottom: 2rem;
}

.evidence-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #444;
}

.evidence-type {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.evidence-id {
  font-size: 0.9rem;
  color: #888;
  font-family: 'Consolas', monospace;
}

.evidence-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #aaa;
}

.evidence-meta svg {
  width: 14px;
  height: 14px;
}

.evidence-text {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  padding: 1.5rem;
  border-radius: 2px;
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 1.5rem;
}

.evidence-text pre {
  color: #ccc;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: 'Consolas', 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
}

.evidence-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.copy-button,
.open-button {
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

.copy-button {
  background: rgba(33, 150, 243, 0.1);
  border: 1px solid rgba(33, 150, 243, 0.3);
  color: #2196F3;
}

.copy-button:hover {
  background: rgba(33, 150, 243, 0.2);
  border-color: rgba(33, 150, 243, 0.5);
}

.open-button {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  color: #4CAF50;
}

.open-button:hover {
  background: rgba(76, 175, 80, 0.2);
  border-color: rgba(76, 175, 80, 0.5);
}

.copy-button svg,
.open-button svg {
  width: 16px;
  height: 16px;
}

.evidence-notice {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(255, 51, 51, 0.05);
  border: 1px solid rgba(255, 51, 51, 0.2);
  border-radius: 2px;
  margin-bottom: 1.5rem;
}

.notice-icon {
  width: 24px;
  height: 24px;
  color: #ff3333;
  flex-shrink: 0;
}

.notice-content h4 {
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 0.5rem 0;
  font-family: 'Consolas', monospace;
  font-size: 0.9rem;
}

.notice-content p {
  color: #ccc;
  font-size: 0.85rem;
  line-height: 1.5;
  margin: 0;
}

/* Scrollbar personalizada para el texto de evidencia */
.evidence-text::-webkit-scrollbar {
  width: 8px;
}

.evidence-text::-webkit-scrollbar-track {
  background: rgba(40, 40, 40, 0.6);
  border-radius: 4px;
}

.evidence-text::-webkit-scrollbar-thumb {
  background: rgba(100, 100, 100, 0.6);
  border-radius: 4px;
}

.evidence-text::-webkit-scrollbar-thumb:hover {
  background: rgba(120, 120, 120, 0.8);
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

/* Cooldown warning */
.cooldown-warning {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(255, 152, 0, 0.1);
  border: 1px solid rgba(255, 152, 0, 0.3);
  margin: 1rem 0 2rem 0;
  align-items: flex-start;
}

.cooldown-icon {
  width: 24px;
  height: 24px;
  color: #FF9800;
  flex-shrink: 0;
}

.cooldown-content {
  flex: 1;
}

.cooldown-title {
  color: #FF9800;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 0.5rem 0;
  font-family: 'Consolas', monospace;
  font-size: 0.9rem;
}

.cooldown-text {
  color: #ccc;
  margin: 0 0 0.5rem 0;
  line-height: 1.5;
}

.cooldown-time {
  color: #FF9800;
  font-weight: 600;
  margin: 0;
  font-family: 'Consolas', monospace;
  font-size: 0.9rem;
}

/* Responsive */
@media (max-width: 768px) {
  .appeals-header,
  .appeals-main {
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
  
  .user-info-panel {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .user-stats {
    justify-content: center;
  }
  
  .appeals-nav {
    flex-direction: column;
  }
  
  .nav-button {
    justify-content: flex-start;
  }
  
  .warning-header,
  .ban-header,
  .history-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .warning-actions,
  .ban-actions {
    width: 100%;
    justify-content: flex-start;
  }
  
  .action-button {
    flex: 1;
  }
  
  .modal-content {
    max-height: 95vh;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .cancel-button,
  .submit-button {
    width: 100%;
  }
  
  .evidence-actions {
    flex-direction: column;
  }
  
  .copy-button,
  .open-button {
    width: 100%;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .appeals-main {
    padding: 1.5rem;
  }
}
</style>