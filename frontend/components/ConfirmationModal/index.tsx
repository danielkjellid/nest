import React from 'react'
import { Modal } from '@mantine/core'
import { Button, ButtonProps } from '../Button'

interface ConfirmationModalProps {
  title: string
  opened: boolean
  onConfirm: () => void
  onClose: () => void
  confirmButtonColor?: ButtonProps['color']
  confirmButtonText?: string
  children: React.ReactNode
}

function ConfirmationModal({
  title,
  opened,
  onConfirm,
  onClose,
  children,
  confirmButtonText,
  confirmButtonColor,
}: ConfirmationModalProps) {
  return (
    <Modal opened={opened} title={title} onClose={onClose} size="md" centered>
      <div className="space-y-6">
        <div className="max-w-prose text-sm">{children}</div>
        <div className="flex w-full space-x-4">
          <Button fullWidth variant="default">
            Cancel
          </Button>
          <Button
            fullWidth
            variant="filled"
            color={confirmButtonColor || 'red'}
            onClick={onConfirm}
          >
            {confirmButtonText || 'Confirm'}
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export { ConfirmationModal }
