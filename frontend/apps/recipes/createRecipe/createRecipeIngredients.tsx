import React, { useEffect, useMemo, useState } from 'react'
import { Card } from '../../../components/Card'
import { Button } from '../../../components/Button'

import { Header } from './components/Header'
import { useCommonStyles } from '../../../styles/common'
import View from '../../../components/View'
import { useFetch } from '../../../hooks/fetcher'
import { IngredientListOut, IngredientListOutAPIResponse } from '../../../types'
import { urls } from '../../urls'
import { ActionIcon, Select, TextInput } from '@mantine/core'
import { IconPlus, IconX } from '@tabler/icons-react'
import { useUnits, UnitOption } from '../../../contexts/UnitsProvider'

interface Ingredient {
  ingredient: string
  amount: string
  unit: UnitOption['value']
}

interface IngredientInputProps {
  units: UnitOption[]
  ingredient: Ingredient
  ingredients: IngredientListOut[]
  onInputDelete: () => void
  onInputChange: (data: Ingredient) => void
}

function IngredientInput({
  ingredient,
  ingredients,
  units,
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
        <TextInput
          label="Ingredient"
          value={ingredient.ingredient}
          required
          className="w-full ml-10"
          onChange={(event) => handleInputChange('ingredient', event)}
        />
        <TextInput
          label="Amount"
          value={ingredient.amount}
          required
          className="w-64 ml-10"
          onChange={(event) => handleInputChange('amount', event)}
        />
        <Select
          label="Unit"
          value={ingredient.unit}
          required
          className="w-64 ml-10"
          data={units}
          onChange={(event) => handleInputChange('unit', event)}
        />
        <ActionIcon className="mb-1" color="red" onClick={() => onInputDelete()}>
          <IconX />
        </ActionIcon>
      </div>
    </div>
  )
}

interface IngredientGroupInputProps {
  units: UnitOption[]
  ingredients: IngredientListOut[]
}

function IngredientGroupInput({ ingredients, units }: IngredientGroupInputProps) {
  const defaultObj = { ingredient: '', amount: '', unit: '' }
  const [addedIngredients, setAddedIngredients] = useState<(typeof defaultObj)[]>([defaultObj])

  const addNewInput = () => {
    setAddedIngredients([...addedIngredients, defaultObj])
  }

  const handleRemoveInput = (index: number) => {
    console.log(index)
    console.log(addedIngredients[index])
    const ingredientCopy = [...addedIngredients]
    ingredientCopy.splice(index, 1)
    setAddedIngredients(ingredientCopy)
  }

  const handleInputChange = (index: number, data: Ingredient) => {
    const ingredientCopy = [...addedIngredients]
    ingredientCopy[index] = data
    setAddedIngredients(ingredientCopy)
  }

  return (
    <div>
      <TextInput label="Ingredient group name" className="z-25" required />
      <div className="relative">
        <div
          style={{ height: 'calc(100% - 20px)' }}
          className="absolute left-3 w-0.5 bg-gray-200 -mt-4"
          aria-hidden
        />
        <div className="relative mt-4 space-y-4">
          {addedIngredients.map((ingredient, index) => (
            <IngredientInput
              key={index}
              ingredient={ingredient}
              ingredients={ingredients}
              units={units}
              onInputDelete={() => handleRemoveInput(index)}
              onInputChange={(data) => handleInputChange(index, data)}
            />
          ))}
        </div>
      </div>
      <ActionIcon
        color="green"
        variant="light"
        className="mt-3 ml-10"
        onClick={() => addNewInput()}
      >
        <IconPlus />
      </ActionIcon>
    </div>
  )
}

interface CreateIngredientFormProps {
  units: UnitOption[]
  ingredients: IngredientListOut[]
}

function CreateIngredientsForm({ ingredients, units }: CreateIngredientFormProps) {
  return (
    <div className="space-y-4">
      <IngredientGroupInput ingredients={ingredients} units={units} />
      <Button variant="light" compact>
        Add group
      </Button>
    </div>
  )
}

interface RecipeIngredientsCreateInnerProps {
  results: {
    ingredients: IngredientListOutAPIResponse
  }
}

function RecipeIngredientsCreateInner({ results }: RecipeIngredientsCreateInnerProps) {
  const { data: ingredients } = results.ingredients
  const { classes } = useCommonStyles()

  const memoedIngredients = useMemo(() => ingredients, [ingredients])
  const { unitsOptions } = useUnits()

  return (
    <div className="space-y-10">
      <Header title="Add ingredients for recipe" />
      <Card>
        <Card.Form
          title="Add ingredients"
          subtitle="Add ingredients and amounts to recipe"
          form={
            <CreateIngredientsForm
              ingredients={memoedIngredients || []}
              units={unitsOptions || []}
            />
          }
        />
        <div className={`flex space-x-3 justify-end py-4 border-t ${classes.border}`}>
          <Button variant="default">Cancel</Button>
          <Button>Continue</Button>
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
