import { ProductDetailOut, ProductDetailOutAPIResponse, ProductEditIn } from '../../../../types'
import React, { useEffect, useState } from 'react'

import Drawer from '../../../../components/Drawer'
import Form from '../../../../components/Form'
import { performGet } from '../../../../hooks/fetcher/http'
import { urls } from '../../../urls'
import { useForm } from '../../../../hooks/forms'
import { useUnits } from '../../../../contexts/UnitsProvider'

interface ProductEditDrawerProps {
  productId: number
}

function ProductEditDrawer({ productId }: ProductEditDrawerProps) {
  const fetchProduct = async () => {
    const fetchedProduct = await performGet<ProductDetailOutAPIResponse>(
      urls.products.detail({ id: productId })
    )
    setProduct(fetchedProduct.data)
  }

  const [product, setProduct] = useState<ProductDetailOut>()
  const form = useForm({ key: 'ProductEditIn', existingObj: product })
  const units = useUnits()
  const unitsOptions = units.map((unit) => ({ label: unit.displayName, value: unit.id.toString() }))

  useEffect(() => {
    if (!product) {
      fetchProduct()
    }
    if (product) {
      form.setData(product)
    }
  }, [product])

  // fetchProduct()
  return (
    <Drawer title={`Edit "${product?.fullName}"`} opened onClose={() => console.log('close')}>
      {product && (
        <Form
          {...form}
          elementsOptions={{
            unit: { options: unitsOptions },
            thumbnail: { placeholder: product.thumbnailUrl },
          }}
        />
      )}
    </Drawer>
  )
}

export default ProductEditDrawer
