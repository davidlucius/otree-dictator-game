from os import environ

SESSION_CONFIGS = [
    dict(
        name='dictator_game_info',
        display_name='Dictator Game - Info',
        app_sequence=['DICTATOR_GAME_INFO'],
        num_demo_participants=2,
        endowment_in_real_world_currency=6,
        real_world_currency_per_point=0.1
    ),
    dict(
        name='dictator_game_normen',
        display_name='Dictator Game - Normen',
        app_sequence=['DICTATOR_GAME_NORMEN'],
        num_demo_participants=3,
        endowment_in_real_world_currency=5,
        real_world_currency_per_point=0.50
    ),
    dict(
        name='dictator_game_prio',
        display_name='Dictator Game - Prio',
        app_sequence=['DICTATOR_GAME_PRIO'],
        num_demo_participants=2,
        endowment_in_real_world_currency=2.5,
        real_world_currency_per_point=0.25,
        min_vaccination_coverage=0.85,
        failure_payoff_in_points=5
    )
]

SESSION_CONFIG_DEFAULTS = dict(
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
