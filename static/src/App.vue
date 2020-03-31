<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <CreateGame />
    <HelloWorld msg='hi'/>
  </div>
</template>

<script>
import CreateGame from './components/CreateGame.vue'
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld,
    CreateGame
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
