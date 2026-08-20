[file name]: Privacy.vue
<template>
  <main class="privacy">
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
    </div>
    
    <div class="navigation">
      <button @click="goToHome" class="nav-button">
        <span class="button-icon">←</span>
        Volver al Inicio
      </button>
      <button @click="goToTerms" class="nav-button secondary">
        <span class="button-icon">⚖</span>
        Términos de Servicio
      </button>
    </div>
    
    <section class="container">
      <div class="document-header">
        <div class="classification-banner">
          <div class="classification-text">CLASIFICADO - NIVEL 3</div>
          <div class="classification-subtext">PROTOCOLO DE PRIVACIDAD DE SITE TWILIGHT</div>
        </div>
        
        <div class="title-section">
          <div class="document-code">DOCUMENTO REF: ST-PP-2025-01</div>
          <h1>POLÍTICA DE PRIVACIDAD</h1>
          <div class="document-line"></div>
          <p class="updated">Última actualización: {{ lastUpdated }}</p>
          <div class="security-clearance">ACCESO: TODO EL PERSONAL</div>
        </div>
      </div>

      <section class="document-section">
        <div class="section-header">
          <span class="section-number">1.</span>
          <h2>RESUMEN</h2>
        </div>
        <div class="section-content">
          <div class="text-card">
            <div class="text-content">
              <p>
                Site Twilight utiliza autenticación de Roblox para identificar usuarios.
                No admitimos registro manual ni cuentas basadas en contraseñas.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="document-section">
        <div class="section-header">
          <span class="section-number">2.</span>
          <h2>DATOS QUE RECOPILAMOS</h2>
        </div>
        <div class="section-content">
          <div class="card">
            <div class="terminal-list">
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">ID de usuario de Roblox</span>
              </div>
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">Nombre de usuario de Roblox</span>
              </div>
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">Identificadores internos de cuenta</span>
              </div>
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">Personajes y datos dentro del sitio que creas</span>
              </div>
            </div>
          </div>
          <div class="warning-card">
            <div class="warning-icon">!</div>
            <p class="warning-text">
              No recopilamos contraseñas, direcciones de correo electrónico, nombres reales o información de pago.
            </p>
          </div>
        </div>
      </section>

      <section class="document-section">
        <div class="section-header">
          <span class="section-number">3.</span>
          <h2>CÓMO USAMOS TUS DATOS</h2>
        </div>
        <div class="section-content">
          <div class="card">
            <div class="terminal-list">
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">Autenticar usuarios a través de Roblox</span>
              </div>
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">Crear y gestionar cuentas de usuario</span>
              </div>
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">Asociar personajes con cuentas</span>
              </div>
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">Hacer cumplir la moderación y reglas del sitio</span>
              </div>
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">Mantener la seguridad e integridad</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="document-section">
        <div class="section-header">
          <span class="section-number">4.</span>
          <h2>PERSONAJES Y CUENTAS</h2>
        </div>
        <div class="section-content">
          <div class="card">
            <div class="terminal-list">
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">Los usuarios pueden tener cero o más personajes</span>
              </div>
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">Los personajes siempre están vinculados a un usuario</span>
              </div>
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">Eliminar un personaje no elimina la cuenta</span>
              </div>
              <div class="terminal-item">
                <div class="terminal-marker"></div>
                <span class="terminal-text">Eliminar una cuenta elimina todos los personajes asociados</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="document-section">
        <div class="section-header">
          <span class="section-number">5.</span>
          <h2>COMPARTIR DATOS</h2>
        </div>
        <div class="section-content">
          <div class="text-card">
            <div class="text-content">
              <p>
                No vendemos, alquilamos ni compartimos tus datos con terceros,
                excepto cuando lo exija la ley, por motivos de seguridad,
                o para operar la autenticación de Roblox.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="document-section">
        <div class="section-header">
          <span class="section-number">6.</span>
          <h2>COOKIES Y SESIONES</h2>
        </div>
        <div class="section-content">
          <div class="text-card">
            <div class="text-content">
              <p>
                Usamos cookies de sesión únicamente para autenticación y seguridad.
                No se utilizan cookies de seguimiento o publicidad.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="document-section">
        <div class="section-header">
          <span class="section-number">7.</span>
          <h2>RETENCIÓN DE DATOS</h2>
        </div>
        <div class="section-content">
          <div class="text-card">
            <div class="text-content">
              <p>
                Los datos se retienen mientras tu cuenta exista.
                Puedes solicitar la eliminación; las copias de seguridad pueden persistir brevemente por razones de seguridad.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="document-section">
        <div class="section-header">
          <span class="section-number">8.</span>
          <h2>SEGURIDAD</h2>
        </div>
        <div class="section-content">
          <div class="text-card">
            <div class="text-content">
              <p>
                Utilizamos medidas de seguridad razonables como HTTPS y sesiones seguras.
                Ningún sistema puede garantizar seguridad absoluta.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="document-section">
        <div class="section-header">
          <span class="section-number">9.</span>
          <h2>PRIVACIDAD INFANTIL</h2>
        </div>
        <div class="section-content">
          <div class="text-card">
            <div class="text-content">
              <p>
                Este sitio se basa en la autenticación de Roblox.
                No recopilamos conscientemente datos personales adicionales de menores.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="document-section">
        <div class="section-header">
          <span class="section-number">10.</span>
          <h2>CAMBIO DE POLÍTICA</h2>
        </div>
        <div class="section-content">
          <div class="text-card">
            <div class="text-content">
              <p>
                Esta política puede ser actualizada.
                Los cambios se publicarán en esta página.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section class="document-section">
        <div class="section-header">
          <span class="section-number">11.</span>
          <h2>CONTACTO</h2>
        </div>
        <div class="section-content">
          <div class="contact-card">
            <div class="contact-icon">✉</div>
            <div class="contact-content">
              <p>
                Para solicitudes de privacidad o eliminación de datos, contacta a través de nuestro servidor de Discord:
              </p>
              <a :href="discordUrl" target="_blank" class="discord-link">
                <span class="discord-icon">#</span>
                {{ discordUrl }}
              </a>
            </div>
          </div>
        </div>
      </section>

      <div class="document-footer">
        <div class="footer-line"></div>
        <div class="footer-text">
          <span>FIN DEL DOCUMENTO</span>
          <span>CONFIDENCIAL - ACCESO NO AUTORIZADO PROHIBIDO</span>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const lastUpdated = "2025-01-01"
const discordUrl = "https://discord.gg/37BrVa6b8E"

const goToHome = () => {
  router.push('/')
}

const goToTerms = () => {
  router.push('/terms-of-service')
}
</script>

<style scoped>
.privacy {
  position: relative;
  min-height: 100vh;
  padding: 2rem 1rem;
  color: #d8d8d8;
  background: #0a0a0a;
  overflow-x: hidden;
  font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
}

.site-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
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
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(60, 60, 60, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(60, 60, 60, 0.1) 1px, transparent 1px);
  background-size: 60px 60px;
  animation: gridMove 20s linear infinite;
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 10% 20%, rgba(100, 100, 100, 0.05) 1px, transparent 1px),
    radial-gradient(circle at 90% 80%, rgba(100, 100, 100, 0.05) 1px, transparent 1px);
  background-size: 50px 50px;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(80, 80, 80, 0.8) 10%, 
    rgba(120, 120, 120, 0.9) 50%, 
    rgba(80, 80, 80, 0.8) 90%, 
    transparent 100%);
  animation: scan 8s linear infinite;
  z-index: 1;
  opacity: 0.3;
}

@keyframes scan {
  0% { top: 0%; }
  100% { top: 100%; }
}

@keyframes gridMove {
  0% { transform: translateY(0); }
  100% { transform: translateY(60px); }
}

.navigation {
  position: sticky;
  top: 1rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
  z-index: 100;
}

.nav-button {
  padding: 0.8rem 1.5rem;
  background: rgba(30, 30, 30, 0.9);
  border: 1px solid #444;
  color: #d8d8d8;
  font-family: inherit;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-radius: 2px;
}

.nav-button:hover {
  background: rgba(40, 40, 40, 0.95);
  border-color: #666;
  transform: translateY(-1px);
}

.nav-button.secondary {
  background: rgba(40, 40, 40, 0.8);
  border-color: #555;
}

.button-icon {
  font-size: 1.1rem;
  opacity: 0.8;
}

.container {
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  z-index: 1;
  background: rgba(15, 15, 15, 0.85);
  border: 1px solid #333;
  padding: 0 2rem 2rem;
  backdrop-filter: blur(5px);
}

.document-header {
  margin-bottom: 3rem;
  border-bottom: 1px solid #333;
  background: linear-gradient(to bottom, rgba(20, 20, 20, 0.9), rgba(15, 15, 15, 0.7));
}

.classification-banner {
  background: linear-gradient(90deg, #222, #333, #222);
  padding: 0.8rem;
  text-align: center;
  border-bottom: 1px solid #444;
}

.classification-text {
  font-size: 0.9rem;
  font-weight: bold;
  letter-spacing: 1px;
  color: #aaa;
  text-transform: uppercase;
}

.classification-subtext {
  font-size: 0.75rem;
  opacity: 0.7;
  margin-top: 0.3rem;
  color: #888;
}

.title-section {
  padding: 2rem 0;
  text-align: center;
}

.document-code {
  font-size: 0.85rem;
  color: #999;
  margin-bottom: 1rem;
  letter-spacing: 0.5px;
  font-family: 'Consolas', monospace;
}

h1 {
  font-size: 2.2rem;
  margin: 0.5rem 0;
  color: #ffffff;
  font-weight: 300;
  letter-spacing: 1px;
}

.document-line {
  height: 1px;
  background: linear-gradient(90deg, transparent, #555, transparent);
  margin: 1.5rem auto;
  width: 70%;
}

.updated {
  font-size: 0.9rem;
  color: #999;
  margin: 1rem 0;
}

.security-clearance {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  border: 1px solid #555;
  color: #aaa;
  font-size: 0.85rem;
  margin-top: 1rem;
  background: rgba(40, 40, 40, 0.5);
}

.document-section {
  margin-bottom: 2rem;
  padding-left: 0;
  position: relative;
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #333;
}

.section-number {
  font-size: 1.4rem;
  font-weight: bold;
  color: #bbb;
  margin-right: 0.8rem;
  min-width: 2rem;
}

h2 {
  font-size: 1.3rem;
  color: #e0e0e0;
  margin: 0;
  font-weight: 400;
}

.section-content {
  padding-left: 2.8rem;
}

/* Cards Styles */
.text-card, .card, .warning-card, .contact-card {
  background: rgba(25, 25, 25, 0.6);
  border: 1px solid #444;
  padding: 1.5rem;
  margin: 0 auto;
  max-width: 800px;
  border-radius: 4px;
}

.text-card {
  background: rgba(25, 25, 25, 0.6);
  border-left: 3px solid #555;
}

.card {
  background: rgba(20, 20, 20, 0.7);
  border-left: 3px solid #666;
}

.warning-card {
  background: rgba(40, 30, 0, 0.3);
  border-left: 3px solid #aa8800;
  margin-top: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.contact-card {
  background: rgba(35, 35, 35, 0.6);
  border-left: 3px solid #777;
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
}

.text-content {
  text-align: center;
}

.text-content p {
  color: #ccc;
  line-height: 1.6;
  margin: 0;
  text-align: center;
}

.warning-icon {
  color: #ffcc00;
  font-weight: bold;
  font-size: 1.2rem;
  margin-top: 0.2rem;
}

.warning-text {
  color: #ddd;
  line-height: 1.6;
  margin: 0;
  text-align: left;
  flex: 1;
}

.contact-icon {
  color: #aaa;
  font-size: 1.2rem;
  margin-top: 0.2rem;
}

.contact-content {
  flex: 1;
  text-align: center;
}

.contact-content p {
  color: #ccc;
  line-height: 1.6;
  margin-bottom: 1rem;
  text-align: center;
}

.terminal-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin: 0;
}

.terminal-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.8rem;
  background: rgba(30, 30, 30, 0.5);
  border-left: 2px solid #555;
  border-radius: 2px;
  text-align: left;
}

.terminal-marker {
  width: 8px;
  height: 8px;
  background: #888;
  border-radius: 50%;
  flex-shrink: 0;
}

.terminal-text {
  color: #ddd;
  line-height: 1.5;
  flex: 1;
}

.discord-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #7289da;
  text-decoration: none;
  padding: 0.8rem 1.2rem;
  background: rgba(114, 137, 218, 0.1);
  border: 1px solid rgba(114, 137, 218, 0.3);
  border-radius: 4px;
  transition: all 0.3s ease;
  text-align: center;
  justify-content: center;
  margin: 0 auto;
}

.discord-link:hover {
  background: rgba(114, 137, 218, 0.2);
  border-color: rgba(114, 137, 218, 0.5);
  transform: translateY(-1px);
}

.discord-icon {
  font-weight: bold;
}

.document-footer {
  margin-top: 3rem;
  padding-top: 2rem;
  text-align: center;
  border-top: 1px solid #333;
}

.footer-line {
  height: 1px;
  background: linear-gradient(90deg, transparent, #555, transparent);
  margin-bottom: 1.2rem;
}

.footer-text {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #777;
  letter-spacing: 0.5px;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem 1.5rem;
  }
  
  h1 {
    font-size: 1.8rem;
  }
  
  .section-content {
    padding-left: 0;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    padding-left: 0;
  }
  
  .navigation {
    flex-direction: column;
    align-items: center;
  }
  
  .nav-button {
    width: 100%;
    max-width: 300px;
    justify-content: center;
  }
  
  .footer-text {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .document-header {
    margin-bottom: 2rem;
  }
  
  .text-card, .card, .warning-card, .contact-card {
    padding: 1.2rem;
  }
  
  .terminal-item {
    padding: 0.6rem;
  }
}
</style>