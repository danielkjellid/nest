import { ScrollArea, Text, rem } from '@mantine/core'
import cx from 'classnames'
import { useEffect, useRef, useState } from 'react'

import { useTableOfContentsStyles } from './TableOfContents.styles'

interface Heading {
  label: string
  slug: string
}

interface TableOfContentProps {
  headings: Heading[]
}

// Calculate closest id (slug) and set active state.
function getActiveElement(rects: DOMRect[]) {
  if (rects.length === 0) {
    return -1
  }

  const closest = rects.reduce(
    (acc, item, index) => {
      if (Math.abs(acc.position) < Math.abs(item.y)) {
        return acc
      }

      return {
        index,
        // - 100 offset because of offset when scrolling into view.
        position: item.y - 100,
      }
    },
    { index: 0, position: rects[0].y }
  )

  return closest.index
}

function TableOfContents({ headings }: TableOfContentProps) {
  const { classes } = useTableOfContentsStyles()
  const [active, setActive] = useState(2)
  const slugs = useRef<HTMLDivElement[]>([])

  useEffect(() => {
    slugs.current = headings.map(
      (heading) => document.getElementById(heading.slug) as HTMLDivElement
    )
  }, [headings])

  const handleScroll = () => {
    setActive(getActiveElement(slugs.current.map((d) => d.getBoundingClientRect())))
  }

  // Add event listener on scroll and set active based on which id is currently closest.
  useEffect(() => {
    setActive(getActiveElement(slugs.current.map((d) => d.getBoundingClientRect())))
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  if (headings.length === 0) {
    return null
  }

  return (
    <nav className={cx(classes.wrapper, { [classes.withTabs]: true })}>
      <div className={classes.inner}>
        <div>
          <ScrollArea.Autosize mah={`calc(100vh - ${rem(140)})`} type="scroll" offsetScrollbars>
            <div className={classes.items}>
              {headings.map((heading, index) => (
                <Text<'a'>
                  key={heading.slug}
                  component="a"
                  size="sm"
                  className={cx(classes.link, { [classes.linkActive]: active === index })}
                  href={`#${heading.slug}`}
                  onClick={(event) => {
                    event.preventDefault()
                    const destination = document.getElementById(heading.slug)
                    if (destination?.offsetTop) {
                      window.scrollTo(0, destination?.offsetTop - 100)
                    } else {
                      destination?.scrollIntoView()
                    }
                  }}
                >
                  {heading.label}
                </Text>
              ))}
            </div>
          </ScrollArea.Autosize>
        </div>
      </div>
    </nav>
  )
}

export { TableOfContents }
