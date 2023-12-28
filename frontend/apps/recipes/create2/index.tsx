import { Title } from '@mantine/core'
import { useState } from 'react'

import { Button } from '../../../components/Button'
import { Card } from '../../../components/Card'
import Form from '../../../components/Form'
import View from '../../../components/View'
import { useFetch } from '../../../hooks/fetcher'
import { useForm } from '../../../hooks/forms'
import { type RecipeIngredientRecordListAPIResponse, type RecipeCreateForm } from '../../../types'
import { urls } from '../../urls'
import { type IngredientGroup, type Ingredient } from '../forms/RecipeIngredientsForm'
import { type Step } from '../forms/RecipeStepsForm'

import { IngredientsFormCard } from './components/IngredientsFormCard'

interface RecipeCreateInnerProps {
  results: {
    ingredients: RecipeIngredientRecordListAPIResponse
  }
}

function RecipeCreateInner({ results }: RecipeCreateInnerProps) {
  const { data: ingredients } = results.ingredients
  const recipeForm = useForm({ key: 'RecipeCreateForm' })

  /***************************
   ** IngredientGroup: data **
   ***************************/

  const defaultIngredient = { ingredient: '', portionQuantity: '', unit: '', additionalInfo: '' }
  const defaultIngredientGroup = { title: '', order: '', ingredients: [defaultIngredient] }
  // TODO: Replace IngredientGroup with generated type.
  const [ingredientGroups, setIngredientGroups] = useState<IngredientGroup[]>([
    defaultIngredientGroup,
  ])

  /*******************************
   ** IngredientGroup: handlers **
   *******************************/

  const handleIngredientGroupInputAdd = () => {
    const ingredientGroupsData = [...ingredientGroups]
    setIngredientGroups([...ingredientGroupsData, defaultIngredientGroup])
  }

  const handleIngredientGroupInputChange = (index: number, data: IngredientGroup) => {
    const ingredientGroupsData = [...ingredientGroups]
    ingredientGroupsData[index] = data
    setIngredientGroups(ingredientGroupsData)
  }

  const handleIngredientGroupInputDelete = (index: number) => {
    const ingredientGroupsData = [...ingredientGroups]
    ingredientGroupsData.splice(index, 1)
    setIngredientGroups(ingredientGroupsData)
  }

  const handleIngredientGroupSequenceChange = (data: IngredientGroup[]) =>
    setIngredientGroups([...data])

  /**************************
   ** Ingredient: handlers **
   **************************/

  const handleIngredientInputAdd = (index: number) => {
    const ingredientGroupsData = [...ingredientGroups]
    const ingredientGroup = ingredientGroupsData[index]

    ingredientGroup.ingredients = [...ingredientGroup.ingredients, defaultIngredient]
    setIngredientGroups(ingredientGroupsData)
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
  }

  const handleIngredientInputDelete = (index: number, ingredientIndex: number) => {
    const ingredientGroupsData = [...ingredientGroups]
    const ingredientGroup = ingredientGroupsData[index]
    const ingredientsData = [...ingredientGroup.ingredients]

    ingredientsData.splice(ingredientIndex, 1)
    ingredientGroup.ingredients = ingredientsData

    setIngredientGroups(ingredientGroupsData)
  }

  /*****************
   ** Steps: data **
   *****************/
  const defaultStep = {
    instruction: '',
    duration: 0,
    type: '',
    ingredientItems: [],
  }
  const [steps, setSteps] = useState<Step[]>([defaultStep])
  const selectedIngredientItems = steps.flatMap((step) => step.ingredientItems)

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <Title weight={600}>Create recipe</Title>
        <Button>Save</Button>
      </div>
      <Card>
        <Card.Form
          title="Recipe information"
          subtitle="Specify basic recipe information"
          form={<Form<RecipeCreateForm> {...recipeForm} />}
        />
      </Card>
      <IngredientsFormCard
        ingredients={ingredients}
        ingredientGroups={ingredientGroups}
        onSequenceChange={handleIngredientGroupSequenceChange}
        onIngredientInputAdd={handleIngredientInputAdd}
        onIngredientInputChange={handleIngredientInputChange}
        onIngredientInputDelete={handleIngredientInputDelete}
        onIngredientGroupInputAdd={handleIngredientGroupInputAdd}
        onIngredientGroupInputChange={handleIngredientGroupInputChange}
        onIngredientGroupInputDelete={handleIngredientGroupInputDelete}
      />
    </div>
  )
}

function RecipeCreate2() {
  const ingredients = useFetch<RecipeIngredientRecordListAPIResponse>(
    urls.recipes.ingredients.list()
  )

  return (
    <View<object, RecipeCreateInnerProps>
      results={{ ingredients: ingredients }}
      component={RecipeCreateInner}
      componentProps={{}}
      loadingProps={{ description: 'Loading' }}
      errorProps={{ description: 'There was an error loading, please try again.' }}
    />
  )
}

export { RecipeCreate2 }
