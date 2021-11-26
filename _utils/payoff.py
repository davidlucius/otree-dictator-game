
def get_points_per_real_world_currency_unit(p):
    return round(1 / p.session.config['real_world_currency_per_point'])


def get_endowment_in_points(p):
    return get_points_per_real_world_currency_unit(p) * p.session.config['endowment_in_real_world_currency']


def get_points_from_partner_in_winning_dec(p):
    return get_endowment_in_points(p) - p.in_round(p.session.winning_dec).get_others_in_group()[0].taler


def get_payoff(p, options):
    if p.role == 'dictator':
        if p.round_number == 1 or p.subsession.vaccination_coverage_is_reached:
            return get_endowment_in_points(p) + options[p.group.appointment]['amount']
        else:
            return p.session.config['failure_payoff_in_points']
    if p.role == 'recipient':
        if p.vaccinated:
            if p.round_number == 1 or p.subsession.vaccination_coverage_is_reached:
                return get_endowment_in_points(p)
            else:
                return p.session.config['failure_payoff_in_points']
    return 0
