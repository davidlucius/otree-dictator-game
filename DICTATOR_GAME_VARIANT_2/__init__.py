from otree.api import *
from settings import POINTS_CUSTOM_NAME
from math import ceil
from random import choices
from _utils.payoff import (
    get_endowment_in_points,
    get_points_per_real_world_currency_unit,
    get_payoff
)


c = Currency


doc = """
Dictator Game - Treatment: Variant 2 (risky)
Course: Behavioral Economic Experiments in the Context of the COVID-19 Pandemic

Created by: David Lucius (david.lucius@posteo.de)
"""


# ----------------------------------------------------------------------------------------------------------------------
# MODELS
# ----------------------------------------------------------------------------------------------------------------------

class Constants(BaseConstants):
    name_in_url = 'variant_2'
    players_per_group = 2
    num_rounds = 2
    dictator_role = 'dictator'
    recipient_role = 'recipient'
    amounts = {counter: amount for counter, amount in enumerate(range(10, -1, -2), start=1)}
    probabilities = {counter: probability for counter, probability in enumerate(range(100, -1, -20), start=1)}


def get_options():
    options = zip(Constants.amounts.items(), Constants.probabilities.items())
    return {i: {'amount': amount, 'probability': probability} for (i, amount), (_, probability) in options}


class Subsession(BaseSubsession):

    @property
    def num_players(self):
        return len(self.get_players())

    @property
    def num_dictators(self):
        return int(self.num_players / 2)

    @property
    def num_recipients(self):
        return int(self.num_players / 2)

    @property
    def min_vaccinated_recipients(self):
        return ceil(self.session.config['min_vaccination_coverage'] * self.num_players - self.num_dictators)

    @property
    def num_vaccinated_recipients(self):
        num_vaccinated_recipients = 0
        for p in self.get_players():
            if p.role == 'recipient':
                if p.field_maybe_none('vaccinated'):
                    num_vaccinated_recipients += 1
        return num_vaccinated_recipients

    @property
    def vaccination_coverage_is_reached(self):
        return self.num_vaccinated_recipients >= self.min_vaccinated_recipients


def creating_session(subsession: Subsession):
    subsession.group_randomly(fixed_id_in_group=True)


class Group(BaseGroup):

    appointment = models.IntegerField(
        label='Welchen Termin wählen Sie?',
        choices=[[i, f'Termin {i}'] for i in range(1, len(get_options()) + 1)]
    )


class Player(BasePlayer):
    vaccinated = models.BooleanField()

    # Screen: Questionnaire01
    belief_d_1 = models.StringField(
        label='Was glauben Sie, welchen Termin die anderen Teilnehmer wählen?',
        choices=[f'Termin {i}' for i in range(1, len(get_options()) + 1)]
    )

    # Screen: Questionnaire01
    belief_e_1 = models.StringField(
        label='Was glauben Sie, welchen Termin die anderen Teilnehmer wählen?',
        choices=[f'Termin {i}' for i in range(1, len(get_options()) + 1)]
    )

    # Screen: Questionnaire01
    belief_d_2 = models.StringField(
        label='Was glauben Sie, wie sich die anderen Diktatoren verhalten haben?',
        choices=[
            'Selbstinteressiert',
            'Mittel',
            'Eher großzügig'
        ]
    )

    # Screen: Questionnaire01
    belief_e_2 = models.StringField(
        label='Was glauben Sie, wie sich der Diktator entscheiden wird?',
        choices=[f'Termin {i}' for i in range(1, len(get_options()) + 1)]
    )

    # Screen: Questionnaire02
    age = models.IntegerField(
        label='Wie alt sind Sie?',
        min=18,
        max=99
    )

    # Screen: Questionnaire02
    gender = models.StringField(
        label='Bitte geben Sie Ihr Geschlecht an.',
        choices=[
            'Männlich',
            'Weiblich',
            'Divers'
        ]
    )

    # Screen: Questionnaire02
    real_vaccinated = models.StringField(
        label='Sind Sie bereits gegen Corona geimpft?',
        choices=[
            'Ja',
            'Nein'
        ],
        widget=widgets.RadioSelect
    )

    # Screen: Questionnaire02
    ready_for_booster = models.StringField(
        label='Sind Sie bereit für eine Auffrischungsimpfung?',
        choices=[
            'Ja',
            'Nein'
        ],
        widget=widgets.RadioSelect
    )

    # Screen: Questionnaire02
    reason_self_protection = models.BooleanField(
        label='Eigenschutz',
        widget=widgets.CheckboxInput,
        blank=True)
    reason_environment = models.BooleanField(
        label='Schutz meines persönlichen Umfeldes',
        widget=widgets.CheckboxInput,
        blank=True)
    reason_herd_immunity = models.BooleanField(
        label='Erreichen der Herdenimmunität',
        widget=widgets.CheckboxInput,
        blank=True)
    reason_get_back_liberties = models.BooleanField(
        label='Um Freiheiten zurückzuerhalten',
        widget=widgets.CheckboxInput,
        blank=True)
    reason_pressure = models.BooleanField(
        label='Druck durch soziales Umfeld und Politik',
        widget=widgets.CheckboxInput,
        blank=True)

    # Screen: Questionnaire02
    risk_evaluation = models.StringField(
        label='Wie hoch schätzen Sie Ihr Risiko ein sich in den kommenden 3 Monaten mit Sars-Cov-2 zu infizieren?',
        choices=[
            'Sehr groß',
            'groß',
            'erheblich',
            'mäßig',
            'gering'
        ]
    )


# ----------------------------------------------------------------------------------------------------------------------
# PAGES
# ----------------------------------------------------------------------------------------------------------------------

class Intro(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class DecisionInfo(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            POINTS_CUSTOM_NAME=POINTS_CUSTOM_NAME,
            endowment_in_points=c(get_endowment_in_points(player)),
            points_per_real_world_currency_unit=c(get_points_per_real_world_currency_unit(player)),
            options=get_options(),
            min_vaccination_coverage=int(player.session.config['min_vaccination_coverage'] * 100),
            num_other_dictators=player.subsession.num_dictators - 1,
            failure_payoff=c(player.session.config['failure_payoff_in_points'])
        )


class Decision(Page):
    form_model = 'group'
    form_fields = [
        'appointment'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.role == 'dictator'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            POINTS_CUSTOM_NAME=POINTS_CUSTOM_NAME,
            endowment_in_points=c(get_endowment_in_points(player)),
            options=get_options()
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            options=get_options(),
            endowment_in_points=get_endowment_in_points(player),
            round_number=player.round_number,
            failure_payoff=player.session.config['failure_payoff_in_points']
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        for p in player.group.get_players():
            if p.role == 'dictator':
                p.vaccinated = True
            elif p.role == 'recipient':
                weight_unvaccinated = get_options()[p.group.appointment]['probability']
                p.vaccinated = choices([True, False], [100 - weight_unvaccinated, weight_unvaccinated])[0]
            if p.round_number == 1:
                p.payoff = get_payoff(p, get_options())


class Questionnaire01(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.role == 'dictator':
            return ['belief_d_1', 'belief_d_2']
        if player.role == 'recipient':
            return ['belief_e_1', 'belief_e_2']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class WaitingForPartner(WaitPage):
    body_text = 'Bitte haben Sie Geduld, Ihr Gegenüber hat sich noch nicht entschieden.'

    @staticmethod
    def is_displayed(player):
        return player.role == 'recipient' and player.round_number == 1


class WaitingForAll(WaitPage):
    wait_for_all_groups = True
    body_text = 'Bitte warten Sie, bis alle Entscheidungen getroffen wurden.'

    @staticmethod
    def is_displayed(player):
        return player.round_number == 2

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        for p in subsession.get_players():
            p.payoff = get_payoff(p, get_options())


class Result(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            partner=player.get_others_in_group()[0],
            endowment_in_points=c(get_endowment_in_points(player)),
            vaccination_coverage_is_reached=player.subsession.vaccination_coverage_is_reached
        )


class Questionnaire02(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'real_vaccinated',
        'ready_for_booster',
        'reason_self_protection',
        'reason_environment',
        'reason_herd_immunity',
        'reason_get_back_liberties',
        'reason_pressure',
        'risk_evaluation'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds


class Payment(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            payoffs=[player.in_round(i + 1).payoff for i in range(Constants.num_rounds)]
        )


page_sequence = [
    Intro,
    DecisionInfo,
    Decision,
    Questionnaire01,
    WaitingForPartner,
    WaitingForAll,
    Result,
    Questionnaire02,
    Payment
]
