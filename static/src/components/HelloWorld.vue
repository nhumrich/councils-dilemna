<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <button v-on:click="spendMoney">
      Spend Money
    </button>
  </div>
</template>

<script>
import { spendMoney } from '../API.js'
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data: () => ({
    playerId: 'tk-421',
    amount: 10,
    destination: 'shrug'
  }),
  methods: {
    spendMoney: function () {
      spendMoney({playerId: this.playerId, amount: this.amount, destination: this.destination}).then(res => {
        console.log('res', res)
        // this.serverResponse = res
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
