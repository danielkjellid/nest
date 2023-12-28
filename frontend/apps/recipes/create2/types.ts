import {
  type RecipeIngredientItemGroupRecord,
  type RecipeIngredientItemRecord,
} from '../../../types'

export type IngredientItem = Pick<
  RecipeIngredientItemRecord,
  'ingredient' | 'portionQuantityUnit' | 'portionQuantity' | 'additionalInfo'
>
export interface IngredientItemGroup
  extends Pick<RecipeIngredientItemGroupRecord, 'title' | 'ordering'> {
  ingredientItems: IngredientItem[]
}

export interface IngredientGroupActions {
  groupAdd: () => void
  groupChange: (index: number, data: IngredientItemGroup) => void
  groupDelete: (index: number) => void
  groupSequenceChange: (data: IngredientItemGroup[]) => void
  inputAdd: (index: number) => void
  inputChange: (index: number, ingredientIndex: number, data: IngredientItem) => void
  inputDelete: (index: number, ingredientIndex: number) => void
}

export type IngredientGroupAction = keyof IngredientGroupActions
export type IngredientGroupActionParameter = Parameters<
  IngredientGroupActions[IngredientGroupAction]
>
export type IngredientGroupActionFunc = (
  action: IngredientGroupAction,
  ...params: IngredientGroupActionParameter
) => void
