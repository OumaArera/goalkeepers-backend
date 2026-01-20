# constants.py

GOALKEEPER_STAT_AVG_FIELDS = [
    # Shot stopping
    "saves",
    "penalty_saved",

    # Handling
    "catches",
    "punches",
    "high_claims",
    "build_up",

    # Distribution
    "throw_outs",
    "goal_kicks",

    # Defensive
    "sweeper_clearances",
    "goals_conceded",
    "error_leading_to_goal",
    "own_goals",
    "total_missed_passes",
    "inaccurate_long_balls",
    "assists",

    # Conceded by type
    "corner_goals_conceded",
    "penalty_goals_conceded",
    "free_kick_goals_conceded",

    # Team play
    "total_passes",
    "passes_per_match",
    "accurate_long_balls",
    "goals_scored",
]


PHYSICAL_HEALTH_AVG_FIELDS = [
    "fitness_level",
    "fatigue_level",
    "muscle_soreness",
    "flexibility",
    "mobility",
    "endurance",
    "injury_risk",
    "recovery_score",
    "pain_level",
    "readiness_score",
]

TRAINING_LOAD_SUM_FIELDS = [
    "total_distance_km",
    "high_speed_distance_km",
    "sprint_distance_km",
    "sprint_count",
    "accelerations",
    "decelerations",
    "player_load",
]

TRAINING_LOAD_AVG_FIELDS = [
    "duration_minutes",
    "intensity_score",
    "max_speed_kmh",
    "avg_heart_rate",
    "max_heart_rate",
]
