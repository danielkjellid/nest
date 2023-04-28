import { ProductListOutAPIResponse, UnitListOutAPIResponse } from '../../types'

import { Button } from '../../components/Button'
import ProductAddDrawer from './components/ProductAddDrawer'
import ProductOverViewTable from './components/ProductOverviewTable'
import React from 'react'
import { Title } from '@mantine/core'
import { UnitsProvider } from '../../contexts/UnitsProvider'
import View from '../../components/View'
import { urls } from '../urls'
import { useDisclosure } from '@mantine/hooks'
import { useFetch } from '../../hooks/fetcher'

interface ProductsAppInnerProps {
  results: {
    products: ProductListOutAPIResponse
    units: UnitListOutAPIResponse
  }
}

function ProductsAppInner({ results }: ProductsAppInnerProps) {
  const { products, units } = results
  const [opened, { open, close }] = useDisclosure(false)

  return (
    <UnitsProvider units={units.data}>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <Title weight={600}>Products</Title>
          <div className="flex items-center space-x-3">
            <Button.Group>
              {/* <Button variant="default">Import from Oda</Button> */}
              <Button variant="default" onClick={open}>
                Add new
              </Button>
            </Button.Group>
          </div>
        </div>
        <ProductOverViewTable data={products.data || []} />
        <ProductAddDrawer opened={opened} onClose={close} />
      </div>
    </UnitsProvider>
  )
}

function ProductsApp() {
  const products = useFetch<ProductListOutAPIResponse>(urls.products.list())
  const units = useFetch<UnitListOutAPIResponse>(urls.units.list())

  return (
    <View<object, ProductsAppInnerProps>
      component={ProductsAppInner}
      results={{ products, units }}
      componentProps={{}}
      loadingProps={{ description: 'Loading products...' }}
      errorProps={{ description: 'There was an error getting products. Please try again.' }}
    />
  )
}

export default ProductsApp
