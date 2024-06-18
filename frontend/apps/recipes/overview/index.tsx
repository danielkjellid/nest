import { Anchor, Menu, Title } from '@mantine/core'
import { IconEdit } from '@tabler/icons-react'
import { useNavigate } from 'react-router-dom'

import { Button } from '../../../components/Button'
import Table from '../../../components/Table'
import View from '../../../components/View'
import { useCommonContext } from '../../../contexts/CommonProvider'
import { useFetch } from '../../../hooks/fetcher'
import { type RecipeRecord, type RecipeRecordListAPIResponse } from '../../../types'
import { routes as recipeRoutes } from '../../recipe/routes'
import { urls } from '../../urls'
import { routes } from '../routes'

interface RecipeOverviewInnerProps {
  results: { recipes: RecipeRecordListAPIResponse }
}

function RecipeOverviewInner({ results }: RecipeOverviewInnerProps) {
  const { currentUser } = useCommonContext()
  const navigate = useNavigate()

  const { recipes } = results

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title weight={600}>Recipes</Title>
        {currentUser && currentUser.isStaff && (
          <div className="flex items-center space-x-3">
            <Button.Group>
              <Button variant="default" onClick={() => navigate(routes.create.build())}>
                Add new
              </Button>
            </Button.Group>
          </div>
        )}
      </div>
      <Table<RecipeRecord>
        rowIdentifier="id"
        columns={[
          {
            header: 'Title',
            accessorKey: 'title',
            id: 'title',
            Cell: ({ row, renderedCellValue }) => (
              <Anchor href={recipeRoutes.detail.build({ recipeId: row.original.id })}>
                {renderedCellValue}
              </Anchor>
            ),
          },
          { header: 'Portions', accessorKey: 'defaultNumPortions' },
          { header: 'Status', accessorKey: 'statusDisplay' },
          { header: 'Difficulty', accessorKey: 'difficultyDisplay' },
          { header: 'Vegetarian', accessorKey: 'isVegetarian', options: { isBoolean: true } },
          { header: 'Pescatarian', accessorKey: 'isPescatarian', options: { isBoolean: true } },
        ]}
        data={recipes.data || []}
        actionMenuItems={({ row }) => [
          <Menu.Item
            key="delete"
            icon={<IconEdit />}
            onClick={() => navigate(routes.edit.build({ recipeId: row.original.id }))}
          >
            Edit
          </Menu.Item>,
        ]}
      />
    </div>
  )
}

function RecipeOverview() {
  const recipes = useFetch<RecipeRecordListAPIResponse>(urls.recipes.list())

  return (
    <View<object, RecipeOverviewInnerProps>
      component={RecipeOverviewInner}
      results={{ recipes: recipes }}
      componentProps={{}}
      loadingProps={{ description: 'Loading recipes' }}
      errorProps={{ description: 'There was an error getting recipes. Please try again.' }}
    />
  )
}

export { RecipeOverview }
