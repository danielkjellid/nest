import { DragStart, DraggableLocation, DropResult } from 'react-beautiful-dnd'

function useDragAndDropSingleList<T>({
  items,
  onSequenceChange,
}: {
  items: T[]
  onSequenceChange: (items: T[]) => void
}) {
  const onDragStart = () => {
    if (window.navigator.vibrate) {
      window.navigator.vibrate(100)
    }
  }

  const onDragEnd = (result: DropResult) => {
    if (result.combine) {
      const newItems: T[] = items.slice()
      newItems.splice(result.source.index, 1)
      onSequenceChange(newItems)
      return
    }

    if (!result.destination) {
      return
    }

    if (result.destination.index === result.source.index) {
      return
    }

    const newItems = reorder(items, result.source.index, result.destination.index)

    onSequenceChange(newItems)
  }

  return {
    onDragStart,
    onDragEnd,
  }
}

function useDragAndDropMultipleLists<T>(
  itemsLists: { [key: string]: T[] },
  onSequenceChange: (itemsLists: { [key: string]: T[] }) => void,
  onDragStarted: (draggableLocation: DraggableLocation) => void
) {
  const onDragStart = (start: DragStart) => {
    onDragStarted(start.source)
    if (window.navigator.vibrate) {
      window.navigator.vibrate(100)
    }
  }

  const onDragEnd = (result: DropResult) => {
    const { source, destination } = result

    if (!destination) {
      return
    }

    if (source.droppableId === destination.droppableId) {
      // item has moved within its own list
      const internalResult: { [key: string]: T[] } = itemsLists
      internalResult[source.droppableId] = reorder(
        itemsLists[source.droppableId],
        source.index,
        destination.index
      )
      onSequenceChange(internalResult)
    } else {
      // item has moved between two lists
      const moveResult = move(
        itemsLists[source.droppableId],
        itemsLists[destination.droppableId],
        source,
        destination
      )

      onSequenceChange(moveResult)
    }
  }

  return {
    onDragStart,
    onDragEnd,
  }
}

function reorder<T>(list: T[], startIndex: number, endIndex: number) {
  const result = Array.from(list)
  const [removed] = result.splice(startIndex, 1)
  result.splice(endIndex, 0, removed)

  return result
}

function move<T>(
  source: T[],
  destination: T[],
  droppableSource: DraggableLocation,
  droppableDestination: DraggableLocation
) {
  const sourceClone = Array.from(source)
  const destinationClone = Array.from(destination)
  const [removed] = sourceClone.splice(droppableSource.index, 1)

  destinationClone.splice(droppableDestination.index, 0, removed)

  const result: { [key: string]: T[] } = {
    [droppableSource.droppableId]: sourceClone,
    [droppableDestination.droppableId]: destinationClone,
  }

  return result
}

export { useDragAndDropMultipleLists, useDragAndDropSingleList }
