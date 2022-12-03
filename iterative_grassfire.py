# Note that this is far from finished it its current state. Please don't rely on it.
"""
A reasonably performant grassfire algorithm capable of operating in arbitrarily large dimensions.

A stated goal is to avoid the stack size limit issues that a straightforward recursive implementation might encounter.

O(?) time complexity
O(?) space complexity
"""

def make_n_cube_field(size, dimensions):
    """Recursively generate an n-cube field of 'dimensions' dimensions.

    Take care of the potentially explosive O(size**dimensions) space complexity.
    """
    # end case
    if dimensions == 1:
        return [None] * size

    # populate higher dimensional containers
    l = [None] * size
    for i in range(size):
        l[i] = make_n_cube_field(size, dimensions - 1)
    return l


def visit_all_nodes(field, position, dimensions, grassfire):
    """Visit every node in the field.
    Call the grassfire function on each node.
    """
    if isinstance(field, list):
        for i in range(len(field)):
            visit_all_nodes(field[i], position + (i,), dimensions, grassfire)
    else:
        # print(field, position)
        grassfire(field, position, dimensions)

def fast_visit_all_nodes(field, position, dimensions, grassfire):
    """A hopefully faster visit_all_nodes
    """
    position = [0] * dimensions
    consecutive_index_errors = 0
    while 1:
        try:
            splat_index(field, position)
            print(position)
            # finally, increase the most nested list
            position[dimensions - 1] += 1
            # we were successful, no consecutive errors now
            consecutive_index_errors = 0
        except IndexError:
            consecutive_index_errors += 1
            index_to_iterate = dimensions - consecutive_index_errors - 1
            # we're done
            if index_to_iterate < 0:
                break
            position[index_to_iterate] += 1
            # reset the positions nested beneath the current index
            # e.g. when index_to_iterate == 0 then set position[1] = 0 and position[2] = 0
            for position_to_reset in range(index_to_iterate + 1, dimensions):
                position[position_to_reset] = 0

def faster_visit_all_nodes(field, position, dimensions, grassfire):
    """A hopefully faster visit_all_nodes
    """
    position = [0] * dimensions
    current_field = field
    frame_number = 0
    stack = []
    current_iter = enumerate(iter(current_field))

    # ci = iter(root) [ [ [] ] ]
    # stack.append(ci)
    # ci = iter(next(ci)) [ [] ]
    # stack.append(ci)
    # ci = iter(next(ci)) []
    # for node in ci:
    #   [0, 0, 0]
    #   [0, 0, 1]
    #   StopIteration
    # ci = iter([ [] ]) = stack.pop(-1)
    # stack.append(ci)
    # ci = next(ci)
    # for node in ci:
    #   [0, 1, 0]
    #   [0, 1, 1]
    # ci = iter([ [] ]) = stack.pop(-1)
    # ci = next(ci)
    # StopIteration
    # ci = iter([ [ [] ] ]) = stack.pop(-1)
    # ci = next(ci)
    # [1, 0, 0]
    # [1, 0, 1]
    # [1, 1, 0]
    # [1, 1, 1]

    while 1:
        if len(stack) == dimensions - 1:
            # This is the final dimension of the field simply iterate through.
            for index, node in current_iter:
                position[dimensions - 1] = index
                grassfire(field, position, dimensions)
            current_iter, frame_number = stack.pop(-1)
        else:
            try:
                index, current_field = next(current_iter)
            except StopIteration:
                if len(stack) == 0:
                    break
                current_iter, frame_number = stack.pop(-1)
                continue
            position[len(stack)] = index
            stack.append((current_iter, frame_number))
            frame_number += 1
            current_iter = enumerate(iter(current_field))

def splat_index(container, indices, **kwargs):
    """Retrieve or set an object inside a nested container using the list of indices provided.
    e.g. splat_index(cube_space, (1,2,3,4,5)) == cube_space[1][2][3][4][5]

    If the kwarg 'set' is passed, the value passed in for 'set' will be assigned at that indices provided.

    This function doesn't allow negative indexing.
    This is for the convenience of detecting out of bounds situations.
    """
    result = container
    for i in range(len(indices) - 1):
        result = result[indices[i]]

    final_index = indices[-1]
    if 'set' in kwargs:
        result[final_index] = kwargs['set']
    return result[final_index]

def strict_neighbor(field, start_position, dimensions):
    """Find all neighbors that are +/- 1 unit away in any single dimension.
    The algorithm used is iterative rather than recursive due to stack size limitations.
    """
    return
    to_check = set()
    if splat_index(visited_field, start_position) is None:
        to_check = {start_position}

    while len(to_check) > 0:
        current_position = to_check.pop()
        # TODO actually perform a check
        if splat_index(field, current_position) or True:
            # denote that this position has been visited
            splat_index(visited_field, current_position, set=1)
            for i in range(dimensions):
                # the next two generated positions will certainly be out of bounds sometimes
                up = current_position[:i] + (current_position[i] + 1,) + current_position[i + 1:]
                down = current_position[:i] + (current_position[i] - 1,) + current_position[i + 1:]

                try:
                    if splat_index(visited_field, up) is None:
                        to_check.add(up)
                except IndexError:
                    pass

                try:
                    # ensure that negative indices are skipped
                    if current_position[i] - 1 > 0 and splat_index(visited_field, down) is None:
                        to_check.add(down)
                except IndexError:
                    pass

size = 1000
dimensions = 3

print('Start')
field = make_n_cube_field(size, dimensions)
visited_field = make_n_cube_field(size, dimensions)
# visit_all_nodes(field, (), dimensions, strict_neighbor)
# fast_visit_all_nodes(field, (), dimensions, strict_neighbor)
faster_visit_all_nodes(field, (), dimensions, strict_neighbor)
print('Done\n')