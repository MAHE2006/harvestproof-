import { useEffect, useState } from 'react'
import { api } from '../api'
import { cropName, daysBetween, fmt, localDate } from '../util'

export default function Passport({ active, onCount, goStart }) {
  const [groups, setGroups] = useState(null)
  const [err, setErr] = useState('')
  const [links, setLinks] = useState({})
  const [printing, setPrinting] = useState(null)

  async function load() {
    try { const r = await api('/passport'); setGroups(r.groups); onCount(r.groups.length); setErr('') } catch (e) { setErr(e.message) }
  }
  useEffect(() => { if (active) load() }, [active]) // eslint-disable-line react-hooks/exhaustive-deps

  async function remove(id) { try { await api('/sprays/' + id, { method: 'DELETE' }); load() } catch (e) { setErr(e.message) } }
  async function share(g, i) {
    try { const d = await api('/passport/share', { method: 'POST', json: { field: g.field, crop: g.crop } }); setLinks({ ...links, [i]: location.origin + d.url }) } catch (e) { setErr(e.message) }
  }
  function print(i) { setPrinting(i); setTimeout(() => { window.print(); setPrinting(null) }, 50) }

  return (
    <>
      <div className="intro"><h2>Step 4. Your harvest passport</h2><p>This shows the earliest day each field is safe to harvest, based on the label waiting period of every spray you logged. Share the link so a buyer can check it.</p></div>
      <div className="col" aria-live="polite">
        {err && <div className="note bad" role="alert">{err}</div>}
        {groups && !groups.length && <div className="card empty"><span style={{ fontSize: '2rem' }}>📋</span><b>No sprays logged yet</b><span>Once you log a spray, this page shows the earliest safe harvest date.</span><button type="button" onClick={goStart}>Start with the leaf check</button></div>}
        {groups?.map((g, i) => {
          const hold = Math.max(0, daysBetween(g.clear, localDate()))      // counted from the farmer's own date
          return (
            <article key={`${g.field}|${g.crop}`} className={`pass ${hold ? 'hold' : ''} ${printing === i ? 'printing' : ''}`}>
              <div className="row"><div className="sp"><h3>{g.field} · {cropName(g.crop)}</h3><p className="sm mu">Earliest safe harvest</p></div><div className="badge">{hold ? `WAIT ${hold} MORE DAY${hold === 1 ? '' : 'S'}` : 'CLEAR TO HARVEST'}</div></div>
              <div className="bigdate">{fmt(g.clear)}</div>
              <ul className="tl">{g.sprays.map((s) => (
                <li key={s.id}><b>{fmt(s.date)}: {s.product}</b><span className="sm mu">Dose {s.dose} · wait {s.wait} days · batch {s.batch}</span><span className={`eu ${s.eu.level}`}>{s.eu.text}</span><span><button type="button" className="link" onClick={() => remove(s.id)}>Remove this entry</button></span></li>
              ))}</ul>
              {g.export_warning && <div className="note">Selling abroad? At least one spray has a strict or unknown EU residue limit. India's waiting period alone may not be enough. Get a lab residue test.</div>}
              <div className="row"><button type="button" onClick={() => share(g, i)}>Create a link for my buyer</button><button type="button" className="gh" onClick={() => print(i)}>Print or save as PDF</button></div>
              {links[i] && <div className="note ok col"><span>Send this link. The buyer sees your passport and whether it has been altered:</span><a href={links[i]} target="_blank" rel="noopener noreferrer">{links[i]}</a><img alt="QR code for the passport link" width="130" height="130" src={`/api/qr.png?text=${encodeURIComponent(links[i])}`} /></div>}
            </article>
          )
        })}
      </div>
    </>
  )
}
