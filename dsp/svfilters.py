from signalflow import SVFilter


class SVFilterNode:
    def __init__(self, filter_type="low_pass", cutoff=1000.0, resonance=0.5):
        self.cutoff = cutoff
        self.resonance = resonance
        self.filter_type = filter_type

    def create_node(self, input_signal):
        return SVFilter(
            input=input_signal,
            filter_type=self.filter_type,
            cutoff=self.cutoff,
            resonance=self.resonance,
        )

    # --- Parameter setters ---
    def set_cutoff(self, cutoff: float):
        self.cutoff=cutoff

    def set_resonance(self, resonance: float):
        self.resonance=resonance

    def set_filter_type(self, filter_type: str):
        self.filter_type=filter_type
