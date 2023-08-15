import React from 'react'
import { Route, Routes } from 'react-router-dom'
import { RecipeOverview } from './overview'
import { RecipeIngredientsOverview } from './ingredients/overview'
import { routes } from './routes'
import { useStrippedRoute } from '../../hooks/route'
import { RecipeCreate } from './createRecipe'
import { RecipeIngredientsCreate } from './createRecipe/CreateRecipeIngredients'
import { RecipeStepsCreate } from './createRecipe/CreateRecipeSteps'

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
      <Route
        path={baseRoute(routes.ingredientsOverview.path)}
        element={<RecipeIngredientsOverview />}
      />
    </Routes>
  )
}
