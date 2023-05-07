import { Route, Routes } from 'react-router-dom'

import { ProductDetail } from './detail'
import { ProductOverview } from './overview'
import React from 'react'
import { routes } from './routes'
import { useStrippedRoute } from '../../hooks/route'

export function ProductsApp() {
  const baseRoute = useStrippedRoute('/products')
  return (
    <Routes>
      <Route path={baseRoute(routes.overview.path)} element={<ProductOverview />} />
      <Route path={baseRoute(routes.detail.path)} element={<ProductDetail />} />
    </Routes>
  )
}
