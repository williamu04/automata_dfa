#!/usr/bin/env python3
"""
🤖 AUTOMATA THEORY TOOLKIT - CORE MODULES 🤖
================================================================
📚 Theory of Languages and Automata - Semester 4
🎓 Computer Science Department
✨ Interactive implementation of DFA, NFA, and Regex operations

🔧 Core Features:
   • Deterministic Finite Automata (DFA) simulation
   • DFA minimization using Hopcroft's algorithm  
   • DFA equivalence checking
   • Regular Expression to NFA conversion
   • NFA simulation with epsilon transitions

👥 Authors: [Team of 5 Amazing Developers]
📅 Created: 2025
🚀 Built with Python & Mathematical Precision

================================================================
"""

from collections import defaultdict, deque

# ===============================================================
# 🤖 DETERMINISTIC FINITE AUTOMATA (DFA) CLASS
# ===============================================================
class DFA:
    """
    🎯 Deterministic Finite Automaton Implementation
    
    A DFA is a 5-tuple (Q, Σ, δ, q0, F) where:
    - Q: finite set of states
    - Σ: finite alphabet 
    - δ: transition function Q × Σ → Q
    - q0: initial state
    - F: set of accept states
    """
    
    def __init__(self, states, alphabet, start_state, accept_states, transitions):
        """
        🔧 Initialize DFA with given parameters
        
        Args:
            states: List of state names
            alphabet: List of input symbols
            start_state: Initial state name
            accept_states: List of accepting state names  
            transitions: Dict mapping (state, symbol) to next state
        """
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.transitions = transitions  # dict[state][symbol] = state

    def simulate(self, input_str):
        """
        🔄 Simulate DFA execution on input string
        
        Args:
            input_str: String to process
            
        Returns:
            bool: True if string is accepted, False otherwise
        """
        current = self.start_state
        for symbol in input_str:
            if symbol not in self.alphabet:
                return False
            current = self.transitions.get(current, {}).get(symbol)
            if current is None:
                return False
        return current in self.accept_states

    def minimize(self):
        """
        ⚡ Minimize DFA using Hopcroft's Algorithm
        
        Returns:
            DFA: Minimized equivalent DFA
        """
        # Hopcroft's Algorithm - O(n log n) complexity
        partition = [self.accept_states, self.states - self.accept_states]
        waiting = deque(partition)

        while waiting:
            A = waiting.popleft()
            for c in self.alphabet:
                X = set(s for s in self.states if self.transitions.get(s, {}).get(c) in A)
                for Y in partition[:]:
                    inter = X & Y
                    diff = Y - X
                    if inter and diff:
                        partition.remove(Y)
                        partition.extend([inter, diff])
                        if Y in waiting:
                            waiting.remove(Y)
                            waiting.extend([inter, diff])
                        else:
                            waiting.append(inter if len(inter) <= len(diff) else diff)

        new_states = ["S" + str(i) for i in range(len(partition))]
        state_map = {}
        for i, group in enumerate(partition):
            for state in group:
                state_map[state] = new_states[i]

        new_transitions = {}
        for state in self.states:
            new_state = state_map[state]
            if new_state not in new_transitions:
                new_transitions[new_state] = {}
            for c in self.alphabet:
                dest = self.transitions.get(state, {}).get(c)
                if dest:
                    new_transitions[new_state][c] = state_map[dest]
        new_start = state_map[self.start_state]
        new_accept = {state_map[s] for s in self.accept_states}
        
        return DFA(new_states, self.alphabet, new_start, new_accept, new_transitions)

    def is_equivalent(self, other):
        """
        ⚖️ Check if this DFA is equivalent to another DFA
        
        Two DFAs are equivalent if they accept the same language.
        Uses BFS to explore the product automaton.
        
        Args:
            other: Another DFA to compare with
            
        Returns:
            bool: True if DFAs are equivalent, False otherwise
        """
        # Check if symmetric difference is empty using BFS
        visited = set()
        queue = deque([(self.start_state, other.start_state)])

        while queue:
            s1, s2 = queue.popleft()
            if (s1 in self.accept_states) != (s2 in other.accept_states):
                return False
            if (s1, s2) in visited:
                continue
            visited.add((s1, s2))

            for c in self.alphabet:
                t1 = self.transitions.get(s1, {}).get(c)
                t2 = other.transitions.get(s2, {}).get(c)
                if t1 is not None and t2 is not None:
                    queue.append((t1, t2))
        return True

    def get_visual_representation(self):
        """
        🎨 Get visual representation of the DFA for display
        
        Returns:
            dict: Dictionary containing DFA structure for visualization
        """
        # Create visualization structure
        dfa_visualization = {
            "states": list(self.states),
            "alphabet": list(self.alphabet),
            "start_state": self.start_state,
            "accept_states": list(self.accept_states),
            "transitions": self.transitions,
            # Additional metadata for visualization
            "num_states": len(self.states),
            "num_accept_states": len(self.accept_states),
            "is_complete": all(
                symbol in self.transitions.get(state, {})
                for state in self.states
                for symbol in self.alphabet
            )
        }
        
        return dfa_visualization

# ===============================================================
# 🎲 NON-DETERMINISTIC FINITE AUTOMATA (NFA) CLASS  
# ===============================================================
class NFA:
    """
    🎲 Non-deterministic Finite Automaton Implementation
    
    An NFA allows:
    - Multiple transitions for the same input symbol
    - Epsilon (empty string) transitions
    - Non-deterministic choices during computation
    """
    
    def __init__(self):
        """🔧 Initialize empty NFA"""
        self.transitions = defaultdict(lambda: defaultdict(set))
        self.start_state = None
        self.accept_states = set()
        self.states = set()

    def add_transition(self, src, symbol, dest):
        """
        ➕ Add transition to NFA
        
        Args:
            src: Source state
            symbol: Input symbol (or "" for epsilon)
            dest: Destination state
        """
        self.transitions[src][symbol].add(dest)
        self.states.update({src, dest})

    def simulate(self, string):
        """
        🔄 Simulate NFA execution using epsilon closure
        
        Args:
            string: Input string to process
            
        Returns:
            bool: True if string is accepted, False otherwise
        """
        
        def epsilon_closure(states):
            """🔄 Compute epsilon closure of given states"""
            stack = list(states)
            closure = set(states)
            while stack:
                state = stack.pop()
                for next_state in self.transitions[state].get("", []):
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
            return closure

        current_states = epsilon_closure({self.start_state})
        for symbol in string:
            next_states = set()
            for state in current_states:
                next_states.update(self.transitions[state].get(symbol, []))
            current_states = epsilon_closure(next_states)
        return bool(self.accept_states & current_states)
        
    def get_visual_representation(self):
        """
        🎨 Get visual representation of the NFA for display
        
        Returns:
            dict: Dictionary containing NFA structure for visualization
        """
        # Convert the defaultdict to a regular dict for JSON serialization
        transitions_dict = {}
        for src in self.transitions:
            transitions_dict[src] = {}
            for symbol, destinations in self.transitions[src].items():
                # Convert sets to lists for JSON serialization
                transitions_dict[src][symbol] = list(destinations)
        
        # Get all unique symbols used in transitions (alphabet)
        alphabet = set()
        for src in self.transitions:
            for symbol in self.transitions[src]:
                if symbol != "":  # Skip epsilon
                    alphabet.add(symbol)
        
        # Create visualization structure
        nfa_visualization = {
            "states": list(self.states),
            "alphabet": list(alphabet),
            "start_state": self.start_state,
            "accept_states": list(self.accept_states),
            "transitions": transitions_dict,
            # Additional metadata for visualization
            "num_states": len(self.states),
            "has_epsilon": any(symbol == "" for src in self.transitions 
                               for symbol in self.transitions[src])
        }
        
        return nfa_visualization

# ===============================================================
# 🔤 REGULAR EXPRESSION TO NFA CONVERSION
# ===============================================================

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

# ===============================================================
# 🎉 END OF AUTOMATA THEORY TOOLKIT CORE MODULES
# ===============================================================
"""
✨ Thank you for using our Automata Theory Toolkit! ✨

This implementation provides a solid foundation for:
• Understanding finite automata concepts
• Learning computational theory
• Implementing language recognition algorithms

🚀 Built with passion for Computer Science education! 🚀
"""