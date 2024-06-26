/* eslint-disable react/prop-types */
import { Box } from '@mantine/core'
import { IconCircleCheckFilled, IconCircleXFilled } from '@tabler/icons-react'
import {
  type MRT_ColumnDef,
  type MRT_RowSelectionState,
  type MRT_TableOptions,
  MantineReactTable,
} from 'mantine-react-table'
import { useEffect, useMemo, useState } from 'react'

import { useCommonContext } from '../../contexts/CommonProvider'

interface ColumnOptions {
  isBoolean?: boolean
}

type Column<TData extends object> = Partial<MRT_ColumnDef<TData>> & {
  header: string
  accessorKey?: string
  options?: ColumnOptions
  Cell?: MRT_ColumnDef<TData>['Cell']
}

interface TableProps<TData extends object> {
  rowIdentifier: string
  columns: Column<TData>[]
  data: TData[]
  actionMenuItems?: MRT_TableOptions<TData>['renderRowActionMenuItems']
  onRowSelectionChange?: (selection: MRT_RowSelectionState) => void
  initialState?: MRT_TableOptions<TData>['initialState']
  positionToolbarAlertBanner?: MRT_TableOptions<TData>['positionToolbarAlertBanner']
}

function Table<TData extends object>({
  data,
  rowIdentifier,
  actionMenuItems,
  onRowSelectionChange,
  columns,
  initialState = {},
  positionToolbarAlertBanner,
}: TableProps<TData>) {
  const getColumnDefinitions = (cols: Column<TData>[]) => {
    const columnDefinitions: MRT_ColumnDef<TData>[] = []

    cols.map((column) => {
      let columnDef: MRT_ColumnDef<TData> = { ...column }

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

  const { currentUser } = useCommonContext()
  const columnDefs = useMemo<MRT_ColumnDef<TData>[]>(() => getColumnDefinitions(columns), [columns])
  const [rowSelection, setRowSelection] = useState<MRT_RowSelectionState>({})

  useEffect(() => {
    if (onRowSelectionChange) {
      onRowSelectionChange(rowSelection)
    }
  }, [rowSelection, onRowSelectionChange])

  return (
    <MantineReactTable
      // State
      initialState={{
        density: 'xs',
        showGlobalFilter: true,
        pagination: { pageSize: 25, pageIndex: 0 },
        ...initialState,
      }}
      state={{ rowSelection: rowSelection }}
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      getRowId={(originalRow) => originalRow[rowIdentifier]}
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      columns={columnDefs}
      data={data}
      // mantinePaginationProps={{ rowsPerPageOptions: ['25', '50', '100'] }} Causes error?!
      // Editing and toggles
      enableEditing={false}
      enableDensityToggle={false}
      positionGlobalFilter="left"
      enableFullScreenToggle={false}
      // Selection
      enableRowSelection={currentUser && currentUser.isStaff && onRowSelectionChange !== undefined}
      onRowSelectionChange={setRowSelection}
      // Actions
      enableRowActions={actionMenuItems !== undefined}
      positionActionsColumn="last"
      renderRowActionMenuItems={actionMenuItems}
      // Search
      mantineSearchTextInputProps={{
        variant: 'filled',
        sx: { minWidth: '400px' },
      }}
      mantinePaperProps={{
        radius: '6px',
        withBorder: false,
        shadow: 'sm',
      }}
      enableGrouping={'grouping' in initialState}
      positionToolbarAlertBanner={positionToolbarAlertBanner}
    />
  )
}

export default Table
