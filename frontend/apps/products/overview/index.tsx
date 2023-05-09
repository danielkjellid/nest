import React, { useState } from 'react'

import { Button } from '../../../components/Button'
import ProductAddDrawer from '../components/ProductAddDrawer'
import ProductEditDrawer from '../components/ProductEditDrawer'
import { ProductListOutAPIResponse } from '../../../types'
import { ProductOdaImportDrawer } from '../components/ProductOdaImportDrawer'
import ProductOverViewTable from './components/ProductOverviewTable'
import { Title } from '@mantine/core'
import View from '../../../components/View'
import { urls } from '../../urls'
import { useCommonContext } from '../../../contexts/CommonProvider'
import { useDisclosure } from '@mantine/hooks'
import { useFetch } from '../../../hooks/fetcher'

interface ProductOverviewInnerProps {
  results: {
    products: ProductListOutAPIResponse
  }
  refetch: () => void
}

function ProductOverviewInner({ results, refetch }: ProductOverviewInnerProps) {
  const { products } = results
  const { currentUser } = useCommonContext()

  const [addDrawerOpened, { open: addDrawerOpen, close: addDrawerClose }] = useDisclosure(false)
  const [editDrawerOpened, { open: editDrawerOpen, close: editDrawerClose }] = useDisclosure(false)
  const [odaImportDrawerOpened, { open: odaImportDrawerOpen, close: odaImportDrawerClose }] =
    useDisclosure(false)

  const [productIdToEdit, setProductIdToEdit] = useState<number>()
  const editProduct = (id: number) => {
    setProductIdToEdit(id)
    editDrawerOpen()
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title weight={600}>Products</Title>
        {currentUser.isStaff && (
          <div className="flex items-center space-x-3">
            <Button.Group>
              <Button variant="default" onClick={odaImportDrawerOpen}>
                Import from Oda
              </Button>
              <Button variant="default" onClick={addDrawerOpen}>
                Add new
              </Button>
            </Button.Group>
          </div>
        )}
      </div>
      <ProductOverViewTable data={products.data || []} onEditProduct={(id) => editProduct(id)} />
      <ProductAddDrawer opened={addDrawerOpened} onClose={addDrawerClose} refetch={refetch} />
      <ProductEditDrawer
        productId={productIdToEdit}
        opened={editDrawerOpened}
        onClose={editDrawerClose}
        refetch={refetch}
      />
      <ProductOdaImportDrawer
        opened={odaImportDrawerOpened}
        onClose={odaImportDrawerClose}
        refetch={refetch}
      />
    </div>
  )
}

function ProductOverview() {
  const products = useFetch<ProductListOutAPIResponse>(urls.products.list())

  const refetch = () => {
    products.reload()
  }

  return (
    <View<object, ProductOverviewInnerProps>
      component={ProductOverviewInner}
      results={{ products }}
      componentProps={{ refetch }}
      loadingProps={{ description: 'Loading products...' }}
      errorProps={{ description: 'There was an error getting products. Please try again.' }}
    />
  )
}

export { ProductOverview }
