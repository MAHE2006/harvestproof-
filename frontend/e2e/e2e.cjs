// End-to-end test: the real React app (bundled) in jsdom, a fake microphone and speaker, and the REAL server.
// Usage: node e2e/e2e.cjs <base-url> <path-to-iife-bundle>
const { JSDOM } = require('jsdom'); const fs = require('fs')
const [BASE, BUNDLE] = [process.argv[2], process.argv[3]]
const dom = new JSDOM('<!doctype html><html><body><div id="root"></div></body></html>', { runScripts: 'outside-only', url: BASE + '/', pretendToBeVisual: true })
const w = dom.window
w.fetch = (u, o) => fetch(String(u).startsWith('http') ? u : BASE + (String(u).startsWith('/') ? u : '/' + u), o)
w.FormData = FormData; w.Blob = Blob; w.crypto = require('crypto').webcrypto; w.scrollTo = () => {}; w.print = () => {}; w.URL.createObjectURL = () => 'blob:x'; w.URL.revokeObjectURL = () => {}
const errors = []; w.addEventListener('error', (e) => errors.push(e.message)); w.console.error = (...a) => errors.push(a.join(' '))
// fake microphone
class Rec { constructor() { Rec.last = this } start() { this.on = true } stop() { this.onend && this.onend() } abort() {}
  say(t) { this.onresult({ resultIndex: 0, results: [Object.assign([{ transcript: t }], { isFinal: true })] }); this.onend() } }
w.SpeechRecognition = Rec
// fake speaker with a Tamil voice
const spoken = []
w.SpeechSynthesisUtterance = class { constructor(t) { this.text = t } }
w.speechSynthesis = { getVoices: () => [{ lang: 'ta-IN' }, { lang: 'en-IN' }], cancel() {}, addEventListener() {}, removeEventListener() {}, speak(u) { spoken.push({ text: u.text, lang: u.lang }); setTimeout(() => u.onend && u.onend(), 0) } }
w.eval(fs.readFileSync(BUNDLE, 'utf8'))

const $ = (s) => w.document.querySelector(s), $$ = (s) => [...w.document.querySelectorAll(s)]
const sleep = (ms) => new Promise((r) => setTimeout(r, ms))
const text = () => w.document.body.textContent.replace(/\s+/g, ' ')
const btn = (re) => $$('button').find((b) => re.test(b.textContent.replace(/\s+/g, ' ')) || re.test(b.getAttribute('aria-label') || ''))
async function until(fn, what, ms = 8000) { const t = Date.now(); while (Date.now() - t < ms) { try { const v = fn(); if (v) return v } catch {} await sleep(60) } throw new Error('TIMEOUT waiting for: ' + what + '\nPAGE: ' + text().slice(0, 600)) }
function type(el, v) { Object.getOwnPropertyDescriptor(el.tagName === 'SELECT' ? w.HTMLSelectElement.prototype : w.HTMLInputElement.prototype, 'value').set.call(el, v); el.dispatchEvent(new w.Event(el.tagName === 'SELECT' ? 'change' : 'input', { bubbles: true })) }
let n = 0; const ok = (c, m) => { n++; if (!c) { console.log('FAIL', n, m); process.exitCode = 1; throw new Error('assertion failed: ' + m) } else console.log('ok  ', n, m) }

;(async () => {
  await until(() => btn(/Start the demo/), 'welcome page'); ok(text().includes('Know it is safe to harvest'), 'welcome page explains the product')
  btn(/Start the demo/).click()
  await until(() => $$('.journey button').length === 4 && $('.crops'), 'app after demo start'); ok(text().includes('Demo mode'), 'demo mode banner shown')
  await until(() => $('.qcard'), 'first question for tea (no photo)'); ok($$('.crops button').length === 4, 'four crops offered')

  // ---- voice, typed path: the headline example in English ----
  const input = () => $('input[placeholder="…"]')
  type(input(), 'My chilli leaves have white powder.'); btn(/அனுப்பு/).click()
  await until(() => text().includes('மிளகாய் சாம்பல் நோய் போல் தெரிகிறது'), 'Tamil reply for the English sentence')
  ok($$('.crops button').find((b) => b.getAttribute('aria-pressed') === 'true').textContent.includes('Chilli'), 'crop switched to Chilli by voice')
  ok(text().includes('Likely: Chilli powdery mildew'), 'result card shows the likely disease')
  ok(text().includes('வெள்ளைத் தூள்: ஆம்'), 'shows what it understood (white powder: yes)')
  await until(() => spoken.length > 0, 'Tamil speech started'); ok(spoken.every((s) => s.lang === 'ta-IN') && spoken.map((s) => s.text).join(' ').includes('உறுதி'), 'answer was read aloud in Tamil')
  ok(text().includes('Azoxystrobin') || text().includes('Registered sprays on the official list'), 'voice answer lists registered sprays')

  // ---- voice, microphone path in Tamil: switches crop and discards old answers ----
  btn(/Start speaking/).click(); ok(Rec.last.on === true, 'microphone started')
  Rec.last.say('நெல் இலை சுருண்டு இருக்கு, மழை இல்லை')
  await until(() => $$('.crops button').find((b) => b.getAttribute('aria-pressed') === 'true').textContent.includes('Rice'), 'crop switched to Rice')
  await until(() => text().includes('இலை சுருட்டை: ஆம்') && text().includes('மழை அல்லது ஈரப்பதம்: இல்லை'), 'understood curl=yes and rain=no in Tamil')
  ok(!text().includes('Likely: Chilli powdery'), 'old chilli answers were discarded')

  // ---- the app asks a follow-up and the farmer answers with the quick buttons ----
  const q = await until(() => btn(/ஆம் · Yes/), 'quick answer buttons'); const before = text()
  q.click(); await until(() => text() !== before, 'page updates after a spoken yes')
  ok(text().includes('ஆம்'), 'follow-up answered')

  // ---- back to chilli by voice, confident, then go to spray planning ----
  type(input(), 'மிளகாய் இலையில் வெள்ளை பவுடர் இருக்கு'); btn(/அனுப்பு/).click()
  await until(() => text().includes('Likely: Chilli powdery mildew'), 'chilli powdery again')
  btn(/Next: find a spray/).click()
  await until(() => text().includes('Step 3. Choose and log the spray') && $$('.opt').length > 0, 'spray options for powdery mildew')
  const best = $('.opt.best'); ok(!!best && /Wait \d+ days/.test(best.textContent), 'best fit option with waiting days and date')
  ok($$('.opt').every((o) => !/Carbendazim.*mode of action as your last/.test(o.textContent)), 'no stale rotation conflict on a fresh field')

  // ---- step 2: verify demo packs ----
  $$('.journey button')[1].click(); await until(() => $$('.demo button').length === 7, 'demo codes')
  const demo = (k) => $$('.demo button.' + k)[0]
  demo('forged').click(); await until(() => text().includes('The signature does not match'), 'forged code rejected'); ok(!!btn(/Check this pack/), 'forged: no "use this pack" button'); ok(!btn(/Use this pack/), 'forged: cannot continue')
  demo('cloned').click(); await until(() => text().includes('Possible cloned code'), 'cloned code flagged')
  demo('expired').click(); await until(() => text().includes('This pack has expired'), 'expired rejected')
  $$('.demo button.genuine').find((b) => b.textContent.includes('azoxystrobin')).click()
  await until(() => text().includes('Genuine pack') && btn(/Use this pack/), 'genuine azoxystrobin pack'); ok($$('.checks li').length === 5, 'five verification checks shown')
  btn(/Use this pack/).click()

  // ---- step 3 -> log -> step 4 ----
  await until(() => $$('.opt').some((o) => o.textContent.includes('Your checked pack')), 'planner marks the verified pack')
  btn(/I sprayed this: log it/).click()
  await until(() => text().includes('Step 4. Your harvest passport') && $('.pass'), 'passport after logging')
  ok(/WAIT 5 MORE DAYS/.test(text()), 'azoxystrobin on chilli: label wait of 5 days shown')
  ok(text().includes('EU limit: 3 mg/kg') || text().includes('EU limit: 3.0 mg/kg') || /EU limit/.test(text()), 'EU limit note shown')
  btn(/Create a link for my buyer/).click(); const a = await until(() => $('.pass a[href*="/p/"]'), 'share link'); ok(!!$('.pass img[alt^="QR"]'), 'QR code for the link')
  const pub = await (await fetch(BASE + '/api/public/passport/' + a.getAttribute('href').split('/').pop())).json()
  ok(JSON.parse(pub.payload).groups[0].sprays.length === 1, 'public passport has the logged spray')

  // ---- photo sample path through the real model ----
  $$('.journey button')[0].click(); $$('.thumbs button')[2].click()          // tea brown blight sample
  await until(() => $$('.chips .chip').length >= 8 && text().includes('Tea brown blight'), 'photo analysed, measurements shown', 12000)
  ok(!!$('#pvimg'), 'photo preview shown'); ok($$('.br').length === 6, 'six tea classes scored')

  // ---- sign out returns to the welcome page ----
  btn(/Sign out/).click(); await until(() => text().includes('Know it is safe to harvest'), 'signed out'); ok(!$('.journey'), 'app hidden after sign out')
  ok(errors.length === 0, 'no JavaScript or React errors' + (errors.length ? ': ' + errors[0] : ''))
  console.log('\nE2E PASSED', n, 'checks'); process.exit(0)
})().catch((e) => { console.log('\nE2E FAILED:', e.message); if (errors.length) console.log('console errors:', errors.slice(0, 3)); process.exit(1) })
