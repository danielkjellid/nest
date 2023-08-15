import React, { useState } from 'react'
import {
  Modal,
  Input,
  TextInput,
  UnstyledButton,
  Highlight,
  Text,
  createStyles,
} from '@mantine/core'
import { IconSearch } from '@tabler/icons-react'
import { useCommonStyles } from '../../../../styles/common'
import { RecipeListOut } from '../../../../types'

const useRecipeSearchModalStyles = createStyles((theme) => ({
  action: {
    '&:hover': { backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[5] : '#f9fafb' },
  },
}))

interface RecipeSearchModalProps {
  opened: boolean
  recipes: RecipeListOut[]
  onClose: () => void
  onRecipeSelect: (recipe: RecipeListOut) => void
}

function RecipeSearchModal({ opened, recipes, onClose }: RecipeSearchModalProps) {
  const { classes } = useCommonStyles()
  const { classes: modalClasses } = useRecipeSearchModalStyles()
  const [query, setQuery] = useState('')
  return (
    <Modal
      opened={opened}
      onClose={onClose}
      size="xl"
      padding={0}
      radius="md"
      className="relative overflow-hidden"
      withCloseButton={false}
    >
      <div className={`border-b ${classes.border}`}>
        <TextInput
          size="xl"
          icon={<IconSearch />}
          classNames={{ input: 'border-0' }}
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => setQuery(event.target.value)}
        />
      </div>
      <div className="p-2">
        {recipes.map((recipe) => (
          <UnstyledButton
            key={recipe.id}
            className={`relative block w-full px-6 py-3 rounded-md ${modalClasses.action}`}
          >
            <div>
              <Highlight highlight={query}>{recipe.title}</Highlight>
              <Text size="xs">{recipe.defaultNumPortions}</Text>
            </div>
          </UnstyledButton>
        ))}
      </div>
    </Modal>
  )
}

export { RecipeSearchModal }
