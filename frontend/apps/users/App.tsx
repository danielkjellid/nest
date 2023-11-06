/* eslint-disable react/prop-types */
import { Menu, Title } from '@mantine/core'
import { IconEye } from '@tabler/icons-react'
import { type MRT_RowSelectionState } from 'mantine-react-table'
import React, { useState } from 'react'

import { Button } from '../../components/Button'
import Table from '../../components/Table'
import View from '../../components/View'
import { useCommonContext } from '../../contexts/CommonProvider'
import { useFetch } from '../../hooks/fetcher'
import { type UserListOut, type UserListOutAPIResponse } from '../../types'
import { urls } from '../urls'

interface UsersAppInnerProps {
  results: { users: UserListOutAPIResponse }
}

function UsersAppInner({ results }: UsersAppInnerProps) {
  const { users } = results
  const { currentUser } = useCommonContext()
  const [selectedRows, setSelectedRows] = useState<MRT_RowSelectionState>({})

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title weight={600}>Users</Title>
        <div className="flex items-center space-x-3">
          {Object.keys(selectedRows).length > 0 && (
            <Button.Group>
              <Button variant="default">Deactivate</Button>
              <Button variant="default">Delete</Button>
            </Button.Group>
          )}
          <Button>Add user</Button>
        </div>
      </div>

      <Table<UserListOut>
        rowIdentifier="id"
        columns={[
          { header: 'Id', accessorKey: 'id', size: 20 },
          { header: 'Name', accessorKey: 'fullName' },
          { header: 'Email', accessorKey: 'email' },
          { header: 'Home', accessorKey: 'home.address' },
          { header: 'Active', accessorKey: 'isActive', options: { isBoolean: true } },
          { header: 'Staff', accessorKey: 'isStaff', options: { isBoolean: true } },
        ]}
        data={users.data || []}
        onRowSelectionChange={setSelectedRows}
        actionMenuItems={({ row }) => [
          <>
            <form action="/hijack/acquire/" method="post">
              <input name="csrfmiddlewaretoken" type="hidden" value={window.csrfToken} />
              <input type="hidden" name="user_pk" value={row.id} />
              <Menu.Item
                key={1}
                icon={<IconEye />}
                type="submit"
                disabled={
                  (currentUser && currentUser.id.toString() === row.id.toString()) ||
                  !currentUser ||
                  (!currentUser.isSuperuser &&
                    users.data?.find((user) => user.id.toString() === row.id.toString())
                      ?.isSuperuser)
                }
              >
                Hijack
              </Menu.Item>
            </form>
          </>,
        ]}
      />
    </div>
  )
}

function UsersApp() {
  const users = useFetch<UserListOutAPIResponse>(urls.users.list())

  return (
    <View<object, UsersAppInnerProps>
      component={UsersAppInner}
      results={{ users }}
      componentProps={{}}
      loadingProps={{ description: 'Loading users...' }}
      errorProps={{ description: 'There was an error getting users. Please try again.' }}
    />
  )
}

export default UsersApp
