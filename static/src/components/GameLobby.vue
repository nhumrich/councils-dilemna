<template>
  <div class='game-lobby'>
    <h1>Welcome to the lobby for game: {{$route.params.game_id}} </h1>
  </div>
</template>

<script>
import { game$ } from '../API.js'
export default {
  name: 'GameLobby',
  mounted: function () {
    const game_id = this.$route.params.game_id
    this.gameSub = game$(game_id).subscribe(
      (e) => {
        console.log('sub', e)
      }
    )
  },
  beforeDestroy: function () {
    this.gameSub.unsubscribe()
  }
}
</script>
<style scoped>
</style>
