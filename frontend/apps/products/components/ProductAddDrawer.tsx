import { Button } from '../../../components/Button'
import Drawer from '../../../components/Drawer'
import Form from '../../../components/Form'
import { ProductCreateIn } from '../../../types'
import React from 'react'
import { performPost } from '../../../hooks/fetcher/http'
import { urls } from '../../urls'
import { useForm } from '../../../hooks/forms'
import { useUnits } from '../../../contexts/UnitsProvider'

interface ProductAddDrawerProps {
  opened: boolean
  onClose: () => void
  refetch: () => void
}

function ProductAddDrawer({ opened, onClose, refetch }: ProductAddDrawerProps) {
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
      await performPost({ url: urls.products.create(), ...form.buildPayload() })
      form.setLoadingState('success')
      close()
      refetch()
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
