import React, { useState } from 'react'
import { useStepsStyles } from '../../../recipe/components/Recipe/Steps/Steps.styles'
import { Step } from '../CreateRecipeSteps'
import {
  ActionIcon,
  Checkbox,
  Select,
  Text,
  Group,
  Avatar,
  TextInput,
  Textarea,
  TransferList,
  TransferListData,
  TransferListItemComponent,
  TransferListItemComponentProps,
  useMantineTheme,
  Input,
  NumberInput,
} from '@mantine/core'
import { IconX, IconPlus, IconMinus } from '@tabler/icons-react'
import { Button } from '../../../../components/Button'

export interface IngredientItemOptionType {
  label: string
  value: string
  image?: string
  description: string
  group: string
}

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
      <Checkbox checked={selected} tabIndex={-1} sx={{ pointerEvents: 'none' }} />
    </div>
  </div>
)

interface StepInputProps {
  step: Step
  index: number
  ingredientItemOptions: IngredientItemOptionType[]
  canBeDeleted?: boolean
  onInputChange: (data: Step) => void
  onInputDelete: () => void
}

function StepInput({
  step,
  index,
  ingredientItemOptions,
  canBeDeleted,
  onInputChange,
  onInputDelete,
}: StepInputProps) {
  const { classes } = useStepsStyles()
  const theme = useMantineTheme()

  const handleIngredientItemTransfer = (
    eventData: [IngredientItemOptionType[], IngredientItemOptionType[]]
  ) => {
    const data = { ...step }
    data.ingredientItems = [...eventData[1]]

    onInputChange(data)
  }

  const handleStepInputChange = (
    key: keyof Step,
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> | number | ''
  ) => {
    if (!event) {
      return
    }

    const data = { ...step }

    if (typeof event === 'number') {
      if (key === 'duration') {
        data[key] = event
      }
    } else if (event instanceof HTMLInputElement || event instanceof HTMLTextAreaElement) {
      if (
        key === 'isPreparationStep' &&
        event.target instanceof HTMLInputElement &&
        event.target.type === 'checkbox'
      ) {
        data[key] = event.target.checked
      } else if (key === 'instruction') {
        data[key] = event.target.value.toString()
      }
    }
    onInputChange(data)
  }

  return (
    <div>
      <div className="flex items-start w-full space-x-2">
        <div className="w-full space-y-3">
          <div className="flex items-start space-x-4 rounded-md appearance-none cursor-pointer">
            <div
              className={`flex items-center justify-center flex-none w-8 h-8 ${classes.stepCircle} rounded-full`}
            >
              {index}
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
            <Checkbox
              label="Is preparation step"
              checked={step.isPreparationStep}
              onChange={(event) => handleStepInputChange('isPreparationStep', event)}
            />
            <Input.Wrapper
              label="Duration"
              required
              description="Duration of step from start to completion. In minutes."
            >
              <div className="flex items-end space-x-2">
                <ActionIcon
                  color={theme.primaryColor}
                  variant="outline"
                  size="lg"
                  disabled={step.duration <= 0}
                  onClick={() => handleStepInputChange('duration', step.duration - 1)}
                >
                  <IconMinus />
                </ActionIcon>
                <NumberInput
                  hideControls
                  className="w-full"
                  value={step.duration}
                  onChange={(event) => handleStepInputChange('duration', event)}
                  styles={{ input: { textAlign: 'center' } }}
                />
                <ActionIcon
                  color={theme.primaryColor}
                  variant="outline"
                  size="lg"
                  disabled={step.duration >= 60}
                  onClick={() => handleStepInputChange('duration', step.duration + 1)}
                >
                  <IconPlus />
                </ActionIcon>
              </div>
            </Input.Wrapper>
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
  )
}

export { StepInput }
