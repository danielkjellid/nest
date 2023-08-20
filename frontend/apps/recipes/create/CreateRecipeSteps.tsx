import React, { useState } from 'react'
import { Header } from './components/Header'
import View from '../../../components/View'
import { Card } from '../../../components/Card'

import { useFetch } from '../../../hooks/fetcher'
import { RecipeIngredientItemGroupListOutAPIResponse } from '../../../types'
import { Button } from '../../../components/Button'
import { useNavigate, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { useCommonStyles } from '../../../styles/common'
import { performPost } from '../../../hooks/fetcher/http'
import { urls } from '../../urls'
import { routes } from '../routes'
import { Step, StepInputError, RecipeStepsForm } from '../forms/RecipeStepsForm'

interface RecipeStepsCreateInnerProps {
  recipeId: string | number
  results: {
    ingredientGroups: RecipeIngredientItemGroupListOutAPIResponse
  }
}

function RecipeStepsCreateInner({ recipeId, results }: RecipeStepsCreateInnerProps) {
  const { data: ingredientGroups } = results.ingredientGroups
  const navigate = useNavigate()

  const { classes } = useCommonStyles()

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
  const ingredientItemOptions = ingredientGroups?.flatMap((ingredientGroup) =>
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
  )

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

  const addSteps = async () => {
    const payload = preparePayload()
    try {
      await performPost({ url: urls.recipes.createSteps({ id: recipeId }), data: payload })
      navigate(routes.overview.build())
    } catch (e) {
      // TODO: set notification
    }
  }

  return (
    <div className="space-y-10">
      <Header title="Add steps for recipe" />
      <Card>
        {JSON.stringify(inputErrors)}
        <hr />
        <button onClick={() => validate()}>validate</button>
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
  const ingredientGroups = useFetch<RecipeIngredientItemGroupListOutAPIResponse>(
    urls.recipes.listIngredientGroups({ id: recipeId })
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
