import React, { useEffect, useState } from 'react'
import { Route, Routes } from 'react-router-dom'
import { UnitListOut, UnitListOutAPIResponse } from '../../types'

import { ProductDetail } from './detail'
import { ProductOverview } from './overview'
import { UnitsProvider } from '../../contexts/UnitsProvider'
import { performGet } from '../../hooks/fetcher/http'
import { routes } from './routes'
import { urls } from '../urls'
import { useStrippedRoute } from '../../hooks/route'

export function ProductsApp() {
  const baseRoute = useStrippedRoute('/products')
  const [units, setUnits] = useState<UnitListOut[]>()

  useEffect(() => {
    const fetchUnits = async () => {
      const fetchedUnits = await performGet<UnitListOutAPIResponse>(urls.units.list())
      if (fetchedUnits && fetchedUnits.data) {
        setUnits(fetchedUnits.data)
      }
    }

    fetchUnits()
  }, [])

  return (
    <UnitsProvider units={units}>
      <Routes>
        <Route path={baseRoute(routes.overview.path)} element={<ProductOverview />} />
        <Route path={baseRoute(routes.detail.path)} element={<ProductDetail />} />
      </Routes>
    </UnitsProvider>
  )
}
