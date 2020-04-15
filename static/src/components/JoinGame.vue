<template>
  <div class="join-game">
    <h2>Join a game</h2>
    <input placeholder='house name' v-model='playerName'>
    <input placeholder='game number' v-model='gameNumber'>
    <button v-on:click="joinGame">
      Join Game
    </button>
  </div>
</template>

<script>
import { joinGame } from '../API.js'
export default {
  name: 'JoinGame',
  data: () => ({
    playerName: '',
    gameNumber: '',
  }),
  methods: {
    joinGame: function () {
      const playerId = localStorage.getItem('player_id')
      joinGame({userName: this.playerName, gameId: this.gameNumber, playerId}).then(results => {
        const { game_id, user_id } = results
        localStorage.setItem('player_id', user_id)
        this.$router.push({name: 'game-lobby', params: {game_id}})
      })
    }
  }
}

</script>
