import { IconMoodSad } from '@tabler/icons-react'
import PageState from '../PageState'
import React from 'react'

interface EmptyProps {
  title: string
  message: string
  className?: string
}

function Empty({ title, message, className }: EmptyProps) {
  return (
    <PageState
      title={title}
      message={message}
      className={className}
      icon={<IconMoodSad className="w-12 h-12 mx-auto" stroke={1.3} />}
    />
  )
}

export default Empty
