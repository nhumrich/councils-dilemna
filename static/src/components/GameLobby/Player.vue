<template>
  <div class="player">
    <div>
      House name: {{player.name}}
    </div>
    <div>
      starting money: {{player.money}}
    </div>
    <div>
      starting power: {{player.power}}
      <button v-on:click="subtractMoney">
        -
      </button>
      <button>
        +
      </button>
    </div>
  </div>
</template>

<script>
import { spendMoney } from '../../API.js'
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
