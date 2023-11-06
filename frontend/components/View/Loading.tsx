import { Loader, LoadingOverlay, Text } from '@mantine/core'
import React from 'react'

export interface LoadingProps {
  description?: string
}

function Loading({ description }: LoadingProps) {
  return (
    <LoadingOverlay
      visible
      loader={
        <div className="text-center space-y-3">
          <Loader size="lg" className="mx-auto" />
          {description && <Text fz="md">{description}</Text>}
        </div>
      }
    />
  )
}

export default Loading
