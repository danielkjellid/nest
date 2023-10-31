import React from 'react'
import { RecipeTable } from '../Table'

interface RecipeTableRecord {
  key: string
  title: string
  value: string
  unit: string
  percentageOfDailyValue: string
}

interface RecipeNutritionTableProps {
  nutrition: RecipeTableRecord[]
}

function RecipeNutritionTable({ nutrition }: RecipeNutritionTableProps) {
  return (
    <RecipeTable headers={['nutrition', 'value', 'percentage of daily value']}>
      {nutrition.map((n) => (
        <RecipeTable.Row key={n.key}>
          <RecipeTable.Row.Data bold>{n.title}</RecipeTable.Row.Data>
          <RecipeTable.Row.Data>
            {n.value} {n.unit}
          </RecipeTable.Row.Data>
          <RecipeTable.Row.Data muted>{n.percentageOfDailyValue}%</RecipeTable.Row.Data>
        </RecipeTable.Row>
      ))}
    </RecipeTable>
  )
}

export { RecipeNutritionTable }
