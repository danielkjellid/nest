import { IconCircleCheck, IconCircleX } from '@tabler/icons-react'
import { Button as MButton, ButtonProps as MButtonProps } from '@mantine/core'

import React from 'react'

export interface ButtonProps extends MButtonProps {
  loadingState?: 'initial' | 'loading' | 'error' | 'success'
  onClick?: () => void
  component?: any
}

function Button({ loadingState, onClick, component, ...props }: ButtonProps) {
  // We want to render the leftIcon based on loading state. Defaults to passed leftIcon
  // prop if present.
  const renderIcon = () => {
    if (loadingState === 'error') {
      return <IconCircleX />
    }

    if (loadingState === 'success') {
      return <IconCircleCheck />
    }

    return props.leftIcon
  }
  return (
    <MButton
      onClick={onClick}
      component={component}
      loading={loadingState === 'loading'}
      loaderProps={{ variant: 'oval' }}
      loaderPosition="left"
      leftIcon={renderIcon()}
      {...props}
    >
      {props.children}
    </MButton>
  )
}

Button.Group = MButton.Group

export { Button }
