#! /usr/bin/env python3

import cv2

def combine_boxes(img, boxes):
  #boxes[i] = (label,x0,y0,x1,y1)
  overlaps = [ [i] for i in range(len(boxes)) ]
  # Each overlaps[i] is a list of all overlapping boxes
  for i in range(len(boxes)):
    # Collect every box that overlaps with i and put it in i
    for j in range(len(boxes)):
      if i == j:
        continue
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
  # Merge indirect overlaps
  for _ in range(2):
    for i in range(len(boxes)):
      indirect = set()
      for overlap in overlaps[i]:
        indirect.update(overlaps[overlap])
      # Remove duplicates, ensure index 0 is the box index
      overlaps[i] = list(indirect)
      overlaps[i].remove(i)
      overlaps[i].insert(0,i)
  # Lambda functions for grouped box painting
  # Check whether we can start painting along a box's edge
  on_edge = {'down': lambda x,y,box: x == box[1] and \
                              y >= box[2] and y < box[4],
            'right': lambda x,y,box: y == box[4] and \
                              x >= box[1] and x < box[3],
            'up':    lambda x,y,box: x == box[3] and \
                              y > box[2] and y <= box[4],
            'left':  lambda x,y,box: y == box[2] and \
                              x > box[1] and x <= box[3]}
  # The maximum point we could move to in a direction
  max_end = {'down': lambda x,y,box: (x, box[4]),
            'right': lambda x,y,box: (box[3], y),
            'up':    lambda x,y,box: (x, box[2]),
            'left':  lambda x,y,box: (box[1], y)}
  # Check whether a box could cross a line
  box_clear = {'down': lambda x,y,box: x < box[1] or x > box[3],
              'right': lambda x,y,box: y < box[2] or y > box[4],
              'up':    lambda x,y,box: x < box[1] or x > box[3],
              'left':  lambda x,y,box: y < box[2] or y > box[4]}
  # Return endx,endy ensuring there won't be a collision
  no_collide = {'down':  lambda x,y,endx,endy,box: (x,
                                                    box[2] if \
                                                y < box[2] and endy > box[2] \
                                                else endy),
                'right': lambda x,y,endx,endy,box: (box[1] if \
                                                x < box[1] and endx > box[1] \
                                                else endx, y),
                'up':    lambda x,y,endx,endy,box: (x,
                                                    box[4] if \
                                                y > box[4] and endy < box[4] \
                                                else endy),
                'left':  lambda x,y,endx,endy,box: (box[3] if \
                                                x > box[3] and endx < box[3] \
                                                else endx, y)}
  # Whether we have a line to paint
  have_line = {'down': lambda x,y,endx,endy: y < endy,
              'right': lambda x,y,endx,endy: x < endx,
              'up':    lambda x,y,endx,endy: endy < y,
              'left':  lambda x,y,endx,endy: endx < x}
  # Our line painting method
  paint = lambda start, end: cv2.line(img, start, end, (0,255,0), 2)
  # Track boxes that are already grouped
  combined = []
  # Process overlap groups in reverse, guarantees groups are inclusive
  while len(overlaps) > 0:
    overlap = overlaps.pop()
    # Skip if we've already done this overlap or there is no overlap
    if overlap[0] in combined or len(overlap) == 1:
      continue
    # Add these to our done list
    combined += overlap
    # Origin of painted lines is the lowest y of the lowest x
    x = boxes[overlap[0]][1]
    # Create a combined label for box 0
    label = ''
    for conflict in overlap:
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
    direction = 'down'
    paint((x,y), (endx,endy))
    # Advance x and y
    x,y = endx,endy
    # Paint the shape
    while (x, y) != (stopx, stopy):
      direction = 'right' if direction == 'down' else \
                    'up' if direction == 'right' else \
                    'left' if direction == 'up' else \
                    'down'
      for lhs in overlap:
        # If we aren't on the boxes edge
        if not on_edge[direction](x,y,boxes[lhs]):
          continue
        endx, endy = max_end[direction](x,y,boxes[lhs])
        # We need to ensure no other box crosses this possible line:
        for rhs in overlap:
          if lhs == rhs or box_clear[direction](x,y,boxes[rhs]):
            continue
          endx, endy = no_collide[direction](x,y,endx,endy,boxes[rhs])
        if have_line[direction](x,y,endx,endy):
          paint((x,y), (endx,endy))
          x,y = endx,endy
          break
    # The shape is painted
    # Make boxes none and get coordinates for the grouped label
    # Get the top-left most x and y
    for conflict in overlap:
      x = min(x, boxes[conflict][1])
      if x == boxes[conflict][1]:
        y = min(y, boxes[conflict][2])
    endx = x + 280
    # Move x,y right/up as needed
    for conflict in overlap:
      # Within the x and y
      if endx <= boxes[conflict][1] or x > boxes[conflict][3]:
        continue
      if y <= boxes[conflict][2]:
        continue
      x,y = boxes[conflict][1],boxes[conflict][2]
      endx = x + 280
    for conflict in overlap:
      boxes[conflict] = None
    # Give the first conflict box the label and position
    boxes[overlap[0]] = (label[:-1], x, y)
  return boxes

