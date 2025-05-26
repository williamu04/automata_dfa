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
    state_id = [0]

    def new_state():
        sid = "q" + str(state_id[0])
        state_id[0] += 1
        return sid

    def parse_regex(expr, pos=0):
        nfa = NFA()
        start = new_state()
        end = new_state()
        nfa.start_state = start
        nfa.accept_states = {end}
        current_states = {start}

        while pos < len(expr):
            char = expr[pos]
            if char in {"a", "b"}:
                # Handle single character
                dest = new_state()
                for s in current_states:
                    nfa.add_transition(s, char, dest)
                current_states = {dest}
                pos += 1
            elif char == "(":
                # Find matching parenthesis
                depth = 1
                sub_pos = pos + 1
                while sub_pos < len(expr) and depth > 0:
                    if expr[sub_pos] == "(": depth += 1
                    elif expr[sub_pos] == ")": depth -= 1
                    sub_pos += 1
                if depth != 0:
                    raise ValueError("Unmatched parenthesis")
                # Parse subexpression
                sub_nfa = parse_regex(expr[pos + 1:sub_pos - 1])[0]
                for s in current_states:
                    nfa.add_transition(s, "", sub_nfa.start_state)
                nfa.transitions.update(sub_nfa.transitions)
                current_states = sub_nfa.accept_states
                pos = sub_pos
            elif char == "*":
                # Apply Kleene star to previous NFA
                if not current_states:
                    raise ValueError("Invalid Kleene star: no preceding expression")
                prev_start = nfa.start_state
                prev_end = new_state()
                nfa.accept_states = {prev_end}
                for s in current_states:
                    nfa.add_transition(s, "", prev_start)
                    nfa.add_transition(s, "", prev_end)
                nfa.add_transition(prev_start, "", prev_end)
                current_states = {prev_end}
                pos += 1
            elif char == "|":
                # Handle union
                right_nfa, new_pos = parse_regex(expr, pos + 1)
                nfa.transitions.update(right_nfa.transitions)
                nfa.add_transition(nfa.start_state, "", right_nfa.start_state)
                for s in right_nfa.accept_states:
                    nfa.add_transition(s, "", end)
                nfa.accept_states = {end}
                return nfa, new_pos
            else:
                raise ValueError(f"Invalid character at position {pos}: {char}")
        nfa.accept_states = current_states
        return nfa, pos

    try:
        nfa, _ = parse_regex(regex)
        if not nfa.start_state:
            raise ValueError("Invalid regex: no start state defined")        
        return nfa
    except ValueError as e:
        raise ValueError(f"Regex parsing error: {str(e)}")

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