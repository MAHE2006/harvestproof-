import { useEffect, useRef, useState } from 'react'
import { api } from '../api'
import { CROPS, cropName, pc, shrinkImage } from '../util'
import { hasVoice, pickVoice, speak, stopSpeaking, synthSupported, useVoices } from '../speech'
import Voice from '../components/Voice'

const MEAS = {
  n_lesions: ['Spots found', (v) => Math.round(v)], burden: ['Leaf area with spots', pc], spindle: ['Long, thin spots', pc], round: ['Round spots', pc],
  green: ['Green leaf area', pc], yellow: ['Yellow area', pc], white: ['White area', pc], dark: ['Dark or grey area', pc],
}
const SAMPLES = [
  ['tea_greyblight', 'tea', 'Tea', 'gray blight'], ['tea_healthy', 'tea', 'Tea', 'healthy'], ['tea_brownblight', 'tea', 'Tea', 'brown blight'],
  ['chilli_powdery', 'chilli', 'Chilli', 'powdery mildew'], ['chilli_cercospora', 'chilli', 'Chilli', 'cercospora'], ['chilli_nutritional', 'chilli', 'Chilli', 'nutrient deficiency'],
]

export default function Diagnose({ meta, crop, setCrop, onDx, goPlan }) {
  const [feats, setFeats] = useState(null)
  const [answers, setAnswers] = useState({})
  const [last, setLast] = useState(null)
  const [preview, setPreview] = useState(null)
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const [more, setMore] = useState(false)
  const reqId = useRef(0)
  const voices = useVoices()
  const [speakingMain, setSpeakingMain] = useState(false)

  const photoTrained = meta.photo_model.trained_crops.includes(crop)

  // Tell the parent which problem (if any) is settled, so step 3 can use it.
  useEffect(() => {
    const v = last?.verdict
    onDx(v && v.id && v.status !== 'asking' ? { id: v.id, name: v.name } : null)
  }, [last]) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => () => { if (preview) URL.revokeObjectURL(preview) }, [preview])
  useEffect(() => { runDx({ crop, answers: {}, feats: null }); return () => stopSpeaking() }, []) // eslint-disable-line react-hooks/exhaustive-deps

  async function runDx({ crop: c = crop, answers: a = answers, feats: f = feats, file = null } = {}) {
    const id = ++reqId.current
    setBusy(true); setErr('')
    const fd = new FormData()
    fd.append('crop', c)
    fd.append('answers', JSON.stringify(a))
    if (file) fd.append('image', file, 'leaf.jpg')
    else if (f) fd.append('features', JSON.stringify(f))
    try {
      const r = await api('/diagnose', { method: 'POST', body: fd })
      if (id !== reqId.current) return
      if (file) setFeats(r.features)
      setLast(r)
    } catch (e) {
      if (id === reqId.current) setErr(e.message)
    } finally {
      if (id === reqId.current) setBusy(false)
    }
  }

  function showPreview(blobOrFile) {
    setPreview(URL.createObjectURL(blobOrFile))
  }

  function pickCrop(c) {
    setCrop(c); setAnswers({}); setFeats(null); setPreview(null); setMore(false); setLast(null)
    runDx({ crop: c, answers: {}, feats: null })
  }

  async function onFile(e) {
    const f = e.target.files?.[0]
    e.target.value = ''
    if (!f) return
    setAnswers({}); setMore(false)
    showPreview(f)
    runDx({ answers: {}, file: await shrinkImage(f) })
  }

  async function useSample(s) {
    try {
      const blob = await (await fetch(`/samples/${s[0]}.jpg`)).blob()
      setCrop(s[1]); setAnswers({}); setMore(false)
      showPreview(blob)
      runDx({ crop: s[1], answers: {}, file: blob })
    } catch { setErr('Could not load the sample photo.') }
  }

  function answer(q, val) {
    const next = { ...answers, [q]: val }
    setAnswers(next)
    runDx({ answers: next })
  }

  function onVoice(r) {
    if (!r.crop) return
    if (r.crop !== crop) { setCrop(r.crop); setFeats(null); setPreview(null) }
    setAnswers(r.answers); setMore(false)
    if (r.diagnosis) setLast(r.diagnosis)
  }

  const tamilOK = !synthSupported() ? false : voices.length === 0 ? null : hasVoice(voices, 'ta')
  function readAloud() {
    if (!last?.reply) return
    if (tamilOK === false) { setErr('No Tamil voice was found on this phone. Please read the answer on screen.'); return }
    setErr(''); setSpeakingMain(true)
    speak(last.reply.ta, { lang: 'ta-IN', voice: pickVoice(voices, 'ta'), onEnd: () => setSpeakingMain(false), onError: () => setSpeakingMain(false) })
  }

  const v = last?.verdict
  const healthy = v?.id?.endsWith('_healthy')
  const showQ = last?.next && (v?.status !== 'confident' || more)

  return (
    <>
      <div className="intro"><h2>Step 1. Check the leaf</h2><p>Choose your crop, then <b>speak</b>, show a photo, or answer simple questions. You can mix them. We ask only the questions that matter most.</p></div>
      <div className="g2">
        <div className="col">
          <div className="card">
            <h3>A. Which crop?</h3>
            <div className="crops">
              {meta.crops.map((c) => (
                <button type="button" key={c} className={c === crop ? 'on' : ''} aria-pressed={c === crop} onClick={() => pickCrop(c)}><span>{CROPS[c]?.[0]}</span>{cropName(c)}</button>
              ))}
            </div>
            <h3>B. Show us the leaf</h3>
            <div className="r2">
              <label className="drop" htmlFor="cam"><span style={{ fontSize: '1.6rem' }}>📷</span><b>Take a photo</b></label>
              <label className="drop" htmlFor="gal"><span style={{ fontSize: '1.6rem' }}>🖼️</span><b>Upload a photo</b></label>
            </div>
            <input id="cam" type="file" accept="image/*" capture="environment" hidden onChange={onFile} />
            <input id="gal" type="file" accept="image/*" hidden onChange={onFile} />
            <p className="sm mu">One leaf, close up, in good light, on a plain background.</p>
            <div>
              <p className="sm mu" style={{ marginBottom: 6 }}>No photo handy? Try a sample (real dataset photos the system never trained on):</p>
              <div className="thumbs">
                {SAMPLES.map((s) => (
                  <button type="button" key={s[0]} onClick={() => useSample(s)} title={`${s[2]} leaf. Dataset label: ${s[3]}`}>
                    <img src={`/samples/${s[0]}.jpg`} alt={`${s[2]} leaf sample`} loading="lazy" /><span>{s[2]}: {s[3]}</span>
                  </button>
                ))}
              </div>
            </div>
            {preview && <div className="col"><img id="pvimg" src={preview} alt="Your leaf photo" />{feats && <div className="chips">{Object.entries(MEAS).map(([k, [n, fn]]) => <span className="chip" key={k}>{n}: <b>{fn(feats[k])}</b></span>)}</div>}</div>}
            {!photoTrained && <div className="note info">Photo analysis is not available for {cropName(crop).toLowerCase()} yet (no labelled photos). Speak or answer the questions and we will work from your answers.</div>}
          </div>
          <div className="card"><Voice crop={crop} answers={answers} features={feats} pending={last?.next?.question || null} onResult={onVoice} onSeeOptions={goPlan} /></div>
        </div>

        <div className="card">
          <h3>C. What we think</h3>
          <div className="col" aria-live="polite">
            {err && <div className="note bad" role="alert">{err}</div>}
            {busy && !last && <div className="sm mu">Thinking…</div>}
            {last?.note && <div className="note bad">{last.note}</div>}
            {last && v.status === 'asking' && (
              <div className="verdict wn"><h3>Not sure yet</h3><p className="sm">Best guess so far: {last.posterior[0].name} ({pc(last.posterior[0].p)}). Answer the question below to sharpen it.</p><div className="meter"><b style={{ width: pc(last.posterior[0].p) }} /></div></div>
            )}
            {last && v.status !== 'asking' && v.id && (
              <div className={`verdict ${healthy ? 'ok' : 'wn'}`}>
                <span className={`tag ${v.status === 'confident' ? 'ok' : 'wn'}`}>{v.status === 'confident' ? 'Confident' : 'Best guess'}</span>
                <h3>{healthy ? 'Your leaf looks healthy' : `Likely: ${v.name}`}</h3>
                <div className="meter"><b style={{ width: pc(v.p) }} /></div>
                <p className="sm">{pc(v.p)} sure, using {last.photo_used ? 'your photo and ' : ''}{last.answered} answer{last.answered === 1 ? '' : 's'}.{last.photo_used && last.photo_only ? ` The photo alone said ${last.photo_only[0].name} (${pc(last.photo_only[0].p)}).` : ''}</p>
              </div>
            )}
            {last && v.status !== 'asking' && !v.id && (
              <div className="verdict bad"><h3>We cannot tell</h3><p className="sm">The evidence does not separate these causes, so we will not guess. Photograph a fresher leaf, or ask your agriculture officer.</p></div>
            )}
            {last?.reply && (
              <div className="tareply">
                <p lang="ta" className="reply-ta">{last.reply.ta}</p>
                <div className="row"><button type="button" className="gh s" onClick={readAloud}>🔊 தமிழில் கேளுங்கள்</button>{speakingMain && <button type="button" className="gh s" onClick={() => { stopSpeaking(); setSpeakingMain(false) }}>⏹ Stop</button>}</div>
              </div>
            )}
            {showQ && (
              <div className="qcard"><h3>{last.next.text}?</h3><p className="sm mu">We ask this because it removes the most doubt right now.</p>
                <div className="row"><button type="button" onClick={() => answer(last.next.question, true)}>Yes</button><button type="button" onClick={() => answer(last.next.question, false)}>No</button><button type="button" className="gh" onClick={() => answer(last.next.question, null)}>Not sure</button></div>
              </div>
            )}
            {last?.next && v.status === 'confident' && !more && <button type="button" className="link" onClick={() => setMore(true)}>Want to double-check? Answer a few more questions</button>}
            {last && <div className="bars">{last.posterior.map((x) => <div className="br" key={x.id}><span>{x.name}</span><i><b style={{ width: pc(x.p) }} /></i><span>{pc(x.p)}</span></div>)}</div>}
            {v?.id && v.status !== 'asking' && !healthy && <button type="button" className="big" onClick={goPlan}>Next: find a spray for this →</button>}
            {healthy && <div className="note ok">No spray is needed. You can still check a pack or view your passport using the steps above.</div>}
            {last && <details><summary>How did we decide?</summary><p>{last.photo_used ? 'The photo was turned into measurements (number of spots, how long and thin they are, how much of the leaf is green, yellow or dark). A model trained on labelled photos converted those into probabilities. ' : 'No photo analysis was used. '}Each answer you give, spoken or tapped, then shifts the probabilities. The system is only called "Confident" once the chance passes {pc(last.photo_used ? last.accept : 0.8)}.</p></details>}
          </div>
        </div>
      </div>
    </>
  )
}
