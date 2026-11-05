import { useCallback, useEffect, useRef, useState } from 'react'
import { api, getToken, setAuthLostHandler, setToken } from './api'
import Welcome from './components/Welcome'
import Journey from './components/Journey'
import How from './components/How'
import Diagnose from './steps/Diagnose'
import Verify from './steps/Verify'
import Plan from './steps/Plan'
import Passport from './steps/Passport'

export default function App() {
  const [authed, setAuthed] = useState(!!getToken())
  const [demo, setDemo] = useState(() => { try { return localStorage.getItem('hp_demo') === '1' } catch { return false } })
  const [page, setPage] = useState('main')
  const [step, setStepRaw] = useState(1)
  const [meta, setMeta] = useState(null)
  const [metaErr, setMetaErr] = useState('')
  const [tries, setTries] = useState(0)
  const [crop, setCrop] = useState('tea')
  const [dx, setDx] = useState(null)
  const [pack, setPack] = useState(null)
  const [groupsN, setGroupsN] = useState(0)
  const [toastMsg, setToastMsg] = useState('')
  const toastTimer = useRef(null)

  const toast = useCallback((m) => { setToastMsg(m); clearTimeout(toastTimer.current); toastTimer.current = setTimeout(() => setToastMsg(''), 3500) }, [])
  const setStep = useCallback((n) => { setStepRaw(n); window.scrollTo?.({ top: 0, behavior: 'smooth' }) }, [])

  const signOut = useCallback(() => {
    setToken(null)
    try { localStorage.removeItem('hp_demo') } catch { /* ignore */ }
    setAuthed(false); setDemo(false); setMeta(null); setDx(null); setPack(null); setGroupsN(0); setStepRaw(1); setPage('main'); setCrop('tea')
  }, [])
  useEffect(() => { setAuthLostHandler(signOut) }, [signOut])

  useEffect(() => {
    if (!authed || meta) return
    api('/meta').then((m) => { setMeta(m); setMetaErr('') }).catch((e) => setMetaErr(e.message))
    api('/passport').then((r) => setGroupsN(r.groups.length)).catch(() => {})
  }, [authed, meta, tries])

  function onAuth(token, isDemo) {
    setToken(token)
    try { localStorage.setItem('hp_demo', isDemo ? '1' : '0') } catch { /* ignore */ }
    setDemo(isDemo); setAuthed(true); setStepRaw(1)
  }

  const done = [!!dx, !!pack, groupsN > 0, groupsN > 0]
  return (
    <div className="w">
      <header className="top">
        <div className="logo"><i>H</i>HarvestProof</div>
        <div className="row">
          <button type="button" className="link" onClick={() => setPage(page === 'how' ? 'main' : 'how')}>{page === 'how' ? 'Back to the app' : 'How it works'}</button>
          {authed && demo && <span className="sm mu">Demo mode</span>}
          {authed && <button type="button" className="gh s" onClick={signOut}>Sign out</button>}
        </div>
      </header>

      {page === 'how' && <How />}
      {page === 'main' && !authed && <Welcome onAuth={onAuth} />}
      {page === 'main' && authed && (
        <main>
          {demo && <div className="note info" style={{ marginBottom: 12 }}><b>Demo mode.</b> Your demo data stays on this server for this browser only. <button type="button" className="link" onClick={signOut}>Create a real account</button></div>}
          {metaErr && <div className="note bad" role="alert">{metaErr} <button type="button" className="link" onClick={() => { setMetaErr(''); setTries((t) => t + 1) }}>Try again</button></div>}
          {!meta && !metaErr && <div className="sm mu">Loading…</div>}
          {meta && (
            <>
              <Journey step={step} setStep={setStep} done={done} />
              <section hidden={step !== 1}><Diagnose meta={meta} crop={crop} setCrop={setCrop} onDx={setDx} goPlan={() => setStep(3)} /></section>
              <section hidden={step !== 2}><Verify meta={meta} pack={pack} setPack={setPack} goPlan={() => setStep(3)} toast={toast} /></section>
              <section hidden={step !== 3}><Plan meta={meta} active={step === 3} crop={crop} dx={dx} pack={pack} toast={toast} onLogged={() => { setGroupsN((n) => Math.max(1, n)); setStep(4) }} /></section>
              <section hidden={step !== 4}><Passport active={step === 4} onCount={setGroupsN} goStart={() => setStep(1)} /></section>
            </>
          )}
        </main>
      )}
      <footer>Sample and training photos: public tea and chilli leaf datasets, CC BY 4.0 (see DATA_SOURCES.md). Pesticide label data: CIB&amp;RC, Government of India. EU limits: APEDA list for green chilli.</footer>
      {toastMsg && <div className="toast" role="status">{toastMsg}</div>}
    </div>
  )
}
