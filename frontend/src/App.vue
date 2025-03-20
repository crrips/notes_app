<template>
  <div id="app">
    <header>
      <div class="header-content">
        <h1 class="app-title">Notes App 📝</h1>
        <nav class="app-nav">
          <router-link to="/" class="nav-link">Home 🏠</router-link>
          <router-link to="/analytics" class="nav-link">Analytics 📊</router-link>
        </nav>
      </div>
    </header>
    <!-- <main class="app-content"> -->
      <router-view />
    <!-- </main> -->
  </div>
</template>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background: linear-gradient(135deg, #a7125f 0%, #2575fc 100%);
  padding: 20px 300px;
  color: rgb(255, 255, 255);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.app-title {
  font-size: 2.5em;
  font-weight: 600;
  margin: 0;
  letter-spacing: 1px;
}

.app-nav {
  display: flex;
}

.nav-link {
  margin-left: 20px;
  color: white;
  text-decoration: none;
  font-size: 1.1em;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #e0e0e0;
}

.app-content {
  flex: 1;
  overflow-y: auto;
  padding: 30px;
  background: linear-gradient(to bottom, #3636ce, #ac1392);
}

a {
  text-decoration: none;
}
</style>