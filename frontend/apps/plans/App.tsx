import { Anchor, Title } from '@mantine/core'

import { Button } from '../../components/Button'
import Empty from '../../components/Empty'
import Form from '../../components/Form'
import Table from '../../components/Table'
import View from '../../components/View'
import { useCommonContext } from '../../contexts/CommonProvider'
import { useFetch } from '../../hooks/fetcher'
import { useForm } from '../../hooks/forms'
import {
  type HomeRecord,
  type RecipePlanCreateForm,
  type RecipePlanItemRecord,
  type RecipePlanRecordListAPIResponse,
} from '../../types'
import { routes as recipeRoutes } from '../recipe/routes'
import { urls } from '../urls'
import { notifications } from '@mantine/notifications'

interface PlansAppInnerProps {
  results: { plans: RecipePlanRecordListAPIResponse }
  currentHome: HomeRecord
  refetch: () => void
}

function PlansAppInner({ results, currentHome, refetch }: PlansAppInnerProps) {
  const { plans } = results
  const planItems = plans && plans.data ? plans?.data.flatMap((plan) => plan.items) : []
  const form = useForm<RecipePlanCreateForm>({
    key: 'RecipePlanCreateForm',
    initialData: {
      budget: currentHome.weeklyBudget.toString(),
      portionsPerRecipe: currentHome.numResidents,
      recipesAmount: 7,
    },
  })

  const onCreatePlan = async () => {
    await form.performPost({ url: urls.recipes.plans.create({ id: currentHome.id }) })
    refetch()
    notifications.show({ message: 'Plan was successfully created', color: 'green' })
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-3">
        <Title weight={600}>Plans</Title>
      </div>
      <div className=" flex items-end justify-between space-x-4">
        <div className="w-full">
          <Form {...form} />
        </div>
        <Button onClick={onCreatePlan}>Create plan</Button>
      </div>
      <Table<RecipePlanItemRecord>
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

  const refetch = () => {
    plans.reload()
  }

  return (
    <View<object, PlansAppInnerProps>
      component={PlansAppInner}
      results={{ plans: plans }}
      componentProps={{ currentHome: currentHome, refetch: refetch }}
      loadingProps={{ description: 'Loading plans...' }}
      errorProps={{ description: 'There was an error getting plans.' }}
    />
  )
}

export default PlansApp
