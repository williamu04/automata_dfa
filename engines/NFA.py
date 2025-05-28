from collections import defaultdict

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