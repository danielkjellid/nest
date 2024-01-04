import { ActionIcon, Select, Text, TextInput, Input } from '@mantine/core'
import { IconPlus, IconX } from '@tabler/icons-react'
import React, { forwardRef, useMemo } from 'react'
import { Draggable } from 'react-beautiful-dnd'

import { type UnitOption } from '../../../../contexts/UnitsProvider'
import { type UnitRecord, type RecipeIngredientRecord } from '../../../../types'
import {
  type IngredientItemGroup,
  type IngredientItem,
  type ActionFunc,
  type IngredientGroupActions,
  type FormError,
  type FormErrorInner,
} from '../types'

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
  ingredientItem: IngredientItem
  ingredients?: RecipeIngredientRecord[]
  units?: UnitRecord[]
  unitOptions?: UnitOption[]
  canBeDeleted: boolean
  onInputDelete: () => void
  onInputChange: (data: IngredientItem) => void
  error?: FormErrorInner[]
}

function IngredientInput({
  ingredientItem,
  ingredients,
  units,
  unitOptions,
  canBeDeleted,
  onInputDelete,
  onInputChange,
  error,
}: IngredientInputProps) {
  const handleInputChange = (
    key: keyof IngredientItem,
    event: React.ChangeEvent<HTMLInputElement> | string | null
  ) => {
    if (!event) {
      return
    }

    let data: IngredientItem = { ...ingredientItem }

    if (typeof event === 'string') {
      if (key === 'ingredient') {
        const ingredient = ingredients?.find((ingredient) => ingredient.id.toString() === event)
        data = {
          ...data,
          ingredient: ingredient || ({} as RecipeIngredientRecord),
          portionQuantityUnit: ingredient?.product.unit || ({} as UnitRecord),
        }
      } else if (key === 'portionQuantityUnit') {
        const unit = units?.find((unit) => unit.id.toString() === event)
        data = {
          ...data,
          portionQuantityUnit: unit || ({} as UnitRecord),
        }
      } else {
        data = { ...data, [key]: event }
      }
    } else {
      data = { ...data, [key]: event.target.value.toString() }
    }
    onInputChange(data)
  }

  const ingredientId = ingredientItem.ingredient.id || ''
  const unitId = ingredientItem.portionQuantityUnit.id || ''

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
    <div className="relative">
      <div className="flex items-center justify-between space-x-2">
        <div>
          <div className="relative">
            <div className="rounded-bl-md absolute bottom-0 w-6 h-8 mb-4 ml-3 bg-transparent border-b-2 border-l-2 border-gray-200" />
            <div className="flex items-center ml-8 space-x-2">
              <Select
                label="Ingredient"
                value={ingredientId.toString()}
                required
                data={ingredientOptions}
                searchable
                itemComponent={IngredientOption}
                onChange={(event) => handleInputChange('ingredient', event)}
                error={!!error}
              />
              <TextInput
                label="Quantity"
                value={ingredientItem.portionQuantity}
                required
                className="w-28"
                onChange={(event) => handleInputChange('portionQuantity', event)}
                error={!!error}
              />
              <Select
                label="Unit"
                value={unitId.toString()}
                required
                className="w-32"
                onChange={(event) => handleInputChange('portionQuantityUnit', event)}
                data={unitOptions || []}
                error={!!error}
              />
              <TextInput
                label="Comment"
                value={ingredientItem.additionalInfo}
                placeholder="Optional comment"
                onChange={(event) => handleInputChange('additionalInfo', event)}
                error={!!error}
              />
              <ActionIcon
                disabled={!canBeDeleted}
                className="mt-6"
                color="red"
                onClick={() => onInputDelete()}
              >
                <IconX />
              </ActionIcon>
            </div>
          </div>
          {error &&
            Object.values(error).map((err) => (
              <Input.Error key={err.message} className="block ml-8">
                {err.message}
              </Input.Error>
            ))}
        </div>
      </div>
    </div>
  )
}

interface IngredientGroupInputProps {
  groupIndex: number
  order: number
  draggableId: string
  isDragDisabled?: boolean
  ingredientGroup: IngredientItemGroup
  units?: UnitRecord[]
  unitOptions?: UnitOption[]
  ingredients?: RecipeIngredientRecord[]
  canBeDeleted: boolean
  onAction: ActionFunc<IngredientGroupActions>
  errors?: FormErrorInner[]
  ingredientItemsErrors: FormError
}

function IngredientGroupInput({
  groupIndex,
  order,
  draggableId,
  isDragDisabled,
  ingredients,
  ingredientGroup,
  units,
  unitOptions,
  canBeDeleted,
  onAction,
  errors,
  ingredientItemsErrors,
}: IngredientGroupInputProps) {
  const handleIngredientGroupInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const data = { ...ingredientGroup, title: event.target.value.toString(), ordering: order }
    onAction('groupChange', groupIndex, data)
  }

  const numErrors = Object.values(ingredientItemsErrors)
    // Only count based on visible field's errors.
    .filter((_error, index) => index < ingredientGroup.ingredientItems.length)
    .flatMap((error) => Object.values(error).flatMap((e) => e)).length

  const height = 30 + 15 * numErrors + 80 * (ingredientGroup.ingredientItems.length - 1)
  return (
    <Draggable draggableId={draggableId} index={order} isDragDisabled={isDragDisabled}>
      {(draggableProvided, _draggableSnapshot) => (
        <div
          ref={draggableProvided.innerRef}
          {...draggableProvided.draggableProps}
          {...draggableProvided.dragHandleProps}
          className="bg-white rounded-md"
        >
          <div className="flex items-start w-full space-x-2">
            <TextInput
              label="Ingredient group name"
              className="z-25 w-full"
              required
              value={ingredientGroup.title}
              onChange={handleIngredientGroupInputChange}
              error={errors && errors[0].message}
            />
            <ActionIcon
              disabled={!canBeDeleted}
              className="mt-7"
              color="red"
              variant="light"
              onClick={() => onAction('groupDelete', groupIndex)}
            >
              <IconX />
            </ActionIcon>
          </div>
          <div className="relative">
            <div
              style={{
                height: `${height}px`,
              }}
              className="absolute left-3 w-0.5 bg-gray-200 -mt-4"
              aria-hidden
            />
            <div className="relative mt-4 space-y-4">
              {ingredientGroup.ingredientItems.map((ingredientItem, ingredientIndex) => (
                <IngredientInput
                  key={ingredientIndex}
                  ingredientItem={ingredientItem}
                  ingredients={ingredients}
                  units={units}
                  unitOptions={unitOptions}
                  canBeDeleted={ingredientGroup.ingredientItems.length > 1}
                  onInputDelete={() => onAction('inputDelete', groupIndex)}
                  onInputChange={(data) =>
                    onAction('inputChange', groupIndex, ingredientIndex, data)
                  }
                  error={ingredientItemsErrors[ingredientIndex]}
                />
              ))}
            </div>
          </div>
          <ActionIcon
            color="green"
            variant="light"
            className="mt-3 ml-8"
            onClick={() => onAction('inputAdd', groupIndex)}
          >
            <IconPlus />
          </ActionIcon>
        </div>
      )}
    </Draggable>
  )
}

export { IngredientGroupInput }
