<template>
  <div class="auth-page">
    <h1>Login / Signup</h1>

    <div class="auth-buttons">
      <a class="roblox-button" href="/accounts/login/roblox">
        Login with Roblox
      </a>
      <!-- Optional: local signup/login -->
      <a class="local-button" href="/accounts/signup">
        Sign Up
      </a>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.auth-page {
  max-width: 400px;
  margin: 5rem auto;
  text-align: center;
  color: #ddd;
}

.auth-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 2rem;
}

.roblox-button,
.local-button {
  display: block;
  padding: 1rem;
  border-radius: 4px;
  text-decoration: none;
  color: #fff;
  font-weight: bold;
  transition: 0.3s;
}

.roblox-button {
  background-color: #f00; /* Roblox red */
}

.roblox-button:hover {
  background-color: #c00;
}

.local-button {
  background-color: #444;
}

.local-button:hover {
  background-color: #666;
}
</style>
