export interface IngredientItemOptionType {
  label: string
  value: string
  image?: string
  description: string
  group: string
}

export interface Step {
  instruction: string
  duration: number
  type: string
  ingredientItems: IngredientItemOptionType[]
}

export interface StepInputError {
  index: number
  unusedIngredientOptions?: boolean
  emptyFields?: (keyof Step)[]
  durationBellowZero?: boolean
}
