import React from 'react'
import View from '../../components/View'
import { OverviewHeader } from '../recipes/components/OverviewHeader'
import { IngredientsOverviewTable } from './components/IngredientsOverviewTable'
import { useFetch } from '../../hooks/fetcher'
import { IngredientListOutAPIResponse, ProductListOutAPIResponse } from '../../types'
import { useCommonContext } from '../../contexts/CommonProvider'
import { Button } from '../../components/Button'

import { urls } from '../urls'
import { IngredientAddDrawer } from './components/IngredientAddDrawer'
import { useDisclosure } from '@mantine/hooks'
import { Title } from '@mantine/core'

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
      <IngredientsOverviewTable data={ingredients.data || []} />
      <IngredientAddDrawer
        opened={addDrawerOpened}
        products={products.data || []}
        onClose={addDrawerClose}
        refetch={refetch}
      />
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
