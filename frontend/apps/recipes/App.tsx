import React from 'react'
import { Route, Routes } from 'react-router-dom'
import { RecipeOverview } from './overview'
import { RecipeIngredientsOverview } from './ingredients/overview'
import { routes } from './routes'
import { useStrippedRoute } from '../../hooks/route'

export function RecipesApp() {
  const baseRoute = useStrippedRoute('/recipes')

  return (
    <Routes>
      <Route path={baseRoute(routes.overview.path)} element={<RecipeOverview />} />
      <Route
        path={baseRoute(routes.ingredientsOverview.path)}
        element={<RecipeIngredientsOverview />}
      />
    </Routes>
  )
}
