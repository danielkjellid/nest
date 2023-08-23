// eslint-disable-next-line
import 'vite/modulepreload-polyfill'
import '../../assets/index.css'

import React from 'react'
import { RecipeApp } from './App'
import { createRoot } from 'react-dom/client'

createRoot(document.getElementById('root') as HTMLElement).render(
  <RecipeApp {...window.initialProps} />
)
