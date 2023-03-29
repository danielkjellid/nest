import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { CommonContextType, CommonProvider } from './contexts/CommonProvider'
import { MenuContextType, MenuProvider } from './contexts/MenuProvider'
import React, { Suspense, useMemo, useState } from 'react'

import BaseApp from './components/BaseApp/BaseApp'
import Header from './components/Header'
import Navbar from './components/Navbar'
import apps from './apps/config'

interface AppProps extends CommonContextType, MenuContextType {}

declare global {
  interface Window {
    initialProps: AppProps
  }
}

function MainAppInner() {
  const reactRoutes = useMemo(() => {
    return apps.map(({ element, key, ...restProps }) => {
      const Component = React.lazy(element)
      return <Route key={key} {...restProps} element={<Component />} />
    })
  }, [])

  return (
    <Suspense fallback={<div />}>
      <Routes>{reactRoutes}</Routes>
    </Suspense>
  )
}

function MainApp(props: AppProps) {
  const { currentUser, availableHomes, config, menu } = props
  /**********
   ** Home **
   **********/

  let home: CommonContextType['currentHome']

  if (currentUser.home) {
    home = currentUser.home
  } else if (!currentUser.home && availableHomes.length) {
    home = availableHomes.sort((a, b) => a.id - b.id)[0]
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
      <MenuProvider menu={menu}>
        <BrowserRouter>
          <BaseApp navbar={<Navbar />} header={<Header />}>
            <MainAppInner />
          </BaseApp>
        </BrowserRouter>
      </MenuProvider>
    </CommonProvider>
  )
}

export default MainApp