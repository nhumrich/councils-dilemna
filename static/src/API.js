import { Subject } from 'rxjs'
import { tap } from 'rxjs/operators'
const API_BASE = process.env.NODE_ENV === 'production' ? './api' : 'http://localhost:8000/api'

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

export function createGame({userName, playerId}) {
  const body = {user_name: userName}
  if (playerId) {
    body.user_id = playerId
  }
  return fetchWrapper(`${API_BASE}/create_game`, {
    method: 'POST',
    body: JSON.stringify(body)
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

export function game$() {
  const subject = new Subject()
  const es = new EventSource(`${API_BASE}/event_stream`)
  es.onmessage = function (event) {
    subject.next(event)
  }
  return subject.asObservable().pipe(
    tap(e => console.log('tap', e))
  )
}
