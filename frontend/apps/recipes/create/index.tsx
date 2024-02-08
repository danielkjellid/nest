import { notifications } from '@mantine/notifications'
import { useNavigate } from 'react-router-dom'

import View from '../../../components/View'
import { useFetch } from '../../../hooks/fetcher'
import { performPost } from '../../../hooks/fetcher/http'
import {
  type RecipeIngredientRecordListAPIResponse,
  type RecipeCreateIn,
  type RecipeCreateIngredientItem,
} from '../../../types'
import { urls } from '../../urls'
import { RecipeForm, type Recipe, type IngredientItem } from '../components/RecipeForm'
import { routes } from '../routes'

interface RecipeCreateInnerProps {
  results: {
    ingredients: RecipeIngredientRecordListAPIResponse
  }
}

function RecipeCreateInner({ results }: RecipeCreateInnerProps) {
  const { data: ingredients } = results.ingredients
  const navigate = useNavigate()

  const makeIngredientItemType = (ingredientItem: IngredientItem): RecipeCreateIngredientItem => ({
    ingredient: ingredientItem.ingredient.id.toString(),
    portionQuantity: ingredientItem.portionQuantity.toString(),
    portionQuantityUnit: ingredientItem.portionQuantityUnit.id.toString(),
    additionalInfo: ingredientItem.additionalInfo || undefined,
  })

  const makePayload = (recipeData: Recipe): RecipeCreateIn => ({
    baseRecipe: { ...recipeData.baseRecipe },
    steps: [
      ...recipeData.steps.map((step, index) => ({
        instruction: step.instruction,
        stepType: step.stepType,
        duration: step.duration,
        number: index + 1,
        ingredientItems: step.ingredientItems.map((ingredientItem) =>
          makeIngredientItemType(ingredientItem)
        ),
      })),
    ],
    ingredientItemGroups: [
      ...recipeData.ingredientItemGroups.map((ingredientGroup) => ({
        title: ingredientGroup.title,
        ordering: ingredientGroup.ordering,
        ingredientItems: ingredientGroup.ingredientItems.map((ingredientItem) =>
          makeIngredientItemType(ingredientItem)
        ),
      })),
    ],
  })

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
