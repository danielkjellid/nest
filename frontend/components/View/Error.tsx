import { IconHeartBroken } from '@tabler/icons-react'
import PageState from '../PageState'
import React from 'react'

export interface ErrorProps {
  description: string
}

function Error({ description }: ErrorProps) {
  return (
    <PageState
      title="Something went wrong"
      message={description}
      icon={<IconHeartBroken className="h-12 w-12" stroke={1.3} />}
    />
  )
}

export default Error
