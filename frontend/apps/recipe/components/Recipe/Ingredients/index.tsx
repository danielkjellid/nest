import React from 'react'
import { useCommonStyles } from '../../../../../styles/common'

interface RecipeIngredientGroupProps {
  title: string
  className?: string
  children: React.ReactNode
}

function RecipeIngredientGroup({ title, className, children }: RecipeIngredientGroupProps) {
  const { classes } = useCommonStyles()
  return (
    <div>
      <h3 className={`mb-2 text-xs font-semibold leading-5 ${classes.muted} uppercase`}>{title}</h3>
      <table className={`min-w-full text-sm ${className}`}>
        <thead className="sr-only">
          <tr>
            <th>Amount</th>
            <th>Item</th>
          </tr>
        </thead>
        <tbody>{children}</tbody>
      </table>
    </div>
  )
}

interface RecipeIngredientGroupItemProps {
  title: string
  amount: number
  unit: string
  basePortions: number
  portions: number
}

function RecipeIngredientGroupItem({
  title,
  amount,
  unit,
  basePortions,
  portions,
}: RecipeIngredientGroupItemProps) {
  const portionAmount = amount * (portions / basePortions)

  return (
    <tr>
      <td className="whitespace-nowrap w-16 py-1 font-medium">
        {portionAmount} {unit}
      </td>
      <td className="py-1">{title}</td>
    </tr>
  )
}

RecipeIngredientGroup.Item = RecipeIngredientGroupItem

export { RecipeIngredientGroup }
