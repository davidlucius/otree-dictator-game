from otree.api import *
from settings import (POINTS_CUSTOM_NAME)
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
    amounts_2 = {counter: amount for counter, amount in enumerate(range(20, -1, -2), start=1)}
    probabilities = {counter: probability for counter, probability in enumerate(range(100, -1, -20), start=1)}


def get_options():
    options = zip(Constants.amounts.items(), Constants.probabilities.items())
    return {i: {'amount': amount, 'probability': probability} for (i, amount), (_, probability) in options}


def get_options_2():
    options = zip(Constants.amounts_2.items(), Constants.probabilities.items())
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
        return round(self.session.config['min_vaccination_coverage'] * self.num_players - self.num_dictators)

    @property
    def req_vaccinated_recipients(self):
        return round(self.session.config['min_vaccination_coverage'] * self.num_players)

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

    helfen = models.StringField(
        label='Ich versuche Anderen zu helfen.',
        choices=[
            'Nie',
            'Fast nie',
            'Ab und zu',
            'Fast immer',
            'Immer'
        ],
        widget=widgets.RadioSelect
    )

    empatie = models.StringField(
        label='Ich bin empathisch gegenüber Menschen, die in Not sind.',
        choices=[
            'Nie',
            'Fast nie',
            'Ab und zu',
            'Fast immer',
            'Immer'
        ],
        widget=widgets.RadioSelect
    )

    fuehlen = models.StringField(
        label='Ich fühle intensiv, was andere fühlen.',
        choices=[
            'Nie',
            'Fast nie',
            'Ab und zu',
            'Fast immer',
            'Immer'
        ],
        widget=widgets.RadioSelect
    )

    lage = models.StringField(
        label='Ich kann mich gut in die Lage derer versetzen, die sich unwohl fühlen.',
        choices=[
            'Nie',
            'Fast nie',
            'Ab und zu',
            'Fast immer',
            'Immer'
        ],
        widget=widgets.RadioSelect
    )

    unterstuetzung = models.StringField(
        label='Ich versuche für diejenigen, die Unterstützung brauchen, da zu sein und mich um sie zu kümmern.',
        choices=[
            'Nie',
            'Fast nie',
            'Ab und zu',
            'Fast immer',
            'Immer'
        ],
        widget=widgets.RadioSelect
    )

    troesten = models.StringField(
        label='Ich versuche diejenigen zu trösten, die traurig sind.',
        choices=[
            'Nie',
            'Fast nie',
            'Ab und zu',
            'Fast immer',
            'Immer'
        ],
        widget=widgets.RadioSelect
    )

    # Screen: Questionnaire01
    belief_d_1 = models.StringField(
        label='Was glauben Sie, welchen Termin die anderen Teilnehmer in der gleichen Entscheidungssituation '
              'gewählt haben?',
        choices=['Termin 1: frühester', 'Termin 2', 'Termin 3', 'Termin 4', 'Termin 5', 'Termin 6: spätester']
    )

    # Screen: Questionnaire01
    belief_e_1 = models.StringField(
        label='Was glauben Sie, für welchen Termin hat sich ihr Gegenüber entschieden?',
        choices=['Termin 1: frühester', 'Termin 2', 'Termin 3', 'Termin 4', 'Termin 5', 'Termin 6: spätester']
        # choices=[f'Termin {i}' for i in range(1, len(get_options()) + 1)]
    )

    # Screen: Questionnaire01
    belief_d_2 = models.StringField(
        label='Wie bewerten Sie ihre eigene Entscheidung?',
        choices=[
            'Sehr eigennützig',
            'Eher eigennützig',
            'Weder eigennützig noch großzügig',
            'Eher großzügig',
            'Sehr großzügig'
        ]
    )

    # Screen: Questionnaire01
    belief_e_2 = models.StringField(
        label='Was vermuten Sie, wie Ihr Gegenüber entschieden hat?',
        choices=[
                 'Sehr eigennützig',
                 'Eher eigennützig',
                 'Weder eigennützig noch großzügig',
                 'Eher großzügig',
                 'Sehr großzügig'
             ]
    )

    ###################################
    # Questionnaire 2
    ###################################

    # Q1
    # Screen: Questionnaire02_p1
    entscheidung = models.StringField(
        label='Haben Sie bei Ihrer Terminwahl die von Ihnen erwartete Entscheidung der anderen Teilnehmer '
              'miteinbezogen?',
        choices=[
            'Ja',
            'Nein',
            'Weiß nicht'
        ],
        widget=widgets.RadioSelect
    )

    # Q2
    # Screen: Questionnaire02_p2
    age = models.IntegerField(
        label='Wie alt sind Sie?',
        min=18,
        max=99
    )

    # Q3
    # Screen: Questionnaire02_p2
    gender = models.StringField(
        label='Bitte geben Sie Ihr Geschlecht an.',
        choices=[
            'Männlich',
            'Weiblich',
            'Divers'
        ],
        widget=widgets.RadioSelect
    )

    # Q4
    # Screen: Questionnaire02_p2
    fakultaet = models.StringField(
        label='Welcher Fakultät gehören Sie an?',
        choices=[
            'Fakultät für Rechtswissenschaft',
            'Fakultät für Wirtschafts- und Sozialwissenschaften',
            'Medizinische Fakultät',
            'Fakultät für Erziehungswissenschaft',
            'Fakultät für Geisteswissenschaften',
            'Fakultät für Mathematik, Informatik und Naturwissenschaften',
            'Fakultät für Psychologie und Bewegungswissenschaft',
            'Fakultät für Betriebswirtschaft'
        ],
        widget=widgets.RadioSelect
    )

    # Q5
    # Screen: Questionnaire02_p2
    erkrankt = models.StringField(
        label='Waren oder sind Sie nachweislich (positiver PCR Test oder positiver Schnelltest) an Covid - 19 '
              'erkrankt?',
        choices=[
            'Ja, als ich ungeimpft war',
            'Ja, als ich geimpft war',
            'Nein'
        ],
        widget=widgets.RadioSelect
    )

    # Q6
    # Screen: Questionnaire02_p3
    # krankheitsverlauf = models.StringField(
    #     label='Wie beschreiben Sie Ihren Krankheitsverlauf am ehesten?',
    #     choices=[
    #         'Asymptomatisch',
    #         'Leichte grippeähnliche Symptome',
    #         'Schwerer Verlauf',
    #         'Intensivstation'
    #     ]
    # )

    # Q6 multiple options
    # Screen: Questionnaire02_p3
    verlauf_asymptomatisch = models.BooleanField(
        label='Asymptomatisch',
        widget=widgets.CheckboxInput,
        blank=True)
    verlauf_leicht = models.BooleanField(
        label='Leichte grippeähnliche Symptome',
        widget=widgets.CheckboxInput,
        blank=True)
    verlauf_schwer = models.BooleanField(
        label='Schwerer Verlauf',
        widget=widgets.CheckboxInput,
        blank=True)
    verlauf_longcovid = models.BooleanField(
        label='Long Covid',
        widget=widgets.CheckboxInput,
        blank=True)
    verlauf_intensiv = models.BooleanField(
        label='Intensivstation',
        widget=widgets.CheckboxInput,
        blank=True)

    # Q7
    # Screen: Questionnaire02_p3
    # longcovid = models.StringField(
    #     label='Haben/Hatten Sie Long-Covid Beschwerden?',
    #     choices=[
    #         'Ja',
    #         'Nein'
    #     ],
    #     widget=widgets.RadioSelect
    # )

    # Q8
    # Screen: Questionnaire02_p4
    real_vaccinated = models.StringField(
        label='Sind Sie gegen Sars-Cov-2 geimpft?',
        choices=[
            'Ja',
            'Nein'
        ],
        widget=widgets.RadioSelect
    )

    # Q9
    # Screen: Questionnaire02_p5
    boosterBereit = models.StringField(
        label='Wären Sie aktuell oder zukünftig bereit für eine Auffrischungsimpfung?',
        choices=[
            'Ja',
            'Ich habe meine Auffrischungsimpfung (Booster) bereits erhalten',
            'Nein'
        ],
        widget=widgets.RadioSelect
    )

    # Q10
    # Screen: Questionnaire02_p5
    wichtigkeit = models.StringField(
        label='Wie wichtig war es Ihnen, zeitnah eine Erstimpfung zu erhalten?',
        choices=[
            'Sehr wichtig',
            'Wichtig',
            'Neutral',
            'Eher unwichtig',
            'Unwichtig'
        ],
        widget=widgets.RadioSelect
    )

    # Q11
    # Screen: Questionnaire02_p5
    warumImpf_eigen = models.BooleanField(
        label='Eigenschutz',
        widget=widgets.CheckboxInput,
        blank=True)

    warumImpf_vorerkrankt = models.BooleanField(
        label='Ich habe coronarelevante Vorerkrankungen (z.B. Asthma, Diabetes, etc.,...)',
        widget=widgets.CheckboxInput,
        blank=True)

    warumImpf_umfeld = models.BooleanField(
        label='Schutz meines persönlichen Umfeldes',
        widget=widgets.CheckboxInput,
        blank=True)
    warumImpf_vuln = models.BooleanField(
        label='Schutz vulnerabler Gruppen',
        widget=widgets.CheckboxInput,
        blank=True)
    warumImpf_gesundsys = models.BooleanField(
        label='Schutz des Gesundheitssystems vor Überlastung',
        widget=widgets.CheckboxInput,
        blank=True)
    warumImpf_freiheit = models.BooleanField(
        label='Um persönliche Freiheiten zurückzuerhalten',
        widget=widgets.CheckboxInput,
        blank=True)
    warumImpf_sozial = models.BooleanField(
        label='Druck durch soziales Umfeld',
        widget=widgets.CheckboxInput,
        blank=True)
    warumImpf_politik = models.BooleanField(
        label='Druck durch Politik (politische Maßnahmen wie 2G Zugangsbeschränkungen)',
        widget=widgets.CheckboxInput,
        blank=True)
    warumImpf_impfpflicht = models.BooleanField(
        label='Vermutete Impfpflicht (Allgemein und/oder Berufsspezifisch)',
        widget=widgets.CheckboxInput,
        blank=True)
    warumImpf_angebot = models.BooleanField(
        label='Angebot bekommen',
        widget=widgets.CheckboxInput,
        blank=True)
    warumImpf_mutant = models.BooleanField(
        label='Mutanten (z.B. Delta oder Omikron)',
        widget=widgets.CheckboxInput,
        blank=True)
    warumImpf_sonst = models.BooleanField(
        label='Sonstiges',
        widget=widgets.CheckboxInput,
        blank=True)

    # Q11 prelim
    # Screen: Questionnaire02_p5
    # warumGeimpft = models.StringField(
    #     label='Was waren die Hauptgründe für Ihre Impfung?',
    #     choices=[
    #         'Eigenschutz',
    #         'Schutz meines persönlichen Umfeldes',
    #         'Schutz vulnerabler Gruppen',
    #         'Schutz des Gesundheitssystems vor Überlastung',
    #         'Um persönliche Freiheiten zurückzuerhalten',
    #         'Druck durch soziales Umfeld ',
    #         'Druck durch Politik (politische Maßnahmen wie 2G Zugangsbeschränkungen)',
    #         'Vermutete Impfpflicht (Allgemein und/oder Berufsspezifisch)',
    #         'Angebot bekommen',
    #         'Mutanten (z.B. Delta oder Omikron)',
    #         'Sonstiges'
    #     ]
    # )

    # Q12
    # Screen: Questionnaire02_p6
    erstImpfen = models.StringField(
        label='Beabsichtigen Sie, sich in den nächsten 4 Wochen erst-impfen zu lassen?',
        choices=[
            'Ja',
            'Nein'
        ],
        widget=widgets.RadioSelect
    )

    # Q13
    # Screen: Questionnaire02_p6
    gegenImpfung_sozial = models.BooleanField(
        label='Druck durch soziales Umfeld',
        widget=widgets.CheckboxInput,
        blank=True)
    gegenImpfung_politik = models.BooleanField(
        label='Druck durch Politik',
        widget=widgets.CheckboxInput,
        blank=True)
    gegenImpfung_nebenwirkung = models.BooleanField(
        label='Angst vor Nebenwirkungen (z.B. Kopfschmerzen, Herzmuskelentzündungen, Hirnvenenthrombose, etc.)',
        widget=widgets.CheckboxInput,
        blank=True)
    gegenImpfung_langzeitfolgen = models.BooleanField(
        label='Angst vor Langzeitfolgen',
        widget=widgets.CheckboxInput,
        blank=True)
    gegenImpfung_altImpfstoff = models.BooleanField(
        label='Warten auf alternative Impfstoffe',
        widget=widgets.CheckboxInput,
        blank=True)
    gegenImpfung_glauben = models.BooleanField(
        label='Ich glaube nicht an den schützenden Effekt der Impfung',
        widget=widgets.CheckboxInput,
        blank=True)
    gegenImpfung_nichtMoeglich = models.BooleanField(
        label='Aus gesundheitlichen Gründen kann ich mich nicht impfen lassen',
        widget=widgets.CheckboxInput,
        blank=True)
    gegenImpfung_keinTermin = models.BooleanField(
        label='Ich habe bisher kein Termin vereinbart',
        widget=widgets.CheckboxInput,
        blank=True)
    gegenImpfung_sonst = models.BooleanField(
        label='Sonstiges',
        widget=widgets.CheckboxInput,
        blank=True)
    gegenImpfung_erprobt = models.BooleanField(
        label='Der Impfstoff ist noch nicht ausreichend erprobt',
        widget=widgets.CheckboxInput,
        blank=True)

    # Q14
    # Screen: Questionnaire02_p7
    moeglich = models.StringField(
        label='Sind Sie der Meinung, dass jede volljährige Person die Möglichkeit hatte, sich impfen zu lassen '
              '(wenn medizinisch möglich)?',
        choices=[
            'Ja',
            'Nein',
            'Keine Meinung'
        ],
        widget=widgets.RadioSelect
    )

    # Q16
    # Screen: Questionnaire02_p7
    richtigeKonzept = models.StringField(
        label='Das richtige Konzept für die Eindämmung der Pandemie in den kommenden Monaten in Freizeit, '
              'Kultur und Einzelhandel ist …',
        choices=[
            '3G (Geimpft, Genesen, Getestet: PCR oder Antigentest)',
            '2G (Geimpft und Genesen)',
            '2G+ (Geimpft, Genesen und zusätzlich getestet oder Genesen/geimpfte Personen, die ihre Auffrischimpfung '
            'erhalten haben)',
            'Lockdown',
            'Allgemeine Impfpflicht für volljährige Personen (bei denen dies medizinisch möglich ist)',
            'Keinerlei Maßnahmen',
            'Sonstiges'
        ],
        widget=widgets.RadioSelect
    )

    # Q18
    # Screen: Questionnaire02_p7
    impfpflicht = models.StringField(
        label='Wie stehen Sie zu einer Impfpflicht?',
        choices=[
            'Ich befürworte eine allgemeine Impfpflicht (für Personen über 18 Jahren und wenn medizinisch möglich)',
            'Ich befürworte eine Impfpflicht für bestimmte Berufsgruppen mit Kontakt zu vulnerablen Personen',
            'Lehne ich ab',
            'Keine Meinung'
        ],
        widget=widgets.RadioSelect
    )

    # Q21
    # Screen: Questionnaire02_p7
    risiko3Mo = models.StringField(
        label='Wie hoch schätzen Sie derzeit Ihr Risiko ein, sich in den kommenden 3 Monaten mit Sars-Cov-2 '
              'zu infizieren?',
        choices=[
            'Sehr hoch',
            'Hoch',
            'Mittel',
            'Niedrig',
            'Sehr niedrig'
        ],
        widget=widgets.RadioSelect
    )

    # Q22
    # Screen: Questionnaire02_p7
    assozHerdImmun = models.StringField(
        label='Was assoziieren Sie vorwiegend mit Herdenimmunität?',
        choices=[
            'Rückgewinnung von persönlicher Freiheit',
            'Schutz von medizinisch nicht impfbaren Gruppen',
            'Rückgewinnung gesellschaftlicher Freiheit in Form der Aufhebung sämtlicher Schutzmaßnahmen',
            'Wirtschaftliche Stabilität',
            'Sonstiges'
        ],
        widget=widgets.RadioSelect
    )

    # Q24
    # Screen: Questionnaire02_p7
    freiwillingEingesch = models.StringField(
        label='Schränken Sie sich bewusst freiwillig ein (bspw. den Verzicht Freunde zu treffen) oder werden Sie '
              'durch politische Maßnahmen unfreiwillig eingeschränkt (bspw. Zwangsschließung der Gastronomie)?',
        choices=[
            'Ich schränke mich freiwillig ein.',
            'Ich werde eher durch politische Maßnahmen eingeschränkt.',
            'Ich werde durch beides gleichermaßen stark eingeschränkt.',
            'Ich fühlte mich aktuell durch die Pandemie in meinem Leben nicht eingeschränkt.'
        ],
        widget=widgets.RadioSelect
    )

    # Q25
    # Screen: Questionnaire02_p7
    extremEingesch = models.StringField(
        label='In welchem Bereich mussten/müssen Sie die für Sie extremsten Einschränkungen in Kauf nehmen?',
        choices=[
            'Beruflich (z.B.: Job verloren, vermindertes Einkommen)',
            'Sozial (z.B.: Ich konnte/kann Freunde und Familie nicht treffen)',
            'Freizeitangebote (z.B.: Ich konnte/kann nicht ins Fitnesscenter/auf Konzerte gehen)',
            'Ich nahm/nehme keine Einschränkungen wahr.',
            'andere/r Bereich/e'
        ],
        widget=widgets.RadioSelect
    )

    # Screen: Questionnaire02
    # ready_for_booster = models.StringField(
    #     label='Sind Sie bereit für eine Auffrischungsimpfung?',
    #     choices=[
    #         'Ja',
    #         'Nein'
    #     ],
    #     widget=widgets.RadioSelect
    # )

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
    # risk_evaluation = models.StringField(
    #       label='Wie hoch schätzen Sie Ihr Risiko ein sich in den kommenden 3 Monaten mit Sars-Cov-2 zu infizieren?',
    #      choices=[
    #          'Sehr groß',
    #          'groß',
    #          'erheblich',
    #         'mäßig',
    #          'gering'
    #     ]
    #  )


def get_partner(player: Player):
    return player.get_others_in_group()[0]


# ----------------------------------------------------------------------------------------------------------------------
# PAGES
# ----------------------------------------------------------------------------------------------------------------------

class Intro01(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Intro02(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            points_per_real_world_currency_unit=c(get_points_per_real_world_currency_unit(player)),
        )

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
            num_other_recipients=player.subsession.num_recipients - 1,
            failure_payoff=c(player.session.config['failure_payoff_in_points']),
            no_herd=player.session.config['failure_payoff_in_points'],
            options_2=get_options_2(),
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
            no_herd=player.session.config['failure_payoff_in_points'],
            options=get_options(),
            options_2=get_options_2(),
            failure_payoff=c(player.session.config['failure_payoff_in_points']),
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


class QuestionnaireProSocial(Page):
    form_model = 'player'
    form_fields = [
        'helfen',
        'empatie',
        'fuehlen',
        'troesten',
        'lage',
        'unterstuetzung'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Questionnaire02P1(Page):
    form_model = 'player'
    form_fields = [
        'entscheidung'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds and player.role == 'dictator'


class Questionnaire02P2(Page):
    form_model = 'player'
    form_fields = [
        'age', 'gender', 'fakultaet', 'erkrankt',
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds


class Questionnaire02P3(Page):
    form_model = 'player'
    form_fields = [
        'verlauf_asymptomatisch',
        'verlauf_leicht',
        'verlauf_schwer',
        'verlauf_intensiv',
        'verlauf_longcovid'

        ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds and (
            player.erkrankt == 'Ja, als ich ungeimpft war' or player.erkrankt == 'Ja, als ich vollständig geimpft war')


class Questionnaire02P4(Page):
    form_model = 'player'
    form_fields = [
        'real_vaccinated'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds


class Questionnaire02P5(Page):
    form_model = 'player'
    form_fields = [
        'warumImpf_eigen',
        'warumImpf_vorerkrankt',
        'warumImpf_umfeld',
        'warumImpf_vuln',
        'warumImpf_gesundsys',
        'warumImpf_freiheit',
        'warumImpf_sozial',
        'warumImpf_politik',
        'warumImpf_impfpflicht',
        'warumImpf_angebot',
        'warumImpf_mutant',
        'warumImpf_sonst',
        'boosterBereit',
        'wichtigkeit'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds and player.real_vaccinated == 'Ja'


class Questionnaire02P6(Page):
    form_model = 'player'
    form_fields = [
        'gegenImpfung_sozial',
        'gegenImpfung_politik',
        'gegenImpfung_nebenwirkung',
        'gegenImpfung_langzeitfolgen',
        'gegenImpfung_altImpfstoff',
        'gegenImpfung_glauben',
        'gegenImpfung_nichtMoeglich',
        'gegenImpfung_keinTermin',
        'gegenImpfung_sonst',
        'gegenImpfung_erprobt',
        'erstImpfen'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds and player.real_vaccinated == 'Nein'


class Questionnaire02P7(Page):
    form_model = 'player'
    form_fields = [
        'moeglich',
        'richtigeKonzept',
        'impfpflicht',
        'risiko3Mo',
        'assozHerdImmun',
        'freiwillingEingesch',
        'extremEingesch'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds


class Questionnaire02(Page):
    form_model = 'player'
    form_fields = [
        # Constants.warumGeimpft,
        'erkrankt',
        'age',
        'gender',
        'fakultaet',
        'real_vaccinated',
        'ready_for_booster',
        'reason_self_protection',
        'reason_environment',
        'reason_herd_immunity',
        'reason_get_back_liberties',
        'reason_pressure',
        'risk_evaluation',
        'boosterBereit',
        'wannGeimpft',
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds


class Questionnaire02a(Page):
    form_model = 'player'
    form_fields = [
        'entscheidung'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds and player.role == 'dictator'


class Questionnaire02b(Page):
    form_model = 'player'
    form_fields = [
        'krankheitsverlauf',
        'longcovid'
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds and (
            player.erkrankt == 'Ja, als ich ungeimpft war' or player.erkrankt == 'Ja, als ich vollständig geimpft war')


class Result(Page):

    @staticmethod
    def vars_for_template(player: Player):
        partner = get_partner(player)
        partner_r1 = partner.in_round(1)

        return dict(
            partner=partner,
            partnerR1=partner_r1,
            endowment_in_points=c(get_endowment_in_points(player)),
            vaccination_coverage_is_reached=player.subsession.vaccination_coverage_is_reached,
            # bloof
            playerR1=player.in_round(1),
            # partnerR1 = playerR1.get_others_in_group()[0]
            # endowment_in_pointsR1 = c(get_endowment_in_points(playerR1)),
            # vaccination_coverage_is_reachedR1 = playerR1.subsession.vaccination_coverage_is_reached
        )

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
    Intro01,
    QuestionnaireProSocial,
    Intro02,
    DecisionInfo,
    Decision,
    Questionnaire01,
    WaitingForPartner,
    WaitingForAll,
    Result,
    Questionnaire02P1,
    Questionnaire02P2,
    Questionnaire02P3,
    Questionnaire02P4,
    Questionnaire02P5,
    Questionnaire02P6,
    Questionnaire02P7,
    Payment
]
