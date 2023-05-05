import { Route, Routes } from 'react-router-dom'

import { ProductsOverview } from './overview'
import React from 'react'
import { routes } from './routes'
import { useStrippedRoute } from '../../hooks/route'

export function ProductsApp() {
  const baseRoute = useStrippedRoute('/products')
  return (
    <Routes>
      <Route path={baseRoute(routes.overview.path)} element={<ProductsOverview />} />
    </Routes>
  )
}
