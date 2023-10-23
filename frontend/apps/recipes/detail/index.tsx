import React from 'react'
import { useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { useFetch } from '../../../hooks/fetcher'
import { urls } from '../../urls'
import View from '../../../components/View'

function RecipeDetailInner() {}

function RecipeDetail() {
  const { recipeId } = useParams()
  invariant(recipeId)

  const recipeResponse = useFetch(urls.recipes.detail({ id: recipeId }))

  return <View<object, any> />
}
