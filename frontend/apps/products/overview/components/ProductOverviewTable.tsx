import { Anchor, Menu } from '@mantine/core'
import { IconEye, IconPencil, IconTrash } from '@tabler/icons-react'
import React from 'react'

import Table from '../../../../components/Table'
import { ProductListOut } from '../../../../types'
import { routes } from '../../routes'

interface ProductOverViewTableProps {
  data: ProductListOut[]
  onEditProduct: (id: number) => void
}

function ProductOverViewTable({ data, onEditProduct }: ProductOverViewTableProps) {
  return (
    <Table<ProductListOut>
      rowIdentifier="id"
      columns={[
        { header: 'Id', accessorKey: 'id', size: 20 },
        {
          header: 'Product',
          accessorKey: 'fullName',
          id: 'fullName',
          Cell: ({ row, renderedCellValue }) => (
            <div className="flex items-center space-x-3">
              <img src={row.original.thumbnailUrl} className="object-contain w-8 h-8" />
              <Anchor href={routes.detail.build({ productId: row.original.id })}>
                {renderedCellValue}
              </Anchor>
            </div>
          ),
        },
        {
          header: 'Gross price',
          accessorKey: 'displayPrice',
          enableColumnFilter: false,
          enableFilterMatchHighlighting: false,
        },
        // { header: 'Gtin', accessorKey: 'gtin' },
        { header: 'Available', accessorKey: 'isAvailable', options: { isBoolean: true } },
        { header: 'Sync enabled', accessorKey: 'isSynced', options: { isBoolean: true } },
        { header: 'Oda product', accessorKey: 'isOdaProduct', options: { isBoolean: true } },
      ]}
      data={data || []}
      actionMenuItems={({ row }) => [
        <Menu.Item key="edit" icon={<IconPencil />} onClick={() => onEditProduct(row.original.id)}>
          Edit
        </Menu.Item>,
        <Menu.Item key="delete" icon={<IconTrash />}>
          Delete
        </Menu.Item>,
        row.original.isOdaProduct && (
          <Menu.Item
            key="view"
            component="a"
            href={row.original.odaUrl}
            target="_blank"
            icon={<IconEye />}
          >
            View at Oda
          </Menu.Item>
        ),
      ]}
    />
  )
}

export default ProductOverViewTable
