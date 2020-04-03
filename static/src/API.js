import { webSocket } from 'rxjs/webSocket'
const API_BASE = process.env.NODE_ENV === 'production' ? './api' : 'http://localhost:8000/api'
const WS_BASE = process.env.NODE_ENV === 'production' ? `ws://${window.location.origin}/ws` : 'ws://localhost:8000/ws'

export function spendMoney ({playerId, amount, destination}) {
  console.log('playerId', playerId)
  console.log('amount', amount)
  console.log('destination', destination)
  return fetch(`${API_BASE}/spend`, {
    method: 'POST',
    body: JSON.stringify({
      current_player: playerId,
      amount,
      destination
    }),
  })
}

function fetchWrapper(url, options) {
  return fetch(url, options)
    .then(response => response.json())
}

export function createGame({userName}) {
  return fetchWrapper(`${API_BASE}/create_game`, {
    method: 'POST',
    body: JSON.stringify({
      user_name: userName
    })
  })
}

export function joinGame({userName, gameId}) {
  return fetchWrapper(`${API_BASE}/join_game`, {
    method: 'POST',
    body: JSON.stringify({
      player_name: userName,
      game_id: gameId
    })
  })
}

export function createGame$(gameId) {
  return webSocket(`${WS_BASE}/game/${gameId}`)
}
