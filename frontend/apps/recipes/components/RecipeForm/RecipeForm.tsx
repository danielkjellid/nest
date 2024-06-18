import { Title } from '@mantine/core'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { Button } from '../../../../components/Button'
import { Card } from '../../../../components/Card'
import Form from '../../../../components/Form'
import { useUnits } from '../../../../contexts/UnitsProvider'
import { useForm } from '../../../../hooks/forms'
import { useCommonStyles } from '../../../../styles/common'
import {
  type RecipeIngredientRecord,
  type UnitRecord,
  type RecipeStepType,
  type RecipeDetailRecord,
  type RecipeCreateForm,
} from '../../../../types'

import { RecipeIngredientsForm } from './RecipeIngredientsForm'
import { RecipeStepsForm } from './RecipeStepsForm'
import {
  type IngredientItem,
  type IngredientItemGroup,
  type IngredientGroupActions,
  type Step,
  type StepActions,
  type ActionFunc,
  type FormError,
  type Recipe,
} from './types'

interface RecipeFormProps {
  recipe?: RecipeDetailRecord
  ingredients: RecipeIngredientRecord[]
  onSubmit: (recipe: Recipe) => void
}

function RecipeForm({ recipe, ingredients, onSubmit }: RecipeFormProps) {
  const { units, unitsOptions } = useUnits()
  const { classes } = useCommonStyles()
  const recipeData = recipe || ({} as RecipeDetailRecord)

  const recipeForm = useForm<RecipeCreateForm | RecipeDetailRecord>({
    key: 'RecipeCreateForm',
    initialData: Object.keys(recipeData).length ? recipeData : null,
  })
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
  const [ingredientGroups, setIngredientGroups] = useState<IngredientItemGroup[]>(
    structuredClone(recipeData?.ingredientItemGroups) || [defaultIngredientGroup]
  )

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

      const deletedIngredientItems = ingredientsData.splice(ingredientIndex, 1)
      ingredientGroup.ingredientItems = ingredientsData

      setIngredientGroups(ingredientGroupsData)

      // Update related steps as well so that they don't automatically get assigned the ingredient
      // if it's added back.
      const stepsData = [...steps]
      const deletedIngredientIds = deletedIngredientItems.map(
        (ingredientItem) => ingredientItem.ingredient.id
      )
      const stepsWithAssignedIngredientItem = steps.filter((step) =>
        step.ingredientItems.filter((ingredientItem) =>
          deletedIngredientIds.includes(ingredientItem.ingredient.id)
        )
      )

      stepsWithAssignedIngredientItem.forEach((step) => {
        const stepIndex = stepsData.indexOf(step)

        if (stepIndex === -1) return

        const ingredientsData = [...step.ingredientItems]
        ingredientsData.splice(ingredientIndex, 1)
        step.ingredientItems = ingredientsData

        stepsData[stepIndex] = step
      })
      setSteps(stepsData)
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
  const [steps, setSteps] = useState<Step[]>(
    // Step duration field is passed in seconds, as is the standard for duration fields.
    // Convert to minutes before passing it.
    structuredClone(
      recipeData?.steps?.map((step) => ({ ...step, duration: step.duration / 60 }))
    ) || [defaultStep]
  )

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

  /****************
   ** Validation **
   ****************/

  const checkEmptyValue = (val: any) =>
    val === '' ||
    (typeof val === 'object' && !Array.isArray(val) && !Object.keys(val).length) ||
    (Array.isArray(val) && !val.length)

  const [ingredientGroupErrors, setIngredientGroupErrors] = useState<FormError | null>(null)

  const validateIngredientGroups = () => {
    const errors: FormError = {}
    ingredientGroups.map((ingredientGroup, index) =>
      Object.values(ingredientGroup).map((val) => {
        if (checkEmptyValue(val)) {
          errors[index] = [{ message: 'This field cannot be empty.', field: null }]
        }
      })
    )

    setIngredientGroupErrors({ ...errors })
    return !Object.keys(errors).length
  }

  const [ingredientItemsErrors, setIngredientItemsErrors] = useState<FormError | null>(null)

  const validateIngredientItems = () => {
    const errors: FormError = {}
    ingredientGroups.map((ingredientGroup) =>
      ingredientGroup.ingredientItems.map((ingredientItem, index) =>
        Object.entries(ingredientItem).map(([key, val]) => {
          if (key !== 'additionalInfo' && checkEmptyValue(val)) {
            errors[index] = [
              {
                message: 'These fields cannot be empty, if redundant please remove it.',
                field: null,
              },
            ]
          }
        })
      )
    )

    setIngredientItemsErrors({ ...errors })
    return !Object.keys(errors).length
  }

  const [stepsErrors, setStepsErrors] = useState<FormError | null>(null)

  const validateSteps = () => {
    const errors: FormError = {}
    steps.map((step, index) =>
      Object.entries(step).map(([key, val]) => {
        const existingError = errors[index] || []
        if (key !== 'ingredientItems' && checkEmptyValue(val)) {
          errors[index] = [{ message: 'This field cannot be empty', field: key }, ...existingError]
        }

        if (key === 'duration' && val <= 0) {
          errors[index] = [
            { message: 'Duration must be higher than zero', field: key },
            ...existingError,
          ]
        }
      })
    )

    setStepsErrors({ ...errors })
    return !Object.keys(errors).length
  }

  const validate = (): boolean => {
    // const recipeValid = recipeForm.validate()
    const groupsValid = validateIngredientGroups()
    const itemsValid = validateIngredientItems()
    const stepsValid = validateSteps()

    return groupsValid && itemsValid && stepsValid
  }

  const resetValidation = () => {
    recipeForm.resetErrors()
    setIngredientGroupErrors(null)
    setIngredientItemsErrors(null)
    setStepsErrors(null)
  }

  /*********************
   ** Recipe creation **
   *********************/

  const submit = () => {
    const isValid = validate()

    if (!isValid) return

    const data: Recipe = {
      baseRecipe: { ...recipeForm.buildPayload().data },
      steps: steps,
      ingredientItemGroups: ingredientGroups,
    }
    onSubmit(data)
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
          form={<Form<RecipeDetailRecord | RecipeCreateForm> {...recipeForm} />}
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
              errors={stepsErrors || {}}
            />
          }
        />
        <div className={`flex space-x-3 justify-end py-4 border-t ${classes.border}`}>
          <Button variant="default" onClick={() => navigate(-1)}>
            Cancel
          </Button>
          <Button onClick={submit}>Save</Button>
        </div>
      </Card>
    </div>
  )
}

export { RecipeForm }
