import { Button, Title } from '@mantine/core'
import {
  ProductAddInForm,
  ProductAddInFormAPIResponse,
  ProductImportIn,
  ProductImportInFormAPIResponse,
  ProductImportOut,
  ProductImportOutAPIResponse,
  ProductListAPIResponse,
  ProductsService,
} from '../../types'
import React, { useState } from 'react'

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
    products: ProductListAPIResponse
    productImportForm: ProductImportInFormAPIResponse
    productAddForm: ProductAddInFormAPIResponse
  }
}

function ProductsAppInner({ results }: ProductsAppInnerProps) {
  // const { products, productImportForm, productAddForm } = results
  const [opened, { open, close }] = useDisclosure(false)
  const [productImportResponse, setProductImportResponse] = useState<ProductImportOut>()

  const form = useForm('ProductAddIn')

  const testImport = async (id: number) => {
    const res = await performPost<ProductImportOutAPIResponse>('/api/v1/products/import/', {
      odaProductId: id,
    })
    setProductImportResponse(res.data)
  }

  const obj = {
    name: 'Some name',
    grossPrice: '1042',
    unitType: 'weight',
    unit: '2',
    isAvailable: true,
    supplier: 'Some suplier',
    odaId: '',
    odaUrl: '',
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title>Products</Title>
      </div>
      {/* <ProductOverViewTable data={products.data || []} /> */}
      <ProductAddDrawer opened={opened} onClose={close} />
      <hr />
      {/* <Form<ProductImportIn>
        form={productImportForm.data}
        elementOptions={{ odaProductId: { afterSlot: <Button>Import product</Button> } }}
      />
      {productImportResponse && JSON.stringify(productImportResponse)}
      <hr />
      <Form<ProductAddIn>
        form={productAddForm.data}
        // elementOptions={{ odaProductId: { afterSlot: <Button>Import product</Button> } }}
        // onSubmit={(values) => testImport(values.odaProductId)}
        // existingObj={obj}
      /> */}
      <p>{JSON.stringify(form)}</p>
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
