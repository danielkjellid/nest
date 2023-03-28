// eslint-disable-next-line
import 'vite/modulepreload-polyfill'
import '../assets/index.css'

import App from './App'
import React from 'react'
import { createRoot } from 'react-dom/client'

createRoot(document.getElementById('root') as HTMLElement).render(<App {...window.initialProps} />)
