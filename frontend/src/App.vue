<template>
  <div class="app">
    <aside class="sidebar">
      <nav>
        <ul>
          <li><router-link to="/dashboard">📊 Dashboard</router-link></li>
          <li><router-link to="/data-collection">📥 Data Collection</router-link></li>
          <li><router-link to="/whis">🧠 Whis</router-link></li>
          <li><router-link to="/agents">🧑‍💻 Agents</router-link></li>
          <li><router-link to="/digest">📒 Digest</router-link></li>
        </ul>
      </nav>
    </aside>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style>
.app {
  display: flex;
  height: 100vh;
}
.sidebar {
  width: 220px;
  background: #111;
  color: #fff;
  padding: 1rem;
}
.sidebar ul {
  list-style: none;
  padding: 0;
}
.sidebar li {
  margin: 1rem 0;
}
.sidebar a {
  color: #0ff;
  text-decoration: none;
}
.content {
  flex-grow: 1;
  padding: 2rem;
  background: #1a1a1a;
  color: #eee;
  overflow-y: auto;
}
</style> 