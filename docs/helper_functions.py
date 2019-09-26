def gen_offensive_outcome_probabilities(dampening=1):
    # League average stats courtesy of Fangraphs
    # https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=0&season=2019&month=0&season1=2019&ind=0&team=0,ss&rost=0&age=0&filter=&players=0&startdate=2019-01-01&enddate=2019-12-31

    _pa = 184578 + 185295 + 185139
    _1b = (27538 + 26918 + 26322) * dampening
    _2b = (8255 + 8397 + 8264) * dampening
    _3b = (873 + 795 + 847) * dampening
    _hr = (5610 + 6105 + 5585) * dampening
    _k  = 38983 + 40104 + 41207
    _bb = (15088 + 15829 + 15686) * dampening


    _batted_ball_outs = _pa - _1b - _2b - _3b - _hr - _k - _bb
    _GO_pct = .429
    _FO_pct = .357
    _go = (_GO_pct/(_GO_pct+_FO_pct)) * _batted_ball_outs
    _fo = (_FO_pct/(_GO_pct+_FO_pct)) * _batted_ball_outs

    _fo_that_are_sf3 = 0 # .80
    _sf_out3 = 0.10 *  _fo_that_are_sf3
    _sf_safe3 = _fo_that_are_sf3 - _sf_out3

    lg_avg_stats = {
        "1B": _1b / _pa,
        "2B": _2b / _pa,
        "3B": _3b / _pa,
        "HR": _hr / _pa,
        "K": _k / _pa,
        "BB": _bb / _pa,
        "GO": _go / _pa,
        "FO": _fo / _pa,
    }
    lg_avg_stats_extra = {
        "_SF3": {'safe': _sf_safe3, 'out': _sf_out3}
    }
    return lg_avg_stats, lg_avg_stats_extra
