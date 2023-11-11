import { Title } from '@mantine/core'

import { Card } from '../../../components/Card'
import View from '../../../components/View'
import { useCommonStyles } from '../../../styles/common'
import { useState } from 'react'
import Form from '../../../components/Form'
import { useForm } from '../../../hooks/forms'

function RecipeForm() {
  const form = useForm({ key: 'RecipeCreateForm' })
  return <Form {...form} />
}

function RecipeCreateInner() {
  const { classes } = useCommonStyles()
  return (
    <div className="space-y-10">
      <Title weight={600} className={classes.title}>
        Create new recipe
      </Title>
      <Card>
        <Card.Form
          title="Recipe information"
          subtitle="Add basic recipe information"
          form={<RecipeForm />}
        />
        <Card.Form
          title="Add ingredients"
          subtitle="Add ingredients and amounts to recipe. If one ingredient is needed within multiple groups, add it to each group respectively."
          form={<></>}
        />
        <Card.Form title="Add steps" subtitle="Add steps to recipe" form={<></>} />
      </Card>
    </div>
  )
}

function RecipeCreate() {
  return (
    <View<object, any>
      component={RecipeCreateInner}
      componentProps={{}}
      results={{}}
      loadingProps={{ description: 'Loading recipe form' }}
      errorProps={{ description: 'There was an error retrieving data.' }}
    />
  )
}

export { RecipeCreate }
