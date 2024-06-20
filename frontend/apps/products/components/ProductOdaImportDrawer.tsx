import { Alert, Badge } from '@mantine/core'
import { useState } from 'react'

import { Button, type ButtonProps } from '../../../components/Button'
import Drawer from '../../../components/Drawer'
import Form from '../../../components/Form'
import { performPost } from '../../../hooks/fetcher/http'
import { useForm } from '../../../hooks/forms'
import { useCommonStyles } from '../../../styles/common'
import {
  type ProductOdaImportForm,
  type ProductOdaImportOutAPIResponse,
  type ProductOdaImportOut,
} from '../../../types'
import { urls } from '../../urls'

interface ProductOdaImportDrawerProps {
  opened: boolean
  onClose: () => void
  refetch: () => void
}

function ProductOdaImportDrawer({ opened, onClose, refetch }: ProductOdaImportDrawerProps) {
  /***********
   ** State **
   ***********/
  const { classes } = useCommonStyles()
  const form = useForm<ProductOdaImportForm>({ key: 'ProductOdaImportForm' })
  const [fetchedProductData, setFetchedProductData] = useState<ProductOdaImportOut | null>()
  const [importLoadingState, setImportLoadingState] =
    useState<ButtonProps['loadingState']>('initial')

  /**************
   ** Handlers **
   **************/

  const close = () => {
    onClose()
    form.resetForm()
    setFetchedProductData(null)
  }

  const fetchOdaProduct = async () => {
    try {
      form.setLoadingState('loading')
      const response = await performPost<ProductOdaImportOutAPIResponse>({
        url: urls.products.oda.import(),
        ...form.buildPayload(),
      })
      form.setLoadingState('success')

      if (response && response.data) {
        setFetchedProductData(response.data)
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
    if (!fetchedProductData) return
    try {
      setImportLoadingState('loading')
      await performPost({
        url: urls.products.oda.importConfirm(),
        data: { odaProductId: fetchedProductData.product.id },
      })
      setImportLoadingState('success')
      close()
      refetch()
    } catch (e) {
      console.error(e)
      setImportLoadingState('error')
    }
  }

  return (
    <Drawer
      title="Import product from Oda"
      opened={opened}
      onClose={close}
      actions={
        <div className="grid w-full grid-cols-2 gap-4">
          <Button
            variant="default"
            disabled={form.loadingState === 'loading'}
            onClick={() => close()}
          >
            Cancel
          </Button>
          <Button
            loadingState={importLoadingState}
            disabled={!fetchedProductData || fetchedProductData.hasBeenImportedPreviously}
            onClick={() => importOdaProduct()}
          >
            Import product
          </Button>
        </div>
      }
    >
      <Form<ProductOdaImportForm>
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
      {fetchedProductData && (
        <div className="mt-6 space-y-6">
          {fetchedProductData.hasBeenImportedPreviously && (
            <Alert color="red">This product is already imported.</Alert>
          )}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-6">
              <img
                className={`object-contain w-16 h-16 p-1 border-2 ${classes.border} border-solid rounded-lg bg-white`}
                src={fetchedProductData.product.images[0].thumbnail.url}
                alt=""
              />
              <div className="w-80 overflow-hidden">
                <div className="whitespace-nowrap text-ellipsis overflow-hidden text-lg font-semibold leading-6">
                  {fetchedProductData.product.fullName},{' '}
                  {Number(fetchedProductData.product.grossPrice) /
                    Number(fetchedProductData.product.grossUnitPrice)}{' '}
                  {fetchedProductData.product.unitPriceQuantityAbbreviation}
                </div>
                {fetchedProductData.product.brand ? (
                  <div className="mt-1 text-sm">{fetchedProductData.product.brand}</div>
                ) : (
                  <div className="mt-1 text-sm">Unknown supplier</div>
                )}
              </div>
            </div>
            <div className="shrink-0 flex flex-col text-right">
              <Badge size="lg" color="green">
                Available
              </Badge>
              <div className="mt-2 text-sm">{fetchedProductData.product.grossPrice} kr</div>
            </div>
          </div>
        </div>
      )}
    </Drawer>
  )
}

export { ProductOdaImportDrawer }
