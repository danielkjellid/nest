import { useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'

import View from '../../../components/View'
import { useFetch } from '../../../hooks/fetcher'
import {
  type RecipeDetailRecordAPIResponse,
  type RecipeIngredientRecordListAPIResponse,
} from '../../../types'
import { urls } from '../../urls'
import { type Recipe, RecipeForm } from '../components/RecipeForm'

interface RecipeEditInnerProps {
  results: {
    recipe: RecipeDetailRecordAPIResponse
    ingredients: RecipeIngredientRecordListAPIResponse
  }
}

function RecipeEditInner({ results }: RecipeEditInnerProps) {
  const { data: ingredients } = results.ingredients
  const { data: recipe } = results.recipe

  const editRecipe = (recipeData: Recipe) => {
    //
  }

  return <RecipeForm recipe={recipe} ingredients={ingredients || []} onSubmit={editRecipe} />
}

function RecipeEdit() {
  const { recipeId } = useParams()
  invariant(recipeId)

  const recipe = useFetch<RecipeDetailRecordAPIResponse>(urls.recipes.detail({ id: recipeId }))
  const ingredients = useFetch<RecipeIngredientRecordListAPIResponse>(
    urls.recipes.ingredients.list()
  )

  return (
    <View<object, RecipeEditInnerProps>
      results={{ recipe: recipe, ingredients: ingredients }}
      component={RecipeEditInner}
      componentProps={{}}
      loadingProps={{ description: 'Loading' }}
      errorProps={{ description: 'There was an error loading, please try again.' }}
    />
  )
}

export { RecipeEdit }
