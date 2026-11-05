import { useEffect, useRef, useState } from 'react'
import { api } from '../api'
import { cropName, fmt } from '../util'

export default function Verify({ meta, pack, setPack, goPlan, toast }) {
  const [code, setCode] = useState('')
  const [res, setRes] = useState(null)
  const [err, setErr] = useState('')
  const [busy, setBusy] = useState(false)
  const [demo, setDemo] = useState([])
  const [scanning, setScanning] = useState(false)
  const video = useRef(null)
  const stream = useRef(null)

  useEffect(() => { if (meta.demo) api('/demo-codes').then(setDemo).catch(() => {}) }, [meta.demo])
  useEffect(() => () => stopScan(), [])

  async function verify(c = code) {
    const value = (c || '').trim()
    if (!value) { setErr('Type or scan the batch code first.'); return }
    setBusy(true); setErr('')
    try {
      const r = await api('/verify', { method: 'POST', json: { code: value } })
      setRes(r)
      setPack(r.ok ? r : null)
      if (r.ok) setCode(r.code)
    } catch (e) { setErr(e.message) } finally { setBusy(false) }
  }

  function stopScan() {
    stream.current?.getTracks().forEach((t) => t.stop())
    stream.current = null
    setScanning(false)
  }

  async function startScan() {
    if (!('BarcodeDetector' in window)) { toast('This browser cannot scan QR codes. Please type the code.'); return }
    try {
      stream.current = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
      setScanning(true)
    } catch { toast('Camera blocked. Allow camera access (needs https or localhost), or type the code.') }
  }

  useEffect(() => {
    if (!scanning) return undefined
    let stop = false
    const v = video.current
    v.srcObject = stream.current
    v.play().catch(() => {})
    const det = new window.BarcodeDetector({ formats: ['qr_code'] })
    const loop = async () => {
      if (stop) return
      try {
        const r = await det.detect(v)
        if (r.length) { stopScan(); setCode(r[0].rawValue); verify(r[0].rawValue); return }
      } catch { /* keep trying */ }
      requestAnimationFrame(loop)
    }
    loop()
    return () => { stop = true }
  }, [scanning]) // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <>
      <div className="intro"><h2>Step 2. Check the pesticide pack</h2><p>Every genuine pack has a printed batch code. We check that it is real, registered, not expired and not being copied. Do this <b>before</b> you spray.</p></div>
      <div className="g2">
        <div className="card">
          <label>Batch code printed on the pack
            <input value={code} onChange={(e) => setCode(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') verify() }} autoComplete="off" spellCheck="false" placeholder="DEMOTR-00001-XXXXXXXX" />
          </label>
          <div className="row"><button type="button" onClick={() => verify()} disabled={busy}>Check this pack</button>{!scanning ? <button type="button" className="gh" onClick={startScan}>Scan the QR code</button> : <button type="button" className="gh" onClick={stopScan}>Stop scanning</button>}</div>
          {scanning && <video ref={video} playsInline muted style={{ width: '100%', borderRadius: 10 }} />}
          {demo.length > 0 && (
            <div>
              <p className="sm mu" style={{ marginBottom: 6 }}>No pack? Try a demo code. The colour shows what to expect:</p>
              <div className="demo">{demo.map((d) => <button type="button" key={d.code} className={d.kind} title={d.label} onClick={() => { setCode(d.code); verify(d.code) }}>{d.label}</button>)}</div>
            </div>
          )}
        </div>
        <div className="card">
          {err && <div className="note bad" role="alert">{err}</div>}
          {!res && !err && <div className="empty"><span style={{ fontSize: '2rem' }}>🔎</span>The result and the label details for the pack will appear here.</div>}
          {res && (
            <div className="col" aria-live="polite">
              <div className={`verdict ${res.ok ? 'ok' : 'bad'}`}><h3>{res.ok ? '✓ ' : '✗ '}{res.title}</h3><p className="sm">{res.text}</p></div>
              <ul className="checks">{(res.checks || []).map((c) => <li key={c.name}><span className={c.ok ? 't' : 'f'}>{c.ok ? '✓' : '✗'}</span><span>{c.name}<small>{c.detail}</small></span></li>)}</ul>
              {res.product && <div><b>{res.product}</b>{res.mfg && <p className="sm mu">Made {fmt(res.mfg)} · expires {fmt(res.exp)}</p>}</div>}
              {res.labels && <table><thead><tr><th>Registered for</th><th>Dose</th><th>Wait before harvest</th></tr></thead><tbody>{res.labels.map((l) => <tr key={l.crop}><td>{cropName(l.crop)}</td><td>{l.dose}</td><td>{l.phi} days</td></tr>)}</tbody></table>}
              {res.ok ? <button type="button" className="big" onClick={goPlan}>Use this pack: choose the spray →</button> : <div className="note bad">Do not spray with this pack until the shop or the company confirms it.</div>}
            </div>
          )}
        </div>
      </div>
    </>
  )
}
