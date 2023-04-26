import { Button, Title } from '@mantine/core'
import { ProductAddIn, TestSchema } from '../../types'
import React, { useEffect, useState } from 'react'

import Form from '../../components/Form'
import ProductAddDrawer from './components/ProductAddDrawer'
import ProductOverViewTable from './components/ProductOverviewTable'
import View from '../../components/View'
import { performPost } from '../../hooks/fetcher/http'
import urls from './urls'
import { useDisclosure } from '@mantine/hooks'
import { useFetch } from '../../hooks/fetcher'
import { useForm } from '../../hooks/forms/useForm'

interface ProductsAppInnerProps {
  results: {
    // products: ProductListAPIResponse
    // productImportForm: ProductImportInFormAPIResponse
    // productAddForm: ProductAddInFormAPIResponse
  }
}

function ProductsAppInner({ results }: ProductsAppInnerProps) {
  // const { products, productImportForm, productAddForm } = results
  const [opened, { open, close }] = useDisclosure(true)
  // const [productImportResponse, setProductImportResponse] = useState<ProductImportOut>()

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
  const form = useForm<ProductAddIn>('ProductAddIn', obj)
  const form2 = useForm<TestSchema>('TestSchema')

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title>Products</Title>
      </div>
      {/* <ProductOverViewTable data={products.data || []} /> */}
      <ProductAddDrawer opened={opened} onClose={close}>
        <Form<ProductAddIn> {...form} />
        {JSON.stringify(form.data)}
        <hr />
        <button onClick={() => form.resetForm()}>Reset</button>
      </ProductAddDrawer>
      <hr />
    </div>
  )
}

function ProductsApp() {
  // const products = useFetch<ProductListAPIResponse>(urls.list())
  // const productAddForm = useFetch<FormRecordAPIResponse>(urls.productAddForm())
  // const productImportForm = useFetch<FormRecordAPIResponse>(urls.productImportForm())

  return (
    <View<object, ProductsAppInnerProps>
      component={ProductsAppInner}
      results={{}}
      componentProps={{}}
      loadingProps={{ description: 'Loading products...' }}
      errorProps={{ description: 'There was an error getting products. Please try again.' }}
    />
  )
}

export default ProductsApp
