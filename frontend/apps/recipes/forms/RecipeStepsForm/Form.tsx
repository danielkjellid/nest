import React from 'react'
import { DragDropContext, Droppable } from 'react-beautiful-dnd'


import { Button } from '../../../../components/Button'
import { useDragAndDropSingleList } from '../../../../hooks/drag-and-drop'

import { StepInput } from './StepInput'
import { IngredientItemOptionType, Step, StepInputError } from './types'

interface RecipeStepsFormProps {
  steps: Step[]
  errors?: StepInputError[]
  ingredientItemOptions: IngredientItemOptionType[]
  onSequenceChange: (steps: Step[]) => void
  onStepInputAdd: () => void
  onStepInputChange: (index: number, data: Step) => void
  onStepInputDelete: (index: number) => void
}

function RecipeStepsForm({
  steps,
  errors,
  ingredientItemOptions,
  onSequenceChange,
  onStepInputAdd,
  onStepInputChange,
  onStepInputDelete,
}: RecipeStepsFormProps) {
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
                  error={errors?.find((error) => error.index === index)}
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

export { RecipeStepsForm }
