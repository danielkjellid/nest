import React, { useMemo } from 'react'
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

interface IngredientInputProps {
  units: UnitOption[]
  ingredients: IngredientListOut[]
}

function IngredientInput({ ingredients, units }: IngredientInputProps) {
  return (
    <div className="relative">
      <div className="rounded-bl-md absolute bottom-0 w-8 h-8 mb-4 ml-3 bg-transparent border-b-2 border-l-2 border-gray-200" />
      <div className="flex items-end w-full space-x-2">
        <TextInput label="Ingredient" required className="w-full ml-10" />
        <TextInput label="Amount" required className="w-64 ml-10" />
        <Select label="Unit" required className="w-64 ml-10" data={units} />
        <ActionIcon className="mb-1" color="red">
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
          <IngredientInput ingredients={ingredients} units={units} />
          <IngredientInput ingredients={ingredients} units={units} />
          <IngredientInput ingredients={ingredients} units={units} />
        </div>
      </div>
      <ActionIcon color="green" variant="light" className="mt-3 ml-10">
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
