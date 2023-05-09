import { Button, ButtonProps } from '../../../components/Button'
import {
  ProductOdaImportIn,
  ProductOdaImportOut,
  ProductOdaImportOutAPIResponse,
} from '../../../types'
import React, { useState } from 'react'
import { performGet, performPost } from '../../../hooks/fetcher/http'

import { Badge } from '@mantine/core'
import Drawer from '../../../components/Drawer'
import Form from '../../../components/Form'
import { urls } from '../../urls'
import { useCommonStyles } from '../../../styles/common'
import { useForm } from '../../../hooks/forms'

interface ProductOdaImportDrawerProps {
  opened: boolean
  onClose: () => void
  refetch: () => void
}

function ProductOdaImportDrawer({ opened, onClose, refetch }: ProductOdaImportDrawerProps) {
  const { classes } = useCommonStyles()
  const form = useForm<ProductOdaImportIn>({ key: 'ProductOdaImportIn' })

  const [fetchedProduct, setFetchedProduct] = useState<ProductOdaImportOut>()
  const [importLoadingState, setImportLoadingState] =
    useState<ButtonProps['loadingState']>('initial')

  const fetchOdaProduct = async () => {
    try {
      form.setLoadingState('loading')
      const response = await performPost<ProductOdaImportOutAPIResponse>({
        url: urls.products.oda.import(),
        ...form.buildPayload(),
      })
      form.setLoadingState('success')

      if (response && response.data) {
        setFetchedProduct(response.data)
      }
    } catch (e) {
      const errorResponse = (e as any).response.data
      form.setLoadingState('error')
      if (errorResponse) {
        form.setErrors(errorResponse.data)
      }
    }
  }

  const importOdaProduct = async () => {
    if (!fetchedProduct) return
    try {
      setImportLoadingState('loading')
      await performPost({
        url: urls.products.oda.importConfirm(),
        data: { odaProductId: fetchedProduct.id },
      })
      setImportLoadingState('success')

      // TODO: cleanup
    } catch (e) {
      console.error(e)
      setImportLoadingState('error')
    }
  }

  return (
    <Drawer
      title="Import product from Oda"
      opened={opened}
      onClose={onClose}
      actions={
        <div className="grid w-full grid-cols-2 gap-4">
          <Button
            variant="default"
            disabled={form.loadingState === 'loading'}
            onClick={() => close()}
          >
            Cancel
          </Button>
          <Button disabled={!fetchedProduct} onClick={() => importOdaProduct()}>
            Import product
          </Button>
        </div>
      }
    >
      <Form<ProductOdaImportIn>
        {...form}
        elementsOptions={{
          odaProductId: {
            afterSlot: (
              <Button
                variant="default"
                loadingState={form.loadingState}
                disabled={!form.data || !form.data['odaProductId']}
                onClick={() => fetchOdaProduct()}
              >
                Get product
              </Button>
            ),
          },
        }}
      />
      {fetchedProduct && (
        <div className="mt-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <img
                className={`object-contain w-16 h-16 p-1 border-2 ${classes.border} border-solid rounded-lg bg-white`}
                src={fetchedProduct.thumbnailUrl}
                alt=""
              />
              <div>
                <div className="text-lg font-semibold leading-6">
                  {fetchedProduct.fullName}, {fetchedProduct.unitQuantity} {fetchedProduct.unit}
                </div>
                <div className="mt-1 text-sm">{fetchedProduct.supplier}</div>
              </div>
            </div>
            <div className="flex flex-col text-right">
              <Badge size="lg" color="green">
                Available
              </Badge>
              <div className="mt-2 text-sm">{fetchedProduct.grossPrice} kr</div>
            </div>
          </div>
        </div>
      )}
    </Drawer>
  )
}

export { ProductOdaImportDrawer }
