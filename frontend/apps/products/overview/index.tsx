import { ProductListOutAPIResponse, UnitListOutAPIResponse } from '../../../types'
import React, { useState } from 'react'

import { Button } from '../../../components/Button'
import ProductAddDrawer from '../components/ProductAddDrawer'
import ProductEditDrawer from '../components/ProductEditDrawer'
import ProductOverViewTable from './components/ProductOverviewTable'
import { Title } from '@mantine/core'
import { UnitsProvider } from '../../../contexts/UnitsProvider'
import View from '../../../components/View'
import { urls } from '../../urls'
import { useDisclosure } from '@mantine/hooks'
import { useFetch } from '../../../hooks/fetcher'

interface ProductsOverviewInnerProps {
  results: {
    products: ProductListOutAPIResponse
    units: UnitListOutAPIResponse
  }
  refetch: () => void
}

function ProductsOverviewInner({ results, refetch }: ProductsOverviewInnerProps) {
  const { products, units } = results
  const [addDrawerOpened, { open: addDrawerOpen, close: addDrawerClose }] = useDisclosure(false)
  const [editDrawerOpened, { open: editDrawerOpen, close: editDrawerClose }] = useDisclosure(false)

  const [productIdToEdit, setProductIdToEdit] = useState<number>()
  const editProduct = (id: number) => {
    setProductIdToEdit(id)
    editDrawerOpen()
  }

  return (
    <UnitsProvider units={units.data}>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <Title weight={600}>Products</Title>
          <div className="flex items-center space-x-3">
            <Button.Group>
              {/* <Button variant="default">Import from Oda</Button> */}
              <Button variant="default" onClick={addDrawerOpen}>
                Add new
              </Button>
            </Button.Group>
          </div>
        </div>
        <ProductOverViewTable data={products.data || []} onEditProduct={(id) => editProduct(id)} />
        <ProductAddDrawer opened={addDrawerOpened} onClose={addDrawerClose} refetch={refetch} />
        <ProductEditDrawer
          productId={productIdToEdit}
          opened={editDrawerOpened}
          onClose={editDrawerClose}
          refetch={refetch}
        />
      </div>
    </UnitsProvider>
  )
}

function ProductsOverview() {
  const products = useFetch<ProductListOutAPIResponse>(urls.products.list())
  const units = useFetch<UnitListOutAPIResponse>(urls.units.list())

  const refetch = () => {
    products.reload()
  }

  return (
    <View<object, ProductsOverviewInnerProps>
      component={ProductsOverviewInner}
      results={{ products, units }}
      componentProps={{ refetch }}
      loadingProps={{ description: 'Loading products...' }}
      errorProps={{ description: 'There was an error getting products. Please try again.' }}
    />
  )
}

export { ProductsOverview }
