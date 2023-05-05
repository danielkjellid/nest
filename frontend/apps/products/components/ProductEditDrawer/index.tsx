import { ProductDetailOut, ProductDetailOutAPIResponse, ProductEditIn } from '../../../../types'
import React, { useEffect, useState } from 'react'
import { performGet, performPost, performPut } from '../../../../hooks/fetcher/http'

import { Button } from '../../../../components/Button'
import Drawer from '../../../../components/Drawer'
import Form from '../../../../components/Form'
import { urls } from '../../../urls'
import { useForm } from '../../../../hooks/forms'
import { useUnits } from '../../../../contexts/UnitsProvider'

interface ProductEditDrawerProps {
  productId: number
  opened: boolean
  onClose: () => void
  refetch: () => void
}

function ProductEditDrawer({ productId, opened, onClose, refetch }: ProductEditDrawerProps) {
  const [product, setProduct] = useState<ProductDetailOut>()
  const form = useForm({ key: 'ProductEditIn', existingObj: product })
  const units = useUnits()
  const unitsOptions = units.map((unit) => ({ label: unit.displayName, value: unit.id.toString() }))

  const close = () => {
    form.resetForm()
    onClose()
    refetch()
  }

  const editProduct = async () => {
    try {
      form.setLoadingState('loading')
      await performPost(urls.products.edit({ id: productId }), form.buildPayload())
      form.setLoadingState('success')
      close()
    } catch (e) {
      const errorResponse = (e as any).response.data
      form.setLoadingState('error')
      if (errorResponse) {
        form.setErrors(errorResponse.data)
      }
    }
  }

  useEffect(() => {
    if (!product || (product && product.id !== productId)) {
      const fetchProduct = async () => {
        const fetchedProduct = await performGet<ProductDetailOutAPIResponse>(
          urls.products.detail({ id: productId })
        )
        setProduct(fetchedProduct.data)
      }

      fetchProduct()
    }
  }, [product])

  return (
    <Drawer
      title={`Edit "${product?.fullName}"`}
      opened={opened}
      onClose={() => console.log('close')}
      actions={
        <div className="grid w-full grid-cols-2 gap-4">
          <Button
            variant="default"
            disabled={form.loadingState === 'loading'}
            onClick={() => close()}
          >
            Cancel
          </Button>
          <Button loadingState={form.loadingState} onClick={() => editProduct()}>
            Save product
          </Button>
        </div>
      }
    >
      {product && (
        <Form
          {...form}
          elementsOptions={{
            unit: { options: unitsOptions, accessorKey: 'unit.id' },
            thumbnail: { placeholder: product.thumbnailUrl?.split('/').pop() },
          }}
        />
      )}
    </Drawer>
  )
}

export default ProductEditDrawer
