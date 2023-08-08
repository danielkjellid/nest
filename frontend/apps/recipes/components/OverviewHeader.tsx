import React from 'react'
import { Title, Tabs } from '@mantine/core'
import { routes } from '../routes'
import { useLocation, useNavigate } from 'react-router-dom'

interface OverviewHeaderProps {
  title: string
  actions?: React.ReactNode
}

function OverviewHeader({ title, actions }: OverviewHeaderProps) {
  const path = useLocation()
  const navigate = useNavigate()
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title weight={600}>{title}</Title>
        {actions}
      </div>
      <Tabs value={path.pathname} onTabChange={(value) => navigate(`${value}`)}>
        <Tabs.List>
          <Tabs.Tab value={routes.overview.path}>Recipes</Tabs.Tab>
          <Tabs.Tab value={routes.ingredientsOverview.path}>Ingredients</Tabs.Tab>
        </Tabs.List>
      </Tabs>
    </div>
  )
}

export { OverviewHeader }
