import { Anchor, Title } from '@mantine/core'

import Empty from '../../components/Empty'
import Table from '../../components/Table'
import View from '../../components/View'
import { useCommonContext } from '../../contexts/CommonProvider'
import { useFetch } from '../../hooks/fetcher'
import { type RecipePlanRecordListAPIResponse } from '../../types'
import { routes as recipeRoutes } from '../recipe/routes'
import { urls } from '../urls'

interface PlansAppInnerProps {
  results: { plans: RecipePlanRecordListAPIResponse }
}

function PlansAppInner({ results }: PlansAppInnerProps) {
  const { plans } = results
  const planItems = plans && plans.data ? plans?.data.flatMap((plan) => plan.items) : []

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-3">
        <Title weight={600}>Plans</Title>
      </div>
      <Table<any>
        initialState={{ grouping: ['planTitle'] }}
        positionToolbarAlertBanner="none"
        rowIdentifier="id"
        columns={[
          {
            header: 'Recipes',
            accessorKey: 'recipe.title',
            Cell: ({ row, renderedCellValue }) => (
              <Anchor href={recipeRoutes.detail.build({ recipeId: row.original.recipe.id })}>
                {renderedCellValue}
              </Anchor>
            ),
          },
          { header: 'Plan', accessorKey: 'planTitle' },
        ]}
        data={planItems}
      />
    </div>
  )
}

function PlansApp() {
  const { currentHome } = useCommonContext()

  if (currentHome === null) {
    return (
      <Empty
        title="You are currently not assigned any homes"
        message="Please contact an admin."
        className="h-full"
      />
    )
  }

  const plans = useFetch<RecipePlanRecordListAPIResponse>(
    urls.recipes.plans.list({ id: currentHome.id })
  )

  return (
    <View<object, PlansAppInnerProps>
      component={PlansAppInner}
      results={{ plans: plans }}
      componentProps={{}}
      loadingProps={{ description: 'Loading plans...' }}
      errorProps={{ description: 'There was an error getting plans.' }}
    />
  )
}

export default PlansApp
