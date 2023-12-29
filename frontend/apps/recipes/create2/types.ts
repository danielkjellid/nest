import {
  type RecipeIngredientItemGroupRecord,
  type RecipeIngredientItemRecord,
  type RecipeStepRecord,
} from '../../../types'

type Action<T> = keyof T
type ActionParameter<T extends Record<string, any>> = Parameters<T[Action<T>]>
export type ActionFunc<T extends Record<string, any>> = (
  action: Action<T>,
  ...params: ActionParameter<T>
) => void

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

export interface Step extends Pick<RecipeStepRecord, 'instruction' | 'duration' | 'stepType'> {
  ingredientItems: IngredientItem[]
}

export interface StepActions {
  inputAdd: () => void
  inputChange: (index: number, data: Step) => void
  inputDelete: (index: number) => void
  stepSequenceChange: (data: Step[]) => void
}
