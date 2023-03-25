import { MantineProvider, createEmotionCache } from '@mantine/core'
import React, { useState } from 'react'
interface AppProps {
  test: number
}

declare global {
  interface Window {
    initialProps: AppProps
  }
}

function App(props: AppProps) {
  console.log(props)

  const emotionCache = createEmotionCache({ key: 'mantine', prepend: false })

  return (
    <MantineProvider emotionCache={emotionCache} theme={{ theme: 'dark' }}>
      <button className="bg-blue-800 py-4">Button</button>
    </MantineProvider>
  )
}

export default App
