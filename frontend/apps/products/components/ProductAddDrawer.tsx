import { Button } from '../../../components/Button'
import Drawer from '../../../components/Drawer'
import Form from '../../../components/Form'
import { useUnits } from '../../../contexts/UnitsProvider'
import { useForm } from '../../../hooks/forms'
import { type ProductCreateIn } from '../../../types'
import { urls } from '../../urls'

interface ProductAddDrawerProps {
  opened: boolean
  onClose: () => void
  refetch: () => void
}

function ProductAddDrawer({ opened, onClose, refetch }: ProductAddDrawerProps) {
  const form = useForm({ key: 'ProductCreateIn' })
  const { unitsOptions } = useUnits()

  const close = () => {
    form.resetForm()
    onClose()
  }

  const addProduct = async () => {
    await form.performPost({ url: urls.products.create() })
    refetch()
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
