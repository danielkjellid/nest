import { createStyles } from '@mantine/core'

export const useStepsStyles = createStyles((theme) => ({
  stepsCard: {
    '&:hover': { backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[5] : '#f9fafb' },
  },
  stepCircle: {
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : '#e5e7eb',
    color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7],
  },
}))
