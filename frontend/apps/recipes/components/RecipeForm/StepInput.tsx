import { ActionIcon, Select, Textarea, MultiSelect } from '@mantine/core'
import { IconX } from '@tabler/icons-react'
import { useMemo } from 'react'
import { Draggable } from 'react-beautiful-dnd'

import { Counter } from '../../../../components/Counter'
import { useEnumToOptions } from '../../../../hooks/enum-to-options'
import { RecipeStepType } from '../../../../types'
import { useStepsStyles } from '../../../recipe/components/Recipe/Steps/Steps.styles'

import {
  type ActionFunc,
  type StepActions,
  type IngredientItemGroup,
  type Step,
  type FormErrorInner,
} from './types'

interface StepInputProps {
  draggableId: string
  isDragDisabled?: boolean
  step: Step
  stepNumber: number
  ingredientGroups: IngredientItemGroup[]
  canBeDeleted?: boolean
  onAction: ActionFunc<StepActions>
  errors?: FormErrorInner[]
}

function StepInput({
  draggableId,
  isDragDisabled,
  step,
  stepNumber,
  ingredientGroups,
  canBeDeleted,
  onAction,
  errors,
}: StepInputProps) {
  const { classes } = useStepsStyles()

  const handleStepInputChange = (
    key: keyof Step,
    eventOrValue:
      | React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
      | number
      | string
      | string[]
  ) => {
    if (!eventOrValue) {
      return
    }

    let data = { ...step }

    if (key === 'ingredientItems' && Array.isArray(eventOrValue)) {
      // The value of the event is <groupIndex>-<ingredientId>, so split and find correct ingredient item.
      const ingredientGroupItemSequences: string[][] = eventOrValue.map((event) => event.split('-'))
      const ingredientItems = ingredientGroupItemSequences.flatMap(([groupIndex, ingredientId]) =>
        ingredientGroups[Number(groupIndex)].ingredientItems.filter(
          (ingredientItem) => ingredientItem.ingredient.id.toString() === ingredientId
        )
      )

      data = { ...data, ingredientItems: ingredientItems }
    } else if (
      !Array.isArray(eventOrValue) &&
      typeof eventOrValue !== 'string' &&
      typeof eventOrValue !== 'number' &&
      eventOrValue.target &&
      (eventOrValue.target instanceof HTMLInputElement ||
        eventOrValue.target instanceof HTMLTextAreaElement)
    ) {
      const value = eventOrValue.target.value.toString()
      if (key === 'stepType') {
        data = { ...data, stepType: RecipeStepType[value as keyof typeof RecipeStepType] }
      } else {
        data = { ...data, [key]: eventOrValue.target.value.toString() }
      }
    } else {
      data = { ...data, [key]: eventOrValue }
    }
    onAction('inputChange', stepNumber - 1, data)
  }

  const stepTypes = useEnumToOptions(RecipeStepType)

  const ingredientOptions = useMemo(
    () =>
      ingredientGroups.flatMap((ingredientGroup, ingredientGroupIndex) =>
        ingredientGroup.ingredientItems
          .filter((ingredientItem) => Object.keys(ingredientItem.ingredient).length)
          .map((ingredientItem) => ({
            label: ingredientItem.ingredient.title,
            value: `${ingredientGroupIndex}-${ingredientItem.ingredient.id.toString()}`,
            group: ingredientGroup.title,
          }))
      ),
    [ingredientGroups]
  )

  // Since we need the group index and the ingredient id, back map the ingredient item and find appropriate
  // item group.
  const selectedIngredientItems = useMemo(() => {
    const mappedIngredientItems: string[] = []

    step.ingredientItems.flatMap((ingredientItem) => {
      let ingredientItemGroup: IngredientItemGroup | undefined = undefined

      if ('id' in ingredientItem) {
        // If we have an id, the ingredient item already exist in the db, and hence back mapping is easier.
        ingredientItemGroup = ingredientGroups.find((ingredientGroup) =>
          ingredientGroup.ingredientItems.some((item) => item.id === ingredientItem.id)
        )
      } else {
        // If not, we try to match on all the properties of the ingredient item to hopefully find the correct one.
        // There are some pitfalls here if we have to different groups with the same ingredient item with all data
        // matching, but it's highly unlikely.
        ingredientItemGroup = ingredientGroups.find((ingredientGroup) =>
          ingredientGroup.ingredientItems.some(
            (item) =>
              item.ingredient.id === ingredientItem.ingredient.id &&
              item.portionQuantity === ingredientItem.portionQuantity &&
              item.portionQuantityUnit.id === ingredientItem.portionQuantityUnit.id &&
              item.additionalInfo === ingredientItem.additionalInfo
          )
        )
      }

      if (ingredientItemGroup) {
        const groupIndex = ingredientGroups.indexOf(ingredientItemGroup)
        mappedIngredientItems.push(`${groupIndex}-${ingredientItem.ingredient.id}`)
      }
    })

    return mappedIngredientItems
  }, [ingredientGroups, step.ingredientItems])

  const getErrorForField = (field: string) => {
    if (!errors) return undefined

    const errorForField = errors.find((error) => error.field === field)

    if (errorForField) {
      return errorForField.message
    } else {
      return undefined
    }
  }

  return (
    <Draggable draggableId={draggableId} index={stepNumber - 1} isDragDisabled={isDragDisabled}>
      {(draggableProvided, _draggableSnapshot) => (
        <div
          ref={draggableProvided.innerRef}
          {...draggableProvided.draggableProps}
          {...draggableProvided.dragHandleProps}
          className="bg-white rounded-md"
        >
          <div className="flex items-start w-full space-x-2">
            <div className="w-full space-y-3">
              <div className=" flex items-start space-x-4 rounded-md appearance-none">
                <div
                  className={`flex items-center justify-center flex-none w-8 h-8 ${classes.stepCircle} rounded-full`}
                >
                  {stepNumber}
                </div>
                <Textarea
                  label="Instruction"
                  required
                  className="w-full text-sm"
                  value={step.instruction}
                  onChange={(event) => handleStepInputChange('instruction', event)}
                  error={getErrorForField('instruction')}
                />
              </div>
              <div className="ml-12 space-y-3">
                <Select
                  label="Step type"
                  required
                  value={step.stepType}
                  data={stepTypes}
                  onChange={(event) => handleStepInputChange('stepType', event || '')}
                  error={getErrorForField('stepType')}
                />
                <MultiSelect
                  label="Ingredients"
                  description="Pick ingredients required in this step"
                  value={selectedIngredientItems}
                  data={ingredientOptions}
                  searchable
                  clearable
                  onChange={(event) => handleStepInputChange('ingredientItems', event)}
                  error={getErrorForField('ingredientItems')}
                />
                <Counter
                  label="Duration"
                  required
                  description="Duration of step from start to completion. In minutes."
                  value={step.duration}
                  min={1}
                  max={60}
                  onChange={(event) => handleStepInputChange('duration', event)}
                  error={getErrorForField('duration')}
                />
              </div>
            </div>
            <ActionIcon
              color="red"
              variant="light"
              className="mt-5"
              disabled={!canBeDeleted}
              onClick={() => onAction('inputDelete', stepNumber - 1)}
            >
              <IconX />
            </ActionIcon>
          </div>
        </div>
      )}
    </Draggable>
  )
}

export { StepInput }
