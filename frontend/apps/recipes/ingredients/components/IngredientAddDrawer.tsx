import React, { forwardRef } from 'react'
import Drawer from '../../../../components/Drawer'
import { useForm } from '../../../../hooks/forms'
import Form from '../../../../components/Form'
import { IngredientCreateIn, ProductListOut } from '../../../../types'
import { Text } from '@mantine/core'
import { Button } from '../../../../components/Button'
import { urls } from '../../../urls'

interface IngredientAddDrawerProps {
  opened: boolean
  products: ProductListOut[]
  onClose: () => void
  refetch: () => void
}

function IngredientAddDrawer({ opened, products, onClose, refetch }: IngredientAddDrawerProps) {
  const form = useForm({ key: 'IngredientCreateIn' })
  const productsOptions = products.map((product) => ({
    image: product.thumbnailUrl,
    label: product.fullName,
    value: product.id.toString(),
    description: `${product.displayPrice}`,
  }))

  const close = () => {
    onClose()
  }

  const addIngredient = async () => {
    await form.performPost({ url: urls.recipes.ingredients.create() })
    refetch()
  }

  return (
    <Drawer
      title="Add ingredient"
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
          <Button loadingState={form.loadingState} onClick={() => addIngredient()}>
            Add ingredient
          </Button>
        </div>
      }
    >
      <div className="space-y-5">
        <Form<IngredientCreateIn>
          {...form}
          elementsOptions={{
            product: { options: productsOptions || [], itemComponent: ProductOption },
          }}
        />
      </div>
    </Drawer>
  )
}

interface ProductOptionProps extends React.ComponentPropsWithoutRef<'div'> {
  image?: string | null
  label: string
  description: string
}

const ProductOption = forwardRef<HTMLDivElement, ProductOptionProps>(
  ({ image, label, description, ...others }: ProductOptionProps, ref) => (
    <div ref={ref} {...others}>
      <div className="flex items-center space-x-3">
        <img src={image || ''} className="object-contain w-12 h-12 rounded-md" />
        <div>
          <Text size="sm">{label}</Text>
          <Text size="xs" opacity={0.65}>
            {description}
          </Text>
        </div>
      </div>
    </div>
  )
)

ProductOption.displayName = 'ProductOption'

export { IngredientAddDrawer }
