export interface IngredientOptionType {
  label: string
  value: string
  image?: string | null
  description: string
}

export interface IngredientGroupFormError {
  index: number
  message: string
}

export interface FormError {
  index: number
  message: string
}
