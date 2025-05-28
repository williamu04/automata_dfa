from engines.NFA import NFA

def regex_to_nfa(regex):
    """
    🔤 Convert Regular Expression to NFA using Thompson's Construction
    
    Supported operations:
    - Basic symbols: a, b, c, ...
    - Union: |
    - Kleene star: *
    - Grouping: ()
    
    Args:
        regex: Regular expression string
        
    Returns:
        NFA: Equivalent non-deterministic finite automaton
    """
    state_counter = 0
    
    def get_new_state():
        nonlocal state_counter
        state = f"q{state_counter}"
        state_counter += 1
        return state
    
    def char_nfa(c):
        """Create NFA for a single character"""
        nfa = NFA()
        start = get_new_state()
        end = get_new_state()
        
        nfa.start_state = start
        nfa.accept_states = {end}
        nfa.add_transition(start, c, end)
        
        return nfa
    
    def union_nfa(nfa1, nfa2):
        """Create NFA for union of two NFAs"""
        result = NFA()
        start = get_new_state()
        end = get_new_state()
        
        result.start_state = start
        result.accept_states = {end}
        
        # Connect start to both NFAs
        result.add_transition(start, "", nfa1.start_state)
        result.add_transition(start, "", nfa2.start_state)
        
        # Connect both NFAs to end
        for state in nfa1.accept_states:
            result.add_transition(state, "", end)
        for state in nfa2.accept_states:
            result.add_transition(state, "", end)
            
        # Copy all transitions
        for src in nfa1.transitions:
            for symbol, destinations in nfa1.transitions[src].items():
                for dest in destinations:
                    result.add_transition(src, symbol, dest)
                    
        for src in nfa2.transitions:
            for symbol, destinations in nfa2.transitions[src].items():
                for dest in destinations:
                    result.add_transition(src, symbol, dest)
        
        return result
    
    def concat_nfa(nfa1, nfa2):
        """Create NFA for concatenation of two NFAs"""
        result = NFA()
        result.start_state = nfa1.start_state
        result.accept_states = nfa2.accept_states
        
        # Copy all transitions from nfa1
        for src in nfa1.transitions:
            for symbol, destinations in nfa1.transitions[src].items():
                for dest in destinations:
                    result.add_transition(src, symbol, dest)
        
        # Copy all transitions from nfa2
        for src in nfa2.transitions:
            for symbol, destinations in nfa2.transitions[src].items():
                for dest in destinations:
                    result.add_transition(src, symbol, dest)
        
        # Connect accept states of nfa1 to start state of nfa2
        for state in nfa1.accept_states:
            result.add_transition(state, "", nfa2.start_state)
        
        return result
    
    def star_nfa(nfa):
        """Create NFA for Kleene star of an NFA"""
        result = NFA()
        start = get_new_state()
        end = get_new_state()
        
        result.start_state = start
        result.accept_states = {end}
        
        # Connect start to end (empty string case)
        result.add_transition(start, "", end)
        
        # Connect start to original NFA
        result.add_transition(start, "", nfa.start_state)
        
        # Copy all transitions from original NFA
        for src in nfa.transitions:
            for symbol, destinations in nfa.transitions[src].items():
                for dest in destinations:
                    result.add_transition(src, symbol, dest)
        
        # Connect accept states back to start state of original NFA
        for state in nfa.accept_states:
            result.add_transition(state, "", nfa.start_state)
            # Connect accept states to end
            result.add_transition(state, "", end)
        
        return result
    
    def parse(regex_str):
        """Parse regex recursively using Thompson's construction"""
        if not regex_str:
            # Empty regex
            nfa = NFA()
            start = get_new_state()
            nfa.start_state = start
            nfa.accept_states = {start}
            return nfa
            
        # Try to find a union operation at the top level
        parenthesis_depth = 0
        for i in range(len(regex_str)):
            if regex_str[i] == '(':
                parenthesis_depth += 1
            elif regex_str[i] == ')':
                parenthesis_depth -= 1
            elif regex_str[i] == '|' and parenthesis_depth == 0:
                # Found a top-level union
                left = parse(regex_str[:i])
                right = parse(regex_str[i+1:])
                return union_nfa(left, right)
        
        # No top-level union, try to parse as concatenation
        if len(regex_str) > 1:
            # Check the first character and if it's followed by a star
            if len(regex_str) > 1 and regex_str[1] == '*' and regex_str[0] != '(':
                # Single char followed by star
                char_nfa_obj = char_nfa(regex_str[0])
                star_nfa_obj = star_nfa(char_nfa_obj)
                
                if len(regex_str) > 2:
                    # More to parse after the star
                    rest = parse(regex_str[2:])
                    return concat_nfa(star_nfa_obj, rest)
                else:
                    return star_nfa_obj
            
            # Check if it starts with a group
            elif regex_str[0] == '(':
                # Find the matching closing parenthesis
                depth = 1
                closing_index = 1
                while depth > 0 and closing_index < len(regex_str):
                    if regex_str[closing_index] == '(':
                        depth += 1
                    elif regex_str[closing_index] == ')':
                        depth -= 1
                    closing_index += 1
                
                if depth != 0:
                    raise ValueError(f"Unmatched parenthesis in regex: {regex_str}")
                
                # Parse the group
                group_content = regex_str[1:closing_index-1]
                group_nfa = parse(group_content)
                
                # Check if group is followed by star
                if closing_index < len(regex_str) and regex_str[closing_index] == '*':
                    group_nfa = star_nfa(group_nfa)
                    closing_index += 1
                
                # If there's more after the group, concatenate
                if closing_index < len(regex_str):
                    rest = parse(regex_str[closing_index:])
                    return concat_nfa(group_nfa, rest)
                else:
                    return group_nfa
            
            else:
                # Simple concatenation of first char and the rest
                first = char_nfa(regex_str[0])
                rest = parse(regex_str[1:])
                return concat_nfa(first, rest)
        
        # Single character
        return char_nfa(regex_str[0])
    
    try:
        return parse(regex)
    except Exception as e:
        raise ValueError(f"Failed to parse regex: {str(e)}")

