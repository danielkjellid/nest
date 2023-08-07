import React, { useState } from 'react'
import cx from 'classnames'
import { Tabs, Title, Text, ActionIcon, useMantineTheme } from '@mantine/core'
import { RecipeHealthScoreMeter } from './HealthScore'
import { RecipeSteps } from './Steps'
import { RecipeSection } from './Section'
import { RecipeNutritionTable } from './Nutrition'
import { useCommonStyles } from '../../../../styles/common'
import { RecipeIngredientGroup } from './Ingredients'
import { IconClock, IconCoin, IconMinus, IconPlus } from '@tabler/icons-react'

function Recipe() {
  const theme = useMantineTheme()
  const { classes } = useCommonStyles()

  const defaultNumPortions = 4
  const [portions, setPortions] = useState<number>(defaultNumPortions)

  return (
    <div className={cx('max-w-7xl py-8 px-10 space-y-6 rounded-lg shadow', classes.panel)}>
      <div className="flex items-center justify-between px-3 py-4 border-b border-gray-200">
        <Title weight={600} className={classes.title}>
          Recipe name
        </Title>
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
      {/* <Tabs value="recipe">
        <Tabs.List>
          <Tabs.Tab value="recipe">Recipe</Tabs.Tab>
          <Tabs.Tab value="products">Products</Tabs.Tab>
        </Tabs.List>
      </Tabs> */}
      <div className="lg:grid-cols-3 xl:grid-cols-5 grid grid-cols-1 gap-6">
        <div className="xl:row-span-2 order-1 col-span-1">
          <RecipeSection title="Ingredients">
            <RecipeIngredientGroup title="Pizzatoast">
              <RecipeIngredientGroup.Item
                basePortions={defaultNumPortions}
                portions={portions}
                title="tomater, røde"
                amount={200}
                unit="g"
              />
              <RecipeIngredientGroup.Item
                basePortions={defaultNumPortions}
                portions={portions}
                title="tomatersaus, ferdig"
                amount={3}
                unit="dl"
              />
              <RecipeIngredientGroup.Item
                basePortions={defaultNumPortions}
                portions={portions}
                title="pizzabunn, halvstekt"
                amount={4}
                unit="stk"
              />
              <RecipeIngredientGroup.Item
                basePortions={defaultNumPortions}
                portions={portions}
                title="parmaskinke"
                amount={100}
                unit="g"
              />
              <RecipeIngredientGroup.Item
                basePortions={defaultNumPortions}
                portions={portions}
                title="basilikum, fersk"
                amount={20}
                unit="g"
              />
              <RecipeIngredientGroup.Item
                basePortions={defaultNumPortions}
                portions={portions}
                title="mozzarella, fersk"
                amount={2}
                unit="stk"
              />
              <RecipeIngredientGroup.Item
                basePortions={defaultNumPortions}
                portions={portions}
                title="pepper, kvernet"
                amount={0.5}
                unit="ts"
              />
            </RecipeIngredientGroup>
            <RecipeIngredientGroup title="Tilbehør">
              <RecipeIngredientGroup.Item
                basePortions={defaultNumPortions}
                portions={portions}
                title="tomater, røde"
                amount={200}
                unit="g"
              />
              <RecipeIngredientGroup.Item
                basePortions={defaultNumPortions}
                portions={portions}
                title="ruccula"
                amount={70}
                unit="g"
              />
            </RecipeIngredientGroup>
          </RecipeSection>
        </div>
        <div className="lg:col-span-2 xl:col-span-3 xl:row-span-2 order-2 col-span-1">
          <RecipeSection title="Steps">
            <RecipeSteps>
              <RecipeSteps.Item index={1} />
              <RecipeSteps.Item index={2} />
              <RecipeSteps.Item index={3} />
              <RecipeSteps.Item index={4} />
              <RecipeSteps.Item index={5} />
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
                  <Title
                    weight={500}
                    size={24}
                    className={`${classes.subtitle} flex items-center space-x-2 -mt-1`}
                  >
                    15 min
                    <span className={`${classes.muted} text-sm ml-1.5`}>(5 min prep)</span>
                  </Title>
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
