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

export function createGame({userName}) {
  console.log('userName', userName)
  return fetch(`${API_BASE}/create_game`, {
    method: 'POST',
    body: JSON.stringify({
      user_name: userName
    })
  })
}
