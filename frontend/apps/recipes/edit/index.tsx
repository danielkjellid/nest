import { notifications } from '@mantine/notifications'
import { useNavigate, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'

import View from '../../../components/View'
import { useFetch } from '../../../hooks/fetcher'
import { performPut } from '../../../hooks/fetcher/http'
import {
  type RecipeDetailRecordAPIResponse,
  type RecipeIngredientRecordListAPIResponse,
} from '../../../types'
import { urls } from '../../urls'
import { type Recipe, RecipeForm, makePayload } from '../components/RecipeForm'
import { routes } from '../routes'

interface RecipeEditInnerProps {
  recipeId: string
  results: {
    recipe: RecipeDetailRecordAPIResponse
    ingredients: RecipeIngredientRecordListAPIResponse
  }
}

function RecipeEditInner({ recipeId, results }: RecipeEditInnerProps) {
  const { data: ingredients } = results.ingredients
  const { data: recipe } = results.recipe
  const navigate = useNavigate()

  const editRecipe = async (recipeData: Recipe) => {
    const payload = makePayload(recipeData)
    console.log(payload)
    try {
      await performPut({ url: urls.recipes.edit({ id: recipeId }), data: payload })
      notifications.show({
        color: 'green',
        title: 'Recipe updated',
        message: 'Recipe was successfully updated.',
      })
      navigate(routes.overview.build())
    } catch (e) {
      console.log(e)
    }
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
      componentProps={{ recipeId: recipeId }}
      loadingProps={{ description: 'Loading' }}
      errorProps={{ description: 'There was an error loading, please try again.' }}
    />
  )
}

export { RecipeEdit }
