<script setup>
import Header from "./components/Header.vue"
import Footer from "./components/Footer.vue"
</script>

<template>
  <div id="app">
    <Header />

    <main class="main-content">
      <router-view />
    </main>

    <Footer />
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #0a0a0a;
  color: #d8d8d8;
  position: relative;
  width: 100vw;
  max-width: 100vw;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

.main-content {
  flex: 1;
  width: 100vw;
  max-width: 100vw;
  padding-top: 64px;
  position: relative;
}

/* Anular estilos del styles.css global */
:global(#app) {
  max-width: 100vw !important;
  margin: 0 !important;
  padding: 0 !important;
  text-align: left !important;
}
</style>

<style>
/* Estilos globales - se aplican a toda la aplicación */
html, body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background: #0a0a0a;
  overflow-x: hidden;
  width: 100vw;
  max-width: 100vw;
}

#app {
  width: 100vw !important;
  max-width: 100vw !important;
  margin: 0 !important;
  padding: 0 !important;
}

* {
  box-sizing: border-box;
}
</style>