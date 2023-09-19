import { IngredientListOutAPIResponse, ProductListOutAPIResponse } from '../../types'

import { Button } from '../../components/Button'
import { IngredientAddDrawer } from './components/IngredientAddDrawer'
import { IngredientsOverviewTable } from './components/IngredientsOverviewTable'
import React from 'react'
import { Title } from '@mantine/core'
import View from '../../components/View'
import { urls } from '../urls'
import { useCommonContext } from '../../contexts/CommonProvider'
import { useDisclosure } from '@mantine/hooks'
import { useFetch } from '../../hooks/fetcher'
import { ConfirmationModal } from '../../components/ConfirmationModal'

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
  const [
    deleteConfirmModalOpened,
    { open: deleteConfirmModalOpen, close: deleteConfirmModalClose },
  ] = useDisclosure()

  const deleteIngredient = () => {}

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
        onDeleteIngredient={deleteConfirmModalOpen}
      />
      <IngredientAddDrawer
        opened={addDrawerOpened}
        products={products.data || []}
        onClose={addDrawerClose}
        refetch={refetch}
      />
      {/* Should probably be moved down so we dont have to store the id up here */}
      <ConfirmationModal
        opened={deleteConfirmModalOpened}
        onClose={deleteConfirmModalClose}
        title="Are you sure?"
        onConfirm={() => console.log('confirm')}
        confirmButtonText="Delete ingredient"
        confirmButtonColor="red"
      >
        <p>Are you sure you want to delete this ingredient? This action is permanent.</p>
      </ConfirmationModal>
    </div>
  )
}

function IngredientsOverview() {
  const ingredients = useFetch<IngredientListOutAPIResponse>(urls.ingredients.list())
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
