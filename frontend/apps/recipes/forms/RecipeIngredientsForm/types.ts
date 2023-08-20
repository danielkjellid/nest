import { UnitOption } from '../../../../contexts/UnitsProvider'

export interface IngredientOptionType {
  label: string
  value: string
  image?: string | null
  description: string
}

export interface Ingredient {
  ingredient: string
  portionQuantity: string
  additionalInfo: string
  unit: UnitOption['value']
}

export interface IngredientGroup {
  title: string
  ingredients: Ingredient[]
}

export interface IngredientGroupFormError {
  index: number
  message: string
}
