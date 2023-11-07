#! /usr/bin/env python3

import cv2

def combine_boxes(img, boxes):
  #boxes[i] = (label,x0,y0,x1,y1)
  overlaps = [ [i] for i in range(len(boxes)) ]
  for i in range(len(boxes)):
    for j in range(i+1,len(boxes)):
      # if i's x0 is within the range of j's (x0,x1)
      # or i's x1 is within the range of j's (x0,x1)
      # and
      # if i's y0 is within the range of j's (y0,y1)
      # or i's y1 is within the range of j's (y0,y1)
      if ((boxes[j][1] <= boxes[i][1] and boxes[i][1] <= boxes[j][3]) or \
          (boxes[j][1] <= boxes[i][3] and boxes[i][3] <= boxes[j][3]))  and \
          ((boxes[j][2] <= boxes[i][2] and boxes[i][2] <= boxes[j][4]) or \
          (boxes[j][2] <= boxes[i][4] and boxes[i][4] <= boxes[j][4])):
        overlaps[i].append(j)
        overlaps[j].append(i)
  combined = []
  # Our line painting method
  paint = lambda start, end: cv2.line(img, start, end, (0,255,0), 2)
  while len(overlaps) > 0:
    overlap = overlaps.pop()
    # Skip if we've already done this overlap, or there is no overlap
    if overlap[0] in combined or len(overlap) == 1:
      continue
    # Find any other connected overlaps
    for i in range(len(overlaps)):
      if any(box in overlap for box in overlaps[i]):
        overlap += overlaps[i]
        for j in range(i-1,-1,-1):
          if any(box in overlap for box in overlaps[j]):
            overlap += overlaps[j]
    # Remove potential duplicates
    conflicts = list(set(overlap))
    del overlap
    # Add these to our done list
    combined += conflicts
    # Origin of painted lines is the lowest y of the lowest x
    x = boxes[conflicts[0]][1]
    # Create a combined label for box 0
    label = ''
    for conflict in conflicts:
      label += boxes[conflict][0] + '\n'
      # Get the minimum x point
      x = min(x, boxes[conflict][1])
      # At our minimum x set our minimum y and get the first endx, endy
      if x == boxes[conflict][1]:
        y = boxes[conflict][2]
        endx, endy = x, boxes[conflict][4]
    # When x, y reach stopx, stopy we have completed the shape
    stopx, stopy = x, y
    # Draw our first line . . . downward (considering top left as 0,0)
    # We are guaranteed to be able to go straight down
    paint((x,y), (endx,endy))
    # Advance x and y
    x, y = endx, endy
    # Paint the shape
    while (x, y) != (stopx, stopy):
      # Prefer directions in order: Down>Right>Up>Left
      # We will not overlap
      # Go down, x must equal x0 and y must be between y0 and y1
      for lhs in conflicts:
        # x must equal x0
        if x != boxes[lhs][1]:
          continue
        # y must be between y0 and y1
        if y < boxes[lhs][2] or y > boxes[lhs][4]:
          continue
        # We could go down as far as to y1
        endy = boxes[lhs][4]
        # We need to ensure no other box crosses this possible line:
        for rhs in conflicts:
          if lhs == rhs:
            continue
          # Only if the x is between their x0 and x1
          if x < boxes[rhs][1] or x > boxes[rhs][3]:
            continue
          # We would cross the other box, stop at their y
          if y < boxes[rhs][2] and endy > boxes[rhs][2]:
            endy = boxes[rhs][2]
        # Paint downward
        if y < endy:
          paint((x,y), (x,endy))
          y = endy
          break
      # Go right, y must equal y1 and x must be between x0 and x1
      for lhs in conflicts:
        # y must be y1
        if y != boxes[lhs][4]:
          continue
        # x must be between x0 and x1
        if x < boxes[lhs][1] or x > boxes[lhs][3]:
          continue
        # We could go right as far as to x1
        endx = boxes[lhs][3]
        # We need to ensure no other box crosses this possible line:
        for rhs in conflicts:
          if lhs == rhs:
            continue
          # Only if the y is between their y0 and y1
          if y < boxes[rhs][2] or y > boxes[rhs][4]:
            continue
          # We would cross the other box, stop at their x
          if x < boxes[rhs][1] and endx > boxes[rhs][1]:
            endx = boxes[rhs][1]
        # Paint rightward
        if x < endx:
          paint((x,y), (endx,y))
          x = endx
          break
      # Go up, x must equal x1 and y must be between y0 and y1
      for lhs in conflicts:
        # x must be x1
        if x != boxes[lhs][3]:
          continue
        # y must be between y0 and y1
        if y < boxes[lhs][2] or y > boxes[lhs][4]:
          continue
        # We could go up as far as to y0
        endy = boxes[lhs][2]
        # We need to ensure no other box crosses this possible line:
        for rhs in conflicts:
          if lhs == rhs:
            continue
          # Only if the x is between their x0 and x1
          if x < boxes[rhs][1] or x > boxes[rhs][3]:
            continue
          # We would cross the other box, stop at their y
          if y > boxes[rhs][4] and endy < boxes[rhs][4]:
            endy = boxes[rhs][4]
        # Paint upward
        if endy < y:
          paint((x,y), (x,endy))
          y = endy
          break
      # Go left, y must equal y0 and x must be between x0 and x1
      for lhs in conflicts:
        # y must be y0
        if y != boxes[lhs][2]:
          continue
        # x must be between x0 and x1
        if x < boxes[lhs][1] or x > boxes[lhs][3]:
          continue
        # We could go left as far as to x0
        endx = boxes[lhs][1]
        # We need to ensure no other box crosses this possible line:
        for rhs in conflicts:
          if lhs == rhs:
            continue
          # Only if the y is between their y0 and y1
          if y < boxes[rhs][2] or y > boxes[rhs][4]:
            continue
          # We would cross the other box, stop at their x
          if x > boxes[rhs][3] and endx < boxes[rhs][3]:
            endx = boxes[rhs][3]
        # Paint leftward
        if endx < x:
          paint((x,y), (endx, endy))
          x = endx
          break
    # The shape is painted
    # Make boxes none and get coordinates for the grouped label
    # Get the bottom-left most x and y
    for conflict in conflicts:
      x = min(x, boxes[conflict][1])
      y = max(y, boxes[conflict][2])
    # Move x,y up/right as needed
    for conflict in conflicts:
      # This box starts at or below y
      if y < boxes[conflict][2]:
        boxes[conflict] = None
        continue
      # We don't have 680px space right, start from this x,y
      if boxes[conflict][1] - x < 680:
        x = boxes[conflict][1]
        y = boxes[conflict][2]
      # Clear this conflict box
      boxes[conflict] = None
    # Give the first conflict box the label and position
    boxes[conflicts[0]] = (label[:-1], x, y)
  return boxes

