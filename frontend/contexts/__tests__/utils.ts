import { Config, Home, User } from '../CommonProvider'

import { MenuItem } from '../MenuProvider'
import { UnitListOut } from '../../types'

const homeTestUtil = (
  id = 1,
  address = 'Example road 1',
  numResidents = 2,
  numWeeksRecipeRotation = 2,
  weeklyBudget = 2000,
  isActive = true
): Home => ({
  id: id,
  address: address,
  numResidents: numResidents,
  numWeeksRecipeRotation: numWeeksRecipeRotation,
  weeklyBudget: weeklyBudget,
  isActive: isActive,
})

const userTestUtil = (
  id = 1,
  email = 'user@example.com',
  firstName = 'Example',
  lastName = 'User',
  isActive = true,
  isStaff = false,
  isSuperuser = false,
  isHijacked = false,
  home = undefined
): User => ({
  id: id,
  email: email,
  firstName: firstName,
  lastName: lastName,
  fullName: `${firstName} ${lastName}`,
  isActive: isActive,
  isStaff: isStaff,
  isSuperuser: isSuperuser,
  home: home,
  isHijacked: isHijacked,
})

const configTestUtil = (isProduction = true): Config => ({
  isProduction: isProduction,
})

export const createCommonContextTestData = () => ({
  currentHome: homeTestUtil(),
  currentUser: userTestUtil(),
  availableHomes: [homeTestUtil(2, 'Example road 2')],
  config: configTestUtil(),
})

export const menuItemTestUtil = (
  key = 'menuItemKey',
  title = 'Item title',
  end = true
): MenuItem => ({
  key: key,
  title: title,
  end: end,
})

export const unitItemTestUtil = (id = 1, name = 'Gram', displayName = 'Gram (g)'): UnitListOut => ({
  id: id,
  name: name,
  displayName: displayName,
})
