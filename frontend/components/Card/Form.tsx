import React from 'react'
import { useCommonStyles } from '../../styles/common'

interface CardFormRowProps {
  title: string
  subtitle: string
  form: React.ReactNode
}

function CardFormRow({ title, subtitle, form }: CardFormRowProps) {
  const { classes } = useCommonStyles()
  return (
    <div
      className={`${classes.border} gap-x-8 gap-y-10 md:grid-cols-3 grid grid-cols-1 py-6 pb-12 border-b border-gray-200`}
    >
      <div>
        <h2 className="text-base font-semibold leading-7 text-gray-900">{title}</h2>
        <p className="mt-1 text-sm leading-6 text-gray-600">{subtitle}</p>
      </div>
      <div className="md:col-span-2">{form}</div>
    </div>
  )
}

interface CardFormProps {
  title: string
  subtitle: string
  form: React.ReactNode
}

function CardForm({ title, subtitle, form }: CardFormProps) {
  const { classes } = useCommonStyles()

  return (
    <div className={`gap-x-8 gap-y-10 md:grid-cols-3 grid grid-cols-1 ${classes.border} py-6`}>
      <div>
        <h2 className={`text-base font-semibold leading-7 ${classes.title} `}>{title}</h2>
        <p className={`mt-1 text-sm leading-6 ${classes.subtitle}`}>{subtitle}</p>
      </div>
      <div className="md:col-span-2">{form}</div>
    </div>
  )
}

export { CardForm, CardFormRow }
