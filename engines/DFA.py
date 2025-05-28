from collections import deque

# ===============================================================
# 🎲 DETERMINISTIC FINITE AUTOMATA (DFA) CLASS  
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