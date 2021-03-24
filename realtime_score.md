# Compute score in near real time


## Thoughs on optimizations

> "Premature optimization is the root of all evil"

We could indeed try write a pretty complex sql query that would follow relationships, 
and compute a derived column being the sum of the card bonuses times the player score. 
It'd be wildly ineficient. So optimizations are required.

But I'd really advise to mesure things before trying to optimize them. Optimizations 
ALWAYS come with trade offs / limitations, but are not always faster for every cases.

In computing you can otpimize for time / cpu usage / storage usage. 
In order to decrease one you'll have to increase the other two.

In order to speed up this, the tools we can use are:
- denormalization
- precomputations
- caching
- distributed computations

## 

> Team Score = ∑ PlayerCard[i].bonus * getTournamentScore(PlayerCard[i].player)


Rather than recompute the score of all teams all the time, we only need to adjust the score of the teams in the current tournament that contains cards of the player whose stats have changed.
And we can only adjust the team score by the delta of the player score times the bonus of their card.

The list of teams is constant during a tournament, so we can compute a key value store of 
`{[key: playerId]: Team[]}"` at the begining of the tournament, and use it from there on.
Redis is a great tool for this kind of things

Last point the ranking of teams is only updated when a team score change, so we can also
store this in cache and avoid recomputing it all the time. But putting the score in an
indexed column of our Team model is probably sufficient to begin with.

## Strategy

player stat update => trigger async player update task

```python
def on_player_stat_change(tounrnament_id, player_id, new_score):
    """
    when polling stats and some data change, we call this method with the new score for the player
    """
    playerStats = PlayerTournamentStats.objects.get_or_create(player=player_id, tournament=tounrnament_id)
    delta_score = new_score - playerStats.score
    playerStats.score = new_score
    playerStats.save()

    # trigger async code
    async_player_update(player_id, delta_score)



# Async task in worker
def async_player_update(player_id, delta_score):
    for team_id in get_teams_in_tournament_that_contains_this_player(player_id):
      async_update_team_score(team_id, player_id, delta_score)

# Async task in worker
# We could combine those two task, but it might get too long to execute. I'd rather have multiple small ones
def async_update_team_score(team_id, player_id, delta_score):
    team = Team.objects.get_by_id(team_id)
    
    # We could also cache those to make it quicker. A redis key/value store could do wonder there
    player_card = team.player_cards.filter(id=player_id)

    # update score to reflect player new stats
    team.score += delta_score * player_card.bonus

    team.save()
```

From there we can get a sorted list of teams per league by doing :

```python
Team.objects.filter(league=league_id).order_by('-score', '-creation_date')
```

## Tradeoff

By doing this denormalization we would end up with a wrong score if some message were 
not delivered, or delivered multiple times

Whenever I implement such optimized path, I also like to have a dumb & slow way to force 
exact recomputations from scratch if something went wrong during the way.