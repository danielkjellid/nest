import { Card } from '../../../../components/Card'
import { RecipeStepsForm } from '../../forms/RecipeStepsForm'
import { type IngredientItemGroup, type Step, type StepActions, type ActionFunc } from '../types'

interface StepsFormCardProps {
  steps: Step[]
  ingredientGroups: IngredientItemGroup[]
  onAction: ActionFunc<StepActions>
}

function StepsFormCard({ steps, ingredientGroups, onAction }: StepsFormCardProps) {
  return (
    <Card.Form
      title="Add steps"
      subtitle="Add steps to recipe"
      form={
        <RecipeStepsForm steps={steps} ingredientGroups={ingredientGroups} onAction={onAction} />
      }
    />
  )
}

export { StepsFormCard }
