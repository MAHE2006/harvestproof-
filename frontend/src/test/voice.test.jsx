import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import Voice from '../components/Voice'
import { chunk } from '../speech'

// ---- fakes for the browser's microphone and speaker ----
class FakeRecognition {
  static last = null
  constructor() { FakeRecognition.last = this; this.started = false }
  start() { this.started = true }
  stop() { this.onend?.() }
  abort() { this.aborted = true }
  say(text) { this.onresult?.({ resultIndex: 0, results: [Object.assign([{ transcript: text }], { isFinal: true })] }); this.onend?.() }
  fail(error) { this.onerror?.({ error }); this.onend?.() }
}
const spoken = []
class FakeUtterance { constructor(text) { this.text = text } }
const makeSynth = (voices) => ({
  getVoices: () => voices, cancel: vi.fn(), addEventListener: vi.fn(), removeEventListener: vi.fn(),
  speak: (u) => { spoken.push({ text: u.text, lang: u.lang }); setTimeout(() => u.onend?.(), 0) },
})
const TA = [{ lang: 'ta-IN', name: 'Tamil' }, { lang: 'en-IN', name: 'English' }]

const reply = (over = {}) => ({
  crop: 'chilli', crop_name: { ta: 'மிளகாய்', en: 'Chilli' }, status: 'confident', transcript: 'x', answers: { white_powder: true },
  heard: [{ q: 'white_powder', value: true, ta: 'வெள்ளைத் தூள்: ஆம்', en: 'white powder: yes' }], pending: null, options: [{ code: 'A', product: 'Azoxystrobin 23% SC', wait: 5, dose: '500 ml/ha' }],
  diagnosis: { verdict: { id: 'chilli_powdery', p: 0.92 } }, reply: { ta: 'மிளகாய் சாம்பல் நோய் போல் தெரிகிறது. உறுதி 92 சதவீதம்.', en: 'This looks like chilli powdery mildew. 92% sure.', status: 'confident' }, ...over,
})

let fetchMock
beforeEach(() => {
  spoken.length = 0
  window.SpeechRecognition = FakeRecognition
  window.SpeechSynthesisUtterance = FakeUtterance
  window.speechSynthesis = makeSynth(TA)
  fetchMock = vi.fn(async () => ({ ok: true, status: 200, json: async () => reply() }))
  globalThis.fetch = fetchMock
})

const setup = (props = {}) => {
  const onResult = vi.fn()
  render(<Voice crop="chilli" answers={{}} features={null} pending={null} onResult={onResult} onSeeOptions={() => {}} {...props} />)
  return onResult
}
const body = () => JSON.parse(fetchMock.mock.calls.at(-1)[1].body)

describe('Voice panel', () => {
  it('listens, sends the transcript, shows the Tamil reply and reads it aloud in Tamil', async () => {
    const onResult = setup()
    fireEvent.click(screen.getByRole('button', { name: /start speaking/i }))
    expect(FakeRecognition.last.started).toBe(true)
    expect(FakeRecognition.last.lang).toBe('ta-IN')
    await act(async () => FakeRecognition.last.say('My chilli leaves have white powder'))
    await waitFor(() => expect(onResult).toHaveBeenCalled())
    expect(body()).toMatchObject({ text: 'My chilli leaves have white powder', lang: 'ta', crop: 'chilli' })
    expect(await screen.findByText(/மிளகாய் சாம்பல் நோய் போல் தெரிகிறது/)).toBeTruthy()
    expect(screen.getByText(/வெள்ளைத் தூள்: ஆம்/)).toBeTruthy()
    await waitFor(() => expect(spoken.length).toBeGreaterThan(0))
    expect(spoken.every((s) => s.lang === 'ta-IN')).toBe(true)
    expect(spoken.map((s) => s.text).join(' ')).toContain('உறுதி 92 சதவீதம்')
  })

  it('uses the chosen speaking language', async () => {
    setup()
    fireEvent.change(screen.getByLabelText(/speaking language/i), { target: { value: 'en-IN' } })
    fireEvent.click(screen.getByRole('button', { name: /start speaking/i }))
    expect(FakeRecognition.last.lang).toBe('en-IN')
    await act(async () => FakeRecognition.last.say('hello'))
    await waitFor(() => expect(body().lang).toBe('en'))
  })

  it('sends typed text, with the current answers and the pending question', async () => {
    setup({ answers: { rings: false }, pending: 'curl' })
    fireEvent.change(screen.getByPlaceholderText('…'), { target: { value: 'இல்லை' } })
    fireEvent.click(screen.getByRole('button', { name: /send/i }))
    await waitFor(() => expect(fetchMock).toHaveBeenCalled())
    expect(body()).toMatchObject({ text: 'இல்லை', answers: { rings: false }, pending: 'curl' })
  })

  it('quick yes / no / not sure buttons send the Tamil words for the pending question', async () => {
    fetchMock.mockImplementation(async () => ({ ok: true, status: 200, json: async () => reply({ status: 'asking', pending: 'curl', options: [], reply: { ta: 'இலைகள் சுருண்டோ?', en: 'Curled?', status: 'asking' } }) }))
    setup()
    fireEvent.change(screen.getByPlaceholderText('…'), { target: { value: 'chilli' } })
    fireEvent.click(screen.getByRole('button', { name: /send/i }))
    for (const [label, word] of [[/ஆம் · Yes/, 'ஆம்'], [/இல்லை · No/, 'இல்லை'], [/தெரியவில்லை · Not sure/, 'தெரியவில்லை']]) {
      fireEvent.click(await screen.findByRole('button', { name: label }))
      await waitFor(() => expect(body().text).toBe(word))
    }
  })

  it('does not speak Tamil when the phone has no Tamil voice, and says why', async () => {
    window.speechSynthesis = makeSynth([{ lang: 'en-US', name: 'English' }])
    setup()
    fireEvent.change(screen.getByPlaceholderText('…'), { target: { value: 'chilli white powder' } })
    fireEvent.click(screen.getByRole('button', { name: /send/i }))
    expect(await screen.findByText(/மிளகாய் சாம்பல் நோய் போல் தெரிகிறது/)).toBeTruthy()
    expect(screen.getAllByText(/No Tamil voice was found/i).length).toBeGreaterThan(0)
    expect(spoken).toHaveLength(0)
  })

  it('shows clear messages for microphone problems', async () => {
    setup()
    fireEvent.click(screen.getByRole('button', { name: /start speaking/i }))
    await act(async () => FakeRecognition.last.fail('not-allowed'))
    expect(await screen.findByText(/microphone is blocked/i)).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: /start speaking/i }))
    await act(async () => FakeRecognition.last.stop())
    expect(await screen.findByText(/did not hear anything/i)).toBeTruthy()
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('works by typing when the browser has no speech recognition', () => {
    delete window.SpeechRecognition
    setup()
    expect(screen.getByText(/Voice input is not available in this browser/i)).toBeTruthy()
    expect(screen.getByRole('button', { name: /start speaking/i }).disabled).toBe(true)
    fireEvent.change(screen.getByPlaceholderText('…'), { target: { value: 'tea' } })
    expect(screen.getByRole('button', { name: /send/i }).disabled).toBe(false)
  })

  it('shows server errors instead of failing silently', async () => {
    fetchMock.mockImplementation(async () => ({ ok: false, status: 429, json: async () => ({}) }))
    setup()
    fireEvent.change(screen.getByPlaceholderText('…'), { target: { value: 'tea' } })
    fireEvent.click(screen.getByRole('button', { name: /send/i }))
    expect(await screen.findByText(/Too many requests/i)).toBeTruthy()
  })

  it('refuses an empty message and does not call the server', () => {
    setup()
    expect(screen.getByRole('button', { name: /send/i }).disabled).toBe(true)
    expect(fetchMock).not.toHaveBeenCalled()
  })
})

describe('reading long answers', () => {
  it('splits text into short sentences so browsers do not cut it off', () => {
    const long = 'அரசு பட்டியலில் இந்த நோய்க்கு 12 மருந்துகள் உள்ளன. திரையில் பட்டியலைப் பார்த்து, பேக் குறியீட்டைச் சரிபார்த்து, லேபிளில் உள்ள அளவையும் காத்திருப்பு நாட்களையும் பின்பற்றவும். இது ஆலோசனை மட்டுமே.'
    const parts = chunk(long)
    expect(parts).toHaveLength(3)
    expect(parts.join(' ')).toBe(long)
    expect(chunk('a '.repeat(200)).every((p) => p.length <= 170)).toBe(true)
    expect(chunk('')).toEqual([])
  })
})
