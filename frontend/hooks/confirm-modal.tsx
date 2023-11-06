import { useDisclosure } from '@mantine/hooks'
import React, { useState } from 'react'

import {
  ConfirmationModal,
  type ConfirmationModalButtonProps,
} from '../components/ConfirmationModal'


interface ModalState {
  title: string
  children: React.ReactNode
  buttons: {
    confirm: ConfirmationModalButtonProps
    cancel: ConfirmationModalButtonProps
  }
  onConfirm: (id: any) => void
}

const useConfirmModal = ({ title, children, buttons, onConfirm }: ModalState) => {
  const [id, setId] = useState<string | number | undefined>(undefined)
  const [modalOpen, { open: openModal, close: closeModal }] = useDisclosure()

  const onOpen = (id: string | number) => {
    setId(id)
    openModal()
  }

  const onClose = () => {
    setId(undefined)
    closeModal()
  }

  return {
    open: (id: any) => onOpen(id),
    close: onClose,
    render: () => (
      <ConfirmationModal
        opened={modalOpen}
        onClose={onClose}
        title={title}
        onConfirm={() => onConfirm(id)}
        buttons={buttons}
      >
        {children}
      </ConfirmationModal>
    ),
  }
}

export { useConfirmModal }
