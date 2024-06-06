import { notifications } from '@mantine/notifications'
import { useNavigate } from 'react-router-dom'

import View from '../../../components/View'
import { useFetch } from '../../../hooks/fetcher'
import { performPost } from '../../../hooks/fetcher/http'
import { type RecipeIngredientRecordListAPIResponse } from '../../../types'
import { urls } from '../../urls'
import { RecipeForm, makePayload, type Recipe } from '../components/RecipeForm'
import { routes } from '../routes'

interface RecipeCreateInnerProps {
  results: {
    ingredients: RecipeIngredientRecordListAPIResponse
  }
}

function RecipeCreateInner({ results }: RecipeCreateInnerProps) {
  const { data: ingredients } = results.ingredients
  const navigate = useNavigate()

  const addRecipe = async (recipeData: Recipe) => {
    const payload = makePayload(recipeData)

    try {
      await performPost({ url: urls.recipes.create(), data: payload })
      notifications.show({
        color: 'green',
        title: 'Recipe created',
        message: 'Recipe was successfully saved.',
      })
      navigate(routes.overview.build())
    } catch (e) {
      console.log(e)
    }
  }

  return (
    <RecipeForm ingredients={ingredients || []} onSubmit={(recipeData) => addRecipe(recipeData)} />
  )
}

function RecipeCreate() {
  const ingredients = useFetch<RecipeIngredientRecordListAPIResponse>(
    urls.recipes.ingredients.list()
  )

  return (
    <View<object, RecipeCreateInnerProps>
      results={{ ingredients: ingredients }}
      component={RecipeCreateInner}
      componentProps={{}}
      loadingProps={{ description: 'Loading' }}
      errorProps={{ description: 'There was an error loading, please try again.' }}
    />
  )
}

export { RecipeCreate }
