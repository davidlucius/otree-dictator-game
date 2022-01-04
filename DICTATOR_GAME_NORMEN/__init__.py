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
Dictator Game - Treatment: Variant 1
Course: Behavioral Economic Experiments in the Context of the COVID-19 Pandemic

Created by: David Lucius (david.lucius@posteo.de)
"""


# ----------------------------------------------------------------------------------------------------------------------
# MODELS
# ----------------------------------------------------------------------------------------------------------------------

class Constants(BaseConstants):
    name_in_url = 'variant_1'
    players_per_group = 2
    num_rounds = 5

    # Hier können die Info-Texte bearbeitet werden:
    # Dazu bitte einfach den Text hinter der entsprechenden Entscheidungsnummer austauschen.
    info_texts = {
        2: 'Info-Text Pflicht …',
        3: 'Info-Text Pflicht …',
        4: 'Info-Text Pflicht …',
        5: 'Info-Text Pflicht …'
    }


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
            points_per_real_world_currency_unit=c(get_points_per_real_world_currency_unit(player))
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
            points_per_real_world_currency_unit=c(get_points_per_real_world_currency_unit(player))
        )

    @staticmethod
    def js_vars(player):
        return dict(
            endowment_in_points=get_endowment_in_points(player)
        )


class Questionnaire(Page):
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


class WaitingForPartner(WaitPage):
    body_text = 'Bitte warten Sie, bis Ihr:e Partner:in bereit ist.'

    @staticmethod
    def after_all_players_arrive(group):
        if group.round_number == group.session.winning_dec:
            for p in group.get_players():
                p.payoff = p.taler + get_points_from_partner_in_winning_dec(p)


page_sequence = [
    Intro,
    DecisionInfo,
    Decision,
    WaitingForPartner,
    Questionnaire,
    Payment
]
