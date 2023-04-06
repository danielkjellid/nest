/* eslint-disable react/prop-types */
import { IconCircleCheckFilled, IconCircleXFilled } from '@tabler/icons-react'
import {
  MRT_ColumnDef,
  MRT_RowSelectionState,
  MantineReactTable,
  MantineReactTableProps,
} from 'mantine-react-table'
import React, { useEffect, useMemo, useState } from 'react'

import { Box } from '@mantine/core'

interface ColumnOptions {
  isBoolean?: boolean
}

type Column = Partial<MRT_ColumnDef> & {
  header: string
  accessorKey: string
  options?: ColumnOptions
}

interface TableProps<TData extends object> {
  rowIdentifier: string
  columns: Column[]
  data: TData[]
  actionMenuItems?: MantineReactTableProps['renderRowActionMenuItems']
  onRowSelectionChange?: (selection: MRT_RowSelectionState) => void
}

function Table<TData extends object>({
  data,
  rowIdentifier,
  actionMenuItems,
  onRowSelectionChange,
  columns,
}: TableProps<TData>) {
  const getColumnDefinitions = (cols: Column[]) => {
    const columnDefinitions: MRT_ColumnDef[] = []

    cols.map((column) => {
      let columnDef: MRT_ColumnDef = { ...column }

      if (column.options) {
        if (column.options.isBoolean) {
          columnDef = {
            enableGlobalFilter: false,
            enableSorting: false,
            filterVariant: 'checkbox',
            size: 20,
            Cell: ({ cell }) => (
              <Box
                sx={(theme) => ({
                  color: cell.getValue() ? theme.colors.green[5] : theme.colors.red[5],
                })}
              >
                {cell.getValue<boolean>() === true ? (
                  <IconCircleCheckFilled color="green" />
                ) : (
                  <IconCircleXFilled />
                )}
              </Box>
            ),
            ...columnDef,
          }
        }
      }

      columnDefinitions.push(columnDef)
    })

    return columnDefinitions
  }

  const columnDefs = useMemo(() => getColumnDefinitions(columns), [columns])
  const [rowSelection, setRowSelection] = useState<MRT_RowSelectionState>({})

  useEffect(() => {
    if (onRowSelectionChange) {
      onRowSelectionChange(rowSelection)
    }
  }, [rowSelection, onRowSelectionChange])

  return (
    <MantineReactTable
      // State
      initialState={{ density: 'xs', showGlobalFilter: true }}
      state={{ rowSelection }}
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      getRowId={(originalRow) => originalRow[rowIdentifier]}
      columns={columnDefs}
      data={data}
      // Editing and toggles
      enableEditing={false}
      enableDensityToggle={false}
      positionGlobalFilter="left"
      enableFullScreenToggle={false}
      // Selection
      enableRowSelection={typeof onRowSelectionChange !== undefined}
      onRowSelectionChange={setRowSelection}
      // Actions
      enableRowActions
      positionActionsColumn="last"
      renderRowActionMenuItems={actionMenuItems}
      // Search
      mantineSearchTextInputProps={{
        variant: 'filled',
        sx: { minWidth: '400px' },
      }}
    />
  )
}

export default Table
