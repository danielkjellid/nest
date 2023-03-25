import React from 'react'
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

  return <p>Front</p>
}

export default App
