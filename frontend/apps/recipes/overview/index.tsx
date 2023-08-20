import React from 'react'
import View from '../../../components/View'
import { OverviewHeader } from '../components/OverviewHeader'
import { Recipe } from '../../recipe/components/Recipe'
import { useCommonContext } from '../../../contexts/CommonProvider'
import { Button } from '../../../components/Button'
import { useNavigate } from 'react-router-dom'
import { routes } from '../routes'

interface RecipeOverviewInnerProps {
  foo?: string
}

function RecipeOverviewInner() {
  const { currentUser } = useCommonContext()
  const navigate = useNavigate()

  return (
    <div className="space-y-6">
      <OverviewHeader
        title="Recipes"
        actions={
          currentUser &&
          currentUser.isStaff && (
            <div className="flex.items-center.space-x-3">
              <Button.Group>
                <Button variant="default" onClick={() => navigate(routes.createRecipe.build())}>
                  Add new
                </Button>
              </Button.Group>
            </div>
          )
        }
      />
      <Recipe />
    </div>
  )
}

function RecipeOverview() {
  return (
    <View<object, RecipeOverviewInnerProps>
      component={RecipeOverviewInner}
      results={{}}
      componentProps={{}}
      loadingProps={{ description: 'Loading recipes' }}
      errorProps={{ description: 'There was an error getting recipes. Please try again.' }}
    />
  )
}

export { RecipeOverview }
