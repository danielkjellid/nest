import { useMantineTheme } from '@mantine/core'
import cx from 'classnames'
import React from 'react'

import { useCommonStyles } from '../../../../../styles/common'

interface RecipeMeterColor {
  text: string
  border: string
  background: string
}

const getColors = (val: number, active: boolean): RecipeMeterColor => {
  const theme = useMantineTheme()

  if (active) {
    if (val >= 9)
      return { text: 'text-green-500', border: 'border-green-400', background: 'bg-green-400' }
    if (val >= 7)
      return { text: 'text-orange-500', border: 'border-orange-400', background: 'bg-orange-400' }
    if (val > 1 && val < 7)
      return { text: 'text-red-500', border: 'border-red-400', background: 'bg-red-400' }
  }

  if (theme.colorScheme === 'dark') {
    return {
      text: 'text-[#909296]',
      border: 'border-[#909296]',
      background: 'bg-[#909296]',
    }
  } else {
    return { text: 'text-gray-400', border: 'border-gray-200', background: 'bg-gray-200' }
  }
}

interface RecipeHealthScoreProps {
  value: number
}

function RecipeHealthScoreMeter({ value }: RecipeHealthScoreProps) {
  const { classes } = useCommonStyles()
  return (
    <div
      style={{ maxWidth: '220px' }}
      className={`relative p-2 border rounded-md ${classes.border}`}
    >
      <div className="grid grid-cols-2 gap-5">
        <div>
          <div className="space-y-px">
            <RecipeHealthScoreMeterSection
              label="High"
              range={[9, 10]}
              value={value}
              colors={getColors(value, value >= 9)}
            />
            <RecipeHealthScoreMeterSection
              label="Medium"
              range={[7, 8]}
              value={value}
              colors={getColors(value, value >= 7)}
            />
            <RecipeHealthScoreMeterSection
              label="Low"
              range={[1, 6]}
              value={value}
              colors={getColors(value, value > 1)}
            />
          </div>
        </div>
        <div className="flex items-center justify-center">
          <span className={`text-3xl font-bold ${getColors(value, true).text}`}>
            {value.toString()}
          </span>
          <span className={`text-xl font-semibold ${getColors(value, false).text}`}>/10</span>
        </div>
      </div>
    </div>
  )
}

interface RecipeHealthScoreMeterSectionProps {
  label: string
  range: number[]
  value: number
  colors: RecipeMeterColor
}

function RecipeHealthScoreMeterSection({
  label,
  range,
  colors,
  value,
}: RecipeHealthScoreMeterSectionProps) {
  const min = range[0]
  const max = range[1]

  const fullRange: number[] = Array.from({ length: max - min + 1 }, (_, i) => i + min)
  const flooredValue = Math.round(value)
  const theme = useMantineTheme()

  return (
    <div className="relative">
      <div className="pb-px space-y-px">
        {fullRange.reverse().map((r) => (
          <div
            key={r}
            className={cx(
              'w-5 h-1.5',
              r <= flooredValue
                ? colors.background
                : theme.colorScheme === 'dark'
                ? 'bg-[#909296]'
                : 'bg-gray-200'
            )}
          />
        ))}
      </div>
      <div className={`absolute bottom-0 w-full h-full border-b ${colors.border}`} />
      <span
        className={`absolute top-0 bottom-0 right-0 flex items-center text-xs font-medium leading-none ${colors.text}`}
      >
        {label}
      </span>
    </div>
  )
}

export { RecipeHealthScoreMeter }
