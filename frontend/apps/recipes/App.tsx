import { Route, Routes } from 'react-router-dom'

import { useStrippedRoute } from '../../hooks/route'

import { RecipeCreate2 } from './create2'
import { RecipeOverview } from './overview'
import { routes } from './routes'

export function RecipesApp() {
  const baseRoute = useStrippedRoute('/recipes')

  return (
    <Routes>
      <Route path={baseRoute(routes.overview.path)} element={<RecipeOverview />} />
      <Route path={baseRoute(routes.createRecipe2.path)} element={<RecipeCreate2 />} />
    </Routes>
  )
}
