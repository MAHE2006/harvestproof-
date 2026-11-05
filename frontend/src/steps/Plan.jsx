import { useEffect, useState } from 'react'
import { api } from '../api'
import { addDays, cropName, fmt, localDate } from '../util'

const HINT = {
  chilli_murda: 'Murda is a mite, thrips and virus complex. A fungicide does not help. Ask an agriculture officer about controlling mites and thrips.',
  chilli_nutritional: 'This looks like a nutrient problem, not a disease. Do not spray fungicide. Get a leaf or soil test.',
  tea_helopeltis: 'Helopeltis is an insect pest, so a fungicide does not help.',
  tea_algalspot: 'No fungicide on the official list names this problem. Ask a tea extension officer.',
  tea_redspot: 'No fungicide on the official list names this problem. Ask a tea extension officer.',
  tea_brownblight: 'No fungicide on the official list names this problem for tea. Ask a tea extension officer.',
}

export default function Plan({ meta, active, crop, dx, pack, onLogged, toast }) {
  const [field, setField] = useState('Plot 1')
  const [pcrop, setPcrop] = useState(crop)
  const [pdis, setPdis] = useState('')
  const [harvest, setHarvest] = useState(addDays(localDate(), 30))
  const [res, setRes] = useState(null)
  const [err, setErr] = useState('')
  const [busy, setBusy] = useState(false)
  const [dates, setDates] = useState({})
  const [sd2, setSd2] = useState(localDate())

  const diseasesOf = (c) => Object.entries(meta.classes).filter(([, v]) => v.crop === c)

  useEffect(() => {
    if (!active) return
    setPcrop(crop)
    const d = dx && meta.classes[dx.id]?.crop === crop ? dx.id : diseasesOf(crop)[0]?.[0] || ''
    setPdis(d); setRes(null); setErr('')
    if (dx && d) run(crop, d)
  }, [active]) // eslint-disable-line react-hooks/exhaustive-deps

  async function run(c = pcrop, d = pdis) {
    if (!d) return
    setBusy(true); setErr('')
    try {
      setRes(await api('/plan', { method: 'POST', json: { crop: c, disease: d, harvest: harvest || null, field, today: localDate() } }))
    } catch (e) { setErr(e.message); setRes(null) } finally { setBusy(false) }
  }

  async function logSpray(sprayed) {
    if (!pack) { toast('Check a pack in step 2 first.'); return }
    try {
      await api('/sprays', { method: 'POST', json: { field, crop: pcrop, code: pack.code, sprayed, disease: pdis } })
      toast('Spray logged. Your passport is updated.')
      onLogged()
    } catch (e) { toast(e.message) }
  }

  const ok = res?.options.filter((o) => !o.why) || []
  const no = res?.options.filter((o) => o.why) || []
  const card = (o) => {
    const mine = pack && pack.product_code === o.code
    const date = dates[o.code] || localDate()
    return (
      <div key={o.code} className={`opt ${o.recommended ? 'best' : ''} ${o.why ? 'no' : ''}`}>
        <div className="row">{o.recommended && <span className="tag ok">Best fit</span>}{mine && <span className="tag wn">Your checked pack</span>}<h3 className="sp">{o.product}</h3></div>
        <div className="sm">Dose: <b>{o.dose}</b> · Mode of action: {o.moa}</div>
        {o.why ? <div className="note">{o.why}</div> : <div><b>Wait {o.wait} days</b> after spraying. Earliest harvest if you spray today: <b>{fmt(o.earliest)}</b></div>}
        <div className={`eu ${o.eu.level}`}>{o.eu.text}</div>
        {!o.why && (mine
          ? <div className="row"><label style={{ flex: 1 }}>I sprayed on<input type="date" value={date} max={localDate()} onChange={(e) => setDates({ ...dates, [o.code]: e.target.value })} /></label><button type="button" onClick={() => logSpray(date)}>I sprayed this: log it</button></div>
          : <p className="sm mu">To log this spray you first need to check a pack of this product in step 2.</p>)}
      </div>
    )
  }

  return (
    <>
      <div className="intro"><h2>Step 3. Choose and log the spray</h2><p>We list only sprays whose official label names your problem on your crop. Sprays that would make you wait past your harvest date are set aside. After you spray, log it so your passport is updated.</p></div>
      <div className="g2">
        <div className="card">
          <div className="r2">
            <label>Field name<input value={field} maxLength={30} onChange={(e) => setField(e.target.value)} /></label>
            <label>Crop<select value={pcrop} onChange={(e) => { setPcrop(e.target.value); setPdis(diseasesOf(e.target.value)[0]?.[0] || ''); setRes(null) }}>{meta.crops.map((c) => <option key={c} value={c}>{cropName(c)}</option>)}</select></label>
          </div>
          <div className="r2">
            <label>Problem<select value={pdis} onChange={(e) => { setPdis(e.target.value); setRes(null) }}>{diseasesOf(pcrop).map(([k, v]) => <option key={k} value={k}>{v.name}</option>)}</select></label>
            <label>Planned harvest date<input type="date" value={harvest} onChange={(e) => setHarvest(e.target.value)} /></label>
          </div>
          <button type="button" onClick={() => run()} disabled={busy || !pdis}>Show my spray options</button>
          <div className="sm mu">{dx ? <>Based on your leaf check: <b>{dx.name}</b>. </> : 'Choose the problem yourself, or go back to step 1. '}{pack ? <>Pack checked: <b>{pack.product}</b>.</> : 'No pack checked yet (step 2).'}</div>
          <details><summary>Already sprayed? Log it without a recommendation</summary>
            <div className="col" style={{ marginTop: 8 }}>
              <p>Uses the pack you checked in step 2 and the crop and problem above.</p>
              <label>Spray date<input type="date" value={sd2} max={localDate()} onChange={(e) => setSd2(e.target.value)} /></label>
              <button type="button" className="gh" onClick={() => logSpray(sd2)}>Log spray</button>
            </div>
          </details>
        </div>
        <div className="col" aria-live="polite">
          {err && <div className="note bad" role="alert">{err}</div>}
          {!res && !err && <div className="card empty"><span style={{ fontSize: '2rem' }}>🧪</span>Pick your problem and press the button.</div>}
          {res?.no_spray && <div className="note ok">No spray needed. The leaf looks healthy.</div>}
          {res && !res.no_spray && !res.options.length && <div className="note bad"><b>No product fits.</b> {HINT[pdis] || 'No fungicide on the official list names this problem on this crop. Ask your agriculture officer.'}</div>}
          {res && !res.no_spray && res.options.length > 0 && (ok.length ? ok.map(card) : <div className="note bad"><b>None of the listed sprays fits your harvest date.</b> Move the harvest date or ask your agriculture officer.</div>)}
          {no.length > 0 && <details><summary>Set aside ({no.length})</summary><div className="col" style={{ marginTop: 8 }}>{no.map(card)}</div></details>}
        </div>
      </div>
    </>
  )
}
