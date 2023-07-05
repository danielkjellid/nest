import { ProductDetailAuditLogsOut, ProductDetailOutAPIResponse } from '../../../types'

import { Anchor } from '@mantine/core'
import { Button } from '../../../components/Button'
import { Card } from '../../../components/Card'
import { Button as MButton } from '@mantine/core'
import ProductEditDrawer from '../components/ProductEditDrawer'
import React from 'react'
import { TableOfContents } from '../../../components/TableOfContents'
import View from '../../../components/View'
import invariant from 'tiny-invariant'
import { urls } from '../../urls'
import { useCommonContext } from '../../../contexts/CommonProvider'
import { useCommonStyles } from '../../../styles/common'
import { useDisclosure } from '@mantine/hooks'
import { useFetch } from '../../../hooks/fetcher'
import { useParams } from 'react-router-dom'
import { useProductDetailStyles } from './detail.styles'

interface ProductDetailInnerProps {
  results: { productResponse: ProductDetailOutAPIResponse }
  refetch: () => void
}

function ProductDetailInner({ results, refetch }: ProductDetailInnerProps) {
  const { classes } = useProductDetailStyles()
  const { classes: commonClasses } = useCommonStyles()
  const { currentUser } = useCommonContext()
  const { data: product } = results.productResponse
  const [editDrawerOpened, { open: editDrawerOpen, close: editDrawerClose }] = useDisclosure(false)

  if (!product) return null

  const auditLogTableHeaders = [
    { label: 'User/Source', value: 'userOrSource' },
    { label: 'Change', value: 'change' },
    { label: 'Date', value: 'date' },
    { label: 'IP', value: 'ip' },
  ]

  // Format change message by highlighting changes, making it a bit more readable.
  const formatChangeMessage = ({ changes }: { changes: ProductDetailAuditLogsOut['changes'] }) => {
    return (
      <div>
        {Object.entries(changes).map(([field, change], i) => (
          <p key={i} className="mb-2">
            <code className={classes.changeMessageCode}>{field}</code> changed from{' '}
            <code className={classes.changeMessageCode}>{change[0]}</code> to{' '}
            <code className={classes.changeMessageCode}>{change[1]}</code>
          </p>
        ))}
      </div>
    )
  }

  let headings = []
  if (product.isOdaProduct) {
    headings = [
      { label: 'Information', slug: 'information' },
      { label: 'Nutrition', slug: 'nutrition' },
      { label: 'Prices', slug: 'prices' },
      { label: 'Oda', slug: 'oda' },
      { label: 'Changes', slug: 'changes' },
    ]
  } else {
    headings = [
      { label: 'Information', slug: 'information' },
      { label: 'Nutrition', slug: 'nutrition' },
      { label: 'Prices', slug: 'prices' },
      { label: 'Changes', slug: 'changes' },
    ]
  }

  return (
    <div>
      <header className="lg:grid-cols-2 grid content-center grid-cols-1 gap-8">
        <div className="lg:order-1 flex items-center self-center order-2 space-x-6">
          <img
            className={`object-contain w-16 h-16 p-1 border-2 ${commonClasses.border} border-solid rounded-lg bg-white`}
            src={product.thumbnailUrl}
            alt=""
          />
          <div>
            <div className="text-lg font-semibold leading-6">{product.fullName}</div>
            <div className="mt-1 text-sm">{product.supplier}</div>
          </div>
        </div>
        {currentUser.isStaff && (
          <div className="lg:order-2 justify-self-start lg:justify-self-end self-center order-1 space-x-1">
            {product.isOdaProduct && <Button variant="default">Update from Oda</Button>}
            {currentUser.isSuperuser && (
              <MButton
                component="a"
                href={`/admin/products/product/${product.id}/`}
                target="_blank"
                variant="default"
              >
                View in admin
              </MButton>
            )}
            <Button onClick={editDrawerOpen}>Edit product</Button>
          </div>
        )}
      </header>
      <div className="lg:grid-cols-3 grid grid-cols-1 gap-6 mt-10">
        <div className="lg:order-1 lg:col-span-2 order-2 col-span-1 space-y-4">
          <div id="information">
            <Card title="Information">
              <Card.KeyValue k="Name" value={product.name} />
              {product.supplier && <Card.KeyValue k="Supplier" value={product.supplier} />}
              <Card.KeyValue k="Unit" value={product.unit.displayName} />
              <Card.KeyValue k="Unit quantity" value={product.unitQuantity} />
              {product.gtin && <Card.KeyValue k="Gtin" value={product.gtin} />}
              <Card.KeyValue k="Is available" value={product.isAvailable} />
              <Card.KeyValue k="Is synced" value={product.isSynced} />
              <Card.KeyValue k="Gluten free" value={!product.containsGluten} />
              <Card.KeyValue k="Lactose free" value={!product.containsLactose} />
              {product.thumbnailUrl && (
                <Card.KeyValue
                  k="Picture"
                  value={
                    <Anchor href={product.thumbnailUrl} target="_blank">
                      {product.thumbnailUrl}
                    </Anchor>
                  }
                />
              )}
              {product.lastDataUpdate && (
                <Card.KeyValue k="Last data update" value={product.lastDataUpdate} />
              )}
            </Card>
          </div>
          <div id="nutrition">
            <Card title="Nutrition" subtitle="Nutritional content per 100g/ml">
              <Card.Table
                headers={[
                  { label: 'Label', value: 'title' },
                  { label: 'Content', value: 'value' },
                ]}
                parentIdentifier="parentKey"
                items={product.nutrition}
              />
            </Card>
          </div>
          <div id="prices">
            <Card title="Prices">
              <Card.KeyValue k="Gross price" value={product.grossPrice} />
              <Card.KeyValue k="Gross unit price" value={product.grossUnitPrice} />
            </Card>
          </div>
          {product.isOdaProduct && (
            <div id="oda">
              <Card title="Oda">
                <Card.KeyValue k="Gross price" value={product.odaId} />
                <Card.KeyValue
                  k="Gross price"
                  value={
                    <Anchor href={product.odaUrl} target="_blank">
                      {product.odaUrl}
                    </Anchor>
                  }
                />
              </Card>
            </div>
          )}
          <div id="changes" className="mt-12">
            <Card title="Changes">
              <Card.Table headers={auditLogTableHeaders}>
                {product.auditLogs.map((logEntry, i) => (
                  <Card.TableRow
                    key={i}
                    headers={auditLogTableHeaders}
                    item={{
                      userOrSource: logEntry.userOrSource,
                      change: formatChangeMessage({ changes: logEntry.changes }),
                      date: logEntry.createdAt,
                      ip: logEntry.remoteAddr,
                    }}
                  />
                ))}
              </Card.Table>
            </Card>
          </div>
        </div>
        <div className="lg:order-2 order-1 col-span-1 space-y-8">
          <TableOfContents headings={headings} />
        </div>
      </div>
      <ProductEditDrawer
        productId={product.id}
        opened={editDrawerOpened}
        onClose={editDrawerClose}
        refetch={refetch}
      />
    </div>
  )
}

function ProductDetail() {
  const { productId } = useParams()
  invariant(productId)

  const productResponse = useFetch<ProductDetailOutAPIResponse>(
    urls.products.detail({ id: productId })
  )

  const refetch = () => {
    productResponse.reload()
  }

  return (
    <View<object, any>
      component={ProductDetailInner}
      results={{ productResponse }}
      componentProps={{ refetch }}
      loadingProps={{ description: 'Loading product...' }}
      errorProps={{
        description: 'There was en error retrieving the product. Please try again later.',
      }}
    />
  )
}

export { ProductDetail }
