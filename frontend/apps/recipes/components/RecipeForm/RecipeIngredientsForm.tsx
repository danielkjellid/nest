import { DragDropContext, Droppable } from 'react-beautiful-dnd'

import { Button } from '../../../../components/Button'
import { type UnitOption } from '../../../../contexts/UnitsProvider'
import { useDragAndDropSingleList } from '../../../../hooks/drag-and-drop'
import { type UnitRecord, type RecipeIngredientRecord } from '../../../../types'

import { IngredientGroupInput } from './IngredientGroupInput'
import {
  type IngredientItemGroup,
  type ActionFunc,
  type IngredientGroupActions,
  type FormError,
} from './types'

interface RecipeIngredientFormProps {
  ingredients?: RecipeIngredientRecord[]
  ingredientGroups: IngredientItemGroup[]
  units?: UnitRecord[]
  unitOptions?: UnitOption[]
  onAction: ActionFunc<IngredientGroupActions>
  ingredientGroupErrors: FormError
  ingredientItemsErrors: FormError
}

function RecipeIngredientsForm({
  ingredients,
  ingredientGroups,
  units,
  unitOptions,
  onAction,
  ingredientGroupErrors,
  ingredientItemsErrors,
}: RecipeIngredientFormProps) {
  const { onDragEnd, onDragStart } = useDragAndDropSingleList({
    items: ingredientGroups,
    onSequenceChange: (items) => onAction('groupSequenceChange', items),
  })

  return (
    <DragDropContext onDragStart={onDragStart} onDragEnd={onDragEnd}>
      <div className="flex items-center justify-end mb-1 space-x-2">
        <Button variant="light" compact onClick={() => onAction('groupAdd')}>
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
                  groupIndex={index}
                  isDragDisabled={ingredientGroups.length <= 1}
                  draggableId={index.toString()}
                  order={index}
                  ingredients={ingredients}
                  ingredientGroup={ingredientGroup}
                  units={units}
                  unitOptions={unitOptions}
                  canBeDeleted={ingredientGroups.length > 1}
                  onAction={onAction}
                  errors={ingredientGroupErrors[index]}
                  ingredientItemsErrors={ingredientItemsErrors}
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
