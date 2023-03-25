// eslint-disable-next-line
import 'vite/modulepreload-polyfill'

import App from './App'
import React from 'react'
import { createRoot } from 'react-dom/client'
import '../../assets/index.css'

createRoot(document.getElementById('root') as HTMLElement).render(
  <App />
)