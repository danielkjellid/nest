import { useMemo } from 'react'

import { Card } from '../../../../components/Card'
import { useUnits } from '../../../../contexts/UnitsProvider'
import { type RecipeIngredientRecord } from '../../../../types'
import { RecipeIngredientsForm } from '../../forms/RecipeIngredientsForm'
import { type IngredientItemGroup, type IngredientItem } from '../types'

interface RecipeIngredientsFormCardProps {
  ingredients?: RecipeIngredientRecord[]
  ingredientGroups: IngredientItemGroup[]
  onSequenceChange: (ingredientGroups: IngredientItemGroup[]) => void
  onIngredientInputAdd: (index: number) => void
  onIngredientInputChange: (index: number, ingredientIndex: number, data: IngredientItem) => void
  onIngredientInputDelete: (index: number, ingredientIndex: number) => void
  onIngredientGroupInputAdd: () => void
  onIngredientGroupInputChange: (index: number, data: IngredientItemGroup) => void
  onIngredientGroupInputDelete: (index: number) => void
}

function IngredientsFormCard({
  ingredients,
  ingredientGroups,
  onSequenceChange,
  onIngredientInputAdd,
  onIngredientInputChange,
  onIngredientInputDelete,
  onIngredientGroupInputAdd,
  onIngredientGroupInputChange,
  onIngredientGroupInputDelete,
}: RecipeIngredientsFormCardProps) {
  const { unitsOptions } = useUnits()
  const ingredientOptions =
    useMemo(
      () =>
        ingredients &&
        ingredients.map((ingredient) => ({
          label: ingredient.title,
          image: ingredient.product.thumbnailUrl,
          description: ingredient.product.fullName,
          value: ingredient.id.toString(),
        })),
      [ingredients]
    ) || []

  return (
    <Card>
      <Card.Form
        title="Add ingredients"
        subtitle="Add ingredients and amounts to recipe. If one ingredient is needed within multiple groups, add it to each group respectively."
        form={
          <RecipeIngredientsForm
            ingredientGroups={ingredientGroups}
            ingredientErrors={[]}
            ingredientGroupsErrors={[]}
            units={unitsOptions || []}
            ingredientOptions={ingredientOptions}
            onSequenceChange={onSequenceChange}
            onIngredientInputAdd={onIngredientInputAdd}
            onIngredientInputChange={onIngredientInputChange}
            onIngredientInputDelete={onIngredientInputDelete}
            onIngredientGroupInputAdd={onIngredientGroupInputAdd}
            onIngredientGroupInputChange={onIngredientGroupInputChange}
            onIngredientGroupInputDelete={onIngredientGroupInputDelete}
          />
        }
      />
    </Card>
  )
}

export { IngredientsFormCard }
