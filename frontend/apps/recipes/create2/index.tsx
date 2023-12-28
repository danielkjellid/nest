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

import { IngredientsFormCard } from './components/IngredientsFormCard'
import { type IngredientItem, type IngredientItemGroup } from './types'

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

  const defaultIngredient = {
    ingredientId: '',
    portionQuantity: 0,
    portionQuantityUnitId: '',
    additionalInfo: '',
  }
  const defaultIngredientGroup = { title: '', ordering: 0, ingredientItems: [defaultIngredient] }
  // TODO: Replace IngredientGroup with generated type.
  const [ingredientGroups, setIngredientGroups] = useState<IngredientItemGroup[]>([
    defaultIngredientGroup,
  ])

  /*******************************
   ** IngredientGroup: handlers **
   *******************************/

  const handleIngredientGroupInputAdd = () => {
    const ingredientGroupsData = [...ingredientGroups]
    setIngredientGroups([...ingredientGroupsData, defaultIngredientGroup])
  }

  const handleIngredientGroupInputChange = (index: number, data: IngredientItemGroup) => {
    const ingredientGroupsData = [...ingredientGroups]
    ingredientGroupsData[index] = data
    setIngredientGroups(ingredientGroupsData)
  }

  const handleIngredientGroupInputDelete = (index: number) => {
    const ingredientGroupsData = [...ingredientGroups]
    ingredientGroupsData.splice(index, 1)
    setIngredientGroups(ingredientGroupsData)
  }

  const handleIngredientGroupSequenceChange = (data: IngredientItemGroup[]) =>
    setIngredientGroups([...data])

  /**************************
   ** Ingredient: handlers **
   **************************/

  const handleIngredientInputAdd = (index: number) => {
    const ingredientGroupsData = [...ingredientGroups]
    const ingredientGroup = ingredientGroupsData[index]

    ingredientGroup.ingredientItems = [...ingredientGroup.ingredientItems, defaultIngredient]
    setIngredientGroups(ingredientGroupsData)
  }

  const handleIngredientInputChange = (
    index: number,
    ingredientIndex: number,
    data: IngredientItem
  ) => {
    const ingredientGroupsData = [...ingredientGroups]
    const ingredientGroup = ingredientGroupsData[index]

    ingredientGroup.ingredientItems[ingredientIndex] = data
    setIngredientGroups(ingredientGroupsData)
    console.log(ingredientGroups)
  }

  const handleIngredientInputDelete = (index: number, ingredientIndex: number) => {
    const ingredientGroupsData = [...ingredientGroups]
    const ingredientGroup = ingredientGroupsData[index]
    const ingredientsData = [...ingredientGroup.ingredientItems]

    ingredientsData.splice(ingredientIndex, 1)
    ingredientGroup.ingredientItems = ingredientsData

    setIngredientGroups(ingredientGroupsData)
  }

  /*****************
   ** Steps: data **
   *****************/
  // const defaultStep = {
  //   instruction: '',
  //   duration: 0,
  //   type: '',
  //   ingredientItems: [],
  // }
  // const [steps, setSteps] = useState<Step[]>([defaultStep])
  // const selectedIngredientItems = steps.flatMap((step) => step.ingredientItems)

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
