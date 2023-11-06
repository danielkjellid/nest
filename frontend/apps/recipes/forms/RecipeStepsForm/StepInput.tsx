import {
  ActionIcon,
  Checkbox,
  Input,
  Select,
  Text,
  Textarea,
  TransferList,
  TransferListItemComponent,
  TransferListItemComponentProps,
} from '@mantine/core'
import { IconX } from '@tabler/icons-react'
import React from 'react'
import { Draggable } from 'react-beautiful-dnd'

import { Counter } from '../../../../components/Counter'
import { useEnumToOptions } from '../../../../hooks/enum-to-options'
import { RecipeStepType } from '../../../../types'
import { useStepsStyles } from '../../../recipe/components/Recipe/Steps/Steps.styles'

import { IngredientItemOptionType } from './types'
import { Step, StepInputError } from './types'

const IngredientItemOption: TransferListItemComponent = ({
  data,
  selected,
}: TransferListItemComponentProps) => (
  <div>
    <div className="w-80 grow shrink basis-0 flex items-center justify-between px-1 space-x-3">
      <div className="flex items-center space-x-2">
        <img src={data.image || ''} className="object-contain w-12 h-12 rounded-md" />
        <div className="w-64 overflow-hidden">
          <Text size="sm">{data.label}</Text>
          <Text size="xs" opacity={0.65} className="truncate">
            {data.description}
          </Text>
        </div>
      </div>
      <Checkbox
        checked={selected}
        tabIndex={-1}
        sx={{ pointerEvents: 'none' }}
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        onChange={() => {}}
      />
    </div>
  </div>
)

interface StepInputProps {
  draggableId: string
  isDragDisabled?: boolean
  step: Step
  error?: StepInputError
  stepNumber: number
  ingredientItemOptions: IngredientItemOptionType[]
  canBeDeleted?: boolean
  onInputChange: (data: Step) => void
  onInputDelete: () => void
}

function StepInput({
  draggableId,
  isDragDisabled,
  step,
  error,
  stepNumber,
  ingredientItemOptions,
  canBeDeleted,
  onInputChange,
  onInputDelete,
}: StepInputProps) {
  const { classes } = useStepsStyles()

  const handleIngredientItemTransfer = (
    eventData: [IngredientItemOptionType[], IngredientItemOptionType[]]
  ) => {
    const data = { ...step }
    data.ingredientItems = [...eventData[1]]

    onInputChange(data)
  }

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

  const getErrorMessage = (key: keyof Step) => {
    if (!error) {
      return undefined
    }

    if (error.emptyFields?.includes(key)) {
      return 'This field cannot be empty.'
    }

    if (key === 'duration' && error.durationBellowZero) {
      return 'Duration cannot be equal to or bellow zero.'
    }

    if (key === 'ingredientItems' && error.unusedIngredientOptions) {
      return 'All ingredient items has to be assigned to a step.'
    }

    return undefined
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
                  error={getErrorMessage('instruction')}
                />
              </div>
              <div className="ml-12 space-y-3">
                <Select
                  label="Step type"
                  required
                  value={step.type}
                  data={stepTypes}
                  onChange={(event) => handleStepInputChange('type', event || '')}
                  error={getErrorMessage('type')}
                />
                <Counter
                  label="Duration"
                  required
                  description="Duration of step from start to completion. In minutes."
                  value={step.duration}
                  min={1}
                  max={60}
                  onChange={(event) => handleStepInputChange('duration', event)}
                  error={getErrorMessage('duration')}
                />
                <Input.Wrapper error={getErrorMessage('ingredientItems')}>
                  <TransferList
                    value={[ingredientItemOptions, step.ingredientItems]}
                    onChange={handleIngredientItemTransfer}
                    searchPlaceholder="Search ingredients"
                    nothingFound="No ingredients matching query"
                    titles={['Available ingredients', 'Ingredients related to step']}
                    listHeight={300}
                    itemComponent={IngredientItemOption}
                    filter={(query, item) =>
                      item.label.toLowerCase().includes(query.toLowerCase().trim()) ||
                      item.description.toLowerCase().includes(query.toLowerCase().trim())
                    }
                  />
                </Input.Wrapper>
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
