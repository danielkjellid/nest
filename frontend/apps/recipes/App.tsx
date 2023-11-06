import React from 'react'
import { Route, Routes } from 'react-router-dom'

import { useStrippedRoute } from '../../hooks/route'

import { RecipeCreate } from './create'
import { RecipeIngredientsCreate } from './create/CreateRecipeIngredients'
import { RecipeStepsCreate } from './create/CreateRecipeSteps'
import { RecipeOverview } from './overview'
import { routes } from './routes'

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
