import React, { forwardRef, useMemo, useState } from 'react'
import { Card } from '../../../components/Card'
import { Button } from '../../../components/Button'

import { Header } from './components/Header'
import { useCommonStyles } from '../../../styles/common'
import View from '../../../components/View'
import { useFetch } from '../../../hooks/fetcher'
import { IngredientListOutAPIResponse } from '../../../types'
import { urls } from '../../urls'
import { ActionIcon, Select, TextInput, Text, createStyles, rem, getSize } from '@mantine/core'
import { IconPlus, IconX } from '@tabler/icons-react'
import { useUnits, UnitOption } from '../../../contexts/UnitsProvider'

interface IngredientOptionType {
  label: string
  value: string
  image?: string | null
  description: string
}

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

interface Ingredient {
  ingredient: string
  amount: string
  unit: UnitOption['value']
}

interface IngredientInputProps {
  units: UnitOption[]
  error?: Error
  ingredient: Ingredient
  ingredientOptions: IngredientOptionType[]
  canBeDeleted: boolean
  onInputDelete: () => void
  onInputChange: (data: Ingredient) => void
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
    key: keyof Ingredient,
    event: React.ChangeEvent<HTMLInputElement> | string | null
  ) => {
    if (!event) {
      return
    }

    const data = { ...ingredient }

    if (typeof event === 'string') {
      data[key] = event
    } else {
      data[key] = event.target.value.toString()
    }
    onInputChange(data)
  }

  return (
    <div className="relative">
      <div className="rounded-bl-md absolute bottom-0 w-8 h-8 mb-4 ml-3 bg-transparent border-b-2 border-l-2 border-gray-200" />
      <div className="flex items-end w-full space-x-2">
        <Select
          label="Ingredient"
          value={ingredient.ingredient}
          required
          className="w-full ml-10"
          data={ingredientOptions}
          searchable
          error={error ? <></> : undefined}
          itemComponent={IngredientOption}
          onChange={(event) => handleInputChange('ingredient', event)}
        />
        <TextInput
          label="Amount"
          value={ingredient.amount}
          required
          error={error ? <></> : undefined}
          className="w-48 ml-10"
          onChange={(event) => handleInputChange('amount', event)}
        />
        <Select
          label="Unit"
          value={ingredient.unit}
          required
          error={error ? <></> : undefined}
          className="w-48 ml-10"
          data={units}
          onChange={(event) => handleInputChange('unit', event)}
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
  ingredientGroup: IngredientGroup
  error?: Error
  ingredientErrors: Error[]
  units: UnitOption[]
  ingredientOptions: IngredientOptionType[]
  canBeDeleted: boolean
  onIngredientGroupInputChange: (data: IngredientGroup) => void
  onIngredientGroupInputDelete: () => void
  onIngredientInputChange: (index: number, data: Ingredient) => void
  onIngredientInputAdd: () => void
  onIngredientInputDelete: (index: number) => void
}

function IngredientGroupInput({
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
    <div>
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
          {ingredientGroup.ingredients.map((ingredient, index) => (
            <IngredientInput
              key={index}
              ingredient={ingredient}
              error={ingredientErrors.find((error) => error.index === index)}
              ingredientOptions={ingredientOptions}
              units={units}
              canBeDeleted={ingredientGroup.ingredients.length > 1}
              onInputDelete={() => onIngredientInputDelete(index)}
              onInputChange={(data) => onIngredientInputChange(index, data)}
            />
          ))}
        </div>
      </div>
      <ActionIcon
        color="green"
        variant="light"
        className="mt-3 ml-10"
        onClick={onIngredientInputAdd}
      >
        <IconPlus />
      </ActionIcon>
    </div>
  )
}

interface IngredientGroup {
  title: string
  ingredients: Ingredient[]
}

interface CreateIngredientFormProps {
  units: UnitOption[]
  ingredientGroups: IngredientGroup[]
  ingredientGroupsErrors: Error[]
  ingredientOptions: IngredientOptionType[]
  ingredientErrors: Error[]
  onIngredientInputAdd: (index: number) => void
  onIngredientInputChange: (index: number, ingredientIndex: number, data: Ingredient) => void
  onIngredientInputDelete: (index: number, ingredientIndex: number) => void
  onIngredientGroupInputAdd: () => void
  onIngredientGroupInputChange: (index: number, data: IngredientGroup) => void
  onIngredientGroupInputDelete: (index: number) => void
}

function CreateIngredientsForm({
  ingredientGroups,
  ingredientGroupsErrors,
  ingredientOptions,
  ingredientErrors,
  units,
  onIngredientInputAdd,
  onIngredientInputChange,
  onIngredientInputDelete,
  onIngredientGroupInputAdd,
  onIngredientGroupInputChange,
  onIngredientGroupInputDelete,
}: CreateIngredientFormProps) {
  return (
    <div className="space-y-4">
      {ingredientGroups.map((ingredientGroup, index) => (
        <IngredientGroupInput
          key={index}
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
      <Button variant="light" compact onClick={onIngredientGroupInputAdd}>
        Add group
      </Button>
    </div>
  )
}

interface Error {
  index: number
  message: string
}

interface RecipeIngredientsCreateInnerProps {
  results: {
    ingredients: IngredientListOutAPIResponse
  }
}

function RecipeIngredientsCreateInner({ results }: RecipeIngredientsCreateInnerProps) {
  const { data: ingredients } = results.ingredients
  const { classes } = useCommonStyles()
  const { unitsOptions } = useUnits()

  const ingredientOptions = useMemo(
    () =>
      ingredients &&
      ingredients.map((ingredient) => ({
        label: ingredient.title,
        image: ingredient.product.thumbnailUrl,
        description: ingredient.product.fullName,
        value: ingredient.id.toString(),
      })),
    [ingredients]
  )

  const [ingredientGroupErrors, setIngredientGroupErrors] = useState<Error[]>([])
  const [ingredientErrors, setIngredientErrors] = useState<Error[]>([])

  const defaultIngredient = { ingredient: '', amount: '', unit: '' }
  const defaultIngredientGroup = { title: '', ingredients: [defaultIngredient] }

  const [ingredientGroups, setIngredientGroups] = useState<IngredientGroup[]>([
    defaultIngredientGroup,
  ])

  const resetErrors = () => {
    if (ingredientGroupErrors.length) {
      setIngredientGroupErrors([])
    }

    if (ingredientErrors.length) {
      setIngredientErrors([])
    }
  }

  const handleIngredientGroupInputAdd = () => {
    const ingredientGroupsData = [...ingredientGroups]
    setIngredientGroups([...ingredientGroupsData, defaultIngredientGroup])
    resetErrors()
  }

  const handleIngredientGroupInputChange = (index: number, data: IngredientGroup) => {
    const ingredientGroupsData = [...ingredientGroups]
    ingredientGroupsData[index] = data
    setIngredientGroups(ingredientGroupsData)
    resetErrors()
  }

  const handleIngredientGroupInputDelete = (index: number) => {
    const ingredientGroupsData = [...ingredientGroups]
    ingredientGroupsData.splice(index, 1)
    setIngredientGroups(ingredientGroupsData)
    resetErrors()
  }

  const handleIngredientInputAdd = (index: number) => {
    const ingredientGroupsData = [...ingredientGroups]
    const ingredientGroup = ingredientGroupsData[index]

    ingredientGroup.ingredients = [...ingredientGroup.ingredients, defaultIngredient]
    setIngredientGroups(ingredientGroupsData)
    resetErrors()
  }

  const handleIngredientInputChange = (
    index: number,
    ingredientIndex: number,
    data: Ingredient
  ) => {
    const ingredientGroupsData = [...ingredientGroups]
    const ingredientGroup = ingredientGroupsData[index]

    ingredientGroup.ingredients[ingredientIndex] = data
    setIngredientGroups(ingredientGroupsData)
    resetErrors()
  }

  const handleIngredientInputDelete = (index: number, ingredientIndex: number) => {
    const ingredientGroupsData = [...ingredientGroups]
    const ingredientGroup = ingredientGroupsData[index]
    const ingredientsData = [...ingredientGroup.ingredients]

    ingredientsData.splice(ingredientIndex, 1)
    ingredientGroup.ingredients = ingredientsData

    setIngredientGroups(ingredientGroupsData)
    resetErrors()
  }

  const validate = () => {
    const ingredientGroupErrorsData = ingredientGroups
      .filter((ingredientGroup) => ingredientGroup.title === '')
      .map((group) => ({
        index: ingredientGroups.indexOf(group),
        message: 'This field cannot be empty. If group is redundant, please remove it.',
      }))

    const ingredientErrorsData = ingredientGroups.flatMap((ingredientGroup) =>
      ingredientGroup.ingredients.flatMap((ingredient) =>
        Object.values(ingredient)
          .filter((val) => val === '')
          .map(() => ({
            index: ingredientGroup.ingredients.indexOf(ingredient),
            message:
              'None of these fields can be empty. If ingredient is redundant, please remove it.',
          }))
      )
    )

    setIngredientErrors(ingredientErrorsData)
    setIngredientGroupErrors(ingredientGroupErrorsData)
  }

  return (
    <div className="space-y-10">
      <Header title="Add ingredients for recipe" />
      <Card>
        <Card.Form
          title="Add ingredients"
          subtitle="Add ingredients and amounts to recipe"
          form={
            <CreateIngredientsForm
              ingredientGroups={ingredientGroups}
              ingredientErrors={ingredientErrors}
              ingredientGroupsErrors={ingredientGroupErrors}
              units={unitsOptions || []}
              ingredientOptions={ingredientOptions || []}
              onIngredientInputAdd={handleIngredientInputAdd}
              onIngredientInputChange={handleIngredientInputChange}
              onIngredientInputDelete={handleIngredientInputDelete}
              onIngredientGroupInputAdd={handleIngredientGroupInputAdd}
              onIngredientGroupInputChange={handleIngredientGroupInputChange}
              onIngredientGroupInputDelete={handleIngredientGroupInputDelete}
            />
          }
        />
        <div className={`flex space-x-3 justify-end py-4 border-t ${classes.border}`}>
          <Button variant="default">Cancel</Button>
          <Button onClick={() => validate()}>Continue</Button>
        </div>
      </Card>
    </div>
  )
}

function RecipeIngredientsCreate() {
  const ingredients = useFetch<IngredientListOutAPIResponse>(urls.recipes.ingredients.list())

  return (
    <View<object, RecipeIngredientsCreateInnerProps>
      results={{ ingredients }}
      component={RecipeIngredientsCreateInner}
      componentProps={{}}
      loadingProps={{ description: 'Loading ingredients' }}
      errorProps={{ description: 'There was an error loading ingredients, please try again.' }}
    />
  )
}

export { RecipeIngredientsCreate }
