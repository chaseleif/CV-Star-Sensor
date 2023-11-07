#! /usr/bin/env python3

import cv2

def combine_boxes(img, boxes):
  #boxes[i] = (label,x0,y0,x1,y1)
  overlaps = []
  for i in range(len(boxes)):
    for j in range(i+1,len(boxes)):
      # if i's x0 is within the range of j's (x0,x1)
      # or i's x1 is within the range of j's (x0,x1)
      # and
      # if i's y0 is within the range of j's (y0,y1)
      # or i's y1 is within the range of j's (y0,y1)
      if ((boxes[j][1] < boxes[i][1] and boxes[i][1] < boxes[j][3]) or \
          (boxes[j][1] < boxes[i][3] and boxes[i][3] < boxes[j][3]))  and \
          ((boxes[j][2] < boxes[i][2] and boxes[i][2] < boxes[j][4]) or \
          (boxes[j][2] < boxes[i][4] and boxes[i][4] < boxes[j][4])):
        overlaps.append((i,j))
  combined = []
  # Our line painting method
  paint = lambda start, end: cv2.line(img, start, end, (0,255,0), 2)
  for i in range(len(overlaps)):
    # If we've already done this overlap, skip
    if overlaps[i][0] in combined:
      continue
    # The minimum conflict is this pair of boxes
    conflicts = [overlaps[i][0], overlaps[i][1]]
    # For any later overlaps that are in the same group
    for j in range(i+1,len(overlaps)):
      # If neither point is in the current conflicts we are done
      if overlaps[j][0] not in conflicts and overlaps[j][1] not in conflicts:
        break
      # Add these points to our conflicts
      conflicts += [overlaps[j][0],overlaps[j][1]]
    # Remove duplicates
    conflicts = list(set(conflicts))
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
      for j in range(len(conflicts)):
        # x must equal x0
        if x != boxes[conflicts[j]][1]:
          continue
        # y must be between y0 and y1
        if y < boxes[conflicts[j]][2] or y > boxes[conflicts[j]][4]:
          continue
        # We could go down as far as to y1
        endy = boxes[conflicts[j]][4]
        # We need to ensure no other box crosses this possible line:
        for k in range(len(conflicts)):
          if j == k:
            continue
          # Only if the x is between their x0 and x1
          if x < boxes[conflicts[k]][1] or x > boxes[conflicts[k]][3]:
            continue
          # We would cross the other box, stop at their y
          if y < boxes[conflicts[k]][2] and endy > boxes[conflicts[k]][2]:
            endy = boxes[conflicts[k]][2]
        # Paint downward
        if y < endy:
          paint((x,y), (x,endy))
          y = endy
          break
      # Go right, y must equal y1 and x must be between x0 and x1
      for j in range(len(conflicts)):
        # y must be y1
        if y != boxes[conflicts[j]][4]:
          continue
        # x must be between x0 and x1
        if x < boxes[conflicts[j]][1] or x > boxes[conflicts[j]][3]:
          continue
        # We could go right as far as to x1
        endx = boxes[conflicts[j]][3]
        # We need to ensure no other box crosses this possible line:
        for k in range(len(conflicts)):
          if j == k:
            continue
          # Only if the y is between their y0 and y1
          if y < boxes[conflicts[k]][2] or y > boxes[conflicts[k]][4]:
            continue
          # We would cross the other box, stop at their x
          if x < boxes[conflicts[k]][1] and endx > boxes[conflicts[k]][1]:
            endx = boxes[conflicts[k]][1]
        # Paint rightward
        if x < endx:
          paint((x,y), (endx,y))
          x = endx
          break
      # Go up, x must equal x1 and y must be between y0 and y1
      for j in range(len(conflicts)):
        # x must be x1
        if x != boxes[conflicts[j]][3]:
          continue
        # y must be between y0 and y1
        if y < boxes[conflicts[j]][2] or y > boxes[conflicts[j]][4]:
          continue
        # We could go up as far as to y0
        endy = boxes[conflicts[j]][2]
        # We need to ensure no other box crosses this possible line:
        for k in range(len(conflicts)):
          if j == k:
            continue
          # Only if the x is between their x0 and x1
          if x < boxes[conflicts[k]][1] or x > boxes[conflicts[k]][3]:
            continue
          # We would cross the other box, stop at their y
          if y > boxes[conflicts[k]][4] and endy < boxes[conflicts[k]][4]:
            endy = boxes[conflicts[k]][4]
        # Paint upward
        if endy != y:
          paint((x,y), (x,endy))
          y = endy
          break
      # Go left, y must equal y0 and x must be between x0 and x1
      for j in range(len(conflicts)):
        # y must be y0
        if y != boxes[conflicts[j]][2]:
          continue
        # x must be between x0 and x1
        if x < boxes[conflicts[j]][1] or x > boxes[conflicts[j]][3]:
          continue
        # We could go left as far as to x0
        endx = boxes[conflicts[j]][1]
        # We need to ensure no other box crosses this possible line:
        for k in range(len(conflicts)):
          if j == k:
            continue
          # Only if the y is between their y0 and y1
          if y < boxes[conflicts[k]][2] or y > boxes[conflicts[k]][4]:
            continue
          # We would cross the other box, stop at their x
          if x > boxes[conflicts[k]][3] and endx < boxes[conflicts[k]][3]:
            endx = boxes[conflicts[k]][3]
        # Paint leftward
        if endx != x:
          paint((x,y), (endx, endy))
          x = endx
          break
    # The shape is painted, change box 0's coordinates for the label
    for conflict in conflicts:
      x = min(x, boxes[conflict][1])
      endx = max(endx, boxes[conflict][3])
      y = min(y, boxes[conflict][2])
      boxes[conflict] = None
    boxes[conflicts[0]] = (label[:-1], x, y)
  return boxes

