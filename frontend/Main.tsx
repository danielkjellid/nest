import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { CommonContextType, CommonProvider } from './contexts/CommonProvider'
import { MenuContextType, MenuProvider } from './contexts/MenuProvider'
import React, { Suspense, useEffect, useMemo, useState } from 'react'
import { UnitListOut, UnitListOutAPIResponse } from './types'

import BaseApp from './components/BaseApp/BaseApp'
import Header from './components/Header'
import Navbar from './components/Navbar'
import { UnitsProvider } from './contexts/UnitsProvider'
import apps from './apps/config'
import { performGet } from './hooks/fetcher/http'
import { urls } from './apps/urls'

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

  const [units, setUnits] = useState<UnitListOut[]>()
  const [unitsOptions, setUnitsOptions] = useState<{ label: string; value: string }[]>()

  useEffect(() => {
    const fetchUnits = async () => {
      const fetchedUnits = await performGet<UnitListOutAPIResponse>({ url: urls.units.list() })
      if (fetchedUnits && fetchedUnits.data) {
        setUnits(fetchedUnits.data)
        setUnitsOptions(
          fetchedUnits.data.map((unit) => ({
            label: unit.displayName,
            value: unit.id.toString(),
          }))
        )
      }
    }
    if (!units) {
      fetchUnits()
    }
  }, [])

  return (
    <CommonProvider
      config={config}
      currentUser={currentUser}
      currentHome={currentHome}
      availableHomes={availableHomes}
      setCurrentHome={setCurrentHome}
    >
      <MenuProvider menu={menu}>
        <UnitsProvider units={units} unitsOptions={unitsOptions}>
          <BrowserRouter>
            <BaseApp navbar={<Navbar />} header={<Header />}>
              <MainAppInner />
            </BaseApp>
          </BrowserRouter>
        </UnitsProvider>
      </MenuProvider>
    </CommonProvider>
  )
}

export default MainApp
