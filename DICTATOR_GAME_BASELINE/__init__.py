from otree.api import *
from settings import POINTS_CUSTOM_NAME
from random import randint
from _utils.payoff import (
    get_endowment_in_points,
    get_points_per_real_world_currency_unit,
    get_points_from_partner_in_winning_dec
)


c = Currency


doc = """
Dictator Game - Treatment: Baseline
Course: Behavioral Economic Experiments in the Context of the COVID-19 Pandemic

Created by: David Lucius (david.lucius@posteo.de)
"""


# ----------------------------------------------------------------------------------------------------------------------
# MODELS
# ----------------------------------------------------------------------------------------------------------------------

class Constants(BaseConstants):
    name_in_url = 'baseline'
    players_per_group = 2
    num_rounds = 3


class Subsession(BaseSubsession):
    is_winning_dec = models.BooleanField(initial=False)


def creating_session(subsession):
    if subsession.round_number == 1:
        subsession.session.winning_dec = randint(1, Constants.num_rounds)
    if subsession.round_number == subsession.session.winning_dec:
        subsession.is_winning_dec = True
    subsession.group_randomly()


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    q1 = models.StringField(
        label='Wie geht es Ihnen?',
        choices=[
            'gar nicht gut',
            'nicht gut',
            'okay',
            'gut',
            'sehr gut'
        ],
        widget=widgets.RadioSelect
    )

    q2 = models.StringField(
        label='Wie ist das Wetter?',
        choices=[
            'gar nicht gut',
            'nicht gut',
            'okay',
            'gut',
            'sehr gut'
        ],
        widget=widgets.RadioSelect
    )

    taler = models.IntegerField(
        label='',
        min=0
    )

    q3 = models.StringField(
        label='Text Frage 1',
        choices=[
            'Option 1',
            'Option 2',
            'Option 3'
        ]
    )

    q4 = models.IntegerField(
        label='Text Frage 2'
    )


def taler_max(player):
    return get_endowment_in_points(player)


# ----------------------------------------------------------------------------------------------------------------------
# PAGES
# ----------------------------------------------------------------------------------------------------------------------

class Intro(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class IntroDecision01(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            endowment_in_points=c(get_endowment_in_points(player)),
            points_per_real_world_currency_unit=c(get_points_per_real_world_currency_unit(player))
        )


class DecisionInfo(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number >= 2

    @staticmethod
    def vars_for_template(player):
        return dict(
            endowment_in_points=c(get_endowment_in_points(player)),
            points_per_real_world_currency_unit=c(get_points_per_real_world_currency_unit(player)),
            partners_answer_to_q1=player.get_others_in_group()[0].participant.q1 if player.round_number == 2 else None,
            partners_answer_to_q2=player.get_others_in_group()[0].participant.q2 if player.round_number == 3 else None
        )


class Decision(Page):
    form_model = 'player'
    form_fields = [
        'taler'
    ]

    @staticmethod
    def vars_for_template(player):
        return dict(
            POINTS_CUSTOM_NAME=POINTS_CUSTOM_NAME,
            endowment_in_points=c(get_endowment_in_points(player)),
            points_per_real_world_currency_unit=c(get_points_per_real_world_currency_unit(player)),
            partners_answer_to_q1=player.get_others_in_group()[0].participant.q1 if player.round_number == 2 else None,
            partners_answer_to_q2=player.get_others_in_group()[0].participant.q2 if player.round_number == 3 else None
        )

    @staticmethod
    def js_vars(player):
        return dict(
            endowment_in_points=get_endowment_in_points(player)
        )


class Questionnaire01(Page):
    form_model = 'player'
    form_fields = [
        'q1',
        'q2'
    ]

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.q1 = player.q1
        player.participant.q2 = player.q2


class Questionnaire02(Page):
    form_model = 'player'
    form_fields = [
        'q3',
        'q4'
    ]

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds


class Payment(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player):
        return dict(
            POINTS_CUSTOM_NAME=POINTS_CUSTOM_NAME,
            points_in_rounds=[player.in_round(r).taler for r in range(1, Constants.num_rounds + 1)],
            points_in_winning_dec=c(player.in_round(player.session.winning_dec).taler),
            points_from_partner_in_winning_dec=c(get_points_from_partner_in_winning_dec(player))
        )


class WaitingForPartner01(WaitPage):
    body_text = 'Bitte warten Sie, bis Ihr:e Partner:in bereit ist.'

    @staticmethod
    def is_displayed(player):
        return player.round_number >= 2


class WaitingForPartner02(WaitPage):
    body_text = 'Bitte warten Sie, bis Ihr:e Partner:in bereit ist.'

    @staticmethod
    def after_all_players_arrive(group):
        if group.round_number == group.session.winning_dec:
            for p in group.get_players():
                p.payoff = p.taler + get_points_from_partner_in_winning_dec(p)


page_sequence = [
    Intro,
    Questionnaire01,
    IntroDecision01,
    WaitingForPartner01,
    DecisionInfo,
    Decision,
    WaitingForPartner02,
    Payment,
    Questionnaire02
]
