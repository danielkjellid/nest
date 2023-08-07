import React, { useState } from 'react'
import { useCommonStyles } from '../../../../../styles/common'
import { IconInfoCircle } from '@tabler/icons-react'
import { ActionIcon, Modal } from '@mantine/core'

interface RecipeSectionProps {
  title: string
  children: React.ReactNode
  infoModalContent?: React.ReactNode
}

function RecipeSection({ title, children, infoModalContent }: RecipeSectionProps) {
  const [infoModalOpen, setInfoModalOpen] = useState<boolean>(false)
  const { classes } = useCommonStyles()
  return (
    <>
      <div className="flex flex-col space-y-3">
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
