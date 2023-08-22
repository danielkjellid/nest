import { Anchor } from '@mantine/core'
import { IngredientListOut } from '../../../types'
import React from 'react'
import Table from '../../../components/Table'
import { routes as productRoutes } from '../../products/routes'
interface IngredientsOverviewTableProps {
  data: IngredientListOut[]
}

function IngredientsOverviewTable({ data }: IngredientsOverviewTableProps) {
  return (
    <Table<IngredientListOut>
      rowIdentifier="id"
      columns={[
        { header: 'Title', accessorKey: 'title' },
        {
          header: 'Product',
          accessorKey: 'product.fullName',
          Cell: ({ row, renderedCellValue }) => (
            <div className="flex items-center space-x-3">
              <img src={row.original.product.thumbnailUrl} className="object-contain w-8 h-8" />
              <Anchor href={productRoutes.detail.build({ productId: row.original.product.id })}>
                {renderedCellValue}
              </Anchor>
            </div>
          ),
        },
      ]}
      data={data || []}
    />
  )
}

export { IngredientsOverviewTable }
