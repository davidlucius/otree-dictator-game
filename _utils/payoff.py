
def get_points_per_real_world_currency_unit(p):
    return round(1 / p.session.config['real_world_currency_per_point'])


def get_endowment_in_points(p):
    return get_points_per_real_world_currency_unit(p) * p.session.config['endowment_in_real_world_currency']


def get_points_from_partner_in_winning_dec(p):
    return get_endowment_in_points(p) - p.in_round(p.session.winning_dec).get_others_in_group()[0].taler
