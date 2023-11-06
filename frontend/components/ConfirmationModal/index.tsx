
import { Modal } from '@mantine/core'
import React from 'react'

import { Button, ButtonProps } from '../Button'

export interface ConfirmationModalButtonProps {
  label?: string
  color?: ButtonProps['color']
}

interface ConfirmationModalProps {
  title: string
  opened: boolean
  onConfirm: () => void
  onClose: () => void
  confirmButtonColor?: ButtonProps['color']
  confirmButtonText?: string
  children: React.ReactNode
  buttons: {
    confirm?: ConfirmationModalButtonProps
    cancel?: ConfirmationModalButtonProps
  }
}

function ConfirmationModal({
  title,
  opened,
  onConfirm,
  onClose,
  children,
  buttons,
}: ConfirmationModalProps) {
  return (
    <Modal opened={opened} title={title} onClose={onClose} size="md" centered>
      <div className="space-y-6">
        <div className="max-w-prose text-sm">{children}</div>
        <div className="flex w-full space-x-4">
          <Button
            fullWidth
            variant="default"
            color={(buttons.cancel && buttons.cancel.color) || undefined}
            onClick={onClose}
          >
            {(buttons.cancel && buttons.cancel.label) || 'Cancel'}
          </Button>
          <Button
            fullWidth
            variant="filled"
            color={(buttons.confirm && buttons.confirm.color) || 'red'}
            onClick={onConfirm}
          >
            {(buttons.confirm && buttons.confirm.label) || 'Confirm'}
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export { ConfirmationModal }
