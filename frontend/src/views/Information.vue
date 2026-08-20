<template>
  <div class="information-page">
    <!-- Fondo SCP -->
    <div class="site-background">
      <div class="grid-overlay"></div>
      <div class="scan-line"></div>
      <div class="particles"></div>
    </div>

    <!-- Header de la Página -->
    <div class="page-header">
      <div class="role-switch">
        <div class="switch-container">
          <button 
            class="switch-option" 
            :class="{ 'active': activeRole === 'on' }"
            @click="setActiveRole('on')"
          >
            <span class="switch-text">ON ROL</span>
            <div class="switch-indicator" v-if="activeRole === 'on'">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
          </button>
          <button 
            class="switch-option" 
            :class="{ 'active': activeRole === 'off' }"
            @click="setActiveRole('off')"
          >
            <span class="switch-text">OFF ROL</span>
            <div class="switch-indicator" v-if="activeRole === 'off'">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
          </button>
        </div>
        <div class="switch-label">
          <div class="status-indicator" :class="activeRole"></div>
          <span class="status-text">{{ activeRole === 'on' ? 'ROL ACTIVO' : 'ROL DESACTIVADO' }}</span>
        </div>
      </div>
    </div>

    <!-- Contenido Principal -->
    <main class="page-content">
      <!-- Contenido ON ROL -->
      <div v-if="activeRole === 'on'" class="on-role-content">
        <!-- Título Principal -->
        <div class="main-title-section">
          <h1 class="main-title">SITE 81: TWILIGHT</h1>
          <h2 class="main-subtitle">SCP Foundation Secure Facility Dossier</h2>
          <div class="title-decoration">
            <div class="decoration-line"></div>
            <div class="decoration-dot"></div>
            <div class="decoration-line"></div>
          </div>
        </div>

        <!-- Información General -->
        <div class="section-block">
          <h3 class="section-title">INFORMACIÓN GENERAL</h3>
          <div class="general-info">
            <!-- Texto de información -->
            <div class="info-text-container">
              <div class="scp-data-grid">
                <div class="data-item">
                  <span class="data-label highlight">Fundada:</span>
                  <span class="data-value">24 de abril de 2011</span>
                </div>
                <div class="data-item">
                  <span class="data-label highlight">Director fundador:</span>
                  <span class="data-value">Dr. Jean Karlyle Aktus</span>
                </div>
                <div class="data-item">
                  <span class="data-label highlight">Localización:</span>
                  <span class="data-value">Isla Cortes, archipiélago de las Islas Discovery, Columbia Británica, Canadá.</span>
                </div>
                <div class="data-item">
                  <span class="data-label highlight">Historia de cobertura:</span>
                  <span class="data-value">Comunidades poblacionales, Base militar canadiense, Estación de tratamiento de agua, Estación de electricidad</span>
                </div>
                <div class="data-item">
                  <span class="data-label highlight">Funciones de sitio:</span>
                  <span class="data-value">Investigación, contención, despliegue de destacamentos móviles, administración.</span>
                </div>
                <div class="data-item">
                  <span class="data-label highlight">Superficie:</span>
                  <span class="data-value">Área de 130 km².</span>
                </div>
                <div class="data-item">
                  <span class="data-label highlight">Composición:</span>
                  <span class="data-value">Cuatro instalaciones principales y cuatro zonas pobladas satélite, operando mayoritariamente en complejos subterráneos.</span>
                </div>
              </div>
            </div>
            
            <!-- Imagen -->
            <div class="info-image-container">
              <div class="image-container">
                <div class="cortes-island-map">
                  <img 
                    src="/Cortes-Island-Map.jpg" 
                    alt="Parte estructural de SCP-2955"
                    class="map-image"
                  />
                  <div class="image-overlay-text">
                    <span class="overlay-caption">Cortes Island</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Poblados - AHORA CON GRID 2x2 -->
        <div class="section-block">
          <h3 class="section-title">POBLADOS</h3>
          <div class="poblados-grid grid-2x2">
            <div 
              class="poblado-card" 
              :class="{ 'expanded': expandedPoblado === 'whaletown' || (hoveredPoblado === 'whaletown' && !isMobile) }"
              @mouseenter="hoverPoblado('whaletown')"
              @mouseleave="unhoverPoblado()"
              @click="togglePoblado('whaletown')"
            >
              <div class="poblado-header">
                <h4 class="poblado-title">WHALETOWN</h4>
                <div class="poblado-indicator">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </div>
              </div>
              <div class="poblado-content">
                <p class="poblado-text">Fachada como comunidad portuaria civil. Funciona como punto de entrada marítima controlada y monitoreo de tráfico naval.</p>
              </div>
            </div>

            <div 
              class="poblado-card" 
              :class="{ 'expanded': expandedPoblado === 'mansons' || (hoveredPoblado === 'mansons' && !isMobile) }"
              @mouseenter="hoverPoblado('mansons')"
              @mouseleave="unhoverPoblado()"
              @click="togglePoblado('mansons')"
            >
              <div class="poblado-header">
                <h4 class="poblado-title">MANSONS LANDING</h4>
                <div class="poblado-indicator">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </div>
              </div>
              <div class="poblado-content">
                <p class="poblado-text">Presentada como un centro turístico y cultural. En realidad, es el principal punto de llegada de suministros y personal encubierto. Única zona donde se permite estar al público civil, 4 veces al año.</p>
              </div>
            </div>

            <div 
              class="poblado-card" 
              :class="{ 'expanded': expandedPoblado === 'cortes' || (hoveredPoblado === 'cortes' && !isMobile) }"
              @mouseenter="hoverPoblado('cortes')"
              @mouseleave="unhoverPoblado()"
              @click="togglePoblado('cortes')"
            >
              <div class="poblado-header">
                <h4 class="poblado-title">CORTES BAY</h4>
                <div class="poblado-indicator">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </div>
              </div>
              <div class="poblado-content">
                <p class="poblado-text">Puerto secundario, utilizado por la Fundación para movimiento discreto de carga sensible. Funciona como sector habitacional para el personal.</p>
              </div>
            </div>

            <div 
              class="poblado-card" 
              :class="{ 'expanded': expandedPoblado === 'squirrel' || (hoveredPoblado === 'squirrel' && !isMobile) }"
              @mouseenter="hoverPoblado('squirrel')"
              @mouseleave="unhoverPoblado()"
              @click="togglePoblado('squirrel')"
            >
              <div class="poblado-header">
                <h4 class="poblado-title">SQUIRREL COVE</h4>
                <div class="poblado-indicator">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </div>
              </div>
              <div class="poblado-content">
                <p class="poblado-text">Poblado costero que sirve como sector habitacional completo para hospedar al personal.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Instalaciones Exteriores -->
        <div class="section-block">
          <h3 class="section-title">INSTALACIONES EXTERIORES</h3>
          <p class="installations-note">Estas son las únicas instalaciones que están por fuera de la tierra, funcionando como fachadas para el Sitio-81.</p>
          
          <div class="facilities-grid">
            <div class="facility-card" @click="openModal('power')">
              <div class="facility-header">
                <h4 class="facility-title">CORTES ISLAND POWER STATION PLANT</h4>
                <div class="facility-wing">Ala A</div>
              </div>
              <p class="facility-text">Planta eléctrica principal que alimenta toda el área del Sitio-81. <br><br><span class="data-label">Ver más</span></p>
            </div>

            <div class="facility-card" @click="openModal('water')">
              <div class="facility-header">
                <h4 class="facility-title">CORTES ISLAND WATER TREATMENT STATION</h4>
                <div class="facility-wing">Ala B</div>
              </div>
              <p class="facility-text">Estación de tratamiento de agua para los poblados satélite. <br><br><span class="data-label">Ver más</span></p>
            </div>

            <div class="facility-card" @click="openModal('military')">
              <div class="facility-header">
                <h4 class="facility-title">CORTES ISLAND MILITARY BASE</h4>
                <div class="facility-wing">Ala C</div>
              </div>
              <p class="facility-text">Base militar operada por personal de seguridad y Destacamentos Móviles. <br><br><span class="data-label">Ver más</span></p>
            </div>
          </div>
        </div>

        <!-- Modales para las instalaciones -->
        <div v-if="activeModal" class="modal-overlay" @click="closeModal">
          <div class="modal-content" @click.stop>
            <button class="modal-close" @click="closeModal">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
            
            <div v-if="activeModal === 'power'" class="modal-installation">
              <h3 class="modal-title">CORTES ISLAND POWER STATION PLANT</h3>
              <div class="modal-wing">Ala A</div>
              
              <div class="modal-description">
                <p>Planta de electricidad potenciada con generadores hidroeléctricos de un río subterráneo; alimenta de electricidad a toda el área del sitio-81, siendo los generadores primarios; no obstante, no alimenta a la instalación principal.</p>
                <p>Cuenta con la entrada principal (Gate A) a la instalación principal, tiene oficinas del Comité de Ética y la sede de la Agencia de Inteligencia en la región.</p>
              </div>
            </div>
            
            <div v-if="activeModal === 'water'" class="modal-installation">
              <h3 class="modal-title">CORTES ISLAND WATER TREATMENT STATION</h3>
              <div class="modal-wing">Ala B</div>
              
              <div class="modal-description">
                <p>Estación de tratamiento de agua que provee a los poblados satélite agua. Tiene oficinas administrativas y es la sede del Departamento de Clasificación y Contención.</p>
                <p>Cuenta con la entrada secundaria (Gate B) a la instalación principal del sitio.</p>
              </div>
            </div>
            
            <div v-if="activeModal === 'military'" class="modal-installation">
              <h3 class="modal-title">CORTES ISLAND MILITARY BASE</h3>
              <div class="modal-wing">Ala C</div>
              
              <div class="modal-description">
                <p>Base militar que es operada por el personal de seguridad y los operativos de los Destacamentos Móviles asignados al sitio.</p>
                <p>Cuenta con túneles subterráneos para acceder a la instalación principal por medio de la Ala F.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Instalación Principal -->
        <div class="section-block">
          <h3 class="section-title">INSTALACIÓN PRINCIPAL</h3>
          <div class="main-facility">
            <div class="office-section">
              <div class="office-card">
                <h4 class="office-title">OFICINAS PRINCIPALES</h4>
                <ul class="office-list">
                  <li class="office-item">
                    <div class="office-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                      </svg>
                    </div>
                    <span class="office-name">Administración</span>
                  </li>
                  <li class="office-item">
                    <div class="office-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                      </svg>
                    </div>
                    <span class="office-name">Comité de Clasificación</span>
                  </li>
                  <li class="office-item">
                    <div class="office-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                      </svg>
                    </div>
                    <span class="office-name">Comité de Ética</span>
                  </li>
                </ul>
              </div>
            </div>

            <div class="wings-section">
              <div class="wings-container">
                <div 
                  v-for="wing in wings" 
                  :key="wing.id"
                  class="wing-card"
                  :class="{ 'expanded': expandedWing === wing.id }"
                  @click="toggleWing(wing.id)"
                >
                  <div class="wing-header">
                    <div class="wing-name">{{ wing.name }}</div>
                    <div class="wing-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="6 9 12 15 18 9"></polyline>
                      </svg>
                    </div>
                  </div>
                  <div v-if="expandedWing === wing.id" class="wing-content">
                    <div class="wing-detail">
                      <span class="detail-label">Nombre:</span>
                      <span class="detail-value">{{ wing.fullName }}</span>
                    </div>
                    <div v-if="wing.subterranean" class="wing-detail">
                      <span class="detail-label subterranean">Subterráneo</span>
                    </div>
                    <div class="wing-detail">
                      <span class="detail-label">Función:</span>
                      <span class="detail-value">{{ wing.function }}</span>
                    </div>
                    <div class="wing-detail">
                      <span class="detail-label">Capacidad:</span>
                      <span class="detail-value">{{ wing.capacity }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- NUEVA SECCIÓN: Información del Personal -->
        <div class="section-block">
          <h3 class="section-title">INFORMACIÓN DEL PERSONAL</h3>
          <div class="personnel-info">
            <!-- Directores -->
            <div class="directors-grid">
              <div class="director-card">
                <h4 class="director-title">Director del Sitio</h4>
                <p class="director-name">Friedrich Eisenberg</p>
                <div class="director-badge">Alta Administración</div>
              </div>
              
              <div class="director-card">
                <h4 class="director-title">Subdirector del Sitio</h4>
                <p class="director-name">Bálint Kovács</p>
                <div class="director-badge">Alta Administración</div>
              </div>
              
              <div class="director-card">
                <h4 class="director-title">Director de Seguridad</h4>
                <p class="director-name">Agente Johann Müller</p>
                <div class="director-badge">Seguridad</div>
              </div>
              
              <div class="director-card">
                <h4 class="director-title">Director de Ética</h4>
                <p class="director-name">-</p>
                <div class="director-badge">Comité de Ética</div>
              </div>
              
              <div class="director-card">
                <h4 class="director-title">Director de Investigación</h4>
                <p class="director-name">Dr. Octavius Arendt</p>
                <div class="director-badge">Investigación</div>
              </div>
              
              <div class="director-card">
                <h4 class="director-title">Director de Destacamentos Móviles</h4>
                <p class="director-name">-</p>
                <div class="director-badge">Operaciones</div>
              </div>
            </div>

            <!-- Personal de Sitio -->
            <div class="staff-section">
              <h4 class="staff-title">Personal de Sitio</h4>
              <div class="staff-grid">
                <div class="staff-item">
                  <span class="staff-label">Jefes de Departamento:</span>
                  <span class="staff-value">8</span>
                </div>
                <div class="staff-item">
                  <span class="staff-label">Doctores:</span>
                  <span class="staff-value">65</span>
                </div>
                <div class="staff-item">
                  <span class="staff-label">Investigadores:</span>
                  <span class="staff-value">127</span>
                </div>
                <div class="staff-item">
                  <span class="staff-label">Personal Administrativo:</span>
                  <span class="staff-value">32</span>
                </div>
                <div class="staff-item">
                  <span class="staff-label">Personal de Mantenimiento y Limpieza:</span>
                  <span class="staff-value">56</span>
                </div>
                <div class="staff-item classified">
                  <span class="staff-label">Personal de Seguridad:</span>
                  <span class="staff-value">████</span>
                </div>
                <div class="staff-item">
                  <span class="staff-label">Clase-D:</span>
                  <span class="staff-value">541</span>
                </div>
                <div class="staff-item">
                  <span class="staff-label">Otro Personal:</span>
                  <span class="staff-value">19</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Información Adicional -->
        <div class="section-block">
          <h3 class="section-title">INFORMACIÓN ADICIONAL</h3>
          <div class="additional-info">
            <p class="info-paragraph">El Sitio-81 de la Fundación SCP es la sede principal del Comité de Clasificación y Contención; este comité tiene como objetivo verificar la clasificación de los objetos contenidos por la Fundación SCP, siendo ayudados por la Administración de Seguridad de Registros e Información (ASRI o RAISA). También tiene oficinas del Comité de Ética y puestos permanentes del DM E-6 "Tontos del Pueblo" en su interior. Se enfoca en el estudio de anomalías espacio-temporales, humanoides y objetos. Compuesta por 4 pueblos, 3 instalaciones y una instalación principal donde se ubican los laboratorios principales, las alas de contención y SCP-2955.</p>
            
            <p class="info-paragraph">Cortes Island ha sido, desde tiempos precoloniales, un punto focal de anomalías astronómicas y espacio-temporales. Los pueblos indígenas locales registraban en petroglifos "la luz que hiere al caer el sol", un fenómeno atmosférico conocido hoy como el "Resplandor Crepuscular" (Afterglow). Durante este resplandor, el tejido de la realidad se debilita, generando grietas dimensionales, distorsiones lumínicas y manifestaciones de entidades extradimensionales.</p>
            
            <p class="info-paragraph">Los registros más antiguos de la Fundación (finales del siglo XIX) muestran que al menos un Grupo de Interés extinto, el Círculo del Crepúsculo, excavó la isla en busca de una reliquia arqueológica: una estructura ciclópea subterránea con inscripciones en un lenguaje no humano. Sus investigaciones se centraban en manipular la energía emanada del Resplandor Crepuscular, convencidos de que era una "llave" hacia otros planos. El grupo colapsó tras varios experimentos fallidos, dejando la estructura olvidada. Se estima que este grupo lo conformaban almenos 20 individuos, para mas información leer GdI-1472.</p>
            
            <p class="info-paragraph">En una primera instancia, el primer acercamiento que tuvo la Fundación con la isla fue el descubrimiento de SCP-2955, en el año 1977. En este primer acercamiento, un grupo de operativos del DM Zeta-9 "Ratas Topo" habría descubierto el objeto mientras exploraban el sistema de cuevas de la isla debido a los numerosos reportes de civiles que señalaban muchos eventos anómalos a la hora del crepúsculo en el área del emplazamiento. Este grupo presenció directamente un evento relacionado con los efectos del SCP y fueron reducidos mientras trataban de salir del sistema de cuevas. Después de este incidente, la Fundación instaló un puesto de vigilancia en la isla para monitorear los efectos de la anomalía que fue designada como SCP-2955.</p>
            
            <p class="info-paragraph">En 2009, durante un eclipse parcial que coincidió con el Resplandor, la isla sufrió una brecha dimensional masiva cerca de la localidad de Whaletown. En cuestión de horas, más del 95% de la población pereció, los cuerpos de los habitantes fueron encontrados en estados de distorsión física o simplemente desaparecidos. Los pocos sobrevivientes fueron reubicados bajo amnésicos de Clase-B. Este evento, registrado internamente como Incidente Whaletown-1.</p>
            
            <p class="info-paragraph">Un grupo de investigación liderado por el Dr. Jean Karlyle Aktus fue enviado a la isla, fueron directamente a investigar a SCP-2955 como el posible causante de la brecha dimensional, dando como el causante de este incidente despues de unos meses. El descubrimiento confirmó que los fenómenos de la isla no eran meramente atmosféricos, sino un nodo de convergencia espacio-temporal por un objeto físico en la isla, siendo el SCP como causante de estos. La alta administración le dió la orden a Aktus que fundara un sitio de contención especializado en SCP-2955 desginandola como Sitio-81.</p>
          </div>

          <div class="mixed-section">
            <div class="mixed-content">
              <div class="mixed-text">
                <p>La Fundación decidió no solo instalar un sitio, sino transformar toda la isla en un enclave anómalo controlado, adquiriendo del gobierno canadiense toda la isla y sus poblados. Se invirtió en la construcción de la Cortes Island Water Treatment Station, la Cortes Island Power Station Plant y la Cortes Island Military Base, funcionando como fachadas para el sitio, con oficinas encubiertas y entradas hacia la instalación principal del sitio. Convirtiéndolo en el sitio seguro de la fundación más grande de la costa oeste del Pacífico.</p>
              </div>
              <div class="mixed-image">
                <div class="image-container">
                  <div class="cortes-island-map">
                    <img 
                      src="/scp-2995.jpg" 
                      alt="Parte estructural de SCP-2955"
                      class="map-image"
                    />
                    <div class="image-overlay-text">
                      <span class="overlay-caption">Parte estructural de SCP-2955</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="info-paragraph solo">
            <p>El sitio fue establecido y fundado el 24 de abril de 2011 por el director Dr. Jean Karlyle Aktus. Aktus se centró en los primeros años del sitio en investigar a SCP-2955 y descubrir su conexión con la isla. En ese tiempo, el sitio se había hecho específicamente para contener a SCP-2955 y vigilar sus efectos en la isla; sin embargo, esto cambió durante los años posteriores. El sitio se fue expandiendo con más alas y conteniendo a objetos y entidades anómalas que fueron capturadas cerca del sitio.</p>
          </div>

          <div class="mixed-section reversed">
            <div class="mixed-content">
              <div class="mixed-image">
                <div class="image-container">
                  <div class="cortes-island-map">
                    <img 
                      src="/entrada-electrica.jpg" 
                      alt="Entrada a la instalación principal en la Estación Eléctrica"
                      class="map-image"
                    />
                    <div class="image-overlay-text">
                      <span class="overlay-caption">Entrada a la instalación principal en la Estación Eléctrica</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="mixed-text">
                <p>El Director Aktus se retiró en el año 2017 dejando a Friedrich Eisenberg, su asistente y fiel amigo, en el cargo de Director de Sitio-81. El nuevo director expandió mucho más el sitio construyendo las Alas E, F y H, también ampliando el Ala C, destinando al sitio a una instalación administrativa regional de despliegue de destacamentos móviles sobre la costa del Pacífico. Hasta el día de hoy se sigue investigando activamente las anomalías espacio-temporales y magnéticas causadas por SCP-2955.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Contenido OFF ROL -->
      <div v-else class="off-role-content">
        <div class="off-role-container">
          <div class="off-role-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="#fc6f03" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line>
            </svg>
          </div>
          <h2 class="off-role-title">EXPLICACIÓN DEL SITIO OFF-RP</h2>
          
          <div class="off-role-intro">
            <p>En <strong>Site Twilight</strong> implementamos diversos sistemas diseñados para garantizar que el roleplay sea justo, inmersivo y entretenido para todos los participantes. Nuestra metodología se divide en dos modalidades principales:</p>
          </div>

          <div class="off-role-section">
            <div class="off-role-section-header">
              <div class="off-role-section-icon">📜</div>
              <h3 class="off-role-section-title">ROL SEMI-GUIONIZADO</h3>
            </div>
            <div class="off-role-section-content">
              <p>Esta modalidad combina la estructura de un guion predeterminado con la flexibilidad creativa de los participantes. <strong>El rol es parcialmente guionizado</strong> para dirigir la narrativa hacia puntos específicos, manteniendo la característica esencial de que los <strong>roleplayers puedan alterar la trama establecida</strong> si presentan razones narrativas sólidas y justificadas.</p>
              
              <div class="off-role-highlight">
                <p><strong>Proceso de aprobación:</strong> Cada borrador de trama y planificación de eventos se presenta a los directores de equipo antes de su implementación, requiriendo la <strong>aprobación unánime de los cuatro directores principales</strong> para proceder.</p>
              </div>
            </div>
          </div>

          <div class="off-role-section">
            <div class="off-role-section-header">
              <div class="off-role-section-icon">🎭</div>
              <h3 class="off-role-section-title">ROL SEMI-SERIO</h3>
            </div>
            <div class="off-role-section-content">
              <p>La modalidad predilecta para mantener la coherencia del universo SCP. Esta modalidad <strong>no permite la inclusión de elementos pertenecientes a franquicias de entretenimiento ajenas al universo SCP</strong>, como:</p>
              
              <div class="off-role-examples">
                <div class="off-role-example-item">• Warhammer 40K</div>
                <div class="off-role-example-item">• Five Nights at Freddy's</div>
                <div class="off-role-example-item">• Fortnite</div>
                <div class="off-role-example-item">• Otras franquicias similares</div>
              </div>
              
              <p>Tampoco se aceptan narrativas que desentonen con la estética del sitio o que carezcan de realismo contextual. <strong>Nota importante:</strong> Nos referimos específicamente a situaciones que violen flagrantemente la coherencia interna de la Fundación SCP, como la aparición injustificada de elementos cuyo único propósito sea obstaculizar la narrativa sin fundamento lógico.</p>
              
              <div class="off-role-note">
                <div class="note-icon">⚠️</div>
                <div class="note-text">Estos equipos mantienen autoridad total en sus áreas correspondientes, con la excepción extraordinaria de que el Subdirector o Director de la CMR puedan invalidar decisiones cuando lo consideren necesario.</div>
              </div>
            </div>
          </div>
          <div class="off-role-section">
            <div class="off-role-section-header">
              <div class="off-role-section-icon">🏛️</div>
              <h3 class="off-role-section-title">CENTRAL DE MODERACIÓN DE ROL (CMR)</h3>
            </div>
            <div class="off-role-section-content">
              <p>Twilight cuenta con un sistema integral de moderación compuesto por cinco equipos especializados que operan bajo la Central de Moderación de Rol:</p>
              
              <div class="off-role-teams-cmr">
                <!-- Fila superior: 3 tarjetas -->
                <div class="cmr-top-row">
                  <div class="off-role-team-card">
                    <div class="team-icon">📖</div>
                    <div class="team-info">
                      <h4 class="team-title">Equipo de Lore y Narración</h4>
                      <p class="team-description">Encargado del desarrollo y supervisión de la trama principal.</p>
                    </div>
                  </div>
                  
                  <div class="off-role-team-card">
                    <div class="team-icon">⚖️</div>
                    <div class="team-info">
                      <h4 class="team-title">Equipo de Moderación de Rol</h4>
                      <p class="team-description">Supervisa la calidad y coherencia del roleplay en general.</p>
                    </div>
                  </div>
                  
                  <div class="off-role-team-card">
                    <div class="team-icon">👥</div>
                    <div class="team-info">
                      <h4 class="team-title">Equipo de Moderación de Facciones</h4>
                      <p class="team-description">Regula y supervisa las interacciones entre diferentes facciones.</p>
                    </div>
                  </div>
                </div>
                
                <!-- Fila inferior: 2 tarjetas más anchas -->
                <div class="cmr-bottom-row">
                  <div class="off-role-team-card wide">
                    <div class="team-icon">🔍</div>
                    <div class="team-info">
                      <h4 class="team-title">Equipo de Supervisión de Actores</h4>
                      <p class="team-description">Monitorea el desempeño y coherencia de personajes y anomalías.</p>
                    </div>
                  </div>
                  
                  <div class="off-role-team-card wide">
                    <div class="team-icon">🎪</div>
                    <div class="team-info">
                      <h4 class="team-title">Equipo de Organización de Eventos</h4>
                      <p class="team-description">Planifica y coordina eventos especiales dentro del sitio.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="off-role-section">
            <div class="off-role-section-header">
              <div class="off-role-section-icon">🌟</div>
              <h3 class="off-role-section-title">PARTICIPACIÓN DE LOS ROLEPLAYERS</h3>
            </div>
            <div class="off-role-section-content">
              <p>En <strong>Site Twilight</strong>, cada participante tiene la oportunidad de convertirse en protagonista de las tramas si demuestra dedicación y se destaca dentro de la comunidad. Nuestro sistema permite una amplia gama de roles:</p>
              
              <div class="off-role-roles">
                <div class="off-role-role-column">
                  <div class="role-item">
                    <div class="role-icon">🛡️</div>
                    <span class="role-name">Guardia de Seguridad</span>
                  </div>
                  <div class="role-item">
                    <div class="role-icon">🔬</div>
                    <span class="role-name">Científico Investigador</span>
                  </div>
                  <div class="role-item">
                    <div class="role-icon">⚕️</div>
                    <span class="role-name">Médico del Sitio</span>
                  </div>
                  <div class="role-item">
                    <div class="role-icon">💼</div>
                    <span class="role-name">Administrador</span>
                  </div>
                </div>
                
                <div class="off-role-role-column">
                  <div class="role-item">
                    <div class="role-icon">🔫</div>
                    <span class="role-name">Combatiente Táctico</span>
                  </div>
                  <div class="role-item">
                    <div class="role-icon">👤</div>
                    <span class="role-name">Miembro de GOI Hostil</span>
                  </div>
                  <div class="role-item">
                    <div class="role-icon">🎭</div>
                    <span class="role-name">Agente Encubierto</span>
                  </div>
                  <div class="role-item">
                    <div class="role-icon">🔮</div>
                    <span class="role-name">Portador Anómalo</span>
                  </div>
                </div>
              </div>
              
              <div class="off-role-highlight final">
                <p><strong>La decisión recae en ti:</strong> Puedes elegir entre defender la normalidad como parte de la Fundación, o desafiar los límites de la realidad desde el otro lado. En Twilight, tu creatividad es el único límite.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const activeRole = ref('on')
const expandedWing = ref(null)
const expandedPoblado = ref(null)
const hoveredPoblado = ref(null)
const activeModal = ref(null)
const isMobile = ref(false)

const wings = ref([
  { id: 1, name: 'Ala A', fullName: 'Sector Administrativo-Científico', subterranean: false, function: 'Gestión y análisis científico', capacity: '120 agentes' },
  { id: 2, name: 'Ala B', fullName: 'Sector de Dirección y Servicios', subterranean: true, function: 'Dirección, ética y salud', capacity: '150 agentes' },
  { id: 3, name: 'Ala C', fullName: 'Sector de Alojamiento', subterranean: false, function: 'Residencia del Personal', capacity: '█████ agentes' },
  { id: 4, name: 'Ala D', fullName: 'Sector de Servicios Generales', subterranean: true, function: 'Servicios y tránsito interno', capacity: '320 agentes' },
  { id: 5, name: 'Ala E', fullName: 'Sector de █████████████', subterranean: false, function: 'Operaciones clasificadas', capacity: '█████ agentes' },
  { id: 6, name: 'Ala F', fullName: 'Sector de Seguridad', subterranean: true, function: 'Respuesta y control táctico', capacity: '████ agentes' },
  { id: 7, name: 'Ala G', fullName: 'Sector de Detención Clase-D', subterranean: false, function: 'Confinamiento personal Clase-D', capacity: '170 agentes' },
  { id: 8, name: 'Ala H', fullName: 'Sector de Contención Clase-Safe', subterranean: true, function: 'Contención', capacity: '250 agentes' },
  { id: 9, name: 'Ala I', fullName: 'Sector de Contención Clase-Euclid', subterranean: true, function: 'Contención', capacity: '███ agentes' },
  { id: 10, name: 'Ala J', fullName: 'Sector de Contención Clase-Keter', subterranean: true, function: 'Contención', capacity: '████ agentes' },
  { id: 11, name: 'Ala K', fullName: '█████ ██ SCP-████', subterranean: true, function: '██████ ██ █████-████', capacity: '████ agentes' }
])

const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

const setActiveRole = (role) => {
  activeRole.value = role
  expandedWing.value = null
  expandedPoblado.value = null
  hoveredPoblado.value = null
  activeModal.value = null
}

const toggleWing = (wingId) => {
  expandedWing.value = expandedWing.value === wingId ? null : wingId
}

const togglePoblado = (pobladoId) => {
  expandedPoblado.value = expandedPoblado.value === pobladoId ? null : pobladoId
}

const hoverPoblado = (pobladoId) => {
  if (!isMobile.value) {
    hoveredPoblado.value = pobladoId
  }
}

const unhoverPoblado = () => {
  if (!isMobile.value) {
    hoveredPoblado.value = null
  }
}

const openModal = (type) => {
  activeModal.value = type
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  activeModal.value = null
  document.body.style.overflow = 'auto'
}
</script>

<style scoped>
/* Estilos principales */
.information-page {
  position: relative;
  min-height: 100vh;
  color: #d8d8d8;
  background: #0a0a0a;
  overflow-x: hidden;
  font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.5;
  width: 100%;
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

/* Todos los párrafos con text-align: left */
.info-paragraph,
.poblado-text,
.facility-text,
.modal-description p,
.mixed-text p,
.off-role-text,
.installations-note,
.section-title,
.data-value {
  text-align: left !important;
}

/* Fondo SCP */
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
  background-size: 40px 40px;
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
  background-size: 30px 30px;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
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

/* Header de la Página */
.page-header {
  position: relative;
  z-index: 2;
  width: 100%;
  padding: 20px 16px;
  background: rgba(15, 15, 15, 0.9);
  border-bottom: 1px solid #333;
  backdrop-filter: blur(10px);
}

.role-switch {
  width: 100%;
  max-width: 100%;
}

.switch-container {
  display: flex;
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 12px;
  width: 100%;
}

.switch-option {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  background: transparent;
  border: none;
  color: #888;
  font-family: inherit;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.switch-option.active {
  background: rgba(252, 111, 3, 0.1);
  color: #fc6f03;
  border-bottom: 2px solid #fc6f03;
}

.switch-option:not(.active):hover {
  background: rgba(40, 40, 40, 0.6);
  color: #aaa;
}

.switch-indicator {
  width: 18px;
  height: 18px;
  color: #fc6f03;
}

.switch-text {
  font-weight: 700;
}

.switch-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  border-radius: 6px;
  width: 100%;
  box-sizing: border-box;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-indicator.on {
  background: #fc6f03;
  box-shadow: 0 0 8px #fc6f03;
  animation: pulse 2s infinite;
}

.status-indicator.off {
  background: #888;
  box-shadow: 0 0 8px #888;
}

.status-text {
  font-size: 14px;
  color: #aaa;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  font-weight: 600;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* Contenido Principal */
.page-content {
  position: relative;
  z-index: 1;
  width: 100%;
  padding: 24px 16px;
  box-sizing: border-box;
  max-width: 100%;
  overflow-x: hidden;
}

/* Título Principal */
.main-title-section {
  width: 100%;
  text-align: center;
  margin-bottom: 32px;
  padding: 20px 0;
  position: relative;
}

.main-title {
  font-size: 32px;
  font-weight: 900;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0 0 8px 0;
  text-shadow: 0 0 10px rgba(252, 111, 3, 0.3);
  line-height: 1.2;
}

.main-subtitle {
  font-size: 16px;
  font-weight: 500;
  color: #fff;
  letter-spacing: 0.5px;
  margin: 0;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
  opacity: 0.9;
}

.title-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
}

.decoration-line {
  width: 40px;
  height: 1px;
  background: linear-gradient(90deg, transparent, #fc6f03, transparent);
}

.decoration-dot {
  width: 6px;
  height: 6px;
  background: #fc6f03;
  border-radius: 50%;
  box-shadow: 0 0 8px #fc6f03;
}

/* Secciones */
.section-block {
  width: 100%;
  margin-bottom: 40px;
  position: relative;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 20px 0;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(252, 111, 3, 0.3);
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 60px;
  height: 2px;
  background: #fc6f03;
  box-shadow: 0 0 5px #fc6f03;
}

/* Información General */
.general-info {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
  align-items: stretch;
}

/* Contenedores con el mismo estilo */
.info-text-container,
.info-image-container {
  width: 100%;
  flex: 1;
}

/* Estilo compartido para ambos contenedores */
.info-text-container .scp-data-grid,
.info-image-container .image-container {
  background: rgba(25, 25, 25, 0.8);
  border: 1px solid #444;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 250px;
}

/* Estilos específicos para el texto */
.scp-data-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;
  box-sizing: border-box;
}

.data-item {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 20px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.data-item:last-child {
  border-bottom: none;
}

.data-label {
  font-size: 14px;
  font-weight: 600;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Consolas', monospace;
  min-width: 200px;
  width: 200px; 
  flex-shrink: 0; 
  text-align: right; 
  padding-right: 20px; 
}

.data-label.highlight {
  color: #fc6f03;
  text-shadow: 0 0 5px rgba(252, 111, 3, 0.3);
}

.data-value {
  font-size: 15px;
  color: #ddd;
  line-height: 1.4;
  text-align: left;
  flex: 1; 
  padding-left: 0; 
}

/* Estilos para la imagen */
.cortes-island-map {
  width: 100%;
  height: 100%;
  position: relative;
}

.map-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}

.image-overlay-text {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 16px;
  background: linear-gradient(
    to top,
    rgba(10, 10, 10, 0.9) 0%,
    rgba(10, 10, 10, 0.7) 50%,
    transparent 100%
  );
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 2;
}

.overlay-caption {
  font-size: 13px;
  color: #aaa;
  letter-spacing: 0.3px;
  flex: 1;
}

/* Poblados - GRID 2x2 */
.poblados-grid.grid-2x2 {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.poblado-card {
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  border-radius: 8px;
  padding: 16px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 60px;
}

/* IMPORTANTE: Solo la tarjeta hovereada cambia de altura */
.poblado-card:hover {
  background: rgba(40, 40, 40, 0.7);
  border-color: #555;
}

.poblado-card.expanded {
  background: rgba(35, 35, 35, 0.8);
  border-color: #fc6f03;
}

.poblado-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: #fc6f03;
  opacity: 0.8;
}

.poblado-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.poblado-title {
  font-size: 16px;
  font-weight: 700;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0;
}

.poblado-indicator {
  width: 20px;
  height: 20px;
  color: #fc6f03;
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.poblado-card.expanded .poblado-indicator {
  transform: rotate(180deg);
}

.poblado-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, margin-top 0.3s ease, opacity 0.3s ease;
  opacity: 0;
}

.poblado-card.expanded .poblado-content {
  max-height: 500px;
  margin-top: 16px;
  opacity: 1;
}

.poblado-text {
  font-size: 14px;
  color: #ccc;
  line-height: 1.5;
  margin: 0;
  text-align: left;
}

/* Nueva sección: Información del Personal */
.personnel-info {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.directors-grid {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.director-card {
  background: rgba(25, 25, 25, 0.8);
  border: 1px solid #444;
  border-radius: 8px;
  padding: 20px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.director-card:hover {
  transform: translateY(-2px);
  border-color: #fc6f03;
  box-shadow: 0 4px 12px rgba(252, 111, 3, 0.1);
}

.director-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: #fc6f03;
  opacity: 0.6;
}

.director-title {
  font-size: 14px;
  font-weight: 600;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin: 0 0 8px 0;
}

.director-name {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 12px 0;
  min-height: 24px;
}

.director-badge {
  display: inline-block;
  font-size: 12px;
  color: #fc6f03;
  background: rgba(252, 111, 3, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid rgba(252, 111, 3, 0.3);
  font-family: 'Consolas', monospace;
  letter-spacing: 0.3px;
}

.staff-section {
  background: rgba(25, 25, 25, 0.8);
  border: 1px solid #444;
  border-radius: 8px;
  padding: 24px;
  width: 100%;
}

.staff-title {
  font-size: 18px;
  font-weight: 700;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 20px 0;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(252, 111, 3, 0.3);
}

.staff-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.staff-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.staff-item:hover {
  background: rgba(50, 50, 50, 0.7);
  border-color: #555;
}

.staff-item.classified {
  background: rgba(50, 30, 30, 0.6);
  border-color: #aa2222;
}

.staff-item.classified:hover {
  background: rgba(60, 40, 40, 0.7);
}

.staff-label {
  font-size: 14px;
  color: #ccc;
  font-weight: 500;
}

.staff-value {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  font-family: 'Consolas', monospace;
}

/* Para móvil */
@media (max-width: 767px) {
  .data-item {
    flex-direction: column;
    gap: 8px;
  }
  
  .data-label {
    min-width: 100%;
    width: 100%;
    text-align: left;
    padding-right: 0;
  }
  
  .data-value {
    padding-left: 0;
  }
  
  .directors-grid {
    grid-template-columns: 1fr;
  }
  
  .staff-grid {
    grid-template-columns: 1fr;
  }
}

/* Para desktop - GRID 2x2 */
@media (min-width: 768px) {
  .poblados-grid.grid-2x2 {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .poblado-card {
    min-height: 60px;
    padding: 20px;
  }
  
  .poblado-content {
    display: block !important;
    max-height: 0;
    opacity: 0;
  }
  
  /* Solo para desktop: hover effect */
  .poblado-card:hover .poblado-content {
    max-height: 200px;
    margin-top: 16px;
    opacity: 1;
  }
  
  /* Ajustes para tablet */
  .data-label {
    min-width: 180px;
    width: 180px;
  }
  
  .directors-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Para desktop - GRID 2x2 mantiene 2 columnas */
@media (min-width: 1024px) {
  .poblados-grid.grid-2x2 {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
  
  .poblado-card {
    min-height: 60px;
    padding: 24px;
  }
  
  .poblado-title {
    font-size: 18px;
  }
  
  .poblado-text {
    font-size: 15px;
  }
  
  .data-label {
    min-width: 200px;
    width: 200px;
    font-size: 15px;
  }
  
  .data-value {
    font-size: 16px;
  }
  
  .directors-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
  
  .director-card {
    padding: 24px;
  }
  
  .director-title {
    font-size: 15px;
  }
  
  .director-name {
    font-size: 20px;
  }
  
  .staff-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }
  
  .staff-item {
    padding: 16px;
  }
  
  .staff-label {
    font-size: 15px;
  }
  
  .staff-value {
    font-size: 18px;
  }
}

/* Para pantallas grandes - GRID 2x2 mantiene 2 columnas */
@media (min-width: 1400px) {
  .poblados-grid.grid-2x2 {
    grid-template-columns: repeat(2, 1fr);
    gap: 32px;
  }
  
  .poblado-card {
    min-height: 60px;
    padding: 28px;
  }
  
  .poblado-title {
    font-size: 20px;
  }
  
  .poblado-text {
    font-size: 16px;
  }
}

/* Nota de instalaciones */
.installations-note {
  font-size: 14px;
  color: #aaa;
  margin: 0 0 20px 0;
  padding: 12px 16px;
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  border-radius: 6px;
  border-left: 4px solid #fc6f03;
}

/* Instalaciones */
.facilities-grid {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.facility-card {
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  border-radius: 8px;
  padding: 20px 16px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.facility-card:hover {
  background: rgba(40, 40, 40, 0.7);
  border-color: #555;
  transform: translateY(-2px);
}

.facility-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: #fc6f03;
  opacity: 0.8;
}

.facility-header {
  margin-bottom: 12px;
}

.facility-title {
  font-size: 17px;
  font-weight: 600;
  color: #fc6f03;
  margin: 0 0 4px 0;
  line-height: 1.3;
}

.facility-wing {
  font-size: 13px;
  color: #888;
  font-family: 'Consolas', monospace;
  letter-spacing: 0.3px;
}

.facility-text {
  font-size: 14px;
  color: #ccc;
  line-height: 1.5;
  margin: 0;
}

/* Modal para instalaciones */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: rgba(25, 25, 25, 0.95);
  border: 1px solid #fc6f03;
  border-radius: 8px;
  padding: 30px;
  max-width: 600px;
  width: 100%;
  position: relative;
  animation: slideUp 0.3s ease;
  max-height: 80vh;
  overflow-y: auto;
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(20px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: transparent;
  border: none;
  color: #aaa;
  cursor: pointer;
  padding: 5px;
  transition: color 0.3s ease;
}

.modal-close:hover {
  color: #fc6f03;
}

.modal-close svg {
  width: 20px;
  height: 20px;
}

.modal-installation {
  color: #ddd;
}

.modal-title {
  font-size: 24px;
  font-weight: 700;
  color: #fc6f03;
  margin: 0 0 10px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-wing {
  font-size: 16px;
  color: #888;
  font-family: 'Consolas', monospace;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(252, 111, 3, 0.3);
}

.modal-description {
  font-size: 16px;
  line-height: 1.6;
}

.modal-description p {
  margin: 0 0 15px 0;
}

.modal-description p:last-child {
  margin-bottom: 0;
}

/* Instalación Principal */
.main-facility {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.office-section {
  width: 100%;
}

.office-card {
  background: rgba(25, 25, 25, 0.8);
  border: 1px solid #444;
  border-radius: 8px;
  padding: 20px 16px;
  width: 100%;
  box-sizing: border-box;
}

.office-title {
  font-size: 18px;
  font-weight: 700;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 20px 0;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(252, 111, 3, 0.3);
}

.office-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.office-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.office-item:hover {
  background: rgba(50, 50, 50, 0.7);
  border-color: #555;
}

.office-icon {
  width: 20px;
  height: 20px;
  color: #fc6f03;
  flex-shrink: 0;
}

.office-name {
  font-size: 15px;
  color: #ddd;
  font-weight: 500;
}

.wings-section {
  width: 100%;
}

.wings-container {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.wing-card {
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  border-radius: 6px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.wing-card:hover {
  background: rgba(40, 40, 40, 0.7);
  border-color: #555;
  transform: translateY(-2px);
}

.wing-card.expanded {
  background: rgba(35, 35, 35, 0.8);
  border-color: #fc6f03;
  grid-column: 1 / -1;
}

.wing-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.wing-name {
  font-size: 16px;
  font-weight: 600;
  color: #ddd;
  font-family: 'Consolas', monospace;
}

.wing-icon {
  width: 20px;
  height: 20px;
  color: #fc6f03;
  transition: transform 0.3s ease;
}

.wing-card.expanded .wing-icon {
  transform: rotate(180deg);
}

.wing-content {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #444;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.wing-detail {
  display: flex;
  gap: 8px;
  font-size: 14px;
}

.detail-label {
  color: #888;
  font-weight: 500;
  min-width: 70px;
}

.detail-label.subterranean {
  color: #666;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  background: rgba(50, 50, 50, 0.6);
  padding: 2px 6px;
  border-radius: 3px;
  border: 1px solid #555;
}

.detail-value {
  color: #ccc;
  flex: 1;
}

/* Información Adicional */
.additional-info {
  width: 100%;
  margin-bottom: 32px;
}

.info-paragraph {
  font-size: 15px;
  color: #ccc;
  line-height: 1.6;
  margin: 0 0 20px 0;
}

.info-paragraph.solo {
  margin: 32px 0;
  padding: 20px;
  background: rgba(25, 25, 25, 0.6);
  border: 1px solid #444;
  border-radius: 8px;
  border-left: 4px solid #fc6f03;
}

.mixed-section {
  width: 100%;
  margin: 32px 0;
}

.mixed-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.mixed-section.reversed .mixed-content {
  flex-direction: column-reverse;
}

.mixed-text {
  width: 100%;
}

.mixed-text p {
  font-size: 15px;
  color: #ccc;
  line-height: 1.6;
  margin: 0;
}

.mixed-image {
  width: 100%;
}

/* Estilos específicos para OFF ROLE CONTENT */
.off-role-content {
  width: 100%;
  padding: 40px 0;
}

.off-role-container {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  text-align: left;
  padding: 40px 20px;
  background: rgba(25, 25, 25, 0.7);
  border: 1px solid #444;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
}

.off-role-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, transparent, #fc6f03, transparent);
}

.off-role-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  color: #fc6f03;
  opacity: 0.8;
}

.off-role-title {
  font-size: 28px;
  font-weight: 700;
  color: #fc6f03;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 32px 0;
  text-shadow: 0 0 10px rgba(252, 111, 3, 0.2);
  text-align: center;
}

.off-role-intro {
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(252, 111, 3, 0.2);
}

.off-role-intro p {
  font-size: 16px;
  color: #ccc;
  line-height: 1.6;
  margin: 0;
}

.off-role-intro strong {
  color: #fc6f03;
}

/* Secciones OFF ROLE */
.off-role-section {
  background: rgba(30, 30, 30, 0.6);
  border: 1px solid #444;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 30px;
  transition: all 0.3s ease;
}

.off-role-section:hover {
  border-color: #555;
  background: rgba(35, 35, 35, 0.7);
}

.off-role-section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(252, 111, 3, 0.2);
}

.off-role-section-icon {
  font-size: 28px;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(252, 111, 3, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(252, 111, 3, 0.3);
}

.off-role-section-title {
  font-size: 22px;
  font-weight: 700;
  color: #fc6f03;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.off-role-section-content p {
  font-size: 15px;
  color: #ccc;
  line-height: 1.6;
  margin: 0 0 16px 0;
}

.off-role-section-content p:last-child {
  margin-bottom: 0;
}

.off-role-highlight {
  background: rgba(252, 111, 3, 0.1);
  border-left: 4px solid #fc6f03;
  padding: 16px;
  margin: 20px 0;
  border-radius: 0 6px 6px 0;
}

.off-role-highlight p {
  font-size: 15px;
  color: #ddd;
  margin: 0;
}

.off-role-highlight.final {
  background: rgba(30, 60, 30, 0.2);
  border-left: 4px solid #4CAF50;
  margin-top: 30px;
}

.off-role-highlight.final p {
  color: #ddd;
  font-size: 16px;
}

/* Ejemplos */
.off-role-examples {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin: 20px 0;
  padding: 16px;
  background: rgba(40, 40, 40, 0.6);
  border-radius: 6px;
  border: 1px solid #444;
}

.off-role-example-item {
  font-size: 14px;
  color: #aaa;
  padding: 8px 12px;
  background: rgba(50, 50, 50, 0.6);
  border-radius: 4px;
  border: 1px solid #555;
}

/* Nota OFF ROLE */
.off-role-note {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin: 24px 0;
  padding: 20px;
  background: rgba(40, 30, 0, 0.2);
  border: 1px solid #aa8800;
  border-radius: 8px;
}

.off-role-note .note-icon {
  font-size: 20px;
  color: #ffcc00;
  flex-shrink: 0;
  margin-top: 2px;
}

.off-role-note .note-text {
  font-size: 15px;
  color: #ffdd88;
  line-height: 1.5;
  flex: 1;
}

/* Equipos OFF ROLE */
.off-role-teams {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin: 24px 0;
}

.off-role-team-card {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  transition: all 0.3s ease;
}

.off-role-team-card:hover {
  background: rgba(50, 50, 50, 0.7);
  border-color: #555;
  transform: translateY(-2px);
}

.team-icon {
  font-size: 20px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(252, 111, 3, 0.1);
  border-radius: 6px;
  border: 1px solid rgba(252, 111, 3, 0.3);
  flex-shrink: 0;
}

.team-info {
  flex: 1;
}

.team-title {
  font-size: 16px;
  font-weight: 600;
  color: #fc6f03;
  margin: 0 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.team-description {
  font-size: 14px;
  color: #aaa;
  line-height: 1.5;
  margin: 0;
}

/* Roles OFF ROLE */
.off-role-roles {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin: 24px 0;
}

.off-role-role-column {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.role-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.role-item:hover {
  background: rgba(50, 50, 50, 0.7);
  border-color: #555;
}

.role-icon {
  font-size: 18px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(252, 111, 3, 0.1);
  border-radius: 6px;
  border: 1px solid rgba(252, 111, 3, 0.3);
  flex-shrink: 0;
}

.role-name {
  font-size: 15px;
  color: #ddd;
  font-weight: 500;
}

/* Responsive - Tablet */
@media (min-width: 768px) {
  .page-header {
    padding: 24px 32px;
  }
  
  .page-content {
    padding: 32px;
  }
  
  .main-title {
    font-size: 40px;
  }
  
  .main-subtitle {
    font-size: 18px;
  }
  
  .section-title {
    font-size: 22px;
  }
  
  /* General info en fila para tablet */
  .general-info {
    flex-direction: row;
    align-items: stretch;
    gap: 32px;
  }
  
  /* Ajustar tamaño de contenedores */
  .info-text-container,
  .info-image-container {
    flex: 1;
  }
  
  .info-text-container .scp-data-grid,
  .info-image-container .image-container {
    min-height: 320px;
  }
  
  .scp-data-grid {
    padding: 24px;
  }
  
  .data-item {
    flex-direction: row;
    align-items: flex-start;
  }
  
  .data-label {
    min-width: 160px;
  }
  
  .data-value {
    flex: 1;
  }
  
  .image-overlay-text {
    padding: 14px 20px;
  }
  
  .overlay-caption {
    font-size: 14px;
  }
  
  /* Instalaciones */
  .facilities-grid {
    flex-direction: row;
    flex-wrap: wrap;
  }
  
  .facility-card {
    flex: 1;
    min-width: 200px;
  }
  
  /* Modal */
  .modal-content {
    padding: 40px;
  }
  
  .modal-title {
    font-size: 28px;
  }
  
  /* Otros ajustes responsive */
  .main-facility {
    flex-direction: row;
    gap: 32px;
  }
  
  .office-section {
    flex: 1;
  }
  
  .wings-section {
    flex: 2;
  }
  
  .wings-container {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .mixed-content {
    flex-direction: row;
    align-items: center;
    gap: 32px;
  }
  
  .mixed-section.reversed .mixed-content {
    flex-direction: row-reverse;
  }
  
  .mixed-text {
    flex: 1;
  }
  
  .mixed-image {
    flex: 1;
  }
  
  .off-role-container {
    padding: 60px 40px;
  }
  
  .off-role-title {
    font-size: 32px;
  }
  
  .off-role-teams {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .off-role-roles {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Responsive - Desktop */
@media (min-width: 1024px) {
  .page-header {
    padding: 28px 40px;
  }
  
  .page-content {
    padding: 40px;
    max-width: 1400px;
    margin: 0 auto;
  }
  
  .main-title {
    font-size: 48px;
  }
  
  .main-subtitle {
    font-size: 20px;
  }
  
  .section-title {
    font-size: 24px;
  }
  
  /* Ajustes para desktop */
  .info-text-container .scp-data-grid,
  .info-image-container .image-container {
    min-height: 350px;
  }
  
  .scp-data-grid {
    padding: 28px;
  }
  
  .image-overlay-text {
    padding: 16px 24px;
  }
  
  .overlay-caption {
    font-size: 15px;
  }
  
  /* Instalaciones */
  .installations-note {
    font-size: 15px;
    padding: 16px 20px;
  }
  
  .facility-title {
    font-size: 18px;
  }
  
  /* Modal desktop */
  .modal-content {
    max-width: 700px;
    padding: 50px;
  }
  
  .modal-title {
    font-size: 32px;
  }
  
  .modal-description {
    font-size: 17px;
  }
  
  /* Otros ajustes desktop */
  .office-card {
    padding: 24px 20px;
  }
  
  .office-title {
    font-size: 20px;
  }
  
  .office-item {
    padding: 14px 16px;
  }
  
  .wings-container {
    gap: 16px;
  }
  
  .wing-card {
    padding: 18px 16px;
  }
  
  .wing-content {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .info-paragraph {
    font-size: 16px;
  }
  
  .mixed-text p {
    font-size: 16px;
  }
  
  /* OFF ROLE desktop */
  .off-role-container {
    max-width: 1000px;
    padding: 60px 50px;
  }
  
  .off-role-section {
    padding: 30px;
  }
  
  .off-role-section-title {
    font-size: 24px;
  }
  
  .off-role-teams {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .off-role-examples {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Responsive - Pantallas grandes */
@media (min-width: 1400px) {
  .page-content {
    padding: 48px 60px;
  }
  
  .main-title {
    font-size: 56px;
  }
  
  .main-subtitle {
    font-size: 22px;
  }
  
  .section-block {
    margin-bottom: 60px;
  }
  
  /* Ajustes para pantallas grandes */
  .general-info {
    gap: 48px;
  }
  
  .info-text-container .scp-data-grid,
  .info-image-container .image-container {
    min-height: 380px;
  }
  
  .scp-data-grid {
    padding: 32px;
  }
  
  /* Instalaciones */
  .facilities-grid {
    gap: 32px;
  }
  
  .facility-card {
    padding: 28px 24px;
  }
  
  /* Modal pantallas grandes */
  .modal-content {
    max-width: 800px;
  }
  
  /* Otros ajustes */
  .main-facility {
    gap: 48px;
  }
  
  .wings-container {
    grid-template-columns: repeat(4, 1fr);
  }
  
  /* OFF ROLE pantallas grandes */
  .off-role-container {
    max-width: 1200px;
    padding: 70px 60px;
  }
  
  .off-role-title {
    font-size: 36px;
  }
  
  .off-role-section {
    padding: 35px;
  }
  
  .off-role-teams {
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
  }
  
  .off-role-roles {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }
}

/* Responsive para móviles - OFF ROLE */
@media (max-width: 767px) {
  .off-role-teams {
    grid-template-columns: 1fr;
  }
  
  .off-role-examples {
    grid-template-columns: 1fr;
  }
  
  .off-role-roles {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .off-role-section {
    padding: 20px;
  }
  
  .off-role-section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .off-role-section-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
  
  .off-role-section-title {
    font-size: 18px;
  }
  
  .team-icon {
    width: 36px;
    height: 36px;
    font-size: 18px;
  }
  
  .team-title {
    font-size: 15px;
  }
  
  .team-description {
    font-size: 13px;
  }
  
  .role-icon {
    width: 32px;
    height: 32px;
    font-size: 16px;
  }
  
  .role-name {
    font-size: 14px;
  }
}

/* ESTILOS PARA LA SECCIÓN CMR CORREGIDA */
.off-role-teams-cmr {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin: 24px 0;
}

/* Fila superior con 3 tarjetas */
.cmr-top-row {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Fila inferior con 2 tarjetas más anchas */
.cmr-bottom-row {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Estilo base para todas las tarjetas CMR */
.off-role-team-card {
  background: rgba(40, 40, 40, 0.6);
  border: 1px solid #444;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  transition: all 0.3s ease;
  width: 100%;
  box-sizing: border-box;
}

.off-role-team-card:hover {
  background: rgba(50, 50, 50, 0.7);
  border-color: #555;
  transform: translateY(-2px);
}

.team-icon {
  font-size: 20px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(252, 111, 3, 0.1);
  border-radius: 6px;
  border: 1px solid rgba(252, 111, 3, 0.3);
  flex-shrink: 0;
}

.team-info {
  flex: 1;
}

.team-title {
  font-size: 16px;
  font-weight: 600;
  color: #fc6f03;
  margin: 0 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.team-description {
  font-size: 14px;
  color: #aaa;
  line-height: 1.5;
  margin: 0;
}

/* Para tablet (768px+): 3 arriba, 2 abajo */
@media (min-width: 768px) {
  .off-role-teams-cmr {
    gap: 24px;
  }
  
  .cmr-top-row {
    flex-direction: row;
    gap: 20px;
  }
  
  .cmr-top-row .off-role-team-card {
    flex: 1; /* Cada tarjeta ocupa el mismo espacio */
  }
  
  .cmr-bottom-row {
    flex-direction: row;
    gap: 20px;
  }
  
  .cmr-bottom-row .off-role-team-card.wide {
    flex: 1; /* Las 2 tarjetas inferiores también iguales */
  }
}

/* Para móvil: todas en columna única */
@media (max-width: 767px) {
  .off-role-team-card {
    width: 100%;
  }
}
</style>