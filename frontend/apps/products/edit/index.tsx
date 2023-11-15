import { useNavigate, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'

import { Button } from '../../../components/Button'
import { Card } from '../../../components/Card'
import Form from '../../../components/Form'
import View from '../../../components/View'
import { useUnits } from '../../../contexts/UnitsProvider'
import { useFetch } from '../../../hooks/fetcher'
import { useForm } from '../../../hooks/forms'
import { type ProductDetailOutAPIResponse } from '../../../types'
import { urls } from '../../urls'
import { ProductDetailHeader } from '../components/ProductDetailHeader'

interface ProductEditInnerProps {
  results: {
    productResponse: ProductDetailOutAPIResponse
  }
  productId: number
}

function ProductEditInner({ results, productId }: ProductEditInnerProps) {
  const navigate = useNavigate()
  const { data: product } = results.productResponse
  const { unitsOptions } = useUnits()

  const productForm = useForm({ key: 'ProductEditForm', initialData: product })

  const submit = async () => {
    productForm.performPost({ url: urls.products.edit({ id: productId }) })
    navigate(-1)
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

  return (
    <View<object, any>
      component={ProductEditInner}
      results={{ productResponse }}
      componentProps={{ productId }}
      loadingProps={{ description: 'Loading product...' }}
      errorProps={{ description: 'There was an error getting the product. Please try again.' }}
    />
  )
}

export { ProductEdit }
