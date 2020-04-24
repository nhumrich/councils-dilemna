<template>
  <div class='game-lobby'>
    <h1>Welcome to the lobby for game: {{$route.params.game_id}} </h1>
    <div v-for='player in players' v-bind:key='player.id'  >
      <Player :player="player"></Player>
    </div>
  </div>
</template>

<script>
import { game$ } from '../../API.js'
import Player from './Player.vue'
export default {
  name: 'GameLobby',
  components: {
    Player
  },
  data: function () {
    return {
      players: [],
      game: {}
    }
  },
  mounted: function () {
    const game_id = this.$route.params.game_id
    this.gameSub = game$(game_id).subscribe(
      (results) => {
        if(results.players) {
          this.players = results.players
        }
        if (results.game) {
          this.game = results.game
        }
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
