import {
  CommonContextType,
  CommonProvider,
  useCommonContext,
} from '../../../contexts/CommonProvider'
import React, { useState } from 'react'

import BaseApp from '../../../components/BaseApp/BaseApp'
import Header from '../../../components/Header'
import { Recipe } from '../components/Recipe'
import { Button } from '../../../components/Button'
import { Button as MButton } from '@mantine/core'
import { useFetcher, useNavigate, useParams } from 'react-router-dom'
import View from '../../../components/View'
import { RecipeDetailOut, RecipeDetailOutAPIResponse, RecipeStatus } from '../../../types'
import { urls } from '../../urls'
import invariant from 'tiny-invariant'
import { useFetch } from '../../../hooks/fetcher'

interface RecipeDetailInnerProps {
  results: {
    recipeResponse: RecipeDetailOutAPIResponse
  }
}

function RecipeDetailInner({ results }: RecipeDetailInnerProps) {
  const navigate = useNavigate()
  const { currentUser } = useCommonContext()
  const { data: recipe } = results.recipeResponse

  if (!recipe) return null

  if ((recipe.status !== RecipeStatus.Published && !currentUser) || !currentUser?.isStaff) {
    navigate('/')
  }

  return (
    <div className="flex flex-col space-y-6">
      {currentUser && currentUser.isStaff && (
        <div className=" flex items-center justify-between">
          <div>Published</div>
          <div className="flex items-center space-x-3">
            {currentUser.isSuperuser && (
              <MButton
                component="a"
                href={'/admin/products/product/'}
                target="_blank"
                variant="default"
              >
                View in admin
              </MButton>
            )}
            <Button>Edit recipe</Button>
          </div>
        </div>
      )}
      <Recipe recipe={recipe} />
    </div>
  )
}

function RecipeDetail() {
  const { recipeId } = useParams()
  invariant(recipeId)

  const recipeResponse = useFetch<RecipeDetailOutAPIResponse>(urls.recipes.detail({ id: recipeId }))

  return (
    <View<object, RecipeDetailInnerProps>
      component={RecipeDetailInner}
      results={{ recipeResponse }}
      componentProps={{}}
      loadingProps={{ description: 'Loading recipe' }}
      errorProps={{
        description: 'There was an error retrieving the recipe. Please try again later.',
      }}
    />
  )
}

export { RecipeDetail }
