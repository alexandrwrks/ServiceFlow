from database.enum import OrderStatusType as S

ALLOWED_TRANSITIONS = {
    S.NEW: frozenset({S.ASSIGNED, S.CANCELLED}),
    S.ASSIGNED: frozenset({S.IN_PROGRESS, S.CANCELLED}),
    S.IN_PROGRESS: frozenset({S.COMPLETED, S.CANCELLED}),
    S.COMPLETED: frozenset({S.INVOICED}),
    S.INVOICED: frozenset({S.PAID}),
    S.PAID: frozenset({S.CLOSED}),
    S.CLOSED: frozenset(),
    S.CANCELLED: frozenset(),
}

WORKER_TARGET_STATUSES = {
    S.IN_PROGRESS,
    S.COMPLETED
}