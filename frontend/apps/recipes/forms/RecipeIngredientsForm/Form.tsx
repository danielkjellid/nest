import { useMemo } from 'react'
import { DragDropContext, Droppable } from 'react-beautiful-dnd'

import { Button } from '../../../../components/Button'
import { type UnitOption } from '../../../../contexts/UnitsProvider'
import { useDragAndDropSingleList } from '../../../../hooks/drag-and-drop'
import { type UnitRecord, type RecipeIngredientRecord } from '../../../../types'
import { type IngredientItemGroup, type IngredientItem } from '../../create2/types'

import { IngredientGroupInput } from './IngredientGroupInput'

interface RecipeIngredientFormProps {
  ingredients?: RecipeIngredientRecord[]
  ingredientGroups: IngredientItemGroup[]
  units?: UnitRecord[]
  unitOptions?: UnitOption[]
  onSequenceChange: (ingredientGroups: IngredientItemGroup[]) => void
  onIngredientInputAdd: (index: number) => void
  onIngredientInputChange: (index: number, ingredientIndex: number, data: IngredientItem) => void
  onIngredientInputDelete: (index: number, ingredientIndex: number) => void
  onIngredientGroupInputAdd: () => void
  onIngredientGroupInputChange: (index: number, data: IngredientItemGroup) => void
  onIngredientGroupInputDelete: (index: number) => void
}

function RecipeIngredientsForm({
  ingredients,
  ingredientGroups,
  units,
  unitOptions,
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
    onSequenceChange: onSequenceChange,
  })

  const ingredientOptions =
    useMemo(
      () =>
        ingredients &&
        ingredients.map((ingredient) => ({
          label: ingredient.title,
          image: ingredient.product.thumbnailUrl,
          description: ingredient.product.fullName,
          value: ingredient.id.toString(),
        })),
      [ingredients]
    ) || []

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
                  ingredients={ingredients}
                  ingredientGroup={ingredientGroup}
                  ingredientOptions={ingredientOptions}
                  units={units}
                  unitOptions={unitOptions}
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
