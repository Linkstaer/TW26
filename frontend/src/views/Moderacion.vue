<template>
  <div class="moderacion-page">
    <!-- Fondo SCP -->
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
    </div>

    <!-- Header -->
    <div class="moderacion-header">
      <div class="header-left">
        <div class="header-logo">
          <div class="header-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#ff3333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 8v4"></path>
              <path d="M12 16h.01"></path>
            </svg>
          </div>
          <div class="header-title">
            <span class="header-main">CONTROL DE MODERACIÓN</span>
            <span class="header-sub">DIVISIÓN DE SEGURIDAD Y CUMPLIMIENTO</span>
          </div>
        </div>
      </div>
      
      <div class="header-right">
        <div class="session-status">
          <div class="session-indicator active"></div>
          <span class="session-text">{{ userRole?.toUpperCase() || 'NO AUTORIZADO' }}</span>
        </div>
        <div class="current-time">
          {{ currentTime }}
        </div>
        <button class="back-button" @click="$router.push('/dashboard')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"></path>
          </svg>
          VOLVER
        </button>
      </div>
    </div>

    <!-- Contenido Principal - Tarjetas de Mods -->
    <main class="moderacion-main">
      <div class="moderacion-header-section">
        <h1 class="moderacion-title">PANEL DE MODERACIÓN</h1>
        <div class="moderacion-subtitle">FUNCIONES DE MODERACIÓN AUTORIZADAS</div>
        
        <!-- Estadísticas Rápidas - MODIFICADO -->
        <div class="quick-stats">
          <!-- SSU Status -->
          <div class="stat-item ssu-status" :class="{'on': ssuStatus, 'off': !ssuStatus}">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-label">SSU STATUS</span>
              <span class="stat-value ssu-value" :class="{'on': ssuStatus, 'off': !ssuStatus}">
                {{ ssuStatus ? 'ACTIVE' : 'INACTIVE' }}
              </span>
              <div class="ssu-indicator-light" :class="{'active': ssuStatus}"></div>
            </div>
          </div>
          
          <!-- Apelaciones Pendientes -->
          <div class="stat-item">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                <path d="M13 8H7"></path>
                <path d="M17 12H7"></path>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-label">APELACIONES PENDIENTES</span>
              <span class="stat-value">{{ stats.pendingAppeals || 0 }}</span>
            </div>
          </div>
          
          <!-- Auditorías Recientes -->
          <div class="stat-item">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-label">[REDACTED]</span>
              <span class="stat-value">-</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Grid de Funciones de Moderación -->
      <div class="moderation-grid">
        <!-- Tarjeta 1: Permission Management -->
        <div class="moderation-card" :class="{ 'active': activeCard === 1 }" @click="activateCard(1)">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                <path d="M12 8v4"></path>
                <path d="M12 16h.01"></path>
              </svg>
            </div>
            <div class="card-title">PERMISSION MANAGEMENT</div>
            <div class="card-status" v-if="hasPermission('full_moderation_control')">
              <span class="status-active">ACCESO CONCEDIDO</span>
            </div>
          </div>
          <div class="card-content">
            <p class="card-description">Gestiona permisos de usuario, asigna roles de moderación y controla niveles de acceso.</p>
            <div class="card-meta">
              <span class="meta-label">PERMISO REQUERIDO:</span>
              <span class="meta-value" :class="hasPermission('full_moderation_control') ? 'authorized' : 'denied'">
                {{ hasPermission('full_moderation_control') ? 'Control Moderación Total' : 'INSUFICIENTE' }}
              </span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button 
                class="action-button" 
                @click.stop="goToPermissionManagement"
                :disabled="!hasPermission('full_moderation_control')"
                :class="{ 'disabled': !hasPermission('full_moderation_control') }"
              >
                <span class="button-text">ACCEDER AL SISTEMA</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 2: Moderation Dashboard -->
        <div class="moderation-card" :class="{ 'active': activeCard === 2 }" @click="activateCard(2)">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="3" y1="9" x2="21" y2="9"></line>
                <line x1="9" y1="21" x2="9" y2="9"></line>
              </svg>
            </div>
            <div class="card-title">MODERATION DASHBOARD</div>
            <div class="card-status" v-if="hasPermission('access_moderation_dashboard')">
              <span class="status-active">ACCESO CONCEDIDO</span>
            </div>
          </div>
          <div class="card-content">
            <p class="card-description">Vista general de moderación con estadísticas, seguimiento de usuarios y monitoreo del sistema.</p>
            <div class="card-meta">
              <span class="meta-label">PERMISO REQUERIDO:</span>
              <span class="meta-value" :class="hasPermission('access_moderation_dashboard') ? 'authorized' : 'denied'">
                {{ hasPermission('access_moderation_dashboard') ? 'Acceso al Dashboard de Moderación' : 'INSUFICIENTE' }}
              </span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button 
                class="action-button" 
                @click.stop="goToGlobalModeration"
                :disabled="!hasPermission('access_moderation_dashboard')"
                :class="{ 'disabled': !hasPermission('access_moderation_dashboard') }"
              >
                <span class="button-text">ACCEDER AL SISTEMA</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 3: Audit Logs -->
        <div class="moderation-card" :class="{ 'active': activeCard === 3 }" @click="activateCard(3)">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
              </svg>
            </div>
            <div class="card-title">AUDIT LOGS</div>
            <div class="card-status" v-if="hasPermission('full_moderation_control')">
              <span class="status-active">ACCESO CONCEDIDO</span>
            </div>
          </div>
          <div class="card-content">
            <p class="card-description">Registro completo de auditoría de todas las acciones de moderación, modificaciones y cambios del sistema.</p>
            <div class="card-meta">
              <span class="meta-label">PERMISO REQUERIDO:</span>
              <span class="meta-value" :class="hasPermission('full_moderation_control') ? 'authorized' : 'denied'">
                {{ hasPermission('full_moderation_control') ? 'Control Moderación Total' : 'INSUFICIENTE' }}
              </span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button 
                class="action-button" 
                @click.stop="goToAuditLogs"
                :disabled="!hasPermission('full_moderation_control')"
                :class="{ 'disabled': !hasPermission('full_moderation_control') }"
              >
                <span class="button-text">ACCEDER AL SISTEMA</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 4: SSU Management -->
        <div class="moderation-card" :class="{ 'active': activeCard === 4 }" @click="activateCard(4)">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="card-title">SSU MANAGEMENT</div>
            <div class="card-status" v-if="hasPermission('change_ssu_status')">
              <span class="status-active">ACCESO CONCEDIDO</span>
            </div>
          </div>
          <div class="card-content">
            <p class="card-description">Gestionar el estado del Servidor (SSU).</p>
            <div class="card-meta">
              <span class="meta-label">PERMISO REQUERIDO:</span>
              <span class="meta-value" :class="hasPermission('change_ssu_status') ? 'authorized' : 'denied'">
                {{ hasPermission('change_ssu_status') ? 'Cambiar Estado SSU' : 'INSUFICIENTE' }}
              </span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button 
                class="action-button" 
                @click.stop="goToSSUManagement"
                :disabled="!hasPermission('change_ssu_status')"
                :class="{ 'disabled': !hasPermission('change_ssu_status') }"
              >
                <span class="button-text">ACCEDER AL SISTEMA</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 5: Facciones -->
        <div class="moderation-card" :class="{ 'active': activeCard === 5 }" @click="activateCard(5)">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="card-title">ADMINISTRACIÓN DE FACCIONES</div>
            <div class="card-status" v-if="hasPermission('moderate_factions_full')">
              <span class="status-active">ACCESO CONCEDIDO</span>
            </div>
          </div>
          <div class="card-content">
            <p class="card-description">Gestiona las facciones del Sitio, crea nuevas organizaciones y modifica las existentes.</p>
            <div class="card-meta">
              <span class="meta-label">PERMISO REQUERIDO:</span>
              <span class="meta-value" :class="hasPermission('moderate_factions_full') ? 'authorized' : 'denied'">
                {{ hasPermission('moderate_factions_full') ? 'Moderación de Facciones' : 'INSUFICIENTE' }}
              </span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button class="action-button" @click.stop="goToFactionsAdmin" :disabled="!hasPermission('moderate_factions_full')" :class="{ 'disabled': !hasPermission('moderate_factions_full') }">
                <span class="button-text">ACCEDER AL SISTEMA</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 6: Tarjetas -->
        <div class="moderation-card" :class="{ 'active': activeCard === 6 }" @click="activateCard(6)">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </div>
            <div class="card-title">TARJETAS DE ACCESO</div>
            <div class="card-status" v-if="hasPermission('moderate_factions_full')">
              <span class="status-active">ACCESO CONCEDIDO</span>
            </div>
          </div>
          <div class="card-content">
            <p class="card-description">Gestiona las tarjetas de acceso y los niveles de clearance del Sitio.</p>
            <div class="card-meta">
              <span class="meta-label">PERMISO REQUERIDO:</span>
              <span class="meta-value" :class="hasPermission('moderate_factions_full') ? 'authorized' : 'denied'">
                {{ hasPermission('moderate_factions_full') ? 'Moderación de Facciones' : 'INSUFICIENTE' }}
              </span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button class="action-button" @click.stop="goToCardsAdmin" :disabled="!hasPermission('moderate_factions_full')" :class="{ 'disabled': !hasPermission('moderate_factions_full') }">
                <span class="button-text">ACCEDER AL SISTEMA</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 7: Búsqueda de personal (spec §1.4 / §6) -->
        <div class="moderation-card" :class="{ 'active': activeCard === 7 }" @click="activateCard(7)">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="7"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </div>
            <div class="card-title">BÚSQUEDA DE PERSONAL</div>
            <div class="card-status" v-if="hasPermission('view_characters_basic')">
              <span class="status-active">ACCESO CONCEDIDO</span>
            </div>
          </div>
          <div class="card-content">
            <p class="card-description">Consulta personajes por Roblox Username, User ID o Codename: tarjeta, facción, rango y SCP asignado. Solo lectura.</p>
            <div class="card-meta">
              <span class="meta-label">PERMISO REQUERIDO:</span>
              <span class="meta-value" :class="hasPermission('view_characters_basic') ? 'authorized' : 'denied'">
                {{ hasPermission('view_characters_basic') ? 'Consulta de Personajes' : 'INSUFICIENTE' }}
              </span>
            </div>
          </div>
          <div class="card-footer">
            <div class="card-action">
              <button class="action-button" @click.stop="goToCharacterSearch" :disabled="!hasPermission('view_characters_basic')" :class="{ 'disabled': !hasPermission('view_characters_basic') }">
                <span class="button-text">ACCEDER AL SISTEMA</span>
                <div class="button-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Tarjeta 8: [REDACTED] -->
        <div class="moderation-card redacted" :class="{ 'active': activeCard === 9 }" @click="showAccessDenied(9)">
          <div class="card-header redacted">
            <div class="card-icon redacted">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M4.93 4.93l14.14 14.14"></path>
              </svg>
            </div>
            <div class="card-title redacted-text">[REDACTED]</div>
            <div class="card-status">
              <span class="status-redacted">CLASIFICADO</span>
            </div>
          </div>
          <div class="card-content redacted">
            <p class="card-description redacted-text">Esta función requiere autorización de nivel 5 y autorización administrativa.</p>
            <div class="card-meta">
              <span class="meta-label">AUTORIZACIÓN:</span>
              <span class="meta-value redacted">NIVEL 5+</span>
            </div>
          </div>
          <div class="card-footer redacted">
            <div class="clearance-warning">
              <div class="warning-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#aa2222" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
              </div>
              <span class="warning-text">SE REQUIERE AUTORIZACIÓN ADMINISTRATIVA</span>
            </div>
          </div>
        </div>

        <!-- Tarjeta 6: [REDACTED] -->
        <div class="moderation-card redacted" :class="{ 'active': activeCard === 10 }" @click="showAccessDenied(10)">
          <div class="card-header redacted">
            <div class="card-icon redacted">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M4.93 4.93l14.14 14.14"></path>
              </svg>
            </div>
            <div class="card-title redacted-text">[REDACTED]</div>
            <div class="card-status">
              <span class="status-redacted">CLASIFICADO</span>
            </div>
          </div>
          <div class="card-content redacted">
            <p class="card-description redacted-text">Esta función requiere autorización de nivel 5 y autorización administrativa.</p>
            <div class="card-meta">
              <span class="meta-label">AUTORIZACIÓN:</span>
              <span class="meta-value redacted">NIVEL 5+</span>
            </div>
          </div>
          <div class="card-footer redacted">
            <div class="clearance-warning">
              <div class="warning-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#aa2222" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
              </div>
              <span class="warning-text">SE REQUIERE AUTORIZACIÓN ADMINISTRATIVA</span>
            </div>
          </div>
        </div>

        <!-- Tarjeta 7: [REDACTED] -->
        <div class="moderation-card redacted" :class="{ 'active': activeCard === 7 }" @click="showAccessDenied(7)">
          <div class="card-header redacted">
            <div class="card-icon redacted">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M4.93 4.93l14.14 14.14"></path>
              </svg>
            </div>
            <div class="card-title redacted-text">[REDACTED]</div>
            <div class="card-status">
              <span class="status-redacted">CLASIFICADO</span>
            </div>
          </div>
          <div class="card-content redacted">
            <p class="card-description redacted-text">Esta función requiere autorización de nivel 5 y autorización administrativa.</p>
            <div class="card-meta">
              <span class="meta-label">AUTORIZACIÓN:</span>
              <span class="meta-value redacted">NIVEL 5+</span>
            </div>
          </div>
          <div class="card-footer redacted">
            <div class="clearance-warning">
              <div class="warning-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#aa2222" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
              </div>
              <span class="warning-text">SE REQUIERE AUTORIZACIÓN ADMINISTRATIVA</span>
            </div>
          </div>
        </div>

        <!-- Tarjeta 8: [REDACTED] -->
        <div class="moderation-card redacted" :class="{ 'active': activeCard === 8 }" @click="showAccessDenied(8)">
          <div class="card-header redacted">
            <div class="card-icon redacted">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M4.93 4.93l14.14 14.14"></path>
              </svg>
            </div>
            <div class="card-title redacted-text">[REDACTED]</div>
            <div class="card-status">
              <span class="status-redacted">CLASIFICADO</span>
            </div>
          </div>
          <div class="card-content redacted">
            <p class="card-description redacted-text">Esta función requiere autorización de nivel 5 y autorización administrativa.</p>
            <div class="card-meta">
              <span class="meta-label">AUTORIZACIÓN:</span>
              <span class="meta-value redacted">NIVEL 5+</span>
            </div>
          </div>
          <div class="card-footer redacted">
            <div class="clearance-warning">
              <div class="warning-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="#aa2222" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
              </div>
              <span class="warning-text">SE REQUIERE AUTORIZACIÓN ADMINISTRATIVA</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Información del Usuario -->
      <div class="user-info-panel">
        <div class="info-header">
          <h3 class="info-title">PERFIL DE MODERADOR</h3>
          <div class="info-subtitle">INFORMACIÓN DE SESIÓN ACTUAL</div>
        </div>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">ID DE MODERADOR:</span>
            <span class="info-value">{{ currentUser?.roblox_username || 'INVITADO' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">NIVEL DE AUTORIZACIÓN:</span>
            <span class="info-value">{{ getClearanceLevel() }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">PERMISOS:</span>
            <span class="info-value permissions">{{ getUserPermissions().length }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">ÁMBITOS:</span>
            <span class="info-value scopes">{{ getUserScopes().length }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">INICIO DE SESIÓN:</span>
            <span class="info-value">{{ sessionStartTime }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">DURACIÓN DE SESIÓN:</span>
            <span class="info-value">{{ sessionDuration }}</span>
          </div>
        </div>
        
        <!-- Permisos Detallados -->
        <div class="permissions-panel" v-if="getUserPermissions().length > 0">
          <h4 class="permissions-title">PERMISOS ACTIVOS</h4>
          <div class="permissions-grid">
            <span 
              v-for="(permission, index) in getUserPermissions()" 
              :key="index"
              class="permission-tag"
              :class="getPermissionType(permission)"
            >
              {{ getPermissionDisplay(permission) }}
            </span>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal de Acceso Denegado -->
    <div v-if="showDeniedModal" class="access-denied-modal">
      <div class="modal-overlay" @click="closeModal"></div>
      <div class="modal-content">
        <div class="modal-header">
          <div class="modal-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#aa2222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
          </div>
          <h3 class="modal-title">ACCESO RESTRINGIDO</h3>
        </div>
        <div class="modal-body">
          <p class="modal-text">No tienes los permisos requeridos para acceder a esta función.</p>
          <div class="clearance-info">
            <div class="clearance-item">
              <span class="clearance-label">AUTORIZACIÓN ACTUAL:</span>
              <span class="clearance-value">{{ getClearanceLevel() }}</span>
            </div>
            <div class="clearance-item">
              <span class="clearance-label">PERMISO REQUERIDO:</span>
              <span class="clearance-value denied">INSUFICIENTE</span>
            </div>
            <div class="clearance-item">
              <span class="clearance-label">ESTADO:</span>
              <span class="clearance-value denied">ACCESO DENEGADO</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="modal-button" @click="closeModal">
            <span class="button-text">ACEPTAR</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Estado principal
const activeCard = ref(1)
const currentUser = ref(null)
const currentTime = ref('')
const sessionStartTime = ref('')
const sessionDuration = ref('00:00:00')
const showDeniedModal = ref(false)
const ssuStatus = ref(false) // Añadido estado SSU
const stats = reactive({
  activeWarns: 0,
  activeBans: 0,
  pendingAppeals: 0,
  recentAudits: 0 // Cambiado de topWarnedUsers a recentAudits
})

// Permisos del usuario
const userPermissions = ref([])

// Scopes del usuario
const userScopes = ref([])

// Traducción de permisos
const permissionTranslations = {
  'create_warn': 'Crear Warn',
  'register_ban': 'Registrar Ban',
  'access_moderation_dashboard': 'Acceso al Dashboard de Moderación',
  'manage_warns': 'Gestionar Warns',
  'view_characters_basic': 'Ver Personajes Básico',
  'full_discord_moderation': 'Moderación Discord Completa',
  'full_moderation_control': 'Control Moderación Total',
  'change_ssu_status': 'Cambiar Estado SSU',
  'edit_rp_files_basic': 'Editar Archivos RP Básico',
  'edit_rp_files_full': 'Editar Archivos RP Completo',
  'moderate_factions_basic': 'Moderar Facciones Básico',
  'moderate_factions_full': 'Moderar Facciones Completo',
  'supervise_actors_basic': 'Supervisar Actores Básico',
  'supervise_actors_full': 'Supervisar Actores Completo'
}

// Computed
const userRole = computed(() => {
  if (!currentUser.value) return null
  if (currentUser.value.is_superuser) return 'ADMINISTRADOR'
  if (currentUser.value.is_staff) return 'MODERADOR'
  if (userPermissions.value.length > 0) return 'MODERADOR JUNIOR'
  return 'INVITADO'
})

// Métodos
const activateCard = (cardNumber) => {
  activeCard.value = cardNumber
  
  const requiredPermissions = {
    1: 'full_moderation_control',
    2: 'access_moderation_dashboard',
    3: 'full_moderation_control',
    4: 'change_ssu_status',
    5: 'admin_only',
    6: 'admin_only',
    7: 'admin_only',
    8: 'admin_only'
  }
  
  const required = requiredPermissions[cardNumber]
  if (required && !hasPermission(required) && cardNumber >= 5) {
    showAccessDenied(cardNumber)
  }
}

const showAccessDenied = (cardNumber) => {
  activeCard.value = cardNumber
  showDeniedModal.value = true
}

const closeModal = () => {
  showDeniedModal.value = false
  activeCard.value = 1
}

const hasPermission = (permission) => {
  if (!currentUser.value) return false
  if (currentUser.value.is_superuser) return true
  
  return userPermissions.value.includes(permission)
}

const getUserPermissions = () => {
  return userPermissions.value
}

const getUserScopes = () => {
  return userScopes.value
}

const getPermissionType = (permission) => {
  const adminPerms = ['full_moderation_control', 'manage_all_users', 'manage_permissions']
  const modPerms = ['access_moderation_dashboard', 'ban_users', 'warn_users']
  const staffPerms = ['register_ban', 'manage_appeals']
  
  if (adminPerms.includes(permission)) return 'admin'
  if (modPerms.includes(permission)) return 'moderator'
  if (staffPerms.includes(permission)) return 'staff'
  return 'basic'
}

const getPermissionDisplay = (permission) => {
  const displays = {
    'full_moderation_control': 'CONTROL TOTAL',
    'manage_all_users': 'GESTIONAR USUARIOS',
    'manage_permissions': 'GESTIONAR PERMISOS',
    'access_moderation_dashboard': 'ACCESO MODERACIÓN',
    'ban_users': 'BANEAR USUARIOS',
    'warn_users': 'ADVERTIR USUARIOS',
    'register_ban': 'REGISTRAR BANS',
    'manage_appeals': 'GESTIONAR APELACIONES'
  }
  return displays[permission] || permission.replace(/_/g, ' ').toUpperCase()
}

const getClearanceLevel = () => {
  if (!currentUser.value) return 'INVITADO'
  if (currentUser.value.is_superuser) return 'NIVEL 5'
  if (userScopes.value.some(s => s.scope === 'global')) return 'NIVEL 4'
  if (userPermissions.value.includes('full_moderation_control')) return 'NIVEL 3'
  if (userPermissions.value.includes('register_ban')) return 'NIVEL 2'
  if (userPermissions.value.length > 0) return 'NIVEL 1'
  return 'NIVEL 0'
}

const goToPermissionManagement = () => {
  if (hasPermission('full_moderation_control')) {
    router.push('/moderation/admin/permissions')
  } else {
    showAccessDenied(1)
  }
}

const goToGlobalModeration = () => {
  if (hasPermission('access_moderation_dashboard')) {
    router.push('/moderation/global')
  } else {
    showAccessDenied(2)
  }
}

const goToAuditLogs = () => {
  if (hasPermission('full_moderation_control')) {
    router.push('/moderation/audit')
  } else {
    showAccessDenied(3)
  }
}

const goToSSUManagement = () => {
  router.push('/moderation/ssu')
}

const goToFactionsAdmin = () => {
  router.push('/moderation/factions')
}

const goToCardsAdmin = () => {
  router.push('/moderation/cards')
}

const goToCharacterSearch = () => {
  if (hasPermission('view_characters_basic')) {
    router.push('/moderation/characters')
  } else {
    showAccessDenied(7)
  }
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
  
  // Actualizar duración de sesión
  if (sessionStartTime.value) {
    const start = new Date(sessionStartTime.value)
    const diff = now - start
    const hours = Math.floor(diff / 3600000)
    const minutes = Math.floor((diff % 3600000) / 60000)
    const seconds = Math.floor((diff % 60000) / 1000)
    sessionDuration.value = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  }
}

// Fetch datos
const fetchCurrentUser = async () => {
  try {
    const response = await fetch('/api/auth/user/')
    if (response.ok) {
      const data = await response.json()
      currentUser.value = data
      
      // Si el usuario está autenticado, inicializar sesión
      if (data.is_authenticated) {
        sessionStartTime.value = new Date().toISOString()
        fetchModerationStats()
        fetchUserPermissions()
        checkSSU()
      }
    }
  } catch (error) {
    console.error('Error obteniendo usuario:', error)
  }
}

const fetchModerationStats = async () => {
  try {
    const response = await fetch('/api/moderation/dashboard/')
    if (response.ok) {
      const data = await response.json()
      stats.activeWarns = data.stats?.active_warns || 0
      stats.activeBans = data.stats?.active_bans || 0
      stats.pendingAppeals = data.stats?.pending_appeals || 0
      stats.recentAudits = data.recent_audits?.length || 0
    }
  } catch (error) {
    console.error('Error obteniendo estadísticas de moderación:', error)
  }
}

const fetchUserPermissions = async () => {
  try {
    const response = await fetch('/api/auth/user/permissions/')
    if (response.ok) {
      const data = await response.json()
      userPermissions.value = data.permissions || []
      userScopes.value = data.scopes || []
    }
  } catch (error) {
    console.error('Error obteniendo permisos:', error)
  }
}

// Lifecycle
onMounted(() => {
  updateTime()
  const timeInterval = setInterval(updateTime, 1000)
  
  fetchCurrentUser()
  
  // Check SSU status every 15 seconds
  const ssuInterval = setInterval(checkSSU, 15000)
  
  return () => {
    clearInterval(timeInterval)
    clearInterval(ssuInterval)
  }
})
</script>

<style scoped>
/* Estilos base */
.moderacion-page {
  position: relative;
  min-height: 100vh;
  color: #d8d8d8;
  background: #0a0a0a;
  font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.5;
  overflow-x: hidden;
  padding: 20px;
  box-sizing: border-box;
}

/* Fondo SCP (mismo que otros componentes) */
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
.moderacion-header {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: rgba(15, 15, 15, 0.95);
  border: 1px solid #333;
  border-radius: 0px;
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-logo {
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
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  border-radius: 2px;
}

.header-icon svg {
  width: 24px;
  height: 24px;
  color: #ff3333;
}

.header-title {
  display: flex;
  flex-direction: column;
}

.header-main {
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: #ff3333;
  text-transform: uppercase;
  line-height: 1.2;
}

.header-sub {
  font-size: 0.7rem;
  letter-spacing: 0.5px;
  color: #888;
  text-transform: uppercase;
}

.header-right {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 16px;
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

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

/* Sección Principal */
.moderacion-main {
  position: relative;
  z-index: 2;
}

.moderacion-header-section {
  text-align: center;
  margin-bottom: 40px;
}

.moderacion-title {
  font-size: 2rem;
  font-weight: 900;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0 0 8px 0;
  text-shadow: 0 0 10px rgba(255, 51, 51, 0.3);
}

.moderacion-subtitle {
  font-size: 0.9rem;
  color: #aaa;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-bottom: 30px;
}

/* Estadísticas Rápidas - MODIFICADO */
.quick-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 30px;
}

.stat-item {
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #333;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.3s ease;
  position: relative;
}

.stat-item:hover {
  border-color: #444;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

/* Estilos específicos para SSU Status */
.stat-item.ssu-status.on {
  border-color: #00aa00;
  background: rgba(0, 40, 0, 0.3);
}

.stat-item.ssu-status.off {
  border-color: #aa0000;
  background: rgba(40, 0, 0, 0.3);
}

.stat-item.ssu-status .stat-icon {
  background: rgba(30, 30, 30, 0.8);
  border-color: #444;
}

.stat-item.ssu-status.on .stat-icon {
  background: rgba(0, 40, 0, 0.3);
  border-color: #00aa00;
}

.stat-item.ssu-status.off .stat-icon {
  background: rgba(40, 0, 0, 0.3);
  border-color: #aa0000;
}

.stat-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 20px;
  height: 20px;
  color: #ff3333;
}

.stat-info {
  flex: 1;
  position: relative;
}

.stat-label {
  display: block;
  font-size: 0.7rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
  margin-bottom: 4px;
}

.stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.5px;
}

/* Valores SSU específicos */
.stat-value.ssu-value.on {
  color: #00ff00;
  text-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
}

.stat-value.ssu-value.off {
  color: #ff3333;
  text-shadow: 0 0 10px rgba(255, 51, 51, 0.3);
}

/* Indicador de luz SSU */
.ssu-indicator-light {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #333;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.ssu-indicator-light.active {
  background: #00ff00;
  box-shadow: 0 0 6px #00ff00;
  animation: pulse 2s infinite;
}

/* Grid de Moderación */
.moderation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.moderation-card {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid #333;
  border-radius: 0px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  backdrop-filter: blur(5px);
}

.moderation-card:hover {
  transform: translateY(-2px);
  border-color: #444;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.moderation-card.active {
  border-color: #ff3333;
  background: rgba(40, 20, 20, 0.95);
  box-shadow: 0 0 20px rgba(255, 51, 51, 0.2);
}

.moderation-card.redacted {
  cursor: not-allowed;
  opacity: 0.8;
}

.moderation-card.redacted:hover {
  transform: none;
  border-color: #aa2222;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px;
  background: rgba(30, 30, 30, 0.8);
  border-bottom: 1px solid #333;
}

.card-header.redacted {
  background: rgba(40, 20, 20, 0.8);
  border-bottom-color: #aa2222;
}

.card-icon {
  width: 24px;
  height: 24px;
  color: #ff3333;
  flex-shrink: 0;
}

.card-icon.redacted {
  color: #aa2222;
}

.card-title {
  font-size: 1rem;
  font-weight: 700;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex: 1;
}

.card-title.redacted-text {
  color: #aa2222;
  font-family: 'Consolas', monospace;
}

.card-status {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.3px;
}

.status-active {
  color: #4CAF50;
  text-transform: uppercase;
}

.status-redacted {
  color: #aa2222;
  text-transform: uppercase;
}

.card-content {
  padding: 20px;
}

.card-description {
  font-size: 0.9rem;
  color: #aaa;
  line-height: 1.6;
  margin: 0 0 16px 0;
}

.card-description.redacted-text {
  color: #884444;
  font-style: italic;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.meta-label {
  font-size: 0.7rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.meta-value {
  font-size: 0.8rem;
  font-weight: 600;
  font-family: 'Consolas', monospace;
}

.meta-value.authorized {
  color: #4CAF50;
}

.meta-value.denied {
  color: #ff3333;
}

.meta-value.redacted {
  color: #aa2222;
}

.card-footer {
  padding: 0 20px 20px 20px;
}

.card-action {
  display: flex;
  justify-content: flex-end;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  border-radius: 0px;
  color: #ff3333;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-button:hover:not(.disabled) {
  background: rgba(255, 51, 51, 0.2);
  border-color: rgba(255, 51, 51, 0.5);
  transform: translateY(-1px);
}

.action-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(40, 40, 40, 0.6);
  border-color: #444;
  color: #888;
}

.button-icon {
  width: 14px;
  height: 14px;
  color: currentColor;
}

.clearance-warning {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  border-radius: 0px;
}

.warning-icon {
  width: 16px;
  height: 16px;
  color: #aa2222;
}

.warning-text {
  font-size: 0.7rem;
  color: #aa2222;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

/* Panel de Información del Usuario */
.user-info-panel {
  background: rgba(15, 15, 15, 0.95);
  border: 1px solid #333;
  border-radius: 0px;
  padding: 25px;
  backdrop-filter: blur(5px);
  margin-bottom: 30px;
}

.info-header {
  text-align: center;
  margin-bottom: 25px;
}

.info-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 8px 0;
}

.info-subtitle {
  font-size: 0.8rem;
  color: #888;
  letter-spacing: 0.3px;
  text-transform: uppercase;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 0.75rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.info-value {
  font-size: 0.85rem;
  font-weight: 600;
  color: #ddd;
  font-family: 'Consolas', monospace;
}

.info-value.permissions {
  color: #4CAF50;
}

.info-value.scopes {
  color: #2196F3;
}

/* Panel de Permisos */
.permissions-panel {
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  padding: 20px;
  margin-top: 20px;
}

.permissions-title {
  font-size: 0.9rem;
  color: #ff3333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 51, 51, 0.3);
}

.permissions-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.permission-tag {
  font-size: 0.7rem;
  padding: 4px 8px;
  border-radius: 2px;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  font-weight: 600;
}

.permission-tag.permission-full {
  background: rgba(255, 51, 51, 0.1);
  border: 1px solid rgba(255, 51, 51, 0.3);
  color: #ff3333;
}

.permission-tag.permission-manage {
  background: rgba(33, 150, 243, 0.1);
  border: 1px solid rgba(33, 150, 243, 0.3);
  color: #2196F3;
}

.permission-tag.permission-create {
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  color: #4CAF50;
}

.permission-tag.permission-view {
  background: rgba(255, 152, 0, 0.1);
  border: 1px solid rgba(255, 152, 0, 0.3);
  color: #FF9800;
}

.permission-tag.permission-basic {
  background: rgba(158, 158, 158, 0.1);
  border: 1px solid rgba(158, 158, 158, 0.3);
  color: #9E9E9E;
}

/* Modal de Acceso Denegado */
.access-denied-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
}

.modal-content {
  position: relative;
  background: rgba(15, 15, 15, 0.98);
  border: 1px solid #aa2222;
  border-radius: 0px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 10px 40px rgba(170, 34, 34, 0.3);
  animation: modalAppear 0.3s ease forwards;
}

@keyframes modalAppear {
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
  padding: 30px 30px 20px 30px;
  text-align: center;
  border-bottom: 1px solid #333;
}

.modal-icon {
  width: 50px;
  height: 50px;
  color: #aa2222;
  margin: 0 auto 15px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 900;
  color: #aa2222;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0;
}

.modal-body {
  padding: 30px;
}

.modal-text {
  font-size: 1rem;
  color: #d8d8d8;
  text-align: center;
  line-height: 1.6;
  margin: 0 0 30px 0;
}

.clearance-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
  background: rgba(40, 20, 20, 0.6);
  border: 1px solid rgba(170, 34, 34, 0.3);
  border-radius: 0px;
}

.clearance-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.clearance-item:last-child {
  border-bottom: none;
}

.clearance-label {
  font-size: 0.8rem;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.clearance-value {
  font-size: 0.9rem;
  font-weight: 700;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.5px;
}

.clearance-value.denied {
  color: #ff4444;
}

.modal-footer {
  padding: 20px 30px 30px 30px;
  text-align: center;
  border-top: 1px solid #333;
}

.modal-button {
  padding: 12px 30px;
  background: rgba(170, 34, 34, 0.1);
  border: 1px solid rgba(170, 34, 34, 0.3);
  border-radius: 0px;
  color: #aa2222;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 200px;
}

.modal-button:hover {
  background: rgba(170, 34, 34, 0.2);
  border-color: rgba(170, 34, 34, 0.5);
  transform: translateY(-1px);
}

.button-text {
  font-family: 'Consolas', monospace;
}

/* Responsive */
@media (max-width: 768px) {
  .moderation-grid {
    grid-template-columns: 1fr;
  }
  
  .moderacion-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .header-left {
    flex-direction: column;
    text-align: center;
  }
  
  .header-right {
    align-items: center;
  }
  
  .quick-stats {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .permissions-grid {
    justify-content: center;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .moderation-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1025px) {
  .moderation-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>