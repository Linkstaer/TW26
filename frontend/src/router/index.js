import { createRouter, createWebHistory } from "vue-router"
import Landing from "@/views/Landing.vue"
import Privacy from "@/views/Privacy.vue"
import TermsOfService from "@/views/TermsOfService.vue"
import LoginSignup from "@/views/LoginSignup.vue"
import Information from "@/views/Information.vue"
import Error_404 from "@/views/Error_404.vue"
import Dashboard from "@/views/Dashboard.vue"
import Personajes from "@/views/Personajes.vue"
import Perfil from "@/views/Perfil.vue"
import Moderacion from "@/views/Moderacion.vue"
import Moderacion_Global from "@/views/Moderacion_Global.vue"
import Adminpermissions from "@/views/Adminpermissions.vue"
import Appeals from "@/views/Appeals.vue"
import Moderacion_SSU from "@/views/Moderacion_SSU.vue"
import Audit_Logs from "@/views/Audit_Logs.vue"
import FaccionesDashboard from "@/views/FaccionesDashboard.vue"
import FactionLeaderPanel from "@/views/FactionLeaderPanel.vue"
import FactionAdminPanel from "@/views/ModerationFactions.vue"
import CardsAdminPanel from "@/views/ModerationCards.vue"
import ModerationCharacters from "@/views/ModerationCharacters.vue"
import NotificationsPanel from "@/views/NotificationsPanel.vue"
import SCPDatabase from "@/views/SCPDatabase.vue"
import Documentacion from "@/views/Documentacion.vue"
import Anuncios from "@/views/Anuncios.vue"
import TerminalAI from "@/views/TerminalAI.vue"
import LoreSuggestions from "@/views/LoreSuggestions.vue"


const routes = [
  { path: "/", name: "Landing", component: Landing },
  { path: "/privacy", name: "Privacy", component: Privacy },
  { path: "/terms-of-service", name: "TermsOfService", component: TermsOfService },
  {
    path: '/login',
    name: 'LoginSignup',
    component: LoginSignup,
  },
  {
    path: "/information",
    name: "Information",
    component: Information,
  },
  {
    path: "/404",
    name: "Error404",
    component: Error_404,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
  },
  {
    path: '/dashboard/personnel',
    name: 'personajes',
    component: Personajes,
    meta: {
      requiresAuth: true,
    }
  },
  {
    path: '/users/:id',  // :id capturará el roblox_id
    name: 'perfil',
    component: Perfil,
    meta: {
      requiresAuth: true,  // Solo usuarios autenticados pueden ver perfiles
    },
    props: true,  // Pasa los parámetros de ruta como props al componente
  },
  {
    path: '/moderation',
    name: 'Moderacion',
    component: Moderacion,
    meta: { 
      requiresAuth: true,
    }
  },
  {
    path: '/moderation/global',
    name: 'Moderacion_Global',
    component: Moderacion_Global,
    meta: { 
      requiresAuth: true,
      requiresModeration: true 
    }
  },
  {
    path: '/moderation/admin/permissions',
    name: 'AdminPermissions',
    component: Adminpermissions,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/appeals',
    name: 'Appeals',
    component: Appeals,
    meta: { requiresAuth: true }
  },
  {
    path: "/moderation/ssu",
    name: "Moderacion_SSU",
    component: Moderacion_SSU,
    meta: { requiresAuth: true },
  },
  {
    path: "/moderation/audit",
    name: "Audit_Logs",
    component: Audit_Logs,
    meta: { requiresAuth: true },
  },
  {
    path: "/moderation/factions",
    name: "ModerationFactions",
    component: FactionAdminPanel,
    meta: { requiresAuth: true, requiresModeration: true }
  },
  {
    path: "/moderation/cards",
    name: "ModerationCards",
    component: CardsAdminPanel,
    meta: { requiresAuth: true, requiresModeration: true }
  },
  {
    // Búsqueda de personal para moderación (spec §1.4 / §6)
    path: "/moderation/characters",
    name: "ModerationCharacters",
    component: ModerationCharacters,
    meta: { requiresAuth: true, requiresModeration: true }
  },
  {
    path: "/dashboard/factions",
    name: "FaccionesDashboard",
    component: FaccionesDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: "/dashboard/factions/manage/:id",
    name: "FactionLeaderPanel",
    component: FactionLeaderPanel,
    meta: { requiresAuth: true }
  },
  {
    path: "/dashboard/notifications",
    name: "NotificationsPanel",
    component: NotificationsPanel,
    meta: { requiresAuth: true }
  },
  {
    path: "/dashboard/scps",
    name: "SCPDatabase",
    component: SCPDatabase,
    meta: { requiresAuth: true }
  },
  {
    path: "/dashboard/documents",
    name: "Documentacion",
    component: Documentacion,
    meta: { requiresAuth: true }
  },
  {
    path: "/dashboard/announcements",
    name: "Anuncios",
    component: Anuncios,
    meta: { requiresAuth: true }
  },
  {
    path: "/dashboard/terminal",
    name: "TerminalAI",
    component: TerminalAI,
    meta: { requiresAuth: true }
  },
  {
    path: "/dashboard/lore-suggestions",
    name: "LoreSuggestions",
    component: LoreSuggestions,
    meta: { requiresAuth: true }
  },
  // IMPORTANTE: El catch-all debe ser la ÚLTIMA ruta
  {
    path: '/:pathMatch(.*)*',
    name: "NotFound",
    component: Error_404,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Interceptor de navegación para verificar autenticación
router.beforeEach(async (to, from, next) => {
  // Verificar si la ruta requiere autenticación
  if (to.meta.requiresAuth) {
    try {
      // Obtener usuario actual
      const response = await fetch('/api/auth/user/')
      const user = await response.json()
      
      if (!user.is_authenticated) {
        // Redirigir a login con parámetro de retorno
        return next({
          path: '/login',
          query: { redirect: to.fullPath }
        })
      }
      
      // Verificar si la ruta requiere permisos de moderación
      if (to.meta.requiresModeration) {
        const hasModerationAccess = await checkModerationAccess(user)
        if (!hasModerationAccess) {
          // Redirigir a dashboard o mostrar acceso denegado
          return next({ 
            path: '/dashboard',
            query: { error: 'access_denied' }
          })
        }
      }

      // Verificar si la ruta requiere ser superusuario
      if (to.meta.requiresSuperuser && !user.is_superuser) {
        return next({
          path: '/dashboard',
          query: { error: 'access_denied' }
        })
      }
      
      // Verificar permisos específicos si se requieren
      if (to.meta.requiresPermission) {
        const hasPermission = await checkUserPermission(user, to.meta.requiresPermission)
        if (!hasPermission) {
          // Redirigir con error de permisos
          return next({ 
            path: '/moderation',
            query: { error: 'insufficient_permissions' }
          })
        }
      }
      
      next()
    } catch (error) {
      console.error('Auth check error:', error)
      next('/login')
    }
  } else {
    next()
  }
})

// Función para verificar acceso a moderación
async function checkModerationAccess(user) {
  if (user.is_superuser || user.is_staff) {
    return true
  }
  
  try {
    // Verificar si el usuario tiene algún rol de moderación
    const response = await fetch('/api/auth/permissions/')
    const data = await response.json()
    
    // Verificar si tiene permisos de moderación
    const moderationPermissions = [
      'create_warn',
      'register_ban',
      'access_moderation_dashboard',
      'manage_warns',
      'view_characters_basic'
    ]
    
    return data.permissions?.some(perm => 
      moderationPermissions.includes(perm)
    ) || false
  } catch (error) {
    console.error('Permission check error:', error)
    return false
  }
}

// Función para verificar un permiso específico
async function checkUserPermission(user, permission) {
  if (user.is_superuser) {
    return true
  }
  
  try {
    const response = await fetch('/api/auth/permissions/')
    const data = await response.json()
    
    return data.permissions?.includes(permission) || false
  } catch (error) {
    console.error('Specific permission check error:', error)
    return false
  }
}

export default router
