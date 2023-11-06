import { Suspense, useState } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

import BaseApp from '../../components/BaseApp/BaseApp'
import Header from '../../components/Header'
import { type CommonContextType, CommonProvider } from '../../contexts/CommonProvider'

import { RecipeDetail } from './detail'
import { routes } from './routes'

function RecipeAppInner() {
  return (
    <Suspense fallback={<div />}>
      <Routes>
        <Route path={routes.detail.path} element={<RecipeDetail />} />
      </Routes>
    </Suspense>
  )
}

function RecipeApp(props: CommonContextType) {
  const { currentUser, availableHomes, config } = props
  let home: CommonContextType['currentHome']

  if (currentUser) {
    if (currentUser.home) {
      home = currentUser.home
    } else if (!currentUser.home && availableHomes.length) {
      home = availableHomes.sort((a, b) => a.id - b.id)[0]
    } else {
      home = null
    }
  } else {
    home = null
  }

  const [currentHome, setCurrentHome] = useState<CommonContextType['currentHome']>(home)

  return (
    <CommonProvider
      config={config}
      currentUser={currentUser}
      currentHome={currentHome}
      availableHomes={availableHomes}
      setCurrentHome={setCurrentHome}
    >
      <BrowserRouter>
        <BaseApp header={<Header />}>
          <RecipeAppInner />
        </BaseApp>
      </BrowserRouter>
    </CommonProvider>
  )
}

export { RecipeApp }
