// eslint-disable-next-line
import 'vite/modulepreload-polyfill'
import '../../assets/index.css'

import React from 'react'
import { createRoot } from 'react-dom/client'

import App from './App'

createRoot(document.getElementById('root') as HTMLElement).render(<App />)
