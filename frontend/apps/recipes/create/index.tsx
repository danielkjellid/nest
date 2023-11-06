import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { Button } from '../../../components/Button'
import { Card } from '../../../components/Card'
import Form from '../../../components/Form'
import { useForm } from '../../../hooks/forms'
import { useCommonStyles } from '../../../styles/common'
import { RecipeCreateOutAPIResponse } from '../../../types'
import { urls } from '../../urls'
import { routes } from '../routes'

import { Header } from './components/Header'

function RecipeCreate() {
  const { classes } = useCommonStyles()
  const navigate = useNavigate()

  /**********
   ** Data **
   **********/

  const [loadingStep, setLoadingStep] = useState<number | undefined>()

  /**********
   ** Form **
   **********/

  const form = useForm({ key: 'RecipeCreateIn' })

  /**************
   ** Handlers **
   **************/

  const createRecipe = async () => {
    setLoadingStep(1)
    const response = await form.performPost<RecipeCreateOutAPIResponse>({
      url: urls.recipes.create(),
    })

    if (response && response.data) {
      const { recipeId } = response.data
      navigate(routes.createRecipeIngredients.build({ recipeId }))
    }
  }

  return (
    <div className="space-y-10">
      <Header title="Create new recipe" loadingStep={loadingStep} />
      <Card>
        <Card.Form
          title="Recipe information"
          subtitle="Add basic recipe information"
          form={<Form {...form} />}
        />
        <div className={`flex space-x-3 justify-end py-4 border-t ${classes.border}`}>
          <Button variant="default" onClick={() => navigate(-1)}>
            Cancel
          </Button>
          <Button onClick={() => createRecipe()}>Continue</Button>
        </div>
      </Card>
    </div>
  )
}

export { RecipeCreate }
