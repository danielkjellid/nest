import React from 'react'
import { Card } from '../../../components/Card'
import { Button } from '../../../components/Button'

import { Header } from './components/Header'
import { useCommonStyles } from '../../../styles/common'
import View from '../../../components/View'
import { useFetch } from '../../../hooks/fetcher'
import { IngredientListOut, IngredientListOutAPIResponse } from '../../../types'
import { urls } from '../../urls'

interface CreateIngredientFormProps {
  ingredients: IngredientListOut[]
}

function CreateIngredientsForm({ ingredients }: CreateIngredientFormProps) {
  return <p>Form</p>
}

interface RecipeIngredientsCreateInnerProps {
  results: {
    ingredients: IngredientListOutAPIResponse
  }
}

function RecipeIngredientsCreateInner({ results }: RecipeIngredientsCreateInnerProps) {
  const { data: ingredients } = results.ingredients
  const { classes } = useCommonStyles()

  return (
    <div className="space-y-10">
      <Header title="Add ingredients for recipe" />
      <Card>
        <Card.Form
          title="Add ingredients"
          subtitle="Add ingredients and amounts to recipe"
          form={<CreateIngredientsForm ingredients={ingredients || []} />}
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
