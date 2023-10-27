import { ActionIcon, Badge, Tabs, Text, Title, useMantineTheme } from '@mantine/core'
import { IconClock, IconCoin, IconMinus, IconPlus } from '@tabler/icons-react'
import React, { useState } from 'react'

import { Duration } from 'luxon'
import { RecipeDetailOut } from '../../../../types'
import { RecipeHealthScoreMeter } from './HealthScore'
import { RecipeIngredientGroup } from './Ingredients'
import { RecipeNutritionTable } from './Nutrition'
import { RecipeSection } from './Section'
import { RecipeSteps } from './Steps'
import cx from 'classnames'
import { useCommonStyles } from '../../../../styles/common'

interface RecipeProps {
  recipe: RecipeDetailOut
}

function Recipe({ recipe }: RecipeProps) {
  const theme = useMantineTheme()
  const { classes } = useCommonStyles()

  const defaultNumPortions = 4
  const [portions, setPortions] = useState<number>(recipe.defaultNumPortions)

  const formatDuration = (duration: string) =>
    Duration.fromISO(duration).toHuman({
      unitDisplay: 'short',
    })

  const totalTime = formatDuration(recipe.duration.totalTimeIso8601)
  const cookTime = formatDuration(recipe.duration.totalTimeIso8601)
  const prepTime = formatDuration(recipe.duration.preparationTimeIso8601)

  return (
    <div className={cx('max-w-7xl py-8 space-y-6 rounded-lg shadow', classes.panel)}>
      <div className="flex items-center justify-between px-12 pt-4">
        <div>
          <Title weight={600} className={classes.title}>
            {recipe.title}
          </Title>
          <div className="w-96 space-3 flex flex-wrap mt-4">
            <Badge className="mb-2 mr-2" color="gray">
              Easy
            </Badge>
            <Badge className="mb-2 mr-2" color="gray">
              Under 30 minutes
            </Badge>
            <Badge className="mb-2 mr-2" color="gray">
              Delicious
            </Badge>
            <Badge className="mb-2 mr-2" color="gray">
              Spicy
            </Badge>
            <Badge className="mb-2 mr-2" color="gray">
              Makes leftovers
            </Badge>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <ActionIcon
            color={theme.primaryColor}
            disabled={portions <= 1}
            onClick={() => {
              if (portions > 1) {
                setPortions(portions - 1)
              }
            }}
          >
            <IconMinus />
          </ActionIcon>
          <Title weight={500} size={24} className={`${classes.subtitle} w-36 text-center`}>
            {portions} {portions > 1 ? 'portions' : 'portion'}
          </Title>
          <ActionIcon
            color={theme.primaryColor}
            disabled={portions >= 99}
            onClick={() => {
              if (portions < 99) {
                setPortions(portions + 1)
              }
            }}
          >
            <IconPlus />
          </ActionIcon>
        </div>
      </div>
      <Tabs value="recipe" className="px-8">
        <Tabs.List>
          <Tabs.Tab value="recipe">Recipe</Tabs.Tab>
          <Tabs.Tab value="products" disabled>
            Products
          </Tabs.Tab>
        </Tabs.List>
      </Tabs>
      <div className="lg:grid-cols-3 xl:grid-cols-5 grid grid-cols-1 gap-6 px-12">
        <div className="xl:row-span-2 order-1 col-span-1">
          <RecipeSection title="Ingredients">
            {recipe.ingredientGroups.map((group) => (
              <RecipeIngredientGroup key={group.id} title={group.title}>
                {group.ingredientItems.map((item) => (
                  <RecipeIngredientGroup.Item
                    key={item.id}
                    basePortions={defaultNumPortions}
                    portions={portions}
                    title={item.ingredient.title}
                    amount={item.portionQuantity}
                    unit={item.portionQuantityUnit.abbreviation}
                  />
                ))}
              </RecipeIngredientGroup>
            ))}
          </RecipeSection>
        </div>
        <div className="lg:col-span-2 xl:col-span-3 xl:row-span-2 order-2 col-span-1">
          <RecipeSection title="Steps">
            <RecipeSteps>
              {recipe.steps.map((step) => (
                <RecipeSteps.Item
                  key={step.id}
                  number={step.number}
                  instruction={step.instruction}
                />
              ))}
            </RecipeSteps>
          </RecipeSection>
        </div>
        <div
          className={`lg:grid-cols-3 lg:col-span-3 xl:col-span-1 xl:grid-cols-1 grid order-3 grid-cols-1 gap-6 pt-8 xl:pt-0 xl:border-none border-t ${classes.border}`}
        >
          <div className="col-span-1">
            <RecipeSection title="Time">
              <div className="flex items-start space-x-2">
                <IconClock className={classes.icon} />
                <div>
                  <Title weight={500} size={24} className={`${classes.subtitle} -mt-1`}>
                    {totalTime}
                  </Title>
                  <div className="mt-1">
                    <span className={`${classes.muted} text-sm block`}>{cookTime} cook</span>
                    <span className={`${classes.muted} text-sm block`}>{prepTime} prep</span>
                  </div>
                </div>
              </div>
            </RecipeSection>
          </div>
          <div className="col-span-1">
            <RecipeSection title="Price">
              <div className="flex items-start space-x-2">
                <IconCoin className={classes.icon} />
                <Title
                  weight={500}
                  size={24}
                  className={`${classes.subtitle} flex items-center space-x-2 -mt-1`}
                >
                  479,00 kr
                </Title>
              </div>
            </RecipeSection>
          </div>
          <div className="col-span-1">
            <RecipeSection title="Health Score">
              <RecipeHealthScoreMeter value={9} />
            </RecipeSection>
          </div>
        </div>
        <div className="lg:col-span-3 xl:col-span-1 xl:col-start-5 order-4 col-span-1">
          <RecipeSection title="Nutrition per serving" className="xl:col-span-1 col-span-3">
            <RecipeNutritionTable
              nutrition={[
                {
                  key: 'calories',
                  title: 'Calories',
                  value: '370.8',
                  unit: 'kcal',
                  percentageOfDailyValue: '19',
                },
                {
                  key: 'total-fat',
                  title: 'Total fat',
                  value: '27.94',
                  unit: 'g',
                  percentageOfDailyValue: '40',
                },
                {
                  key: 'carbs',
                  title: 'Carbs',
                  value: '6.59',
                  unit: 'g',
                  percentageOfDailyValue: '3',
                },
                {
                  key: 'sugars',
                  title: 'Sugars',
                  value: '2.35',
                  unit: 'g',
                  percentageOfDailyValue: '3',
                },
                {
                  key: 'protein',
                  title: 'Protein',
                  value: '23.97',
                  unit: 'g',
                  percentageOfDailyValue: '48',
                },
                {
                  key: 'sodium',
                  title: 'Sodium',
                  value: '428.9',
                  unit: 'mg',
                  percentageOfDailyValue: '21',
                },
                {
                  key: 'fiber',
                  title: 'Fiber',
                  value: '1.64',
                  unit: 'g',
                  percentageOfDailyValue: '6',
                },
              ]}
            />
            <Text size="sm" className={classes.muted}>
              Percentage of daily values are based on a 2000 calories diet.
            </Text>
          </RecipeSection>
        </div>
      </div>
    </div>
  )
}

export { Recipe }
