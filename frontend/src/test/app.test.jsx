import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'

const META = { classes: { tea_healthy: { crop: 'tea', name: 'Healthy tea leaf' } }, crops: ['tea', 'chilli'], photo_model: { trained_crops: ['tea', 'chilli'] }, demo: false }
const DX = { features: null, photo_used: false, photo_trained: true, note: '', photo_only: null, posterior: [{ id: 'tea_healthy', name: 'Healthy tea leaf', p: 1 }], next: null,
  verdict: { status: 'uncertain', id: null, p: 0.3, name: null }, answered: 0, accept: 0.8, reply: { ta: 'சோதனை', en: 'test', status: 'uncertain' } }
const json = (d, status = 200) => ({ ok: status < 400, status, json: async () => d })

describe('App', () => {
  beforeEach(() => { localStorage.clear(); vi.resetModules() })

  it('shows the welcome page when signed out, with the voice feature explained', async () => {
    const { default: App } = await import('../App')
    render(<App />)
    expect(screen.getByText(/Know it is safe to harvest/)).toBeTruthy()
    expect(screen.getAllByText(/speak in Tamil/i).length).toBeGreaterThan(0)
    expect(screen.getByRole('button', { name: /Start the demo/ })).toBeTruthy()
  })

  it('retries loading when the first attempt fails (Try again really works)', async () => {
    localStorage.setItem('hp_token', 't')
    const { default: App } = await import('../App')
    let metaCalls = 0
    globalThis.fetch = vi.fn(async (u) => {
      if (u === '/api/meta') { metaCalls += 1; if (metaCalls === 1) throw new Error('offline'); return json(META) }
      if (u === '/api/diagnose') return json(DX)
      return json({ groups: [] })
    })
    render(<App />)
    expect(await screen.findByText(/Cannot reach the server/)).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: /Try again/ }))
    expect(await screen.findByText('Check the leaf', { selector: 'b' })).toBeTruthy()
    expect(metaCalls).toBe(2)
  })

  it('signs the farmer out when the session expires', async () => {
    localStorage.setItem('hp_token', 'expired')
    const { default: App } = await import('../App')
    globalThis.fetch = vi.fn(async () => json({ detail: 'Sign in required' }, 401))
    render(<App />)
    await waitFor(() => expect(screen.getByText(/Know it is safe to harvest/)).toBeTruthy())
    expect(localStorage.getItem('hp_token')).toBeNull()
  })

  it('local-date helpers never use UTC', async () => {
    const { localDate, addDays, daysBetween, parseDate } = await import('../util')
    expect(localDate(new Date(2026, 0, 5, 0, 30))).toBe('2026-01-05')            // 00:30 local is still the 5th
    expect(localDate(new Date(2026, 0, 5, 23, 59))).toBe('2026-01-05')
    expect(addDays('2026-02-27', 3)).toBe('2026-03-02')
    expect(daysBetween('2026-03-30', '2026-03-28')).toBe(2)
    expect(daysBetween('2026-10-26', '2026-10-25')).toBe(1)                       // across a daylight-saving change in other zones
    expect(parseDate('2026-11-03').getDate()).toBe(3)
  })
})
