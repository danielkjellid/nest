import React, { useState } from 'react'

import cx from 'classnames'
import { useStepsStyles } from './Steps.styles'

interface RecipeStepsProps {
  children: React.ReactNode
}

function RecipeSteps({ children }: RecipeStepsProps) {
  return <div className="max-w-prose space-y-2">{children}</div>
}

interface RecipeStepItemProps {
  index: number
}

function RecipeStepItem({ index }: RecipeStepItemProps) {
  const { classes } = useStepsStyles()
  const [completed, setCompleted] = useState<boolean>(false)

  return (
    <div
      className={`${classes.stepsCard} flex items-start p-4 space-x-4 rounded-md appearance-none cursor-pointer`}
      onClick={() => setCompleted(!completed)}
    >
      <div
        className={`flex items-center justify-center flex-none w-8 h-8 ${classes.stepCircle} rounded-full`}
      >
        {index}
      </div>
      <p className={cx('text-sm', { 'line-through': completed })}>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam aliquet diam nec pretium
        ultricies. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nulla vel leo et
        libero ultrices commodo. Suspendisse eu scelerisque lectus, eu hendrerit elit. Morbi vitae
        metus eget tellus tincidunt mollis ac vel tellus.
      </p>
    </div>
  )
}

RecipeSteps.Item = RecipeStepItem

export { RecipeSteps }
