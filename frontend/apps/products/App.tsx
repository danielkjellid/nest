import { Menu, Title } from '@mantine/core'
import { ProductList, ProductListAPIResponse } from '../../types'

import { IconEye } from '@tabler/icons-react'
import React from 'react'
import Table from '../../components/Table'
import View from '../../components/View'
import urls from './urls'
import { useCommonContext } from '../../contexts/CommonProvider'
import { useFetch } from '../../hooks/fetcher'

interface ProductsAppInnerProps {
  results: { products: ProductListAPIResponse }
}

function ProductsAppInner({ results }: ProductsAppInnerProps) {
  const { products } = results
  const { currentUser } = useCommonContext()

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title>Products</Title>
      </div>
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
        data={products.data || []}
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
        disableRowSelection={!currentUser.isStaff}
      />
    </div>
  )
}

function ProductsApp() {
  const products = useFetch<ProductListAPIResponse>(urls.list())

  return (
    <View<object, ProductsAppInnerProps>
      component={ProductsAppInner}
      results={{ products }}
      componentProps={{}}
      loadingProps={{ description: 'Loading products...' }}
      errorProps={{ description: 'There was an error getting products. Please try again.' }}
    />
  )
}

export default ProductsApp
