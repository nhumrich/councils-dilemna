<template>
  <div class='set-up'>
    <h1>Welcome to Councils Delemna</h1>
    <div class='links'>
      <router-link :to="{name: 'create-game'}">Create a Game</router-link>
      <router-link :to="{name: 'join-game'}">Join a Game</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Setup'
}
</script>
<style scoped>
.links {
  margin: 0 40px;
  display: flex;
  justify-content: space-between;
}
</style>
