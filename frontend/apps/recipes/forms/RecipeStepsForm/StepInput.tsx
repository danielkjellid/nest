import { ActionIcon, Select, Textarea, MultiSelect } from '@mantine/core'
import { IconX } from '@tabler/icons-react'
import { useMemo } from 'react'
import { Draggable } from 'react-beautiful-dnd'

import { Counter } from '../../../../components/Counter'
import { useEnumToOptions } from '../../../../hooks/enum-to-options'
import { RecipeStepType } from '../../../../types'
import { useStepsStyles } from '../../../recipe/components/Recipe/Steps/Steps.styles'
import { type IngredientItemGroup } from '../../create2/types'

import { type Step } from './types'

interface StepInputProps {
  draggableId: string
  isDragDisabled?: boolean
  step: Step
  stepNumber: number
  ingredientGroups: IngredientItemGroup[]
  canBeDeleted?: boolean
  onInputChange: (data: Step) => void
  onInputDelete: () => void
}

function StepInput({
  draggableId,
  isDragDisabled,
  step,
  stepNumber,
  ingredientGroups,
  canBeDeleted,
  onInputChange,
  onInputDelete,
}: StepInputProps) {
  const { classes } = useStepsStyles()

  const handleStepInputChange = (
    key: keyof Step,
    eventOrValue: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | number | string | ''
  ) => {
    if (!eventOrValue || key === 'ingredientItems') {
      return
    }

    const data = { ...step }

    if (
      typeof eventOrValue !== 'string' &&
      typeof eventOrValue !== 'number' &&
      eventOrValue.target &&
      (eventOrValue.target instanceof HTMLInputElement ||
        eventOrValue.target instanceof HTMLTextAreaElement)
    ) {
      //@ts-ignore
      data[key] = eventOrValue.target.value.toString()
    } else {
      //@ts-ignore
      data[key] = eventOrValue
    }

    onInputChange(data)
  }

  const stepTypes = useEnumToOptions(RecipeStepType)

  const ingredientOptions = useMemo(
    () =>
      ingredientGroups.flatMap((ingredientGroup) =>
        ingredientGroup.ingredientItems
          .filter((ingredientItem) => Object.keys(ingredientItem.ingredient).length)
          .map((ingredientItem) => ({
            label: ingredientItem.ingredient.title,
            value: ingredientItem.ingredient.id.toString(),
            group: ingredientGroup.title,
          }))
      ),
    [ingredientGroups]
  )

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
                />
              </div>
              <div className="ml-12 space-y-3">
                <Select
                  label="Step type"
                  required
                  value={step.type}
                  data={stepTypes}
                  onChange={(event) => handleStepInputChange('type', event || '')}
                />
                <Counter
                  label="Duration"
                  required
                  description="Duration of step from start to completion. In minutes."
                  value={step.duration}
                  min={1}
                  max={60}
                  onChange={(event) => handleStepInputChange('duration', event)}
                />
                <MultiSelect
                  label="Ingredients"
                  description="Pick ingredients required in this step"
                  data={ingredientOptions}
                  required
                  searchable
                  clearable
                />
              </div>
            </div>
            <ActionIcon
              color="red"
              variant="light"
              className="mt-5"
              disabled={!canBeDeleted}
              onClick={onInputDelete}
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
