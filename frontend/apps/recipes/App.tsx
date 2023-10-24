import { Route, Routes } from 'react-router-dom'

import React from 'react'
import { RecipeCreate } from './create'
import { RecipeIngredientsCreate } from './create/CreateRecipeIngredients'
import { RecipeOverview } from './overview'
import { RecipeStepsCreate } from './create/CreateRecipeSteps'
import { routes } from './routes'
import { useStrippedRoute } from '../../hooks/route'

export function RecipesApp() {
  const baseRoute = useStrippedRoute('/recipes')

  return (
    <Routes>
      <Route path={baseRoute(routes.overview.path)} element={<RecipeOverview />} />
      <Route path={baseRoute(routes.createRecipe.path)} element={<RecipeCreate />} />
      <Route
        path={baseRoute(routes.createRecipeIngredients.path)}
        element={<RecipeIngredientsCreate />}
      />
      <Route path={baseRoute(routes.createRecipeSteps.path)} element={<RecipeStepsCreate />} />
    </Routes>
  )
}
