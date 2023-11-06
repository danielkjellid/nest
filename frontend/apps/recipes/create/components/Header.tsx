import { Stepper as MStepper, Title } from '@mantine/core'
import React from 'react'
import { useLocation } from 'react-router-dom'
import { useParams } from 'react-router-dom'

import { useCommonStyles } from '../../../../styles/common'
import { routes } from '../../routes'

interface StepperProps {
  loadingStep?: number
}

function Stepper({ loadingStep }: StepperProps) {
  const steps = [
    {
      step: 1,
      label: 'Create recipe',
      description: 'Add basic recipe information',
      path: routes.createRecipe.path,
      buildPath(_recipeId: string | number) {
        return routes.createRecipe.build()
      },
    },
    {
      step: 2,
      label: 'Add ingredients',
      description: 'Specify ingredients and amounts',
      path: routes.createRecipeIngredients.path,
      buildPath(recipeId: string | number) {
        return routes.createRecipeIngredients.build({ recipeId })
      },
    },
    {
      step: 3,
      label: 'Add steps',
      description: 'Add step and instructions',
      path: routes.createRecipeSteps.path,
      buildPath(recipeId: string | number) {
        return routes.createRecipeSteps.build({ recipeId })
      },
    },
  ]

  const location = useLocation()
  const { recipeId } = useParams()
  const currentStep = steps.find(
    (step) => step.buildPath(recipeId || '') === location.pathname.replace(/\/+$/, '')
  )

  return (
    <MStepper active={currentStep ? currentStep.step - 1 : 0}>
      {steps.map((step) => (
        <MStepper.Step
          key={step.step}
          label={step.label}
          description={step.description}
          loading={loadingStep === step.step}
        />
      ))}
    </MStepper>
  )
}

interface HeaderProps extends StepperProps {
  title: string
}

function Header({ title, loadingStep }: HeaderProps) {
  const { classes } = useCommonStyles()

  return (
    <div className="space-y-6">
      <Title weight={600} className={classes.title}>
        {title}
      </Title>
      <Stepper loadingStep={loadingStep} />
    </div>
  )
}

export { Header }
