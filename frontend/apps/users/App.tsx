import {
  APIResponse,
  UserList,
  UserListAPIResponse,
  UsersToggleActive,
} from '../../types/generated/dist'
/* eslint-disable react/prop-types */
import { Button, Menu, Title } from '@mantine/core'
import React, { useState } from 'react'
import { useFetch, useLazyFetch } from '../../hooks/fetcher'

import { IconEye } from '@tabler/icons-react'
import { MRT_RowSelectionState } from 'mantine-react-table'
import Table from '../../components/Table'
import View from '../../components/View'
import { notifications } from '@mantine/notifications'
import { performPost } from '../../hooks/fetcher/http'
import urls from './urls'
import { useCommonContext } from '../../contexts/CommonProvider'

interface UsersAppInnerProps {
  results: { users: UserListAPIResponse }
  refetch: () => void
}

function UsersAppInner({ results, refetch }: UsersAppInnerProps) {
  const { users } = results
  const { currentUser } = useCommonContext()
  const [selectedRows, setSelectedRows] = useState<MRT_RowSelectionState>({})

  const onToggleActive = async () => {
    if (users.data) {
      const usersToUpdate = users.data
        .filter((user) => Object.keys(selectedRows).includes(user.id.toString()))
        .map((user) => user.id)

      if (usersToUpdate.length) {
        const payload: UsersToggleActive = { userIds: usersToUpdate }
        try {
          await performPost<APIResponse>(urls.toggleActive(), payload)
          notifications.show({
            title: 'Users updated',
            message: 'Successfully toggled active state of users.',
            color: 'green',
          })
          setSelectedRows({})
          refetch()
        } catch (e) {
          const error = e as { message: string }
          notifications.show({
            title: 'Something went wrong',
            message: error.message,
            color: 'red',
          })
          console.error(e)
        }
      }
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Title>Users</Title>
        <div className="flex items-center space-x-3">
          {Object.keys(selectedRows).length > 0 && (
            <Button.Group>
              <Button variant="default" onClick={() => onToggleActive()}>
                Toggle active
              </Button>
              <Button variant="default">Delete</Button>
            </Button.Group>
          )}
          <Button>Add user</Button>
        </div>
      </div>

      <Table<UserList>
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
        rowSelection={selectedRows}
        onRowSelectionChange={setSelectedRows}
        actionMenuItems={({ row }) => [
          <>
            <form key={1} action="/hijack/acquire/" method="post">
              <input name="csrfmiddlewaretoken" type="hidden" value={window.csrfToken} />
              <input type="hidden" name="user_pk" value={row.id} />
              <Menu.Item
                key={1}
                icon={<IconEye />}
                type="submit"
                disabled={
                  currentUser.id.toString() === row.id.toString() ||
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
  const users = useFetch<UserListAPIResponse>(urls.list())

  const refetch = () => {
    users.reload()
  }

  return (
    <View<object, UsersAppInnerProps>
      component={UsersAppInner}
      results={{ users }}
      componentProps={{ refetch }}
      loadingProps={{ description: 'Loading users...' }}
      errorProps={{ description: 'There was an error getting users. Please try again.' }}
    />
  )
}

export default UsersApp
