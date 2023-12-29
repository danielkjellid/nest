import { Card } from '../../../../components/Card'
import { useUnits } from '../../../../contexts/UnitsProvider'
import { type RecipeIngredientRecord } from '../../../../types'
import { RecipeIngredientsForm } from '../../forms/RecipeIngredientsForm'
import { type IngredientItemGroup, type ActionFunc, type IngredientGroupActions } from '../types'

interface RecipeIngredientsFormCardProps {
  ingredients?: RecipeIngredientRecord[]
  ingredientGroups: IngredientItemGroup[]
  onAction: ActionFunc<IngredientGroupActions>
}

function IngredientsFormCard({
  ingredients,
  ingredientGroups,
  onAction,
}: RecipeIngredientsFormCardProps) {
  const { units, unitsOptions } = useUnits()

  return (
    <Card.Form
      title="Add ingredients"
      subtitle="Add ingredients and amounts to recipe. If one ingredient is needed within multiple groups, add it to each group respectively."
      form={
        <RecipeIngredientsForm
          ingredients={ingredients}
          ingredientGroups={ingredientGroups}
          units={units}
          unitOptions={unitsOptions}
          onAction={onAction}
        />
      }
    />
  )
}

export { IngredientsFormCard }
