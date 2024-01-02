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
  type RecipeCreateIn,
} from '../../../types'
import { urls } from '../../urls'

import { RecipeIngredientsForm } from './components/RecipeIngredientsForm'
import { RecipeStepsForm } from './components/RecipeStepsForm'
import {
  type IngredientItem,
  type IngredientItemGroup,
  type IngredientGroupActions,
  type Step,
  type StepActions,
  type ActionFunc,
  type FormError,
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

  const recipeForm = useForm<RecipeCreateForm>({ key: 'RecipeCreateForm' })
  const navigate = useNavigate()

  /***************************
   ** IngredientGroup: data **
   ***************************/

  const defaultIngredient = {
    ingredient: {} as RecipeIngredientRecord,
    portionQuantityUnit: {} as UnitRecord,
    portionQuantity: '',
    additionalInfo: '',
  }
  const defaultIngredientGroup = { title: '', ordering: 0, ingredientItems: [defaultIngredient] }
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
      resetValidation()
    },
    groupChange: function (index: number, data: IngredientItemGroup) {
      const ingredientGroupsData = [...ingredientGroups]
      ingredientGroupsData[index] = data
      setIngredientGroups(ingredientGroupsData)
      resetValidation()
    },
    groupDelete: function (index: number) {
      const ingredientGroupsData = [...ingredientGroups]
      ingredientGroupsData.splice(index, 1)
      setIngredientGroups(ingredientGroupsData)
      resetValidation()
    },
    groupSequenceChange: function (data: IngredientItemGroup[]) {
      setIngredientGroups([...data])
      resetValidation()
    },
    inputAdd: function (index: number) {
      const ingredientGroupsData = [...ingredientGroups]
      const ingredientGroup = ingredientGroupsData[index]

      ingredientGroup.ingredientItems = [...ingredientGroup.ingredientItems, defaultIngredient]
      setIngredientGroups(ingredientGroupsData)
      resetValidation()
    },
    inputChange: function (index: number, ingredientIndex: number, data: IngredientItem) {
      const ingredientGroupsData = [...ingredientGroups]
      const ingredientGroup = ingredientGroupsData[index]

      ingredientGroup.ingredientItems[ingredientIndex] = data
      setIngredientGroups(ingredientGroupsData)
      resetValidation()
    },
    inputDelete: function (index: number, ingredientIndex: number) {
      const ingredientGroupsData = [...ingredientGroups]
      const ingredientGroup = ingredientGroupsData[index]
      const ingredientsData = [...ingredientGroup.ingredientItems]

      ingredientsData.splice(ingredientIndex, 1)
      ingredientGroup.ingredientItems = ingredientsData

      setIngredientGroups(ingredientGroupsData)
      resetValidation()
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

  /*********************
   ** Steps: handlers **
   *********************/

  const stepActions: StepActions = {
    inputAdd: function () {
      const stepsData = [...steps]
      setSteps([...stepsData, defaultStep])
      resetValidation()
    },
    inputChange: function (index: number, data: Step) {
      const stepsData = [...steps]
      stepsData[index] = data
      setSteps(stepsData)
      resetValidation()
    },
    inputDelete: function (index: number) {
      const stepsData = [...steps]
      stepsData.splice(index, 1)
      setSteps(stepsData)
      resetValidation()
    },
    stepSequenceChange: function (data) {
      setSteps([...data])
      resetValidation()
    },
  }

  const handleStepAction: ActionFunc<StepActions> = (action, ...params) => {
    // @ts-ignore
    return stepActions[action](...params)
  }

  const makeIngredientItemFromIngredient = (ingredientItem: IngredientItem) => ({
    // TODO: Make sure we're able to do .toString()
    ...ingredientItem,
    ingredient: ingredientItem.ingredient.id.toString(),
    portionQuantity: ingredientItem.portionQuantity.toString(),
    portionQuantityUnit: ingredientItem.portionQuantityUnit.id.toString(),
    additionalInfo: ingredientItem.additionalInfo || undefined,
  })

  /****************
   ** Validation **
   ****************/

  const checkEmptyValue = (val: any) =>
    val === '' || (typeof val === 'object' && !Array.isArray(val) && !Object.keys(val).length)

  const [ingredientGroupErrors, setIngredientGroupErrors] = useState<FormError | null>(null)

  const validateIngredientGroups = () => {
    const errors: FormError = {}
    ingredientGroups.map((ingredientGroup, index) =>
      Object.values(ingredientGroup).map((val) => {
        console.log(val)
        if (checkEmptyValue(val)) {
          errors[index] = ['This field cannot be empty.']
        }
      })
    )

    setIngredientGroupErrors({ ...errors })
    return !!Object.keys(errors).length
  }

  const [ingredientItemsErrors, setIngredientItemsErrors] = useState<FormError | null>(null)

  const validateIngredientItems = () => {
    const errors: FormError = {}
    ingredientGroups.map((ingredientGroup) =>
      ingredientGroup.ingredientItems.map((ingredientItem, index) =>
        Object.entries(ingredientItem).map(([key, val]) => {
          if (key !== 'additionalInfo' && checkEmptyValue(val)) {
            errors[index] = ['These fields cannot be empty, if redundant please remove it.']
          }
        })
      )
    )

    setIngredientItemsErrors({ ...errors })
    return !!Object.keys(errors).length
  }

  const validate = (): boolean => {
    // recipeForm.validate()
    const groupsValid = validateIngredientGroups()
    const itemsValid = validateIngredientItems()

    return groupsValid && itemsValid
    // validateSteps()
  }

  const resetValidation = () => {
    setIngredientGroupErrors(null)
    setIngredientItemsErrors(null)
  }

  /*********************
   ** Recipe creation **
   *********************/

  const makePayload = (): RecipeCreateIn => ({
    // TODO: validate that data is set
    baseRecipe: { ...recipeForm.buildPayload() },
    steps: steps.map((step, index) => ({
      ...step,
      number: index + 1,
      ingredientItems: step.ingredientItems.map((ingredientItem) =>
        makeIngredientItemFromIngredient(ingredientItem)
      ),
    })),
    ingredientItemGroups: ingredientGroups.map((ingredientGroup) => ({
      ...ingredientGroup,
      ingredients: ingredientGroup.ingredientItems
        .map((ingredientItem) => makeIngredientItemFromIngredient(ingredientItem))
        .filter((val) => val !== undefined),
    })),
  })

  const addRecipe = async () => {
    const isValid = validate()

    if (!isValid) return
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
              ingredientGroupErrors={ingredientGroupErrors || {}}
              ingredientItemsErrors={ingredientItemsErrors || {}}
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
          <Button onClick={() => validate()}>Save</Button>
        </div>
      </Card>
    </div>
  )
}

function RecipeCreate() {
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

export { RecipeCreate }
