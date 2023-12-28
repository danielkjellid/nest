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
