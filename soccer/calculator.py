def calc_points(bet):
    """ calculate the points for a bet """
    points = 0
    if bet.bet == bet.match.result:
        points += 1
    return points


'''
if($score->homeEval() == $bet->homeEval()) {
        $points += $tendency;

        if(($score->mHome == $bet->mHome) && ($score->mAway == $bet->mAway)) {
                $points += $exact;
        }
}
'''
