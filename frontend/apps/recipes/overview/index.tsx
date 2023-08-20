import React from 'react'
import View from '../../../components/View'
import { Recipe } from '../../recipe/components/Recipe'
import { useCommonContext } from '../../../contexts/CommonProvider'
import { Button } from '../../../components/Button'
import { useNavigate } from 'react-router-dom'
import { routes } from '../routes'
import { Title } from '@mantine/core'

interface RecipeOverviewInnerProps {
  foo?: string
}

function RecipeOverviewInner() {
  const { currentUser } = useCommonContext()
  const navigate = useNavigate()

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
