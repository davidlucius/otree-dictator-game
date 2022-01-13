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

    qshelfen = models.StringField(
        label='Sie versuchen Anderen zu helfen.',
        choices=[
            'trifft voll zu',
            'trifft eher zu',
            'weder zutreffend, noch unzutreffend',
            'trifft eher nicht zu',
            'trifft gar nicht zu'
        ],
        widget=widgets.RadioSelect
    )

    qsempathisch = models.StringField(
        label='Sie sind empathisch mit denjenigen, die Unterstützung benötigen.',
        choices=[
            'trifft voll zu',
            'trifft eher zu',
            'weder zutreffend, noch unzutreffend',
            'trifft eher nicht zu',
            'trifft gar nicht zu'
        ],
        widget=widgets.RadioSelect
    )

    qsUnterstuetzung = models.StringField(
        label='Sie fühlen intensiv, was Andere fühlen.',
        choices=[
            'trifft voll zu',
            'trifft eher zu',
            'weder zutreffend, noch unzutreffend',
            'trifft eher nicht zu',
            'trifft gar nicht zu',
        ],
        widget=widgets.RadioSelect
    )

    qsTroesten = models.StringField(
        label='Sie versuchen diejenigen zu trösten, die traurig sind.',
        choices=[
            'trifft voll zu',
            'trifft eher zu',
            'weder zutreffend, noch unzutreffend',
            'trifft eher nicht zu',
            'trifft gar nicht zu'
        ],
        widget=widgets.RadioSelect
    )

    qsLage = models.StringField(
        label='Sie können sich gut in die Lage derer versetzen, die sich unwohl fühlen.',
        choices=[
            'trifft voll zu',
            'trifft eher zu',
            'weder zutreffend, noch unzutreffend',
            'trifft eher nicht zu',
            'trifft gar nicht zu'
        ],
        widget=widgets.RadioSelect
    )

    qsDasein = models.StringField(
        label='Sie versuchen für diejenigen da zu sein, die Unterstützung benötigen.',
        choices=[
            'trifft voll zu',
            'trifft eher zu',
            'weder zutreffend, noch unzutreffend',
            'trifft eher nicht zu',
            'trifft gar nicht zu'
        ],
        widget=widgets.RadioSelect
    )

    qcErkrankti = models.StringField(
        label='Sind Sie schon einmal an COVID-19 erkrankt?',
        choices=[
            'Ja, milder Verlauf',
            'Ja, schwerer Verlauf',
            'Nein'
        ],
        widget=widgets.RadioSelect
    )

    qcErkranktf = models.StringField(
        label='Ist ein Familienmitglied schon einmal an COVID-19 erkrankt?',
        choices=[
            'Ja, milder Verlauf',
            'Ja, schwerer Verlauf',
            'Nein'
        ],
        widget=widgets.RadioSelect
    )

    q1 = models.StringField(
        label='Haben Sie Ihre Kontakte in den letzten 14 Tagen bewusst reduziert?',
        choices=[
            'trifft voll zu',
            'trifft eher zu',
            'weder zutreffend, noch unzutreffend',
            'trifft eher nicht zu',
            'trifft gar nicht zu'
        ],
        widget=widgets.RadioSelect
    )

    qcMaske = models.StringField(
        label='Haben Sie in den letzten 14 Tagen <strong>freiwillig, über die geltenden '
              'Corona-Maßnahmen hinaus,</strong> </br>eine medizinische Maske getragen? '
              '<i>(z.B. in Fußgängerzonen, bei privaten Treffen)</i>',
        choices=[
            'trifft voll zu',
            'trifft eher zu',
            'weder zutreffend, noch unzutreffend',
            'trifft eher nicht zu',
            'trifft gar nicht zu'
        ],
        widget=widgets.RadioSelect
    )

    qcTesten = models.StringField(
        label='Haben Sie sich in den letzten 14 Tagen <strong> freiwillig, über die geltenden Corona-Maßnahmen '
              'hinaus, </strong> </br> auf Covid-19 testen lassen? <i>'
              '(z.B. PCR/Schnelltest vor oder nach einem privaten Treffen) </i>',
        choices=[
            'trifft voll zu',
            'trifft eher zu',
            'weder zutreffend, noch unzutreffend',
            'trifft eher nicht zu',
            'trifft gar nicht zu'
        ],
        widget=widgets.RadioSelect
    )

    q2 = models.StringField(
        label='Ich habe mich am ehesten impfen lassen, weil...',
        choices=[
            'ich mich selbst schützen möchte.',
            'ich Andere schützen möchte.',
            'ich am öffentlichen Leben teilnehmen möchte.',
            'ich Angst hatte im privaten Umfeld ausgeschlossen zu werden.',
            'Ich habe mich nicht impfen lassen.',
        ],
        widget=widgets.RadioSelect
    )

    qcMasnahmen = models.StringField(
        label='Welche der folgenden Aussagen trifft am ehesten auf Sie zu: </br>'
              'Ich habe mich in den letzten 14 Tagen an die geltenden Corona-Maßnahmen gehalten, weil...',
        choices=[
            'es mich nicht stört, mich an die geltenden Maßnahmen zu halten.',
            'ich mich schützen möchte.',
            'ich meine Familie/Freunde schützen möchte.',
            'ich die Allgemeinheit schützen möchte.',
            'ich kein Bußgeld zahlen möchte.',
            'sich Andere auch daran halten.',
            'Ich halte mich nicht an die geltenden Regelungen.',
        ],
        widget=widgets.RadioSelect
    )

    taler = models.IntegerField(
        label='',
        min=0
    )

    Alter = models.IntegerField(
        label='Bitte geben Sie Ihr Alter in Jahren an.'
    )

    Geschlecht = models.StringField(
        label='Bitte geben Sie Ihr Geschlecht an.',
        choices=[
            'Weiblich',
            'Männlich',
            'Divers'
        ],
        widget=widgets.RadioSelect
    )

    Fakultaet = models.StringField(
        label='Welcher Fakultät gehört Ihr Studiengang an?',
        choices=[
            'Betriebswirtschaft',
            'Erziehungswissenschaften',
            'Geisteswissenschaften',
            'Mathematik, Informatik und Naturwissenschaften',
            'Medizin',
            'Rechtswissenschaften',
            'Psychologie und Bewegungswissenschaft',
            'Wirtschafts- und Sozialwissenschaften',
            'sonstige',
        ],
        widget=widgets.RadioSelect
    )

    Bildung = models.StringField(
        label='Bitte geben Sie Ihren höchsten Bildungsabschluss an.',
        choices=[
            'Mittlere Reife',
            '(Fach)Hochschulreife',
            'Hochschulabschluss Bachelor',
            'Hochschulabschluss Master oder höher',
        ],
        widget=widgets.RadioSelect
    )

    Erwerbstaetigkeit = models.StringField(
        label='Bitte geben Sie Ihr derzeitiges Anstellungsverhältnis an.',
        choices=[
            'Minijob',
            'Werkstudent:in',
            'Teilzeit',
            'Vollzeit',
            'derzeitig gehe ich keiner Erwerbstätigkeit nach',
        ],
        widget=widgets.RadioSelect
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
        'q2',
        'qsUnterstuetzung',
        'qsTroesten',
        'qsLage',
        'qsDasein',
        'qcErkrankti',
        'qcErkranktf',
        'qsempathisch',
        'qcMaske',
        'qcTesten',
        'qshelfen',
        'qcMasnahmen',
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
        'Alter',
        'Geschlecht',
        'Bildung',
        'Fakultaet',
        'Erwerbstaetigkeit',
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
    Questionnaire02,
    Payment
]
