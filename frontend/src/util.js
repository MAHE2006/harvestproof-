export const CROPS = { rice: ['🌾', 'Rice'], chilli: ['🌶️', 'Chilli'], grapes: ['🍇', 'Grapes'], tea: ['🍵', 'Tea'] }
export const cropName = (c) => CROPS[c]?.[1] || c
export const pc = (v) => Math.round(v * 100) + '%'

// Dates are handled in the farmer's local time, never UTC (UTC would be a day behind in the early morning in India).
export const localDate = (d = new Date()) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
export const parseDate = (s) => { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d) }
export const addDays = (s, n) => { const d = parseDate(s); d.setDate(d.getDate() + n); return localDate(d) }
export const daysBetween = (a, b) => Math.round((parseDate(a) - parseDate(b)) / 864e5)
export const fmt = (s) => parseDate(s).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' })

// crypto.randomUUID only exists on https/localhost, so use getRandomValues which works everywhere.
export const randomHex = (bytes = 16) => Array.from(crypto.getRandomValues(new Uint8Array(bytes)), (b) => b.toString(16).padStart(2, '0')).join('')

// Phone photos are 3 to 8 MB. Shrinking them before upload is much faster on a slow mobile network, and the
// server only analyses a 256 pixel version anyway. Falls back to the original file if anything is unavailable.
export async function shrinkImage(file, max = 1280) {
  try {
    if (typeof createImageBitmap !== 'function') return file
    const bmp = await createImageBitmap(file)
    const scale = Math.min(1, max / Math.max(bmp.width, bmp.height))
    if (scale === 1 && file.size < 1.5e6) return file
    const c = document.createElement('canvas')
    c.width = Math.max(1, Math.round(bmp.width * scale)); c.height = Math.max(1, Math.round(bmp.height * scale))
    c.getContext('2d').drawImage(bmp, 0, 0, c.width, c.height)
    const blob = await new Promise((res) => c.toBlob(res, 'image/jpeg', 0.9))
    return blob && blob.size < file.size ? blob : file
  } catch {
    return file
  }
}
