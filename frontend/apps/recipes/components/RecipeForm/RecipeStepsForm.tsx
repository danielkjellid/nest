import { DragDropContext, Droppable } from 'react-beautiful-dnd'

import { Button } from '../../../../components/Button'
import { useDragAndDropSingleList } from '../../../../hooks/drag-and-drop'

import { StepInput } from './StepInput'
import {
  type IngredientItemGroup,
  type Step,
  type ActionFunc,
  type StepActions,
  type FormError,
} from './types'

interface RecipeStepsFormProps {
  steps: Step[]
  ingredientGroups: IngredientItemGroup[]
  onAction: ActionFunc<StepActions>
  errors: FormError
}

function RecipeStepsForm({ steps, ingredientGroups, onAction, errors }: RecipeStepsFormProps) {
  const { onDragEnd, onDragStart } = useDragAndDropSingleList({
    items: steps,
    onSequenceChange: (items) => onAction('stepSequenceChange', items),
  })

  return (
    <div>
      <DragDropContext onDragStart={onDragStart} onDragEnd={onDragEnd}>
        <div className="flex items-center justify-end mb-1 space-x-2">
          <Button variant="light" compact onClick={() => onAction('inputAdd')}>
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
                  onAction={onAction}
                  errors={errors[index]}
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
