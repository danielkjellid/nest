import React, { Suspense, useEffect, useMemo, useState } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

import apps from './apps/config'
import { urls } from './apps/urls'
import BaseApp from './components/BaseApp/BaseApp'
import Header from './components/Header'
import Navbar from './components/Navbar'
import { type CommonContextType, CommonProvider } from './contexts/CommonProvider'
import { type MenuContextType, MenuProvider } from './contexts/MenuProvider'
import { UnitsProvider } from './contexts/UnitsProvider'
import { performGet } from './hooks/fetcher/http'
import { type UnitRecord, type UnitRecordListAPIResponse } from './types'

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

  const [units, setUnits] = useState<UnitRecord[]>()
  const [unitsOptions, setUnitsOptions] = useState<{ label: string; value: string }[]>()

  useEffect(() => {
    const fetchUnits = async () => {
      const fetchedUnits = await performGet<UnitRecordListAPIResponse>({ url: urls.units.list() })
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
