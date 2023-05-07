import { Badge, Paper, Stepper, Table, Tabs, Text, Timeline, Title } from '@mantine/core'

import { Button } from '@mantine/core'
import { Card } from '../../../components/Card'
import React from 'react'
import { TableOfContents } from '../../../components/TableOfContents'
import View from '../../../components/View'

function ProductDetailInner() {
  return (
    <div>
      <header className="flex items-center justify-between">
        <div className="flex items-center space-x-6">
          <div className="w-16 h-16 bg-red-400 rounded-full"></div>
          <div>
            <div className="text-lg font-semibold leading-6">Coca-Cola 0.5l</div>
            <div className="mt-1 text-sm">Coca-Cola Company</div>
          </div>
        </div>
        <Button.Group>
          <Button variant="default">Update from Oda</Button>
          <Button variant="default">View in admin</Button>
          <Button>Edit product</Button>
        </Button.Group>
      </header>
      <div className="grid grid-cols-3 gap-6 mt-10">
        <div className="col-span-2 space-y-4">
          <div id="information">
            <Card
              title="Information"
              subtitle="All base information about the product."
              withDivider
            >
              <Card.KeyValue k="first name" value="Maggie foster" />
              <Card.KeyValue k="first name" value="Maggie foster" />
              <Card.KeyValue k="first name" value="Maggie foster" />
              <Card.KeyValue k="first name" value="Maggie foster" />
              <Card.KeyValue k="first name" value={<Badge>Test</Badge>} />
            </Card>
          </div>
          <div id="changes" className="mt-12">
            <Card title="Changes">
              <Card.Table
                headers={[
                  { label: 'User', value: 'user' },
                  { label: 'Change', value: 'change' },
                  { label: 'Date', value: 'date' },
                  { label: 'IP', value: 'ip' },
                ]}
                items={[
                  {
                    user: 'Daniel Kjellid',
                    change: 'first_name changed from some random value to some other random value',
                    date: '23.04.2023 15:43',
                    ip: '185.32.202.116',
                  },
                ]}
              />
            </Card>
          </div>
        </div>
        <div className="col-span-1 space-y-8">
          <TableOfContents
            headings={[
              { label: 'Information', slug: 'information' },
              { label: 'Changes', slug: 'changes' },
            ]}
          />
        </div>
      </div>
    </div>
  )
}

function ProductDetail() {
  return (
    <View<object, any>
      component={ProductDetailInner}
      results={{}}
      componentProps={{}}
      loadingProps={{ description: 'Loading product...' }}
      errorProps={{
        description: 'There was en error retrieving the product. Please try again later.',
      }}
    />
  )
}

export { ProductDetail }
