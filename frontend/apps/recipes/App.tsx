import { Route, Routes } from 'react-router-dom'

import { useStrippedRoute } from '../../hooks/route'

import { RecipeCreate } from './create'
import { RecipeEdit } from './edit'
import { RecipeOverview } from './overview'
import { routes } from './routes'

export function RecipesApp() {
  const baseRoute = useStrippedRoute('/recipes')

  return (
    <Routes>
      <Route path={baseRoute(routes.overview.path)} element={<RecipeOverview />} />
      <Route path={baseRoute(routes.create.path)} element={<RecipeCreate />} />
      <Route path={baseRoute(routes.edit.path)} element={<RecipeEdit />} />
    </Routes>
  )
}
