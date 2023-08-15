import React, { useMemo, useState } from 'react'
import { Card } from '../../../components/Card'
import { Button } from '../../../components/Button'
import { DragDropContext, Droppable } from 'react-beautiful-dnd'

import { Header } from './components/Header'
import { useCommonStyles } from '../../../styles/common'
import View from '../../../components/View'
import { useFetch } from '../../../hooks/fetcher'
import { IngredientListOutAPIResponse } from '../../../types'
import { urls } from '../../urls'
import { useUnits, UnitOption } from '../../../contexts/UnitsProvider'
import {
  Ingredient,
  IngredientGroup,
  IngredientOptionType,
  IngredientGroupInput,
} from './components/IngredientGroupInput'
import { performPost } from '../../../hooks/fetcher/http'
import { useDragAndDropSingleList } from '../../../hooks/drag-and-drop'

export interface FormError {
  index: number
  message: string
}

interface CreateIngredientFormProps {
  units: UnitOption[]
  ingredientGroups: IngredientGroup[]
  ingredientGroupsErrors: FormError[]
  ingredientOptions: IngredientOptionType[]
  ingredientErrors: FormError[]
  onSequenceChange: (ingredientGroups: IngredientGroup[]) => void
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
  onSequenceChange,
  onIngredientInputAdd,
  onIngredientInputChange,
  onIngredientInputDelete,
  onIngredientGroupInputAdd,
  onIngredientGroupInputChange,
  onIngredientGroupInputDelete,
}: CreateIngredientFormProps) {
  const { onDragEnd, onDragStart } = useDragAndDropSingleList({
    items: ingredientGroups,
    onSequenceChange,
  })

  return (
    <DragDropContext onDragStart={onDragStart} onDragEnd={onDragEnd}>
      <div className="flex items-center justify-end mb-1 space-x-2">
        <Button variant="light" compact onClick={onIngredientGroupInputAdd}>
          Add group
        </Button>
      </div>
      <div>
        <Droppable
          droppableId="ingredientGroups"
          ignoreContainerClipping
          isDropDisabled={ingredientGroups.length <= 1}
        >
          {(provided, snapshot) => (
            <div ref={provided.innerRef} {...provided.droppableProps} className="space-y-4">
              {ingredientGroups.map((ingredientGroup, index) => (
                <IngredientGroupInput
                  key={index}
                  isDragDisabled={ingredientGroups.length <= 1}
                  draggableId={index.toString()}
                  order={index}
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
              {provided.placeholder}
              {!snapshot.isDraggingOver}
            </div>
          )}
        </Droppable>
      </div>
    </DragDropContext>
  )
}

interface RecipeIngredientsCreateInnerProps {
  results: {
    ingredients: IngredientListOutAPIResponse
  }
}

function RecipeIngredientsCreateInner({ results }: RecipeIngredientsCreateInnerProps) {
  const { classes } = useCommonStyles()
  const { unitsOptions } = useUnits()

  /**********
   ** Data **
   **********/

  const { data: ingredients } = results.ingredients
  const defaultIngredient = { ingredient: '', portionQuantity: '', unit: '', additionalInfo: '' }
  const defaultIngredientGroup = { title: '', order: '', ingredients: [defaultIngredient] }
  const [ingredientGroups, setIngredientGroups] = useState<IngredientGroup[]>([
    defaultIngredientGroup,
  ])

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

  /************
   ** Errors **
   ************/

  const [ingredientErrors, setIngredientErrors] = useState<FormError[]>([])
  const [ingredientGroupErrors, setIngredientGroupErrors] = useState<FormError[]>([])

  const resetErrors = () => {
    if (ingredientGroupErrors.length) {
      setIngredientGroupErrors([])
    }

    if (ingredientErrors.length) {
      setIngredientErrors([])
    }
  }

  /*******************************
   ** IngredientGroup: handlers **
   *******************************/

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

  const handleSequenceChange = (data: IngredientGroup[]) => {
    setIngredientGroups([...data])
  }

  /**************************
   ** Ingredient: handlers **
   **************************/

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

  /****************
   ** Validators **
   ****************/

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

  /********************
   ** Submit handler **
   ********************/

  const addIngredients = async () => {
    validate()

    if (!ingredientErrors.length && !ingredientGroupErrors.length) {
      const payload = ingredientGroups.map((ingredientGroup, index) => ({
        ...ingredientGroup,
        ordering: index + 1,
      }))

      await performPost({ url: '/api/v1/recipes/1/ingredients/create/', data: payload })
    }
  }

  return (
    <div className="space-y-10">
      <Header title="Add ingredients for recipe" />
      <Card>
        <Card.Form
          title="Add ingredients"
          subtitle="Add ingredients and amounts to recipe. If one ingredient is needed within multiple groups, add it to each group respectively."
          form={
            <CreateIngredientsForm
              ingredientGroups={ingredientGroups}
              ingredientErrors={ingredientErrors}
              ingredientGroupsErrors={ingredientGroupErrors}
              units={unitsOptions || []}
              ingredientOptions={ingredientOptions || []}
              onSequenceChange={handleSequenceChange}
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
          <Button onClick={() => addIngredients()}>Continue</Button>
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
