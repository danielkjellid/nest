import { IconEye } from '@tabler/icons-react'
import { Menu } from '@mantine/core'
import { ProductList } from '../../../../types'
import React from 'react'
import Table from '../../../../components/Table'

interface ProductOverViewTableProps {
  data: ProductList[]
}

function ProductOverViewTable({ data }: ProductOverViewTableProps) {
  return (
    <Table<ProductList>
      rowIdentifier="id"
      columns={[
        { header: 'Id', accessorKey: 'id', size: 20 },
        {
          header: 'Product',
          accessorKey: 'fullName',
          id: 'fullName',
          Cell: ({ row, renderedCellValue }) => (
            <div className="flex items-center space-x-3">
              <img src={row.original.thumbnailUrl} className="object-cover h-8" />
              <div>{renderedCellValue}</div>
            </div>
          ),
        },
        {
          header: 'Gross price',
          accessorFn: (row) => (
            <span>
              {row.grossPrice} ({row.grossUnitPrice} per {row.unit.abbreviation})
            </span>
          ),
          enableColumnFilter: false,
          enableFilterMatchHighlighting: false,
        },
        { header: 'Available', accessorKey: 'isAvailable', options: { isBoolean: true } },
        { header: 'Sync enabled', accessorKey: 'isSynced', options: { isBoolean: true } },
        { header: 'Last sync', accessorKey: 'lastSyncedAt' },
        { header: 'Oda Id', accessorKey: 'odaId', size: 20 },
      ]}
      data={data || []}
      actionMenuItems={({ row }) => [
        <>
          <Menu.Item
            key={1}
            component="a"
            href={row.original.odaUrl}
            target="_blank"
            icon={<IconEye />}
          >
            View at Oda
          </Menu.Item>
        </>,
      ]}
    />
  )
}

export default ProductOverViewTable
