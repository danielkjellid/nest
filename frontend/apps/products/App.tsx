import { ProductAddIn, ProductListAPIResponse } from '../../types'

import Form from '../../components/Form'
import ProductAddDrawer from './components/ProductAddDrawer'
import ProductOverViewTable from './components/ProductOverviewTable'
import React from 'react'
import { Title } from '@mantine/core'
import View from '../../components/View'
import urls from './urls'
import { useDisclosure } from '@mantine/hooks'
import { useFetch } from '../../hooks/fetcher'
import { useForm } from '../../hooks/forms'

interface ProductsAppInnerProps {
  results: {
    products: ProductListAPIResponse
  }
}

function ProductsAppInner({ results }: ProductsAppInnerProps) {
  const { products } = results
  const [opened, { open, close }] = useDisclosure(true)

  const obj = {
    name: 'Some name',
    grossPrice: '1042',
    unitType: 'weight',
    unit: '2',
    isAvailable: true,
    supplier: 'Some supplier',
    odaId: '',
    odaUrl: '',
  }

  const form = useForm<ProductAddIn>({ key: 'ProductAddIn', existingObj: obj })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title>Products</Title>
      </div>
      <ProductOverViewTable data={products.data || []} />
      <ProductAddDrawer opened={opened} onClose={close}>
        <Form<ProductAddIn> {...form} />
      </ProductAddDrawer>
      <hr />
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
