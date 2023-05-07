import { Anchor, Badge, Paper, Stepper, Table, Tabs, Text, Timeline, Title } from '@mantine/core'
import { ProductDetailAuditLogsOut, ProductDetailOutAPIResponse } from '../../../types'
import { useLocation, useParams } from 'react-router-dom'

import { Button } from '@mantine/core'
import { Card } from '../../../components/Card'
import React from 'react'
import { TableOfContents } from '../../../components/TableOfContents'
import View from '../../../components/View'
import invariant from 'tiny-invariant'
import { urls } from '../../urls'
import { useFetch } from '../../../hooks/fetcher'
import { useProductDetailStyles } from './detail.styles'

interface ProductDetailInnerProps {
  results: { productResponse: ProductDetailOutAPIResponse }
}

function ProductDetailInner({ results }: ProductDetailInnerProps) {
  const { classes } = useProductDetailStyles()
  const { data: product } = results.productResponse

  if (!product) return null

  const headings = [
    { label: 'Information', slug: 'information' },
    // { label: 'Nutrition', slug: 'nutrition' },
    { label: 'Prices', slug: 'prices' },
    { label: 'Oda', slug: 'oda' },
    { label: 'Changes', slug: 'changes' },
  ]

  const auditLogTableHeaders = [
    { label: 'User', value: 'user' },
    { label: 'Change', value: 'change' },
    { label: 'Date', value: 'date' },
    { label: 'IP', value: 'ip' },
  ]
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

  return (
    <div>
      <header className="flex items-center justify-between">
        <div className="flex items-center space-x-6">
          <img
            className={`object-contain w-16 h-16 p-1 border-2 ${classes.border} border-solid rounded-full`}
            src={product.thumbnailUrl}
            alt=""
          />
          <div>
            <div className="text-lg font-semibold leading-6">{product.fullName}</div>
            <div className="mt-1 text-sm">{product.supplier}</div>
          </div>
        </div>
        <Button.Group>
          <Button variant="default">Update from Oda</Button>
          <Button variant="default">View in admin</Button>
          <Button>Edit product</Button>
        </Button.Group>
      </header>
      <div className="lg:grid-cols-3 grid grid-cols-1 gap-6 mt-10">
        <div className="lg:order-1 lg:col-span-2 order-2 col-span-1 space-y-4">
          <div id="information">
            <Card title="Information">
              <Card.KeyValue k="Name" value={product.name} />
              <Card.KeyValue k="Supplier" value={product.supplier} />
              <Card.KeyValue k="Unit" value={product.unit.displayName} />
              <Card.KeyValue k="Unit quantity" value={product.unitQuantity} />
              {product.gtin && <Card.KeyValue k="Gtin" value={product.gtin} />}
              <Card.KeyValue k="Is available" value={product.isAvailable} />
              <Card.KeyValue k="Is synced" value={product.isSynced} />
            </Card>
          </div>
          {/* <div id="nutrition">
            <Card title="Nutrition">
              <p>Nutrition</p>
            </Card>
          </div> */}
          <div id="prices">
            <Card title="Prices">
              <Card.KeyValue k="Gross price" value={product.grossPrice} />
              <Card.KeyValue k="Gross unit price" value={product.grossUnitPrice} />
            </Card>
          </div>
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
          <div id="changes" className="mt-12">
            <Card title="Changes">
              <Card.Table headers={auditLogTableHeaders}>
                {product.auditLogs.map((logEntry, i) => (
                  <Card.TableRow
                    key={i}
                    headers={auditLogTableHeaders}
                    item={{
                      user: logEntry.user,
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
    </div>
  )
}

function ProductDetail() {
  const { productId } = useParams()

  invariant(productId)

  const productResponse = useFetch<ProductDetailOutAPIResponse>(
    urls.products.detail({ id: productId })
  )

  return (
    <View<object, any>
      component={ProductDetailInner}
      results={{ productResponse }}
      componentProps={{}}
      loadingProps={{ description: 'Loading product...' }}
      errorProps={{
        description: 'There was en error retrieving the product. Please try again later.',
      }}
    />
  )
}

export { ProductDetail }
