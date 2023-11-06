// eslint-disable-next-line
import 'vite/modulepreload-polyfill'
import '../../assets/index.css'

import React from 'react'
import { createRoot } from 'react-dom/client'

import { RecipeApp } from './App'

createRoot(document.getElementById('root') as HTMLElement).render(
  <RecipeApp {...window.initialProps} />
)
