import { notifications } from '@mantine/notifications'
import { useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'

import { Button } from '../../../components/Button'
import { Card } from '../../../components/Card'
import View from '../../../components/View'
import { useUnits } from '../../../contexts/UnitsProvider'
import { useFetch } from '../../../hooks/fetcher'
import { performPost } from '../../../hooks/fetcher/http'
import { useCommonStyles } from '../../../styles/common'
import { type IngredientListOutAPIResponse } from '../../../types'
import { urls } from '../../urls'
import {
  type FormError,
  type Ingredient,
  type IngredientGroup,
  RecipeIngredientsForm,
} from '../forms/RecipeIngredientsForm'
import { routes } from '../routes'

import { Header } from './components/Header'

interface RecipeIngredientsCreateInnerProps {
  results: {
    ingredients: IngredientListOutAPIResponse
  }
  recipeId: string | number
}

function RecipeIngredientsCreateInner({ recipeId, results }: RecipeIngredientsCreateInnerProps) {
  const { classes } = useCommonStyles()
  const { unitsOptions } = useUnits()
  const navigate = useNavigate()

  /**********
   ** Data **
   **********/

  const { data: ingredients } = results.ingredients
  const defaultIngredient = { ingredient: '', portionQuantity: '', unit: '', additionalInfo: '' }
  const defaultIngredientGroup = { title: '', order: '', ingredients: [defaultIngredient] }
  const [ingredientGroups, setIngredientGroups] = useState<IngredientGroup[]>([
    defaultIngredientGroup,
  ])

  const ingredientOptions = useMemo(
    () =>
      ingredients &&
      ingredients.map((ingredient) => ({
        label: ingredient.title,
        image: ingredient.product.thumbnailUrl,
        description: ingredient.product.fullName,
        value: ingredient.id.toString(),
      })),
    [ingredients]
  )

  /************
   ** Errors **
   ************/

  const [ingredientErrors, setIngredientErrors] = useState<FormError[]>([])
  const [ingredientGroupErrors, setIngredientGroupErrors] = useState<FormError[]>([])

  const resetErrors = () => {
    if (ingredientGroupErrors.length) {
      setIngredientGroupErrors([])
    }

    if (ingredientErrors.length) {
      setIngredientErrors([])
    }
  }

  /*******************************
   ** IngredientGroup: handlers **
   *******************************/

  const handleIngredientGroupInputAdd = () => {
    const ingredientGroupsData = [...ingredientGroups]
    setIngredientGroups([...ingredientGroupsData, defaultIngredientGroup])
    resetErrors()
  }

  const handleIngredientGroupInputChange = (index: number, data: IngredientGroup) => {
    const ingredientGroupsData = [...ingredientGroups]
    ingredientGroupsData[index] = data
    setIngredientGroups(ingredientGroupsData)
    resetErrors()
  }

  const handleIngredientGroupInputDelete = (index: number) => {
    const ingredientGroupsData = [...ingredientGroups]
    ingredientGroupsData.splice(index, 1)
    setIngredientGroups(ingredientGroupsData)
    resetErrors()
  }

  const handleSequenceChange = (data: IngredientGroup[]) => {
    setIngredientGroups([...data])
  }

  /**************************
   ** Ingredient: handlers **
   **************************/

  const handleIngredientInputAdd = (index: number) => {
    const ingredientGroupsData = [...ingredientGroups]
    const ingredientGroup = ingredientGroupsData[index]

    ingredientGroup.ingredients = [...ingredientGroup.ingredients, defaultIngredient]
    setIngredientGroups(ingredientGroupsData)
    resetErrors()
  }

  const handleIngredientInputChange = (
    index: number,
    ingredientIndex: number,
    data: Ingredient
  ) => {
    const ingredientGroupsData = [...ingredientGroups]
    const ingredientGroup = ingredientGroupsData[index]

    ingredientGroup.ingredients[ingredientIndex] = data
    setIngredientGroups(ingredientGroupsData)
    resetErrors()
  }

  const handleIngredientInputDelete = (index: number, ingredientIndex: number) => {
    const ingredientGroupsData = [...ingredientGroups]
    const ingredientGroup = ingredientGroupsData[index]
    const ingredientsData = [...ingredientGroup.ingredients]

    ingredientsData.splice(ingredientIndex, 1)
    ingredientGroup.ingredients = ingredientsData

    setIngredientGroups(ingredientGroupsData)
    resetErrors()
  }

  /****************
   ** Validators **
   ****************/

  const validate = () => {
    const ingredientGroupErrorsData = ingredientGroups
      .filter((ingredientGroup) => ingredientGroup.title === '')
      .map((group) => ({
        index: ingredientGroups.indexOf(group),
        message: 'This field cannot be empty. If group is redundant, please remove it.',
      }))

    const ingredientErrorsData = ingredientGroups.flatMap((ingredientGroup) =>
      ingredientGroup.ingredients.flatMap((ingredient) =>
        Object.values(ingredient)
          .filter((val) => val === '')
          .map(() => ({
            index: ingredientGroup.ingredients.indexOf(ingredient),
            message:
              'None of these fields can be empty. If ingredient is redundant, please remove it.',
          }))
      )
    )

    setIngredientErrors(ingredientErrorsData)
    setIngredientGroupErrors(ingredientGroupErrorsData)
  }

  /********************
   ** Submit handler **
   ********************/

  const addIngredients = async () => {
    validate()

    if (!ingredientErrors.length && !ingredientGroupErrors.length) {
      const payload = ingredientGroups.map((ingredientGroup, index) => ({
        ...ingredientGroup,
        ordering: index + 1,
      }))

      try {
        await performPost({
          url: urls.recipes.ingredients.groups.create({ id: recipeId }),
          data: payload,
        })
        notifications.show({
          color: 'green',
          title: 'Ingredient groups created',
          message: 'Ingredient groups and ingredients was successfully saved.',
        })
        navigate(routes.createRecipeIngredients.build({ recipeId }))
      } catch (e) {
        console.log(e)
      }
    }
  }

  return (
    <div className="space-y-10">
      <Header title="Add ingredients for recipe" />
      <Card>
        <Card.Form
          title="Add ingredients"
          subtitle="Add ingredients and amounts to recipe. If one ingredient is needed within multiple groups, add it to each group respectively."
          form={
            <RecipeIngredientsForm
              ingredientGroups={ingredientGroups}
              ingredientErrors={ingredientErrors}
              ingredientGroupsErrors={ingredientGroupErrors}
              units={unitsOptions || []}
              ingredientOptions={ingredientOptions || []}
              onSequenceChange={handleSequenceChange}
              onIngredientInputAdd={handleIngredientInputAdd}
              onIngredientInputChange={handleIngredientInputChange}
              onIngredientInputDelete={handleIngredientInputDelete}
              onIngredientGroupInputAdd={handleIngredientGroupInputAdd}
              onIngredientGroupInputChange={handleIngredientGroupInputChange}
              onIngredientGroupInputDelete={handleIngredientGroupInputDelete}
            />
          }
        />
        <div className={`flex space-x-3 justify-end py-4 border-t ${classes.border}`}>
          <Button variant="default">Cancel</Button>
          <Button onClick={() => addIngredients()}>Continue</Button>
        </div>
      </Card>
    </div>
  )
}

function RecipeIngredientsCreate() {
  const { recipeId } = useParams()
  invariant(recipeId)

  const ingredients = useFetch<IngredientListOutAPIResponse>(urls.recipes.ingredients.list())

  return (
    <View<object, RecipeIngredientsCreateInnerProps>
      results={{ ingredients }}
      component={RecipeIngredientsCreateInner}
      componentProps={{ recipeId }}
      loadingProps={{ description: 'Loading ingredients' }}
      errorProps={{ description: 'There was an error loading ingredients, please try again.' }}
    />
  )
}

export { RecipeIngredientsCreate }
