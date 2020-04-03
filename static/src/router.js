import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const Setup = () => import(/* webpackChunkName: "setup" */'./components/Setup.vue')
const CreateGame = () => import(/* webpackChunkName: "CreateGame" */'./components/CreateGame.vue')
const JoinGame = () => import(/* webpackChunkName: "JoinGame" */'./components/JoinGame.vue')
const GameLobby = () => import(/* webpackChunkName: "GameLobby" */'./components/GameLobby.vue')

export default new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'set-up',
      component: Setup,
    },
    {
      path: '/create-game',
      name: 'create-game',
      component: CreateGame
    },
    {
      path: '/join-game',
      name: 'join-game',
      component: JoinGame
    },
    {
      path: '/game-lobby/:game_id',
      name: 'game-lobby',
      component: GameLobby
    }
  ],
})
