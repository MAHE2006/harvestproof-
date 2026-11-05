import { afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'

afterEach(() => cleanup())
if (!window.scrollTo || String(window.scrollTo).includes('not implemented')) window.scrollTo = () => {}
if (!globalThis.crypto?.getRandomValues) globalThis.crypto = require('node:crypto').webcrypto
