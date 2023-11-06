import React from 'react'
import { Route, Routes } from 'react-router-dom'

import { useStrippedRoute } from '../../hooks/route'

import { ProductDetail } from './detail'
import { ProductEdit } from './edit'
import { ProductOverview } from './overview'
import { routes } from './routes'


export function ProductsApp() {
  const baseRoute = useStrippedRoute('/products')

  return (
    <Routes>
      <Route path={baseRoute(routes.overview.path)} element={<ProductOverview />} />
      <Route path={baseRoute(routes.detail.path)} element={<ProductDetail />} />
      <Route path={baseRoute(routes.edit.path)} element={<ProductEdit />} />
    </Routes>
  )
}
