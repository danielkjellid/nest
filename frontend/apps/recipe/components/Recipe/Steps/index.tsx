import cx from 'classnames'
import { useState, type ReactNode } from 'react'

import { useStepsStyles } from './Steps.styles'

interface RecipeStepsProps {
  children: ReactNode
}

function RecipeSteps({ children }: RecipeStepsProps) {
  return <div className="max-w-prose space-y-2">{children}</div>
}

interface RecipeStepItemProps {
  number: number
  instruction: string
}

function RecipeStepItem({ number, instruction }: RecipeStepItemProps) {
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
        {number}
      </div>
      <p className={cx('text-sm', { 'line-through': completed })}>{instruction}</p>
    </div>
  )
}

RecipeSteps.Item = RecipeStepItem

export { RecipeSteps }
