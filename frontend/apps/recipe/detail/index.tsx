import { Badge, Button as MButton } from '@mantine/core'
import { useNavigate, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'

import { Button } from '../../../components/Button'
import View from '../../../components/View'
import { useCommonContext } from '../../../contexts/CommonProvider'
import { useFetch } from '../../../hooks/fetcher'
import { type RecipeDetailOutAPIResponse, RecipeStatus } from '../../../types'
import { urls } from '../../urls'
import { Recipe } from '../components/Recipe'

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

  const getRecipeBadge = (status: RecipeStatus) => {
    const badges: Record<RecipeStatus, React.ReactNode> = {
      draft: (
        <Badge size="lg" radius="sm" color="blue" variant="dot">
          Draft
        </Badge>
      ),
      published: (
        <Badge size="lg" radius="sm" color="green" variant="dot">
          Published
        </Badge>
      ),
    }

    return badges[status]
  }

  return (
    <div className="flex flex-col space-y-6">
      {currentUser && currentUser.isStaff && (
        <div className=" flex items-center justify-between">
          {getRecipeBadge(recipe.status)}
          <div className="flex items-center space-x-3">
            {currentUser.isSuperuser && (
              <MButton
                component="a"
                href={`/admin/recipes/recipe/${recipe.id}/`}
                target="_blank"
                variant="default"
              >
                View in admin
              </MButton>
            )}
            <Button onClick={() => navigate('/')}>Edit recipe</Button>
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
