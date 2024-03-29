
#test_timeseries = [0,0,1,1,1,2,3,4,5,5,5,5,5,5,4,3,2,1,0,1,2,3,2,1,0,0,0,1,2,3,4,5,5,5]
#interfaces = [1,4]
#count_changes(test_timeseries, interfaces)

interfaces = [1,4,6,8]
test_timeseries = [0,0,1,1,1,2,3,4,5,5,5,5,6,6,6,7,8,9,9,9,9,9,9,8,7,8,9,9,9,9,8,7,7,6,6,6,5,5,5,4,3,2,1,2,2,3,4,5,5,5,5,5,4,3,2,1,0,1,2,3,2,1,0,0,0,1,2,3,4,5,5,5]


def count_changes(timeseries, interfaces, min_residence=1):
    #if len(interfaces) == 2:
    if False:
        result = count_changes_2state(timeseries, interfaces, min_residence)
    else:
        result = count_changes_Nstate(timeseries, interfaces, min_residence)

    return result


def count_changes_Nstate(timeseries, interfaces, min_residence=1):
    '''
    region    state or interface or transition placement
    1         dimensions in state space
    N         states
    2(N-1)    interfaces
    N-1       forward changes
    N-1       backward changes

    concept            interface            assigned
                       parity               region idx

       [ state 1 ]                          0
    --- interface ---  o     ^  arrow in    0
       < xregion >           |  backward    1
    --- interface ---  e     |  direction   1
       [ state 2 ]                          2
    --- interface ---  o                    2
       < xregion >                          3
    --- interface ---  e                    3
       [ state 3 ]                          4
    --- interface ---  o                    4
       < xregion >                          5
    --- interface ---  e                    5
       [ state 3 ]                          6
    --- interface ---  o                    6
       < xregion >                          7
    --- interface ---  e                    7

          ...

       < xregion >
    --- interface ---                       2N-1
       [ state N ]                          2N

    Returns
    -------
    (forward_changes, backward_changes)

    2-tuple with sub N-tuples containing counts of
    forward and backward changes into states {N}
    '''

    assert len(interfaces) % 2 == 0 # always even since N is counting num & 1D
                                    # 2 interfaces per possible transition
                                    # 1 transition per state

    assert min_residence >= 1  # residence time
                                    # before transition "into" state

    n_interfaces       = len(interfaces)
    n_states           = int(n_interfaces / 2) + 1
    forward_changes    = [list() for _ in range(n_states - 1)]
    backward_changes   = [list() for _ in range(n_states - 1)]

    def assign_current_index(timepoint):
        '''Get first interface index higher than timepoint value
        '''
        # assume state 1: below interface[0]
        i = 0
        try:
            while timepoint > interfaces[i]:

                # if greater: check next
                i += 1

            # after no satisfy while condition return last i
            else:
                return i

        # timepoint is beyond last interface
        except IndexError:
            return i

    # Initial counting state cannot be the transition region
    #   - loop breaks with first actual state
    ts             = iter(enumerate(timeseries))
    current_region = assign_current_index(next(ts)[1])

    # while in transition region
    # TODO
    #while current_region in xregion:
    while current_region % 2 == 1:
        current_region = assign_current_index(next(ts)[1])
    else:
        last_region = current_region
        last_state  = current_region

    # Main loop to count transitions
    residence_time = -1
    for stepnum, tp in ts:
        current_region = assign_current_index(tp)

        # SAME idea
        #if current_region in states:
        if current_region % 2 == 0:

            # If in new region, residence tracking
            if current_region != last_state:

                # First visit, count starts
                if current_region != last_region:
                    last_region = current_region
                    residence_time += 1

                # SAME as elif shown
                #elif current_region == last_region:
                else:
                    residence_time += 1

                    # OFFICIALLY entered a state
                    if residence_time >= min_residence:
                        # Forwards if new index is higher
                        forwards   = True if last_state < last_region else False
                        last_state = last_region
                        
                        # FIXME to track the residence times
                        residence_time = -1

                        if forwards:
                            forward_changes[current_region//2-1].append(stepnum)
                        else:
                            backward_changes[current_region//2].append(stepnum)

            # Residing in state
            else:
                pass

        # In transition region
        else:
            # From a quick exit below `min_residence`
            #   - reset the residence counter
            # TODO FIXME probably don't need reset `last_region`
            if last_region != last_state:
                residence_time = -1
                last_region = last_state

            # From well-established `last_state`
            else:
                pass

    return (forward_changes, backward_changes)



def count_changes_2state(timeseries, interfaces, min_residence=1):
    '''Count changes between 2 primary states separated by a transition region
    Each state is defined by an exit/entrance interface, when the timeseries
    successfully exits a state and enters the other, a change is counted.
    
       [ state 1 ]

    --- interface ---

       < xregion >

    --- interface ---

       [ state 2 ]

    Returns
    -------
    (forward_changes, backward_changes)

    2-tuple with counts of forward and backward changes
    '''

    forward_changes    = list() # from state1 to state2
    backward_changes   = list() # from state2 to state1
    
    assert len(interfaces) == 2 # to use as described
    assert min_residence >= 1 # how long to remain before "in" state

    state1 = "state1"
    state2 = "state2"
    states = [state1, state2]
    xregion = "xregion"

    def check_current(timepoint):
        if timepoint < interfaces[0]:
            return state1
        elif timepoint > interfaces[1]:
            return state2
        else:
            return xregion

    # Initial state cannot be the transition region
    #   - loop breaks with first actual state
    ts = iter(enumerate(timeseries))
    current_region = check_current(next(ts)[1])
    while current_region == xregion:
        current_region = check_current(next(ts)[1])

    else:
        # `_last_state` tracks residence w/out assigning state
        _last_state = current_region
        # `last_state` is assignment of last state
        last_state = current_region

    # Main loop to count transitions
    residence_time = -1
    for stepnum, tp in ts:
        current_region = check_current(tp)

        if current_region in states:

            # If in new region, start residence tracker
            if current_region != last_state:

                if current_region != _last_state:
                    _last_state = current_region
                    residence_time += 1

                # SAME as elif here
                #elif current_region == _last_state:
                else:
                    residence_time += 1

                    if residence_time >= min_residence:
                        last_state = _last_state
                        residence_time = -1

                        if current_region == state2:
                            forward_changes.append(stepnum)

                        else:
                            backward_changes.append(stepnum)

            # Residing in state
            else:
                pass

        # In transition region
        else:
            # From a quick exit below `min_residence`
            #   - reset the residence counter
            if _last_state != last_state:
                residence_time = -1
                _last_state = last_state

            # From well-established `last_state`
            else:
                pass

    return (forward_changes, backward_changes)
