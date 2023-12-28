import { ActionIcon, Select, Text, TextInput } from '@mantine/core'
import { IconPlus, IconX } from '@tabler/icons-react'
import React, { forwardRef } from 'react'
import { Draggable } from 'react-beautiful-dnd'

import { type UnitOption } from '../../../../contexts/UnitsProvider'
import { type RecipeIngredientRecord } from '../../../../types'
import { type IngredientItemGroup, type IngredientItem } from '../../create2/types'

import { type IngredientOptionType } from './types'

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
  ingredient: IngredientItem
  ingredientOptions: IngredientOptionType[]
  ingredients?: RecipeIngredientRecord[]
  canBeDeleted: boolean
  onInputDelete: () => void
  onInputChange: (data: IngredientItem) => void
}

function IngredientInput({
  ingredient,
  ingredientOptions,
  ingredients,
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
      if (key === 'ingredient') {
        const ingredient = ingredients?.find((ingredient) => ingredient.id.toString() === event)
        data = {
          ...data,
          ingredient: ingredient || ({} as RecipeIngredientRecord),
        }
      } else {
        data = { ...data, [key]: event }
      }
    } else {
      data = { ...data, [key]: event.target.value.toString() }
    }
    onInputChange(data)
  }

  const ingredientId = ingredient.ingredient.id || ''

  return (
    <div className="relative">
      <div className="rounded-bl-md absolute bottom-0 w-6 h-8 mb-4 ml-3 bg-transparent border-b-2 border-l-2 border-gray-200" />
      <div className="flex items-end w-full space-x-2">
        <Select
          label="Ingredient"
          value={ingredientId.toString()}
          required
          className="w-96 ml-8"
          data={ingredientOptions}
          searchable
          itemComponent={IngredientOption}
          onChange={(event) => handleInputChange('ingredient', event)}
        />
        <TextInput
          label="Quantity"
          value={ingredient.portionQuantity}
          required
          className="w-48"
          onChange={(event) => handleInputChange('portionQuantity', event)}
        />
        <Select
          label="Unit"
          value={ingredient.portionQuantityUnitId}
          required
          className="w-48"
          data={units}
          onChange={(event) => handleInputChange('portionQuantityUnitId', event)}
        />
        <TextInput
          label="Comment"
          value={ingredient.additionalInfo}
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
  units: UnitOption[]
  ingredientOptions: IngredientOptionType[]
  ingredients?: RecipeIngredientRecord[]
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
  ingredientOptions,
  ingredients,
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
                  ingredientOptions={ingredientOptions}
                  ingredients={ingredients}
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
