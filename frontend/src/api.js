// Thin client for the HarvestProof API. The token lives in localStorage.
let token = null
try { token = localStorage.getItem('hp_token') } catch { /* private mode */ }
let onAuthLost = () => {}

export const getToken = () => token
export const setToken = (t) => {
  token = t
  try { t ? localStorage.setItem('hp_token', t) : localStorage.removeItem('hp_token') } catch { /* ignore */ }
}
export const setAuthLostHandler = (fn) => { onAuthLost = fn }

export async function api(path, { method = 'GET', json, body } = {}) {
  const headers = {}
  if (token) headers.Authorization = 'Bearer ' + token
  if (json !== undefined) { headers['Content-Type'] = 'application/json'; body = JSON.stringify(json) }
  let r
  try {
    r = await fetch('/api' + path, { method, headers, body })
  } catch {
    throw new Error('Cannot reach the server. Check your internet connection and try again.')
  }
  let d = {}
  try { d = await r.json() } catch { /* empty body */ }
  if (r.status === 401 && token) { onAuthLost(); throw new Error('Your session ended. Please sign in again.') }
  if (!r.ok) {
    if (typeof d.detail === 'string') throw new Error(d.detail)
    if (r.status === 429) throw new Error('Too many requests. Please wait a minute and try again.')
    if (r.status === 422) throw new Error('Please check what you entered and try again.')
    throw new Error(`Something went wrong (${r.status}). Please try again.`)
  }
  return d
}
