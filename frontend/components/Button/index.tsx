import { Button as MButton, ButtonProps as MButtonProps } from '@mantine/core'
import { IconCircleCheck, IconCircleX } from '@tabler/icons-react'
import React from 'react'

import { useCommonStyles } from '../../styles/common'

export interface ButtonProps extends MButtonProps {
  loadingState?: 'initial' | 'loading' | 'error' | 'success'
  onClick?: () => void
}

function Button({ loadingState, onClick, ...props }: ButtonProps) {
  const { classes } = useCommonStyles()
  // We want to render the leftIcon based on loading state. Defaults to passed leftIcon
  // prop if present.
  const renderIcon = () => {
    if (loadingState === 'error') {
      if (props.variant === 'default') return <IconCircleX className={classes.iconDanger} />
      return <IconCircleX color="white" />
    }

    if (loadingState === 'success') {
      if (props.variant === 'default') return <IconCircleCheck className={classes.iconSuccess} />
      return <IconCircleCheck color="white" />
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
