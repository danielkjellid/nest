import { useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { diff, addedDiff, deletedDiff, updatedDiff, detailedDiff } from 'deep-object-diff'

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

  const isEmpty = (o: any) => Object.keys(o).length === 0
  const isObject = (o: any) => o != null && typeof o === 'object' && !Array.isArray(o)
  const isArray = (o: any) => o != null && Array.isArray(o)

  const isEqual = (newValue: any, oldValue: any) => {
    if (isArray(newValue) && isArray(oldValue)) {
      let isEqualValues = true
      newValue.forEach((newVal: any) =>
        oldValue.forEach((oldVal: any) => {
          if (!isEqualValues) {
            // Already esthablised that current array is not equal, no point in checking the rest
            return
          }
          // console.log('Recursive iteration')
          if (!isEqual(newVal, oldVal)) {
            isEqualValues = false
          }
        })
      )
      return isEqualValues
    } else if (isObject(newValue) && isObject(oldValue)) {
      return JSON.stringify(newValue) === JSON.stringify(oldValue)
    } else if (newValue !== undefined && oldValue !== undefined) {
      return newValue === oldValue
    }
  }

  const getObjectDifference = (oldObj: Record<string, any>, newObj: Record<string, any>) => {
    let difference = {}

    if (isEmpty(newObj) || isEmpty(oldObj) || !isObject(oldObj) || !isObject(newObj)) {
      return difference
    }

    const newKeys = Object.keys(newObj)

    for (const key of newKeys) {
      if (oldObj[key] !== undefined) {
        if (isObject(newObj[key])) {
          const differenceForKey = getObjectDifference(oldObj[key], newObj[key])
          if (differenceForKey && Object.keys(differenceForKey).length) {
            difference = { [key]: getObjectDifference(oldObj[key], newObj[key]), ...difference }
            continue
          }
        } else if (isArray(oldObj[key]) && isArray(newObj[key])) {
          // Filter out changes made.
          const updates: any[] = []
          newObj[key].flatMap((unpackedNewObj: any) =>
            Object.keys(unpackedNewObj).flatMap((k) =>
              oldObj[key].flatMap((unpackedOldObj: any) => {
                const existingUpdateIndex = updates.indexOf(unpackedNewObj)
                if (!isEqual(unpackedNewObj[k], unpackedOldObj[k])) {
                  if (existingUpdateIndex === -1) {
                    updates.push(unpackedNewObj)
                  } else {
                    updates[existingUpdateIndex] = unpackedNewObj
                  }
                }
              })
            )
          )

          if (updates.length) {
            difference = { [key]: [...updates], ...difference }
          }
        } else if (newObj[key] != oldObj[key] && !isArray(oldObj[key]) && !isArray(newObj[key])) {
          difference = { [key]: newObj[key], ...difference }
        }
      } else {
        console.warn(`Unknown key passed to diff, skipping. Key: ${key}`)
      }
    }

    return difference
  }

  const editRecipe = (recipeData: Recipe) => {
    const flattenedRecipeData = {
      ...recipeData.baseRecipe,
      ingredientItemGroups: [...recipeData.ingredientItemGroups],
      steps: [...recipeData.steps.flatMap((step) => ({ ...step, duration: step.duration * 60 }))],
    }
    console.log(getObjectDifference(recipe, flattenedRecipeData))
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
