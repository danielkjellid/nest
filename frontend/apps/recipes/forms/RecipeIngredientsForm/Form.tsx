import React from 'react'
import { DragDropContext, Droppable } from 'react-beautiful-dnd'

import { Button } from '../../../../components/Button'
import { type UnitOption } from '../../../../contexts/UnitsProvider'
import { useDragAndDropSingleList } from '../../../../hooks/drag-and-drop'

import { IngredientGroupInput } from './IngredientGroupInput'
import {
  type Ingredient,
  type IngredientGroup,
  type IngredientGroupFormError,
  type IngredientOptionType,
} from './types'

interface RecipeIngredientFormProps {
  units: UnitOption[]
  ingredientGroups: IngredientGroup[]
  ingredientGroupsErrors: IngredientGroupFormError[]
  ingredientOptions: IngredientOptionType[]
  ingredientErrors: IngredientGroupFormError[]
  onSequenceChange: (ingredientGroups: IngredientGroup[]) => void
  onIngredientInputAdd: (index: number) => void
  onIngredientInputChange: (index: number, ingredientIndex: number, data: Ingredient) => void
  onIngredientInputDelete: (index: number, ingredientIndex: number) => void
  onIngredientGroupInputAdd: () => void
  onIngredientGroupInputChange: (index: number, data: IngredientGroup) => void
  onIngredientGroupInputDelete: (index: number) => void
}

function RecipeIngredientsForm({
  ingredientGroups,
  ingredientGroupsErrors,
  ingredientOptions,
  ingredientErrors,
  units,
  onSequenceChange,
  onIngredientInputAdd,
  onIngredientInputChange,
  onIngredientInputDelete,
  onIngredientGroupInputAdd,
  onIngredientGroupInputChange,
  onIngredientGroupInputDelete,
}: RecipeIngredientFormProps) {
  const { onDragEnd, onDragStart } = useDragAndDropSingleList({
    items: ingredientGroups,
    onSequenceChange,
  })

  return (
    <DragDropContext onDragStart={onDragStart} onDragEnd={onDragEnd}>
      <div className="flex items-center justify-end mb-1 space-x-2">
        <Button variant="light" compact onClick={onIngredientGroupInputAdd}>
          Add group
        </Button>
      </div>
      <div>
        <Droppable
          droppableId="ingredientGroups"
          ignoreContainerClipping
          isDropDisabled={ingredientGroups.length <= 1}
        >
          {(provided, snapshot) => (
            <div ref={provided.innerRef} {...provided.droppableProps} className="space-y-4">
              {ingredientGroups.map((ingredientGroup, index) => (
                <IngredientGroupInput
                  key={index}
                  isDragDisabled={ingredientGroups.length <= 1}
                  draggableId={index.toString()}
                  order={index}
                  ingredientGroup={ingredientGroup}
                  error={ingredientGroupsErrors.find((error) => error.index === index)}
                  ingredientErrors={ingredientErrors}
                  ingredientOptions={ingredientOptions}
                  units={units}
                  canBeDeleted={ingredientGroups.length > 1}
                  onIngredientInputAdd={() => onIngredientInputAdd(index)}
                  onIngredientInputChange={(ingredientIndex, data) =>
                    onIngredientInputChange(index, ingredientIndex, data)
                  }
                  onIngredientInputDelete={(ingredientIndex) =>
                    onIngredientInputDelete(index, ingredientIndex)
                  }
                  onIngredientGroupInputChange={(data) => onIngredientGroupInputChange(index, data)}
                  onIngredientGroupInputDelete={() => onIngredientGroupInputDelete(index)}
                />
              ))}
              {provided.placeholder}
              {!snapshot.isDraggingOver}
            </div>
          )}
        </Droppable>
      </div>
    </DragDropContext>
  )
}

export { RecipeIngredientsForm }
