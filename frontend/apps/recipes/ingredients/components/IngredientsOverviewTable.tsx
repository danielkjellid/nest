import Table from '../../../../components/Table'
import React from 'react'
import { IngredientListOut } from '../../../../types'
import { routes as productRoutes } from '../../../products/routes'
import { Anchor } from '@mantine/core'
interface IngredientsOverviewTableProps {
  data: IngredientListOut[]
}

function IngredientsOverviewTable({ data }: IngredientsOverviewTableProps) {
  return (
    <Table<IngredientListOut>
      rowIdentifier="id"
      columns={[
        { header: 'Id', accessorKey: 'id', size: 20 },
        {
          header: 'Product',
          accessorKey: 'product.fullName',
          Cell: ({ row, renderedCellValue }) => (
            <div className="flex items-center space-x-3">
              <img src={row.original.product.thumbnailUrl} className="object-contain w-8 h-8" />
              <Anchor href={productRoutes.detail.build({ productId: row.original.id })}>
                {renderedCellValue}
              </Anchor>
            </div>
          ),
        },
        { header: 'Title', accessorKey: 'title' },
      ]}
      data={data || []}
    />
  )
}

export { IngredientsOverviewTable }
