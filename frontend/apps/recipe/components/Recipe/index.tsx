import React from 'react'
import cx from 'classnames'
import { Tabs, Title, Text } from '@mantine/core'
import { RecipeHealthScoreMeter } from './HealthScore'
import { RecipeSteps } from './Steps'
import { RecipeSection } from './Section'
import { RecipeNutritionTable } from './Nutrition'
import { useCommonStyles } from '../../../../styles/common'
import { RecipeIngredientGroup } from './Ingredients'

function Recipe() {
  const { classes } = useCommonStyles()

  return (
    <div className={cx('max-w-7xl py-8 px-10 space-y-6 rounded-lg shadow', classes.panel)}>
      <div className="flex items-center justify-between px-3 py-4 border-b border-gray-200">
        <Title weight={600} className={classes.title}>
          Recipe name
        </Title>
        <Title weight={500} size={24} className={classes.subtitle}>
          - 4 portions +
        </Title>
      </div>
      <Tabs value="recipe">
        <Tabs.List>
          <Tabs.Tab value="recipe">Recipe</Tabs.Tab>
          <Tabs.Tab value="products">Products</Tabs.Tab>
        </Tabs.List>
      </Tabs>
      <div className="grid grid-cols-5 gap-6 px-3">
        <div className="col-span-1">
          <RecipeSection title="Ingredients">
            <RecipeIngredientGroup title="Pizzatoast">
              <RecipeIngredientGroup.Item title="tomater, røde" amount={200} unit="g" />
              <RecipeIngredientGroup.Item title="tomatersaus, ferdig" amount={3} unit="dl" />
              <RecipeIngredientGroup.Item title="pizzabunn, halvstekt" amount={4} unit="stk" />
              <RecipeIngredientGroup.Item title="parmaskinke" amount={100} unit="g" />
              <RecipeIngredientGroup.Item title="basilikum, fersk" amount={20} unit="g" />
              <RecipeIngredientGroup.Item title="mozzarella, fersk" amount={2} unit="stk" />
              <RecipeIngredientGroup.Item title="pepper, kvernet" amount={0.5} unit="ts" />
            </RecipeIngredientGroup>
            <RecipeIngredientGroup title="Tilbehør">
              <RecipeIngredientGroup.Item title="tomater, røde" amount={200} unit="g" />
              <RecipeIngredientGroup.Item title="ruccula" amount={70} unit="g" />
            </RecipeIngredientGroup>
          </RecipeSection>
        </div>
        <div className="col-span-3">
          <RecipeSection title="Steps">
            <RecipeSteps>
              <RecipeSteps.Item index={1} />
              <RecipeSteps.Item index={2} />
            </RecipeSteps>
          </RecipeSection>
        </div>
        <div className="space-y-6">
          <RecipeSection title="Price">
            <Title weight={500} size={24} className={classes.subtitle}>
              479,00 kr
            </Title>
          </RecipeSection>
          <RecipeSection title="Time">
            <p>TIME</p>
          </RecipeSection>
          <RecipeSection title="Health Score">
            <RecipeHealthScoreMeter value={5} />
          </RecipeSection>
          <RecipeSection title="Nutrition per serving">
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
          <div>
            <Text size="lg" weight={500}>
              Glycemic values
            </Text>
            <Text size="sm">400</Text>
          </div>
        </div>
      </div>
    </div>
  )
}

export { Recipe }
