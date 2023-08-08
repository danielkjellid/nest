import React from 'react'
import View from '../../../components/View'
import { OverviewHeader } from '../components/OverviewHeader'
import { Recipe } from '../../recipe/components/Recipe'

interface RecipeOverviewInnerProps {
  foo?: string
}

function RecipeOverviewInner() {
  return (
    <div className="space-y-6">
      <OverviewHeader title="Recipes" />
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
