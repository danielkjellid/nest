import { Anchor, Menu } from '@mantine/core'
import { IconTrash } from '@tabler/icons-react'

import Table from '../../../components/Table'
import { type RecipeIngredientRecord } from '../../../types'
import { routes as productRoutes } from '../../products/routes'

interface IngredientsOverviewTableProps {
  data: RecipeIngredientRecord[]
  onDeleteIngredient: (id: number) => void
}

function IngredientsOverviewTable({ data, onDeleteIngredient }: IngredientsOverviewTableProps) {
  return (
    <Table<RecipeIngredientRecord>
      rowIdentifier="id"
      columns={[
        { header: 'Title', accessorKey: 'title' },
        {
          header: 'Product',
          accessorKey: 'product.fullName',
          Cell: ({ row, renderedCellValue }) => (
            <div className="flex items-center space-x-3">
              <img src={row.original.product?.thumbnailUrl} className="object-contain w-8 h-8" />
              {row.original.product?.id && (
                <Anchor href={productRoutes.detail.build({ productId: row.original.product.id })}>
                  {renderedCellValue}
                </Anchor>
              )}
            </div>
          ),
        },
      ]}
      data={data || []}
      actionMenuItems={({ row }) => [
        <Menu.Item
          key="delete"
          icon={<IconTrash />}
          onClick={() => onDeleteIngredient(row.original.id)}
        >
          Delete
        </Menu.Item>,
      ]}
    />
  )
}

export { IngredientsOverviewTable }
