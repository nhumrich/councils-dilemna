<template>
  <div class='game-lobby'>
    <h1>Welcome to the lobby for game: {{$route.params.game_id}} </h1>
  </div>
</template>

<script>
import { createGame$ } from '../API.js'
export default {
  name: 'GameLobby',
  mounted: function () {
    const game_id = this.$route.params.game_id
    window.gameSource = createGame$(game_id)
    this.gameSource = window.gameSource
    this.gameSource.onmessage = function (event) {
      console.log('event', event)
    }
    this.gameSource.addEventListener(event, function (test) {
      console.log('test', test)
    })
    // this.gameSub$ = createGame$(game_id).subscribe(
    //   (game) => {
    //     console.log('game sub', game)
    //   },
    //   err => {
    //     console.error(err)
    //   }
    // )
  },
  beforeDestroy: function () {
    // this.gameSource.close()
  }
}
</script>
<style scoped>
</style>
