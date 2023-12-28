import {
  type RecipeIngredientItemGroupRecord,
  type RecipeIngredientItemRecord,
} from '../../../types'

export interface IngredientItem
  extends Pick<RecipeIngredientItemRecord, 'portionQuantity' | 'additionalInfo'> {
  ingredientId: string
  portionQuantityUnitId: string
}
export interface IngredientItemGroup
  extends Pick<RecipeIngredientItemGroupRecord, 'title' | 'ordering'> {
  ingredientItems: IngredientItem[]
}
