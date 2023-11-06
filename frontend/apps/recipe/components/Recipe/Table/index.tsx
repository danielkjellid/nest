import cx from 'classnames'

import { useCommonStyles } from '../../../../../styles/common'

import { useTableStyles } from './Table.styles'

interface RecipeTableProps {
  headers: string[]
  children: React.ReactNode
}

function RecipeTable({ headers, children }: RecipeTableProps) {
  const { classes } = useCommonStyles()
  return (
    <div className={`rounded-md border overflow-hidden ${classes.border}`}>
      <table className="min-w-full">
        <thead>
          <tr className="sr-only">
            {headers.map((header) => (
              <th key={header}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>{children}</tbody>
      </table>
    </div>
  )
}

interface RecipeTableRowProps {
  children: React.ReactNode
}

function RecipeTableRow({ children }: RecipeTableRowProps) {
  const { classes } = useTableStyles()
  return <tr className={classes.rowBackground}>{children}</tr>
}

interface RecipeTableRowDataProps {
  bold?: boolean
  muted?: boolean
  children: React.ReactNode
}

function RecipeTableRowData({ bold, muted, children }: RecipeTableRowDataProps) {
  const { classes } = useCommonStyles()
  return (
    <td className={cx('px-2 py-2 text-sm', { 'font-medium': bold }, [muted ? classes.muted : ''])}>
      {children}
    </td>
  )
}

RecipeTableRow.Data = RecipeTableRowData
RecipeTable.Row = RecipeTableRow

export { RecipeTable }
