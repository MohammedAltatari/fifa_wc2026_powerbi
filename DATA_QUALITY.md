# Data Quality Findings

The source is one CSV file: **54,600 rows × 75 columns**, one row per player per match, no missing values. "No missing values" did not mean "no problems". These are the issues found while profiling the file in Python before building the model, and how each one was handled.

## 1. Unused substitutes are in the data

- **Finding:** 23,042 rows (42%) have `minutes_played = 0`. Their `player_rating` is 0, but they still carry values such as `stamina_score` (average 74.9).
- **Risk:** a simple average would pull the average rating down from 6.29 to 3.63 and mix non-players into physical metrics.
- **Decision:** added `is_appearance` (minutes > 0) in Power Query. Appearances, average rating, top speed and stamina are calculated only where the player actually played. Totals and per-90 rates are unaffected because 0 minutes add nothing.

## 2. Team score does not equal the sum of player goals

- **Finding:** `goals_team` matches the sum of the team's player `goals` in only 575 of 2,100 team-matches (27%). Overall, player goals add up to 3,024 while the match scores add up to 2,794.
- **Decision:** two fact tables. Team and tournament goals come from the match score (`Fact_TeamMatch`), player goals from player rows (`Fact_PlayerMatch`). The two measures have different names (`Total Goals` vs `Goals`) so they are never mixed.
- **Checked:** `match_result` is fully consistent with `goals_team` / `goals_opponent`, and every match has two mirrored team rows.

## 3. Pre-calculated ratio columns disagree with their own inputs

| Column | Matches its formula | Decision |
|---|---|---|
| `pass_accuracy` = successful / total passes | 22% of rows | Dropped; `Pass Accuracy %` recalculated from summed passes |
| `save_percentage` = saves / (saves + goals conceded) | 6% of goalkeeper rows | Dropped; `Save %` recalculated |

Recalculating from the components is also the correct way to aggregate: an average of per-match percentages over-weights matches with few passes.

## 4. "Tournament total" columns are not stable

- **Finding:** `total_goals_tournament`, `total_assists_tournament`, `total_minutes_tournament` and `tournament_rating` change between rows of the same player (1,102 players affected). `player_of_match_awards` changes for 666 players and sums to as many as 7 awards in a single match.
- **Decision:** all excluded. Every tournament total is calculated in DAX from the per-match columns.

## 5. Expected goals (xG) are on a different scale

- **Finding:** actual goals are **3.18×** total xG (2,794 goals vs 879.7 xG).
- **Decision:** xG is kept for relative comparison only (which team creates more), not to judge finishing quality.

## 6. Uneven number of matches per team

- **Finding:** teams played between 33 and 66 matches.
- **Decision:** teams are compared with rates (win %, points per match, goals per match), never with totals.

## 7. Tournament structure is not realistic

- **Finding:** 1,050 matches (the real 2026 tournament has 104). Stage dates are not sequential: "Final" matches occur from 15 June to 30 July. 119 knockout matches, including 4 finals, ended in a draw, and there is no penalty shoot-out data.
- **Decision:** results are shown as recorded; stages are ordered by a `Stage Order` column instead of a date axis. The report and README label the data as simulated.

## 8. Duplicate player names

- **Finding:** 1,248 player IDs but 1,245 names. Three pairs of team-mates share the same name.
- **Decision:** `Player Label` adds the shirt number only for duplicated names (for example `Kalidou Mendy #5` and `Kalidou Mendy #2`), so every label in slicers and charts is unique.

## 9. Minor goalkeeper inconsistencies

- **Finding:** goalkeeper `goals_conceded` matches the team's goals against in 94.5% of team-matches, and `clean_sheet` in 98.4%.
- **Decision:** team clean sheets use the match score; goalkeeper clean sheets and saves use the goalkeeper columns. Both are labelled separately.

## What was confirmed clean

- Player attributes (age, position, club, market value…) are constant across all of a player's rows.
- Match attributes (date, stadium, stage) are constant within a match, and each stadium maps to one city.
- No duplicate player-match rows; exactly 26 players per team per match, and exactly one goalkeeper with minutes per team-match.
