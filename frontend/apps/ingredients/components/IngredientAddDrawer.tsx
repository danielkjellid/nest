import { Text } from '@mantine/core'
import React, { forwardRef } from 'react'

import { Button } from '../../../components/Button'
import Drawer from '../../../components/Drawer'
import Form from '../../../components/Form'
import { useForm } from '../../../hooks/forms'
import { type IngredientCreateIn, type ProductListOut } from '../../../types'
import { urls } from '../../urls'

interface ProductOptionProps extends React.ComponentPropsWithoutRef<'div'> {
  image: string | null
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
    form.resetForm()
  }

  const addIngredient = async () => {
    await form.performPost({ url: urls.recipes.ingredients.create() })
    refetch()
    close()
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

export { IngredientAddDrawer }
