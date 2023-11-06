import { Title } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { notifications } from '@mantine/notifications'
import React from 'react'

import { Button } from '../../components/Button'
import View from '../../components/View'
import { useCommonContext } from '../../contexts/CommonProvider'
import { useConfirmModal } from '../../hooks/confirm-modal'
import { useFetch } from '../../hooks/fetcher'
import { performDelete } from '../../hooks/fetcher/http'
import {
  type IngredientDeleteIn,
  type IngredientListOutAPIResponse,
  type ProductListOutAPIResponse,
} from '../../types'
import { urls } from '../urls'

import { IngredientAddDrawer } from './components/IngredientAddDrawer'
import { IngredientsOverviewTable } from './components/IngredientsOverviewTable'

interface IngredientsOverviewInnerProps {
  results: {
    ingredients: IngredientListOutAPIResponse
    products: ProductListOutAPIResponse
  }
  refetch: () => void
}

function IngredientsOverviewInner({ results, refetch }: IngredientsOverviewInnerProps) {
  const { ingredients, products } = results
  const { currentUser } = useCommonContext()

  const [addDrawerOpened, { open: addDrawerOpen, close: addDrawerClose }] = useDisclosure()

  const deleteIngredient = async (id: number) => {
    modal.close()
    const payload: IngredientDeleteIn = { ingredientId: id }
    try {
      await performDelete({ url: urls.recipes.ingredients.delete(), data: payload })
      refetch()
      notifications.show({
        color: 'green',
        title: 'Ingredient deleted',
        message: 'Ingredient was successfully deleted.',
      })
    } catch (e) {
      console.log(e)
    }
  }

  const modal = useConfirmModal({
    title: 'Are you sure?',
    children: <p>Are you sure you want to delete this ingredient? This action is permanent.</p>,
    buttons: {
      confirm: { label: 'Delete ingredient', color: 'red' },
      cancel: { label: 'Cancel' },
    },
    onConfirm: deleteIngredient,
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title weight={600}>Ingredients</Title>
        {currentUser && currentUser.isStaff && (
          <div className="flex items-center space-x-3">
            <Button.Group>
              <Button variant="default" onClick={addDrawerOpen}>
                Add new
              </Button>
            </Button.Group>
          </div>
        )}
      </div>
      <IngredientsOverviewTable
        data={ingredients.data || []}
        onDeleteIngredient={(id: number) => modal.open(id)}
      />
      <IngredientAddDrawer
        opened={addDrawerOpened}
        products={products.data || []}
        onClose={addDrawerClose}
        refetch={refetch}
      />
      {modal.render()}
    </div>
  )
}

function IngredientsOverview() {
  const ingredients = useFetch<IngredientListOutAPIResponse>(urls.recipes.ingredients.list())
  const products = useFetch<ProductListOutAPIResponse>(urls.products.list())

  const refetch = () => {
    ingredients.reload()
  }

  return (
    <View<object, IngredientsOverviewInnerProps>
      component={IngredientsOverviewInner}
      results={{ ingredients, products }}
      componentProps={{ refetch }}
      loadingProps={{ description: 'Loading ingredients' }}
      errorProps={{ description: 'There was an error getting ingredients. Please try again.' }}
    />
  )
}

export { IngredientsOverview }
