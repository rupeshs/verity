MINIMUM_MAX_SCORE = 0.2


def select_by_score_gap(
    reranked,
    gap_threshold=0.3,
    min_docs=2,
):
    if not reranked:
        return []

    selected = [reranked[0]]

    for i in range(1, len(reranked)):
        prev_score = reranked[i - 1][1]
        curr_score = reranked[i][1]

        if prev_score - curr_score < gap_threshold:
            selected.append(reranked[i])
        else:
            break

    if len(selected) < min_docs:
        selected = reranked[:min_docs]
    return selected


def should_abort_due_to_low_score(reranked: list) -> bool:
    if not reranked:
        return True
    max_score = max(reranked, key=lambda x: x[1])[1]
    return max_score < MINIMUM_MAX_SCORE
