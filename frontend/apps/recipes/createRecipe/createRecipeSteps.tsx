import React, { useState } from 'react'
import { Header } from './components/Header'
import View from '../../../components/View'
import { Card } from '../../../components/Card'
import { DragDropContext, Droppable } from 'react-beautiful-dnd'

import { useFetch } from '../../../hooks/fetcher'
import {
  RecipeIngredientItemGroupListOutAPIResponse,
  RecipeListOut,
  RecipeListOutAPIResponse,
} from '../../../types'
import { IngredientItemOptionType, StepInput } from './components/StepInput'
import { Button } from '../../../components/Button'
import { useNavigate, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { useCommonStyles } from '../../../styles/common'
import { performPost } from '../../../hooks/fetcher/http'
import { urls } from '../../urls'
import { routes } from '../routes'
import { useDragAndDropSingleList } from '../../../hooks/drag-and-drop'

export interface Step {
  instruction: string
  duration: number
  type: string
  ingredientItems: IngredientItemOptionType[]
}

interface CreateStepsForm {
  steps: Step[]
  ingredientItemOptions: IngredientItemOptionType[]
  onSequenceChange: (steps: Step[]) => void
  onStepInputAdd: () => void
  onStepInputChange: (index: number, data: Step) => void
  onStepInputDelete: (index: number) => void
}

function CreateStepsForm({
  steps,
  ingredientItemOptions,
  onSequenceChange,
  onStepInputAdd,
  onStepInputChange,
  onStepInputDelete,
}: CreateStepsForm) {
  const { onDragEnd, onDragStart } = useDragAndDropSingleList({ items: steps, onSequenceChange })

  return (
    <div>
      <DragDropContext onDragStart={onDragStart} onDragEnd={onDragEnd}>
        <div className="flex items-center justify-end mb-1 space-x-2">
          <Button variant="light" compact onClick={onStepInputAdd}>
            Add step
          </Button>
        </div>
        <Droppable droppableId="steps" ignoreContainerClipping isDropDisabled={steps.length <= 1}>
          {(droppableProvided, droppableSnapshot) => (
            <div
              ref={droppableProvided.innerRef}
              {...droppableProvided.droppableProps}
              className="space-y-6"
            >
              {steps.map((step, index) => (
                <StepInput
                  draggableId={index.toString()}
                  isDragDisabled={steps.length <= 1}
                  key={index}
                  step={step}
                  stepNumber={index + 1}
                  ingredientItemOptions={ingredientItemOptions}
                  canBeDeleted={steps.length > 1}
                  onInputChange={(data) => onStepInputChange(index, data)}
                  onInputDelete={() => onStepInputDelete(index)}
                />
              ))}
              {droppableProvided.placeholder}
              {!droppableSnapshot.isDraggingOver}
            </div>
          )}
        </Droppable>
      </DragDropContext>
    </div>
  )
}

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

    setSteps(stepsData)
  }

  const handleStepInputDelete = (index: number) => {
    const stepsData = [...steps]
    stepsData.splice(index, 1)
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
      ingredientItems: step.ingredientItems.map((ingredientItem) => ingredientItem.value),
    }))
  }

  // TODO: validate that all ingredients are used
  // TODO: validate that all inputs are filled
  // TODO: validate that duration > 0
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
        <Card.Form
          title="Add steps"
          subtitle="Add steps to recipe"
          form={
            <CreateStepsForm
              steps={steps}
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
