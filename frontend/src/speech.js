// Browser voice features: speech recognition (microphone to text) and speech synthesis (text to speech).
import { useEffect, useState } from 'react'

const SR = () => (typeof window !== 'undefined' ? window.SpeechRecognition || window.webkitSpeechRecognition : null)
export const recognitionSupported = () => !!SR()
export const synthSupported = () => typeof window !== 'undefined' && 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window
export const secureContext = () => typeof window === 'undefined' || window.isSecureContext !== false

const norm = (l) => (l || '').toLowerCase().replace('_', '-')
export const hasVoice = (voices, prefix) => voices.some((v) => norm(v.lang).startsWith(prefix))
export const pickVoice = (voices, prefix) => voices.find((v) => norm(v.lang).startsWith(prefix + '-in')) || voices.find((v) => norm(v.lang).startsWith(prefix))

// Voices load asynchronously in most browsers.
export function useVoices() {
  const [voices, setVoices] = useState(() => (synthSupported() ? window.speechSynthesis.getVoices() : []))
  useEffect(() => {
    if (!synthSupported()) return undefined
    const update = () => setVoices(window.speechSynthesis.getVoices())
    update()
    window.speechSynthesis.addEventListener?.('voiceschanged', update)
    const t = setTimeout(update, 1000)
    return () => { window.speechSynthesis?.removeEventListener?.('voiceschanged', update); clearTimeout(t) }
  }, [])
  return voices
}

// Some browsers stop reading long text after about 15 seconds, so read it one sentence at a time.
export function chunk(text, max = 170) {
  const sentences = (text.replace(/\s+/g, ' ').trim().match(/[^.?!]+[.?!]*/g) || []).map((s) => s.trim()).filter(Boolean)
  const out = []
  for (const s of sentences) {
    if (s.length <= max) { out.push(s); continue }
    let cur = ''
    for (const w of s.split(' ')) {
      if ((cur + ' ' + w).trim().length > max) { out.push(cur.trim()); cur = w } else cur += ' ' + w
    }
    if (cur.trim()) out.push(cur.trim())
  }
  return out
}

export function stopSpeaking() {
  if (synthSupported()) window.speechSynthesis.cancel()
}

export function speak(text, { lang, voice, onEnd, onError } = {}) {
  if (!synthSupported()) { onError?.('unsupported'); return }
  window.speechSynthesis.cancel()
  const parts = chunk(text)
  if (!parts.length) { onEnd?.(); return }
  let done = 0
  parts.forEach((t) => {
    const u = new window.SpeechSynthesisUtterance(t)
    u.lang = lang
    if (voice) u.voice = voice
    u.rate = 0.9
    u.onend = () => { done += 1; if (done === parts.length) onEnd?.() }
    u.onerror = (e) => { if (e?.error !== 'interrupted' && e?.error !== 'canceled') onError?.(e?.error || 'error') }
    window.speechSynthesis.speak(u)
  })
}

export const RECOGNITION_ERRORS = {
  'not-allowed': 'The microphone is blocked. Allow microphone access for this site in the browser settings, then try again.',
  'service-not-allowed': 'The microphone is blocked. Allow microphone access for this site in the browser settings, then try again.',
  'no-speech': 'I did not hear anything. Tap the microphone, then speak close to the phone.',
  'audio-capture': 'No microphone was found on this device.',
  network: 'Voice recognition needs an internet connection.',
  'language-not-supported': 'This language is not supported for voice input on this device. Try English, or type instead.',
}

// One listening session. onEnd receives the final text (empty if nothing was heard).
export function createRecognizer({ lang, onInterim, onError, onEnd }) {
  const Ctor = SR()
  const r = new Ctor()
  r.lang = lang
  r.interimResults = true
  r.continuous = false
  r.maxAlternatives = 1
  let finalText = ''
  let errored = false
  r.onresult = (e) => {
    let interim = ''
    for (let i = e.resultIndex; i < e.results.length; i += 1) {
      const t = e.results[i][0].transcript
      if (e.results[i].isFinal) finalText += t; else interim += t
    }
    onInterim?.((finalText + interim).trim())
  }
  r.onerror = (e) => { if (e.error !== 'aborted') { errored = true; onError?.(e.error) } }
  r.onend = () => onEnd?.(finalText.trim(), errored)
  return { start: () => r.start(), stop: () => r.stop(), abort: () => r.abort() }
}
