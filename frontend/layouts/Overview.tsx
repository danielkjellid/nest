import { Title } from '@mantine/core'
import React from 'react'

interface OverviewProps {
  title: string
  actions?: React.ReactNode
  table?: React.ReactNode
}

function Overview({ title, actions, table }: OverviewProps) {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title weight={600}>{title}</Title>
        {actions && <div className="flex items-center space-x-3">{actions}</div>}
      </div>
      {table}
    </div>
  )
}

export { Overview }
