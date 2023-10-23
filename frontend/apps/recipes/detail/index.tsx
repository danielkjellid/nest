import React from 'react'
import { useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { useFetch } from '../../../hooks/fetcher'
import { urls } from '../../urls'
import View from '../../../components/View'
import { RecipeDetailOutAPIResponse } from '../../../types'
import { Card } from '../../../components/Card'
import { TableOfContents } from '../../../components/TableOfContents'
import { Badge } from '@mantine/core'
import { RecipeIngredientGroup } from '../../recipe/components/Recipe/Ingredients'

interface RecipeDetailInnerProps {
  results: { recipeResponse: RecipeDetailOutAPIResponse }
}

function RecipeDetailInner({ results }: RecipeDetailInnerProps) {
  const { data: recipe } = results.recipeResponse

  if (!recipe) return null

  return (
    <div>
      <header className="lg:grid-cols-2 grid content-center grid-cols-1 gap-8">
        <div className="lg:order-1 text-ellipsis flex items-center self-center order-2 space-x-6">
          <div className="overflow-hidden">
            <div className=" max-w-full text-lg font-semibold leading-6 truncate">
              {recipe.title}
            </div>
            <div className="mt-1 text-sm">TAGS</div>
          </div>
        </div>
        <div className="lg:order-2 justify-self-start lg:justify-self-end self-center order-1 space-x-1">
          <p>Actions</p>
        </div>
      </header>
      <div className="lg:grid-cols-3 grid grid-cols-1 gap-6 mt-10">
        <div className="lg:order-1 lg:col-span-2 order-2 col-span-1 space-y-4">
          <div id="information">
            <Card title="Information">
              <Card.KeyValue k="Name" value={recipe.title} />
              <Card.KeyValue k="Slug" value={recipe.slug} />
              <Card.KeyValue k="Default portions" value={recipe.defaultNumPortions} />
              {recipe.externalId && <Card.KeyValue k="External id" value={recipe.externalId} />}
              {recipe.externalUrl && <Card.KeyValue k="External id" value={recipe.externalUrl} />}
              <Card.KeyValue k="Status" value={recipe.statusDisplay} />
              <Card.KeyValue k="Difficulty" value={recipe.difficultyDisplay} />
              <Card.KeyValue k="Vegetarian" value={recipe.isVegetarian} />
              <Card.KeyValue k="Pescatarian" value={recipe.isPescatarian} />
            </Card>
          </div>
          <div id="ingredients">
            <Card title="Ingredients">
              {recipe.ingredientGroups.map((group) => (
                <Card.KeyValue
                  key={group.id}
                  k={group.title}
                  value={
                    <RecipeIngredientGroup title={''}>
                      {group.ingredientItems.map((item) => (
                        <RecipeIngredientGroup.Item
                          key={item.id}
                          title={item.ingredient.title}
                          amount={item.portionQuantity}
                          unit={item.portionQuantityUnit.abbreviation}
                          basePortions={recipe.defaultNumPortions}
                          portions={recipe.defaultNumPortions}
                        />
                      ))}
                    </RecipeIngredientGroup>
                  }
                />
              ))}
            </Card>
          </div>
          <div id="steps">
            <Card title="Steps">
              {recipe.steps.map((step) => (
                <Card.KeyValue
                  key={step.id}
                  k={`Step ${step.number}`}
                  value={
                    <div className="flex flex-col space-y-px">
                      <span>{step.instruction}</span>
                      <div className="w-96 flex flex-wrap mt-2">
                        {step.ingredientItems.map((item) => (
                          <Badge key={item.id}>
                            {item.ingredient.title}, {item.portionQuantityDisplay}{' '}
                            {item.portionQuantityUnit.abbreviation}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  }
                />
              ))}
            </Card>
          </div>
        </div>
        <div className="lg:order-2 order-1 col-span-1 space-y-8">
          <TableOfContents
            headings={[
              { label: 'Information', slug: 'information' },
              { label: 'Ingredients', slug: 'ingredients' },
              { label: 'Steps', slug: 'steps' },
            ]}
          />
        </div>
      </div>
    </div>
  )
}

function RecipeDetail() {
  const { recipeId } = useParams()
  invariant(recipeId)

  const recipeResponse = useFetch(urls.recipes.detail({ id: recipeId }))

  return (
    <View<object, any>
      component={RecipeDetailInner}
      results={{ recipeResponse }}
      componentProps={{}}
      loadingProps={{ description: 'Loading recipe' }}
      errorProps={{
        description: 'There was an error retrieving the recipe. Please try again later. ',
      }}
    />
  )
}

export { RecipeDetail }
