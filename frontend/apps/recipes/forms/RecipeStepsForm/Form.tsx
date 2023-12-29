import { DragDropContext, Droppable } from 'react-beautiful-dnd'

import { Button } from '../../../../components/Button'
import { useDragAndDropSingleList } from '../../../../hooks/drag-and-drop'
import { type IngredientItemGroup, type IngredientItem } from '../../create2/types'

import { StepInput } from './StepInput'
import { type Step } from './types'

interface RecipeStepsFormProps {
  steps: Step[]
  ingredientGroups: IngredientItemGroup[]
  onSequenceChange: (steps: Step[]) => void
  onStepInputAdd: () => void
  onStepInputChange: (index: number, data: Step) => void
  onStepInputDelete: (index: number) => void
}

function RecipeStepsForm({
  steps,
  ingredientGroups,
  onSequenceChange,
  onStepInputAdd,
  onStepInputChange,
  onStepInputDelete,
}: RecipeStepsFormProps) {
  const { onDragEnd, onDragStart } = useDragAndDropSingleList({
    items: steps,
    onSequenceChange: onSequenceChange,
  })

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
                  ingredientGroups={ingredientGroups}
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
