import { Route, Routes } from 'react-router-dom'

import { useStrippedRoute } from '../../hooks/route'

import { IngredientsOverview } from './overview'
import { routes } from './routes'

export function IngredientsApp() {
  const baseRoute = useStrippedRoute('/ingredients')

  return (
    <Routes>
      <Route path={baseRoute(routes.overview.path)} element={<IngredientsOverview />} />
    </Routes>
  )
}
