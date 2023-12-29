import { Title } from '@mantine/core'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { Button } from '../../../components/Button'
import { Card } from '../../../components/Card'
import Form from '../../../components/Form'
import View from '../../../components/View'
import { useUnits } from '../../../contexts/UnitsProvider'
import { useFetch } from '../../../hooks/fetcher'
import { useForm } from '../../../hooks/forms'
import { useCommonStyles } from '../../../styles/common'
import {
  type RecipeIngredientRecordListAPIResponse,
  type RecipeCreateForm,
  type RecipeIngredientRecord,
  type UnitRecord,
  type RecipeStepType,
} from '../../../types'
import { urls } from '../../urls'
import { RecipeIngredientsForm } from '../forms/RecipeIngredientsForm'
import { RecipeStepsForm } from '../forms/RecipeStepsForm'

import {
  type IngredientItem,
  type IngredientItemGroup,
  type IngredientGroupActions,
  type Step,
  type StepActions,
  type ActionFunc,
} from './types'

interface RecipeCreateInnerProps {
  results: {
    ingredients: RecipeIngredientRecordListAPIResponse
  }
}

function RecipeCreateInner({ results }: RecipeCreateInnerProps) {
  const { units, unitsOptions } = useUnits()
  const { data: ingredients } = results.ingredients
  const { classes } = useCommonStyles()

  const recipeForm = useForm({ key: 'RecipeCreateForm' })
  const navigate = useNavigate()

  /***************************
   ** IngredientGroup: data **
   ***************************/

  const defaultIngredient = {
    ingredient: {} as RecipeIngredientRecord,
    portionQuantityUnit: {} as UnitRecord,
    portionQuantity: 0,
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

  const ingredientGroupActions: IngredientGroupActions = {
    groupAdd: function () {
      const ingredientGroupsData = [...ingredientGroups]
      setIngredientGroups([...ingredientGroupsData, defaultIngredientGroup])
    },
    groupChange: function (index: number, data: IngredientItemGroup) {
      const ingredientGroupsData = [...ingredientGroups]
      ingredientGroupsData[index] = data
      setIngredientGroups(ingredientGroupsData)
    },
    groupDelete: function (index: number) {
      const ingredientGroupsData = [...ingredientGroups]
      ingredientGroupsData.splice(index, 1)
      setIngredientGroups(ingredientGroupsData)
    },
    groupSequenceChange: function (data: IngredientItemGroup[]) {
      setIngredientGroups([...data])
    },
    inputAdd: function (index: number) {
      const ingredientGroupsData = [...ingredientGroups]
      const ingredientGroup = ingredientGroupsData[index]

      ingredientGroup.ingredientItems = [...ingredientGroup.ingredientItems, defaultIngredient]
      setIngredientGroups(ingredientGroupsData)
    },
    inputChange: function (index: number, ingredientIndex: number, data: IngredientItem) {
      const ingredientGroupsData = [...ingredientGroups]
      const ingredientGroup = ingredientGroupsData[index]

      ingredientGroup.ingredientItems[ingredientIndex] = data
      setIngredientGroups(ingredientGroupsData)
      console.log(ingredientGroups)
    },
    inputDelete: function (index: number, ingredientIndex: number) {
      const ingredientGroupsData = [...ingredientGroups]
      const ingredientGroup = ingredientGroupsData[index]
      const ingredientsData = [...ingredientGroup.ingredientItems]

      ingredientsData.splice(ingredientIndex, 1)
      ingredientGroup.ingredientItems = ingredientsData

      setIngredientGroups(ingredientGroupsData)
    },
  }

  const handleIngredientGroupAction: ActionFunc<IngredientGroupActions> = (action, ...params) => {
    // @ts-ignore
    return ingredientGroupActions[action](...params)
  }

  /*****************
   ** Steps: data **
   *****************/

  const defaultStep = {
    instruction: '',
    duration: 0,
    stepType: '' as RecipeStepType,
    ingredientItems: [],
  }
  const [steps, setSteps] = useState<Step[]>([defaultStep])

  const stepActions: StepActions = {
    inputAdd: function () {
      const stepsData = [...steps]
      setSteps([...stepsData, defaultStep])
    },
    inputChange: function (index: number, data: Step) {
      const stepsData = [...steps]
      stepsData[index] = data

      setSteps(stepsData)
    },
    inputDelete: function (index: number) {
      const stepsData = [...steps]
      stepsData.splice(index, 1)
      setSteps(stepsData)
    },
    stepSequenceChange: function (data) {
      setSteps([...data])
    },
  }

  const handleStepAction: ActionFunc<StepActions> = (action, ...params) => {
    // @ts-ignore
    return stepActions[action](...params)
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <Title weight={600}>Create recipe</Title>
      </div>
      <Card>
        <Card.Form
          title="Recipe information"
          subtitle="Specify basic recipe information"
          form={<Form<RecipeCreateForm> {...recipeForm} />}
        />
        <Card.Form
          title="Add ingredients"
          subtitle="Add ingredients and amounts to recipe. If one ingredient is needed within multiple groups, add it to each group respectively."
          form={
            <RecipeIngredientsForm
              ingredients={ingredients}
              ingredientGroups={ingredientGroups}
              units={units}
              unitOptions={unitsOptions}
              onAction={handleIngredientGroupAction}
            />
          }
        />
        <Card.Form
          title="Add steps"
          subtitle="Add steps to recipe"
          form={
            <RecipeStepsForm
              steps={steps}
              ingredientGroups={ingredientGroups}
              onAction={handleStepAction}
            />
          }
        />
        <div className={`flex space-x-3 justify-end py-4 border-t ${classes.border}`}>
          <Button variant="default" onClick={() => navigate(-1)}>
            Cancel
          </Button>
          <Button>Save</Button>
        </div>
      </Card>
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
