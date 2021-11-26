from os import environ

SESSION_CONFIGS = [
    dict(
        name='dictator_game_baseline',
        display_name=f'Dictator Game - Treatment: Baseline',
        app_sequence=['DICTATOR_GAME_BASELINE'],
        num_demo_participants=4,
        endowment_in_real_world_currency=3
    ),
    dict(
        name='dictator_game_variant_1',
        display_name=f'Dictator Game - Treatment: Variant 1',
        app_sequence=['DICTATOR_GAME_VARIANT_1'],
        num_demo_participants=6,
        endowment_in_real_world_currency=3
    ),
    dict(
        name='dictator_game_variant_2',
        display_name=f'Dictator Game - Treatment: Variant 2 (risky)',
        app_sequence=['DICTATOR_GAME_VARIANT_2'],
        num_demo_participants=6,
        endowment_in_real_world_currency=0.5,
        min_vaccination_coverage=0.85,
        failure_payoff_in_points=5
    )
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.05,
    participation_fee=0.00,
    doc=""
)

PARTICIPANT_FIELDS = [
    'q1',
    'q2'
]
SESSION_FIELDS = [
    'winning_dec'
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'Taler'

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4943619871704'
