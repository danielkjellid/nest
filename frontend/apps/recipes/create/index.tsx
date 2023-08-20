import React, { useState } from 'react'
import { Header } from './components/Header'
import { Card } from '../../../components/Card'
import { useForm } from '../../../hooks/forms'
import Form from '../../../components/Form'
import { Button } from '../../../components/Button'
import { useCommonStyles } from '../../../styles/common'
import { RecipeCreateOutAPIResponse } from '../../../types'
import { useNavigate } from 'react-router-dom'
import { routes } from '../routes'
import { urls } from '../../urls'

function RecipeCreate() {
  const [loadingStep, setLoadingStep] = useState<number | undefined>()
  const form = useForm({ key: 'RecipeCreateIn' })

  const navigate = useNavigate()
  const { classes } = useCommonStyles()

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
