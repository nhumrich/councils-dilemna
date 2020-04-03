<template>
  <div class="create-game">
    <h1>Create a game</h1>
    <input placeholder='house name' v-model='playerName'>
    <button v-on:click="createGame">
      Create game
    </button>
  </div>
</template>

<script>
import { createGame } from '../API.js'
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
  }
}

</script>
