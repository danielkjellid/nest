import { Route, Routes } from 'react-router-dom'

import { IngredientsOverview } from './overview'
import React from 'react'
import { routes } from './routes'
import { useStrippedRoute } from '../../hooks/route'

export function IngredientsApp() {
  const baseRoute = useStrippedRoute('/ingredients')

  return (
    <Routes>
      <Route path={baseRoute(routes.overview.path)} element={<IngredientsOverview />} />
    </Routes>
  )
}
