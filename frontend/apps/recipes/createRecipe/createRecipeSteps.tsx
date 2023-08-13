import React, { useState } from 'react'
import { Header } from './components/Header'
import View from '../../../components/View'
import { Card } from '../../../components/Card'

import { useFetch } from '../../../hooks/fetcher'
import { RecipeIngredientItemGroupListOutAPIResponse } from '../../../types'
import { TextInput, Textarea } from '@mantine/core'
import { IngredientItemOptionType, StepInput } from './components/StepInput'
import { Button } from '../../../components/Button'

export interface Step {
  instruction: string
  duration: number
  isPreparationStep: boolean
  ingredientItems: IngredientItemOptionType[]
}

interface CreateStepsForm {
  steps: Step[]
  ingredientItemOptions: IngredientItemOptionType[]
  onStepInputAdd: () => void
  onStepInputChange: (index: number, data: Step) => void
  onStepInputDelete: (index: number) => void
}

function CreateStepsForm({
  steps,
  ingredientItemOptions,
  onStepInputAdd,
  onStepInputChange,
  onStepInputDelete,
}: CreateStepsForm) {
  return (
    <div>
      <div className="flex items-center justify-end mb-1 space-x-2">
        <Button variant="light" compact>
          Add recipe as step
        </Button>
        <Button variant="light" compact onClick={onStepInputAdd}>
          Add step
        </Button>
      </div>
      <div className="space-y-6">
        {steps.map((step, index) => (
          <StepInput
            key={index}
            step={step}
            index={index + 1}
            ingredientItemOptions={ingredientItemOptions}
            canBeDeleted={steps.length > 1}
            onInputChange={(data) => onStepInputChange(index, data)}
            onInputDelete={() => onStepInputDelete(index)}
          />
        ))}
      </div>
    </div>
  )
}

interface RecipeStepsCreateInnerProps {
  results: {
    ingredientGroups: RecipeIngredientItemGroupListOutAPIResponse
  }
}

function RecipeStepsCreateInner({ results }: RecipeStepsCreateInnerProps) {
  const { data: ingredientGroups } = results.ingredientGroups

  const defaultStep = {
    instruction: '',
    duration: 0,
    isPreparationStep: false,
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

    setSteps(stepsData)
  }

  const handleStepInputDelete = (index: number) => {
    const stepsData = [...steps]
    stepsData.splice(index, 1)
    setSteps(stepsData)
  }

  return (
    <div className="space-y-10">
      <Header title="Add steps for recipe" />
      <Card>
        <Card.Form
          title="Add steps"
          subtitle="Add steps to recipe"
          form={
            <CreateStepsForm
              steps={steps}
              ingredientItemOptions={ingredientItemOptions || []}
              onStepInputAdd={handleStepInputAdd}
              onStepInputChange={handleStepInputChange}
              onStepInputDelete={handleStepInputDelete}
            />
          }
        />
      </Card>
    </div>
  )
}

function RecipeStepsCreate() {
  const ingredientGroups = useFetch<RecipeIngredientItemGroupListOutAPIResponse>(
    '/api/v1/recipes/5/ingredients/'
  )

  return (
    <View<object, RecipeStepsCreateInnerProps>
      results={{ ingredientGroups }}
      component={RecipeStepsCreateInner}
      componentProps={{}}
      loadingProps={{ description: 'Loading steps' }}
      errorProps={{ description: 'There was an error loading steps, please try again.' }}
    />
  )
}

export { RecipeStepsCreate }
