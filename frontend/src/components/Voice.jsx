import { useEffect, useRef, useState } from 'react'
import { api } from '../api'
import { pc } from '../util'
import { createRecognizer, hasVoice, pickVoice, recognitionSupported, RECOGNITION_ERRORS, secureContext, speak, stopSpeaking, synthSupported, useVoices } from '../speech'

const NO_TAMIL_VOICE = 'No Tamil voice was found on this phone, so the answer cannot be read aloud in Tamil. Install the Tamil voice (Settings, Language, Text-to-speech, Google, Tamil). The answer is shown below.'
const CROP_WORDS = { rice: 'நெல்', chilli: 'மிளகாய்', grapes: 'திராட்சை', tea: 'தேயிலை' }
const CROP_LABEL = { rice: 'நெல் · Rice', chilli: 'மிளகாய் · Chilli', grapes: 'திராட்சை · Grapes', tea: 'தேயிலை · Tea' }

export default function Voice({ crop, answers, features, pending, onResult, onSeeOptions }) {
  const voices = useVoices()
  const [lang, setLang] = useState('ta-IN')
  const [text, setText] = useState('')
  const [listening, setListening] = useState(false)
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState('')
  const [res, setRes] = useState(null)
  const [autoSpeak, setAutoSpeak] = useState(true)
  const [autoListen, setAutoListen] = useState(false)
  const [speaking, setSpeaking] = useState(false)
  const rec = useRef(null)
  const reqId = useRef(0)
  const mounted = useRef(true)

  // Latest values for use inside callbacks that run later (speech events, async replies).
  const tamilOK = !synthSupported() ? false : voices.length === 0 ? null : hasVoice(voices, 'ta')
  const ctx = useRef({})
  ctx.current = { crop, answers, features, pending, lang, autoSpeak, autoListen, tamilOK, voices }

  useEffect(() => { mounted.current = true; return () => { mounted.current = false; rec.current?.abort?.(); stopSpeaking() } }, [])

  function say(r, which = 'ta') {
    const c = ctx.current
    if (which === 'ta' && c.tamilOK === false) { setMsg(NO_TAMIL_VOICE); return }
    if (!synthSupported()) { setMsg('This browser cannot read text aloud. Please read the answer on screen.'); return }
    setMsg('')
    setSpeaking(true)
    speak(which === 'ta' ? r.reply.ta : r.reply.en, {
      lang: which === 'ta' ? 'ta-IN' : 'en-IN',
      voice: pickVoice(c.voices, which === 'ta' ? 'ta' : 'en'),
      onEnd: () => {
        if (!mounted.current) return
        setSpeaking(false)
        if (ctx.current.autoListen && r.pending && which === 'ta') startListening()
      },
      onError: () => { if (mounted.current) { setSpeaking(false); setMsg('The answer could not be read aloud. Please read it on screen.') } },
    })
  }

  async function send(raw) {
    const t = (raw ?? text).trim()
    if (!t) { setMsg('Say something or type it first.'); return }
    rec.current?.abort?.()
    stopSpeaking()
    setSpeaking(false); setListening(false)
    setBusy(true); setMsg('')
    const id = ++reqId.current
    const c = ctx.current
    try {
      const r = await api('/voice', { method: 'POST', json: { text: t, lang: c.lang.slice(0, 2), crop: c.crop, answers: c.answers, features: c.features, pending: c.pending } })
      if (id !== reqId.current || !mounted.current) return
      setRes(r)
      onResult(r)
      if (ctx.current.autoSpeak) say(r)
    } catch (e) {
      if (id === reqId.current && mounted.current) setMsg(e.message)
    } finally {
      if (id === reqId.current && mounted.current) setBusy(false)
    }
  }

  function startListening() {
    if (!recognitionSupported() || !secureContext()) return
    stopSpeaking(); setSpeaking(false)
    setMsg(''); setText('')
    let r
    try {
      r = createRecognizer({
        lang: ctx.current.lang,
        onInterim: (t) => setText(t),
        onError: (code) => setMsg(RECOGNITION_ERRORS[code] ?? `Voice input problem (${code}). You can type instead.`),
        onEnd: (final, errored) => {
          if (!mounted.current) return
          setListening(false)
          if (final) { setText(final); send(final) } else if (!errored) setMsg(RECOGNITION_ERRORS['no-speech'])
        },
      })
      rec.current = r
      r.start()
      setListening(true)
    } catch {
      setListening(false)
      setMsg('Could not start the microphone. Please try again, or type instead.')
    }
  }

  const toggleMic = () => (listening ? rec.current?.stop?.() : startListening())
  const supported = recognitionSupported()
  const stopAll = () => { stopSpeaking(); setSpeaking(false) }

  return (
    <div className="voice" aria-label="Ask by voice">
      <div className="row">
        <h3 className="sp">🎤 குரலில் கேளுங்கள் · Ask by voice</h3>
        <label className="inline">Speak in
          <select value={lang} onChange={(e) => setLang(e.target.value)} aria-label="Speaking language">
            <option value="ta-IN">தமிழ் (Tamil)</option>
            <option value="en-IN">English</option>
          </select>
        </label>
      </div>
      <p className="sm mu">Tap the microphone and describe the leaf. For example: “என் மிளகாய் இலையில் வெள்ளை பவுடர் இருக்கு” or “My chilli leaves have white powder”.</p>

      {!supported && <div className="note">Voice input is not available in this browser. Use Chrome on Android or on a computer, or type your sentence below.</div>}
      {supported && !secureContext() && <div className="note">Voice input needs a secure address (https, or localhost). You can still type your sentence below.</div>}

      <div className="mic-row">
        <button type="button" className={`mic ${listening ? 'on' : ''}`} onClick={toggleMic} disabled={!supported || !secureContext() || busy} aria-pressed={listening} aria-label={listening ? 'Stop listening' : 'Start speaking'}>
          {listening ? '⏹' : '🎤'}
        </button>
        <span aria-live="polite">{listening ? 'கேட்கிறேன்… Listening…' : busy ? 'யோசிக்கிறேன்… Thinking…' : 'பேச தட்டவும் · Tap to speak'}</span>
      </div>

      <div className="row" style={{ alignItems: 'end' }}>
        <label className="sp">What I heard (you can correct it, or type here)
          <input value={text} onChange={(e) => setText(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') send() }} placeholder="…" lang={lang.slice(0, 2)} />
        </label>
        <button type="button" onClick={() => send()} disabled={busy || !text.trim()}>அனுப்பு · Send</button>
      </div>

      {msg && <div className="note" role="alert">{msg}</div>}

      {res && (
        <div className={`reply ${res.status}`} aria-live="polite">
          {res.heard.length > 0 && (
            <div className="chips">{res.heard.map((h) => <span key={h.q} className={`chip ${h.value ? '' : 'no'}`}><b>{h.ta}</b> · {h.en}</span>)}</div>
          )}
          <p lang="ta" className="reply-ta">{res.reply.ta}</p>
          <p className="sm mu">{res.reply.en}</p>
          {res.status === 'need_crop' && (
            <div className="row">{Object.keys(CROP_WORDS).map((c) => <button type="button" className="gh s" key={c} onClick={() => send(CROP_WORDS[c])}>{CROP_LABEL[c]}</button>)}</div>
          )}
          {res.pending && (
            <div className="row" aria-label="Quick answers">
              <button type="button" onClick={() => send('ஆம்')}>ஆம் · Yes</button>
              <button type="button" onClick={() => send('இல்லை')}>இல்லை · No</button>
              <button type="button" className="gh" onClick={() => send('தெரியவில்லை')}>தெரியவில்லை · Not sure</button>
            </div>
          )}
          {res.options.length > 0 && (
            <div className="col">
              <b className="sm">Registered sprays on the official list (shortest wait first):</b>
              {res.options.map((o) => <div key={o.code} className="sm">• {o.product}: wait {o.wait} days · dose {o.dose}</div>)}
              <button type="button" className="gh s" onClick={onSeeOptions}>See all options and dates →</button>
            </div>
          )}
          <div className="row">
            <button type="button" className="gh s" onClick={() => say(res, 'ta')}>🔊 தமிழில் கேளுங்கள்</button>
            <button type="button" className="gh s" onClick={() => say(res, 'en')}>🔊 In English</button>
            {speaking && <button type="button" className="gh s" onClick={stopAll}>⏹ நிறுத்து · Stop</button>}
            {res.diagnosis?.verdict?.id && res.status !== 'need_crop' && <span className="sm mu">{pc(res.diagnosis.verdict.p)} sure</span>}
          </div>
        </div>
      )}

      <div className="row sm">
        <label className="chk"><input type="checkbox" checked={autoSpeak} onChange={(e) => setAutoSpeak(e.target.checked)} /> Read answers aloud in Tamil · தமிழில் படித்துக் காட்டு</label>
        <label className="chk"><input type="checkbox" checked={autoListen} onChange={(e) => setAutoListen(e.target.checked)} /> Listen again after each question</label>
      </div>
      {tamilOK === false && <div className="note sm">{NO_TAMIL_VOICE}</div>}
      <p className="sm mu">Voice recognition is done by your browser, which may send the audio to its provider (for example Google) to turn it into text. Tamil wording should be checked by an agriculture officer.</p>
    </div>
  )
}
