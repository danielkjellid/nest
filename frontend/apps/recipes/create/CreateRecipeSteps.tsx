import { notifications } from '@mantine/notifications'
import React, { useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'

import { Button } from '../../../components/Button'
import { Card } from '../../../components/Card'
import View from '../../../components/View'
import { useFetch } from '../../../hooks/fetcher'
import { performPost } from '../../../hooks/fetcher/http'
import { useCommonStyles } from '../../../styles/common'
import { type RecipeIngredientGroupsListOutAPIResponse } from '../../../types'
import { urls } from '../../urls'
import { RecipeStepsForm, type Step, type StepInputError } from '../forms/RecipeStepsForm'
import { routes } from '../routes'

import { Header } from './components/Header'

interface RecipeStepsCreateInnerProps {
  recipeId: string | number
  results: {
    ingredientGroups: RecipeIngredientGroupsListOutAPIResponse
  }
}

function RecipeStepsCreateInner({ recipeId, results }: RecipeStepsCreateInnerProps) {
  const { classes } = useCommonStyles()
  const navigate = useNavigate()

  /**********
   ** Data **
   **********/

  const { data: ingredientGroups } = results.ingredientGroups

  const defaultStep = {
    instruction: '',
    duration: 0,
    type: '',
    ingredientItems: [],
  }
  const [steps, setSteps] = useState<Step[]>([defaultStep])
  const selectedIngredientItems = steps.flatMap((step) => step.ingredientItems)

  // Get a list of available IngredientItem options. This incudes filtering out ingredients
  // "claimed" by other steps.
  const ingredientItemOptions = useMemo(
    () =>
      ingredientGroups?.flatMap((ingredientGroup) =>
        ingredientGroup.ingredientItems
          .filter(
            (ingredientItem) =>
              !selectedIngredientItems
                .map((selectedItem) => selectedItem.value)
                .includes(ingredientItem.id.toString())
          )
          .map((item) => ({
            label: item.ingredient.title,
            image: item.ingredient.product.thumbnailUrl,
            description: item.ingredient.product.fullName,
            value: item.id.toString(),
            group: ingredientGroup.title,
          }))
      ),
    [ingredientGroups, selectedIngredientItems]
  )

  /************
   ** Errors **
   ************/

  const [inputErrors, setInputErrors] = useState<StepInputError[]>()

  const clearErrorForIndex = ({ index }: { index: number }) => {
    if (inputErrors?.length) {
      const errorsData = [...inputErrors]
      const errorIndex = errorsData.findIndex((error) => error.index === index)

      if (errorIndex !== -1) {
        errorsData.splice(errorIndex, 1)
        setInputErrors(errorsData)
      }
    }
  }

  /**************
   ** Handlers **
   **************/

  const handleStepInputAdd = () => {
    const stepsData = [...steps]
    setSteps([...stepsData, defaultStep])
  }

  const handleStepInputChange = (index: number, data: Step) => {
    const stepsData = [...steps]
    stepsData[index] = data

    clearErrorForIndex({ index })
    setSteps(stepsData)
  }

  const handleStepInputDelete = (index: number) => {
    const stepsData = [...steps]
    stepsData.splice(index, 1)
    clearErrorForIndex({ index })
    setSteps(stepsData)
  }

  const handleSequenceChange = (data: Step[]) => {
    setSteps([...data])
  }

  /****************
   ** Validators **
   ****************/

  const validate = () => {
    const errors: StepInputError[] = []
    const unusedIngredientOptions = ingredientItemOptions?.filter((itemOption) =>
      steps.map((step) => step.ingredientItems.includes(itemOption))
    )

    steps.map((step, index) => {
      const error: StepInputError = {
        index: index,
        unusedIngredientOptions: !!unusedIngredientOptions?.length,
        durationBellowZero: false,
      }

      Object.keys(step).map((key) => {
        const stepKey = key as keyof Step
        if (step[stepKey] === '') {
          if (!error.emptyFields) {
            error.emptyFields = [stepKey]
          } else {
            error.emptyFields.push(stepKey)
          }
        }
      })

      if (step.duration <= 0) {
        error.durationBellowZero = true
      }

      if (
        unusedIngredientOptions?.length ||
        error.emptyFields?.length ||
        error.durationBellowZero
      ) {
        errors.push(error)
      }
    })

    setInputErrors(errors)
  }

  /********************
   ** Submit handler **
   ********************/

  const preparePayload = () => {
    return steps.map((step, index) => ({
      number: index + 1,
      instruction: step.instruction,
      duration: step.duration,
      stepType: step.type,
      // Get an array of ingredient item ids.
      ingredientItems: step.ingredientItems.map((ingredientItem) => ingredientItem.value),
    }))
  }

  const addSteps = async () => {
    validate()

    const payload = preparePayload()

    if (!inputErrors) {
      try {
        await performPost({ url: urls.recipes.steps.create({ id: recipeId }), data: payload })
        notifications.show({
          title: 'Recipe created',
          message: 'Recipe was successfully created.',
          color: 'green',
        })
        navigate(routes.overview.build())
      } catch (e) {
        console.log(e)
      }
    }
  }

  return (
    <div className="space-y-10">
      <Header title="Add steps for recipe" />
      <Card>
        <Card.Form
          title="Add steps"
          subtitle="Add steps to recipe"
          form={
            <RecipeStepsForm
              steps={steps}
              errors={inputErrors}
              ingredientItemOptions={ingredientItemOptions || []}
              onSequenceChange={handleSequenceChange}
              onStepInputAdd={handleStepInputAdd}
              onStepInputChange={handleStepInputChange}
              onStepInputDelete={handleStepInputDelete}
            />
          }
        />
        <div className={`flex space-x-3 justify-end py-4 border-t ${classes.border}`}>
          <Button variant="default">Cancel</Button>
          <Button onClick={() => addSteps()}>Finish</Button>
        </div>
      </Card>
    </div>
  )
}

function RecipeStepsCreate() {
  const { recipeId } = useParams()
  invariant(recipeId)

  const ingredientGroups = useFetch<RecipeIngredientGroupsListOutAPIResponse>(
    urls.recipes.ingredients.groups.list({ id: recipeId })
  )

  return (
    <View<object, RecipeStepsCreateInnerProps>
      results={{ ingredientGroups }}
      component={RecipeStepsCreateInner}
      componentProps={{ recipeId }}
      loadingProps={{ description: 'Loading steps' }}
      errorProps={{ description: 'There was an error loading steps, please try again.' }}
    />
  )
}

export { RecipeStepsCreate }
