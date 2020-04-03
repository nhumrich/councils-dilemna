<template>
  <div class='game-lobby'>
    <h1>Welcome to the lobby for game: {{$route.params.game_id}} </h1>
  </div>
</template>

<script>
// import { createGame$ } from '../API.js'
export default {
  name: 'GameLobby',
  mounted: function () {
    const game_id = this.$route.params.game_id
    console.log('game_id', game_id)
    this.ws = new WebSocket(`ws://localhost:8000/ws/game/${game_id}`)
    this.ws.onmessage = function (event) {
      console.log('event', event)
    }
    // this.gameSub$ = createGame$(this.$route.params.game_id).subscribe(
    //   (game) => {
    //     console.log('game', game)
    //   },
    //   err => {
    //     console.err(err)
    //   }
    // )
  },
  beforeDestroy: function () {
    this.ws.close()
    // this.gameSub$.unsubscribe()
  }
}
</script>
<style scoped>
</style>
