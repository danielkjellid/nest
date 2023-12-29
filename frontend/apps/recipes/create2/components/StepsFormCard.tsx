import { Card } from '../../../../components/Card'
import { RecipeStepsForm } from '../../forms/RecipeStepsForm'
import { type IngredientItemGroup, type Step } from '../types'

interface StepsFormCardProps {
  steps: Step[]
  ingredientGroups: IngredientItemGroup[]
  onSequenceChange: (steps: Step[]) => void
  onStepInputAdd: () => void
  onStepInputChange: (index: number, data: Step) => void
  onStepInputDelete: (index: number) => void
}

function StepsFormCard({
  steps,
  ingredientGroups,
  onSequenceChange,
  onStepInputAdd,
  onStepInputChange,
  onStepInputDelete,
}: StepsFormCardProps) {
  return (
    <Card.Form
      title="Add steps"
      subtitle="Add steps to recipe"
      form={
        <RecipeStepsForm
          steps={steps}
          ingredientGroups={ingredientGroups}
          onSequenceChange={onSequenceChange}
          onStepInputAdd={onStepInputAdd}
          onStepInputChange={onStepInputChange}
          onStepInputDelete={onStepInputDelete}
        />
      }
    />
  )
}

export { StepsFormCard }
