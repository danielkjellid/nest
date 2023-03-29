import React from 'react'

export interface ErrorProps {
  description?: string
  inline?: boolean
}

function Error({ description }: ErrorProps) {
  return <p>Error</p>
}

export default Error
