import { useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'

import View from '../../../components/View'
import { useFetch } from '../../../hooks/fetcher'
import {
  type RecipeDetailRecord,
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

  const isObject = (o: any) => o != null && typeof o === 'object' && !Array.isArray(o)
  const isArray = (o: any) => o != null && Array.isArray(o)

  function isEqual(newValue: any, oldValue: any) {
    if (
      Array.isArray(newValue) &&
      Array.isArray(oldValue) &&
      isArray(newValue) &&
      isArray(oldValue)
    ) {
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

  function getObjectDifference<A extends Record<string, any>, B extends Record<string, any>>(
    oldObj?: A,
    newObj?: B
  ) {
    let difference = {}

    if (oldObj === undefined || newObj === undefined || !isObject(oldObj) || !isObject(newObj)) {
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
          const updates: B[] = []
          newObj[key].flatMap((unpackedNewObj: B) =>
            Object.keys(unpackedNewObj).flatMap((k) =>
              oldObj[key].flatMap((unpackedOldObj: A) => {
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

  type Unpack<T> = {
    [K in keyof T]: T[K] extends object ? Unpack<T[K]> : T[K]
  }

  interface ModifiedRecipe extends Unpack<Recipe['baseRecipe']> {
    ingredientItemGroups: Recipe['ingredientItemGroups']
    steps: Recipe['steps']
  }

  const editRecipe = (recipeData: Recipe) => {
    const flattenedRecipeData: ModifiedRecipe = {
      ...recipeData.baseRecipe,
      ingredientItemGroups: [...recipeData.ingredientItemGroups],
      steps: [...recipeData.steps.flatMap((step) => ({ ...step, duration: step.duration * 60 }))],
    }
    const difference = getObjectDifference<RecipeDetailRecord, ModifiedRecipe>(
      recipe,
      flattenedRecipeData
    )
    console.log(difference)
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
