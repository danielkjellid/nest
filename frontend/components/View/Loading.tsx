import React from 'react'

export interface LoadingProps {
  description?: string
  inline?: boolean
}

function Loading({ description }: LoadingProps) {
  return <p>Loading</p>
}

export default Loading
