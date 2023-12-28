import { ActionIcon, Select, Text, TextInput } from '@mantine/core'
import { IconPlus, IconX } from '@tabler/icons-react'
import React, { forwardRef } from 'react'
import { Draggable } from 'react-beautiful-dnd'

import { type UnitOption } from '../../../../contexts/UnitsProvider'
import { type IngredientItemGroup, type IngredientItem } from '../../create2/types'

import { type FormError, type IngredientOptionType } from './types'

interface IngredientOptionProps extends React.ComponentPropsWithoutRef<'div'> {
  image?: string | null
  label: string
  description: string
}

const IngredientOption = forwardRef<HTMLDivElement, IngredientOptionProps>(
  ({ image, label, description, ...others }: IngredientOptionProps, ref) => (
    <div ref={ref} {...others}>
      <div className="flex items-center space-x-2">
        <img src={image || ''} className="object-contain w-12 h-12 rounded-md" />
        <div className="w-full">
          <Text size="sm">{label}</Text>
          <Text size="xs" opacity={0.65} className="truncate">
            {description}
          </Text>
        </div>
      </div>
    </div>
  )
)

IngredientOption.displayName = 'IngredientOption'

interface IngredientInputProps {
  units: UnitOption[]
  error?: FormError
  ingredient: IngredientItem
  ingredientOptions: IngredientOptionType[]
  canBeDeleted: boolean
  onInputDelete: () => void
  onInputChange: (data: IngredientItem) => void
}

function IngredientInput({
  ingredient,
  error,
  ingredientOptions,
  units,
  canBeDeleted,
  onInputDelete,
  onInputChange,
}: IngredientInputProps) {
  const handleInputChange = (
    key: keyof IngredientItem,
    event: React.ChangeEvent<HTMLInputElement> | string | null
  ) => {
    if (!event) {
      return
    }

    let data: IngredientItem = { ...ingredient }

    if (typeof event === 'string') {
      data = { [key]: event, ...data }
    } else {
      data = { [key]: event.target.value.toString(), ...data }
    }
    onInputChange(data)
  }

  return (
    <div className="relative">
      <div className="rounded-bl-md absolute bottom-0 w-6 h-8 mb-4 ml-3 bg-transparent border-b-2 border-l-2 border-gray-200" />
      <div className="flex items-end w-full space-x-2">
        <Select
          label="Ingredient"
          value={ingredient.ingredientId}
          required
          className="w-96 ml-8"
          data={ingredientOptions}
          searchable
          error={error ? <></> : undefined}
          itemComponent={IngredientOption}
          onChange={(event) => handleInputChange('ingredientId', event)}
        />
        <TextInput
          label="Quantity"
          value={ingredient.portionQuantity}
          required
          error={error ? <></> : undefined}
          className="w-48"
          onChange={(event) => handleInputChange('portionQuantity', event)}
        />
        <Select
          label="Unit"
          value={ingredient.portionQuantityUnitId}
          required
          error={error ? <></> : undefined}
          className="w-48"
          data={units}
          onChange={(event) => handleInputChange('portionQuantityUnitId', event)}
        />
        <TextInput
          label="Comment"
          value={ingredient.additionalInfo}
          error={error ? <></> : undefined}
          className="w-80"
          placeholder="Optional comment"
          onChange={(event) => handleInputChange('additionalInfo', event)}
        />
        <ActionIcon
          disabled={!canBeDeleted}
          className="mb-1"
          color="red"
          onClick={() => onInputDelete()}
        >
          <IconX />
        </ActionIcon>
      </div>
    </div>
  )
}

interface IngredientGroupInputProps {
  order: number
  draggableId: string
  isDragDisabled?: boolean
  ingredientGroup: IngredientItemGroup
  error?: FormError
  ingredientErrors: FormError[]
  units: UnitOption[]
  ingredientOptions: IngredientOptionType[]
  canBeDeleted: boolean
  onIngredientGroupInputChange: (data: IngredientItemGroup) => void
  onIngredientGroupInputDelete: () => void
  onIngredientInputChange: (index: number, data: IngredientItem) => void
  onIngredientInputAdd: () => void
  onIngredientInputDelete: (index: number) => void
}

function IngredientGroupInput({
  order,
  draggableId,
  isDragDisabled,
  ingredientGroup,
  error,
  ingredientErrors,
  ingredientOptions,
  units,
  canBeDeleted,
  onIngredientGroupInputChange,
  onIngredientGroupInputDelete,
  onIngredientInputChange,
  onIngredientInputAdd,
  onIngredientInputDelete,
}: IngredientGroupInputProps) {
  const handleIngredientGroupInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const data = { ...ingredientGroup }
    data.title = event.target.value.toString()

    onIngredientGroupInputChange(data)
  }

  return (
    <Draggable draggableId={draggableId} index={order} isDragDisabled={isDragDisabled}>
      {(draggableProvided, _draggableSnapshot) => (
        <div
          ref={draggableProvided.innerRef}
          {...draggableProvided.draggableProps}
          {...draggableProvided.dragHandleProps}
          className="bg-white rounded-md"
        >
          <div className="flex items-end w-full space-x-2">
            <TextInput
              label="Ingredient group name"
              className="z-25 w-full"
              required
              error={error?.message}
              value={ingredientGroup.title}
              onChange={handleIngredientGroupInputChange}
            />
            <ActionIcon
              disabled={!canBeDeleted}
              className="mb-1"
              color="red"
              variant="light"
              onClick={onIngredientGroupInputDelete}
            >
              <IconX />
            </ActionIcon>
          </div>
          <div className="relative">
            <div
              style={{ height: 'calc(100% - 20px)' }}
              className="absolute left-3 w-0.5 bg-gray-200 -mt-4"
              aria-hidden
            />
            <div className="relative mt-4 space-y-4">
              {ingredientGroup.ingredientItems.map((ingredient, index) => (
                <IngredientInput
                  key={index}
                  ingredient={ingredient}
                  error={ingredientErrors.find((error) => error.index === index)}
                  ingredientOptions={ingredientOptions}
                  units={units}
                  canBeDeleted={ingredientGroup.ingredientItems.length > 1}
                  onInputDelete={() => onIngredientInputDelete(index)}
                  onInputChange={(data) => onIngredientInputChange(index, data)}
                />
              ))}
            </div>
          </div>
          <ActionIcon
            color="green"
            variant="light"
            className="mt-3 ml-8"
            onClick={onIngredientInputAdd}
          >
            <IconPlus />
          </ActionIcon>
        </div>
      )}
    </Draggable>
  )
}

export { IngredientGroupInput }
