import { ActionIcon, Modal } from '@mantine/core'
import { IconInfoCircle } from '@tabler/icons-react'
import React, { useState } from 'react'

import { useCommonStyles } from '../../../../../styles/common'

interface RecipeSectionProps {
  title: string
  children: React.ReactNode
  infoModalContent?: React.ReactNode
  className?: string
}

function RecipeSection({ title, children, infoModalContent, className }: RecipeSectionProps) {
  const [infoModalOpen, setInfoModalOpen] = useState<boolean>(false)
  const { classes } = useCommonStyles()
  return (
    <>
      <div className={`${className} flex flex-col w-full space-y-3`}>
        <div className="flex items-center justify-between">
          <h2 className={`${classes.subtitle} font-medium`}>{title}</h2>
          {infoModalContent && (
            <ActionIcon onClick={() => setInfoModalOpen(true)}>
              <IconInfoCircle className={classes.icon} />
            </ActionIcon>
          )}
        </div>
        {children}
        {infoModalContent && (
          <Modal
            opened={infoModalOpen}
            onClose={() => setInfoModalOpen(false)}
            size="md"
            title={title}
          >
            {infoModalContent}
          </Modal>
        )}
      </div>
    </>
  )
}

export { RecipeSection }
