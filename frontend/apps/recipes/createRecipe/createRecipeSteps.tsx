import React, { useState } from 'react'
import { Header } from './components/Header'
import View from '../../../components/View'
import { Card } from '../../../components/Card'

import { useFetch } from '../../../hooks/fetcher'
import {
  RecipeIngredientItemGroupListOutAPIResponse,
  RecipeListOut,
  RecipeListOutAPIResponse,
} from '../../../types'
import { IngredientItemOptionType, StepInput } from './components/StepInput'
import { Button } from '../../../components/Button'
import { RecipeSearchModal } from './components/RecipeSearchModal'
import { useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'

export interface Step {
  recipeId?: number
  stepNumber: number
  instruction: string
  duration: number
  isPreparationStep: boolean
  ingredientItems: IngredientItemOptionType[]
}

interface CreateStepsForm {
  recipes: RecipeListOut[]
  steps: Step[]
  ingredientItemOptions: IngredientItemOptionType[]
  onStepInputAdd: () => void
  onStepInputChange: (index: number, data: Step) => void
  onStepInputDelete: (index: number) => void
  onRecipeStepsCopy: (recipe: RecipeListOut) => void
}

function CreateStepsForm({
  recipes,
  steps,
  ingredientItemOptions,
  onStepInputAdd,
  onStepInputChange,
  onStepInputDelete,
  onRecipeStepsCopy,
}: CreateStepsForm) {
  const [modalOpened, setModalOpened] = useState(false)

  return (
    <div>
      <div className="flex items-center justify-end mb-1 space-x-2">
        <Button variant="light" compact onClick={() => setModalOpened(true)}>
          Copy steps from existing recipe
        </Button>
        <Button variant="light" compact onClick={onStepInputAdd}>
          Add step
        </Button>
      </div>
      <div className="space-y-6">
        {steps
          .sort((a, b) => a.stepNumber - b.stepNumber)
          .map((step, index) => (
            <StepInput
              key={index}
              step={step}
              stepNumber={step.stepNumber}
              ingredientItemOptions={ingredientItemOptions}
              canBeDeleted={steps.length > 1}
              onInputChange={(data) => onStepInputChange(index, data)}
              onInputDelete={() => onStepInputDelete(index)}
            />
          ))}
      </div>
      <RecipeSearchModal
        opened={modalOpened}
        recipes={recipes}
        onClose={() => setModalOpened(false)}
        onRecipeSelect={onRecipeStepsCopy}
      />
    </div>
  )
}

interface RecipeStepsCreateInnerProps {
  recipeId: string | number
  results: {
    recipes: RecipeListOutAPIResponse
    ingredientGroups: RecipeIngredientItemGroupListOutAPIResponse
  }
}

function RecipeStepsCreateInner({ recipeId, results }: RecipeStepsCreateInnerProps) {
  const { data: ingredientGroups } = results.ingredientGroups
  const { data: recipes } = results.recipes

  // Remove current recipe from list of recipes.
  const modifiedRecipes = recipes?.filter((recipe) => recipe.id.toString() !== recipeId)

  const defaultStep = (steps?: Step[]): Step => ({
    stepNumber: steps ? steps.length + 1 : 1,
    instruction: '',
    duration: 0,
    isPreparationStep: false,
    ingredientItems: [],
  })
  const [steps, setSteps] = useState<Step[]>([defaultStep()])

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
    setSteps([...stepsData, defaultStep(steps)])
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

  const handleRecipeStepCopy = (data: RecipeListOut) => {
    // const stepData = [...steps]
    // stepData.push({
    //   instruction: data.
    // })
    // TODO: Need to handle after you can add steps to recipe
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
              recipes={modifiedRecipes || []}
              steps={steps}
              ingredientItemOptions={ingredientItemOptions || []}
              onStepInputAdd={handleStepInputAdd}
              onStepInputChange={handleStepInputChange}
              onStepInputDelete={handleStepInputDelete}
              onRecipeStepsCopy={handleRecipeStepCopy}
            />
          }
        />
      </Card>
    </div>
  )
}

function RecipeStepsCreate() {
  const { recipeId } = useParams()
  invariant(recipeId)

  const recipes = useFetch<RecipeListOutAPIResponse>('/api/v1/recipes/')
  const ingredientGroups = useFetch<RecipeIngredientItemGroupListOutAPIResponse>(
    '/api/v1/recipes/5/ingredients/'
  )

  return (
    <View<object, RecipeStepsCreateInnerProps>
      results={{ recipes, ingredientGroups }}
      component={RecipeStepsCreateInner}
      componentProps={{ recipeId }}
      loadingProps={{ description: 'Loading steps' }}
      errorProps={{ description: 'There was an error loading steps, please try again.' }}
    />
  )
}

export { RecipeStepsCreate }
