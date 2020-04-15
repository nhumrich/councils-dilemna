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
      const playerId = localStorage.getItem('player_id')
      createGame({userName: this.playerName, playerId}).then(results => {
        const { game_id, user_id } = results
        localStorage.setItem('player_id', user_id)
        this.$router.push({name: 'game-lobby', params: {game_id}})
      })
    },
  }
}

</script>
