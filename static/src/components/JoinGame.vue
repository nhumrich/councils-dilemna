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
      joinGame({userName: this.playerName, gameId: this.gameNumber}).then(r => {
        console.log('r', r)
      })
    }
  }
}

</script>
