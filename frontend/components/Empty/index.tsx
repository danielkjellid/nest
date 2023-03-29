import { Text, Title, createStyles } from '@mantine/core'

import { IconMoodSad } from '@tabler/icons-react'
import PageState from '../PageState'
import React from 'react'

interface EmptyProps {
  title: string
  message: string
}

function Empty({ title, message }: EmptyProps) {
  return (
    <PageState
      title={title}
      message={message}
      icon={<IconMoodSad className="h-12 w-12" stroke={1.3} />}
    />
  )
}

export default Empty
