import { Button } from '../../../../components/Button'
import Drawer from '../../../../components/Drawer'
import Form from '../../../../components/Form'
import { ProductCreateIn } from '../../../../types'
import React from 'react'
import { performPost } from '../../../../hooks/fetcher/http'
import urls from '../../urls'
import { useForm } from '../../../../hooks/forms'
import { useUnits } from '../../../../contexts/UnitsProvider'

interface ProductAddDrawerProps {
  opened: boolean
  onClose: () => void
}

function ProductAddDrawer({ opened, onClose }: ProductAddDrawerProps) {
  const form = useForm({ key: 'ProductCreateIn' })
  const units = useUnits()
  const unitsOptions = units.map((unit) => ({ label: unit.displayName, value: unit.id.toString() }))

  const close = () => {
    form.resetForm()
    onClose()
  }

  const addProduct = async () => {
    try {
      form.setLoadingState('loading')
      await performPost(urls.productCreate(), form.buildPayload())
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

  return (
    <Drawer
      title="Add product"
      opened={opened}
      onClose={onClose}
      actions={
        <div className="grid grid-cols-2 gap-4 w-full">
          <Button
            variant="default"
            disabled={form.loadingState === 'loading'}
            onClick={() => close()}
          >
            Cancel
          </Button>
          <Button loadingState={form.loadingState} onClick={() => addProduct()}>
            Add product
          </Button>
        </div>
      }
    >
      <div className="space-y-5">
        <Form<ProductCreateIn>
          {...form}
          elementsOptions={{ unit: { options: unitsOptions || [] } }}
        />
      </div>
    </Drawer>
  )
}

export default ProductAddDrawer
