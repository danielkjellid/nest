/* eslint-disable react/prop-types */
import { IconCircleCheckFilled, IconCircleXFilled } from '@tabler/icons-react'
import { MRT_ColumnDef, MRT_Row, MRT_TableInstance, MantineReactTable } from 'mantine-react-table'
import React, { useMemo } from 'react'

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
  actionMenuItems?: (props: { row: MRT_Row; table: MRT_TableInstance }) => React.ReactNode
}

function Table<TData extends object>({
  data,
  rowIdentifier,
  actionMenuItems,
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

  return (
    <MantineReactTable
      enableEditing={false}
      enableDensityToggle={false}
      positionGlobalFilter="left"
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      getRowId={(originalRow) => originalRow[rowIdentifier]}
      enableRowSelection
      positionActionsColumn="last"
      enableRowActions
      renderRowActionMenuItems={actionMenuItems}
      enableFullScreenToggle={false}
      initialState={{ density: 'xs', showGlobalFilter: true }}
      mantineSearchTextInputProps={{
        variant: 'filled',
        sx: { minWidth: '400px' },
      }}
      columns={columnDefs}
      data={data}
    />
  )
}

export default Table
