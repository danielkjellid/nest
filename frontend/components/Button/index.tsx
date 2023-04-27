import { IconCircleCheck, IconCircleX } from '@tabler/icons-react'
import { Button as MButton, ButtonProps as MButtonProps } from '@mantine/core'

import React from 'react'

export interface ButtonProps extends MButtonProps {
  loadingState?: 'initial' | 'loading' | 'error' | 'success'
  onClick?: () => void
}

function Button({ loadingState, onClick, ...props }: ButtonProps) {
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
