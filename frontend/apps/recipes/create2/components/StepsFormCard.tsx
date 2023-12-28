import { useMemo } from 'react'

import { Card } from '../../../../components/Card'
import { RecipeStepsForm, type Step } from '../../forms/RecipeStepsForm'
import { type IngredientGroup } from '../../forms/RecipeIngredientsForm'
interface StepsFormCardProps {
  steps: Step[]
  ingredientGroups: IngredientGroup[]
}

function StepsFormCard({ steps, ingredientGroups }: StepsFormCardProps) {
  // Get a list of available IngredientItem options. This incudes filtering out ingredients
  // "claimed" by other steps.
  const ingredientItemOptions = useMemo(
    () =>
      ingredientGroups?.flatMap((ingredientGroup) =>
        ingredientGroup.ingredientItems
          .filter(
            (ingredientItem) =>
              !selectedIngredientItems
                .map((selectedItem) => selectedItem.value)
                .includes(ingredientItem.id.toString())
          )
          .map((item) => ({
            label: item.ingredient.title,
            image: item.ingredient.product.thumbnailUrl,
            description: item.ingredient.product.fullName,
            value: item.id.toString(),
            group: ingredientGroup.title,
          }))
      ),
    [ingredientGroups, selectedIngredientItems]
  )

  return (
    <Card>
      <Card.Form
        title="Add steps"
        subtitle="Add steps to recipe"
        form={
          <RecipeStepsForm
            steps={steps}
            errors={[]}
            ingredientItemOptions={ingredientItemOptions || []}
            onSequenceChange={handleSequenceChange}
            onStepInputAdd={handleStepInputAdd}
            onStepInputChange={handleStepInputChange}
            onStepInputDelete={handleStepInputDelete}
          />
        }
      />
    </Card>
  )
}

export { StepsFormCard }
