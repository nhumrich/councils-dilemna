import { Subject } from 'rxjs'
import { map, tap, pluck, filter, finalize } from 'rxjs/operators'
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

export function joinGame({userName, gameId, playerId}) {
  const body = {
    player_name: userName,
    game_id: gameId,
  }
  if (playerId) {
    body.player_id = playerId
  }
  return fetchWrapper(`${API_BASE}/join_game`, {
    method: 'POST',
    body: JSON.stringify(body)
  })
}

export function game$(gameId) {
  const subject = new Subject()
  const es = new EventSource(`${API_BASE}/game_stream/${gameId}`)
  es.onmessage = function (event) {
    subject.next(event)
  }
  return subject.asObservable().pipe(
    pluck('data'),
    filter(data => {
      console.log('raw', data)
      try {
        const jsonData = JSON.parse(data)
        return jsonData
      } catch (e) {
        return false
      }
    }),
    map(data => JSON.parse(data)),
    tap(data => console.log('data tap', data, typeof(data))),
    finalize(() => es.close())
  )
}
