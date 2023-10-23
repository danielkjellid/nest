import { Button } from '../../../components/Button'
import React from 'react'
import { RecipeListOutAPIResponse } from '../../../types'
import Table from '../../../components/Table'
import { Title } from '@mantine/core'
import View from '../../../components/View'
import { routes } from '../routes'
import { urls } from '../../urls'
import { useCommonContext } from '../../../contexts/CommonProvider'
import { useFetch } from '../../../hooks/fetcher'
import { useNavigate } from 'react-router-dom'
import { RecipeListOut } from '../../../types'
import { Anchor } from '@mantine/core'
interface RecipeOverviewInnerProps {
  results: { recipes: RecipeListOutAPIResponse }
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
              <Button variant="default" onClick={() => navigate(routes.createRecipe.build())}>
                Add new
              </Button>
            </Button.Group>
          </div>
        )}
      </div>
      <Table<RecipeListOut>
        rowIdentifier="id"
        columns={[
          {
            header: 'Title',
            accessorKey: 'title',
            id: 'title',
            Cell: ({ row, renderedCellValue }) => (
              <Anchor href={routes.detail.build({ recipeId: row.original.id })}>
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
      />
    </div>
  )
}

function RecipeOverview() {
  const recipes = useFetch<RecipeListOutAPIResponse>(urls.recipes.list())

  return (
    <View<object, RecipeOverviewInnerProps>
      component={RecipeOverviewInner}
      results={{ recipes }}
      componentProps={{}}
      loadingProps={{ description: 'Loading recipes' }}
      errorProps={{ description: 'There was an error getting recipes. Please try again.' }}
    />
  )
}

export { RecipeOverview }
