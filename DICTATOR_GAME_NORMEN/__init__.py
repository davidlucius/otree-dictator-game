from otree.api import *
from settings import POINTS_CUSTOM_NAME
from random import randint
from _utils.payoff import (
    get_endowment_in_points,
    get_points_per_real_world_currency_unit
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
# hier haben wir den Multiplier (2) eingefügt, mit dem die abgegebene Anzahl Taler multipliziert wird.
# players_per_group = None weil alle zusammen in einer Gruppe spielen
class Constants(BaseConstants):
    name_in_url = 'variant_1'
    players_per_group = None
    num_rounds = 3
    multiplier = 2

    # Hier können die Info-Texte bearbeitet werden:
    # Dazu bitte einfach den Text hinter der entsprechenden Entscheidungsnummer austauschen.
    info_texts = {
        1: 'Hallo',
        2: '<div class="fw-bold mb-1">Nun sind Sie dazu verpflichtet mindestens 5 Taler abzugeben. '
           'Das bedeutet, dass Sie maximal 5 Ihrer Taler behalten dürfen. </div>'
           'Sollten Sie trotz der Pflicht weniger als '
           '5 Taler abgeben, so ergibt sich folgende Konsequenz: ' 
           'Unter allen Personen, die weniger als 5 Taler abgeben, '
           'wird zufällig eine Person bestimmt, die ihre gesamten behaltenen Taler dieser Spielrunde verliert. '
           'Diese Person erhält allerdings trotzdem ihren Anteil der gesammelten Taler von der Gemeinschaft.</div>',
        3: '<div class="fw-bold mb-1">Die Pflicht, 5 Taler abzugeben, ist nun aufgehoben </div>',
        4: '4 …',
        5: '5Info-Text Pflicht …'
    }


class Subsession(BaseSubsession):
    is_winning_dec = models.BooleanField(initial=False)

    @property
    def num_players(self):
        return len(self.get_players())


def creating_session(subsession):
    if subsession.round_number == 1:
        subsession.session.winning_dec = randint(1, Constants.num_rounds)
    if subsession.round_number == subsession.session.winning_dec:
        subsession.is_winning_dec = True
    subsession.group_randomly()


class Group(BaseGroup):
    total_contribution = models.FloatField()
    total_profit = models.IntegerField()
    individual_share = models.FloatField()


class Player(BasePlayer):

    taler = models.IntegerField(
        label='',
        min=0
    )

    contribution = models.IntegerField()

    freeriding = models.BooleanField()

    loosing = models.BooleanField()

    q3 = models.StringField(
        label='Sind Sie geimpft?',
        choices=[
            'Ja',
            'Nein',
        ],
        widget=widgets.RadioSelect
    )

    q4 = models.StringField(
        label='Hatten Sie bereits Covid19?',
        choices=[
            'Ja',
            'Nein',
        ],
        widget=widgets.RadioSelect
    )

    q5 = models.IntegerField(
        label='Die Impfung ist die Rettung aus der Pandemie.',
        choices=[
            (1, 'Stimme überhaupt nicht zu'),
            (2, 'Stimme eher nicht zu'),
            (3, 'Stimme weder zu noch stimme ich nicht zu'),
            (4, 'Stimme eher zu'),
            (5, 'Stimme voll und ganz zu'),
        ],
    )

    q6 = models.IntegerField(
        label='2G (Geimpft oder Genesen) in geschlossenen Räumlichkeiten für Freizeitvergnügen halte ich für sinnvoll '
              '(z.B. Restaurant, Kino, Konzerte).',
        choices=[
         (1, 'Stimme überhaupt nicht zu'),
         (2, 'Stimme eher nicht zu'),
         (3, 'Stimme weder zu noch stimme ich nicht zu'),
         (4, 'Stimme eher zu'),
         (5, 'Stimme voll und ganz zu'),
        ],
    )

    q7 = models.IntegerField(
        label='In maskenpflichtigen Bereichen trage ich stets meine Maske.',
        choices=[
            (1, 'Stimme überhaupt nicht zu'),
            (2, 'Stimme eher nicht zu'),
            (3, 'Stimme weder zu noch stimme ich nicht zu'),
            (4, 'Stimme eher zu'),
            (5, 'Stimme voll und ganz zu'),
        ],
    )

    q8 = models.IntegerField(
        label='Ich trage meine Maske stets ordnungsgemäß. Ich bedecke sowohl meinen Mund als auch meine Nase.',
        choices=[
            (1, 'Stimme überhaupt nicht zu'),
            (2, 'Stimme eher nicht zu'),
            (3, 'Stimme weder zu noch stimme ich nicht zu'),
            (4, 'Stimme eher zu'),
            (5, 'Stimme voll und ganz zu'),
        ],
    )

    q9 = models.IntegerField(
        label='Händeschütteln und Umarmungen vermeide ich.',
        choices=[
            (1, 'Stimme überhaupt nicht zu'),
            (2, 'Stimme eher nicht zu'),
            (3, 'Stimme weder zu noch stimme ich nicht zu'),
            (4, 'Stimme eher zu'),
            (5, 'Stimme voll und ganz zu'),
        ],
    )

    q10 = models.IntegerField(
        label='Ich halte Abstand zu meinen Mitmenschen (wenn möglich).',
        choices=[
            (1, 'Stimme überhaupt nicht zu'),
            (2, 'Stimme eher nicht zu'),
            (3, 'Stimme weder zu noch stimme ich nicht zu'),
            (4, 'Stimme eher zu'),
            (5, 'Stimme voll und ganz zu'),
        ],
    )

    q11 = models.IntegerField(
        label='Mein Verhalten während der Covid19-Pandemie empfinde ich als gewissenhaft.',
        choices=[
            (1, 'Stimme überhaupt nicht zu'),
            (2, 'Stimme eher nicht zu'),
            (3, 'Stimme weder zu noch stimme ich nicht zu'),
            (4, 'Stimme eher zu'),
            (5, 'Stimme voll und ganz zu'),
        ],
    )

    q12 = models.StringField(
        label='Bitte wählen Sie Ihr Geschlecht',
        choices=[
            'Männlich',
            'Weiblich',
            'Divers',
        ],
        widget=widgets.RadioSelectHorizontal
    )

    q13 = models.IntegerField(
        label='Wie alt sind Sie?'
    )

    q14 = models.StringField(
        label='Studieren Sie?',
        choices=[
            'Ja',
            'Nein',
        ],
        widget=widgets.RadioSelectHorizontal
    )

    q15 = models.StringField(
        label='An welcher Fakultät studieren Sie?',
        choices=[
            'Rechtswissenschaften',
            'Wirtschafts- und Sozialwissenschaften',
            'Erziehungswissenschaften',
            'Geisteswissenschaften',
            'Psychologie und Bewegungswissenschaften',
            'Betriebswirtschaft',
            'Sonstige',
            'Ich studiere nicht',
        ],
    )


def taler_max(player):
    return get_endowment_in_points(player)


# ----------------------------------------------------------------------------------------------------------------------
# PAGES
# ----------------------------------------------------------------------------------------------------------------------
# hier haben wir timeouts eingebaut, um die Zeit pro Seite zu begrenzen
class Intro(Page):
    timeout_seconds = 120

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            endowment_in_points=c(get_endowment_in_points(player)),
            points_per_real_world_currency_unit=c(get_points_per_real_world_currency_unit(player)),
        )


class DecisionInfo(Page):
    timeout_seconds = 60

    @staticmethod
    def is_displayed(player):
        return player.round_number >= 2

    @staticmethod
    def vars_for_template(player):
        return dict(
            endowment_in_points=c(get_endowment_in_points(player)),
            points_per_real_world_currency_unit=c(get_points_per_real_world_currency_unit(player))
        )


class DecisionNeu(Page):
    timeout_seconds = 120

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
            num_other_players=player.subsession.num_players - 1,
        )

    @staticmethod
    def js_vars(player):
        return dict(
            endowment_in_points=get_endowment_in_points(player)
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.contribution = get_endowment_in_points(player)-player.taler
        if player.round_number == 2:
            if player.contribution < 5:
                player.freeriding = True
            else:
                player.freeriding = False


class Questionnaire(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = [
        'q3',
        'q4',
    ]

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds


class Questionnaire2(Page):
    timeout_seconds = 180
    form_model = 'player'
    form_fields = [
        'q5',
        'q6',
        'q7',
        'q8',
        'q9',
        'q10',
        'q11',
    ]

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds


class Questionnaire3(Page):
    timeout_seconds = 60
    form_model = 'player'
    form_fields = [
        'q12',
        'q13',
        'q14',
        'q15',
    ]

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds


class Info(Page):
    form_model = 'player'

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
            points_in_round_1=[player.in_round(1).taler],
            points_in_round_2=[player.in_round(2).taler],
            points_in_round_3=[player.in_round(3).taler],
            contrib_in_round_1=[player.in_round(1).contribution],
            contrib_in_round_2=[player.in_round(2).contribution],
            contrib_in_round_3=[player.in_round(3).contribution],
            groupcontrib_in_round_1=[player.group.in_round(1).total_profit],
            groupcontrib_in_round_2=[player.group.in_round(2).total_profit],
            groupcontrib_in_round_3=[player.group.in_round(3).total_profit],
            taler_in_winning_dec=c(player.in_round(player.session.winning_dec).taler),
            share_in_winning_dec=c(player.group.in_round(player.group.session.winning_dec).individual_share),
            points_in_winning_dec=c(player.in_round(player.session.winning_dec).taler + player.group.in_round(
                player.group.session.winning_dec).individual_share),
            freerider=c(player.in_round(2).freeriding),
            loosing_money=c(player.in_round(2).loosing),
        )


class RoundWaitPage(WaitPage):
    body_text = 'Bitte warten Sie, bis alle Entscheidungen getroffen wurden.'

    @staticmethod
    def after_all_players_arrive(group: Group):
        total_contribution = 0
        for player in group.get_players():
            total_contribution += player.contribution
        group.total_contribution = total_contribution
        group.total_profit = total_contribution * Constants.multiplier
        group.individual_share = total_contribution * Constants.multiplier / (len(group.get_players()))
        if group.round_number == group.session.winning_dec:
            for p in group.get_players():
                p.payoff = p.taler + p.group.individual_share
        list_of_freeriders = []
        if group.round_number == 2:
            for player in group.get_players():
                if player.freeriding:
                    list_of_freeriders.append(player.id_in_group)
            freerider_id = list_of_freeriders[0]
            for player in group.get_players():
                player.loosing = False
                if player.id_in_group == freerider_id:
                    player.loosing = True
                    player.payoff = 0


# Payment erst ganz am Ende
page_sequence = [
    Intro,
    DecisionInfo,
    DecisionNeu,
    RoundWaitPage,
    Info,
    Questionnaire,
    Questionnaire2,
    Questionnaire3,
    Payment
]
