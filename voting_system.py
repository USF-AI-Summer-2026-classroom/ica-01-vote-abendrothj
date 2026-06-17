from candidate import Candidate
from voter import Voter

import random


class VotingSystem:
    def __init__(self):
        self.candidates = []
        self.voters = []

    def generate_candidates(self, count):
        names = ['Aang', 'Katara', 'Sokka', 'Zuko', 'Iroh', 'Appa', 'Momo', 'Toph', 'Azula', 'Suki', 'Ozai', 'Mai', 'Ty']
        self.candidates = [
            Candidate(
                name=names[i],
                leaning=random.uniform(-1.0, 1.0)
            )
            for i in range(count)
        ]

    def generate_voters(self, count):
        self.voters = [
            Voter(
                id=i + 1,
                leaning=random.uniform(-1.0, 1.0)
            )
            for i in range(count)
        ]

    def rank_voters(self):
        for voter in self.voters:
            voter.rank_candidates(self.candidates)

    def run_ranked_choice_election(self):
        if not self.candidates or not self.voters:
            raise ValueError("Candidates and voters must be generated before running an election.")

        self.rank_voters()
        active_candidates = {
            candidate.get_name(): candidate
            for candidate in self.candidates
        }
        round_number = 1

        while len(active_candidates) > 1:
            active_candidate_names = set(active_candidates)
            votes = {name: 0 for name in active_candidates}

            for voter in self.voters:
                chosen_candidate = voter.get_vote(active_candidate_names)
                if chosen_candidate is not None:
                    votes[chosen_candidate.get_name()] += 1

            total_votes = sum(votes.values())

            print(f"\nRound {round_number}")
            for name, vote_count in sorted(
                votes.items(),
                key=lambda item: item[1],
                reverse=True
            ):
                percentage = (vote_count / total_votes * 100) if total_votes else 0
                print(f"{name}: {percentage:.2f}% ({vote_count} votes)")

            winner_name, winner_votes = max(votes.items(), key=lambda item: item[1])
            if winner_votes > total_votes / 2:
                print(
                    f"\nWinner: {winner_name} "
                    f"with {winner_votes / total_votes * 100:.2f}% of the vote."
                )
                return active_candidates[winner_name]

            eliminated_name = min(votes.items(), key=lambda item: (item[1], item[0]))[0]
            print(f"Eliminated: {eliminated_name}")
            del active_candidates[eliminated_name]
            round_number += 1

        final_name = next(iter(active_candidates))
        print(f"\nWinner: {final_name} by default (last remaining candidate).")
        return active_candidates[final_name]

if __name__ == "__main__":
    voting_system = VotingSystem()

    voting_system.generate_candidates(5)
    voting_system.generate_voters(100)

    print("Candidates:")
    for candidate in voting_system.candidates:
        print(candidate)

    voting_system.run_ranked_choice_election()
