import React, { useState } from 'react'
import View from '../../../components/View'
import { Title } from '@mantine/core'
import {
  ProductDetailOut,
  ProductDetailOutAPIResponse,
  ProductOdaImportOutAPIResponse,
} from '../../../types'
import { useUnits } from '../../../contexts/UnitsProvider'
import { useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { useFetch } from '../../../hooks/fetcher'
import { urls } from '../../urls'
import { useForm } from '../../../hooks/forms'
import { ProductDetailHeader } from '../components/ProductDetailHeader'
import { Button } from '../../../components/Button'
import Form from '../../../components/Form'
import { Card } from '../../../components/Card'

interface ProductEditInnerProps {
  results: {
    productResponse: ProductDetailOutAPIResponse
  }
  productId: number
  refetch: () => void
}

function ProductEditInner({ results, productId, refetch }: ProductEditInnerProps) {
  const { data: product } = results.productResponse
  const { unitsOptions } = useUnits()

  const productForm = useForm({ key: 'ProductEditIn', existingObj: product })

  const submit = async () => {
    productForm.performPost({ url: urls.products.edit({ id: productId }) })
    refetch()
  }

  return (
    <div className="space-y-6">
      {product && (
        <ProductDetailHeader
          fullName={product.fullName}
          thumbnailUrl={product.thumbnailUrl}
          supplier={product.supplier}
          actions={<Button onClick={() => submit()}>Save product</Button>}
        />
      )}
      {product && (
        <Card>
          <Card.Form
            title="Product information"
            subtitle="Edit all relevant properties of the product, such as name, price, unit and nutrition."
            form={
              <Form
                {...productForm}
                elementsOptions={{
                  unit: { options: unitsOptions, accessorKey: 'unit.id' },
                  thumbnail: { placeholder: product.thumbnailUrl?.split('/').pop() },
                }}
              />
            }
          />
        </Card>
      )}
    </div>
  )
}

function ProductEdit() {
  const { productId } = useParams()
  invariant(productId)

  const productResponse = useFetch<ProductDetailOutAPIResponse>(
    urls.products.detail({ id: productId })
  )

  const refetch = () => {
    productResponse.reload()
  }

  return (
    <View<object, any>
      component={ProductEditInner}
      results={{ productResponse }}
      componentProps={{ productId, refetch }}
      loadingProps={{ description: 'Loading product...' }}
      errorProps={{ description: 'There was an error getting the product. Please try again.' }}
    />
  )
}

export { ProductEdit }
