// eslint-disable-next-line
import 'vite/modulepreload-polyfill'
import './assets/index.css'

import { createRoot } from 'react-dom/client'

import App from './Main'

createRoot(document.getElementById('root') as HTMLElement).render(<App {...window.initialProps} />)
