import { useState } from 'react'
import { api } from '../api'
import { randomHex } from '../util'

export default function Welcome({ onAuth }) {
  const [mode, setMode] = useState('in')
  const [f, setF] = useState({ email: '', password: '', name: '', district: '' })
  const [err, setErr] = useState('')
  const [busy, setBusy] = useState(false)
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value })

  async function enter(path, json, demo) {
    setBusy(true); setErr('')
    try { const d = await api(path, { method: 'POST', json }); onAuth(d.token, demo) } catch (e) { setErr(e.message) } finally { setBusy(false) }
  }
  const submit = (e) => {
    e.preventDefault()
    if (mode === 'in') enter('/login', { email: f.email, password: f.password }, false)
    else enter('/register', f, false)
  }
  const demo = () => { const r = randomHex(16); enter('/register', { email: `demo-${r.slice(0, 12)}@demo.local`, password: r, name: 'Demo farmer', district: 'Demo' }, true) }

  return (
    <section>
      <div className="hero">
        <h1>Know it is safe to harvest, and prove it.</h1>
        <p>HarvestProof helps a farmer answer four questions before selling a crop: <b>What is wrong with my leaf? Is my pesticide pack genuine? Which spray fits my harvest date? When can I safely harvest?</b> You can even just <b>speak in Tamil</b> and hear the answer in Tamil.</p>
      </div>
      <div className="steps4">
        <div className="st"><span className="ic">🎤</span><b>1. Tell us or show us</b><span>Speak in Tamil or English, take a photo, or answer simple questions. We say the likely problem, or say we are not sure.</span></div>
        <div className="st"><span className="ic">🔎</span><b>2. Check the pack</b><span>Type or scan the code on the pesticide pack to see if it is registered, in date and not copied.</span></div>
        <div className="st"><span className="ic">🧪</span><b>3. Choose the spray</b><span>See only sprays whose label lists your problem on your crop, and that wait long enough before harvest.</span></div>
        <div className="st"><span className="ic">📋</span><b>4. Get the passport</b><span>A page with your earliest safe harvest date and every spray, which a buyer can open and check.</span></div>
      </div>
      <div className="g2" style={{ marginTop: 22 }}>
        <div className="card"><h2>Try it now</h2><p className="mu">No sign-up needed. The demo comes with sample photos and sample pack codes so you can see every step, including the voice assistant.</p>
          <button type="button" className="big" onClick={demo} disabled={busy}>Start the demo</button>
          <p className="sm mu">Advice only, not a laboratory certificate. Always follow the product label.</p></div>
        <form className="card" onSubmit={submit}>
          <div className="tabs"><button type="button" className={mode === 'in' ? 'on' : ''} onClick={() => setMode('in')}>Sign in</button><button type="button" className={mode === 'up' ? 'on' : ''} onClick={() => setMode('up')}>Create account</button></div>
          <label>Email<input type="email" value={f.email} onChange={set('email')} autoComplete="username" required /></label>
          <label>Password (8 or more characters)<input type="password" value={f.password} onChange={set('password')} autoComplete={mode === 'in' ? 'current-password' : 'new-password'} required minLength={mode === 'up' ? 8 : undefined} /></label>
          {mode === 'up' && <div className="r2"><label>Your name<input value={f.name} onChange={set('name')} /></label><label>District<input value={f.district} onChange={set('district')} /></label></div>}
          <button type="submit" disabled={busy}>{mode === 'in' ? 'Sign in' : 'Create account'}</button>
          {err && <div className="note bad" role="alert">{err}</div>}
        </form>
      </div>
    </section>
  )
}
