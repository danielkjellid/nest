import {
  type RecipeCreateIn,
  type RecipeEditIn,
  type IngredientItem,
  type RecipeIngredientItemRecord,
  type RecipeStepRecord,
  type Step,
  type IngredientGroupItem,
  type RecipeIngredientItemGroupRecord,
} from '../../../../types'

import {
  type Recipe,
  type IngredientItem as FormIngredientItem,
  type Step as FormStep,
  type IngredientItemGroup as FromIngredientItemGroup,
} from './types'

const makeIngredientItemType = (
  ingredientItem: RecipeIngredientItemRecord | FormIngredientItem
): IngredientItem => ({
  id: 'id' in ingredientItem ? ingredientItem.id : undefined,
  ingredient: ingredientItem.ingredient.id.toString(),
  portionQuantity: ingredientItem.portionQuantity.toString(),
  portionQuantityUnit: ingredientItem.portionQuantityUnit.id.toString(),
  additionalInfo: ingredientItem.additionalInfo || undefined,
})

const makeStepType = (step: FormStep | RecipeStepRecord, index: number): Step => ({
  id: 'id' in step ? step.id : undefined,
  instruction: step.instruction,
  stepType: step.stepType,
  duration: step.duration,
  number: index + 1,
  ingredientItems: step.ingredientItems.map((ingredientItem: any) =>
    makeIngredientItemType(ingredientItem)
  ),
})

const makeIngredientItemGroupType = (
  ingredientGroup: FromIngredientItemGroup | RecipeIngredientItemGroupRecord
): IngredientGroupItem => ({
  id: 'id' in ingredientGroup ? ingredientGroup.id : undefined,
  title: ingredientGroup.title,
  ordering: ingredientGroup.ordering,
  ingredientItems: ingredientGroup.ingredientItems.map((ingredientItem) =>
    makeIngredientItemType(ingredientItem)
  ),
})

const makePayload = (recipeData: Recipe): RecipeCreateIn | RecipeEditIn => ({
  baseRecipe: { ...recipeData.baseRecipe },
  steps: [...recipeData.steps.map((step, index) => makeStepType(step, index))],
  ingredientItemGroups: [
    ...recipeData.ingredientItemGroups.map((ingredientGroup) =>
      makeIngredientItemGroupType(ingredientGroup)
    ),
  ],
})

export { makePayload }
