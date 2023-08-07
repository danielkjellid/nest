import React from 'react'

interface RecipeIngredientGroupProps {
  title: string
  className?: string
  children: React.ReactNode
}

function RecipeIngredientGroup({ title, className, children }: RecipeIngredientGroupProps) {
  return (
    <div>
      <h3 className="mb-2 text-xs font-semibold leading-5 text-gray-500 uppercase">{title}</h3>
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
}

function RecipeIngredientGroupItem({ title, amount, unit }: RecipeIngredientGroupItemProps) {
  return (
    <tr>
      <td className="py-1 font-medium">
        {amount} {unit}
      </td>
      <td className="py-1">{title}</td>
    </tr>
  )
}

RecipeIngredientGroup.Item = RecipeIngredientGroupItem

export { RecipeIngredientGroup }
