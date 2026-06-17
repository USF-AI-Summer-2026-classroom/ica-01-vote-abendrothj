from collections import deque


class Voter:

    def __init__(self, id, leaning):
        self.id = id
        self.leaning = leaning
        # Queue of candidates ordered by voter preference (left = top choice).
        self.ranked_choices = deque()

    def rank_candidates(self, candidates):
        ordered_candidates = sorted(
            candidates,
            key=lambda candidate: abs(candidate.get_leaning() - self.leaning)
        )
        self.ranked_choices = deque(ordered_candidates)

    def get_vote(self, active_candidate_names):
        while self.ranked_choices and self.ranked_choices[0].get_name() not in active_candidate_names:
            self.ranked_choices.popleft()

        if not self.ranked_choices:
            return None

        return self.ranked_choices[0]

    def __repr__(self):
        return (
            f"Voter with ID={self.id}, "
            f"leaning: {self.leaning:.3f}"
        )

