<template>
  <div class="create-game">
    <h1>Create a game</h1>
    <input placeholder='house name' v-model='playerName'>
    <button v-on:click="createGame">
      Create game
    </button>
    <h2>Join a game</h2>
    <input placeholder='house name' v-model='playerName'>
    <input placeholder='game number' v-model='gameNumber'>
    <button v-on:click="joinGame">
      Join Game
    </button>
  </div>
</template>

<script>
import { createGame, joinGame } from '../API.js'
export default {
  name: 'CreateGame',
  data: () => ({
    playerName: '',
    gameNumber: '',
  }),
  methods: {
    createGame: function () {
      console.log('createGame', this.playerName)
      createGame({userName: this.playerName}).then(r => {
        console.log('r', r)
      })
    },
    joinGame: function () {
      joinGame({userName: this.playerName, gameId: this.gameNumber}).then(r => {
        console.log('r', r)
      })

    }
  }
}

</script>
