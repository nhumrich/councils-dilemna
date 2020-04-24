<template>
  <div class="player">
    <div>
      House name: {{player.name}}
    </div>
    <div>
      starting power: {{player.power}}
      <button v-on:click="subtractPower">
        -
      </button>
      <button v-on:click="addPower">
        +
      </button>
    </div>
    <div>
      starting money: {{player.money}}
      <button v-on:click="subtractMoney">
        -
      </button>
      <button v-on:click="addMoney">
        +
      </button>
    </div>
  </div>
</template>

<script>
import { spendMoney, gainMoney, spendPower, gainPower } from '../../API.js'
export default {
  name: 'Player',
  props: {
    player: {
      type: Object,
      required: true,
    }
  },
  methods: {
    subtractMoney: function() {
      spendMoney({playerId: this.player.id, amount: 1, destination: 'GAME_SETUP'})
    },
    addMoney: function() {
      gainMoney({playerId: this.player.id, amount: 1, destination: 'GAME_SETUP'})
    },
    subtractPower: function() {
      spendPower({playerId: this.player.id, amount: 1, destination: 'GAME_SETUP'})
    },
    addPower: function() {
      gainPower({playerId: this.player.id, amount: 1, destination: 'GAME_SETUP'})
    }
  }
}
</script>
<style scoped>
.player{
  display: flex;
}
.player > div {
  margin-left: 12px;
  margin-right: 12px;
}
</style>
