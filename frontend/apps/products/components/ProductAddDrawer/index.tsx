import { Drawer } from '@mantine/core'
import React from 'react'

interface ProductAddDrawerProps {
  opened: boolean
  children?: React.ReactNode
  onClose: () => void
}

function ProductAddDrawer({ opened, onClose, children }: ProductAddDrawerProps) {
  return (
    <Drawer opened={opened} onClose={onClose} title="Add new product" position="right">
      {children}
    </Drawer>
  )
}

export default ProductAddDrawer
